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
    $.get('/api/session',{},function (reply) {
        if ('0'!=reply.errno)
        {location.href='/login.html';}
    });

    $.get('/api/userinfo',function (reply) {
        $('#user-avatar').prop({src:reply.avatar});
        $('#user-name').prop({placeholder:reply.name});
    });

    $('#form-avatar').submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            //Content-Type和data不需要添加，使用表单提供的原始内容即可
            url:'/api/avatar',
            type:'PUT',
            headers:{'X-XSRFToken':getCookie('_xsrf')},
            dataType:'json',
            success:function (reply) {
                if ('0'==reply.errno)
                {$('#user-avatar').prop({src:reply.avatarUrl});}
                else if ('4101'==reply.errno)
                {location.href='/login.html';}
                else
                {alert('头像上传失败');}
            }
        });
    });

    $('#form-name').submit(function (e) {
       e.preventDefault();
       name=$('#user-name').val();
       if(!name){return;}
       $(this).ajaxSubmit({
           url:'/api/userinfo',
           type:'PUT',
           headers:{'X-XSRFToken':getCookie('_xsrf')},
           dataType:'json',
           success:function (reply) {
                if('0'==reply.errno)
                {alert('保存成功！');location.reload();}
                else
                {alert('保存失败！');}
           }
       });
    });
});

