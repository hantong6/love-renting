function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
    });
    $(".form-login").submit(function(e){
        e.preventDefault();
        mobile = $("#mobile").val();
        passwd = $("#password").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }

        $.ajax({
            url:'/api/session',
            type:'PUT',
            contentType:'application/json',
            data:JSON.stringify({'mobile':mobile,'passwd':passwd}),
            headers:{'X-XSRFToken':getCookie('_xsrf')},
            dataType:'json',
            success:function (reply) {
                if ('4106'==reply.errno)
                {
                    $('#password-err span').html(reply.errmsg);
                    $('#password-err').show();
                }
                else if ('0'==reply.errno)
                {location.href='/index.html';}
                else
                {
                    $('#mobile-err span').html(reply.errmsg);
                    $('#mobile-err').show();
                }
            }
        });
    });
});