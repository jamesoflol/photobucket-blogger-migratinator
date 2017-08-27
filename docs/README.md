This small app is for anyone who's got Blogger blog posts that contain (now broken) Photobucket embedded images. It automatically migrates your photos from Photobucket to Google Photos, and then updates all your Blogger posts with the new links.

Please use with caution, backup your blog, and note the liability waiver at the bottom of this page. Please use the discussion/comments thingo at the bottom of this page if you have any questions and I'll help as best I can. If you make use of this, all I ask is that you spread the word to others that are affected.

### Steps:

1. Download the executable program for windows or mac from [https://github.com/jamesoflol/photobucket-blogger-migratinator/releases](https://github.com/jamesoflol/photobucket-blogger-migratinator/releases).
2. Extract the zip file, and double click the file to run app.
3. The first thing the program will ask you to do is to authenticate with Google. You do that by clicking this link: [AUTHENTICATE WITH GOOGLE NOW](https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=https://jamesoflol.github.io/photobucket-blogger-migratinator/auth_success&prompt=consent&response_type=code&client_id=475469684563-3tkh3bscomb3548fq4fs8fg7b5t34qlf.apps.googleusercontent.com&scope=https://www.googleapis.com/auth/blogger+https://picasaweb.google.com/data/&access_type=offline). This app requires access access to your Google account. To be prudent, upon following the link you will see that it only asks for access to the Blogger and Google Photos parts of your account.

4. (Extra step for people with more than ~2,000 photos to fix.) Albums have a limit of 2,000 photos per album, so you might have to create several extra albums and run the migratinator again.
    1. Go to [https://photos.google.com](https://photos.google.com)
    2. Click 'Albums' on the left
    3. Click 'New album'
    4. Creating an album requires having at least one photo to put in it. (If you have zero photos in Google Photos right now, you'll need to upload a dummy one.) Select any one of your photos.
    5. In the top-right of the page, click 'Create'
    6. Replace the heading text of 'Untitled' with a name containing the word 'migratinator'. (It MUST contain that word. E.g.: 'Migratinator 1'), and click the tick button in the top-left.
    7. If your blog has more than 2,000 photos to be migrated, you'll need to do steps iii to vi multiple times. (E.g., Migratinator2, Migratinator2, etc.)

### Misc notes:
* The pictures linked will be a max of 512px wide. This is because of a limitation in the Google Photos API (it's a pretty horrible API D:). But note that the underlying photos are actually full res. So if you were to browse through your photos at photos.google.com you could find the full-res picture, 'copy image url' on it, and put the full thing back in. Hopefully the 512px versions work for most needs.
* The pictures will sit alongside all your other Google Photos, if you have ever used Google Photos. If you've got a huge backlog to be migrated (why else would you be using the script) then you'll never be able to pick out your existing photos again. I suggest adding all your existing photos to another photo album(s) before you start.
* For the nerds/security conscious: Instead of downloading, you can clone, inspect, and run the Python source from https://github.com/jamesoflol/photobucket-blogger-migratinator. It's been tested with Python 2.7.10. The only dependency is the python requests module (pip install requests). Please feel free to raise issues or pull requests.

<div id="disqus_thread"></div>
<script>
/**
DISQUS COMMENTS
*/
(function() { // DON'T EDIT BELOW THIS LINE
var d = document, s = d.createElement('script');
s.src = 'https://migratinator.disqus.com/embed.js';
s.setAttribute('data-timestamp', +new Date());
(d.head || d.body).appendChild(s);
})();
</script>


MIT License

Copyright (c) 2017 jamesoflol

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
