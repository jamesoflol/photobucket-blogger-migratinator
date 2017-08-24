import requests
from xml.etree import ElementTree
import uuid
from datetime import datetime

# Uploads image, returns image embed url
def upload_image_to_picasa(auth, image_binary, filename, album_id='default'):
	extension = filename.split('.')[-1].lower()
	if extension == 'jpg':
		extension = 'jpeg'
	content_type = 'image/' + extension

	url = 'https://picasaweb.google.com/data/feed/api/user/default/albumid/' + album_id # E.g., first 2000 photos go in to a bucket called 'migratinator1'
	headers = {
		'Content-Type': content_type, 
		'Slug': 'Blog Import ' + datetime.now().strftime('%Y-%m-%d') + ' - ' + filename + ' - ' + str(uuid.uuid4().hex), # Unique filename because there will be dupes
		'Authorization': 'Bearer ' + auth, 
		'Gdata-version': '2'
	}

	# POST the image
	r = requests.post(url, headers=headers, data=image_binary, timeout=20)
	# print('file upload http status: ' + str(r.status_code)) # 201 = Created
	r.raise_for_status()

	# Get URL of uploaded image
	e = ElementTree.fromstring(r.text)
	google_image_url = e.find('{http://www.w3.org/2005/Atom}content').attrib['src']

	return google_image_url


# Get list of photo albums so that we can use the ID
def get_list_of_albums(auth):
	url = 'https://picasaweb.google.com/data/feed/api/user/default'
	headers = {
		'Authorization': 'Bearer ' + auth, 
		'Gdata-version': '2'
	}

	# GET the list
	r = requests.get(url, headers=headers, timeout=10)
	r.raise_for_status()

	# Get list of IDs for albums that contain the word 'migratinator'
	e = ElementTree.fromstring(r.text.encode('utf-8'))
	album_entries_xml = e.findall('{http://www.w3.org/2005/Atom}entry')
	albums = []
	for album_entry in album_entries_xml:
		title = album_entry.find('{http://www.w3.org/2005/Atom}title').text
		if 'migratinator' in title.lower():
			print("Found photo album: " + title)
			album_id = album_entry.find('{http://schemas.google.com/photos/2007}id').text
			albums.append(album_id)
	return albums


