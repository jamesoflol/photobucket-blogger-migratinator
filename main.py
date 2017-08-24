import requests
import json
import re
import sys
import hashlib
import picasa # picasa.py in this folder
from oauth import Oauth # oauth.py in this folder

def list_blogs():
	url = 'https://www.googleapis.com/blogger/v3/users/self/blogs'
	headers = {
		'Authorization': 'Bearer ' + oauth.access_token
	}

	# GET
	# try:
	r = requests.get(url, headers=headers)
	r.raise_for_status() # Raise an exception if HTTP status code not 2xx
	# except Exception as err:
	# 	print(err)
	# 	sys.exit(1)

	# Get blog urls and ids	
	json_obj = json.loads(r.text)

	return json_obj['items']


# Recursive function, recurses through paginated results, 10 posts per page.
def list_posts(blog_id, page_token=None, page_num=0):
	url = "https://www.googleapis.com/blogger/v3/blogs/{0}/posts".format(blog_id)
	headers = {
		'Authorization': 'Bearer ' + oauth.access_token
	}
	params = {
		'pageToken': page_token
	}

	# HTTP GET
	r = requests.get(url, headers=headers, params=params, timeout=10)
	r.raise_for_status() # Raise an exception if HTTP status code not 2xx
	#print('http status: ' + str(r.status_code))
	#print(r.text)

	# Get json from result
	json_obj = json.loads(r.text)
	# Get list from json
	if 'items' in json_obj:
		results = json_obj['items']
	else:
		results = []
	#print("Got page {0}.".format(page_num))

	# Looks for another page of results
	nextPageToken = None
	try:
		nextPageToken = json_obj['nextPageToken']
	except:
		pass

	if nextPageToken:
		# Recurse this function to get the next page of results
		print("Page {0} done. Found approx {1} posts so far. On to page ID: {2}".format(page_num, page_num*10+len(results), nextPageToken))
		next_results = list_posts(blog_id, nextPageToken, page_num+1)

		# Combine the recursed function's results with this one in to mega result
		for item in next_results:
			results.append(item)
	else:
		print('No more pages. All done.')

	return results


# Update a single post 
# Params:
# - post: dict var from json_obj['items']. post keys = content, url, id, etc.
def edit_post(post, quiet=False, is_retry=0):
	try:
		# Find all urls in post content
		regexString = "(?:'|\")(https*:\/\/.+?)(?:'|\")" # Finds URLs
		all_urls = re.findall(regexString, post['content'])

		# Filter for just the photobucket.com image links
		photobucket_urls = []
		allowed_suffixes = ('png','PNG','jpg','JPG','jpeg','JPEG','bmp','BMP','gif','GIF') # This is all Picasa allows
		for url in all_urls:
			if 'photobucket.com/' in url and url.endswith(allowed_suffixes):
				#print('Found URL: ' + url)
				if "https://" in url:
					url = url.replace("https://", "http://")
					#print('Replacing with: ' + url) # Some posts have both a HTTPS img src and a HTTPS link
				photobucket_urls.append(url)

		photobucket_photos_de_duped = list(set(photobucket_urls))

		# For each image, download from photobucket, upload to picasa, and update the image link in the post content (local, in memory)
		for url in photobucket_photos_de_duped:
			# Download image from photobucket
			headers = {
				'Referer': url + '.html'
			}
			r = requests.get(url, headers=headers, timeout=5)
			if r.status_code == 404:
				raise Exception("Photobucket download error 404.")
			r.raise_for_status()
			image_binary = r.content

			# Check to make sure we haven't accidentally downloaded the photobucket pay-up notice image
			md5_hash = hashlib.md5(image_binary).hexdigest()
			if md5_hash == 'aafa26a6610d377d8e42f44bc7e76635':
				raise Exception("It looks like something's gone wrong and we've accidentally downloaded the photobucket pay-up notice image.")

			# Upload image to picasa
			filename = url.split("/")[-1:][0] # Grabs everythign after the last slash
			google_image_url = picasa.upload_image_to_picasa(oauth.access_token, image_binary, filename, photo_album_id)

			# Update URLs in blog post content from photobucket to google
			post['content'] = post['content'].replace(url, google_image_url)
			# Also update the httpS version of any such url
			post['content'] = post['content'].replace(url.replace("http://","https://"), google_image_url)

		# Were any photos updated locally? If so, update the Blogger post
		if len(photobucket_photos_de_duped) > 0:
			# Save content changes
			url = "https://www.googleapis.com/blogger/v3/blogs/{0}/posts/{1}".format(blog_id, post['id'])
			headers = {
				'Authorization': 'Bearer ' + oauth.access_token,
				'Content-Type': 'application/json'
			}
			data_obj = dict()
			data_obj['content'] = post['content']
			data = json.dumps(data_obj)
			# HTTP PATCH (Just editing one value, rather than PUT which replaces all)
			r = requests.patch(url, headers=headers, data=data, timeout=5)
			r.raise_for_status() # Raise an exception if HTTP status code not 2xx

			print('Saved changes. See result at: ' + post['url'])

			return True

		else:
			if not quiet:
				print('No changes at: ' + post['url'])

			return False

	except Exception as err:
		if is_retry > 1:
			print("ERROR ON RETRY: {0}. Skipping this post: {1}".format(err, post['url']))
			if type(err) == requests.exceptions.HTTPError:
				print("Error reason: " + err.response.text)
			return False

			# else:
			# 	# Print err and exit
			# 	print("ERROR ON RETRY: {0}. Post {1}".format(err, post['url']))
			# 	print("Exiting.")
			# 	raise

		else:
			# Attempt to fix the error, and try this post again
			if type(err) == requests.exceptions.HTTPError:
				if err.response.text == "Photo limit reached.":
					# Set photo_album_id to that of the next 'migratinator' album in the list
					print("Photo album full. Selecting next one.")
					try:
						global photo_album_id
						photo_album_id = photo_albums[photo_albums.index(photo_album_id) + 1]
					except:
						print("No more albums to select.")
						raise

				elif err.response.text == "Not a valid image.":
					print("Skipping post. Not editing post because Google Photos rejecting invalid image on page: " + post['url'])
					return False

		 		elif err.response.reason == "Unauthorized" or err.response.text == "Token invalid - Invalid token: Token expired.":
					# Access token might have expired (1 hour)
					# "Unauthorized" is from Blogger, "Token invalid..." is from Picasa
					print("Access token might have expired (1 hour). Refreshing and trying again.")
					oauth.refresh_access_token()

			elif type(err) == requests.exceptions.ReadTimeout:
				print("ERROR: Network timeout. Trying this post again.")

			else:
				print("ERROR: {0}. Retrying post {1}".format(err, post['url']))

			# Try this post again
			return edit_post(post, quiet, is_retry + 1)


# Update all posts for a single blog
def edit_all_posts(all_blog_posts):
	for single_post in all_blog_posts:
		edit_post(single_post)

	## took out multiprocessing. so much pain. if you'd like to try, replace above with below
	# pool = multiprocessing.Pool(processes = 20)
	# results = pool.map(edit_post, all_blog_posts)

def find_and_edit_single_post(all_blog_posts):
	processed_index = None
	for index, single_post in enumerate(all_blog_posts):
		actually_changed_something = edit_post(single_post, True)

		if actually_changed_something:
			processed_index = index
			break

	if processed_index:
		return {'success': True, 'processed_index': processed_index}
	else:
		return {'success': False}


# Main function - program entry point
if __name__ == '__main__':
	print("")
	print("INSTRUCTIONS:")
	print("First, backup your blog. Blogger->Settings->Other->Import & back up")
	print("Go to https://jamesoflol.github.io/photobucket-blogger-migratinator")
	print("Under Step 4, click 'AUTHENTICATE WITH GOOGLE NOW'. Follow prompts to log in with the Google account you use for Blogger.")
	auth_code = raw_input("Paste the 'Authentication code' here, and press enter: (It'll start with something like 4/Y2_b...): ").strip()
	oauth = Oauth(auth_code)
	print("Got access token: " + oauth.access_token)

	all_my_blogs = list_blogs()
	print("")
	print("Here's a list of your blogs: ")
	for index, blog in enumerate(all_my_blogs):
		print("- Blog number: {0}, url: {1}".format(index, blog['url']))

	print("")
	blog_num = raw_input("Type the number of the blog you want to work on: Default [0]: ")
	if blog_num:
		blog_num = int(blog_num)
	else:
		blog_num = 0

	print("")
	print("Gathering list of all blog posts. This can take a while...")
	blog_id = all_my_blogs[blog_num]['id']
	all_blog_posts = list_posts(blog_id)
	print("Found {0} posts.".format(len(all_blog_posts)))

	print("")
	print("Gathering list of your Google Photo albums that contain the word 'migratinator'")
	print("")
	photo_albums = picasa.get_list_of_albums(oauth.access_token)
	if len(photo_albums) > 0:
		photo_album_id = photo_albums[0]
	else:
		print("No appropriate albums found. Will use the inbuilt album called 'drop box'. Note that there will be a limit of 2000 photos.")
		photo_album_id = "default"

	print("")
	raw_input("OK, now we're going to process/update a single blog post. This is for real. It will edit your blog live. Press ENTER to proceed. Press CTRL+C to exit.")

	try:
		while True:
			single_post_edit_result = find_and_edit_single_post(all_blog_posts)
			if single_post_edit_result['success']:
				processed_index = single_post_edit_result['processed_index']
				del all_blog_posts[processed_index] # Remove the one we've already processed so it doesn't try again on the next loop
			else:
				print("No remaining posts with photobucket links. I think we're all done!")
				break

			do_one_or_all = raw_input("Please check the URL above in a browser. If you're happy... Press ENTER to do one more, or type ALL and press enter to do the rest, or pretty CTRL+C to exit: ") # Blank = str = ''
			if do_one_or_all.lower() == "all":
				edit_all_posts(all_blog_posts)
				print("All posts edited.")
				break

	except Exception as err:
		print("ERROR: " + str(err))
		try:
			print("ERROR REASON: " + str(err.response.text))
		except:
			print("No additional error reason.")

	raw_input("Press enter to exit.")
