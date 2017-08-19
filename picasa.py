import requests
from xml.etree import ElementTree
import uuid
from datetime import datetime

# Uploads image, returns image embed url
def upload_image_to_picasa(auth, image_binary, filename):
	extension = filename.split('.')[-1].lower()
	if extension == 'jpg':
		extension = 'jpeg'
	content_type = 'image/' + extension

	url = 'https://picasaweb.google.com/data/feed/api/user/default/albumid/default'
	headers = {
		'Content-Type': content_type, 
		'Slug': 'Blog Import ' + datetime.now().strftime('%Y-%m-%d') + ' - ' + filename + ' - ' + str(uuid.uuid4().hex), # Unique filename because there will be dupes
		'Authorization': 'Bearer ' + auth, 
		'Gdata-version': '2'
	}

	# POST the image
	r = requests.post(url, headers=headers, data=image_binary, timeout=10)

	# print(r.text)
	# print('file upload http status: ' + str(r.status_code)) # 201 = Created
	r.raise_for_status()

	# Get URL of uploaded image
	e = ElementTree.fromstring(r.text)
	google_image_url = e.find('{http://www.w3.org/2005/Atom}content').attrib['src']

	return google_image_url
