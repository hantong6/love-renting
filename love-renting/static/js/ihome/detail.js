function hrefBack() {
    history.go(-1);
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

$(document).ready(function(){
    var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationType: 'fraction'
    });
    $(".book-house").show();

    $.get('/api/session',function (reply) {
        if ('0'!=reply.errno)
        {location.href='/login.html';}
        else
        {$('.book-house').prop({href:'/booking.html?id='+getQueryString('id')});}
    });

    $.get('/api/house/detail?house_id='+getQueryString('id'),function (reply) {
        if(reply.avatar)
        {$('.landlord-pic img').prop({src:reply.avatar});}
        if(reply.house)
        {
            $('.landlord-name span').html(reply.house['name']);
            $('.swiper-slide img').prop({src:reply.house['image_url']});
            $('.house-price span').html(reply.house['price']);
            $('.house-title').html(reply.house['title']);
            $('.house-info-list li').eq(0).html(reply.house['address']);
            $('.icon-text h3').eq(0).html('出租'+reply.house['room_count']+'间');
            $('.icon-text p').eq(0).html('房屋面积：'+reply.house['acreage']+'平米');
            $('.icon-text p').eq(1).html('房屋户型：'+reply.house['house_unit']);
            $('.icon-text h3').eq(1).html('宜住'+reply.house['capacity']+'人');
            $('.icon-text p').eq(2).html(reply.house['beds']);
            $('.house-info-list li span').eq(0).html(reply.house['deposit']);
            $('.house-info-list li span').eq(1).html(reply.house['min_days']);
            if(reply.house['max_days'])
            {$('.house-info-list li span').eq(2).html(reply.house['max_days']);}
            else
            {$('.house-info-list li span').eq(2).html('无限制');}
            if(reply.house['client_id']==reply.house['user_id'])
            {$('.book-house').hide();}
        }
        if(reply.facility)
        {
            for(var i=0;i<reply.facility.length;i++)
            {
                if(1==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="wirelessnetwork-ico"></span>无线网络</li>');}
                if(13==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="shower-ico"></span>热水淋浴</li>');}
                if(2==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="aircondition-ico"></span>空调</li>');}
                if(14==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="heater-ico"></span>暖气</li>');}
                if(3==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="smoke-ico"></span>允许吸烟</li>');}
                if(15==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="drinking-ico"></span>饮水设备</li>');}
                if(4==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="brush-ico"></span>牙具</li>');}
                if(16==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="soap-ico"></span>香皂</li>');}
                if(5==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="slippers-ico"></span>拖鞋</li>');}
                if(17==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="toiletpaper-ico"></span>手纸</li>');}
                if(6==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="towel-ico"></span>毛巾</li>');}
                if(18==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="toiletries-ico"></span>沐浴露、洗发露</li>');}
                if(7==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="icebox-ico"></span>冰箱</li>');}
                if(19==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="washer-ico"></span>洗衣机</li>');}
                if(8==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="elevator-ico"></span>电梯</li>');}
                if(20==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="iscook-ico"></span>允许做饭</li>');}
                if(9==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="pet-ico"></span>允许带宠物</li>');}
                if(21==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="meet-ico"></span>允许聚会</li>');}
                if(10==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="accesssys-ico"></span>门禁系统</li>');}
                if(22==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="parkingspace-ico"></span>停车位</li>');}
                if(11==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="wirednetwork-ico"></span>有线网络</li>');}
                if(23==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="tv-ico"></span>电视</li>');}
                if(12==reply.facility[i]['facility_id'])
                {$('.house-facility-list').append('<li><span class="jinzhi-ico"></span>浴缸</li>');}
            }
        }
        if(reply.comment)
        {
            render_html=template('tpl_comment',{comments:reply.comment});
            $('.house-comment-list').append(render_html);
        }
    });
});