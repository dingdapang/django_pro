$(function () {

    $(".account_follow_success").click(function () {
        account_id = $("#account_id").attr("accountid");
        $.getJSON("/app/follow/", {"account_id": account_id}, function (data) {
            console.log(data);
            window.location.reload();
        });
    });

    $(".account_follow_cancel").click(function () {
        account_id = $("#account_id").attr("accountid");
        $.getJSON("/app/unfollow/", {"account_id": account_id}, function (data) {
            console.log(data);
            window.location.reload();
        });
    });

    $(".account_unfollow_success").click(function () {
        account_id = $("#account_id").attr("accountid");
        $.getJSON("/app/block/", {"account_id": account_id}, function (data) {
            console.log(data);
            window.location.reload();
        });
    });

    $(".account_unfollow_cancel").click(function () {
        account_id = $("#account_id").attr("accountid");
        $.getJSON("/app/unblock/", {"account_id": account_id}, function (data) {
            console.log(data);
            window.location.reload();
        });
    });
});