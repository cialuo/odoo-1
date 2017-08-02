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
            this.model2 = new Model('dispatch.control.desktop.component');
            this.model_choseline = new Model('route_manage.route_manage');
            this.dis_desk = data;
            console.log(data);
        },
        start: function () {
            var self = this;
            var data = this.dis_desk;
            if (data) {
                // qrend_desktop(data, '.can_top', '.can_bottom', '.canvas_left', '.canvas_right',self.$el);
                var websocket = null;
                //判断当前浏览器是否支持WebSocket
                if ('WebSocket' in window) {
                    websocket = new SockJS("http://127.0.0.1:8766/wstest?userId=45454");
                }
                else {
                    alert('当前浏览器 Not support websocket');
                }
                //连接发生错误的回调方法
                websocket.onerror = function () {
                    setMessageInnerHTML("WebSocket连接发生错误");
                };
                //连接成功建立的回调方法
                websocket.onopen = function () {
                    setMessageInnerHTML("WebSocket连接成功");
                }
                //接收到消息的回调方法
                var controllerId, moduleName, recv;
                websocket.onmessage = function (event) {
                    setMessageInnerHTML(event.data);
                };
                //连接关闭的回调方法
                websocket.onclose = function () {
                    setMessageInnerHTML("WebSocket连接关闭");
                };
                //监听窗口关闭事件，当窗口关闭时，主动去关闭websocket连接，防止连接还没断开就关闭窗口，server端会抛异常。
                window.onbeforeunload = function () {
                    closeWebSocket();
                };
                //将消息显示在网页上
                function setMessageInnerHTML(innerHTML) {
                    self.$el.find('.aaa')[0].innerHTML = innerHTML.substring(78, 80);
                    var a = self.$el.find('.line_car')[0];
                    //配车数量...
                    for (var i = 0; i < self.$('.bus_info li').length; i++) {
                        self.$('.bus_info li').eq(i).find('span').html(innerHTML.substring(78 + i, 80 + i));
                    }
                    var data = new Object();
                    data.dataCir = [12, 200, 300, 450, 600, 860, 1170];
                    data.color = ["#ff46" + innerHTML.substring(78, 80), "#4dcf" + innerHTML.substring(78, 80), "#ffd2" + innerHTML.substring(78, 80), "#cc21" + innerHTML.substring(78, 80), "#4dcf" + innerHTML.substring(78, 80), "#f691" + innerHTML.substring(78, 80), "#a19e" + innerHTML.substring(78, 80), "#cc21" + innerHTML.substring(78, 80)];
                    data.dataSite = [{'name': "武汉", 'status': '1', 'color': '#f' + innerHTML.substring(78, 80) + 'f75'},
                        {'name': "武汉", 'status': '0', 'color': '#cc2' + innerHTML.substring(78, 80) + '3'},
                        {'name': "武汉", 'status': '1', 'color': '#ffd2' + innerHTML.substring(78, 80)},
                        {'name': "武汉", 'status': '1', 'color': '#4' + innerHTML.substring(78, 80) + 'df7'},
                        {'name': "武汉", 'status': '1', 'color': '#ffcf' + innerHTML.substring(78, 80)},
                        {'name': "武汉", 'status': '1', 'color': '#ffd2' + innerHTML.substring(78, 80)},
                        {'name': "武汉", 'status': '1', 'color': '#aad2' + innerHTML.substring(78, 80)},
                        {'name': "武汉", 'status': '1', 'color': '#cc21' + innerHTML.substring(78, 80)}];
                    data.dataSite2 = [{'name': "武汉1", 'status': '0', 'color': '#ffd2' + innerHTML.substring(78, 80)},
                        {'name': "武汉1", 'status': '0', 'color': '#cc' + innerHTML.substring(78, 80) + '21'},
                        {'name': "武汉2", 'status': '1', 'color': '#' + innerHTML.substring(78, 80) + 'ffd2'},
                        {'name': "武汉3", 'status': '1', 'color': '#cf' + innerHTML.substring(77, 81)},
                        {'name': "武汉4", 'status': '1', 'color': '#c7' + innerHTML.substring(78, 82)},
                        {'name': "武汉5", 'status': '1', 'color': '#cc7' + innerHTML.substring(77, 80)},
                        {'name': "武汉6", 'status': '1', 'color': '#ffd2' + innerHTML.substring(78, 80)},
                        {'name': "武汉7", 'status': '1', 'color': '#dc' + innerHTML.substring(80, 83) + '3'}];
                    data.subsection = [];
                    for (var j = 0; j < 8; j++) {
                        data.subsection.push(parseInt(innerHTML.substring(78 + j, 80 + j)));
                    }
                    data.busNumber = parseInt(innerHTML.substring(78, 79));
                    //公交模拟地图canvas
                    if (!isNaN((data.subsection[0]))) {
                        qrend_desktop(data, '.can_top', '.can_bottom', '.canvas_left', '.canvas_right', self.$el);
                        self.dataCir = data.dataCir;
                        self.color = data.color;
                        self.dataSite = data.dataSite;
                        self.dataSite2 = data.dataSite2;
                        self.subsection = data.subsection;
                        self.busNumber = data.busNumber;
                    }
                    var toLeft = parseInt(innerHTML.substring(80, 81));
                    var oLeft = self.$el.find('.line_car')[0].offsetLeft;
                    toLeft += oLeft;
                    self.$('.content_car_road').eq(0).find('.line_car').css({
                        'position': 'absolute',
                        'left': toLeft + 'px',
                        'top': '0'
                    });
                }

                //关闭WebSocket连接
                function closeWebSocket() {
                    websocket.close();
                }

                //发送消息
                function send() {
                    var message = document.getElementById('text').value;
                    websocket.send(message);
                }
            }
            self.$('.can_top').bind('contextmenu',function(){
                return false;
            });
            self.$('.can_bottom').bind('contextmenu',function(){
                return false;
            });
        },
        events: {
            //上下的车辆是否隐藏
            'mousedown .can_top': 'clk_can_top',
            'click .can_bottom': 'clk_can_bottom',
            // 删除选择路线弹框
            'click .del': 'del_chose_line',
            // 选择路线
            'click .line_edit': 'show_chose_line',
            //车辆信息
            'click .type_car': 'bus_info',
            // 左右侧车场
            'click .canvas_left': 'clk_can_left',
            'click .canvas_right': 'clk_can_right',
            // 鼠标划过上左右车场时的cursor属性
            'mousemove .canvas_left': 'slide_cursor_pointer_left',
            'mousemove .canvas_right': 'slide_cursor_pointer_right',
            //点击上方详情
            'mouseup .bus_info': 'bus_man_src',
            //鼠标划过上下行车路线时的cursor属性
            'mousemove .can_top': 'slide_cursor_pointer_top',
            'mousemove .can_bottom': 'slide_cursor_pointer_bottom',
            // 右击站点事件
            'click .min': 'closeFn'
        },
        closeFn: function () {
            var tid = this.$el.attr('tid');
            this.model2.call("unlink",[parseInt(tid)]).then(function () {
                alert("delete!!!");
            })
            this.destroy();
        },
        cursor_pointer_tb: function (canvas, e) {
            var e = e || window.event;
            var c = this.$el.find(canvas.cId)[0];
            var cxt = c.getContext("2d");
            var x = e.pageX - c.getBoundingClientRect().left;
            var y = e.pageY - c.getBoundingClientRect().top;
            c.style.cursor = 'auto';
            if (canvas.dataCir) {
                for (var i = 0; i < canvas.dataCir.length; i++) {
                    cxt.beginPath();
                    //渲染参数，x距离,y距离,半径,起始角，结束角，是否顺势针
                    cxt.arc(canvas.dataCir[i], canvas.ciry, 3, 0, 360, false);
                    //判断鼠标的点是否在圆圈内
                    if (cxt.isPointInPath(x, y)) {
                        c.style.cursor = 'pointer';
                    }
                    cxt.closePath();
                    cxt.beginPath();
                    if (canvas.dataSite[i].status == 1) {
                        cxt.rect(canvas.dataCir[i] - (6 * canvas.dataSite[i].name.length), canvas.testy - 16, 12 * canvas.dataSite[i].name.length, 16)
                        if (cxt.isPointInPath(x, y)) {
                            c.style.cursor = 'pointer';
                        }
                    }
                }
            }

        },
        slide_cursor_pointer_top: function (e) {
            var option = {
                cId: '.can_top',
                dataCir: this.dataCir,
                dataSite: this.dataSite,
                testy: 13,
                ciry: 27
            }
            this.cursor_pointer_tb(option, e);
        },
        slide_cursor_pointer_bottom: function (e) {
            var option = {
                cId: '.can_bottom',
                dataCir: this.dataCir,
                dataSite: this.dataSite2,
                testy: 25,
                ciry: 6
            }
            this.cursor_pointer_tb(option, e);
        },
        bus_info: function (e) {
            var car_num = e.target.textContent;
            var line_id = e.delegateTarget.getAttribute("tid");
            var options =
                {
                    x: e.clientX + 5,
                    y: e.clientY + 5,
                    zIndex: 5,
                    line_id: line_id,
                    car_num: car_num
                };
            var dialog = new bus_real_info(this, options);
            dialog.appendTo($("body"));
            // e.delegateTarget.parentElement.append(dialog);
        },
        clk_can_top: function (e) {
            var option = {
                id: '.can_top',
                ciry: 27,
                testy: 13,
                self: this.$el,
                dataCir: this.dataCir,
                color: this.color,
                dataSite: this.dataSite,
                subsection: this.subsection
            };
            //调用点击canvas事件
            this.clickTb(option, e);
        },
        clk_can_bottom: function (e) {
            var option = {
                id: '.can_bottom',
                ciry: 6,
                testy: 25,
                self: this.$el,
                dataCir: this.dataCir,
                color: this.color,
                dataSite: this.dataSite2,
                subsection: this.subsection
            }
            this.clickTb(option, e);
        },
        bus_man_src: function (e) {
            if (!isDrag) {
                //先把doMouseDownTimmer清除，不然200毫秒后setGragTrue方法还是会被调用的
                clearTimeout(timmerHandle);
                var line_id = e.delegateTarget.getAttribute("tid");
                var options =
                    {
                        x: e.clientX + 5,
                        y: e.clientY + 5,
                        zIndex: 5,
                        line_id: line_id,
                    };
                var abc = new bus_source_config(this, options);
                abc.appendTo($("body"));
            }
            else {
                isDrag = false;
            }
        },
        clickTb: function (canvas, e) {
            var event = e || window.event;
            var c = canvas.self.find(canvas.id)[0];
            var cxt = c.getContext("2d");
            var x = event.pageX - c.getBoundingClientRect().left;
            var y = event.pageY - c.getBoundingClientRect().top;
            for (var i = 0; i < canvas.dataCir.length; i++) {
                cxt.beginPath();
                //渲染参数，x距离,y距离,半径,起始角，结束角，是否顺势针
                cxt.arc(canvas.dataCir[i], canvas.ciry, 3, 0, 360, false);
                //判断鼠标的点是否在圆圈内
                if (cxt.isPointInPath(x, y)) {
                    c.style.cursor = 'pointer';
                    //获取鼠标点击区域的颜色值
                    var imgData = cxt.getImageData(x, y, 1, 1);
                    // 重绘画布
                    cxt.clearRect(0, 0, c.width, c.height);
                    canvas.dataSite[i].status == 1 ? canvas.dataSite[i].status = 0 : canvas.dataSite[i].status = 1;
                    var traffic_top = {
                        id: canvas.id,
                        y: canvas.ciry - 1,
                        self: canvas.self,
                        subsection: canvas.subsection,
                        color: canvas.color
                    };
                    traffic_distance(traffic_top);
                    var cirTop1 = {
                        id: canvas.id,
                        ciry: canvas.ciry,
                        testy: canvas.testy,
                        self: canvas.self,
                        color: canvas.color,
                        dataCir: canvas.dataCir,
                        dataSite: canvas.dataSite
                    };
                    cir_and_text(cirTop1);
                    cxt.closePath();
                    // 转换16进制像素
                    var hex = "#" + ((1 << 24) + (imgData.data[0] << 16) + (imgData.data[1] << 8) + imgData.data[2]).toString(16).slice(1);
                    if (hex == "#ffffff") {
                        // 清除画布
                        // 绘上实心圆
                        cxt.beginPath();
                        cxt.arc(canvas.dataCir[i], canvas.ciry, 4, 0, 360, false);
                        cxt.fillStyle = canvas.dataSite[i].color;
                        cxt.fill();
                        cxt.closePath();
                    } else {
                        cxt.beginPath();
                        cxt.arc(canvas.dataCir[i], canvas.ciry, 4, 0, 360, false);
                        cxt.fillStyle = "white";
                        cxt.fill();
                        cxt.closePath();
                    }
                    break
                }
                cxt.closePath();
                cxt.beginPath();
                if (canvas.dataSite[i].status == 1) {
                    cxt.rect(canvas.dataCir[i] - (6 * canvas.dataSite[i].name.length), canvas.testy - 16, 12 * canvas.dataSite[i].name.length, 16)
                    if (cxt.isPointInPath(x, y)) {
                        //如果是左击
                        if (e.button == 0) {
                            var options =
                                {
                                    x: e.clientX + 5,
                                    y: e.clientY + 5,
                                    zIndex: 5,
                                    line_id: canvas.self.attr("tid")
                                };
                            var dialog = new passenger_flow(this, options);
                            dialog.appendTo($("body"));
                            cxt.closePath();
                        }
                        //如果是右击
                        else if (e.button == 2) {
                            if (canvas.dataSite[i].status == 1) {
                                cxt.rect(canvas.dataCir[i] - (6 * canvas.dataSite[i].name.length), canvas.testy - 16, 12 * canvas.dataSite[i].name.length, 16)
                                if (cxt.isPointInPath(x, y)) {
                                    var options =
                                        {
                                            x: x + 5 + 12 + 26,
                                            y: y + 5 + 55,
                                            zIndex: 5,
                                        };
                                    new bus_site_info(this, options).appendTo(this.$el);
                                    cxt.closePath();
                                    //如果提供了事件对象，则这是一个非IE浏览器
                                }
                            }
                        }
                    }
                }

            }
        },
        // 点击左侧车场
        clk_can_left: function (e) {
            this.click_lr({
                id: '.canvas_left',
            }, e);
        },
        // 点击右侧车场
        clk_can_right: function (e) {
            this.click_lr({
                id: '.canvas_right',
            }, e);
        },
        del_chose_line: function () {
            this.$('.edit_content').hide();
        },
        show_chose_line: function () {
            var self = this;
            self.model_choseline.query().filter([["state", "=", 'inuse']]).all().then(function (data) {
                console.log(data)
                self.$('.edit_content .chs').html('')
                for (var i = 0; i < data.length; i++) {
                    if (data[i].id) {
                        var oLi = "<li lineid=" + data[i].id + ">" + data[i].lineName + "</li>";
                        self.$('.edit_content .chs').append(oLi);
                    }
                }
            })
            self.$('.edit_content');
            self.$('.edit_content').show();

        },
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
        },
        slide_cursor_pointer_left: function (e) {
            this.cursor_pointer_lr({
                id: '.canvas_left',
            }, e);
        },
        slide_cursor_pointer_right: function (e) {
            this.cursor_pointer_lr({
                id: '.canvas_right',
            }, e);
        },
        //左侧的停车场的点击事件
        click_lr: function (canvas, e) {
            var event = e || window.event;
            var c = this.$el.find(canvas.id)[0];
            var cxt = c.getContext("2d");
            var x = event.pageX - c.getBoundingClientRect().left;
            var y = event.pageY - c.getBoundingClientRect().top;
            cxt.arc(13, 58, 13, 0, 360, false);
            if (cxt.isPointInPath(x, y)) {
                var options =
                    {
                        x: e.clientX + 5,
                        y: e.clientY + 5,
                        zIndex: 5,
                        line_id: this.$el.attr("tid")
                    };
                var dialog = new plan_display(this, options);
                dialog.appendTo($("body"));
            }
        }
    });
    //选择车辆组件
    //上下行路线组件
    // 线路选择
    var dispatch_line_control = Widget.extend({
        init: function (parent, data) {
            this._super(parent);
            this.model2 = new Model('dispatch.control.desktop.component');
            this.model_choseline = new Model('route_manage.route_manage');
            this.data = data;
        },
        start: function () {
            var data = this.data;
            new dispatch_canvas(this, data).appendTo(this.$el);
            new dispatch_updown_line(this, data).appendTo(this.$el);
        },
        events: {
            'click .chs>li': 'chose_line',
        },
        chose_line: function (event) {
            var x = event.currentTarget;
            var self = this;
            var dom = self.$el;
            var exitline = $('body').find('.dispatch_desktop .line_line');
            var res = [];
            for (var i = 0; i < exitline.length; i++) {
                var exitline_info = exitline[i].innerHTML;
                res.push(exitline_info);
            }
            var tidLen = $('body').find('.dispatch_desktop').length;
            var tid = self.$el.find('.dispatch_desktop')[0].getAttribute('tid');
            var siteZindex = self.$el.find('.dispatch_desktop')[0].style.zIndex;
            var siteLeft = self.$el.find('.dispatch_desktop')[0].offsetLeft;
            var siteTop = self.$el.find('.dispatch_desktop')[0].offsetTop;
            if (tid == '') {
                if (tidLen > 1) {
                    tid = $('body').find('.dispatch_desktop')[tidLen - 1].getAttribute('tid') + 1;
                } else {
                    tid = 1;
                }
                // self.model2.call("write", [tid,
                //     {
                //         'line_id': $(x).attr('lineid'),
                //         'position_left': siteLeft,
                //         'position_top': siteTop,
                //         'position_z_index': siteZindex,
                //     }]).then(function (data) {
                //
                // });
                self.model2.call("create", [
                    {
                        'desktop_id': 2,
                        'id': tid,
                        'position_left': siteLeft,
                        'position_top': siteTop,
                        'position_z_index': siteZindex,
                        'line_id': $(x).attr('lineid'),
                        'name': x.innerHTML
                    }]).then(function (data) {
                    self.model2.query().filter([["id", "=", data]]).all().then(function (data) {
                        self.$el.html('');
                        new dispatch_canvas(this, data[0]).appendTo(self.$el);
                    });
                });
            } else if (tid) {
                self.model2.call("write", [parseInt(tid),
                    {
                        'line_id': $(x).attr("lineid"),
                        'position_left': siteLeft,
                        'position_top': siteTop,
                        'position_z_index': siteZindex,
                        'name': x.innerHTML,
                    }]).then(function (data) {
                    self.model2.query().filter([["id", "=", tid]]).all().then(function (data) {
                        self.$el.html('');
                        new dispatch_canvas(this, data[0]).appendTo(self.$el);
                    });
                });
            }
            // var chartTop = self.$el.find('.updown_line_table')[0].offsetTop;
            // 读取线路接口
            //odoo自带write更新方法
            // data[1].oneline.line_show_or_hide.left = siteLeft;
            // data[1].oneline.line_show_or_hide.top = siteTop;
            // data[1].oneline.chart_show_or_hide.left = chartLeft;
            // data[1].oneline.chart_show_or_hide.top = chartTop;
            // self.$el.html('');
            // //渲染车辆canvas图形组件
            //
            // var a = $('body').find('.dispatch_desktop')
            // new dispatch_canvas(this, data[1]).appendTo(self.$el);
            // new dispatch_updown_line(this, data[1]).appendTo(self.$el);
            // //渲染车辆客流与运力组件
            // qrend_desktop(data[1], '.can_top', '.can_bottom', '.canvas_left', '.canvas_right', dom);
            // self.dataCir = data[1].oneline.site_to_startpoint;
            // self.color = data[1].oneline.plan_feedback;
            // self.dataSite = data[1].oneline.siteTop;
            // self.dataSite2 = data[1].oneline.siteBottom;
            // self.subsection = data[1].oneline.traffic_distance;

        },
    });
    //车辆组件

    //整个车行的组件
    var dispatch_bus = Widget.extend({
        init: function (parent, data) {
            this._super(parent);
            // this.model = new Model('lty_dispatch_desktop.lty_dispatch_desktop');
            this.data = data;
        },
        start: function () {
            var data = this.data;
            new dispatch_line_control(this, data).appendTo(this.$el);
        }
    })
    return dispatch_bus;
});