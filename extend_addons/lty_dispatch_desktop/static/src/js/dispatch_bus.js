/**
 * Created by Administrator on 2017/7/18.
 */
odoo.define('lty_dispaych_desktop.getWidget', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var Model = require('web.Model');
    var QWeb = core.qweb;
    var dispatch_updown_line = require('lty_dispaych_desktop.updown_line');
    var bus_source_config = require('lty_dispatch_desktop.bus_source_config');
    var bus_site_info = require('lty_dispatch_desktop.bus_site_info');
    var bus_real_info = require('lty_dispatch_desktop_widget.bus_real_info');
    var passenger_flow = require('lty_dispatch_desktop_widget.passenger_flow');
    var plan_display = require('lty_dispatch_desktop_widget.plan_display').plan_display;
    //最原始车辆组件
    var dispatch_canvas = Widget.extend({
        template: 'dispatch_desktop',
        init: function (parent, data, rendr_index) {
            this._super(parent);
            // 线路info
            this.model_line = new Model('dispatch.control.desktop.component');
            // 线路
            this.model_choseline = new Model('route_manage.route_manage');
            // 上下行站点
            this.model_station_platform = new Model('opertation_resources_station_platform');
            // 线路资源
            this.model_linesrc = new Model('scheduleplan.excutetable');
            //控制台
            this.model_config = new Model('dispatch.control.desktop');
            //odoo提供数据
            this.dis_desk = data;
            //传进来的index层级的值
            this.rendr_index = rendr_index;
        },
        start: function () {
            var self = this;
            //控制台id
            this.desktop_id = this.$el.parents(".back_style").attr("desktop_id");
            //线路id
            this.line_id = self.$el.attr('line_id');
            //为了每条线路对应左右两个模块的tid相同问题
            var tid = self.$el.attr('tid');
            this.gprs_id = self.$el.attr('gprs_id');
            //所有点击的按钮移除click属性并给当前的添加
            $('*[click="yes"]').removeAttr('click');
            this.$el.attr("click", "yes");
            //串车小部件显示串车详情
            self.$('.traffic_car').on('click', '.same_car_show', function (event) {
                var x = event.currentTarget;
                var zIndex = parseInt(self.$el[0].style.zIndex) + 1;
                if (!$(x).hasClass('beChose')) {
                    $(x).addClass('beChose').html('<div class="nzindex">' + $(x).siblings('.data_same').html() + '</div>');
                    $(x).find('.nzindex').css('zIndex', zIndex);
                    setTimeout(function () {
                        $(x).removeClass('beChose').html('...');
                    }, 5000);
                } else {
                    $(x).removeClass('beChose').html('...');
                }
            });
            //点击所串车辆打开车内详情
            self.$('.traffic_car').on('click', '.same_car_show>div>div', function (event) {
                stopPropagation(event);
                var car_num = $(event.currentTarget).html();
                var car_id = $(event.currentTarget).attr("car_id");
                var zIndex = parseInt(self.$el[0].style.zIndex) + 1;
                var options =
                    {
                        x: event.clientX + 5,
                        y: event.clientY + 5 - 60,
                        zIndex: zIndex,
                        line_id: self.line_id,
                        line_name: self.$el.attr("line_name"),
                        car_num: car_num,
                        car_id: car_id,
                        controllerId: self.desktop_id
                    };
                if ($(".busRealStateModel_" + options.line_id + "_" + options.car_num).length > 0) {
                    return;
                } else {
                    $(".busRealStateModel").remove();
                    var dialog = new bus_real_info(self, options);
                    dialog.appendTo($(".controller_" + options.controllerId));
                }
            });

            function site_info(mode_line, model_station_platform, model_src, model_config) {
                if (self.$el.find('.line_line')[0] != undefined) {
                    // 根据tid拿到线路id
                    mode_line.query().filter([["id", "=", parseInt(tid)]]).all().then(function (data) {
                        // 根据线路id拿到线路的数据
                        model_station_platform.query().order_by("sequence").filter([["route_id", "=", data[0].line_id[0]], ["direction", "=", "up"]]).all().then(function (res_top) {
                            model_station_platform.query().order_by("sequence").filter([["route_id", "=", data[0].line_id[0]], ["direction", "=", "down"]]).all().then(function (res_down) {
                                var site_t = [];
                                for (var st = 0; st < res_top.length; st++) {
                                    site_t.push(res_top[st].station_id[1].split('/')[0]);
                                }
                                sessionStorage.setItem("bus_site_top" + self.line_id, site_t);
                                // 给每个上下行的车辆所在位置添加一个盒子，后面用来装和判断是否发生串车
                                for (var it = 0; it < res_top.length * 2; it++) {
                                    self.$el.find('.content_car_road_top').append('<div class="car_line_tb car_line_top' + it + '"></div>');
                                    self.$el.find('.car_line_top' + it).css('left', 1190 * (it + 1) / (res_top.length * 2) + 'px');
                                }
                                for (var id = 0; id < res_down.length * 2; id++) {
                                    self.$el.find('.content_car_road_down').append('<div class="car_line_tb car_line_down' + id + '"></div>');
                                    self.$el.find('.car_line_down' + id).css('left', 1990 - 1190 * (id + 1) / (res_down.length * 2) + 'px');
                                }
                                // 查询模拟地图上方车辆信息
                                model_config.query().filter([["id", "=", parseInt(self.desktop_id)]]).all().then(function (conf) {

                                    // 用来做上方信息的可配置显示与否
                                    // 配车数量
                                    if (conf[0].applycar_num == true) {
                                        self.$el.find('.show_applycar_num').show();
                                    }
                                    // 机动车辆
                                    if (conf[0].active_car == true) {
                                        self.$el.find('.show_active_car').show();
                                    }
                                    // 维保停运
                                    if (conf[0].main_outage == true) {
                                        self.$el.find('.show_main_outage').show();
                                    }
                                    // 共享机动
                                    if (conf[0].share_active_car == true) {
                                        self.$el.find('.show_share_active_car').show();
                                    }
                                    // 信号在线
                                    if (conf[0].signal_online == true) {
                                        self.$el.find('.show_signal_online').show();
                                    }
                                    // 信号在线
                                    if (conf[0].signal_outline == true) {
                                        self.$el.find('.show_signal_outline').show();
                                    }
                                    // 司机
                                    if (conf[0].car_driver == true) {
                                        self.$el.find('.show_car_driver').show();
                                    }
                                    // 乘务员
                                    if (conf[0].car_attendant == true) {
                                        self.$el.find('.show_car_attendant').show();
                                    }
                                    //挂车数量
                                    if (conf[0].trailerNum == true) {
                                        self.$el.find('.show_trailerNum').show();
                                    }
                                    var dataSite_top_color_cof = {};
                                    var dataSite_down_color_cof = {};
                                    var res_down_deal = res_down.reverse();
                                    var site_d = [];
                                    //将站点信息缓存起来，车辆资源模块调用
                                    for (var sd = 0; sd < res_down_deal.length; sd++) {
                                        site_d.push(res_down_deal[sd].station_id[1].split('/')[0]);
                                    }
                                    sessionStorage.setItem("bus_site_down" + self.line_id, site_d);
                                    self.$el.find('.bus_info>ul>li').css('color', conf[0].src_font_conf);
                                    for (var i = 0; i < res_top.length; i++) {
                                        var color = 'color' + res_top[i].id;
                                        dataSite_top_color_cof[color] = '#18d76b';
                                    }
                                    for (var i = 0; i < res_down_deal.length; i++) {
                                        var color = 'color' + res_down_deal[i].id;
                                        dataSite_down_color_cof[color] = '#18d76b';
                                    }
                                    // 上下行的车辆描圈
                                    var cirTop = {
                                        id: '.can_top',
                                        ciry: 27,
                                        testy: 13,
                                        // color: data.color,
                                        self: self.$el,
                                        dataSite_color: dataSite_top_color_cof,
                                        site_infos: res_top
                                    };
                                    var cirBottom = {
                                        id: '.can_bottom',
                                        ciry: 6,
                                        testy: 25,
                                        self: self.$el,
                                        // color: data.color,
                                        dataSite_color: dataSite_down_color_cof,
                                        site_infos: res_down_deal
                                    };
                                    // 上下行的名称显示
                                    cir_and_text(cirTop);
                                    cir_and_text(cirBottom);
                                    self.site_top_infos = res_top;
                                    self.site_down_infos = res_down_deal;
                                    // 站点颜色
                                    self.dataSite_top_color = dataSite_top_color_cof;
                                    self.dataSite_down_color = dataSite_down_color_cof;
                                    self.subsection = '';
                                    var model_id = "line_message__" + self.line_id;
                                    if (socket_model_info[model_id]) {
                                        delete socket_model_info[model_id];
                                    }
                                    // 查询显示车辆上方数据
                                    $.ajax({
                                        url: RESTFUL_URL + '/ltyop/dispatchRealtimeStatus/cachelineStat?apikey=71029270&params={"gprsId":' + self.gprs_id + '}',
                                        type: 'get',
                                        async: false,
                                        dataType: 'json',
                                        data: {},
                                        success: function (data) {
                                            console.log(data)
                                            if (data) {
                                                //配车数量
                                                self.$el.find('.show_applycar_num span').html(data[0].withBus);
                                                //挂车数量
                                                self.$el.find('.show_trailerNum span').html(data[0].runBus);
                                                //机动车辆
                                                self.$el.find('.show_active_car span').html(data[0].motorBus);
                                                // 信号在线
                                                self.$el.find('.show_signal_online span').html(data[0].online);
                                                //信号掉线
                                                self.$el.find('.show_signal_outline span').html(data[0].offline);
                                                //司机
                                                self.$el.find('.show_car_driver span').html(data[0].driver);
                                                //乘务
                                                self.$el.find('.show_car_attendant span').html(data[0].train);
                                                self.$el.find('.park_left li').eq(0).html(data[0].upReturnLevel1);
                                                self.$el.find('.park_left li').eq(1).html(data[0].upReturnLevel2);
                                                self.$el.find('.park_left li').eq(2).html(data[0].upReturnLevel3);
                                                self.$el.find('.park_left li').eq(3).html(data[0].upReturnLevel4);
                                                self.$el.find('.park_right li').eq(3).html(data[0].downReturnLevel1);
                                                self.$el.find('.park_right li').eq(2).html(data[0].downReturnLevel2);
                                                self.$el.find('.park_right li').eq(1).html(data[0].downReturnLevel3);
                                                self.$el.find('.park_right li').eq(0).html(data[0].downReturnLevel4);
                                                $.ajax({
                                                    url: RESTFUL_URL + '/ltyop/dispatchRealtimeStatus/cacheDrivingStat?apikey=71029270&params={"gprsId":"' + self.gprs_id + '"}',
                                                    type: 'get',
                                                    async: false,
                                                    dataType: 'json',
                                                    data: {},
                                                    success: function (res) {
                                                        for (var i = 0; i < res.length; i++) {
                                                            $('.run_car_hide').find('.line_car').attr('bus_no', res[i].onboard);
                                                            if (res[i].onlineFlag == 0) {
                                                                $('.run_car_hide').find('.line_car').removeClass('to_gray');
                                                            } else if (res[i].onlineFlag == 1) {
                                                                $('.run_car_hide').find('.line_car').addClass('to_gray');
                                                            }
                                                            // 上下行
                                                            if (res[i].direction == 0) {
                                                                //是否在车场
                                                                if (res[i].stationFlag != 2) {
                                                                    if (res[i].stationFlag == 0) {
                                                                        self.$el.find('.content_car_road_top .car_line_top' + (parseInt(res[i].stationNo) * 2 - 2)).append($('.run_car_hide').html());
                                                                        var oLeft = 1190 * (parseInt(res[i].stationNo) - 0.5) / res_top.length;
                                                                    } else if (res[i].stationFlag == 1) {
                                                                        self.$el.find('.content_car_road_top .car_line_top' + (parseInt(res[i].stationNo) * 2 - 1)).append($('.run_car_hide').html());
                                                                        var oLeft = 1190 * (parseInt(res[i].stationNo)) / res_top.length;
                                                                    }
                                                                    self.$('.content_car_road_top').find('.line_car[bus_no=' + res[i].onboard + ']').css('left', oLeft - 15 + 'px');
                                                                    self.$('.content_car_road_top').find('.line_car[bus_no=' + res[i].onboard + ']').find('.type_car span').attr("car_id", res[i].car_id).html(res[i].onboard);
                                                                }
                                                            } else if (res[i].direction == 1) {
                                                                if (res[i].stationFlag != 2) {
                                                                    // 进站   出站
                                                                    if (res[i].stationFlag == 0) {
                                                                        self.$el.find('.content_car_road_down .car_line_down' + (parseInt(res[i].stationNo) * 2 - 2)).append($('.run_car_hide').html());
                                                                        var oLeft = 1190 - 1190 * (parseInt(res[i].stationNo) - 0.5) / res_down_deal.length;
                                                                    } else if (res[i].stationFlag == 1) {
                                                                        self.$el.find('.content_car_road_down .car_line_down' + (parseInt(res[i].stationNo) * 2 - 1)).append($('.run_car_hide').html());
                                                                        var oLeft = 1190 - 1190 * (parseInt(res[i].stationNo)) / res_down_deal.length;
                                                                    }

                                                                    self.$('.content_car_road_down').find('.line_car[bus_no=' + res[i].onboard + ']').css('left', oLeft - 15 + 'px');
                                                                    self.$('.content_car_road_down').find('.line_car[bus_no=' + res[i].onboard + ']').find('.type_car span').attr("car_id", res[i].car_id).html(res[i].onboard);
                                                                }
                                                            }
                                                        }
                                                        for (var aj_nu = 0; aj_nu < self.$('.content_car_road_top .car_line_tb').length; aj_nu++) {
                                                            //移除之前的重复位置
                                                            //如果已经有两辆车
                                                            self.$('.content_car_road_top .car_line_top' + aj_nu).find('.same_car_show').remove();
                                                            self.$('.content_car_road_top .car_line_top' + aj_nu).find('.data_same').remove();
                                                            if (self.$('.content_car_road_top .car_line_top' + aj_nu).find('.line_car').length > 1) {
                                                                var html_c = '';
                                                                for (var i = 0; i < self.$('.content_car_road_top .car_line_top' + aj_nu).find('.line_car').length; i++) {
                                                                    var carObj = self.$('.content_car_road_top .car_line_top' + aj_nu).find('.line_car .type_car span').eq(i);
                                                                    html_c += '<div car_id=' + carObj.attr("car_id") + '>' + carObj.html() + '</div>';
                                                                }
                                                                self.$('.content_car_road_top .car_line_top' + aj_nu).append('<div class="same_car_show" style="left: ' + (parseFloat(self.$('.content_car_road_top .car_line_top' + aj_nu).find('.line_car').css('left')) - 50) + 'px">...</div><span style="display: none" class="data_same"></span>')
                                                                self.$('.content_car_road_top .car_line_top' + aj_nu).find('.data_same').html(html_c);
                                                            }
                                                        }
                                                        for (var aj_num = 0; aj_num < self.$('.content_car_road_down .car_line_tb').length; aj_num++) {
                                                            //移除之前的重复位置
                                                            //如果已经有两辆车
                                                            self.$('.content_car_road_down .car_line_down' + aj_num).find('.same_car_show').remove();
                                                            self.$('.content_car_road_down .car_line_down' + aj_num).find('.data_same').remove();
                                                            if (self.$('.content_car_road_down .car_line_down' + aj_num).find('.line_car').length > 1) {
                                                                var html_cd = '';
                                                                for (var i = 0; i < self.$('.content_car_road_down .car_line_down' + aj_num).find('.line_car').length; i++) {
                                                                    var carObj = self.$('.content_car_road_down .car_line_down' + aj_num).find('.line_car .type_car span').eq(i);
                                                                    html_cd += '<div car_id=' + carObj.attr("car_id") + '>' + carObj.html() + '</div>';
                                                                }
                                                                self.$('.content_car_road_down .car_line_down' + aj_num).append('<div class="same_car_show" style="left: ' + (parseFloat(self.$('.content_car_road_down .car_line_down' + aj_num).find('.line_car').css('left')) + 30) + 'px">...</div><span style="display: none" class="data_same"></span>')
                                                                self.$('.content_car_road_down .car_line_down' + aj_num).find('.data_same').html(html_cd);
                                                            }
                                                        }
                                                        $('.run_car_hide').find('.line_car').removeClass('to_gray');
                                                        can_left_right(
                                                            {
                                                                id: '.canvas_left',
                                                                color: '#252B43',
                                                                ciry: 27,
                                                                self: self.$el,
                                                                r: 4,
                                                                lineLen: 17,
                                                                sta: 1,
                                                                busNumber: data[0].upFieldBusNum + '辆'
                                                            }
                                                        );
                                                        can_left_right(
                                                            {
                                                                id: '.canvas_right',
                                                                color: '#252B43',
                                                                ciry: 27,
                                                                self: self.$el,
                                                                r: 4,
                                                                lineLen: 0,
                                                                sta: 1.5,
                                                                busNumber: data[0].downFieldBusNum + '辆'
                                                            }
                                                        );
                                                        socket_model_info[model_id] =
                                                            {
                                                                fn: self.site_websocket,
                                                                arg: {
                                                                    self: self,
                                                                    line_id: self.line_id,
                                                                    desktop_id: self.desktop_id,
                                                                    site_top_infos: res_top,
                                                                    site_down_infos: res_down_deal,     //此处修改
                                                                    dataSite_top_color_cof: dataSite_top_color_cof,
                                                                    dataSite_down_color_cof: dataSite_down_color_cof,
                                                                    busTopNumber: data[0].upFieldBusNum + '辆',
                                                                    busDownNumber: data[0].downFieldBusNum + '辆',
                                                                    hasCar: []
                                                                }
                                                            };
                                                    },
                                                    error: function () {
                                                        layer.msg('请求出错', {time: 1000, shade: 0.3});
                                                    }
                                                });
                                            }
                                        },
                                        error: function () {
                                            layer.msg('请求出错', {time: 1000, shade: 0.3});
                                        }
                                    });
                                });
                            });
                        });
                    });
                }
            }

            site_info(this.model_line, this.model_station_platform, this.model_linesrc, this.model_config);
            //阻止右键引起的默认事件必须使用contextmenu,暂时功能弃用
            // self.$('.can_top').bind('contextmenu', function () {
            //     return false;
            // });
            // self.$('.can_bottom').bind('contextmenu', function () {
            //     return false;
            // });
        },
        site_websocket: function (data_list, arg) {
            var self = arg.self;
            var data_use = JSON.parse(data_list)
            var data = new Object();
            var line_c = parseInt(arg.line_id);
            //车辆在途刷新  后期socket推送
            if (data_use.moduleName == "line_park" || data_use.moduleName == "line_online") {
                $.ajax({
                    url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename:"op_busresource",controlsId:' + self.desktop_id + ',lineId:' + line_c + '}',
                    type: 'get',
                    dataType: 'json',
                    data: {},
                    success: function (data) {
                        bus_way_top = bus_way_down = 0;
                        for (var i = 0; i < data.respose.length; i++) {
                            if (data.respose[i].direction == 0 && data.respose[i].inField == 0) {
                                bus_way_top++;
                            }
                            else if (data.respose[i].direction == 1 && data.respose[i].inField == 0) {
                                bus_way_down++;
                            }
                        }
                        self.$el.find('.park_left li').html(bus_way_top);
                        self.$el.find('.park_right li').html(bus_way_down);
                    },
                    error: function () {
                        layer.msg('请求出错', {time: 1000, shade: 0.3});
                    }
                });
            }

            //匹配line_id和desktop_id
            if (data_use.data.line_id == line_c && data_use.controllerId == self.desktop_id) {
                if (data_use.moduleName == "line_park" || data_use.moduleName == "line_online") {
                    $.ajax({
                        url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename:"op_busresource",controlsId:' + self.desktop_id + ',lineId:' + line_c + '}',
                        type: 'get',
                        dataType: 'json',
                        data: {},
                        success: function (data) {
                            bus_way_top = bus_way_down = 0;
                            for (var i = 0; i < data.respose.length; i++) {
                                if (data.respose[i].direction == 0 && data.respose[i].inField == 0) {
                                    bus_way_top++;
                                }
                                else if (data.respose[i].direction == 1 && data.respose[i].inField == 0) {
                                    bus_way_down++;
                                }
                            }
                            self.$el.find('.park_left li').html(bus_way_top);
                            self.$el.find('.park_right li').html(bus_way_down);
                        },
                        error: function () {
                            layer.msg('请求出错', {time: 1000, shade: 0.3});
                        }
                    });
                }
                if (data_use.moduleName == "bus_resource") {
                    // debugger
                }
                //线路状态分段颜色   目前使用的假数据
                data.color = [
                    "#4dcf22",
                    "#ffd233",
                    "#cc2111",
                    "#f69144",
                    "#a19dde",
                    "#cc21ff"
                ];
                // 线路路况实时反馈
                // if(data_use.type== "1032"){
                //     debugger
                //     var road_info = data_use.data.road_condition.split('|');
                //     for(var i = 0;i<road_info.length;i++){
                //         data.color.push(parseInt(road_info[i].split(',')[0]));
                //     }
                // }
                data.site_top_infos = arg.site_top_infos;
                data.site_down_infos = arg.site_down_infos;
                //站点滞站客流  根据状态值决定显示
                if (data_use.type == "1036") {
                    if (data_use.data.direction == 0) {
                        var color_id = data_use.data.location_id;
                        arg.dataSite_top_color_cof['color' + color_id] = data_use.data.state;
                        for (var each in  arg.dataSite_top_color_cof) {
                            if (arg.dataSite_top_color_cof[each] == 1) {
                                arg.dataSite_top_color_cof[each] = '#123145';
                            } else if (arg.dataSite_top_color_cof[each] == 2) {
                                arg.dataSite_top_color_cof[each] = '#1dd345';
                            } else if (arg.dataSite_top_color_cof[each] == 3) {
                                arg.dataSite_top_color_cof[each] = '#123c45';
                            } else if (arg.dataSite_top_color_cof[each] == 4) {
                                arg.dataSite_top_color_cof[each] = '#f12345';
                            } else if (arg.dataSite_top_color_cof[each] == 5) {
                                arg.dataSite_top_color_cof[each] = '#1c2345';
                            }
                        }
                    } else {
                        var color_id = data_use.data.location_id;
                        arg.dataSite_down_color_cof['color' + color_id] = data_use.data.state;
                        for (var each in arg.dataSite_down_color_cof) {
                            // 路况色值配置项
                            if (arg.dataSite_down_color_cof[each] == 1) {
                                arg.dataSite_down_color_cof[each] = 'green';
                            } else if (arg.dataSite_down_color_cof[each] == 2) {
                                arg.dataSite_down_color_cof[each] = 'yellow';
                            } else if (arg.dataSite_down_color_cof[each] == 3) {
                                arg.dataSite_down_color_cof[each] = 'orange';
                            } else if (arg.dataSite_down_color_cof[each] == 4) {
                                arg.dataSite_down_color_cof[each] = 'red';
                            } else if (arg.dataSite_down_color_cof[each] == 5) {
                                arg.dataSite_down_color_cof[each] = 'blue';
                            }
                        }
                    }
                }
                data.dataSite_top_color = arg.dataSite_top_color_cof;
                data.dataSite_down_color = arg.dataSite_down_color_cof;
                // 车场车辆
                if (data_use.type == "1031") {
                    if (data_use.data.direction == 0) {
                        arg.busTopNumber = data_use.data.bus_no_of_park + '辆';
                    }
                    if (data_use.data.direction == 1) {
                        arg.busDownNumber = data_use.data.bus_no_of_park + '辆';
                    }
                    //进场之后车辆消失
                    if (data_use.data.inField == 1) {
                        $('body').find('.dispatch_desktop[line_id=' + data_use.data.line_id + ']').find('.traffic_car .line_car[bus_no=' + data_use.data.bus_no + ']').remove();
                    }
                }
                //车辆实时位置  分上下行已经进出站
                if (data_use.data.packageType == "1044") {
                    self.$el.find('.line_car[bus_no=' + data_use.data.abnormal_description.bus_no + ']').removeClass('to_gray');
                    self.$el.find('.show_signal_online span').html(parseInt(self.$el.find('.show_signal_online span').html()) + 1);
                    self.$el.find('.show_signal_outline span').html(parseInt(self.$el.find('.show_signal_outline span').html()) - 1);
                }
                if (data_use.data.packageType == "1045") {
                    arg.busTopNumber = data_use.data.upFieldBusNum + '辆';
                    arg.busDownNumber = data_use.data.downFieldBusNum + '辆';
                    self.$el.find('.show_trailerNum span').html(data_use.data.runBus);
                    self.$el.find('.show_active_car span').html(data_use.data.motorBus);
                }
                if (data_use.type == "1035") {
                    //如果车辆id未出现   车辆到达最后站点出站remove未做处理
                    //删除车辆此时的位置显示，并重新渲染，防止上行穿到下行不显示
                    $('.traffic_car .line_car[bus_no=' + data_use.data.terminalNo + ']').remove();
                    $('.run_car_hide').find('.line_car').attr('bus_no', data_use.data.terminalNo);
                    // 车辆进出站上下行 进出站  0 上行 in进站
                    if (data_use.data.direction == 0) {
                        if (data_use.data.type == "in") {
                            self.$el.find('.content_car_road_top .car_line_top' + (parseInt(data_use.data.stationNo) * 2 - 2)).append($('.run_car_hide').html());
                            var oLeft = 1190 * (parseInt(data_use.data.stationNo) - 0.5) / arg.site_top_infos.length;
                        } else if (data_use.data.type == "out") {
                            self.$el.find('.content_car_road_top .car_line_top' + (parseInt(data_use.data.stationNo) * 2 - 1)).append($('.run_car_hide').html());
                            var oLeft = 1190 * (parseInt(data_use.data.stationNo)) / arg.site_top_infos.length;
                        }
                        self.$('.content_car_road_top').find('.line_car[bus_no=' + data_use.data.terminalNo + ']').css('left', oLeft - 15 + 'px');
                        self.$('.content_car_road_top').find('.line_car[bus_no=' + data_use.data.terminalNo + ']').find('.type_car span').attr("car_id", data_use.data.car_id).html(data_use.data.terminalNo);
                        //遍历每个小格子
                    } else if (data_use.data.direction == 1) {
                        if (data_use.data.type == "in") {
                            self.$el.find('.content_car_road_down .car_line_down' + (parseInt(data_use.data.stationNo) * 2 - 2)).append($('.run_car_hide').html());
                            var oLeft = 1190 - 1190 * (parseInt(data_use.data.stationNo) - 0.5) / arg.site_down_infos.length;
                        } else if (data_use.data.type == "out") {
                            self.$el.find('.content_car_road_down .car_line_down' + (parseInt(data_use.data.stationNo) * 2 - 1)).append($('.run_car_hide').html());
                            var oLeft = 1190 - 1190 * (parseInt(data_use.data.stationNo)) / arg.site_down_infos.length;
                        }
                        self.$('.content_car_road_down').find('.line_car[bus_no=' + data_use.data.terminalNo + ']').css('left', oLeft - 15 + 'px');
                        self.$('.content_car_road_down').find('.line_car[bus_no=' + data_use.data.terminalNo + ']').find('.type_car span').attr("car_id", data_use.data.car_id).html(data_use.data.terminalNo);

                    }
                    for (var nu = 0; nu < self.$('.content_car_road_top .car_line_tb').length; nu++) {
                        //移除之前的重复位置
                        //如果已经有两辆车
                        self.$('.content_car_road_top .car_line_top' + nu).find('.same_car_show').remove();
                        self.$('.content_car_road_top .car_line_top' + nu).find('.data_same').remove();
                        if (self.$('.content_car_road_top .car_line_top' + nu).find('.line_car').length > 1) {
                            var html_c = '';
                            for (var i = 0; i < self.$('.content_car_road_top .car_line_top' + nu).find('.line_car').length; i++) {
                                var carObj = self.$('.content_car_road_top .car_line_top' + nu).find('.line_car .type_car span').eq(i);
                                html_c += '<div car_id=' + carObj.attr("car_id") + '>' + carObj.html() + '</div>';
                            }
                            self.$('.content_car_road_top .car_line_top' + nu).append('<div class="same_car_show" style="left: ' + (parseFloat(self.$('.content_car_road_top .car_line_top' + nu).find('.line_car').css('left')) - 50) + 'px">...</div><span style="display: none" class="data_same"></span>')
                            self.$('.content_car_road_top .car_line_top' + nu).find('.data_same').html(html_c);
                        }
                    }
                    for (var num = 0; num < self.$('.content_car_road_down .car_line_tb').length; num++) {
                        //移除之前的重复位置
                        //如果已经有两辆车
                        self.$('.content_car_road_down .car_line_down' + num).find('.same_car_show').remove();
                        self.$('.content_car_road_down .car_line_down' + num).find('.data_same').remove();
                        if (self.$('.content_car_road_down .car_line_down' + num).find('.line_car').length > 1) {
                            var html_c = '';
                            for (var i = 0; i < self.$('.content_car_road_down .car_line_down' + num).find('.line_car').length; i++) {
                                var carObj = self.$('.content_car_road_down .car_line_down' + num).find('.line_car .type_car span').eq(i);
                                html_c += '<div car_id=' + carObj.attr("car_id") + '>' + carObj.html() + '</div>';
                            }
                            self.$('.content_car_road_down .car_line_down' + num).append('<div class="same_car_show" style="left: ' + (parseFloat(self.$('.content_car_road_down .car_line_down' + num).find('.line_car').css('left')) + 30) + 'px">...</div><span style="display: none" class="data_same"></span>')
                            self.$('.content_car_road_down .car_line_down' + num).find('.data_same').html(html_c);
                        }
                    }
                }
                data.busTopNumber = arg.busTopNumber;
                data.busDownNumber = arg.busDownNumber;
                data.subsection = [1, 2, 3, 4, 5, 6];
                //公交模拟地图canvas绘制
                qrend_desktop_canvas(data, '.can_top', '.can_bottom', '.canvas_left', '.canvas_right', self.$el);
                // 线路颜色
                self.color = data.color;
                self.site_top_infos = data.site_top_infos;
                self.site_down_infos = data.site_down_infos;
                // 站点颜色
                self.dataSite_top_color = arg.dataSite_top_color_cof;
                self.dataSite_down_color = arg.dataSite_down_color_cof;
                self.subsection = data.subsection;
            }
        },
        events: {
            //上下的车辆是否隐藏 click事件被占用
            'mouseup .can_top': 'clk_can_top',
            'mouseup .can_bottom': 'clk_can_bottom',
            // 删除选择路线弹框
            'click .del': 'del_chose_line',
            // 选择路线
            'click .line_edit': 'show_chose_line',
            //车辆信息
            'click .line_car': 'bus_info',
            // 左右侧车场
            'click .canvas_left': 'clk_can_left',
            'click .canvas_right': 'clk_can_right',
            // 鼠标划过上左右车场时的cursor属性
            'mousemove .canvas_left': 'slide_cursor_pointer_left',
            'mousemove .canvas_right': 'slide_cursor_pointer_right',
            'mousemove .can_top': 'slide_cursor_pointer_top',
            'mousemove .can_bottom': 'slide_cursor_pointer_bottom',
            //点击上方详情
            'mouseup .bus_info li': 'bus_man_src',
            //鼠标划过上下行车路线时的cursor属性
            // 行车组件关闭
            'click .min': 'closeFn',
            'click .park_top_down_way': 'open_park_way',
            'mouseup .show_mutual_information': 'show_mutual_information'
        },
        show_mutual_information: function (ev) {
            var self = this;
            var zIndex = parseInt(this.$el[0].style.zIndex) + 1;
            self.layer_index = layer.msg('加载中...', {time: 0, shade: 0.3});
            this.model_choseline.query().filter([["state", "=", 'inuse']]).all().then(function (data) {
                var option =
                    {
                        x: ev.clientX + 5,
                        y: ev.clientY + 5,
                        zIndex: zIndex,
                        line_id: self.line_id,
                        controllerId: self.desktop_id,
                        data: data
                    };
                layer.close(self.layer_index)
                if ($(".mutual_information_" + option.line_id).length > 0) {
                    return;
                } else {
                    $(".mutual_information").remove();
                    new mutual_information(self, option).appendTo($(".controller_" + option.controllerId));
                }
            })
            // $.ajax({
            //     url: RESTFUL_URL + '/exchange/list?apikey=71029270&params={lineId:'+this.line_id+',controlId:'+this.desktop_id+',arg:'',arg1:1,pageNum:1,pageSize1}',
            //     type: 'get',
            //     dataType: 'json',
            //     data: {},
            //     success: function (data) {
            //
            //     },
            //     error:function () {
            //         layer.msg('请求出错', {time: 1000, shade: 0.3});
            //     }
            // });
        },
        closeFn: function () {
            var self = this;
            var tid = this.$el.attr('tid');
            var desktop_id = self.desktop_id;

            if (tid != undefined) {
                // socket_model_info[tid].status =false;
                // 查询tid,拿到tid下面的lineid并得到相同lineid的一条线路  desktopid!!!
                self.model_line.query().filter([["desktop_id", '=', parseInt(desktop_id)], ["id", "=", parseInt(tid)]]).all().then(function (pp) {
                    // 查询tid下的lineid
                    self.model_line.query().filter([["desktop_id", '=', parseInt(desktop_id)], ["line_id", "=", pp[0].line_id[0]]]).all().then(function (data) {
                        // 删除该tid，即此线路
                        self.model_line.call("unlink", [data[1].id]).then(function () {
                            self.$el.parent().find('.updown_line_table').remove();
                            self.model_line.call("unlink", [data[0].id]).then(function () {
                                self.destroy();
                            });
                        });
                    });
                });
            } else {
                self.$el.parent().find('.updown_line_table').remove();
                self.destroy();
            }
            if ($('body').find('.dispatch_desktop').length > 0) {
                $('body').find('.dispatch_desktop:last').attr("click", "yes");
            }
        }
        ,
        open_park_way: function (e) {
            var self = this;
            var zIndex = parseInt(this.$el[0].style.zIndex) + 1;
            var options =
                {
                    x: e.clientX + 5,
                    y: e.clientY + 5 - 60,
                    zIndex: zIndex,
                    line_id: self.$el.attr("line_id"),
                    line_name: self.$el.attr("line_name"),
                    controllerId: self.desktop_id
                };
            if ($(".linePlanParkOnlineModel_" + options.line_id).length > 0) {
                return;
            } else {
                // try {
                $(".linePlanParkOnlineModel").remove();
                var dialog = new plan_display(self, options);
                dialog.appendTo($(".controller_" + options.controllerId));
                // } catch(e){
                // var layer_index = layer.msg("websoket断开链接，请检查网络是否通畅", {shade: 0.3});
                // }
            }
        }
        ,
        cursor_pointer_tb: function (canvas, e) {
            var e = e || window.event;
            var c = this.$el.find(canvas.cId)[0];
            var cxt = c.getContext("2d");
            var x = e.pageX - c.getBoundingClientRect().left;
            var y = e.pageY - c.getBoundingClientRect().top;
            c.style.cursor = 'auto';
            this.$el.find('.show_tip_top').hide().html('');
            if (canvas.site_infos) {
                for (var i = 0; i < canvas.site_infos.length; i++) {
                    var everyLen = 1190 * (i + 0.5) / canvas.site_infos.length;
                    var mySite = canvas.site_infos[i].station_id[1].split('/')[0];
                    cxt.beginPath();
                    //渲染参数，x距离,y距离,半径,起始角，结束角，是否顺势针
                    cxt.arc(everyLen, canvas.ciry, 3, 0, 360, false);
                    //判断鼠标的点是否在圆圈内
                    if (cxt.isPointInPath(x, y)) {
                        c.style.cursor = 'pointer';
                        if (canvas.cId == '.can_top') {
                            this.$el.find('.show_tip_top').css({
                                'left': x + 20,
                                'top': y + 20
                            }).show().html(mySite);
                        } else if (canvas.cId == '.can_bottom') {
                            this.$el.find('.show_tip_top').css({
                                'left': x + 20,
                                'top': y + 45
                            }).show().html(mySite);
                        }

                    }
                    cxt.closePath();
                    cxt.beginPath();
                    if (canvas.site_infos[i].is_show_name == true) {
                        // 计算每段文字的长度，算出点击的区域
                        cxt.rect(everyLen - (6 * canvas.site_infos[i].station_id[1].split('/')[0].length), canvas.testy - 16, 12 * canvas.site_infos[i].station_id[1].split('/')[0].length, 16)
                        if (cxt.isPointInPath(x, y)) {
                            c.style.cursor = 'pointer';
                        }
                    }
                }
            }
        }
        ,
        slide_cursor_pointer_top: function (e) {
            var option = {
                cId: '.can_top',
                dataSite_color: this.dataSite_top_color,
                site_infos: this.site_top_infos,
                testy: 13,
                ciry: 27
            }
            this.cursor_pointer_tb(option, e);
        }
        ,
        slide_cursor_pointer_bottom: function (e) {
            var option = {
                cId: '.can_bottom',
                dataSite_color: this.dataSite_down_color,
                site_infos: this.site_down_infos,
                testy: 25,
                ciry: 6
            }
            this.cursor_pointer_tb(option, e);
        }
        ,
        bus_info: function (e) {
            var car_num = e.currentTarget.getElementsByClassName("type_car")[0].children[0].textContent;
            var car_id = e.currentTarget.getElementsByClassName("type_car")[0].children[0].getAttribute("car_id");
            var line_id = e.delegateTarget.getAttribute("line_id");
            var zIndex = parseInt(this.$el[0].style.zIndex) + 1;
            var options =
                {
                    x: e.clientX + 5,
                    y: e.clientY + 5 - 60,
                    zIndex: zIndex,
                    line_id: line_id,
                    line_name: this.$el.attr("line_name"),
                    car_num: car_num,
                    car_id: car_id,
                    controllerId: this.desktop_id
                };
            // if (line_id != 1 || car_num != 1) {
            //     layer.alert("模拟soket实时加载，请选择810线路1号车进行点击", {title: "车辆实时信息"});
            //     return false;
            // }
            // ;
            if ($(".busRealStateModel_" + options.line_id + "_" + options.car_num).length > 0) {
                return;
            } else {
                $(".busRealStateModel").remove();
                var dialog = new bus_real_info(this, options);
                dialog.appendTo($(".controller_" + options.controllerId));
            }
            // e.delegateTarget.parentElement.append(dialog);
        }
        ,
        clk_can_top: function (e) {
            this.clickTb({
                id: '.can_top',
                ciry: 27,
                testy: 13,
                self: this.$el,
                color: this.color,
                site_infos: this.site_top_infos,
                dataSite_color: this.dataSite_top_color,
                subsection: this.subsection,
                model: this.model_station_platform
            }, e);
        }
        ,
        clk_can_bottom: function (e) {
            this.clickTb({
                id: '.can_bottom',
                ciry: 6,
                testy: 25,
                self: this.$el,
                color: this.color,
                site_infos: this.site_down_infos,
                dataSite_color: this.dataSite_down_color,
                subsection: this.subsection,
                model: this.model_station_platform
            }, e);
        }
        ,
        bus_man_src: function (e) {
            var self = this;
            var ev = e || window.event;
            var zIndex = parseInt(this.$el[0].style.zIndex) + 1;
            if (ev.button == 0) {
                if (!isDrag) {
                    if ($('body').find('.bus_src_config').length > 0) {
                        $('body').find('.bus_src_config').remove();
                    }
                    //先把doMouseDownTimmer清除，不然200毫秒后setGragTrue方法还是会被调用的
                    clearTimeout(timmerHandle);
                    var line_id = ev.delegateTarget.getAttribute("line_id");
                    var options =
                        {
                            x: ev.clientX + 5,
                            y: ev.clientY + 5,
                            zIndex: zIndex,
                            line_id: line_id,
                            controllerId: self.desktop_id,
                        };
                    $.ajax({
                        url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename:"op_busresource",controlsId:' + self.desktop_id + ',lineId:' + self.line_id + '}',
                        type: 'get',
                        dataType: 'json',
                        data: {},
                        success: function (data) {
                            function formatDate(now) {
                                var year = now.getYear();
                                var month = now.getMonth() + 1;
                                var date = now.getDate();
                                var hour = now.getHours();
                                if (hour < 10) {
                                    hour = "0" + hour;
                                }
                                var minute = now.getMinutes();
                                if (minute < 10) {
                                    minute = "0" + minute;
                                }
                                var second = now.getSeconds();
                                if (second < 10) {
                                    second = "0" + second;
                                }
                                return year + "-" + month + "-" + date + " " + hour + ":" + minute + ":" + second;
                            }

                            if (data.respose != undefined) {
                                for (var i = 0; i < data.respose.length; i++) {
                                    if (data.respose[i].planRunTime) {
                                        data.respose[i].planRunTime = formatDate(new Date(data.respose[i].planRunTime)).split(' ')[1];
                                    }
                                    if (data.respose[i].realReachTime) {
                                        data.respose[i].realReachTime = formatDate(new Date(data.respose[i].realReachTime)).split(' ')[1];
                                    }
                                }
                                if (data.respose != '') {
                                    new bus_source_config(this, options, data).appendTo($(".controller_" + options.controllerId));
                                } else {
                                    layer.msg('暂无数据', {time: 1000, shade: 0.3});
                                }
                            }
                        },
                        error: function () {
                            layer.msg('请求出错', {time: 1000, shade: 0.3});
                        }
                    });
                }
                else {
                    isDrag = false;
                }
            }
        }
        ,
        clickTb: function (canvas, e) {
            var self = this;
            var event = e || window.event;
            var c = canvas.self.find(canvas.id)[0];
            var cxt = c.getContext("2d");
            var x = event.pageX - c.getBoundingClientRect().left;
            var y = event.pageY - c.getBoundingClientRect().top;
            var zIndex = parseInt(this.$el[0].style.zIndex) + 1;
            // if (e.button == 2) {
            //     if ($('body').find('.bus_site_info').length > 0) {
            //         $('body').find('.bus_site_info').remove();
            //     }
            //     var options =
            //         {
            //             x: event.clientX - self.$el[0].offsetLeft + 5,
            //             y: event.clientY - self.$el[0].offsetTop + 5,
            //             zIndex: zIndex,
            //         };
            //     new bus_site_info(this, options).appendTo(this.$el);
            // }
            if (canvas.site_infos) {
                for (var i = 0; i < canvas.site_infos.length; i++) {
                    cxt.beginPath();
                    //渲染参数，x距离,y距离,半径,起始角，结束角，是否顺势针
                    var everyLen = 1190 * (i + 0.5) / canvas.site_infos.length;
                    cxt.arc(everyLen, canvas.ciry, 3, 0, 360, false);
                    //判断鼠标的点是否在圆圈内
                    if (cxt.isPointInPath(x, y)) {
                        c.style.cursor = 'pointer';
                        //获取鼠标点击区域的颜色值
                        var imgData = cxt.getImageData(x, y, 1, 1);
                        // 重绘画布
                        cxt.clearRect(0, 0, c.width, c.height);
                        canvas.site_infos[i].is_show_name == true ? canvas.site_infos[i].is_show_name = false : canvas.site_infos[i].is_show_name = true;
                        canvas.model.call("write", [canvas.site_infos[i].id,
                            {
                                'is_show_name': canvas.site_infos[i].is_show_name
                            }]).then(function (res) {

                        });
                        if (canvas.subsection != '') {
                            var traffic_top = {
                                id: canvas.id,
                                y: canvas.ciry - 1,
                                self: canvas.self,
                                subsection: canvas.subsection,
                                color: canvas.color
                            };
                            traffic_distance(traffic_top);
                        }
                        var cir_text = {
                            id: canvas.id,
                            ciry: canvas.ciry,
                            testy: canvas.testy,
                            self: canvas.self,
                            // color: canvas.color,
                            dataSite_color: canvas.dataSite_color,
                            site_infos: canvas.site_infos
                        };
                        cir_and_text(cir_text);
                        cxt.closePath();
                        // 转换16进制像素
                        var hex = "#" + ((1 << 24) + (imgData.data[0] << 16) + (imgData.data[1] << 8) + imgData.data[2]).toString(16).slice(1);
                        if (hex == "#ffffff") {
                            // 清除画布
                            // 绘上实心圆
                            cxt.beginPath();
                            cxt.arc(everyLen, canvas.ciry, 4, 0, 360, false);
                            cxt.fillStyle = transform(canvas.dataSite_color)[i];
                            cxt.fill();
                            cxt.closePath();
                        } else {
                            cxt.beginPath();
                            cxt.arc(everyLen, canvas.ciry, 4, 0, 360, false);
                            cxt.fillStyle = "white";
                            cxt.fill();
                            cxt.closePath();
                        }
                        break
                    }
                    cxt.closePath();
                    cxt.beginPath();
                    if (canvas.site_infos[i].is_show_name == true) {
                        cxt.rect(everyLen - (6 * canvas.site_infos[i].station_id[1].split('/')[0].length), canvas.testy - 16, 12 * canvas.site_infos[i].station_id[1].split('/')[0].length, 16)
                        if (cxt.isPointInPath(x, y)) {
                            //如果是左击
                            if (e.button == 0) {
                                var options =
                                    {
                                        x: e.clientX + 5,
                                        y: e.clientY + 5 - 60,
                                        zIndex: zIndex,
                                        controllerId: self.desktop_id,
                                        line_id: canvas.self.attr("line_id"),
                                        line_name: canvas.self.attr("line_name"),
                                        site: canvas.site_infos[i].station_id[1].split('/')[0],
                                        site_id: canvas.site_infos[i].id,
                                        site_infos: canvas.site_infos[i].direction == "up" ? self.site_top_infos : self.site_down_infos
                                    };
                                if ($(".passengerDelayModel_" + options.line_id + "_" + options.site_id).length > 0) {
                                    return;
                                } else {
                                    $(".passengerDelayModel").remove();
                                    var dialog = new passenger_flow(self, options);
                                    dialog.appendTo($(".controller_" + options.controllerId));
                                }
                                cxt.closePath();
                            }
                        }
                    }
                }
            }
        }
        ,
// 点击左侧车场
        clk_can_left: function (e) {
            this.click_lr({
                id: '.canvas_left',
            }, e);
        }
        ,
// 点击右侧车场
        clk_can_right: function (e) {
            this.click_lr({
                id: '.canvas_right',
            }, e);
        }
        ,
        del_chose_line: function () {
            this.$('.edit_content').hide();
        }
        ,
        show_chose_line: function () {
            var self = this;
            self.$el.find(".edit_content .chs").mCustomScrollbar("destroy");
            self.model_choseline.query().filter([["state", "=", 'inuse']]).all().then(function (data) {
                self.$('.edit_content .chs').html('')
                for (var i = 0; i < data.length; i++) {
                    if (data[i].id) {
                        var oLi = "<li gid=" + data[i].gprs_id + " lineid=" + data[i].id + ">" + data[i].line_name + "</li>";
                        self.$('.edit_content .chs').append(oLi);
                    }
                }
                self.$el.find('.edit_content .chs').mCustomScrollbar({
                    theme: 'minimal'
                });
                self.$('.edit_content').show();
            });
        }
        ,
        cursor_pointer_lr: function (canvas, e) {
            var event = e || window.event;
            var c = this.$el.find(canvas.id)[0];
            var cxt = c.getContext("2d");
            var x = event.pageX - c.getBoundingClientRect().left;
            var y = event.pageY - c.getBoundingClientRect().top;
            c.style.cursor = 'auto';
            cxt.arc(13, 58, 13, 0, 360, false);
            if (cxt.isPointInPath(x, y)) {
                c.style.cursor = 'pointer';
            }
        }
        ,
        slide_cursor_pointer_left: function (e) {
            this.cursor_pointer_lr({
                id: '.canvas_left',
            }, e);
        }
        ,
        slide_cursor_pointer_right: function (e) {
            this.cursor_pointer_lr({
                id: '.canvas_right',
            }, e);
        }
        ,
//左侧的停车场的点击事件
        click_lr: function (canvas, e) {
            var self = this;
            var event = e || window.event;
            var c = this.$el.find(canvas.id)[0];
            var cxt = c.getContext("2d");
            var x = event.pageX - c.getBoundingClientRect().left;
            var y = event.pageY - c.getBoundingClientRect().top;
            var zIndex = parseInt(this.$el[0].style.zIndex) + 1;
            cxt.arc(13, 58, 13, 0, 360, false);
            if (cxt.isPointInPath(x, y)) {
                var options =
                    {
                        x: e.clientX + 5,
                        y: e.clientY + 5 - 60,
                        zIndex: zIndex,
                        line_id: self.$el.attr("line_id"),
                        line_name: self.$el.attr("line_name"),
                        controllerId: self.desktop_id
                    };
                if ($(".linePlanParkOnlineModel_" + options.line_id).length > 0) {
                    return;
                } else {
                    // try {
                    $(".linePlanParkOnlineModel").remove();
                    var dialog = new plan_display(self, options);
                    dialog.appendTo($(".controller_" + options.controllerId));
                    // } catch(e){
                    // var layer_index = layer.msg("websoket断开链接，请检查网络是否通畅", {shade: 0.3});
                    // }
                }
            }
        }
    });
    var mutual_information = Widget.extend({
        template: 'mutual_information',
        init: function (parent, option) {
            this._super(parent);
            this.location_data = option;
            this.model_route_bus = new Model('fleet.vehicle');
        },
        start: function () {
            this.desktop_id = this.$el.parents(".back_style").attr("desktop_id");
        },
        events: {
            'click .mutal_srh_btn': 'mutual_search',
            'click  .min': 'close_this',
            'change .line_way_chs': 'bus_chs'
        },
        bus_chs: function () {
            var self = this;
            var val = parseInt($(".line_way_chs option:selected").attr("oid"));
            if (val) {
                self.layer_index = layer.msg('加载中...', {time: 0, shade: 0.3});
                this.model_route_bus.query().filter([["route_id", "=", val]]).all().then(function (data) {
                    layer.close(self.layer_index);
                    self.$el.find('.bus_way_chs').html("<option selected='selected'>车辆</option>");
                    var str = "";
                    $.each(data, function (index, value) {   // 解析出data对应的Object数组s
                        str += "<option bid=" + value.on_boardid + ">" + value.on_boardid + "</option>";
                    });
                    self.$el.find('.bus_way_chs').append(str)
                })
            } else {
                self.$el.find('.bus_way_chs').html("<option>全部车辆</option>")
            }
        },
        mutual_search: function () {
            var line_val = this.$el.find('.line_way_chs option:selected').attr("oid");
            var bus_val = this.$el.find('.bus_way_chs option:selected').attr("bid");
            var make_deal = this.$el.find('.type_chs option:selected').attr("mid");
            var self = this;
            if (bus_val == undefined) {
                bus_val = '';
            }
            var td_txt = '';
            $.ajax({
                    url: RESTFUL_URL + '/ltyop/exchange/list?apikey=71029270&params={lineId:' + line_val + ',controlId:' + self.desktop_id + ',arg:\'' + bus_val + '\',arg1:\'' + make_deal + '\',pageSize:10}',
                    type: 'get',
                    dataType: 'json',
                    data: {},
                    success: function (data) {
                        console.log(data)
                        var totalPage = data.respose.vo.totalCount % 10 == 0 ? data.respose.vo.totalCount / 10 : Math.ceil(data.respose.vo.totalCount / 10);
                        self.$el.find('.mutual_content tbody').html('');
                        if (data.respose.opWarningList.length > 0) {
                            $.each(data.respose.opWarningList, function (index, value) {   // 解析出data对应的Object数组
                                td_txt += "<tr>"
                                    + "<td>" + index + "</td>"
                                    + "<td>" + value.occurTime + "</td>"
                                    + "<td>" + value.lineName + "</td>"
                                    + "<td>" + value.onBoardId + "</td>"
                                    + "<td>" + value.logText + "</td>"
                                    + "<td>" + value.remark + "</td>"
                                if (value.result == 0) {
                                    td_txt += "<td><a>同意</a>|<a>拒绝</a></td>"
                                        + "<td>待操作</td>"
                                } else if (value.result == 1) {
                                    td_txt += "<td></td>"
                                        + "<td>已操作</td>"
                                }
                                td_txt += "</tr>";
                            });
                            self.$el.find('.mutual_content tbody').html(td_txt);
                        }
                        if (data.respose.opWarningList.length > 0) {
                            $('.pagination_tbl').bootstrapPaginator({
                                currentPage: 1,//当前的请求页面。
                                totalPages: totalPage,//一共多少页。
                                size: "normal",//应该是页眉的大小。
                                bootstrapMajorVersion: 3,//bootstrap的版本要求。
                                alignment: "right",
                                numberOfPages: 10,
                                itemTexts: function (type, page, current) {//如下的代码是将页眉显示的中文显示我们自定义的中文。
                                    switch (type) {
                                        case "first":
                                            return "首页";
                                        case "prev":
                                            return "上一页";
                                        case "next":
                                            return "下一页";
                                        case "last":
                                            return "末页";
                                        case "page":
                                            return page;
                                    }
                                },
                                onPageClicked: function (event, originalEvent, type, page) {
                                    $.ajax({
                                        url: RESTFUL_URL + '/ltyop/exchange/list?apikey=71029270&params={lineId:' + line_val + ',controlId:' + self.desktop_id + ',arg:\'' + bus_val + '\',arg1:\'' + make_deal + '\',pageNum:' + page + ',pageSize:10}',
                                        type: "get",
                                        dataType: "json",
                                        data: '',
                                        success: function (data1) {
                                            self.$el.find('.mutual_content tbody').html('');
                                            td_txt = '';
                                            $.each(data1.respose.opWarningList, function (index, value) {   // 解析出data对应的Object数组
                                                var index_num = parseInt((page - 1) * 10) + index;
                                                td_txt += "<tr>"
                                                    + "<td>" + index_num + "</td>"
                                                    + "<td>" + value.occurTime + "</td>"
                                                    + "<td>" + value.lineName + "</td>"
                                                    + "<td>" + value.onBoardId + "</td>"
                                                    + "<td>" + value.logText + "</td>"
                                                    + "<td>" + value.remark + "</td>"
                                                if (value.result == 0) {
                                                    td_txt += "<td><a>同意</a>|<a>拒绝</a></td>"
                                                        + "<td>待操作</td>"
                                                } else if (value.result == 1) {
                                                    td_txt += "<td></td>"
                                                        + "<td>已操作</td>"
                                                }
                                                td_txt += "</tr>";
                                            });
                                            self.$el.find('.mutual_content tbody').html(td_txt);
                                        }
                                    })
                                }
                            })

                        }
                    },
                    error: function () {
                        layer.msg('请求出错', {time: 1000, shade: 0.3});
                    }
                }
            );
        },
        close_this: function () {
            this.destroy()
        }
    })
    var dispatch_line_control = Widget.extend({
        init: function (parent, data, type) {
            this._super(parent);
            this.model_line = new Model('dispatch.control.desktop.component');
            this.model_choseline = new Model('route_manage.route_manage');
            this.data = data;
            this.type = type;
        },
        start: function () {
            this.desktop_id = this.$el.parents(".back_style").attr("desktop_id");
            var data = this.data;
            var type = this.type;
            // 界面初始渲染
            if (type == 0) {
                // 只存在其中一种组件
                if (data.length == 1) {
                    // 只存在dispatch_desktop组件
                    if (data[0].model_type == "dis patch_desktop") {
                        new dispatch_canvas(this, data[0], 0).appendTo(this.$el);
                        this.$el.find('.line_edit').hide();
                        // 只存在updown_line_table组件
                    } else if (data[0].model_type == "updown_line_table") {
                        new dispatch_updown_line(this, data[0], 0).appendTo(this.$el);
                    }
                    // 存在完整组件
                } else if (data.length > 1) {
                    new dispatch_canvas(this, data[0], 0).appendTo(this.$el);
                    new dispatch_updown_line(this, data[1], 0).appendTo(this.$el);
                    // this.$el.find('.show_right').hide();
                    if (data[1].tem_display == 'none') {
                        this.$el.find('.show_right').show();
                        this.$el.find('.line_edit').hide();
                    } else {
                        this.$el.find('.show_right').hide();
                        this.$el.find('.line_edit').show();
                    }
                }
                // 手动添加渲染
            } else if (type == 1) {
                var zr_index = 1;
                if ($('body').find('.dragContent[click]').length > 0) {
                    zr_index = parseInt($('body').find('.dragContent[click]')[0].style.zIndex) + 1;
                }
                new dispatch_canvas(this, data[0], zr_index).appendTo(this.$el);
                new dispatch_updown_line(this, data[1], zr_index).appendTo(this.$el);
            }
        },
        events: {
            'click .chs li': 'chose_line',

        },
        chose_line: function (event) {
            var x = event.currentTarget;
            var self = this;
            var line = $(x).attr("lineid");
            var tid = self.$el.find('.dispatch_desktop')[0].getAttribute('tid');
            var siteZindex = self.$el.find('.dispatch_desktop')[0].style.zIndex;
            var siteLeft = self.$el.find('.dispatch_desktop')[0].offsetLeft;
            var siteTop = self.$el.find('.dispatch_desktop')[0].offsetTop;
            var siteZindexPf = self.$el.find('.updown_line_table')[0].style.zIndex;
            var siteLeftPf = self.$el.find('.updown_line_table')[0].offsetLeft;
            var siteTopPf = self.$el.find('.updown_line_table')[0].offsetTop;
            var lineName = $('body').find('.line_line');
            var resName = [];
            var desktop_id = self.desktop_id;
            for (var j = 0; j < lineName.length; j++) {
                resName.push(lineName[j].innerHTML);
            }
            // 不存在其他的组件时候
            if (tid == '') {
                if (resName.indexOf(x.innerHTML) != -1) {
                    layer.msg('该线路已被选择，请重新选择', {time: 1000, shade: 0.3});
                } else {
                    self.model_line.call("create", [
                        {
                            'desktop_id': desktop_id,
                            "model_type": "dispatch_desktop",
                            'position_left': siteLeft,
                            'position_top': siteTop,
                            'position_z_index': 0,
                            'line_id': $(x).attr('lineid'),
                            'gprs_id': $(x).attr('gid'),
                            'name': x.innerHTML
                        }]).then(function () {
                        self.model_line.call("create", [
                            {
                                'desktop_id': desktop_id,
                                "model_type": "updown_line_table",
                                'position_left': siteLeftPf,
                                'position_top': siteTopPf,
                                'position_z_index': 0,
                                'line_id': $(x).attr('lineid'),
                                'name': x.innerHTML
                            }]).then(function () {
                            self.model_line.query().filter([['desktop_id', '=', parseInt(desktop_id)], ["line_id", "=", parseInt($(x).attr('lineid'))]]).all().then(function (data) {
                                self.$el.html('');
                                data[0].position_z_index = siteZindex;
                                data[1].position_z_index = siteZindexPf;
                                new dispatch_bus(this, data, 0).appendTo(self.$el);
                            });
                        });
                    });
                }
            } else {
                if (resName.indexOf(x.innerHTML) != -1) {
                    layer.msg('该线路已被选择，请重新选择', {time: 1000, shade: 0.3});
                } else {
                    self.model_line.call("write", [parseInt(tid),
                        {
                            'line_id': $(x).attr("lineid"),
                            'gprs_id': $(x).attr('gid'),
                            'position_left': siteLeft,
                            'position_top': siteTop,
                            'position_z_index': 0,
                            'name': x.innerHTML
                        }]).then(function (res) {
                        self.model_line.call("write", [parseInt(tid) + 1,
                            {
                                'line_id': $(x).attr("lineid"),
                                'position_left': siteLeftPf,
                                'position_top': siteTopPf,
                                'position_z_index': 0,
                                'name': x.innerHTML
                            }]).then(function (res) {
                            self.model_line.query().filter([["desktop_id", '=', parseInt(desktop_id)], ["line_id", "=", parseInt(line)]]).all().then(function (data) {
                                data[1].position_left = self.$el.find('.updown_line_table')[0].offsetLeft;
                                data[1].position_top = self.$el.find('.updown_line_table')[0].offsetTop;
                                data[1].position_z_index = self.$el.find('.updown_line_table')[0].style.zIndex;
                                self.$el.html('');
                                new dispatch_bus(this, data, 0).appendTo(self.$el);
                            });
                        });
                    });
                }
            }
        }
    });
//整个车行的组件
    var dispatch_bus = Widget.extend({
        init: function (parent, data, type) {
            this._super(parent);
            this.data = data;
            this.type = type;
            this.model_line = new Model('dispatch.control.desktop.component');
        },
        start: function () {
            var data = this.data;
            var type = this.type;
            new dispatch_line_control(this, data, type).appendTo(this.$el);
        },
        events: {
            'click .show_right': 'show_right'
        },
        show_right: function (event) {
            var ev = event || window.event;
            var x = ev.currentTarget;
            var self = this;
            var zIndex = parseInt(this.$el[0].style.zIndex) + 1;
            var tid = this.$el.find('.updown_line_table').attr('tid');
            self.model_line.call("write", [parseInt(tid),
                {
                    'tem_display': ''
                }]).then(function () {
                self.$el.find('.updown_line_table').show().css('z-index', zIndex);
                $(x).hide();
                $(x).siblings('.line_edit').show();
            });
        }
    });
    return dispatch_bus;
})
;