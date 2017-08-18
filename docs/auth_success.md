Below is your Google authentication code for pasting in to the Photobucket Blogger Migratinator app.

> Your Google authentication code should appear here. If you're seeing this message, you may have navigated to this page directly. You should only arrive here via [https://jamesoflol.github.io/photobucket-blogger-migratinator](https://jamesoflol.github.io/photobucket-blogger-migratinator).

This code can only be used once - each time you run the app you'll need a new one. Please don't share this code with anyone you don't trust. It's only for use in the Migratinator.

<script>
// Simple script for grabbing parameter name from the browser URL bar
function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

// Get auth code parameter
var authcode = getParameterByName('code');

// Display it on screen
document.getElementsByTagName('Blockquote')[0].innerHTML = authcode;
</script>
