/**
 * Created by Administrator on 2017/11/7.
 */
odoo.define('price_setting', function (require) {
    "use strict";
    var Model = require('web.Model');
    // var model = new Model("scheduleplan.busmovetime");
    var model_line = new Model('opertation_resources_station_platform');
    var model_price = new Model('opertation_resources_ticket_price');
    // 切换上下行路线
    $('.chose_price_line li').click(function () {
        $(this).addClass('active').siblings().removeClass('active');
    });
    // // 添加上下行的站点数据

    var the_line_id = $('#the_rec_id .o_form_field').html();
    $('.price_table thead>tr').append(th_str);
    var site_t = [];
    var th_str = '';
    var td_str = '';
    var li_str_clone = '';
    var li_str = '';
    var set_pi_dom = setInterval(function () {
        if ($('body').find('.table_price_set').length > 0) {
            clearInterval(set_pi_dom)
            model_line.query().filter([["route_id", "=", parseInt(the_line_id)]]).all().then(function (data) {
                console.log(data);
                for (var st = 0; st < data.length; st++) {
                    th_str += '<th>' + data[st].station_id[1].split('/')[0] + '</th>';
                    li_str += '<li>' + data[st].station_id[1].split('/')[0] + '</li>';
                    li_str_clone += '<li>' + data[st].station_id[1].split('/')[0] + '</li>';
                    td_str += '<td><input type="text"></td>';
                }
                td_str = '<tr>' + td_str + '</tr>'
                $('.table_price_set thead>tr').append(th_str);
                for (var td = 0; td < data.length; td++) {
                    $('.table_price_set tbody').append(td_str);
                }
                $('.clone_th').append(li_str_clone);
                $('.div_heng_site').append(li_str);
                model_price.query().filter().all().then(function (data_p) {
                    var of_left = ($(window).width() - 1172) / 2 +8 + 120;
                    $('.o_content').scroll(function () {
                        if ($(this).scrollTop() >= 544) {
                            $('.o_content').addClass('pos_re');
                            $('.clone_th_pa').show().css({'top':$(this).scrollTop()+'px','left':of_left+'px'});
                            // $('.table_price_set thead').css('top',$(this).scrollTop()+'px');
                        } else {
                            $('.o_content').removeClass('pos_re');
                            $('.clone_th_pa').hide();
                        }
                    });
                    $('.table_price_set_pa').scroll(function () {
                        //先找出距离左边固定的宽度
                        $('.clone_th').css('left',0-$(this).scrollLeft()+'px');
                    });

                });
            });
        }
    }, 300);
})
;