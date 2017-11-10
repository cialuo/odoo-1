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

    window.onhashchange = function () {
        $('.chose_price_line li').click(function () {
            $(this).addClass('active').siblings().removeClass('active');
            if ($(this).attr('direction') == "up") {
                render_price_down_up("up");
            } else if ($(this).attr('direction') == "down") {
                render_price_down_up("down");
            }
        });
        //渲染
        render_price_down_up("up");
    }
    // // 添加上下行的站点数据
    function render_price_down_up(direction) {
        var the_line_id = $('#the_rec_id .o_form_field').html();
        var th_str = '', td_str = '', li_str_clone = '', li_str = '', li_si_id = '';
        //因使用odoo，需定时器先把dom判断出来
        var set_pi_dom = setInterval(function () {
            if ($('body').find('.table_price_set').length > 0) {
                //如果找到dom就清除定时器
                clearInterval(set_pi_dom);
                // 查询线路
                model_line.query().order_by("sequence").filter([["route_id", "=", parseInt(the_line_id)], ["direction", "=", direction]]).all().then(function (data) {
                    if(data.length>0){
                        $('.dom_price_set').show();
                    }else{
                        $('.dom_price_set').hide();
                    }
                    $('.table_price_set thead>tr').html('');
                    // 渲染表内容
                    $('.table_price_set tbody').html('');
                    //将内容渲染到页面中
                    $('.clone_th').html('');
                    $('.div_site_id').html('<li class="div_site_title">站点Id</li>');
                    $('.div_heng_site').html('<li class="div_heng_title">名称</li>');
                    for (var st = 0; st < data.length; st++) {
                        //th的内容
                        th_str += '<th data_id=' + data[st].id + '>' + data[st].station_id[1].split('/')[0] + '</th>';
                        //左侧公交的站点内容
                        li_str += '<li>' + data[st].station_id[1].split('/')[0] + '</li>';
                        // 克隆出来漂浮的站点内容
                        li_str_clone += '<li>' + data[st].station_id[1].split('/')[0] + '</li>';
                        //行内容
                        td_str += '<td></td>';
                        // 站点id
                        li_si_id += '<li tr_id=' + data[st].id + '>' + data[st].id + '</li>';
                    }
                    td_str = '<tr>' + td_str + '</tr>'
                    //渲染表头
                    $('.table_price_set thead>tr').append(th_str);
                    // 渲染表内容
                    for (var td = 0; td < data.length; td++) {
                        $('.table_price_set tbody').append(td_str);
                        for (var ti = 0; ti <= td; ti++) {
                            $('.table_price_set tbody tr').eq(td).find('td').eq(ti).append('<input type="text">');
                        }
                    }
                    //将内容渲染到页面中
                    $('.clone_th').append(li_str_clone);
                    $('.div_site_id').append(li_si_id);
                    $('.div_heng_site').append(li_str);
                    //查询价格
                    model_price.query().filter([["direction", "=", direction]]).all().then(function (data_p) {
                        //根据数据渲染票价
                        for (var m = 0; m < data_p.length; m++) {
                            var td_id_index = $('.table_price_set thead th[data_id=' + data_p[m].start_station_id[0] + ']').index();
                            var tr_id_index = parseInt($('.div_site_id li[tr_id=' + data_p[m].end_station_id[0] + ']').index()) - 1;
                            $('.table_price_set tbody tr').eq(tr_id_index).find('td').eq(td_id_index).addClass('has_price').attr('change_id', data_p[m].id).find('input').val(data_p[m].price);
                        }
                        // 设置悬浮站点位置
                        var of_left = ($(window).width() - 1172) / 2 + 60 + 8 + 120;
                        $('.o_content').scroll(function () {
                            //悬浮框
                            if ($(this).scrollTop() >= 544) {
                                $('.o_content').addClass('pos_re');
                                $('.clone_th_pa').show().css({
                                    'top': $(this).scrollTop() + 'px',
                                    'left': of_left + 'px'
                                });
                            } else if ($(this).scrollTop() <= 574) {
                                $('.o_content').removeClass('pos_re');
                                $('.clone_th_pa').hide();
                            }
                        });
                        $('.table_price_set_pa').scroll(function () {
                            //先找出距离左边固定的宽度
                            $('.clone_th').css('left', 0 - $(this).scrollLeft() + 'px');
                        });
                    });
                    //修改或者添加价格
                    $('.table_price_set tbody input').on('blur', function () {
                            var val_change_price = $(this).val();
                            var parnt = /^\d+(?=\.{0,1}\d+$|$)/;
                            var tr_index = $(this).parents('tr').index();
                            var td_index = $(this).parent('td').index();
                            var price_end_id = $('.div_site_id li').eq(parseInt(tr_index) + 1).html()
                            var price_start_id = $('.table_price_set th').eq(td_index).attr('data_id');
                            // 如果输入为空
                            if (val_change_price == '') {
                                // 如果此票价一开始是有的
                                if ($(this).parent().hasClass('has_price')) {
                                    // unlink掉
                                    model_price.call("unlink", [parseInt($(this).parent().attr('change_id'))]).then(function () {

                                    });
                                    // 如果一开始票价没有 则忽略
                                } else {

                                }
                                // 如果输入不为空
                            } else {
                                // 校验通过
                                if (parnt.test(val_change_price)) {
                                    //如果是修改
                                    if ($(this).parent().hasClass('has_price')) {
                                        model_price.call("write", [parseInt($(this).parent().attr('change_id')),
                                            {
                                                "route_id": parseInt(the_line_id),
                                                'start_station_id': parseInt(price_start_id),
                                                'end_station_id': parseInt(price_end_id),
                                                "price": parseFloat(val_change_price),
                                                "direction": direction
                                            }]).then(function () {
                                            $(this).parent().addClass('has_price');
                                        });
                                        //如果是新加
                                    } else {
                                        model_price.call("create", [
                                            {
                                                'route_id': parseInt(the_line_id),
                                                'start_station_id': parseInt(price_start_id),
                                                'end_station_id': parseInt(price_end_id),
                                                "price": parseFloat(val_change_price),
                                                "direction": direction
                                            }]).then(function (res) {
                                            $(this).parent().addClass('has_price').attr('change_id', res);
                                        });
                                    }
                                } else {
                                    layer.msg('请输入票价为正数', {time: 1000, shade: 0.3});
                                    $(this).val('');
                                }
                            }
                        }
                    );
                });
            }
        }, 300);
    }


});