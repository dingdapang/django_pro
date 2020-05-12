$(function(){
    $(".btn-normal").click(function () {
        // console.log()
        level = $(this).attr("level");
        $.getJSON("/app/ordervip/", {"level": level}, function (data) {
            console.log(data);


        })
    });

    $(".add-month").click(function () {

        var $add = $(this);
        level = $add.attr("level");

        $.get('/app/addmonth/', {'level': level}, function (data) {
            console.log(data);
            if(data['status'] === 200){
                $add.siblings('span').eq(0).html(data['month']);
                $add.siblings('span').eq(1).html(data['month'] * 100);
            }
        })
    });

    $(".sub-month").click(function () {
        var $add = $(this);
        level = $add.attr("level");

        $.get('/app/submonth/', {'level': level}, function (data) {
            console.log(data);
            if(data['status'] === 200){
                $add.siblings('span').eq(0).html(data['month']);
                $add.siblings('span').eq(1).html(data['month'] * 100);
            }

        })
    })
});