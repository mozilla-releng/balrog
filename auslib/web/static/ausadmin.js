function getHTML(url) {
    return $.get(url, {'format': 'html'})
    .error(function(req, code, error) {
        alert(req);
        alert(code);
        alert(error);
    });
}

function getUsers() {
    return getHTML('/users');
}

function getUserPermissions(username) {
    return getHTML('/users/' + username + '/permissions');
}
