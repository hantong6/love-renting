function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
    $.get('/api/session',function (reply) {
        if ('0'!=reply.errno)
        {location.href='/login.html';}
        else{}
    });

    $.get('/api/auth',function (reply) {
        if('0'==reply.errno)
        {
            $('.btn-commit').removeAttr('disabled');
            $('.btn-commit').prop({value:'确认信息，提交房源'});
        }
        else if('4001'==reply.errno)
        {alert('查询实名信息异常，请刷新页面重试！')}
        else {}
    });

   $.get('/api/area',function (reply) {
        if('0'==reply.errno)
        {
            // for(var i=0;i<reply.data.length;i++)
            // {$('#area-id').append('<option value="'+reply.data[i].aid+'">'+reply.data[i].aname+'</option>');}
            render_html=template('tpl_area',{areas:reply.data});
            $('#area-id').html(render_html);
        }
        else
        {alert(reply.errmsg);}
   });

   $.get('/api/facility',function (reply) {
        if('0'==reply.errno)
        {
            // for(var i=0;i<reply.data.length;i++)
            // {$('#area-id').append('<option value="'+reply.data[i].aid+'">'+reply.data[i].aname+'</option>');}
            render_html=template('tpl_facility',{facilitys:reply.facilitys});
            $('.house-facility-list').html(render_html);
        }
        else
        {alert(reply.errmsg);}

   });

   $('#form-house-info').submit(function (e) {
       e.preventDefault();
       $(document).css('cursor','wait');
       minDays=parseInt($('#house-min-days').val());
       maxDays=parseInt($('#house-max-days').val());
       if(maxDays!=0 && minDays>maxDays)
       {alert('最多入住天数不能少于最少入住天数！');return;}
       $(this).ajaxSubmit({
           url:'/api/house',
           type:'POST',
           headers:{'X-XSRFToken':getCookie('_xsrf')},
           dataType:'json',
           success:function (reply) {
                if('0'==reply.errno)
                {alert('保存成功！');location.href='/myhouse.html';}
                else
                {alert('保存失败！');$(document).css('cursor','default');}
           }
       });
    });
});