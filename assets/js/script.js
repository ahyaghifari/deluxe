$(document).ready(function () {
    $('#nav-toggle').on('click', function () {
        $(this).toggleClass('active')
        $('#nav-list').toggleClass('active')
    })
    var nav = document.getElementsByTagName('nav');
    var navtoggle = document.getElementById('nav-toggle');
    var navlist = document.getElementById('nav-list');

    $(document).on('click', function (e) {
        if (!$(e.target).closest('nav').length) {
            $('#nav-toggle').removeClass('active')
            $('#nav-list').removeClass('active')
        }
    })

});