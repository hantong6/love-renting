function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function getQueryString(name)
{
    var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    var r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return decodeURI(r[2]);
    }
    return null;
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function orderSubmit() {
    var houseId=getQueryString('id');
    var startDate=$('#start-date').val();
    var endDate=$('#end-date').val();
    $.ajax({
        url:'/api/booking',
        type:'POST',
        contentType:'application/json',
        data:JSON.stringify({'house_id':houseId,'start_date':startDate,'end_date':endDate}),
        headers:{'X-XSRFToken':getCookie('_xsrf')},
        dataType:'json',
        success:function (reply) {
            alert(reply.errmsg);
            if('0'==reply.errno)
            {location.href='/orders.html'}
            else {}
        }
    });
}

$(document).ready(function(){

    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });

    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });

    $.get('/api/session',function (reply) {
        if ('0'!=reply.errno)
        {location.href='/login.html';}
        else {}
    });

    $.get('/api/booking?id='+getQueryString('id'),function (reply) {
        if('0'==reply.errno)
        {$('.house-info').html(template('tpl_house',{house:reply.data}));}
        else
        {alert(reply.errmsg);}
    });

    $('.submit-btn').on('click',function (e) {
       orderSubmit();
    });
});
