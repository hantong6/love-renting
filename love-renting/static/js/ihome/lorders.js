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

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);

    $('.modal-accept').on('click',function () {
        var orderId = $(this).attr("order-id");
        $.ajax({
            url:"/api/order",
            type:"PUT",
            data:JSON.stringify({"order_id":orderId,"action":"accept"}),
            contentType:"application/json",
            dataType:"json",
            headers:{"X-XSRFTOKEN":getCookie("_xsrf")},
            success:function (reply) {
                alert(reply.errmsg);
                if ("0" == reply.errno)
                {
                    $("#accept-modal").modal("hide");
                    $("ul.orders-list>li[order-id="+ orderId +"]>div.order-content>div.order-text>ul li:eq(4)>span").html("已接单");
                    $("ul.orders-list>li[order-id="+ orderId +"]>div.order-title>div.order-operate").hide();
                }
            }
        });
    });

    $('.modal-reject').on('click',function () {
        var orderId = $(this).attr("order-id");
        var reject_reason = $("#reject-reason").val();
        if (!reject_reason){return;}
        $.ajax({
            url:"/api/order",
            type:"PUT",
            data:JSON.stringify({"order_id":orderId,"action":"reject","reject_reason":reject_reason}),
            contentType:"application/json",
            dataType:"json",
            headers:{"X-XSRFTOKEN":getCookie("_xsrf")},
            success:function (reply) {
                alert(reply.errmsg);
                if ("0" == reply.errno)
                {
                    $("#reject-modal").modal("hide");
                    $("ul.orders-list>li[order-id="+ orderId +"]>div.order-content>div.order-text>ul li:eq(4)>span").html("已拒单");
                    $("ul.orders-list>li[order-id="+ orderId +"]>div.order-title>div.order-operate").hide();
                }
            }
        });
    });

    $.get('/api/session',{},function (reply) {
        if ('0'!=reply.errno)
        {location.href='/login.html';}
    });

    $.get('/api/order?role=landlord',function (reply) {
        if('0'==reply.errno)
        {
            $('.orders-list').html(template('tpl_order',{orders:reply.data}));

            $(".order-accept").on("click", function(){
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-accept").attr("order-id", orderId);
            });

            $(".order-reject").on("click", function(){
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-reject").attr("order-id", orderId);
            });
        }
        else
        {alert(reply.errmsg);}
    });
});