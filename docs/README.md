## Welcome to Photobucket->Blogger Migratinator

This small app is for anyone who's got Blogger blog posts that contain (now broken) Photobucket embedded images. It automatically migrates your photos from Photobucket to Google Photos, and then updates all your Blogger posts with the new links.

Steps:

1. Download the executable program for windows or mac from https://github.com/jamesoflol/photobucket-blogger-migratinator/releases
2. The first thing the program will ask you to do is to authenticate with Google. You do that by clicking this link: [AUTHENTICATE WITH GOOGLE NOW](https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=https://jamesoflol.github.io/photobucket-blogger-migratinator/auth_success&prompt=consent&response_type=code&client_id=475469684563-3tkh3bscomb3548fq4fs8fg7b5t34qlf.apps.googleusercontent.com&scope=https://www.googleapis.com/auth/blogger+https://picasaweb.google.com/data/&access_type=offline). This app requires access access to your Google account. To be prudent, upon following the link you will see that it only asks for access to the Blogger and Google Photos parts of your account.

Misc notes:
- It isn't quite possible to actually put the photos in to your Blogger the same way that you would upload new photos, but the next best thing is that we put them in to Google Photos. All the photos will be visible in your account in photos.google.com, in an album called 'drop box'.
- For the nerds/security conscious: Clone, inspect, and run the Python source from https://github.com/jamesoflol/photobucket-blogger-migratinator. It's been tested with Python 2.7.10. The only dependency is the python requests module (pip install requests).
