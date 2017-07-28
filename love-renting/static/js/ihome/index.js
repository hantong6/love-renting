function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function setStartDate() {
    var startDate = $("#start-date-input").val();
    if (startDate) {
        $(".search-btn").attr("start-date", startDate);
        $("#start-date-btn").html(startDate);
        $("#end-date").datepicker("destroy");
        $("#end-date-btn").html("离开日期");
        $("#end-date-input").val("");
        $(".search-btn").attr("end-date", "");
        $("#end-date").datepicker({
            language: "zh-CN",
            keyboardNavigation: false,
            startDate: startDate,
            format: "yyyy-mm-dd"
        });
        $("#end-date").on("changeDate", function() {
            $("#end-date-input").val(
                $(this).datepicker("getFormattedDate")
            );
        });
        $(".end-date").show();
    }
    $("#start-date-modal").modal("hide");
}

function setEndDate() {
    var endDate = $("#end-date-input").val();
    if (endDate) {
        $(".search-btn").attr("end-date", endDate);
        $("#end-date-btn").html(endDate);
    }
    $("#end-date-modal").modal("hide");
}

function goToSearchPage(th) {
    var url = "/search.html?";
    url += ("aid=" + $(th).attr("area-id"));
    url += "&";
    url += ("aname=" + $(th).attr("area-name"));
    url += "&";
    url += ("sd=" + $(th).attr("start-date"));
    url += "&";
    url += ("ed=" + $(th).attr("end-date"));
    location.href = url;
}

function logout() {
    $.ajax({
        url:'/api/session',
        type:'DELETE',
        dataType:'json',
        headers:{'X-XSRFToken':getCookie('_xsrf')},
        success:function (reply) {
            if ('0'==reply.errno)
                {location.href='/index.html';}
            else
                {alert(reply.errmsg);}
        }
    });
}

$(document).ready(function(){
    $(".top-bar>.register-login").show();

    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);               //当窗口大小变化的时候

    $("#start-date").datepicker({
        language: "zh-CN",
        keyboardNavigation: false,
        startDate: "today",
        format: "yyyy-mm-dd"
    });

    $("#start-date").on("changeDate", function() {
        var date = $(this).datepicker("getFormattedDate");
        $("#start-date-input").val(date);
    });

    $.get('/api/session',function (reply) {
        if ('0'==reply.errno)
        {
            $('.hasname').html(reply.userName);
            $('.haslogin').show();
            $('.notlogin').hide();
        }
    });
    
    $.get('/api/index',function (reply) {
        if('0'==reply.errno)
        {
            render_html=template('tpl_index',{indexs:reply.data});
            $('.swiper-wrapper').html(render_html);
            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationClickable: true,
                // observer:true,
                // observerParents:true
            });
            // mySwiper.update();
        }
        else
        {alert('获取主页展示房源失败！')}
    });
    
    $.get('/api/area',function (reply) {
        if('0'==reply.errno)
        {
            // for(var i=0;i<reply.data.length;i++)
            // {$('#area-id').append('<option value="'+reply.data[i].aid+'">'+reply.data[i].aname+'</option>');}
            render_html=template('tpl_area',{areas:reply.data});
            $('.area-list').html(render_html);
            $(".area-list a").click(function(e){
                $("#area-btn").html($(this).html());
                $(".search-btn").attr("area-id", $(this).attr("area-id"));
                $(".search-btn").attr("area-name", $(this).html());
                $("#area-modal").modal("hide");
            });
        }
        else
        {alert(reply.errmsg);}
    });
});