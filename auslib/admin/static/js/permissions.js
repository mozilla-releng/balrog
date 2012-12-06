function getPermissionUrl(username, permission) {
    return SCRIPT_ROOT + '/users/' + username + '/permissions/' + permission;
}

function addNewPermission(form, username, permission, options, element) {
    url = getPermissionUrl(username, permission);
    data = {
        'options': options
    };
    preAJAXLoad(form);
    $.ajax(url, {'type': 'put', 'data': data})
    .error(handleError
    ).success(function(data) {
        $.get(url, {'format': 'html'})
        .error(handleError
        ).success(function(data) {
            postAJAXLoad(form);
            element.append(data);
            alertify.success('Permission added!');
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

function submitPermissionForm(form, username, permissionForm, element) {
    clicked = permissionForm.data('clicked');
    permission = $('[name*=permission]', permissionForm);
    options = $('[name*=options]', permissionForm);
    data_version = $('[name*=data_version]', permissionForm);
    preAJAXLoad(form);
    if (clicked === 'update') {
        updatePermission(username, permission.val(), options.val(), data_version.val())
        .success(function(data) {
            data = JSON.parse(data);
            data_version.val(data.new_data_version);
            postAJAXLoad(form);
            alertify.success('Permission updated');
        });
    }
    else if (clicked === 'delete') {
        deletePermission(username, permission.val(), data_version.val())
        .success(function() {
            element.remove();
            postAJAXLoad(form);
            alertify.success('Permission deleted');
        });
    }
}
