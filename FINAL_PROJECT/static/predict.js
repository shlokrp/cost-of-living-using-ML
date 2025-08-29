$(document).ready(function () {
    $('#predict-button').click(function (e) {
        e.preventDefault();
        $.ajax
            ({
                type: 'POST',
                url: '/predict',
                data: $('#cost-form').serialize(),
                success: function (response) {
                    $('body').html(response);
                },
                error: function (error) {
                    console.log(error);
                }
            });
    });
});
