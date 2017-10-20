odoo.define(function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var datepicker = require('web.datepicker');
    var Model = require('web.Model');
    var model_choseline = new Model('route_manage.route_manage');
    var model_city = new Model('ir.config_parameter');
    var model_site = new Model('opertation_resources_station_platform');
    var res_company = new Model("res.company");
    var config_parameter = new Model('ir.config_parameter');

    // 乘客满意度title
    var satisfaction_title = Widget.extend({
        template: "satisfaction_title_template",
        events: {
            "click .ok_bt": "get_filter_fn"
        },
        init: function (parent, data) {
            this._super(parent);
            this.supply = data;
            $(".o_loading").hide();
        },
        start: function () {
            var self = this;
            // 加载日期组件
            self.$(".supply_datepicker_input").datetimepicker({
                format: 'YYYYMMDD',
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
            // self.$(".plan_way").on("click", "li", function () {
            //     $(this).addClass("active").siblings().removeClass('active');
            // });
            // 9.25---gy
            self.$(".plan_way").on("click", "li", function () {
                if ($(this).hasClass('active')) {
                    return;
                }
                var name = $(this).attr("name");
                $(this).addClass("active").siblings().removeClass('active');
                if (self.supply.title == "候车满意度分析") {
                    self.waiting_satisfaction_switch(name);
                }
            });
            // 
            // 公司单位切换事件              9.22事件为1不能切换！！！
            self.$(".company").change(function () {
                // var self = this;
                var company = self.$(".company");
                if (company.length == 0) {
                    return false;
                }
                var company_id = self.$(".company option:selected").val();
                var line_id = self.$(".supply_line option:selected").val();
                model_choseline.query().filter([["state", "=", 'inuse']]).all().then(function (lines) {//线路
                    self.$(".supply_line").find("option").remove();
                    var options = "";
                    for (var i = 0; i < lines.length; i++) {
                        // <option name="tjw测试线路" value="10">tjw测试线路</option>
                        var item = lines[i];
                        options += "<option name='" + item.line_name + "' value='" + item.id + "' >" + item.line_name + "</option>";
                    };
                    self.$(".supply_line").html(options);
                })
            });        //self.$
            // self.$(".ok_bt").click();//加载页面自动触发click
        },             //start
        // 满意度分析9.25天月周切换
        waiting_satisfaction_switch: function (name) {
            var self = this;
            if (name == "when") {
                self.$(".history_passenger_flow").parent().removeClass("dis_none");
                self.$(".predict_passenger_flow_time").parent().removeClass("dis_none");
                self.$(".data_scope").addClass("dis_none");
                self.$(".data_type").parent().removeClass("dis_none");
                self.$(".direction").removeClass("dis_none");
            } else {
                // self.$(".ok_bt").click();//加载页面自动触发click        
                // 9.25天月周
                self.$(".history_passenger_flow").parent().removeClass("dis_none");
                self.$(".predict_passenger_flow_time").parent().removeClass("dis_none");
                self.$(".data_scope").addClass("dis_none");
                self.$(".data_type").parent().removeClass("dis_none");
                self.$(".direction").removeClass("dis_none");
            }
        },
        // 
        get_filter_fn: function (e) {
            var arg_options = {
                history_time: this.$(".history_passenger_flow").val(),//9.25
                predict_passenger_flow_time: this.$(".predict_passenger_flow_time").val(),//9.25
                plan_way: this.$(".plan_way li.active").attr("name"),
                step: this.$(".plan_way li.active").attr("value"),
                line_id: this.$(".supply_line option:selected").val(),
                line_name: this.$(".supply_line option:selected").attr("name"),
                predict_start_time: this.$(".data_scope .start_time").val(),
                predict_end_time: this.$(".data_scope .end_time").val(),
                company: this.$(".company option:selected").val(),  //公交.单位
                company_name: this.$(".company option:selected").text(),
                city_code: this.$(".cityCode").val()
            };
            self.layer_index = layer.msg("加载中...", { time: 0, shade: 0.3 });
            var chart_cont_obj = this.$el.parent(".operate_title").next();
            arg_options.chart_obj = chart_cont_obj;
            chart_cont_obj.html("");
            // 1.3满意度渲染
            var time_hysteresis = {
                wait_satisfaction_rate: "",
                x_data: "",
                average_start_interval: "",
                up_passenger: "",
                down_passenger: "",
                comfortable_satisfaction_rate: "",
                passenger_satisfaction_rate_y: "",
                enterprise_satisfaction_rate: "",
                capacity: "",
            };
            $.ajax({
                type: 'get',
                // url: 'http://192.168.2.121:8080/ltyop/busReport/getCustomerDegree?apikey=222&line_id=' + arg_options.line_id + '&city_code=' + arg_options.city_code + '&date_end=' + arg_options.predict_passenger_flow_time + '&date_period=' + arg_options.history_time + '&step=' + arg_options.step + '',
                url: RESTFUL_URL + '/ltyop/busReport/getCustomerDegree',
                data: {
                    apikey: 222, line_id: arg_options.line_id, city_code: arg_options.city_code, date_end: arg_options.predict_passenger_flow_time, date_period: arg_options.history_time, step: arg_options.step
                },
                dataType: 'json',
                error: function (res) {
                    console.log(res.resultMsg);
                },
                success: function (res) {
                    console.log(res.resultMsg);
                    layer.close(self.layer_index);
                    if (res.result != 0) {
                        var layer_index = layer.msg(res.resultMsg, { time: 2000, shade: 0.3 });
                        return false;
                    }
                    var x_data = [];                          //x轴坐标时间
                    var y_data = [];                          //y+满意度
                    var y_lose_data = [];                     //y-时间间隔错差
                    var wait_satisfaction_rate = [];          //y+侯车满意度
                    var comfortable_satisfaction_rate = [];    //舒适满意度
                    var enterprise_satisfaction_rate = [];     //公司收益满意度
                    var average_start_interval = [];           //平均发车间隔
                    var up_passenger = [];                     //上车人数
                    var down_passenger = [];                  //下车人数
                    var capacity = [];                         //运力
                    var passenger_satisfaction_rate_y = [];   //乘客满意度             
                    $.each(res.response, function (key, val) {       //table详情
                        if (key == "satisfaction_details") {
                            for (var i in val) {
                                x_data.unshift(val[i].x_data);
                                wait_satisfaction_rate.unshift(val[i].wait_satisfaction_rate * 100);
                                average_start_interval.unshift(val[i].average_start_interval);
                                up_passenger.unshift(val[i].up_passenger);
                                down_passenger.unshift(val[i].down_passenger);
                                comfortable_satisfaction_rate.unshift(val[i].comfortable_satisfaction_rate * 100);
                                capacity.unshift(val[i].capacity * 100);
                                enterprise_satisfaction_rate.unshift(val[i].enterprise_satisfaction_rate * 100);
                                passenger_satisfaction_rate_y.unshift(val[i].passenger_satisfaction_rate * 100)
                            };
                        };
                    });    //$.each
                    // 异常处理
                    if (res.response.satisfaction_details.length == 0 || !res.response.satisfaction_details) {
                        var layer_index = layer.msg("暂无数据 ！...", { time: 2000, shade: 0.3 });
                        return false;
                    } 
                    time_hysteresis = {
                        wait_satisfaction_rate: wait_satisfaction_rate,
                        x_data: x_data,
                        average_start_interval: average_start_interval,
                        up_passenger: up_passenger,
                        down_passenger: down_passenger,
                        comfortable_satisfaction_rate: comfortable_satisfaction_rate,
                        passenger_satisfaction_rate_y: passenger_satisfaction_rate_y,
                        capacity: capacity,
                        enterprise_satisfaction_rate: enterprise_satisfaction_rate
                    };
                    self.run_chart(time_hysteresis);
                }//succes     
            });//$.ajax
        },
        run_chart: function(time_hysteresis){
            var self = this;
            //数据加载相同
            var passenger_flow_data = {
                xAxis_data: time_hysteresis.x_data,     //x轴坐标时间
                yAxis_data: ['20', '40', '60', '80', '100'],
                series_data_set: { type: "line", symbolSize: 1 },
                data_list: [{
                    name: "乘客满意度",
                    lineStyle: {
                        normal: {
                            color: '#ff0000'
                        }
                    },
                    // data: [62, 58, 63, 49, 32]
                    data: time_hysteresis.passenger_satisfaction_rate_y
                },
                {
                    name: "候车满意度",
                    lineStyle: {
                        normal: {
                            color: '#0000ff'
                        }
                    },
                    // data: [42, 45, 57, 59, 43, 50, 38, 52, 66, 68, 57, 48, 56, 40, 66, 68, 72]
                    data: time_hysteresis.wait_satisfaction_rate
                },
                {
                    name: "舒适满意度",
                    lineStyle: {
                        normal: {
                            color: '#ccff99'
                        }
                    },
                    // data: [42, 45, 57, 59, 43, 50, 38, 52, 66, 68, 57, 48, 56, 40, 66, 68, 72]
                    data: time_hysteresis.enterprise_satisfaction_rate
                }
                ],
            };
            var satisfaction_data = {
                yName: "发车间隔",
                xAxis_data: time_hysteresis.x_data,     //x轴坐标时间
                yAxis_data: ['0', '5', '10', '15', '20'],
                series_data_set: { type: "line", symbolSize: 1 },
                data_list: [{
                    name: "发车间隔",
                    step: 'middle',
                    lineStyle: {
                        normal: {
                            color: '#330000'
                        }
                    },
                    // data: [5, 6, 8, 9, 10, 5, 6, 7, 8, 25, 6, 8, 9, 10, 5, 6, 7]
                    data: time_hysteresis.average_start_interval
                }
                ]
            };
            var table_data = [];
            // 满意度详情table
            if (arg_options.plan_way == "when") {
                for (var i = 0; i < time_hysteresis.average_start_interval.length; i++) {
                    var obj = {
                        "line": arg_options.line_name,
                        "site": arg_options.platform_name,
                        "time": time_hysteresis.x_data[i] + ':' + '00' + '--' + time_hysteresis.x_data[i] + ':' + '59',
                        "on_number": time_hysteresis.up_passenger[i],
                        "capacity": time_hysteresis.capacity[i],
                        "out_number": time_hysteresis.down_passenger[i],
                        "departure_interval": time_hysteresis.average_start_interval[i],
                        "waiting": time_hysteresis.wait_satisfaction_rate[i] + '%',
                        "comfort": Math.floor(time_hysteresis.comfortable_satisfaction_rate[i] * 100) / 100 + '%',
                        "earnings": time_hysteresis.enterprise_satisfaction_rate[i] + '%',
                    };
                    table_data.push(obj);
                }//for
            } else {
                for (var i = 0; i < time_hysteresis.average_start_interval.length; i++) {
                    var obj = {
                        "line": arg_options.line_name,
                        "site": arg_options.platform_name,
                        "time": time_hysteresis.x_data[i],
                        "on_number": time_hysteresis.up_passenger[i],
                        "capacity": time_hysteresis.capacity[i],
                        "out_number": time_hysteresis.down_passenger[i],
                        "departure_interval": time_hysteresis.average_start_interval[i],
                        "waiting": time_hysteresis.wait_satisfaction_rate[i] + '%',
                        "comfort": Math.floor(time_hysteresis.comfortable_satisfaction_rate[i] * 100) / 100 + '%',
                        "earnings": time_hysteresis.enterprise_satisfaction_rate[i] + '%',
                    };
                    table_data.push(obj);
                }
            };//else
            // layer.close(layer_index);
            new waiting_chart(this, passenger_flow_data, satisfaction_data, table_data).appendTo(arg_options.chart_obj);
        }
    });

    //总表候车满意度 odoo extend
    var waiting_satisfaction_base = Widget.extend({
        init: function (parent) {
            this._super(parent);
        },
        start: function () {
            var self = this;
            model_city.query().filter([["key", "=", 'city.code']]).all().then(function (citys) {//城市
                // res_company.query().filter([]).all().then(function (companys) {
                    model_choseline.query().filter([["state", "=", 'inuse']]).all().then(function (lines) {//线路
                        config_parameter.query().filter([["key", "=", "dispatch.desktop.restful"]]).all().then(function (restful) {    //url
                            RESTFUL_URL = restful[0].value; //url-end
                            var options = {
                                cityCode: citys[0].value,
                                lineInfo: lines,
                                // company: companys[0].name,
                                company: ""
                            };
                            new waiting_satisfaction(self, options).appendTo(self.$el);
                        });
                    });
                // });
            });
        }

    });
    // 候车满意度
    var waiting_satisfaction = Widget.extend({
        template: "supply_template",
        init: function (parent, args) {
            this._super(parent);
            this.lineDate = args.lineInfo;
            this.cityCode = args.cityCode;
            this.company = args.company;
        },
        start: function () {
            $(".o_loading").show();
            var title = "候车满意度分析";
            // 9.25跟换时间模型
            var history_passenger_flow = [
                { name: "前30天", id: "30" },
                { name: "前60天", id: "60" },
                { name: "前90天", id: "90" },
                { name: "前365天", id: "365" },
                { name: "所有", id: "all" },
            ];
            // 时间戳
            var getdate = function () {
                var now = new Date(),
                    y = now.getFullYear(),
                    m = now.getMonth() + 1,
                    d = now.getDate();
                return y + "" + (m < 10 ? "0" + m : m) + "" + (d < 10 ? "0" + d : d);
            }
            var predict_passenger_flow_time = getdate();
            // 
            var plan_way = [
                { name: "按时", en_name: "when", value: 1 },
                { name: "按天", en_name: "day", value: 2 },
                { name: "按周", en_name: "weeks", value: 3 },
                { name: "按月", en_name: "month", value: 4 },
            ];
            // var line_list = [
            //     { name: "236路", id: "b1" },
            //     { name: "M231路", id: "b2" },
            //     { name: "229路", id: "b3" },
            //     { name: "298路", id: "b4" },
            // ];
            var line_list = this.lineDate;
            var data_scope = [
                "2017-06-26", "2017-07-31"
            ];
            var dis_set = {
                data_scope: true
            }
            // var company_list = [
            //     { name: "公交一公司", id: "g1" },
            //     { name: "公交二公司", id: "g2" },
            //     { name: "公交三公司", id: "g3" },
            // ];
            var company_list = this.company;
            var options = {
                title: title,
                plan_way: plan_way,
                line_list: line_list,
                company_list: company_list,
                data_scope: data_scope,
                dis_set: dis_set,//9.25                
                city_code: this.cityCode,
                history_passenger_flow: history_passenger_flow, //9.25
                predict_passenger_flow_time: predict_passenger_flow_time//9.25
            };
            new satisfaction_title(this, options).appendTo(this.$('.operate_title'));
        }
    });
    // core.action_registry.add('lty_operating_supply.waiting_satisfaction', waiting_satisfaction);
    core.action_registry.add('lty_operating_supply.waiting_satisfaction', waiting_satisfaction_base);//odoo

    var waiting_chart = Widget.extend({
        template: "waiting_chart_template",
        init: function (parent, data1, data2, data3) {
            this._super(parent);
            this.chart_parameter_data = data1;
            this.chart_satisfaction_data = data2;
            this.table_data = data3;
        },
        start: function () {
            // 客流运力图表
            this.chart_passenger_flow();
            // 峰值图表
            this.chart_peak_canvas();
            // 满意度图表
            this.chart_satisfaction();
            // 数据详情
            this.table_info();
        },
        chart_passenger_flow: function () {
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
            if (this.chart_parameter_data && this.chart_parameter_data.data_list[1].data.length != 0) {
                var chart_option = supply_make_chart_options.default_option_set1(this.chart_parameter_data, set_option);
                var mychart = echarts.init(this.$('.chart_passenger_flow')[0]);
                mychart.setOption(chart_option);
            }
        },
        chart_peak_canvas: function () {
            var min = 65,
                max = 78;
            if (this.chart_parameter_data && this.chart_parameter_data.data_list[1].data.length != 0) {//10.13异常判断
                var oe_data = this.chart_parameter_data.data_list[1].data;
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
            };
        },
        chart_satisfaction: function () {
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
                    show: true,
                    axisLabel: {
                        formatter: '{value}'
                    },
                },
                yAxis: {
                    inverse: true,
                    axisLabel: {
                        formatter: '{value}分钟',
                    },
                }
            };
            if (this.chart_satisfaction_data && this.chart_satisfaction_data.data_list[0].data) {
                var chart_option = supply_make_chart_options.default_option_set1(this.chart_satisfaction_data, set_option);
                var mychart = echarts.init(this.$('.chart_satisfaction')[0]);
                mychart.setOption(chart_option);
            } else {
                this.$(".chart_peak").hide();
            };
        },
        table_info: function () {
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