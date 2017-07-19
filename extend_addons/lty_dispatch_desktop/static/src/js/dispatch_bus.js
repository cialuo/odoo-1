/**
 * Created by Administrator on 2017/7/18.
 */
odoo.define('lty_dispaych_desktop.getWidget', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var Model = require('web.Model');
    var QWeb = core.qweb;
    var bus_real_info = require('lty_dispatch_desktop_widget.bus_real_info');
    var dispatch_bus=Widget.extend({
         init: function (parent,data,selfDom) {
            this._super(parent);
            this.model = new Model('lty_dispatch_desktop.lty_dispatch_desktop');
            this.data = data;
            this.selfDom= selfDom;
        },
        start: function () {
            var self = this;
            var data =this.data;
            var selfDom = this.selfDom;
            self.$el.append(QWeb.render("dispatch_desktop", {dis_desk: data}));
            if(data){
                qrend_desktop(data, '.can_top', '.can_bottom', '.canvas_left', '.canvas_right',selfDom);
                self.dataCir = data.ab.k;
                self.color = data.ab.g;
                self.dataSite = data.ab.d;
                self.dataSite2 = data.ab.d2;
                self.subsection = data.ab.e;
            }
        },
        events:{
             'click .can_top':'clk_can_top',
             'click .can_bottom':'clk_can_bottom',
             'click .chs>li':'chose_line',
             'click .del':'del_chose_line',
             'click .line_edit':'show_chose_line',
             'click .type_car':'bus_info'
        },
        bus_info:function (e) {
            var self = this;
            var ab = new bus_real_info(this, {x:e.clientX, y:e.clientY, zIndex:5});
            ab.appendTo(self.$el);
        },
        clk_can_top:function (e) {
            var self = this;
            var dom = self.$('.dispatch_desktop');
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
            var dom = self.$('.dispatch_desktop');
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
        chose_line:function () {
            var self = this;
            var dis_desk = self.dis_desk;
            var dom = self.$el;
            self.model.call('dispatch_desktop',[dis_desk]).then(function (data) {
                console.log(data);
                self.$el.html('')
                self.$el.html(QWeb.render("dispatch_desktop", {dis_desk: data[1]}));
                qrend_desktop(data[1], '.can_top', '.can_bottom', '.canvas_left', '.canvas_right',dom);
                self.dataCir = data[1].ab.k;
                self.color = data[1].ab.g;
                self.dataSite = data[1].ab.d;
                self.dataSite2 = data[1].ab.d2;
                self.subsection = data[1].ab.e;
            });

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
    })
    return dispatch_bus;
});