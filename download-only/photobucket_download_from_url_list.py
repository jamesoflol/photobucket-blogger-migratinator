# Run this after get_url_list_from_blogger_backup_xml_file.py, which generates the input file for this.

import urllib2
import os
import json
import multiprocessing

# This is the subfolder of our code directory where the images will be downloaded to. Can be changed, or set to a non-code path
# (E.g., '/home/james/downloaded_photobucket_images')
SUBFOLDER_NAME = 'downloaded_images'

# Read from url list text file (json)
f = open('photobucket_url_list.json', 'r')
json_str = f.read()

# Load it in to a python list
image_url_list = json.loads(json_str)

# Function for downloading each individual picture
def process_pic_url(pic_url):
    try:
        # Get filename from URL
        index = pic_url.index('photobucket.com')
        folders_and_filename = pic_url[index+16:].split('/')
        filename = folders_and_filename[-1]

        # Check if local folder exists (we store files in relative subfolders to prevent dupes)
        # Start with the root subfolder name
        sub_subfolder_path = SUBFOLDER_NAME
        # Add each subfolder (from photobucket) to our local save path
        for subfolder in folders_and_filename:
            if not subfolder == filename:
                sub_subfolder_path = os.path.join(sub_subfolder_path, subfolder)

        try:
            if not os.path.exists(sub_subfolder_path):
                os.makedirs(sub_subfolder_path)
        except:
            pass

        # print('debug: pic_url: ' + pic_url)
        # print('debug: local_subfolder_path: ' + sub_subfolder_path)

        # Check if file exists before downloading
        if os.path.exists(os.path.join(sub_subfolder_path, filename)):
            print("DUPE: " + filename + " -- " + pic_url)
            #dupe += 1
            return ('dupe', pic_url)
        else:
            # Download the picture
            req = urllib2.Request(pic_url)
            req.add_header('Referer', pic_url + '.html') # The referer tag is how photobucket prevents hotlinking
            response = urllib2.urlopen(req)
            the_page = response.read()

            # Write the picture to disk
            f = open(os.path.join(sub_subfolder_path, filename), 'w')
            f.write(the_page)
            f.close()
            print("Downloaded: " + filename)
            #success += 1
            return ('success', pic_url)
    except Exception as e:
        print("ERROR: " + pic_url + " -- " + str(e) + " -- " + str(type(e)))
        #failure += 1
        return ('failure', pic_url)

# Multiprocessing: Run 20 concurrent threads downloading the images
pool = multiprocessing.Pool(processes = 20)
results = pool.map(process_pic_url, image_url_list)

# Get results, print results
success = 0
failure = 0
dupe = 0
for result in results:
    if result[0] == 'success':
        success += 1
    if result[0] == 'failure':
        failure += 1
    if result[0] == 'dupe':
        dupe += 1

print("")
print("successes: " + str(success))
print("failures: " + str(failure))
print("dupes: " + str(dupe))

# Prettify the result, just so we can eyeball it in its file
json_str = json.dumps(results, sort_keys=True,
    indent=4, separators=(',', ': '))

# Write resulting photobucket url list to file
f = open('photobucket_download_result_for_debugging.txt', 'w')
f.write(json_str)
f.close()

