function resetForm(form) {
    // 'form' is a jQuery instance of a form
    form.each(function() {
        this.reset();
    });
}

function showError(message) {
   alertify.alert(message);
}

function handleError(response, code, error) {
    $('.loading:visible').hide();
    $('form.disabled').removeClass('disabled');
    showError('ERROR: ' + response.responseText);
}

function preAJAXLoad(form) {
    if (!$('.loading', form).size()) {
        // add the loading fragment after the last submit button
        $('#loading .loading')
          .clone()
          .insertAfter($('[type="submit"]', form).eq(-1));
    }
    $('.loading', form).show();
    form.addClass('disabled');
}

function postAJAXLoad(form) {
    $('.loading:visible').hide();
    $('form.disabled').removeClass('disabled');
    if (form !== undefined) {
        resetForm(form);
    }
}

function redirect(page, args) {
    window.location.assign(page + '?' + $.param(args));
}
