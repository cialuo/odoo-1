odoo.define('lty_dispatch_desktop.dispatch_desktop', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    //导入模块用户后台交互
    var Model = require('web.Model');
    var dispatch_desktop = Widget.extend({
        // template: 'dispatch_desktop',
        init: function (parent, context) {
            this._super(parent, context);
            this.model = new Model('lty_dispatch_desktop.lty_dispatch_desktop');
        },
        start: function () {
            var self = this;
            var dis_desk = self.dis_desk;
            self.$el.append(QWeb.render("myConsole"));
            self.$el.append(QWeb.render("updown_line_table"));
            self.model.call('dispatch_desktop', [dis_desk]).then(function (data) {
                self.$el.append(QWeb.render("dispatch_desktop", {dis_desk: data}));
                // 对应id，y高，分段距离，颜色
                var dataCir = data[0].ab.k;
                var color = data[0].ab.g;
                var dataSite = data[0].ab.d;
                var dataSite2 = data[0].ab.d2;
                var subsection = data[0].ab.e;
                var traffic_top = {
                    id: "can",
                    y: 26,
                    subsection: subsection,
                    color: color
                };
                var traffic_bottom = {
                    id: "can1",
                    y: 5,
                    subsection: subsection,
                    color: color
                };
                traffic_distance(traffic_top);
                traffic_distance(traffic_bottom);

                self.subsection = subsection;
                self.dataCir = dataCir;
                self.color = color;
                self.dataSite = dataSite;
                self.dataSite2 = dataSite2;
                var cirTop = {
                    id: "can",
                    ciry: 27,
                    testy: 13,
                    color: color,
                    dataCir: dataCir,
                    dataSite: dataSite
                };
                var cirBottom = {
                    id: "can1",
                    ciry: 6,
                    testy: 25,
                    color: color,
                    dataCir: dataCir,
                    dataSite: dataSite2
                };
                cir_and_text(cirTop);
                cir_and_text(cirBottom);

                can_left(
                    {
                        id: "canvas_left",
                        color:color[0],
                        ciry:27,
                        r:4,
                        lineLen:17,
                        sta:1
                    }
                );
                can_left(
                    {
                        id: "canvas_right",
                        color:color[color.length-1],
                        ciry:27,
                        r:4,
                        lineLen:0,
                        sta:1.5,
                    }
                )
            })
        },
        events: {
            'click #can': 'canvas_info',
            'click #can1': 'canvas_info1',
        },
        do: function (canvas,e) {
            var event =e||window.event;
            var dataCir = canvas.dataCir;
            var cId = canvas.id;
            var ciry = canvas.ciry;
            var self = canvas.self;
            var testy =canvas.testy;

            var subsection = canvas.subsection;
            var color = canvas.color;
            var dataSite = canvas.dataSite;
            var c = document.getElementById(cId);
            var cxt = c.getContext("2d");
            var x = event.pageX - c.getBoundingClientRect().left;
            var y = event.pageY - c.getBoundingClientRect().top;
            for (var i =0; i < dataCir.length; i++) {
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
                        y: ciry-1,
                        subsection: subsection,
                        color: color
                    };
                    traffic_distance(traffic_top);
                    var cirTop1 = {
                        id: cId,
                        ciry: ciry,
                        testy: testy,
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
        },
        canvas_info: function (e) {
            this.do({
                id: 'can',
                ciry: 27,
                testy: 13,
                self: self,
                dataCir: this.dataCir,
                color: this.color,
                dataSite: this.dataSite,
                subsection: this.subsection
            },e)
        },
        canvas_info1: function (e) {
            this.do({
                id: 'can1',
                ciry: 6,
                testy: 25,
                self: self,
                dataCir: this.dataCir,
                color: this.color,
                dataSite: this.dataSite2,
                subsection: this.subsection
            },e)
        }
    })
    core.action_registry.add('dispatch_desktop.page', dispatch_desktop);
})