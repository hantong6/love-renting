function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    $.get('/api/session',function (reply) {
        if ('0'!=reply.errno)
        {location.href='/login.html';}
    });

    $.get('/api/auth',function (reply) {
        if('0'==reply.errno)
        {
            $('#real-name').prop({placeholder:reply.realName});
            $('#id-card').prop({placeholder:reply.idCard});
        }
        else if('4001'==reply.errno)
        {alert('查询实名信息异常，请刷新页面重试！')}
        else
        {
            $('#real-name').removeAttr('disabled');
            $('#id-card').removeAttr('disabled');
            $('.btn-success').removeAttr('disabled');
            $('.btn-success').prop({value:'提交'});
        }
    });

    $('#form-auth').submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            //Content-Type和data不需要添加，使用表单提供的原始内容即可
            url:'/api/auth',
            type:'PUT',
            headers:{'X-XSRFToken':getCookie('_xsrf')},
            dataType:'json',
            success:function (reply) {
                if ('0'==reply.errno)
                {alert('提交成功！');location.reload();}
                else
                {alert('提交失败！');}
            }
        });
    });
});

