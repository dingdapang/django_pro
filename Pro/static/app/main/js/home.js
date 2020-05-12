$(function () {
    var top = $(window).scrollTop() + ($(window).height() - $("#login-style").outerHeight()) / 2;
    var left = ($(window).width() - $("#login-style").outerWidth(true)) / 2;

    $("#login-style").css({
        left: left,
        top: top
    });

    $(window).on("scroll resize", function () {
        var top = $(window).scrollTop() + ($(window).height() - $("#login-style").outerHeight()) / 2;
        var left = ($(window).width() - $("#login-style").outerWidth(true)) / 2;

        $("#login-style").css({
            left: left,
            top: top
        })
    });
    $(".login_in").click(function () {
        $("#login-style").css("display", "block");
    });
    $(".close").click(function () {
        $("#login-style").css("display", "none");
    });
    // $(".remove_button").click(function () {
    //     $("#login-style").css("display", "none");
    // });




});

function parse_data() {
    // console.log('触发');

    var $password_input = $("#password_input");

    var password = $password_input.val().trim();

    $password_input.val(md5(password));

    return true
}