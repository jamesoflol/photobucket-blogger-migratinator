import re
import json

# Load up your blogger backup file, or really any giant ball of text that has broken photobucket links in it
f = open('blogger_backup.xml','r')
wholefile_str = f.read()

# Find all urls in file
#regexString = "\/\/(?:.+?)(?:'|\")"
#regexString = "(?:'|\")(?:http|https)(?::\/\/)(.+?)(?:'|\")"
regexString = "(?:'|\")(https*:\/\/.+?)(?:'|\")"
results = re.findall(regexString, wholefile_str)

urls = []
allowed_suffixes = ('png','PNG','jpg','JPG','jpeg','JPEG','bmp','BMP','gif','GIF') # This is all Picasa allows

# Filter for just the photobucket.com links
for result in results:
    if 'photobucket.com/' in result and result.endswith(allowed_suffixes):
        #urls.append('http:' + result[:-1]) # Add 'http:' to the start, and cut the ' or " from the end.
        urls.append(result)

de_dupe = list(set(urls))

# Prettify the result, just so we can eyeball it in its file
json_str = json.dumps(de_dupe, sort_keys=True,
    indent=4, separators=(',', ': '))

# Write resulting photobucket url list to file
f = open('photobucket_url_list.json', 'w')
f.write(json_str)
f.close()
