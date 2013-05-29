
function getReleaseUrl(release) {
    return SCRIPT_ROOT + '/releases/' + release;
}


function submitNewReleaseForm(releaseForm, table){
    var name = $('[name*=name]', releaseForm).val();
    if (!name) {
        return showError('name missing');
    }

    var url = getReleaseUrl(name);

    var data_version = $('[name*=data_version]', releaseForm).val();
    var version = $('[name*=version]', releaseForm).val();
    var product = $('[name*=product]', releaseForm).val();
    var blob_field = $('[name*=blob]', releaseForm);
    var csrf_token = $('[name*=csrf_token]', releaseForm).val();
    if (!blob_field[0].files.length) {
        showError('No file chosen');
        return;
    }

    preAJAXLoad(releaseForm);

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
            'csrf_token': csrf_token
        };

        $.ajax(url, {'type': 'put', 'data': data})
            .error(handleError)
            .success(function(data) {
                  $.get(url)
                  .error(handleError).
                  success(function(data) {
                          postAJAXLoad(releaseForm);
                          table.append(data);
                          alertify.success('Release added!');
                      });
              });
    }
}


$(document).ready(function() {
    $('#Releases_table').dataTable();

    $('#ReleasesForm').submit(function() {
        submitNewReleaseForm($(this), $('#Releases_table'));
        return false;
    });

} );
