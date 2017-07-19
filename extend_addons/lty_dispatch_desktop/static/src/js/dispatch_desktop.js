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

            self.model.call('dispatch_desktop', [dis_desk]).then(function (data) {
                self.$el.append(QWeb.render("dispatch_desktop", {dis_desk: data[0]}));
                // 对应id，y高，分段距离，颜色
                var dataCir = data[0].ab.k;
                var color = data[0].ab.g;
                var dataSite = data[0].ab.d;
                var dataSite2 = data[0].ab.d2;
                var subsection = data[0].ab.e;
                var traffic_top = {
                    id: ".can",
                    y: 26,
                    self:self,
                    subsection: subsection,
                    color: color
                };
                var traffic_bottom = {
                    id: ".can1",
                    y: 5,
                    self:self,
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
                    id: ".can",
                    ciry: 27,
                    testy: 13,
                    color: color,
                    self:self,
                    dataCir: dataCir,
                    dataSite: dataSite
                };
                var cirBottom = {
                    id: ".can1",
                    ciry: 6,
                    testy: 25,
                    self:self,
                    color: color,
                    dataCir: dataCir,
                    dataSite: dataSite2
                };
                cir_and_text(cirTop);
                cir_and_text(cirBottom);

                can_left(
                    {
                        id: ".canvas_left",
                        color: color[0],
                        ciry: 27,
                        self:self,
                        r: 4,
                        lineLen: 17,
                        sta: 1
                    }
                );
                can_left(
                    {
                        id: ".canvas_right",
                        color: color[color.length - 1],
                        ciry: 27,
                        self:self,
                        r: 4,
                        lineLen: 0,
                        sta: 1.5,
                    }
                );

                self.$el.append(QWeb.render("updown_line_table"));
                carousel({
                    content:'.carousel_content'
                })
                var absnormalChart = echarts.init(self.$el.find('.absnormal_chart')[0]);
                option = {
                    title: {
                        text: '34路·客流与动力',
                        left: 'center',
                        textStyle: {
                            color: 'white',
                            fontSize: 14
                        },
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'cross',
                            label: {}
                        }
                    },
                    textStyle: {
                        color: '#a3a5ab'
                    },
                    legend: {
                        data: ['实际客流', '预测客流', '计划客流', '调整客流'],
                        orient: 'vertical',
                        right: "10px",
                        top: '10px',
                        textStyle: {
                            color: 'white',
                            fontSize: 12
                        },
                        icon: 'stack'
                    },
                    grid: {
                        left: '3%',
                        right: '105px',
                        bottom: '3%',
                        top: "23%",
                        show: true,
                        borderColor: "#3F4663",
                        containLabel: true,
                    },
                    xAxis: [
                        {
                            type: 'category',
                            name: '时间',
                            boundaryGap: false,
                            data: ['5:00', '8:00', '13:00', '16:00', '19:00', '0:00'],
                            axisLine: {
                                lineStyle: {
                                    color: '#3F4663',//左边线的颜色
                                }
                            },
                            splitLine: {
                                show: true,
                                lineStyle: {
                                    // 使用深浅的间隔色,可用来设置横坐标的颜色
                                    color: ['#3F4663']
                                }
                            }
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value',
                            name: '人力',
                            axisLine: {
                                lineStyle: {
                                    color: '#3F4663',//左边线的颜色
                                }
                            },
                            splitLine: {
                                lineStyle: {
                                    // 使用深浅的间隔色,可用来设置横坐标的颜色
                                    color: ['#3F4663']
                                }
                            }
                        }
                    ],
                    series: [
                        {
                            name: '实际客流',
                            type: 'line',
                            symbol: 'none',
                            data: [120, 152, 101, 134, 90, 230, 210],
                            lineStyle: {//线条颜色
                                normal: {
                                    width: 1,
                                }
                            },
                        },
                        {
                            name: '预测客流',
                            type: 'line',
                            symbol: 'none',
                            data: [220, 182, 191, 234, 290, 330, 310],
                            lineStyle: {//线条颜色
                                normal: {
                                    width: 1,
                                }
                            },
                        },
                        {
                            name: '计划客流',
                            type: 'line',
                            symbol: 'none',
                            data: [150, 232, 201, 154, 190, 330, 410],
                            lineStyle: {//线条颜色
                                normal: {
                                    width: 1,
                                }
                            },
                        },
                        {
                            name: '调整客流',
                            type: 'line',
                            symbol: 'none',
                            data: [320, 332, 301, 334, 390, 330, 320],
                            lineStyle: {//线条颜色
                                normal: {
                                    width: 1,
                                }
                            },
                        }
                    ]
                };
                absnormalChart.setOption(option);
                var lagstation_chart = echarts.init(document.getElementById('lagstation_chart'));
                option1 = {
                    title: {
                        text: '34路·客流与动力',
                        left: 'center',
                        textStyle: {
                            color: '#fff',
                            fontSize: 14
                        },
                    },
                    tooltip: {
                        trigger: 'axis',
                    },
                    textStyle: {
                        color: '#a3a5ab'
                    },
                    legend: {
                        data: ['滞站客流', '预测滞站'],
                        orient: 'vertical',
                        right: "10px",
                        top: '10px',
                        textStyle: {
                            color: '#a3a5ab',
                            fontSize: 12
                        },
                        icon: 'stack'
                    },
                    grid: {
                        left: '13%',
                        right: '105px',
                        bottom: '13%',
                        top: "13%",
                        containLabel: false,
                    },
                    xAxis : [
                        {
                            type : 'category',
                            name: '时间',
                            data : ['周一','周二','周三','周四','周五','周六']
                        }
                    ],
                    yAxis : [
                        {
                            type : 'value',
                            name: '人力',
                        }
                    ],
                    series: [
                        {
                            name: '滞站客流',
                            type: 'bar',
                            data: [120, 152, 101, 134, 90, 230],
                             itemStyle:{
                                    normal:{color:'#4ecfc7'}
                                }
                        },
                        {
                            name: '预测滞站',
                            type: 'bar',
                            data: [220, 182, 191, 234, 290, 330],
                             itemStyle:{
                                    normal:{color:'#5093e1'}
                                }
                        }
                    ]
                };
                lagstation_chart.setOption(option1);
            })
        },
        events: {
            'click .can': 'canvas_info',
            'click .can1': 'canvas_info1',
            'click .new_console':'addLine_click',

        },
		addLine_click:function () {
        	var self = this;
			self.$el.append(QWeb.render("dispatch_desktop",{dis_desk: ''}));
			self.$(".del").click(function() {
                    $(this).parent().parent().hide()
                })
            self.$(".line_edit").click(function() {
                    $(this).siblings('.edit_content').show()
                })
            self.$(".edit_content li li").click(function() {
                var domThis=this;
                var dis_desk = self.dis_desk;
                self.model.call('dispatch_desktop', [dis_desk]).then(function (data) {
                    $(domThis).parents('.edit_content');
                    $(domThis).parents('.dispatch_desktop').html(QWeb.render("dispatch_desktop", {dis_desk: data[1]}))
                })
                })
        },
        do: function (canvas, e) {
            var event = e || window.event;
            var dataCir = canvas.dataCir;
            var cId = canvas.id;
            var ciry = canvas.ciry;
            var self = canvas.self;
            var testy = canvas.testy;
            var subsection = canvas.subsection;
            var color = canvas.color;
            var dataSite = canvas.dataSite;
            var c = self.$el.find(cId)[0];
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
                        self:self,
                        subsection: subsection,
                        color: color
                    };
                    traffic_distance(traffic_top);
                    var cirTop1 = {
                        id: cId,
                        ciry: ciry,
                        testy: testy,
                        self:self,
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
            var self = this;
            this.do({
                id: '.can',
                ciry: 27,
                testy: 13,
                self: self,
                dataCir: this.dataCir,
                color: this.color,
                dataSite: this.dataSite,
                subsection: this.subsection
            }, e)
        },
        canvas_info1: function (e) {
            var self = this;
            this.do({
                id: '.can1',
                ciry: 6,
                testy: 25,
                self: self,
                dataCir: this.dataCir,
                color: this.color,
                dataSite: this.dataSite2,
                subsection: this.subsection
            }, e)
        }
    })
    core.action_registry.add('dispatch_desktop.page', dispatch_desktop);
})