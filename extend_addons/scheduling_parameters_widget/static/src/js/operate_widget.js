odoo.define("scheduling_parameters_widget.operate", function(require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var datepicker = require('web.datepicker');

    // 线路分时客流
    var line_passenger_flow = Widget.extend({
        template: "line_passenger_flow_template",
        init: function(parent){
            this._super(parent);
        },
        start: function(){
            this.load_fn();
        },
        load_fn: function(){
            $(".o_loading").show();
            // var layer_index = layer.msg("加载中...", {time:0, shade: 0.3});
            var title = "线路分时客流";
            var history_passenger_flow = [
                {name: "前30天", id: "p1"},
                {name: "前60天", id: "p2"},
                {name: "前90天", id: "p3"},
                {name: "前365天", id: "p4"},
                {name: "所有", id: "p5"},
            ];
            var predict_passenger_flow_time = "2017-07-31";
            var plan_way = [
                {name: "按时", type: "when"},
                {name: "按天", type: "day"},
                {name: "按周", type: "weeks"},
                {name: "按月", type: "month"},
            ];
            var line_list = [
                {name: "236路", id: "o1"},
                {name: "M231路", id: "o1"},
                {name: "229路", id: "o1"},
                {name: "298路", id: "o1"},
            ];
            var direction = [
                {name: "上行", id: "i1"},
                {name: "下行", id: "i2"},
            ];
            var data_type = [
                {name: "工作日", id: "u1"},
                {name: "周末", id: "u2"},
                {name: "节假日", id: "u3"},
            ];
            var data_scope = [
                "2017-06-26", "2017-07-31"
            ];
            var options = {
                title: title,
                history_passenger_flow: history_passenger_flow,
                predict_passenger_flow_time: predict_passenger_flow_time,
                plan_way: plan_way,
                line_list: line_list,
                direction: direction,
                data_type: data_type,
                data_scope: data_scope
            };
            new line_passenger_flow_title(this, options).appendTo(this.$('.operate_title'));
        }
    });
    core.action_registry.add('scheduling_parameters_widget.line_passenger_flow', line_passenger_flow);

    // 线路客流title
    var line_passenger_flow_title = Widget.extend({
        template: "line_passenger_flow_title_template",
        events: {
            "click .ok_bt": "queryDataFn"
        },
        init: function(parent, data){
            this._super(parent);
            this.argObj = data;
            $(".o_loading").hide();
        },
        start: function(){
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
            self.$(".plan_way").on("click", "li", function(){
                if ($(this).hasClass('active')){
                    return;
                }
                $(this).addClass("active").siblings().removeClass('active');
                var name = $(this).attr("name");
                if (name == "when"){
                    self.$(".history_passenger_flow").removeClass("dis_none");
                    self.$(".predict_passenger_flow_time").removeClass("dis_none");
                    self.$(".data_scope").addClass("dis_none");
                    self.$(".data_type").removeClass("dis_none");
                    self.$(".direction").removeClass("dis_none");
                }else {
                    self.$(".history_passenger_flow").addClass("dis_none");
                    self.$(".predict_passenger_flow_time").addClass("dis_none");
                    self.$(".data_scope").removeClass("dis_none");
                    self.$(".data_type").addClass("dis_none");
                    if (name=="month"){
                        self.$(".direction").addClass("dis_none");
                    }else{
                        self.$(".direction").removeClass("dis_none");
                    }
                }
            });
        },
        queryDataFn: function(e){
            var plan_way = this.$(".plan_way li.active").attr("name");
            var history_time = this.$(".history_passenger_flow select").val();
            var predict_passenger_flow_time = this.$(".predict_time").val();
            var line = this.$(".line select[name='line']").val();
            var line_name = this.$(".line select[name='line'] option:selected").text();
            var direction = this.$(".line select[name='direction']").val();
            var data_type = this.$(".data_type select").val();
            var predict_start_time = this.$(".predict_passenger_flow .start_time").val();
            var predict_end_time = this.$(".predict_passenger_flow .end_time").val();
            var chart_cont_obj = this.$el.parent(".operate_title").next();
            chart_cont_obj.html("");
            if (plan_way == "when"){
                var parameter_obj_test = {
                    line: line_name,
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
                var satisfaction_obj_test = {
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
                new line_passenger_flow_hour_chart(this, parameter_obj_test, satisfaction_obj_test).appendTo(chart_cont_obj);
            }else{
                var parameter_data_test = {
                    day:{
                        line: line_name,
                        yAxis_data: [3000, 6000, 9000, 12000, 15000],
                        xAxis_data: ["05-01", "05-02", "05-03", "05-04", "05-05", "05-06", "05-07", "05-08", "05-09", "05-10", "05-11", "05-12", "05-13", "05-14"],
                        data: [14000, 12500, 13000, 11800, 11900, 10000, 11700, 9900, 9980, 10500, 10000, 8000, 10000, 7000],
                    },
                    weeks: {
                        line: line_name,
                        yAxis_data: [30000, 60000, 90000, 120000, 150000],
                        xAxis_data: ["2017-17周", "2017-18周", "2017-19周", "2017-20周", "2017-21周", "2017-22周"],
                        data: [105000, 90000, 106000, 90000, 130000, 110000],
                    },
                    month: {
                        line: line_name,
                        yAxis_data: [30000, 60000, 90000, 120000, 150000],
                        xAxis_data: ["2017-01", "2017-02", "2017-03", "2017-04", "2017-05", "2017-06"],
                        data: [110000, 80500, 120000, 80000, 136000, 120000],
                    },
                }
                new passenger_flow_chart(this, parameter_data_test[plan_way]).appendTo(chart_cont_obj);
            }
        }
    })

    // 线路按时客流
    var line_passenger_flow_hour_chart = Widget.extend({
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

    // 按天（周，月）客流
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
                    name: self.chart_data.line,
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

    // 站点分时客流
    var site_passenger_flow = Widget.extend({
        template: "line_passenger_flow_template",
        init: function(parent){
            this._super(parent);
        },
        start: function(){
            this.load_fn();
        },
        load_fn: function(){
            $(".o_loading").show();
            // var layer_index = layer.msg("加载中...", {time:0, shade: 0.3});
            var title = "站点分时客流";
            var plan_way = [
                {name: "按时", type: "when"},
                {name: "按天", type: "day"},
                {name: "按周", type: "weeks"},
                {name: "按月", type: "month"},
            ];
            var line_list = [
                {name: "236路", id: "o1"},
                {name: "M231路", id: "o1"},
                {name: "229路", id: "o1"},
                {name: "298路", id: "o1"},
            ];
            var direction = [
                {name: "上行", id: "i1"},
                {name: "下行", id: "i2"},
            ];
            var data_type = [
                {name: "工作日", id: "u1"},
                {name: "周末", id: "u2"},
                {name: "节假日", id: "u3"},
            ];
            var data_scope = [
                "2017-06-26", "2017-07-31"
            ];
            var platform = [
                {name: "全部", id: "total"},
                {name: "世界之窗", id: "s1"},
                {name: "白石洲", id: "s2"},
                {name: "蛇口", id: "s3"},
                {name: "人民公园", id: "s4"},
                {name: "市政府", id: "s5"},
                {name: "白菜花园", id: "s6"},
                {name: "酷派信息港", id: "s7"}
            ];
            var options = {
                title: title,
                plan_way: plan_way,
                line_list: line_list,
                direction: direction,
                data_type: data_type,
                data_scope: data_scope,
                platform: platform
            };
            new site_passenger_flow_title(this, options).appendTo(this.$('.operate_title'));
        }
    });
    core.action_registry.add('scheduling_parameters_widget.site_passenger_flow', site_passenger_flow);

    // 站点客流title
    var site_passenger_flow_title = Widget.extend({
        template: "site_passenger_flow_title_template",
        events: {
            "click .ok_bt": "queryDataFn"
        },
        init: function(parent, data){
            this._super(parent);
            this.argObj = data;
            $(".o_loading").hide();
        },
        start: function(){
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
            self.$(".plan_way").on("click", "li", function(){
                if ($(this).hasClass('active')){
                    return;
                }
                $(this).addClass("active").siblings().removeClass('active');
                var name = $(this).attr("name");
                if (name == "when"){
                    self.$(".data_type").removeClass("dis_none");
                    self.$(".direction").removeClass("dis_none");
                }else {
                    self.$(".data_type").addClass("dis_none");
                    self.$(".direction").addClass("dis_none");
                }
            });
        },
        queryDataFn: function(e){
            var plan_way = this.$(".plan_way li.active").attr("name");
            var line = this.$(".line select[name='line']").val();
            var line_name = this.$(".line select[name='line'] option:selected").text();
            var direction = this.$(".line select[name='direction']").val();
            var data_type = this.$(".data_type select").val();
            var predict_start_time = this.$(".predict_passenger_flow .start_time").val();
            var predict_end_time = this.$(".predict_passenger_flow .end_time").val();
            var platform = this.$(".platform select").val();
            var platform_name = this.$(".platform select option:selected").attr("name");
            var chart_cont_obj = this.$el.parent(".operate_title").next();
            if (platform!="total"){
                line_name += "/"+platform_name;
            }
            chart_cont_obj.html("");
            if (plan_way == "when"){
                if (platform == "total"){
                    var data = [
                        ['06', '蛇口站', 1, 3],
                        ['07', '滨海站', 50, 50],
                        ['07', '世界之窗', 780, 300],
                        ['08', '下沙', 200, 900],
                        ['09', '白石洲', 700, 100],
                        ['10', '红树林', 500, 250],
                        ['11', '下沙', 300, 700],
                        ['12', '蛇口站', 200, 100],
                        ['13', '蛇口站', 1, 3],
                        ['14', '滨海站', 50, 50],
                        ['15', '世界之窗', 780, 300],
                    ];
                    var new_data = this.get_new_date(data);
                    var scatter_data_test = {
                        yAxis_data: ['蛇口站', '滨海站', '世界之窗', '白石洲', '红树林', '下沙', '购物公园'],
                        xAxis_data: ['06','07','08','09','10','11','12','13','14','15','16'],
                        data: new_data
                    }
                    new site_passenger_flow_chart_scatter(this, scatter_data_test).appendTo(chart_cont_obj);
                }else{
                    var site_hour_data = {
                        
                    };
                    new site_passenger_flow_hour_chart(this, site_hour_data).appendTo(chart_cont_obj);
                }
            }else{
                var parameter_data_test = {
                    day:{
                        line: line_name,
                        yAxis_data: [3000, 6000, 9000, 12000, 15000],
                        xAxis_data: ["05-01", "05-02", "05-03", "05-04", "05-05", "05-06", "05-07", "05-08", "05-09", "05-10", "05-11", "05-12", "05-13", "05-14"],
                        data: [14000, 12500, 13000, 11800, 11900, 10000, 11700, 9900, 9980, 10500, 10000, 8000, 10000, 7000],
                    },
                    weeks: {
                        line: line_name,
                        yAxis_data: [30000, 60000, 90000, 120000, 150000],
                        xAxis_data: ["2017-17周", "2017-18周", "2017-19周", "2017-20周", "2017-21周", "2017-22周"],
                        data: [105000, 90000, 106000, 90000, 130000, 110000],
                    },
                    month: {
                        line: line_name,
                        yAxis_data: [30000, 60000, 90000, 120000, 150000],
                        xAxis_data: ["2017-01", "2017-02", "2017-03", "2017-04", "2017-05", "2017-06"],
                        data: [110000, 80500, 120000, 80000, 136000, 120000],
                    },
                }
                new passenger_flow_chart(this, parameter_data_test[plan_way]).appendTo(chart_cont_obj);
            }
        },
        get_new_date: function(data){
            var new_data = [];
            for (var i=0,l=data.length;i<l;i++){
                var color = '#dbff71';
                var d = data[i];
                var kl = d[2];
                var yl = d[3];
                if (kl-yl>200){
                    color = '#fe613b';
                }else if (kl>yl){
                    color = '#fedc52';
                }
                new_data.push({value:d,itemStyle:{normal:{color:color}}});
            }

            return new_data;
        }
    })

    var site_passenger_flow_chart_scatter = Widget.extend({
        template: "site_chart_scatter_template",
        init: function(parent, data){
            this._super(parent);
            this.parameter_data = data;
        },
        start: function(){
            this.load_fn();
        },
        load_fn: function(){
            debugger;
            var site_list = this.parameter_data.yAxis_data;
            var time_list = this.parameter_data.xAxis_data;
            var new_data = this.parameter_data.data;
            var schema = [
                {name: 'date', index: 0, text: '时间'},
                {name: 'site', index: 1, text: '站'},
                {name: 'kl', index: 2, text: '客流'},
                {name: 'yl', index: 3, text: '运力'}
            ];
            var itemStyle = {
                normal: {
                    opacity: 0.8,
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowOffsetY: 0,
                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
            };

            var scatter_option = {
                grid: {
                    left: '8%',
                    bottom: '8%',
                    right: '8%',
                    top: '8%',
                    containLabel: true
                },
                tooltip: {
                    padding: 10,
                    backgroundColor: '#222',
                    borderColor: '#777',
                    borderWidth: 1,
                    formatter: function (obj) {
                        var value = obj.value;
                        return '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 18px;padding-bottom: 7px;margin-bottom: 7px">'
                            + value[1] + ' ' + value[0] + '点：</div>'
                            + schema[2].text + '：' + value[2] + '<br>'
                            + schema[3].text + '：' + value[3] + '<br>'
                    }
                },
                xAxis: {
                        type: 'category',
                        data: time_list,
                        boundaryGap: false,
                        splitLine: {
                            show: true,
                            lineStyle: {
                                color: '#999',
                                type: 'dashed'
                            }
                        },
                        axisLabel: {
                            formatter: '{value}点',
                            },
                        axisLine: {
                            show: false
                        },
                        axisTick: {
                            show: false
                        },
                    },
                    yAxis: {
                        type: 'category',
                        data: site_list,
                        axisLine: {
                            show: false
                        },
                        axisTick: {
                            show: false
                        },
                        offset: 30
                    },
                visualMap: [
                    {
                        left: 'right',
                        top: '10%',
                        show: false,
                        dimension: 2,
                        min: 0,
                        max: 1000,
                        itemWidth: 30,
                        itemHeight: 120,
                        calculable: true,
                        precision: 0.1,
                        textGap: 30,
                        textStyle: {
                            color: '#000'
                        },
                        inRange: {
                            symbolSize: [10, 70]
                        },
                        outOfRange: {
                            symbolSize: [10, 70],
                        }
                    }
                ],
                series: [
                    {
                        name: '北京',
                        type: 'scatter',
                        itemStyle: itemStyle,
                        data: new_data
                    },
                ]
            };
            var scatter_chart = echarts.init(this.$('.chart_passenger_flow')[0]);
            scatter_chart.setOption(scatter_option);
        }
    })

    var site_passenger_flow_hour_chart = Widget.extend({
        template: "site_passenger_flow_hour_chart_template",
        init: function(parent, data){
            this._super(parent);
        }
    });

    return operate;
});