## Welcome to Photobucket->Blogger Migratinator

This small app is for anyone who's got Blogger blog posts that contain (now broken) Photobucket embedded images. It automatically migrates your photos from Photobucket to Google Photos, and then updates all your Blogger posts with the new links.

Steps:

1. The first thing you'll have to do is create 'albums' for the photos to go in to in Google Photos. Albums have a limit of 2,000 photos per album, so you might have to create several.
    1. Go to https://photos.google.com
    2. Click 'Albums' on the left
    3. Click 'New album'
    4. Creating an album requires having at least one photo to put in it. (If you have zero photos in Google Photos right now, you'll need to upload a dummy one.) Select any one of your photos.
    5. In the top-right of the page, click 'Create'
    6. Replace the heading text of 'Untitled' with a name containing the word 'migratinator'. (It MUST contain that word. E.g.: 'Migratinator 1'), and click the tick button in the top-left.
    7. If your blog has more than 2,000 photos to be migrated, you'll need to do steps iii to vi multiple times. (E.g., Migratinator2, Migratinator2, etc.)
2. Download the executable program for windows or mac from https://github.com/jamesoflol/photobucket-blogger-migratinator/releases.
3. Extract the zip file, and double click the file to run app.
4. The first thing the program will ask you to do is to authenticate with Google. You do that by clicking this link: [AUTHENTICATE WITH GOOGLE NOW](https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=https://jamesoflol.github.io/photobucket-blogger-migratinator/auth_success&prompt=consent&response_type=code&client_id=475469684563-3tkh3bscomb3548fq4fs8fg7b5t34qlf.apps.googleusercontent.com&scope=https://www.googleapis.com/auth/blogger+https://picasaweb.google.com/data/&access_type=offline). This app requires access access to your Google account. To be prudent, upon following the link you will see that it only asks for access to the Blogger and Google Photos parts of your account.

Misc notes:
- All the photos will also be visible at photos.google.com, in an album called 'drop box'.
- For the nerds/security conscious: Instead of downloading, you can clone, inspect, and run the Python source from https://github.com/jamesoflol/photobucket-blogger-migratinator. It's been tested with Python 2.7.10. The only dependency is the python requests module (pip install requests). Please feel free to raise issues or pull requests.
