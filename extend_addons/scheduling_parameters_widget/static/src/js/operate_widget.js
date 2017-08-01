odoo.define("scheduling_parameters_widget.operate", function(require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var datepicker = require('web.datepicker');

    // 线路站点分时客流
    var operate = Widget.extend({
        template: "line_site_time_sharing_template",
        init: function(parent) {
            this._super(parent);
            this.parameter_obj = {
                line: '236',
                type: 'hour',
                data_list: [{
                        name: "预测客流",
                        color: "#ff0000",
                        data: [800, 850, 930, 1200, 1300, 1250, 1000, 700, 900, 990, 1010, 1050, 920, 1000, 1000, 1000, 1000]
                    },
                    {
                        name: "历史客流",
                        color: "#898989",
                        data: [700, 750, 830, 1100, 1200, 1150, 900, 600, 800, 890, 910, 950, 820, 900, 900, 900, 900]
                    },
                    {
                        name: "建议运力",
                        color: "#00cc66",
                        data: [900, 1000, 1000, 1200, 1200, 1200, 900, 900, 900, 1100, 1100, 1200, 900, 1300, 1300, 1300, 1300]
                    },
                    {
                        name: "历史运力",
                        color: "#9d3b9d",
                        data: [900, 900, 900, 1100, 1100, 1100, 800, 800, 800, 1000, 1000, 1100, 1000, 1200, 1200, 1200, 1200]
                    }
                ],
                hour_list: ['06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22'],
            };
            this.satisfaction_obj = {
                data_list: [{
                        name: "候车满意度",
                        color: "#be5453",
                        data: [5, 6, 8, 9, 10, 5, 6, 7, 8, 25, 6, 8, 9, 10, 5, 6, 7]
                    },
                    {
                        name: "乘车舒适满意度",
                        color: "#668ea6",
                        data: [5, 6, 8, 9, 10, 5, 6, 7, 8, 25, 6, 8, 9, 10, 5, 6, 7]
                    },
                    {
                        name: "企业满意度",
                        color: "#82b6be",
                        data: [5, 6, 8, 9, 10, 5, 6, 7, 8, 25, 6, 8, 9, 10, 5, 6, 7]
                    },
                    {
                        name: "乘客满意度",
                        color: "#2f4554",
                        data: [5, 6, 8, 9, 10, 5, 6, 7, 8, 25, 6, 8, 9, 10, 5, 6, 7]
                    },
                ]
            };

            this.parameter_data = {
                day:{
                    line: 236,
                    yAxis_data: [3000, 6000, 9000, 12000, 15000],
                    xAxis_data: ["05-01", "05-02", "05-03", "05-04", "05-05", "05-06", "05-07", "05-08", "05-09", "05-10", "05-11", "05-12", "05-13", "05-14"],
                    data: [14000, 12500, 13000, 11800, 11900, 10000, 11700, 9900, 9980, 10500, 10000, 8000, 10000, 7000],
                },
                weeks: {
                    line: 236,
                    yAxis_data: [30000, 60000, 90000, 120000, 150000],
                    xAxis_data: ["2017-17周", "2017-18周", "2017-19周", "2017-20周", "2017-21周", "2017-22周"],
                    data: [105000, 90000, 106000, 90000, 130000, 110000],
                },
                month: {
                    line: 236,
                    yAxis_data: [30000, 60000, 90000, 120000, 150000],
                    xAxis_data: ["2017-01", "2017-02", "2017-03", "2017-04", "2017-05", "2017-06"],
                    data: [110000, 80500, 120000, 80000, 136000, 120000],
                },
            }
        },
        start: function() {
            new line_hour_chart(this, this.parameter_obj, this.satisfaction_obj).appendTo(this.$('.operate_cont'));
            this.load_fn();
        },
        load_fn: function(){
            var self = this;
            self.$(".oe_datepicker_input").datetimepicker({
                format: 'YYYY-MM-DD',
                autoclose: true,
                pickTime: false,
                // startViewMode: 1,
                // minViewMode: 1,
                forceParse: false,
                language: 'zh-CN',
                todayBtn: "linked",
                autoclose: true
            });
            self.$(".screening").on("click", ".swt_box li", function(){
                if ($(this).hasClass("active")){
                    return;
                }
                self.$(".operate_cont").html("");
                var name = $(this).attr("name");
                if (name == "when"){
                    self.$(".part_data_scope").addClass("dis_none");
                    self.$(".part_hour").removeClass("dis_none");
                    self.$(".direction").removeClass("dis_none");
                    new line_hour_chart(self, self.parameter_obj, self.satisfaction_obj).appendTo(self.$('.operate_cont'));
                }else{
                    self.$(".part_hour").addClass("dis_none");
                    self.$(".part_data_scope").removeClass("dis_none");
                    self.$(".direction").removeClass("dis_none");
                    if (name=="month"){
                        self.$(".direction").addClass("dis_none");
                    }
                    new passenger_flow_chart(self, self.parameter_data[name]).appendTo(self.$('.operate_cont'));
                }
                $(this).addClass("active").siblings().removeClass('active');
            });
            self.$(".screening").on("click", ".ok_bt", function(){
                layer.msg("等待查询接口给到", {time: 1000, shade: 0.3});
            });
        }
    });
    core.action_registry.add('scheduling_parameters_widget.operate', operate);

    var line_hour_chart = Widget.extend({
        template: "line_hour_chart_template",
        init: function(parent, data1, data2) {
            this._super(parent);
            this.chart_parameter_data = data1;
            this.chart_satisfaction_data = data2;
        },
        start: function() {
            // 客流运力图表
            this.chart_passenger_flow();
            // 峰值图表
            this.chart_peak_canvas();
            // 满意度图表
            this.chart_satisfaction();
        },
        chart_passenger_flow: function() {
            var line = this.chart_parameter_data.line;
            var data_list = this.chart_parameter_data.data_list;
            var passenger_flow_option = {
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    icon: 'stack',
                    orient: 'vertical',
                    right: '100px',
                    top: '10px',
                    data: [data_list[0].name, data_list[1].name, data_list[2].name, data_list[3].name],
                },
                color: [data_list[0].color, data_list[1].color, data_list[2].color, data_list[3].color],
                grid: {
                    left: '3%',
                    bottom: '3%',
                    right: 190,
                    top: '30%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    show: false,
                    data: ['06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22'],
                    axisLabel: {
                        formatter: '{value}点'
                    },
                    axisLine: {
                        show: false,
                    },
                    axisTick: {
                        show: false
                    },
                },
                yAxis: {
                    type: 'value',
                    name: line + '路',
                    data: ['300', '600', '900', '1200', '1500'],
                    nameGap: 32,
                    nameTextStyle: {
                        fontSize: 16
                    },
                    axisLabel: {
                        formatter: '{value}人/次',
                    },
                    offset: 20,
                    axisLine: {
                        show: false,
                    },
                    axisTick: {
                        show: false
                    },
                    splitLine: {
                        lineStyle: {
                            type: 'dashed'
                        }
                    }
                },
                series: [{
                        name: data_list[0].name,
                        type: 'line',
                        symbolSize: 1,
                        lineStyle: {
                            normal: {
                                color: data_list[0].color,
                            }
                        },
                        data: data_list[0].data
                    },
                    {
                        name: data_list[1].name,
                        type: 'line',
                        symbolSize: 1,
                        lineStyle: {
                            normal: {
                                type: "dashed",
                                color: data_list[1].color,
                            }
                        },
                        data: data_list[1].data
                    },
                    {
                        name: data_list[2].name,
                        type: 'line',
                        step: 'middle',
                        symbolSize: 1,
                        lineStyle: {
                            normal: {
                                color: data_list[2].color,
                            }
                        },
                        data: data_list[2].data
                    },
                    {
                        name: data_list[3].name,
                        type: 'line',
                        step: 'satrt',
                        symbolSize: 1,
                        lineStyle: {
                            normal: {
                                type: "dashed",
                                color: data_list[3].color,
                            }
                        },
                        data: data_list[3].data
                    },
                ]
            };
            var passenger_flow_chart = echarts.init(this.$('.chart_passenger_flow')[0]);
            passenger_flow_chart.setOption(passenger_flow_option);
        },
        chart_peak_canvas: function() {
            var min = 1200,
                max = 1300;
            var oe_data = this.chart_parameter_data.data_list[2].data;
            var canvas = this.$('.chart_peak_canvas')[0];
            var context = canvas.getContext('2d');
            context.lineWidth = 10;
            var tw = canvas.width;
            var w = tw / 16
            var star_x = 0;
            var star_y = 0;
            var end_x = w;
            for (var i = 0, l = 16; i < l; i++) {
                var c = "#99ff00";
                context.beginPath();
                if (oe_data.length > i) {
                    var ov = oe_data[i];
                    if (ov >= max) {
                        c = "#ff0000";
                    } else if (ov >= min) {
                        c = "#fedc52";
                    }
                }
                context.strokeStyle = c;
                context.moveTo(star_x, star_y);
                context.lineTo(end_x, star_y);
                context.lineCap = "butt";
                context.stroke();
                star_x = end_x;
                end_x += w;
            }
        },
        chart_satisfaction: function() {
            var data_list = this.chart_satisfaction_data.data_list;
            var itemStyle = {
                emphasis: {
                    barBorderWidth: 1,
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowOffsetY: 0,
                    shadowColor: 'rgba(0,0,0,0.5)'
                }
            };
            var satisfaction_option = {
                tooltip: {
                    trigger: 'axis'
                },
                legend: {
                    icon: 'stack',
                    orient: 'vertical',
                    right: '10px',
                    top: '10px',
                    data: [data_list[0].name, data_list[1].name, data_list[2].name, data_list[3].name]
                },
                color: [data_list[0].color, data_list[1].color, data_list[2].color, data_list[3].color],
                grid: {
                    left: 46,
                    top: '0%',
                    right: 165,
                    containLabel: true
                },
                xAxis: {
                    data: ['06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22'],
                    axisLabel: {
                        formatter: '{value}点',
                    },
                    axisLine: {
                        show: false,
                    },
                    axisTick: {
                        show: false
                    },
                    position: 'top',
                    silent: false,
                },
                yAxis: {
                    inverse: true,
                    max: 100,
                    name: '满意度',
                    nameGap: 32,
                    nameTextStyle: {
                        fontSize: 16
                    },
                    offset: 20,
                    axisLine: {
                        show: false,
                    },
                    axisTick: {
                        show: false
                    },
                    splitLine: {
                        lineStyle: {
                            type: 'dashed'
                        }
                    }
                },
                series: [{
                        name: data_list[0].name,
                        type: 'bar',
                        stack: 'one',
                        barWidth: '60%',
                        barMinHeight: 15,
                        itemStyle: itemStyle,
                        data: data_list[0].data,
                        lineStyle: {
                            normal: {
                                color: data_list[0].color,
                            }
                        },
                    },
                    {
                        name: data_list[1].name,
                        type: 'bar',
                        stack: 'one',
                        barMinHeight: 15,
                        itemStyle: itemStyle,
                        data: data_list[1].data,
                        lineStyle: {
                            normal: {
                                color: data_list[1].color,
                            }
                        },
                    },
                    {
                        name: data_list[2].name,
                        type: 'bar',
                        stack: 'one',
                        barMinHeight: 15,
                        itemStyle: itemStyle,
                        data: data_list[2].data,
                        lineStyle: {
                            normal: {
                                color: data_list[2].color,
                            }
                        },
                    },
                    {
                        name: data_list[3].name,
                        type: 'bar',
                        stack: 'one',
                        barMinHeight: 15,
                        itemStyle: itemStyle,
                        data: data_list[3].data,
                        lineStyle: {
                            normal: {
                                color: data_list[3].color,
                            }
                        },
                    }
                ]
            };
            var satisfaction_chart = echarts.init(this.$('.chart_satisfaction')[0]);
            satisfaction_chart.setOption(satisfaction_option);
            // 满意度切换按钮
            this.switch_chart(satisfaction_chart);
        },
        switch_chart: function(mychart){
            var option_set_1 = {
                legend: {
                    selected: {
                        '候车满意度': true,
                        '乘车舒适满意度': true,
                        '企业满意度': true,
                        '乘客满意度': false,
                    }
                },
            };
            var option_set_2 = {
                legend: {
                    selected: {
                        '候车满意度': false,
                        '乘车舒适满意度': false,
                        '企业满意度': true,
                        '乘客满意度': true,
                    }
                },
            };
            var option = {};
            this.$el.on("click", ".chart_satisfaction_bt label", function(){
                if ($(this).find("input[type='radio']").hasClass("way_1")){
                    option = option_set_1;
                }else{
                    option = option_set_2;
                }
                mychart.setOption(option);
            });
        }
    });

    var passenger_flow_chart = Widget.extend({
        template: "passenger_flow_chart_template",
        init: function(parent, data) {
            this._super(parent);
            this.chart_data = data;
        },
        start: function(){
            this.chart_passenger_flow();
        },
        chart_passenger_flow: function() {
            var self = this;
            var passenger_flow_option = {
                tooltip: {
                    trigger: 'axis'
                },
                grid: {
                    left: '3%',
                    bottom: '3%',
                    right: 190,
                    top: '30%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    // show: false,
                    data: self.chart_data.xAxis_data,
                    axisLine: {
                        show: false,
                    },
                    axisTick: {
                        show: false
                    },
                },
                yAxis: {
                    type: 'value',
                    name: self.chart_data.line + '路',
                    data: self.chart_data.yAxis_data,
                    nameGap: 32,
                    nameTextStyle: {
                        fontSize: 16
                    },
                    axisLabel: {
                        formatter: '{value}人/次',
                    },
                    offset: 20,
                    axisLine: {
                        show: false,
                    },
                    axisTick: {
                        show: false
                    },
                    splitLine: {
                        lineStyle: {
                            type: 'dashed'
                        }
                    }
                },
                series: [
                    {
                        name: "客流",
                        type: 'line',
                        symbolSize: 1,
                        lineStyle: {
                            normal: {
                                color: "#3399ff"
                            }
                        },
                        data: self.chart_data.data
                    }
                ]
            };
            var passenger_flow_c = echarts.init(this.$('.chart_passenger_flow')[0]);
            passenger_flow_c.setOption(passenger_flow_option);
        },
    });

    return operate;
});