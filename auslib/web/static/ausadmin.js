function handleError(response, code, error) {
    alert(response.responseText);
}

function getPermissionUrl(username, permission) {
    return SCRIPT_ROOT + '/users/' + username + '/permissions/' + permission;
}

function addNewPermission(username, permission, options, element) {
    url = getPermissionUrl(username, permission);
    data = {
        'options': options
    };
    $.ajax(url, {'type': 'put', 'data': data})
    .error(handleError
    ).success(function(data) {
        $.get(url, {'format': 'html'})
        .error(handleError
        ).success(function(data) {
            element.append(data);
        });
    });
}

function updatePermission(username, permission, options, data_version) {
    url = getPermissionUrl(username, permission);
    data = {
        'options': options,
        'data_version': data_version
    };
    return $.ajax(url, {'type': 'post', 'data': data})
    .error(handleError
    );
}

function deletePermission(username, permission, data_version) {
    url = getPermissionUrl(username, permission);
    data = {
        'data_version': data_version
    };
    url += '?' + $.param(data);
    // Can't put the data version in the request body, because Flask
    // and many web servers/proxies don't support DELETE + request body.
    return $.ajax(url, {'type': 'delete'})
    .error(handleError
    );
}

function submitPermissionForm(username, permissionForm, element) {
    clicked = permissionForm.data('clicked');
    permission = $('[name*=permission]', permissionForm);
    options = $('[name*=options]', permissionForm);
    data_version = $('[name*=data_version]', permissionForm);
    if (clicked === 'update') {
        updatePermission(username, permission.val(), options.val(), data_version.val())
        .success(function(data) {
            data = JSON.parse(data);
            data_version.val(data['new_data_version']);
        });
    }
    else if (clicked === 'delete') {
        deletePermission(username, permission.val(), data_version.val())
        .success(function() {
            element.remove();
        });
    }
}

function redirect(page, args) {
    window.location.assign(page + '?' + $.param(args));
}
