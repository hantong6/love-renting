function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $.get('/api/session',function (reply) {
        if ('0'!=reply.errno)
        {location.href='/login.html';}
        else
        {$('.page-title span').html(reply.userName);}
    });

    $.get('/api/house',function (reply) {
        if('0'==reply.errno)
        {
            render_html=template('tpl_house',{houses:reply.data});
            $('#houses-list').append(render_html);
        }
        else
        {alert('获取房源异常');}
    });

    $.get('/api/auth',function (reply) {
        if('0'==reply.errno)
        {
            $('.auth-warn').hide();
            $('.btn-success').removeAttr('disabled');
        }
        else if('4001'==reply.errno)
        {alert('查询实名信息异常，请刷新页面重试！')}
        else {}
    });
});