$(function () {

    $(".Previous").click(function () {
        var keyword = $("#keyword").val().trim();
        var page = $("#page").val();
        if (page <= 1){
            window.open(`/app/search/?keyword=${keyword}&page=1`, target=self);
        }else {
            window.open(`/app/search/?keyword=${keyword}&page=${page-1}`, target=self);
        }
    });
    $(".Next").click(function () {
        var keyword = $("#keyword").val().trim();
        var page = $("#page").val();
        var max_len = $(".max_length").val();
        if (parseInt(page) >= Math.ceil(max_len / 5)){
            window.location.reload();
        }else {
            window.open(`/app/search/?keyword=${keyword}&page=${parseInt(page)+1}`, target=self);
        }
    });
    $("#keyword").change(function () {
        $("#page").val(1);
    })








});



var searchArr;
    //定义一个search的，判断浏览器有无数据存储（搜索历史）
if(localStorage.search){
//如果有，转换成 数组的形式存放到searchArr的数组里（localStorage以字符串的形式存储，所以要把它转换成数组的形式）
    searchArr= localStorage.search.split(",")
}else{
//如果没有，则定义searchArr为一个空的数组
    searchArr = [];
}
//把存储的数据显示出来作为搜索历史
MapSearchArr();

function add_search(){

    var val = $(".searchInput").val();
    if (val.length>=2){
        //点击搜索按钮时，去重
        KillRepeat(val);
        //去重后把数组存储到浏览器localStorage
        localStorage.search = searchArr;
        //然后再把搜索内容显示出来
        MapSearchArr();
    }

    window.location.href=search_url+'?keyword='+val+"&search_type="+"official";

}
function add_search2(){

    var val = $(".searchInput").val();
    if (val.length>=2){
        //点击搜索按钮时，去重
        KillRepeat(val);
        //去重后把数组存储到浏览器localStorage
        localStorage.search = searchArr;
        //然后再把搜索内容显示出来
        MapSearchArr();
    }

    window.location.href=search_article_url+'?keyword='+val+"&search_type="+"title";

}

function MapSearchArr(){
    var tmpHtml = "";
    var arrLen = 0
    if (searchArr.length >= 5){
        arrLen = 5
    }else {
        arrLen = searchArr.length
    }
    for (var i=0;i<arrLen;i++){

        // tmpHtml += '<a href="'+search_url+'?q='+searchArr[i]+'">'+searchArr[i]+'</a>'
        tmpHtml += `<span style="color: #2aabd${i}">${searchArr[i]}  </span>`
    }
    $(".mysearch .all-search").html(tmpHtml);
}
//去重
function KillRepeat(val){
    var kill = 0;
    for (var i=0;i<searchArr.length;i++){
        if(val===searchArr[i]){
            kill ++;
        }
    }
    if(kill<1){
        searchArr.unshift(val);
    }else {
        removeByValue(searchArr, val)
        searchArr.unshift(val)
    }
}

var suggest_url = "/app/searchsuggest/";

        var search_url = "/app/search/";
        var search_article_url = "/app/searcharticle/";

        $('.searchList').on('click', '.searchItem', function () {
            $('.searchList .searchItem').removeClass('current');
            $(this).addClass('current');
        });

        function removeByValue(arr, val) {
            for (var i = 0; i < arr.length; i++) {
                if (arr[i] == val) {
                    arr.splice(i, 1);
                    break;
                }
            }
        }


        // 搜索建议
        $(function () {
            $('.searchInput').bind(' input propertychange ', function () {
                var searchText = $(this).val();
                var tmpHtml = "";
                var accHtml = "";
                $.ajax({
                    cache: false,
                    type: 'get',
                    dataType: 'json',
                    url: suggest_url + "?s=" + searchText + "&s_type=",
                    async: true,
                    success: function (key) {
                        article_data = key['article_datas'];
                        for (var i = 0; i < article_data.length; i++) {
                            tmpHtml += '<li><a href="' + search_article_url + '?keyword=' + article_data[i] + '&page=1&search_type=title">' + article_data[i] + '</a></li>'

                        }
                        account_data = key['account_datas'];
                        for (var i = 0; i < account_data.length; i++) {
                            accHtml += '<li><a href="' + search_url + '?keyword=' + account_data[i] + '&page=1&search_type=official">' + account_data[i] + '</a></li>'

                        }

                        $(".dataList").html("");
                        $(".dataList").append('<li style="color: orange;font-size: 18px;">公众号</li>');
                        $(".dataList").append(accHtml);
                        $(".dataList").append('<li style="color: orange;font-size: 18px;">文章</li>');
                        $(".dataList").append(tmpHtml);
                        if (account_data.length == 0 ||article_data.length == 0) {
                            $('.dataList').hide()
                        } else {
                            $('.dataList').show()
                        }



                    }
                });
            });
        })

        function hideElement(currentElement, targetElement) {
            if (!$.isArray(targetElement)) {
                targetElement = [targetElement];
            }
            $(document).on("click.hideElement", function (e) {
                var len = 0, $target = $(e.target);
                for (var i = 0, length = targetElement.length; i < length; i++) {
                    $.each(targetElement[i], function (j, n) {
                        if ($target.is($(n)) || $.contains($(n)[0], $target[0])) {
                            len++;
                        }
                    });
                }
                if ($.contains(currentElement[0], $target[0])) {
                    len = 1;
                }
                if (len == 0) {
                    currentElement.hide();
                }
            });
        };
        hideElement($('.dataList'), $('.searchInput'));

