$(document).ready(function () {
    $('#nav-toggle').on('click', function () {
        $(this).toggleClass('active')
        $('#nav-list').toggleClass('active')
    })
});