odoo.define('lty_dispatch_desktop.dispatch_desktop', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var dispatch_bus = require('lty_dispaych_desktop.getWidget');
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
                var a = new dispatch_bus(this, data[0], self.$el);
                a.appendTo(self.$el);
                self.$el.append(QWeb.render("updown_line_table"));
                carousel({
                    content: '.carousel_content'
                });
                var absnormalChart = echarts.init(self.$el.find('.absnormal_chart')[0]);
                var absnormalChart1 = echarts.init(self.$el.find('.absnormal_chart')[1]);
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
                absnormalChart1.setOption(option);
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
                    xAxis: [
                        {
                            type: 'category',
                            name: '时间',
                            data: ['周一', '周二', '周三', '周四', '周五', '周六']
                        }
                    ],
                    yAxis: [
                        {
                            type: 'value',
                            name: '人力',
                        }
                    ],
                    series: [
                        {
                            name: '滞站客流',
                            type: 'bar',
                            data: [120, 152, 101, 134, 90, 230],
                            itemStyle: {
                                normal: {color: '#4ecfc7'}
                            }
                        },
                        {
                            name: '预测滞站',
                            type: 'bar',
                            data: [220, 182, 191, 234, 290, 330],
                            itemStyle: {
                                normal: {color: '#5093e1'}
                            }
                        }
                    ]
                };
                lagstation_chart.setOption(option1);
            });
        },
        events: {
            'click .new_console': 'addLine_click',
        },
        addLine_click: function () {
            var self = this;
            var b = new dispatch_bus(this, '', '');
            b.appendTo(self.$el);
        }
    })
    core.action_registry.add('dispatch_desktop.page', dispatch_desktop);
})