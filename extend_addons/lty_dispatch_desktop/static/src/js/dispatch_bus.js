/**
 * Created by Administrator on 2017/7/18.
 */
odoo.define('lty_dispaych_desktop.getWidget', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var Model = require('web.Model');
    var QWeb = core.qweb;
    var dispatch_updown_line=require('lty_dispaych_desktop.updown_line');
    var bus_real_info = require('lty_dispatch_desktop_widget.bus_real_info');
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
            }
        },
        events:{
             'click .can_top':'clk_can_top',
             'click .can_bottom':'clk_can_bottom',
             'click .del':'del_chose_line',
             'click .line_edit':'show_chose_line',
             'click .type_car':'bus_info'
        },
        bus_info:function (e) {
            var self = this;
            var dialog = new bus_real_info(this, {x:e.clientX+5, y:e.clientY+5, zIndex:5});
            dialog.appendTo(self.$el);
        },
        clk_can_top:function (e) {
            var self = this;
            var dom = self.$el;
            self.do({
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
        clk_can_bottom:function (e) {
            var self = this;
            var dom = self.$el;
            self.do({
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
        del_chose_line:function () {
             var self = this;
             self.$('.edit_content').hide();
        },
        show_chose_line:function () {
             var self = this;
             self.$('.edit_content').show();
        },
         do: function (canvas, e) {
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

            }
        }
    });
    //选择车辆组件
    //上下行路线组件


    // 线路选择
    var dispatch_line_control=Widget.extend({
        init: function (parent,data) {
            this._super(parent);
            this.model = new Model('lty_dispatch_desktop.lty_dispatch_desktop');
            this.data = data;
        },
        start: function () {
            var data =this.data;
            new dispatch_canvas(this, data).appendTo(this.$el);
            new dispatch_updown_line(this,data).appendTo(this.$el);
        },
        events: {
            'click .chs>li': 'chose_line',
        },
        chose_line:function () {
            var self = this;
            var dis_desk = self.dis_desk;
            var dom = self.$el;
            self.model.call('dispatch_desktop',[dis_desk]).then(function (data) {
                var siteLeft=self.$el.find('.dispatch_desktop')[0].offsetLeft;
                var chartLeft=self.$el.find('.updown_line_table')[0].offsetLeft;
                var siteTop=self.$el.find('.dispatch_desktop')[0].offsetTop;
                var chartTop=self.$el.find('.updown_line_table')[0].offsetTop;
                data[1].oneline.line_show_or_hide.left = siteLeft;
                data[1].oneline.line_show_or_hide.top = siteTop;
                data[1].oneline.chart_show_or_hide.left = chartLeft;
                data[1].oneline.chart_show_or_hide.top = chartTop;
                self.$el.html('');
                //渲染车辆canvas图形组件
                new dispatch_canvas(this, data[1]).appendTo(self.$el);
                new dispatch_updown_line(this,data[1]).appendTo(self.$el);
                //渲染车辆客流与运力组件
                qrend_desktop(data[1], '.can_top', '.can_bottom', '.canvas_left', '.canvas_right',dom);
                self.dataCir = data[1].oneline.site_to_startpoint;
                self.color = data[1].oneline.plan_feedback;
                self.dataSite = data[1].oneline.siteTop;
                self.dataSite2 = data[1].oneline.siteBottom;
                self.subsection = data[1].oneline.traffic_distance;
            });
        },
    });
    //车辆组件

    //整个车行的组件
    var dispatch_bus=Widget.extend({
         init: function (parent,data) {
            this._super(parent);
            // this.model = new Model('lty_dispatch_desktop.lty_dispatch_desktop');
            this.data = data;
        },
        start: function () {
            var data =this.data;
            new dispatch_line_control(this,data).appendTo(this.$el);
        }
    })
    return dispatch_bus;
});