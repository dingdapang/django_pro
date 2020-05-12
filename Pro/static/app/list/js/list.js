$(function () {

   $(".li-header").mouseenter(function () {
        $(this).css('background', '#bce8f1');
   }).mouseleave(function () {
        $(this).css('background', '');
   });
   $(".types-header").mousedown(function () {
        $("#content").find('tr').remove();
        $(this).parent("li").siblings().find("a").css('color', '');
        $(this).css('color', '#bce8f1');

        type = $(this).attr("type");

        $.getJSON("/app/rankselect/", {"t_type": type}, function (data) {
            if(data['status'] === 200){
                var limit = data['limit'];
                var arrs = data['arrs'];
                // var count = 0;
                $.each(arrs.slice(0, limit),function(index,value){
                    // console.log(index);
                    var $tbody = $("#content");
                    var $c_tr = $(`<tr class="account_select">
                                        <td>${index+1}</td>
                                        <td><img src="${value['head_img']}" alt=""><a href="/app/accountdetail/${value['account_id']}/" class="button2">${value['name']}</a></td>
                                        <td>${value['is_origin_num']}</td>
                                        <td>${value['put_num']}</td>
                                        <td>${value['all_read_num']}</td>
                                        <td>${value['origin_avg']}</td>
                                        <td>${value['all_watch_num']}</td>
                                        <td>${value['all_admire_num']}</td>
                                        <td class="Button"><a href="/app/accountdetail/${value['account_id']}/" >详情</a></td>
                                    </tr>`
                    );
                    $tbody.append($c_tr);
                });
            }
            else{
                console.log('出错');
            }
        })
   });

    var $menu = $(".menu2");
    var $now_time = Math.round(new Date(new Date().toLocaleDateString()).getTime() / 1000); // 当天零时零点的时间戳
    var $now_week = new Date().getDay();
    var $last_week_end_time = 0;

    if($now_week === 0){
        $last_week_end_time = $now_time - 6 * 24 * 60 * 60;
    }
    else{
        $last_week_end_time = $now_time - ($now_week - 1) * 24 * 60 * 60;
    }

    $last_week_start_time = $last_week_end_time - 7 * 24 * 60 * 60;

    var $m_li = $(`
        <li><a href="#" value="${$last_week_end_time}" >上周</a></li>
        <li><a href="#" value="${$last_week_end_time-7*24*60*60}">${getLocalTime($last_week_start_time-7*24*60*60)}--${getLocalTime($last_week_end_time-7*24*60*60)}</a></li>
        <li><a href="#" value="${$last_week_end_time-14*24*60*60}">${getLocalTime($last_week_start_time-14*24*60*60)}--${getLocalTime($last_week_end_time-14*24*60*60)}</a></li>
        <li><a href="#" value="${$last_week_end_time-21*24*60*60}">${getLocalTime($last_week_start_time-21*24*60*60)}--${getLocalTime($last_week_end_time-21*24*60*60)}</a></li>
    `);
    $menu.append($m_li);

    $menu.find("li").click(function () {
        var screen_time=$(this).find("a").attr("value");
        // console.log(value);
        $(".time-button").attr("time-value", $(this).find("a").attr("value"))
        .html(`${$(this).find("a").html()} <span class="caret"></span>`);

         $.getJSON("/app/timeselect/", {"screen_time": screen_time}, function (data){
                console.log(data);

                window.location.reload();

         });

    });

    function getLocalTime(nS) {
        var date = new Date(nS*1000);
        M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1) + '月';
        D = date.getDate() + '日';
        return (M+D);
    }


});
