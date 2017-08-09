odoo.define(function(require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var datepicker = require('web.datepicker');

    // 乘客满意度title
    var satisfaction_title = Widget.extend({
        template: "satisfaction_title_template",
        events: {
            "click .ok_bt": "get_filter_fn"
        },
        init: function(parent, data) {
            this._super(parent);
            this.supply = data;
            $(".o_loading").hide();
        },
        start: function() {
            var self = this;
            // 加载日期组件
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

            // 时间筛选方式
            self.$(".plan_way").on("click", "li", function() {
                $(this).addClass("active").siblings().removeClass('active');
            });
        },
        get_filter_fn: function(e){
            var arg_options = {
                plan_way: this.$(".plan_way li.active").attr("name"),
                line_id: this.$(".supply_line option:selected").val(),
                line_name: this.$(".supply_line option:selected").attr("name"),
                predict_start_time: this.$(".data_scope .start_time").val(),
                predict_end_time: this.$(".data_scope .end_time").val(),
                company: this.$(".company option:selected").val(),
                company_name: this.$(".company option:selected").text()
            };
            var chart_cont_obj = this.$el.parent(".operate_title").next();
            arg_options.chart_obj = chart_cont_obj;
            chart_cont_obj.html("");
            // 暂时都数据加载相同
            var passenger_flow_data = {
                xAxis_data: ['06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22'],
                yAxis_data: ['20', '40', '60', '80', '100'],
                series_data_set: {type: "line", symbolSize: 1},
                data_list: [{
                        name: "乘客满意度",
                        lineStyle: {
                            normal: {
                                color: '#ff0000'
                            }
                        },
                        data: [62, 58, 63, 49, 32, 55, 49, 65, 78, 88, 76, 72, 59, 38, 75, 56, 68]
                    },
                    {
                        name: "候车满意度",
                        lineStyle: {
                            normal: {
                                color: '#0000ff'
                            }
                        },
                        data: [42, 45, 57, 59, 43, 50, 38, 52, 66, 68, 57, 48, 56, 40, 66, 68, 72]
                    }
                ],
            };
            var satisfaction_data = {
                yName: "发车间隔",
                xAxis_data: ['06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22'],
                yAxis_data: ['0', '5', '10', '15', '20'],
                series_data_set: {type: "line", symbolSize: 1},
                data_list: [{
                        name: "发车间隔",
                        step: 'middle',
                        lineStyle: {
                            normal: {
                                color: '#330000'
                            }
                        },
                        data: [5, 6, 8, 9, 10, 5, 6, 7, 8, 25, 6, 8, 9, 10, 5, 6, 7]
                    }
                ]
            };
            var table_data = [];
            for (var i = 0; i < 100; i++) {
                var obj = {
                    "line": arg_options.line_name,
                    "site": arg_options.platform_name,
                    "time": "2017-06-26 06:00",
                    "on_number": "232",
                    "capacity": "250",
                    "out_number": "235",
                    "departure_interval": "5",
                    "waiting": "1.5",
                    "comfort": "1.3",
                    "earnings": "1.2"
                };
                table_data.push(obj);
            }
            new waiting_chart(this, passenger_flow_data, satisfaction_data, table_data).appendTo(arg_options.chart_obj);
        }
    });

    // 候车满意度
    var waiting_satisfaction = Widget.extend({
        template: "supply_template",
        init: function(parent) {
            this._super(parent);
        },
        start: function() {
            $(".o_loading").show();
            var title = "候车满意度分析";
            var plan_way = [
                { name: "按时", en_name: "when" },
                { name: "按天", en_name: "day" },
                { name: "按周", en_name: "weeks" },
                { name: "按月", en_name: "month" },
            ];
            var line_list = [
                { name: "236路", id: "b1" },
                { name: "M231路", id: "b2" },
                { name: "229路", id: "b3" },
                { name: "298路", id: "b4" },
            ];
            var data_scope = [
                "2017-06-26", "2017-07-31"
            ];
            var company_list = [
                { name: "公交一公司", id: "g1" },
                { name: "公交二公司", id: "g2" },
                { name: "公交三公司", id: "g3" },
            ];
            var options = {
                title: title,
                plan_way: plan_way,
                line_list: line_list,
                company_list: company_list,
                data_scope: data_scope
            };
            new satisfaction_title (this, options).appendTo(this.$('.operate_title'));
        }
    });
    core.action_registry.add('lty_operating_supply.waiting_satisfaction', waiting_satisfaction);

    var waiting_chart = Widget.extend({
        template: "waiting_chart_template",
        init: function(parent, data1, data2, data3) {
            this._super(parent);
            this.chart_parameter_data = data1;
            this.chart_satisfaction_data = data2;
            this.table_data = data3;
        },
        start: function() {
            // 客流运力图表
            this.chart_passenger_flow();
            // 峰值图表
            this.chart_peak_canvas();
            // 满意度图表
            this.chart_satisfaction();
            // 数据详情
            this.table_info();
        },
        chart_passenger_flow: function(){
            var set_option = {
                legend: {
                    icon: 'stack',
                    orient: 'vertical',
                    right: '100px',
                    top: '10px'
                },
                grid: {
                    left: 70,
                    bottom: '3%',
                    right: 190,
                    top: '30%',
                    containLabel: true
                },
                yAxis: {
                    offset: 20,
                    axisLabel: {
                        formatter: '{value}',
                    },
                }
            }
            var chart_option = supply_make_chart_options.default_option_set1(this.chart_parameter_data, set_option);
            var mychart = echarts.init(this.$('.chart_passenger_flow')[0]);
            mychart.setOption(chart_option);
        },
        chart_peak_canvas: function(){
            var min = 65,
                max = 78;
            var oe_data = this.chart_parameter_data.data_list[0].data;
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
        chart_satisfaction: function(){
            var set_option = {
                grid: {
                    left: 53,
                    top: '0%',
                    right: 190,
                    containLabel: true
                },
                xAxis: {
                    position: 'top',
                    silent: false,
                    show: true
                },
                yAxis: {
                    inverse: true,
                    axisLabel: {
                        formatter: '{value}分钟',
                    },
                }
            }
            var chart_option = supply_make_chart_options.default_option_set1(this.chart_satisfaction_data, set_option);
            var mychart = echarts.init(this.$('.chart_satisfaction')[0]);
            mychart.setOption(chart_option);
        },
        table_info: function(){
            $(".site_info_table").bootstrapTable({
                data: this.table_data,
                pagination: true,
                pageNumber: 1,
                pageSize: 10,
                pageList: [],
                paginationLoop: false,
                paginationPreText: "上一页",
                paginationNextText: "下一页",
            })
        }
    });
});