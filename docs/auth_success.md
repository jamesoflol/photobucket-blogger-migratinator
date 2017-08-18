> Your Google authentication code should appear here

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
