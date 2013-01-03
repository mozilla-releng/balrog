function getRedirectURL() {
    if (location.pathname.match('/rules'))
        return '/rules.html';
    if (location.pathname.match('/releases'))
        return '/releases.html';
    if (location.pathname.match('/permissions'))
        return '/permissions.html';
    return '/';
}


$(function() {
    $('[type="reset"]').click(function() {
        location.href = getRedirectURL();
    });

    $('form#revisions').submit(function() {
        var form = $(this);
        var change_id = $('input[name="change_id"]:checked', form).val();
        if (!change_id) {
            alertify.alert('Pick one');
            return false;
        }
        preAJAXLoad(form);
        $.ajax(location.href, {
            type: 'post',
            data: {change_id: change_id}
        }).error(handleError)
          .success(function() {
              postAJAXLoad(form);
              alertify.alert('Rolled back!', function() {
                location.href = getRedirectURL();
              });
          });
        return false;
    });
});
