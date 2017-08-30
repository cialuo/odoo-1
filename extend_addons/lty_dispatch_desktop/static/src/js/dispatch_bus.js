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
    var plan_display = require('lty_dispatch_desktop_widget.plan_display');
    //最原始车辆组件
    var dispatch_canvas = Widget.extend({
        template: 'dispatch_desktop',
        init: function (parent, data) {
            this._super(parent);
            // 线路info
            this.model_line = new Model('dispatch.control.desktop.component');
            // 线路
            this.model_choseline = new Model('route_manage.route_manage');
            // 上行站点
            this.model_station_platform = new Model('opertation_resources_station_platform');
            // 下行站点
            this.model_site_down = new Model('opertation_resources_station_down');
            //odoo提供数据
            this.dis_desk = data;
        },
        start: function () {
            var self = this;
            this.desktop_id = this.$el.parents(".back_style").attr("desktop_id");
            function site_info(mode_line, model_station_platform) {
                if (self.$el.find('.line_line')[0] != undefined) {
                    var tid = self.$el.attr('tid');
                    var model_name = self.$el[0].className;
                    // 根据tid拿到线路id
                    mode_line.query().filter([["id", "=", parseInt(tid)]]).all().then(function (data) {
                        model_station_platform.query().filter([["route_id", "=", data[0].line_id[0]], ["direction", "=", "up"]]).all().then(function (res_top) {
                            model_station_platform.query().filter([["route_id", "=", data[0].line_id[0]], ["direction", "=", "down"]]).all().then(function (res_down) {
                                // 库
                                var model_id = model_name + "" + tid;
                                if (socket_model_info[model_id]) {
                                    delete socket_model_info[model_id];
                                }
                                var package_send = {
                                    type: 1000,
                                    open_modules: ["dispatch-line_message-1"],
                                    msgId: Date.parse(new Date())
                                };
                                websocket.send(JSON.stringify(package_send));
                                var dataSite_top_color_cof = {};
                                var dataSite_down_color_cof = {};
                                for (var i = 0; i < res_top.length; i++) {
                                    var color = 'color' + res_top[i].id;
                                    dataSite_top_color_cof[color] = 'blue';
                                }
                                for (var i = 0; i < res_down.length; i++) {
                                    var color = 'color' + res_down[i].id;
                                    dataSite_down_color_cof[color] = 'blue';
                                }
                                socket_model_info[model_id] =
                                    {
                                        fn: self.site_websocket,
                                        arg: {
                                            self: self,
                                            site_top_infos: res_top,
                                            site_down_infos: res_down,     //此处修改
                                            dataSite_top_color_cof: dataSite_top_color_cof,
                                            dataSite_down_color_cof: dataSite_down_color_cof,
                                            busTopNumber: '',
                                            busDownNumber: '',
                                            hasCar: []
                                        }
                                    };

                            });
                        });
                    });
                }
            }

            // 上行站点
            site_info(this.model_line, this.model_station_platform)
            // 下行站点
            // site_info(this.model_site_down)
            //阻止右键引起的默认事件
            self.$('.can_top').bind('contextmenu', function () {
                return false;
            });
            self.$('.can_bottom').bind('contextmenu', function () {
                return false;
            });
        },
        site_websocket: function (data_list, arg) {
            var self = arg.self;
            var data_use = JSON.parse(data_list)
            //配车数量...
            for (var i = 0; i < self.$('.bus_info li').length; i++) {
                self.$('.bus_info li').eq(i).find('span').html(10);
            }
            var data = new Object();
            //站点到起点距离
            //分段颜色
            data.color = [
                "#4dcf22",
                "#ffd233",
                "#cc2111",
                "#f69144",
                "#a19dde",
                "#cc21ff",
            ];
            data.site_top_infos = arg.site_top_infos;
            data.site_down_infos = arg.site_down_infos;
            if (data_use.type == "2001") {
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

            if (data_use.type == "1031") {
                if (data_use.data.direction == 0) {
                    arg.busTopNumber = data_use.data.bus_no_of_park + '辆';
                }
                if (data_use.data.direction == 1) {
                    arg.busDownNumber = data_use.data.bus_no_of_park + '辆';
                }
            }
            // if(data_use.type== "1032"){
            //     debugger
            //     var road_info = data_use.data.road_condition.split('|');
            //     for(var i = 0;i<road_info.length;i++){
            //         data.color.push(parseInt(road_info[i].split(',')[0]));
            //     }
            // }
            //车辆实时位置
            if (data_use.type == "1035") {
                //如果车辆id未出现
                if (arg.hasCar.indexOf(data_use.data.bus_no) == -1) {
                    arg.hasCar.push(data_use.data.bus_no);
                    //车辆上行方向
                    // 添加车辆
                    self.$el.find('.content_car_road_top').append($('.run_car_hide').html());
                    // 上下行方向
                }
                // 车辆进出站
                if (data_use.data.type == "in") {
                    var oLeft = 1190 * (parseInt(data_use.data.status) + 0.5) / arg.site_top_infos.length;
                } else {
                    var oLeft = 1190 * (parseInt(data_use.data.status) + 1) / arg.site_down_infos.length;
                }
                //车辆上下行
                if (data_use.data.direction == 0) {
                    self.$('.content_car_road_top').find('.line_car').attr('bus_no', data_use.data.bus_no).css('left', oLeft - 22 + 'px');
                } else {
                    self.$('.content_car_road_down').find('.line_car').attr('bus_no', data_use.data.bus_no).css('left', 1190 - oLeft - 22 + 'px');
                }
                self.$('.content_car_road_top').find('.line_car[bus_no=' + data_use.data.bus_no + ']').find('.num_car span').html(data_use.data.line_id);
                self.$('.content_car_road_top').find('.line_car[bus_no=' + data_use.data.bus_no + ']').find('.type_car span').html(data_use.data.status);
                // 进出场
            }
            data.busTopNumber = arg.busTopNumber;
            data.busDownNumber = arg.busDownNumber;
            data.subsection = [1, 2, 3, 4, 5, 6];
            //公交模拟地图canvas
            // 距离车场距离
            // if (!isNaN((data.subsection[0]))) {
            qrend_desktop_canvas(data, '.can_top', '.can_bottom', '.canvas_left', '.canvas_right', self.$el);
            // 线路颜色
            self.color = data.color;
            self.site_top_infos = data.site_top_infos;
            self.site_down_infos = data.site_down_infos;
            // 站点颜色
            self.dataSite_top_color = arg.dataSite_top_color_cof;
            self.dataSite_down_color = arg.dataSite_down_color_cof;
            self.subsection = data.subsection;
            // }
            // 上下行的车辆的拥挤人数数量
            // $('.park_left').html('')
        },
        events: {
            //上下的车辆是否隐藏
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
            'mouseup .bus_info': 'bus_man_src',
            //鼠标划过上下行车路线时的cursor属性

            // 右击站点事件
            'click .min': 'closeFn'
            // 行车组件关闭
        }
        ,
        closeFn: function () {
            var self = this;
            var tid = this.$el.attr('tid');
            var desktop_id = self.desktop_id;
            //已经添加了路线
            //  var package = {
            //     type: 1001,
            //     open_modules: "dispatch-passenge_flow-4",
            //     msgId: Date.parse(new Date())
            // };
            // websocket.send(JSON.stringify(package));
            if (tid != undefined) {
                // socket_model_info[tid].status =false;
                // 查询tid,拿到tid下面的lineid并得到相同lineid的一条线路
                self.model_line.query().filter([["desktop_id", '=', parseInt(desktop_id)], ["id", "=", tid]]).all().then(function (pp) {
                    // 查询tid下的lineid
                    self.model_line.query().filter([["line_id", "=", pp[0].line_id[0]]]).all().then(function (data) {
                        // 删除该tid，即此线路
                        self.model_line.call("unlink", [data[1].id]).then(function () {
                            self.$el.parent().find('.updown_line_table').remove();
                            self.model_line.call("unlink", [data[0].id]).then(function () {
                                self.destroy();
                            });
                        });
                    });
                });
            }
            //未添加路线
            else {
                self.$el.parent().find('.updown_line_table').remove();
                self.destroy();
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
            if (canvas.site_infos) {
                for (var i = 0; i < canvas.site_infos.length; i++) {
                    var everyLen = 1190 * (i + 0.5) / canvas.site_infos.length;
                    cxt.beginPath();
                    //渲染参数，x距离,y距离,半径,起始角，结束角，是否顺势针
                    cxt.arc(everyLen, canvas.ciry, 3, 0, 360, false);
                    //判断鼠标的点是否在圆圈内
                    if (cxt.isPointInPath(x, y)) {
                        c.style.cursor = 'pointer';
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
            var line_id = e.delegateTarget.getAttribute("line_id");
            var zIndex = parseInt(this.$el[0].style.zIndex) + 1;
            var options =
                {
                    x: e.clientX + 5,
                    y: e.clientY + 5,
                    zIndex: zIndex,
                    line_id: line_id,
                    car_num: car_num,
                    controllerId: this.desktop_id
                };
            if (line_id != 5 || car_num != 222) {
                layer.alert("模拟soket实时加载，请选择572线路222号车进行点击", {title: "车辆实时信息"});
                return false;
            }
            ;
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
            //调用点击canvas事件
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
                        url: 'http://10.1.254.122:8080/ltyop/planData/query?apikey=71029270&params={tablename:"op_busresource",controlsId:2032,gprsId:161}',
                        type: 'get',
                        dataType: 'json',
                        data: {},
                        success: function (data) {
                            console.log(data)
                            function getLocalTime(nS) {
                                return new Date(parseInt(nS) * 1000).toLocaleString().replace(/:\d{1,2}$/, ' ');
                            }

                            for (var i = 0; i < data.respose.length; i++) {
                                if (data.respose[i].planRunTime > 0) {
                                    data.respose[i].planRunTime = getLocalTime(data.respose[i].planRunTime / 1000);
                                }
                                if (data.respose[i].realReachTime > 0) {
                                    data.respose[i].realReachTime = getLocalTime(data.respose[i].realReachTime / 1000);
                                }
                            }
                            new bus_source_config(this, options, data).appendTo($(".controller_" + options.controllerId));
                        },
                        error: function () {
                            alert("请求出错")
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

            if (e.button == 2) {
                if ($('body').find('.bus_site_info').length > 0) {
                    $('body').find('.bus_site_info').remove();
                }
                var options =
                    {
                        x: event.clientX - self.$el[0].offsetLeft + 5,
                        y: event.clientY - self.$el[0].offsetTop + 5,
                        zIndex: zIndex,
                    };
                new bus_site_info(this, options).appendTo(this.$el);
            }
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
                        var traffic_top = {
                            id: canvas.id,
                            y: canvas.ciry - 1,
                            self: canvas.self,
                            subsection: canvas.subsection,
                            color: canvas.color
                        };
                        traffic_distance(traffic_top);
                        var cir_text = {
                            id: canvas.id,
                            ciry: canvas.ciry,
                            testy: canvas.testy,
                            self: canvas.self,
                            color: canvas.color,
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
                                        y: e.clientY + 5,
                                        zIndex: zIndex,
                                        controllerId: self.desktop_id,
                                        line_id: canvas.self.attr("line_id"),
                                        site: canvas.site_infos[i].station_id[1].split('/')[0],
                                        site_id: canvas.site_infos[i].id,
                                        site_infos: self.site_top_infos
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
            self.model_choseline.query().filter([["state", "=", 'inuse']]).all().then(function (data) {
                self.$('.edit_content .chs').html('')
                for (var i = 0; i < data.length; i++) {
                    if (data[i].id) {
                        var oLi = "<li lineid=" + data[i].id + ">" + data[i].line_name + "</li>";
                        self.$('.edit_content .chs').append(oLi);
                    }
                }
            });
            self.$('.edit_content');
            self.$('.edit_content').show();
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
                        y: e.clientY + 5,
                        zIndex: zIndex,
                        line_id: self.$el.attr("line_id"),
                        line_name: self.$el.attr("line_name"),
                        controllerId: self.desktop_id
                    };
                if ($(".linePlanParkOnlineModel_" + options.line_id).length > 0) {
                    return;
                } else {
                    // try {
                    //     $(".linePlanParkOnlineModel").remove();
                    var dialog = new plan_display(self, options);
                    dialog.appendTo($(".controller_" + options.controllerId));
                    // } catch(e){
                    // var layer_index = layer.msg("websoket断开链接，请检查网络是否通畅", {shade: 0.3});
                    // }
                }
            }
        }
    });
//选择车辆组件
//上下行路线组件
// 线路选择

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
                    if (data[0].model_type == "dispatch_desktop") {
                        new dispatch_canvas(this, data[0]).appendTo(this.$el);
                        this.$el.find('.line_edit').hide();
                        // 只存在updown_line_table组件
                    } else if (data[0].model_type == "updown_line_table") {
                        new dispatch_updown_line(this, data[0]).appendTo(this.$el);
                    }
                    // 存在完整组件
                } else if (data.length > 1) {
                    new dispatch_canvas(this, data[0]).appendTo(this.$el);
                    new dispatch_updown_line(this, data[1]).appendTo(this.$el);
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
                new dispatch_canvas(this, data[0]).appendTo(this.$el);
                new dispatch_updown_line(this, data[1]).appendTo(this.$el);
            }
        },
        events: {
            'click .chs>li': 'chose_line',
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
                    alert('该线路已被选择，请重新选择');
                } else {
                    layer.load(1)
                    self.model_line.call("create", [
                        {
                            'desktop_id': desktop_id,
                            "model_type": "dispatch_desktop",
                            'position_left': siteLeft,
                            'position_top': siteTop,
                            'position_z_index': 0,
                            'line_id': $(x).attr('lineid'),
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
                                layer.closeAll('loading');
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
                    alert('该线路已被选择，请重新选择');
                } else {
                    layer.load(1)
                    self.model_line.call("write", [parseInt(tid),
                        {
                            'line_id': $(x).attr("lineid"),
                            'position_left': siteLeft,
                            'position_top': siteTop,
                            'position_z_index': 0,
                            'name': x.innerHTML,
                        }]).then(function (res) {
                        self.model_line.call("write", [parseInt(tid) + 1,
                            {
                                'line_id': $(x).attr("lineid"),
                                'position_left': siteLeftPf,
                                'position_top': siteTopPf,
                                'position_z_index': 0,
                                'name': x.innerHTML,
                            }]).then(function (res) {
                            self.model_line.query().filter([["desktop_id", '=', parseInt(desktop_id)], ["line_id", "=", parseInt(line)]]).all().then(function (data) {
                                data[1].position_left = self.$el.find('.updown_line_table')[0].offsetLeft;
                                data[1].position_top = self.$el.find('.updown_line_table')[0].offsetTop;
                                data[1].position_z_index = self.$el.find('.updown_line_table')[0].style.zIndex;
                                layer.closeAll('loading');
                                self.$el.html('');
                                new dispatch_bus(this, data, 0).appendTo(self.$el);
                            });
                        });
                    });
                }
            }
        },
    });
//车辆组件

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
            var tid = this.$el.find('.updown_line_table').attr('tid');
            self.model_line.call("write", [parseInt(tid),
                {
                    'tem_display': ''
                }]).then(function (res) {
                self.$el.find('.updown_line_table').show();
                $(x).hide();
                $(x).siblings('.line_edit').show();
            });
        }
    });
    return dispatch_bus;
})
;