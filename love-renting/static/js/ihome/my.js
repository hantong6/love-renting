function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
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
    $.get('/api/session',{},function (reply) {
        if ('0'!=reply.errno)
        {location.href='/login.html';}
    });

    $.get('/api/userinfo',function (reply) {
        $('#user-avatar').prop({src:reply.avatar});
        $('#user-name').html(reply.name);
        $('#user-mobile').html(reply.mobile);
    });
});