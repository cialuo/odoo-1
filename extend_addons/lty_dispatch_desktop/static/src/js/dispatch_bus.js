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
    var bus_real_info = require('lty_dispatch_desktop_widget.bus_real_info');
    var passenger_flow = require('lty_dispatch_desktop_widget.passenger_flow');
    var plan_display = require('lty_dispatch_desktop_widget.plan_display');

   //最原始车辆组件
    var dispatch_canvas=Widget.extend({
         template:'dispatch_desktop',
         init: function (parent,data) {
            this._super(parent);
            this.model = new Model('lty_dispatch_desktop.lty_dispatch_desktop');
            this.dis_desk = data;
        },
        start: function () {
            var self = this;
            var data=this.dis_desk;
            if(data){
                qrend_desktop(data, '.can_top', '.can_bottom', '.canvas_left', '.canvas_right',self.$el);

                self.dataCir = data.oneline.site_to_startpoint;
                self.color = data.oneline.plan_feedback;
                self.dataSite = data.oneline.siteTop;
                self.dataSite2 = data.oneline.siteBottom;
                self.subsection = data.oneline.traffic_distance;
                // var websocket = null;
                // //判断当前浏览器是否支持WebSocket
                // if ('WebSocket' in window) {
                //     websocket = new SockJS("http://127.0.0.1:8766/wstest?userId=45454");
                // }
                // else {
                //     alert('当前浏览器 Not support websocket');
                // }
                // //连接发生错误的回调方法
                // websocket.onerror = function () {
                //     setMessageInnerHTML("WebSocket连接发生错误");
                // };
                // //连接成功建立的回调方法
                // websocket.onopen = function () {
                //     setMessageInnerHTML("WebSocket连接成功");
                // }
                // //接收到消息的回调方法
                // var controllerId, moduleName, recv;
                // websocket.onmessage = function (event) {
                //     setMessageInnerHTML(event.data);
                // };
                // //连接关闭的回调方法
                // websocket.onclose = function () {
                //     setMessageInnerHTML("WebSocket连接关闭");
                // };
                // //监听窗口关闭事件，当窗口关闭时，主动去关闭websocket连接，防止连接还没断开就关闭窗口，server端会抛异常。
                // window.onbeforeunload = function () {
                //     closeWebSocket();
                // }
                // //将消息显示在网页上
                // function setMessageInnerHTML(innerHTML) {
                //     for(var i = 0;i<$('body').find('.aaa').length;i++){
                //         $('body').find('.aaa')[i].innerHTML=innerHTML.substring(78+i,80+i);
                //     }
                // }
                //
                // //关闭WebSocket连接
                // function closeWebSocket() {
                //     websocket.close();
                // }
                //
                // //发送消息
                // function send() {
                //     var message = document.getElementById('text').value;
                //     websocket.send(message);
                // }
            }
        },
        events: {
            'click .can_top': 'clk_can_top',
            'click .can_bottom': 'clk_can_bottom',
            'click .del': 'del_chose_line',
            'click .line_edit': 'show_chose_line',
            'click .type_car': 'bus_info',
            'click .canvas_left':'clk_can_left',
            'click .canvas_right':'clk_can_right',
            'mouseup .bus_info':'bus_man_src'
        },
        bus_info:function (e) {
            var car_num = e.target.textContent;
            var line_id = e.delegateTarget.getAttribute("tid");
            var options = 
                {
                    x:e.clientX+5,
                    y:e.clientY+5,
                    zIndex:5,
                    line_id: line_id,
                    car_num: car_num
                };
            $(".bus_real_info").remove();
            var dialog = new bus_real_info(this, options);
            dialog.appendTo($("body"));
            // e.delegateTarget.parentElement.append(dialog);
        },
        clk_can_top:function (e) {
            var self = this;
            var dom = self.$el;
            self.clickTb({
                id: '.can_top',
                ciry: 27,
                testy: 13,
                self: dom,
                dataCir: self.dataCir,
                color: self.color,
                dataSite: self.dataSite,
                subsection: self.subsection
            }, e);
        },
        clk_can_bottom: function (e) {
            var self = this;
            var dom = self.$el;
            self.clickTb({
                id: '.can_bottom',
                ciry: 6,
                testy: 25,
                self: dom,
                dataCir: self.dataCir,
                color: self.color,
                dataSite: self.dataSite2,
                subsection: self.subsection
            }, e);
        },
        clk_can_left:function(e){
            var self = this;
            var dom = self.$el;
            self.clickLr({
                id: '.canvas_left',
                self: dom,
            }, e);
        },
        clk_can_right:function(e){
            var self = this;
            var dom = self.$el;
            self.clickLr({
                id: '.canvas_right',
                self: dom,
            }, e);
        },
        del_chose_line: function () {
            var self = this;
            self.$('.edit_content').hide();
        },
        show_chose_line: function () {
            var self = this;
            self.$('.edit_content').show();
        },
        bus_man_src:function (e) {
            if(hasmove == false){
            var self = this;
            var line_id = e.delegateTarget.getAttribute("tid");
            var options =
                {
                    x:e.clientX+5,
                    y:e.clientY+5,
                    zIndex:5,
                    line_id: line_id,
                };
            var abc=new bus_source_config(this,options);
            abc.appendTo($("body"));
            }
            hasmove = false;
            document.onmousemove = null;
            document.onmouseup = null;
        },
        //左侧的停车场的点击事件
        clickLr:function (canvas,e) {
            var cId = canvas.id;
            var self = canvas.self;
            var event = e || window.event;
            var c = self.find(cId)[0];
            var cxt = c.getContext("2d");
            var x = event.pageX - c.getBoundingClientRect().left;
            var y = event.pageY - c.getBoundingClientRect().top;
            cxt.arc(13, 58, 13, 0, 360, false);
            if (cxt.isPointInPath(x, y)) {
                var options = 
                    {
                        x:e.clientX+5, 
                        y:e.clientY+5, 
                        zIndex:5,
                        line_id: self.attr("tid")
                    };
                var dialog = new plan_display(this, options);
                $(".plan_display").remove();
                dialog.appendTo($("body"));
            }
        },
        clickTb: function (canvas, e) {
            var event = e || window.event;
            var dataCir = canvas.dataCir;
            var cId = canvas.id;
            var ciry = canvas.ciry;
            var testy = canvas.testy;
            var subsection = canvas.subsection;
            var self = canvas.self;
            var color = canvas.color;
            var dataSite = canvas.dataSite;
            var c = self.find(cId)[0];
            var cxt = c.getContext("2d");
            var x = event.pageX - c.getBoundingClientRect().left;
            var y = event.pageY - c.getBoundingClientRect().top;
            for (var i = 0; i < dataCir.length; i++) {
                cxt.beginPath();
                //渲染参数，x距离,y距离,半径,起始角，结束角，是否顺势针
                cxt.arc(dataCir[i], ciry, 3, 0, 360, false);
                //判断鼠标的点是否在圆圈内
                if (cxt.isPointInPath(x, y)) {
                    //获取鼠标点击区域的颜色值
                    var imgData = cxt.getImageData(x, y, 1, 1);
                    // 重绘画布
                    cxt.clearRect(0, 0, c.width, c.height);
                    dataSite[i].status == 1 ? dataSite[i].status = 0 : dataSite[i].status = 1;

                    var traffic_top = {
                        id: cId,
                        y: ciry - 1,
                        self: self,
                        subsection: subsection,
                        color: color
                    };
                    traffic_distance(traffic_top);
                    var cirTop1 = {
                        id: cId,
                        ciry: ciry,
                        testy: testy,
                        self: self,
                        color: color,
                        dataCir: dataCir,
                        dataSite: dataSite
                    };
                    cir_and_text(cirTop1);
                    cxt.closePath();
                    // 转换16进制像素
                    var hex = "#" + ((1 << 24) + (imgData.data[0] << 16) + (imgData.data[1] << 8) + imgData.data[2]).toString(16).slice(1);
                    if (hex == "#ffffff") {
                        // 清除画布
                        // 绘上实心圆
                        cxt.beginPath();
                        cxt.arc(dataCir[i], ciry, 4, 0, 360, false);
                        cxt.fillStyle = dataSite[i].color;
                        cxt.fill();
                        cxt.closePath();
                    } else {
                        cxt.beginPath();
                        cxt.arc(dataCir[i], ciry, 4, 0, 360, false);
                        cxt.fillStyle = "white";
                        cxt.fill();
                        cxt.closePath();
                    }
                    break
                }
                cxt.closePath();
                cxt.beginPath();
                if(dataSite[i].status == 1){
                 cxt.rect(dataCir[i]-(6*dataSite[i].name.length),testy-16,12*dataSite[i].name.length,16)
                 if (cxt.isPointInPath(x, y)) {
                    cxt.closePath();
                    var options = 
                        {
                            x:e.clientX+5, 
                            y:e.clientY+5, 
                            zIndex:5,
                            line_id: self.attr("tid"),
                            site: dataSite[i]
                        };
                    var dialog = new passenger_flow(this, options);
                    $(".passenger_flow_trend_chart").remove();
                    dialog.appendTo($("body"));
                }
                }

            }
        }
    });
    //选择车辆组件
    //上下行路线组件


    // 线路选择
    var dispatch_line_control = Widget.extend({
        init: function (parent, data) {
            this._super(parent);
            this.model = new Model('lty_dispatch_desktop.lty_dispatch_desktop');
            this.data = data;
        },
        start: function () {
            var data = this.data;
            new dispatch_canvas(this, data).appendTo(this.$el);
            new dispatch_updown_line(this,data).appendTo(this.$el);
        },
        events: {
            'click .chs>li': 'chose_line',
        },
        chose_line: function (event) {
            var x = event.currentTarget;
            var self = this;
            var dis_desk = self.dis_desk;
            var dom = self.$el;
            var ab = $('body').find('.dispatch_desktop .line_line');
            var res = []
            for (var i = 0; i < ab.length; i++) {
                var a = ab[i].innerHTML;
                res.push(a);
            }
            self.model.call('dispatch_desktop', [dis_desk]).then(function (data) {
                var a = -1;
                if (res.indexOf(x.innerHTML) != a) {
                    alert('选择有重复');
                } else {
                    var siteLeft = self.$el.find('.dispatch_desktop')[0].offsetLeft;
                    var chartLeft = self.$el.find('.updown_line_table')[0].offsetLeft;
                    var siteTop = self.$el.find('.dispatch_desktop')[0].offsetTop;
                    var chartTop = self.$el.find('.updown_line_table')[0].offsetTop;
                    data[1].oneline.line_show_or_hide.left = siteLeft;
                    data[1].oneline.line_show_or_hide.top = siteTop;
                    data[1].oneline.chart_show_or_hide.left = chartLeft;
                    data[1].oneline.chart_show_or_hide.top = chartTop;
                    self.$el.html('');
                    //渲染车辆canvas图形组件

                    var a = $('body').find('.dispatch_desktop')
                    new dispatch_canvas(this, data[1]).appendTo(self.$el);
                    new dispatch_updown_line(this, data[1]).appendTo(self.$el);
                    //渲染车辆客流与运力组件
                    qrend_desktop(data[1], '.can_top', '.can_bottom', '.canvas_left', '.canvas_right', dom);
                    self.dataCir = data[1].oneline.site_to_startpoint;
                    self.color = data[1].oneline.plan_feedback;
                    self.dataSite = data[1].oneline.siteTop;
                    self.dataSite2 = data[1].oneline.siteBottom;
                    self.subsection = data[1].oneline.traffic_distance;
                }
            });
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