$(function () {

    $(".cancel-follow").click(function () {

        account_id = $(this).parent().attr("account_id");
        $.getJSON('/app/unfollow/', {"account_id": account_id}, function (data) {
            console.log(data);
            window.location.reload();
        })
    })

    $(".cancel-block").click(function () {

        account_id = $(this).parent().attr("account_id");
        $.getJSON('/app/unblock/', {"account_id": account_id}, function (data) {
            console.log(data);
            window.location.reload();
        })
    })
});