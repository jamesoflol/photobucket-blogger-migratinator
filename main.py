import requests
import json
import re
import urllib2
import sys
import hashlib
import multiprocessing
# import itertools
import picasa # picasa.py in this folder

def list_blogs(auth):
	url = 'https://www.googleapis.com/blogger/v3/users/self/blogs'
	headers = {
		'Authorization': auth
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
def list_posts(auth, blog_id, page_token=None, page_num=0):
	url = "https://www.googleapis.com/blogger/v3/blogs/{0}/posts".format(blog_id)
	headers = {
		'Authorization': auth
	}
	params = {
		'pageToken': page_token
	}

	# HTTP GET
	r = requests.get(url, headers=headers, params=params)
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

	if nextPageToken and page_num < 5:
		# Recurse this function to get the next page of results
		print("Page {0} done. Found approx {1} posts so far. On to page ID: {2}".format(page_num, page_num*10+len(results), nextPageToken))
		next_results = list_posts(auth, blog_id, nextPageToken, page_num+1)

		# Combine the recursed function's results with this one in to mega result
		for item in next_results:
			results.append(item)
	else:
		print('No more pages. All done.')

	return results


# Update a single post 
# Params:
# - post: dict var from json_obj['items']. post keys = content, url, id, etc.
def edit_post(post):
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

	# For each image, download from photobucket, upload to picasa, and update the image link in the post content
	for url in photobucket_photos_de_duped:
		# Download image from photobucket
		req = urllib2.Request(url)
		req.add_header('Referer', url + '.html') # The referer HTTP header is how photobucket prevents hotlinking/downloading your images
		response = urllib2.urlopen(req)
		image_binary = response.read()

		# Check to make sure we haven't accidentally downloaded the photobucket pay-up notice image
		md5_hash = hashlib.md5(image_binary).hexdigest()
		if md5_hash == 'aafa26a6610d377d8e42f44bc7e76635':
			raise Exception("It looks like something's gone wrong and we've accidentally downloaded the photobucket pay-up notice image.")

		# Upload image to picasa
		filename = url.split("/")[-1:][0] # Grabs everythign after the last slash
		google_image_url = picasa.upload_image_to_picasa(auth, image_binary, filename)

		# Update URLs in blog post content from photobucket to google
		post['content'] = post['content'].replace(url, google_image_url)
		# Also update the httpS version of any such url
		post['content'] = post['content'].replace(url.replace("http://","https://"), google_image_url)

	# Were any photos updated?
	if len(photobucket_photos_de_duped) > 0:
		# Save content changes
		url = "https://www.googleapis.com/blogger/v3/blogs/{0}/posts/{1}".format(blog_id, post['id'])
		headers = {
			'Authorization': auth,
			'Content-Type': 'application/json'
		}
		data_obj = dict()
		data_obj['content'] = post['content']
		data = json.dumps(data_obj)
		# HTTP PATCH (Just editing one item, rather than PUT or POST)
		r = requests.patch(url, headers=headers, data=data)
		r.raise_for_status() # Raise an exception if HTTP status code not 2xx

		print('Saved changes. See result at: ' + post['url'])

		return True
	else:
		print('No changes at: ' + post['url'])

		return False


# Update all posts for a single blog
def edit_all_posts(auth, all_blog_posts):
	# for single_post in all_blog_posts:
	# 	try:
	# 		edit_post(single_post)
	# 	except requests.exceptions.HTTPError as err:
	# 		print 'ERROR: ' + err
	pool = multiprocessing.Pool(processes = 20)
	results = pool.map(edit_post, all_blog_posts)


def find_and_edit_single_post(auth, all_blog_posts):
	processed_index = None
	for index, single_post in enumerate(all_blog_posts):

		actually_changed_something = edit_post(single_post)

		# problem with this is that it'll forever look at the one where nothing 
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
	print('Go to https://developers.google.com/oauthplayground/')
	print('Under Step 1, select:')
	print('- Blogger: https://www.googleapis.com/auth/blogger, and')
	print('- Picasa: https://picasaweb.google.com/data/')
	print('Click Authorize APIs. Follow prompts to log in with the Google account you use for Blogger')
	print('Under Step 2, click "Exchange authorization code for tokens"')
	auth = 'Bearer ' + raw_input("Paste the 'Access token' here, and press enter: (It'll start with something like ya29.GlulBJ...): ")

	all_my_blogs = list_blogs(auth)
	print("")
	print("Here's a list of your blogs: ")
	for index, blog in enumerate(all_my_blogs):
		print("- Blog number: {0}, url: {1}".format(index, blog['url']))

	print("")
	blog_num = raw_input("Type the number of the blog you want to work on: Default [0]: ")
	if not blog_num:
		blog_num = 0

	print("Gathering list of all blog posts. This can take a while...")
	blog_id = all_my_blogs[blog_num]['id']
	all_blog_posts = list_posts(auth, blog_id)
	print("Found {0} posts.".format(len(all_blog_posts)))

	print("")
	raw_input("OK, now we're going to process/update a single blog post. This is for real. It will edit your blog live. Press ENTER to proceed. Press CTRL+C to exit.")

	try:
		while True:
			single_post_edit_result = find_and_edit_single_post(auth, all_blog_posts)
			if single_post_edit_result['success']:
				processed_index = single_post_edit_result['processed_index']
				del all_blog_posts[processed_index] # Remove the one we've already processed so it doesn't try again on the next loop
			else:
				print("No remaining posts with photobucket links. I think we're all done!")
				break

			do_one_or_all = raw_input("Please check the URL above in a browser. If you're happy... Press ENTER to do one more, or type ALL and press enter to do the rest, or pretty CTRL+C to exit: ") # Blank = str = ''
			if do_one_or_all.lower() == "all":
				edit_all_posts(auth, all_blog_posts)
				print("All posts edited.")
				break

		raw_input("Press enter to exit.")
	except requests.exceptions.HTTPError as err:
		#print(err.response.status_code) #e.g., '401'
		if err.response.status_code == 401:
			print("ERROR: HTTP 401 error. Your authorization code from https://developers.google.com/oauthplayground/ may have expired - it only lasts for 1 hour. Start program again to start where we left off.")

