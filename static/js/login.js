function check_email(t) {
    $.ajax({
        url: check_email_url,
        contentType: 'application/json',
        type: 'GET',
        async: true,
        data: {
            'email__exact': $('#email').val()
        },
        beforeSend: function(jqXHR, settings) {
            // Pull the token out of the DOM.
            jqXHR.setRequestHeader('X-CSRFToken', $('input[name=csrfmiddlewaretoken]').val());
        },
        success: function(data) {
            if (data.objects.length > 0) {
                set_login_mode();
            } else {
                set_save_mode();
            }
        }
    });
}

function set_login_mode() {
    $('.i-know-u').removeClass('d-none');
    $('.i-dont-know-u').addClass('d-none');
    $('.displaypass').removeClass('d-none');
    $('.savebutton').html('Se connecter');

    $('.savebutton').off('click', check_email)
    $('.savebutton').prop("type", "submit");
}

function set_save_mode() {
    $('.i-know-u').addClass('d-none');
    $('.i-dont-know-u').removeClass('d-none');
    $('.displaypass').removeClass('d-none');
    $('.profile').removeClass('d-none')
    $('.savebutton').html('Enregistrer');

    $('.savebutton').prop("type", "submit");
}

function hide_pass() {
    $('.displaypass').addClass('d-none');
    $('.profile').addClass('d-none');
    $('.savebutton').prop("type", "button");
    $('.savebutton').html('Vérifier');
    $('.savebutton').on('click', check_email)
}

$('.savebutton').on('click', check_email)
$('#email').on('keydown', hide_pass)