odoo.define(function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var datepicker = require('web.datepicker');
    // 9.26
    var Model = require('web.Model');
    var model_choseline = new Model('route_manage.route_manage');
    var model_city = new Model('ir.config_parameter');
    var model_site = new Model('opertation_resources_station_platform');
    var res_company = new Model("res.company");
    var config_parameter = new Model('ir.config_parameter');
    // 服务保障能力分析title
    var service_title = Widget.extend({
        template: "supply_title_template",
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
            });//self
            // 时间筛选方式
            self.$(".plan_way").on("click", "li", function () {
                if ($(this).hasClass('active')) {
                    return;
                }
                var name = $(this).attr("name");
                $(this).addClass("active").siblings().removeClass('active');
                if (self.supply.title == "服务保障能力分析") {
                    self.service_switch(name);
                };
            });//self-gy
            self.$(".company").change(function () {// 公司切换事件
                self.company_fn();
            });
            self.$(".supply_line").change(function () {//线路切换事件
                self.supply_line_fn();
            });
            self.$(".ok_bt").click();//加载页面自动触发click
        },//start
        company_fn: function () {
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
                    var item = lines[i];
                    // <option name="测试线路22" value="9">测试线路22</option>
                    options += "<option name='" + item.line_name + "' value='" + item.id + "' >" + item.line_name + "</option>";
                };
                self.$(".supply_line").html(options);
            });
        },//company_fn
        supply_line_fn: function () {
            var self = this;
            var supply_line = self.$(".supply_line");
            if (supply_line.length == 0) {
                return false;
            }
            var line_id = self.$(".supply_line option:selected").val();
            var platform_id = self.$(".platform option:selected").val();
            model_site.query().filter([["route_id", "=", parseInt(line_id)]]).all().then(function (sites) {
                var platform = self.$('.platform');
                platform.find("option").remove();
                var options = "";
                for (var i = 0; i < sites.length; i++) {
                    var item = sites[i];
                    options += "<option value='" + item.id + "' >" + item.station_id[1].split('/')[0] + "</option>";
                };
                platform.html(options);
            });
        },//supply_line_fn
        // 服务天周月切换
        service_switch: function (name) {
            var self = this;
            if (name == "when") {
                self.$(".ok_bt").click();//加载页面自动触发click                
                self.$(".history_passenger_flow").parent().removeClass("dis_none");
                self.$(".predict_passenger_flow_time").parent().removeClass("dis_none");
                self.$(".data_scope").addClass("dis_none");
                self.$(".data_type").parent().removeClass("dis_none");
                self.$(".direction").removeClass("dis_none");
                self.$(".company").parent().removeClass('dis_none');
                self.$(".platform").parent().addClass("dis_none");
                // 线路初始化（根据默认选中公司来筛选线路）
                self.$(".supply_line").find("option").remove();
                // self.$(".supply_line").prepend("<option value='0'>请选择</option>");//追加options默认值 
                model_choseline.query().filter([["state", "=", 'inuse']]).all().then(function (lines) {//线路
                    var options = "";
                    for (var i = 0; i < lines.length; i++) {
                        var item = lines[i];
                        options += "<option name='" + item.line_name + "' value='" + item.id + "' >" + item.line_name + "</option>";
                    };
                    self.$(".supply_line").html(options);
                });
            } else {
                // self.$(".ok_bt").click();//加载页面自动触发click            
                self.$(".history_passenger_flow").parent().removeClass("dis_none");
                self.$(".predict_passenger_flow_time").parent().removeClass("dis_none");
                self.$(".company").parent().removeClass("dis_none");
                self.$(".data_scope").addClass("dis_none");
                self.$(".data_type").parent().removeClass("dis_none");
                self.$(".direction").addClass("dis_none");
                self.$(".company").parent().addClass('dis_none');
                self.$(".platform").parent().removeClass("dis_none");
                // 查表，拿到所有线路
                res_company.query().filter([]).all().then(function (companys) {//单位
                    model_choseline.query().filter([["state", "=", 'inuse']]).all().then(function (lines) {//线路
                        model_site.query().filter([["route_id", "=", parseInt(lines[0].id)]]).all().then(function (sites) {
                            //线路--
                            var options = "";
                            for (var j = 0; j < companys.length; j++) {
                                for (var i = 0; i < lines.length; i++) {
                                    var item = lines[i];
                                    options += "<option name='" + item.line_name + "' value='" + item.id + "' >" + item.line_name + "</option>";
                                }
                            };
                            self.$(".supply_line").html(options);
                            // 站点
                            var platform = self.$('.platform');
                            platform.find("option").remove();
                            var options = "";
                            for (var i = 0; i < sites.length; i++) {
                                var item = sites[i];
                                // options+="<option value="42">人民站台123</option>
                                options += "<option value='" + item.id + "' >" + item.station_id[1].split('/')[0] + "</option>";
                            };
                            platform.html(options);
                        });
                    });  //线路
                });//单位
            }
        },
        // gy-9.26
        get_filter_fn: function () {
            var self = this;
            var arg_options = {
                history_time: this.$(".history_passenger_flow").val(),//9.26
                predict_passenger_flow_time: this.$(".predict_passenger_flow_time").val(),//9.26
                plan_way: this.$(".plan_way li.active").attr("name"),
                step: this.$(".plan_way li.active").attr("value"),
                line_id: this.$(".supply_line option:selected").val(),
                line_name: this.$(".supply_line option:selected").attr("name"),
                direction: this.$(".direction option:selected").val(),
                predict_start_time: this.$(".data_scope .start_time").val(),
                predict_end_time: this.$(".data_scope .end_time").val(),
                company: this.$(".company option:selected").val(),
                company_name: this.$(".company option:selected").text(),
                city_code: this.$(".cityCode").val(),
                platform: this.$(".platform option:selected").val(),
                platform_name: this.$(".platform option:selected").text(),
            };
            var chart_cont_obj = this.$el.parent(".operate_title").next();
            arg_options.chart_obj = chart_cont_obj;
            chart_cont_obj.html("");
            self.layer_index = layer.msg("加载中...", { time: 0, shade: 0.3 });
            // 服务保障能力分析
            $.ajax({
                type: 'get',
                url: 'http://192.168.2.121:8080/ltyop/busReport/ServiceSupportCapability?apikey=123&line_id=' + arg_options.line_id + '&city_code=' + arg_options.city_code + '&date_end=' + arg_options.predict_passenger_flow_time + '&date_period=' + arg_options.history_time + '&company_id=' + arg_options.company + '&direction=' + arg_options.direction + '&step=' + arg_options.step + '',

                // url: RESTFUL_URL + '/ltyop/busReport/ServiceSupportCapability?apikey=123&line_id=' + arg_options.line_id + '&city_code=' + arg_options.city_code + '&date_end=' + arg_options.predict_passenger_flow_time + '&date_period=' + arg_options.history_time + '&company_id='+arg_options.company+'&direction=' + arg_options.direction + '&step=' + arg_options.step + '',
                data: {},
                dataType: 'json',
                error: function (res) {
                    console.log(res.resultMsg);
                },
                success: function (res) {
                    console.log(res.resultMsg);
                    layer.close(self.layer_index);// 结束LODING 
                    if (res.result !== 0) {
                        var layer_index = layer.msg(res.resultMsg, { time: 1200, shade: 0.3 });
                        return false;
                    } else {
                        var x_data = [];            //x+时间轴
                        var y_data_passenger_flow = [];//客流
                        // var history_passenger_flow_y = [];//历史客流
                        var y_data_capacity = [];       //历史运力
                        var y_data_capacity_sugguest = [];//建议客流
                        var bus_model = [];       //--车型
                        var bus_number = [];      //--车数量
                        var driver_number = [];   //--司机数量
                        var crew_number = [];     //--乘务数量
                        $.each(res.response, function (key, val) {
                            if (key == "graph_data") {//up
                                for (var i in val) {
                                    x_data.unshift(val[i].x_data);
                                    y_data_passenger_flow.unshift(val[i].y_data_passenger_flow);
                                    y_data_capacity_sugguest.unshift(val[i].y_data_capacity_sugguest);
                                    y_data_capacity.unshift(val[i].y_data_capacity);
                                };
                            };
                            if (key == "pivot_data") {//down
                                for (var i in val) {
                                    bus_model.unshift(val[i].bus_model);
                                    bus_number.unshift(val[i].bus_number);
                                    driver_number.unshift(val[i].driver_number);
                                    crew_number.unshift(val[i].crew_number);
                                };
                            };
                        });
                        //异常处理
                        if (res.response.graph_data.length == 0 && res.response.pivot_data.length == 0) {
                            var layer_index = layer.msg("暂无数据 ！...", { time: 1200, shade: 0.3 });
                        } else {
                            var fuwu_baozhang = {
                                x_data: x_data,
                                y_data_passenger_flow: y_data_passenger_flow,
                                y_data_capacity_sugguest: y_data_capacity_sugguest,
                                y_data_capacity: y_data_capacity,
                                bus_model: bus_model,
                                bus_number: bus_number,
                                driver_number: driver_number,
                                crew_number: crew_number,
                            };
                            self.line_sever_query(arg_options, fuwu_baozhang);
                        };//else
                    };
                }//success
            });//$.ajax  end
            // new service_chart(this).appendTo(arg_options.chart_obj);
        },
        //服务保障能力分析样式
        line_sever_query: function (arg_options, fuwu_baozhang) {
            if (arg_options.plan_way == "when") {
                var passenger_flow_data = {
                    yName: arg_options.line_name,
                    xAxis_data: fuwu_baozhang.x_data,
                    // xAxis_data: ['06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22'],
                    yAxis_data: ['300', '600', '900', '1200', '1500'],
                    series_data_set: { type: "line" },
                    data_list: [
                        {
                            name: "客流",
                            lineStyle: {
                                normal: {
                                    color: '#ff0000'
                                }
                            },
                            // data: [800, 850, 930, 1200, 1300, 1250, 1000, 700, 900, 990, 1010, 1050, 920, 1000, 1000, 1000, 1000]
                            data: fuwu_baozhang.y_data_passenger_flow
                        },
                        {
                            name: "历史运力",
                            step: 'satrt',
                            lineStyle: {
                                normal: {
                                    type: 'dashed',
                                    color: '#898989'
                                }
                            },
                            // data: [900, 900, 900, 1100, 1100]
                            data: fuwu_baozhang.y_data_capacity
                        },
                        {
                            name: "建议客流",
                            step: 'middle',
                            lineStyle: {
                                normal: {
                                    color: '#00cc66'
                                }
                            },
                            // data: [900, 1000, 1000, 1200, 1200]
                            data: fuwu_baozhang.y_data_capacity_sugguest
                        },
                        // 
                        {
                            name: "前一日",
                            lineStyle: {
                                normal: {
                                    color: '#fe7da9'
                                }
                            },
                            data: [48, 65, 180, 130, 105, 148, 102, 95, 125, 70, 75, 140, 68, 70, 20, 40, 65],
                            data: fuwu_baozhang.y_data_passenger_flow
                        },
                        {
                            name: "上周同期",
                            lineStyle: {
                                normal: {
                                    color: '#fe7da9'
                                }
                            },
                            // data: [70, 82, 206, 140, 128, 125, 100, 95, 125, 118, 100, 130, 158, 98, 75, 40, 25],
                            data: fuwu_baozhang.y_data_passenger_flow
                        },
                        {
                            name: "上月同期",
                            lineStyle: {
                                normal: {
                                    color: '#fe7da9'
                                }
                            },
                            // data: [53, 60, 75, 70, 68, 98, 215, 225, 208, 155, 160, 190, 159, 120, 110, 80, 75],
                            data: fuwu_baozhang.y_data_passenger_flow
                        }
                    ]
                };
                var table_table = [];//时--table
                for (var i = 0; i < fuwu_baozhang.bus_model.length; i++) {
                    var objj = {
                        "motorcycle": fuwu_baozhang.bus_model,
                        "number": fuwu_baozhang.bus_number,
                        "driver_number": fuwu_baozhang.driver_number,
                        "Flight": fuwu_baozhang.crew_number,
                    };//objj
                    table_table.push(objj);
                }
                new service_chart(this, passenger_flow_data, table_table).appendTo(arg_options.chart_obj);
            } else {//天  月 周部分
                var passenger_flow_data = {
                    day: {
                        yName: arg_options.line_name,
                        yAxis_data: [3000, 6000, 9000, 12000, 15000],
                        // xAxis_data: ["05-01", "05-02", "05-03", "05-04", "05-05", "05-06", "05-07", "05-08", "05-09", "05-10", "05-11", "05-12", "05-13", "05-14"],
                        xAxis_data: fuwu_baozhang.x_data,
                        series_data_set: {
                            symbolSize: 1,
                            type: 'line',
                            lineStyle: {
                                normal: {
                                    color: "#3399ff"
                                }
                            },
                        },
                        data_list: [
                            {
                                name: "客流",
                                // data: [14000, 12500, 13000, 11800, 11900, 10000, 11700, 9900, 9980, 10500, 10000, 8000, 10000, 7000]
                                data: fuwu_baozhang.y_data_passenger_flow
                            }
                        ],
                    },
                    weeks: {
                        yName: arg_options.line_name,
                        yAxis_data: [30000, 60000, 90000, 120000, 150000],
                        // xAxis_data: ["2017-17周", "2017-18周", "2017-19周", "2017-20周", "2017-21周", "2017-22周"],
                        xAxis_data: fuwu_baozhang.x_data,
                        series_data_set: {
                            symbolSize: 1,
                            type: 'line',
                            lineStyle: {
                                normal: {
                                    color: "#3399ff"
                                }
                            },
                        },
                        data_list: [
                            {
                                name: "客流",
                                // data: [105000, 90000, 106000, 90000, 130000, 110000]
                                data: fuwu_baozhang.y_data_passenger_flow
                            }
                        ],
                    },
                    month: {
                        yName: arg_options.line_name,
                        yAxis_data: [30000, 60000, 90000, 120000, 150000],
                        // xAxis_data: ["2017-01", "2017-02", "2017-03", "2017-04", "2017-05", "2017-06"],
                        xAxis_data: fuwu_baozhang.x_data,
                        series_data_set: {
                            symbolSize: 1,
                            type: 'line',
                            lineStyle: {
                                normal: {
                                    color: "#3399ff"
                                }
                            },
                        },
                        data_list: [
                            {
                                name: "客流",
                                // data: [110000, 80500, 120000, 80000, 136000, 120000]
                                data: fuwu_baozhang.y_data_passenger_flow
                            }
                        ],
                    },
                };
                new line_passenger_flow_chart(this, passenger_flow_data[arg_options.plan_way]).appendTo(arg_options.chart_obj);
            }
        }
    });//title
    //服务保障能力分析 odoo extend
    var service_flow_base = Widget.extend({
        init: function (parent) {
            this._super(parent);
        },
        start: function () {
            var self = this;
            model_city.query().filter([["key", "=", 'city.code']]).all().then(function (citys) {//城市
                res_company.query().filter([]).all().then(function (companys) {//公司单位
                    model_choseline.query().filter([["state", "=", 'inuse']]).all().then(function (lines) {//线路, ["company_id", "=", companys[0].id]
                        config_parameter.query().filter([["key", "=", "dispatch.desktop.restful"]]).all().then(function (restful) {//url
                            RESTFUL_URL = restful[0].value;              //url-end
                            var options = {
                                cityCode: citys[0].value,
                                lineInfo: lines,
                                // company: companys[0].name,
                                company: companys
                            };
                            new service(self, options).appendTo(self.$el);
                        });
                    });
                });
            })
        }//start
    });
    // 服务保障
    var service = Widget.extend({
        template: "supply_template",
        init: function (parent, args) {
            this._super(parent);
            this.lineDate = args.lineInfo;
            this.cityCode = args.cityCode;
            this.company = args.company;
            // this.siteDate = args.initSiteInfo;
        },
        start: function () {
            $(".o_loading").show();
            var title = "服务保障能力分析";
            // 9.26跟换时间模型
            var history_passenger_flow = [
                { name: "前30天", id: "30" },
                { name: "前60天", id: "60" },
                { name: "前90天", id: "90" },
                { name: "前365天", id: "365" },
                { name: "所有", id: "all" },
            ];
            var predict_passenger_flow_time = "20170731";
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
            // var company_list = [
            //     { name: "集团", id: "g0" },
            //     { name: "一公司", id: "g1" },
            //     { name: "二公司", id: "g2" },
            //     { name: "三公司", id: "g3" },
            // ];
            var company_list = this.company;
            var platform = [];
            var direction = [
                { name: "上行", id: "0" },
                { name: "下行", id: "1" },
            ];
            var dis_set = {
                data_scope: true
            };
            var options = {
                title: title,
                history_passenger_flow: history_passenger_flow,//9.26
                predict_passenger_flow_time: predict_passenger_flow_time,//9.26
                plan_way: plan_way,
                line_list: line_list,
                company_list: company_list,
                direction: direction,
                dis_set: dis_set,
                data_scope: data_scope,
                city_code: this.cityCode,
                platform: platform
            };
            new service_title(this, options).appendTo(this.$('.operate_title'));
        }
    });
    core.action_registry.add('lty_operating_supply.service', service_flow_base);
    //(按时方式) Line-hour
    var service_chart = Widget.extend({
        template: "service_chart_template",
        init: function (parent, data1, data2) {
            this._super(parent);
            this.chart_parameter_data = data1;
            this.table_table = data2;
        },
        start: function () {
            // 客流运力图表
            this.chart_passenger_flow();
            // 峰值图表
            this.chart_peak_canvas();
            // 数据详情
            this.table_info();
        },
        chart_passenger_flow: function () {//9.30上月同期...线路隐藏切换
            this.chart_parameter_data.legend_number = 2;
            var set_option = {
                legend: {
                    icon: 'stack',
                    orient: 'vertical',
                    right: '100px',
                    top: '10px',
                    selected: {
                        '客流统计': true,
                        '运力统计': true,
                        '前一日': false,
                        '上周同期': false,
                        '上月同期': false
                    }
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
                        formatter: '{value}人/次',
                    },
                }
            }
            var chart_option = supply_make_chart_options.default_option_set1(this.chart_parameter_data, set_option);
            var mychart = echarts.init(this.$('.chart_passenger_flow')[0]);
            mychart.setOption(chart_option);
            this.switch_chart(mychart);//9.30上月同期...
        },
        // 9.30上月同期....
        switch_chart: function (mychart) {
            var selected = {
                '客流统计': true,
                '运力统计': true,
                '前一日': false,
                '上周同期': false,
                '上月同期': false
            };
            this.$(".chart_satisfaction_bt").on("click", ".set_bt", function () {
                if ($(this).hasClass('way_1')) {
                    selected = {
                        '客流统计': true,
                        '运力统计': true,
                        '前一日': true,
                        '上周同期': false,
                        '上月同期': false
                    };
                } else if ($(this).hasClass('way_2')) {
                    selected = {
                        '客流统计': true,
                        '运力统计': true,
                        '前一日': false,
                        '上周同期': true,
                        '上月同期': false
                    };
                } else {
                    selected = {
                        '客流统计': true,
                        '运力统计': true,
                        '前一日': false,
                        '上周同期': false,
                        '上月同期': true
                    };
                }
                var option_set = {
                    legend: {
                        selected: selected
                    },
                };

                mychart.setOption(option_set);

            });
        },
        //
        chart_peak_canvas: function () {
            var min = 1200,
                max = 1300;
            if (this.chart_parameter_data.data_list[2].data != 0) {
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
            }//if
        },
        table_info: function () {
            $(".site_info_table").bootstrapTable({
                data: this.table_table,
                pagination: true,
                pageNumber: 1,
                pageSize: 10,
                pageList: [],
                paginationLoop: false,
                paginationPreText: "上一页",
                paginationNextText: "下一页",
            })
        }
    })//widget
    //(其它方式) Line-day/weeks/month
    var line_passenger_flow_chart = Widget.extend({
        template: "passenger_flow_chart_template",
        init: function (parent, data) {
            this._super(parent);
            this.chart_data = data;
        },
        start: function () {
            this.chart_passenger_flow();
        },
        chart_passenger_flow: function () {
            var set_option = {
                grid: {
                    left: '3%',
                    bottom: '3%',
                    right: 190,
                    top: '30%',
                    containLabel: true
                },
                xAxis: {
                    show: true,
                    axisLabel: {
                        formatter: '{value}',
                    },
                },
            };
            var chart_option = supply_make_chart_options.default_option_set1(this.chart_data, set_option);
            var mychart = echarts.init(this.$('.chart_passenger_flow')[0]);
            mychart.setOption(chart_option);
        }
    });
});
