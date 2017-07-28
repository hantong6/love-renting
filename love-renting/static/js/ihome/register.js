function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var captchaId = "";

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}

function generateImageCode() {
    captchaId=generateUUID();
    var captchaUrl='/api/captcha?id='+captchaId;
    $('.image-code img').prop({src:captchaUrl});
}

function sendSMSCode() {
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    } 
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }
    $.get("/api/sms", {mobile:mobile, text:imageCode, id:captchaId}, function(data){
            if ('0' != data.errno) {
                if ('4004'==data.errno)
                {
                    $("#image-code-err span").html(data.errmsg);
                    $("#image-code-err").show();
                    generateImageCode();
                }
                else
                {
                    $("#phone-code-err span").html(data.errmsg);
                    $("#phone-code-err").show();
                }
                $(".phonecode-a").attr("onclick", "sendSMSCode();");
            }   
            else {
                var $time = $(".phonecode-a");
                var duration = 60;
                var intervalid = setInterval(function(){
                    $time.html(duration + "秒"); 
                    if(duration === 1){
                        clearInterval(intervalid);
                        $time.html('获取验证码'); 
                        $(".phonecode-a").attr("onclick", "sendSMSCode();");
                    }
                    duration--;
                },1000,60);
            }
    }, 'json'); 
}

$(document).ready(function() {
    generateImageCode();
    $("#mobile").focus(function(){
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function(){
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function(){
        $("#phone-code-err").hide();
    });
    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });
    $(".form-register").submit(function(e){
        e.preventDefault();
        var mobile = $("#mobile").val();
        var phoneCode = $("#phonecode").val();
        var passwd = $("#password").val();
        var passwd2 = $("#password2").val();
        if (!mobile) {
            $("#mobile-err span").html("请填写正确的手机号！");
            $("#mobile-err").show();
            return;
        } 
        if (!phoneCode) {
            $("#phone-code-err span").html("请填写短信验证码！");
            $("#phone-code-err").show();
            return;
        }
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        if (passwd != passwd2) {
            $("#password2-err span").html("两次密码不一致!");
            $("#password2-err").show();
            return;
        }
        /*快捷提取表单字段值
        var data={};
        $('.form-register').serializeArray().map(function (x) {data[x.name]=x.value});
        */
        var data={'mobile':mobile,'password':passwd,'password2':passwd2,'phonecode':phoneCode};
        $.ajax({
            url:'/api/user',
            type:'PUT',
            contentType:'application/json',
            //将data转化为json格式发送
            data:JSON.stringify(data),
            headers:{'X-XSRFToken':getCookie('_xsrf')},
            dataType:'json',
            success:function (reply) {
                        if (reply.errno=='0')
                            {location.href='/index.html';}
                        else if (reply.errno=='4101')
                            {location.href='/login.html';}
                        else
                            {
                                $('#password2-err span').html(reply.errmsg);
                                $('#password2-err').show();
                            }
                    }
        });
    });
});