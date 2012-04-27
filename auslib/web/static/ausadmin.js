function handleError(response, code, error) {
    console.log(response);
    alert(response.responseText);
}

function getPermissionUrl(username, permission) {
    return SCRIPT_ROOT + '/users/' + username + '/permissions/' + permission;
}


function getReleaseUrl(release) {
    return SCRIPT_ROOT + '/releases/' + release;
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
            data_version.val(data.new_data_version);
        });
    }
    else if (clicked === 'delete') {
        deletePermission(username, permission.val(), data_version.val())
        .success(function() {
            element.remove();
        });
    }
}


function submitNewReleaseForm(releaseForm, table){
    name = $('[name*=name]', releaseForm).val();

    var url = getReleaseUrl(name);

    var data_version = $('[name*=data_version]', releaseForm).val();
    var version = $('[name*=version]', releaseForm).val();
    var product = $('[name*=product]', releaseForm).val();
    var blob_field = $('[name*=blob]', releaseForm);
    var csrf =    $('[name*=csrf]', releaseForm).val();

    console.log(csrf);
    file = blob_field[0].files[0];

    var fr = new FileReader();
    fr.onload = receivedText;
    fr.readAsText(file);

    function receivedText() {
        result = fr.result;
        data = {
            'name': name,
            'version':version,
            'product': product,
            'blob': result,
            'data_version': data_version,
            'csrf': csrf
        };
        $.ajax(url, {'type': 'put', 'data': data})
            .error(handleError)
            .success(function(data) {
                  $.get(url)
                  .error(handleError).
                  success(function(data) {
                          table.append(data);
                      });
              });
    }
}


function redirect(page, args) {
    window.location.assign(page + '?' + $.param(args));
}
