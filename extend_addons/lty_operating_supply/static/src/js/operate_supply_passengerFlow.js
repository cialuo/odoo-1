odoo.define(function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var Model = require('web.Model');
    var datepicker = require('web.datepicker');
    var model_choseline = new Model('route_manage.route_manage');
    var model_city = new Model('ir.config_parameter');
    var model_site = new Model('opertation_resources_station_platform');
    var res_company = new Model("res.company");
    var config_parameter = new Model('ir.config_parameter');
    // 线路客流title
    var supply_title = Widget.extend({
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
            });

            // 时间筛选方式
            self.$(".plan_way").on("click", "li", function () {
                if ($(this).hasClass('active')) {
                    return;
                }
                var name = $(this).attr("name");
                $(this).addClass("active").siblings().removeClass('active');
                if (self.supply.title == "线路分时客流") {
                    self.line_passenger_flow_time_switch(name);
                } else if (self.supply.title == "站点分时客流") {
                    self.site_passenger_flow_time_switch(name);
                } else if (self.supply.title == "分时准点率与滞站客流") {
                    self.time_sharing_rate_switch(name);
                } else if (self.supply.title == "各公司分时客流") {
                    self.companies_are_time_sharing(name);
                }
            });

            //线路-方向-站台切换事件
            self.$(".supply_line").change(function () {     //线路事件
                self.update_site_fn();

            });
            self.$(".direction").change(function () {      //方向事件
                self.update_site_fn();
            });

            // self.$(".ok_bt").click();
        },
        update_site_fn: function () {
            var self = this;
            var platform = self.$('.platform');
            if (platform.length == 0) {
                return false;
            }
            var line_id = self.$(".supply_line option:selected").val();
            var direction = self.$(".direction option:selected").val();
            var direction_v = direction == 0 ? 'up' : 'down'
            model_site.query().filter([["route_id", "=", parseInt(line_id)], ["direction", "=", direction_v]]).all().then(function (sites) {
                console.log(sites);
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
        },
        // 线路分时客流时间切换事件
        line_passenger_flow_time_switch: function (name) {
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
                // 
                // self.$(".history_passenger_flow").parent().addClass("dis_none");
                // self.$(".predict_passenger_flow_time").parent().addClass("dis_none");
                // self.$(".data_scope").removeClass("dis_none");
                // self.$(".data_type").parent().addClass("dis_none");
                if (name == "month") {
                    self.$(".direction").addClass("dis_none");
                } else {
                    self.$(".direction").removeClass("dis_none");
                }
            }
        },
        // 站点分时客流时间切换事件
        site_passenger_flow_time_switch: function (name) {
            // 9.25
            var self = this;
            if (name == "when") {
                self.$(".history_passenger_flow").parent().removeClass("dis_none");
                self.$(".predict_passenger_flow_time").parent().removeClass("dis_none");
                self.$(".data_scope").addClass("dis_none");
                self.$(".data_type").parent().removeClass("dis_none");
                self.$(".direction").removeClass("dis_none");
            } else {
                // self.$(".ok_bt").click();//加载页面自动触发click          
                self.$(".history_passenger_flow").parent().removeClass("dis_none");
                self.$(".predict_passenger_flow_time").parent().removeClass("dis_none");
                self.$(".data_type").parent().addClass("dis_none");
                self.$(".direction").addClass("dis_none");
                self.$(".platform").parent().removeClass("dis_none");
                self.$(".data_scope").addClass("dis_none");
                // if (name == "month") {                  
                //     self.$(".direction").addClass("dis_none");
                // } else {                   
                //     self.$(".direction").removeClass("dis_none");
                // }
            }
        },
        //分时准点率与滞站客流时间切换事件
        time_sharing_rate_switch: function (name) {
            var self = this;
            self.$(".history_passenger_flow").parent().removeClass("dis_none");
            self.$(".predict_passenger_flow_time").parent().removeClass("dis_none");
            self.$(".data_scope").addClass("dis_none");
            self.$(".data_type").parent().removeClass("dis_none");
            self.$(".direction").removeClass("dis_none");
            self.$(".platform").parent().removeClass("dis_none");
        },
        //各公司分时客流
        companies_are_time_sharing: function (name) {
            var self = this;
            // self.$(".ok_bt").click();//加载页面自动触发click     
            self.$(".history_passenger_flow").parent().removeClass("dis_none");
            self.$(".predict_passenger_flow_time").parent().removeClass("dis_none");
            self.$(".company").parent().removeClass("dis_none");
        },
        // 获取筛选条件
        get_filter_fn: function (name) {
            var self = this;
            var arg_options = {
                history_time: this.$(".history_passenger_flow").val(),
                predict_passenger_flow_time: this.$(".predict_passenger_flow_time").val(),
                plan_way: this.$(".plan_way li.active").attr("name"),
                step: this.$(".plan_way li.active").attr("value"),
                line_id: this.$(".supply_line option:selected").val(),
                line_name: this.$(".supply_line option:selected").attr("name"),
                direction: this.$(".direction option:selected").val(),
                data_type: this.$(".data_type option:selected").val(),
                platform: this.$(".platform option:selected").val(),
                platform_name: this.$(".platform option:selected").text(),
                predict_start_time: this.$(".data_scope .start_time").val(),
                predict_end_time: this.$(".data_scope .end_time").val(),
                company: this.$(".company option:selected").val(),
                company_name: this.$(".company option:selected").text(),
                city_code: this.$(".cityCode").val()
            };
            var chart_cont_obj = this.$el.parent(".operate_title").next();
            arg_options.chart_obj = chart_cont_obj;
            chart_cont_obj.html("");
            //Ajax请求体
            self.layer_index = layer.msg("加载中...", { time: 0, shade: 0.3 });
            if (this.supply.title == "线路分时客流") {
                // y+线路分时客流查询接口
                $.ajax({
                    type: 'get',
                    // url: 'http://192.168.2.121:8080/ltyop/busReport/getPassengerFlow?apikey=222&line_id=' + arg_options.line_id + '&city_code=' + arg_options.city_code + '&date_end=' + arg_options.predict_passenger_flow_time + '&date_period=' + arg_options.history_time + '&direction=' + arg_options.direction + '&step=' + arg_options.step + '',

                    url: RESTFUL_URL + '/ltyop/busReport/getPassengerFlow?apikey=222&line_id=' + arg_options.line_id + '&city_code=' + arg_options.city_code + '&date_end=' + arg_options.predict_passenger_flow_time + '&date_period=' + arg_options.history_time + '&direction=' + arg_options.direction + '&step=' + arg_options.step + '',
                    data: {},
                    dataType: 'json',
                    error: function (res) {
                        console.log(res.resultMsg);
                    },
                    success: function (res) {
                        //异常处理
                        if (res.result !== 0) {
                            layer.close(self.layer_index);// 结束LODING
                            var layer_index = layer.msg(res.resultMsg, { time: 2000, shade: 0.3 });
                            return false;
                        } else {
                            var passenger_flow_x = [];           //x+时间轴
                            var pre_passenger_flow_y = [];       //y+预测客流
                            var history_passenger_flow_y = [];   //y+历史客流
                            var history_capacity_y = [];        //y+历史运力
                            var sugguset_capacity = [];         //y+建议运力
                            var y_lose_data = [];              //y-的坐标值
                            $.each(res.response, function (key, val) {
                                if (key == "pre_passenger_flow") {
                                    for (var i in val) {
                                        passenger_flow_x.push(val[i].x_data);
                                        pre_passenger_flow_y.push(val[i].y_data);
                                    };
                                };
                                if (key == "history_passenger_flow") {
                                    for (var i in val) {
                                        // passenger_flow_x.push(val[i].x_data);
                                        history_passenger_flow_y.push(val[i].y_data)
                                    }
                                };
                                if (key == "history_capacity") {
                                    for (var i in val) {
                                        // passenger_flow_x.push(val[i].x_data);
                                        history_capacity_y.push(val[i].y_data)
                                    }
                                };
                                if (key == "sugguset_capacity") {
                                    for (var i in val) {
                                        // passenger_flow_x.push(val[i].x_data);
                                        sugguset_capacity.push(val[i].y_data)
                                    }
                                }
                            });
                            // 客流数据集
                            var line_time_sharing_traffic = {
                                passenger_flow_x: passenger_flow_x,
                                pre_passenger_flow_y: pre_passenger_flow_y,
                                history_passenger_flow_y: history_passenger_flow_y,
                                history_capacity_y: history_capacity_y,
                                sugguset_capacity: sugguset_capacity
                            };
                            if (arg_options.plan_way == "when") {
                                //y-满意度
                                $.ajax({
                                    type: 'get',
                                    // url: 'http://192.168.2.121:8080/ltyop/busReport/getSatisfactionDegree?apikey=123&line_id=' + arg_options.line_id + '&city_code=' + arg_options.city_code + '&date_end=' + arg_options.predict_passenger_flow_time + '&date_period=' + arg_options.history_time + '&direction=' + arg_options.direction + '',

                                    url: RESTFUL_URL + '/ltyop/busReport/getSatisfactionDegree?apikey=123&line_id=' + arg_options.line_id + '&city_code=' + arg_options.city_code + '&date_end=' + arg_options.predict_passenger_flow_time + '&date_period=' + arg_options.history_time + '&direction=' + arg_options.direction + '',
                                    data: {},
                                    dataType: 'json',
                                    error: function (res) {
                                        console.log(res.resultMsg);
                                    },
                                    success: function (res) {
                                        if (res.result != 0) {
                                            layer.close(self.layer_index);// 结束LODING   
                                            self.line_passenger_flow_query(arg_options, line_time_sharing_traffic, "");
                                            return false;
                                        }
                                        layer.close(self.layer_index);// 结束LODING   
                                        var passenger_flow = [];            //x+时间轴
                                        var wait_pleased = [];              //y-候车满意度
                                        var comfortable_pleased = [];        //y-舒适满意度
                                        var enterprise_pleased = [];        //y-企业满意度
                                        var passenger_pleased = [];         //y-乘客满意度
                                        var y_lose_data = [];              //y-的坐标值
                                        $.each(res.response, function (key, val) {
                                            if (key == "wait_pleased") {
                                                for (var i in val) {
                                                    passenger_flow.push(val[i].x_data);
                                                    wait_pleased.push(val[i].y_data * 100);
                                                };
                                            };
                                            if (key == "comfortable_pleased") {
                                                for (var i in val) {
                                                    // passenger_flow_x.push(val[i].x_data);
                                                    comfortable_pleased.push(val[i].y_data * 100)
                                                }
                                            };
                                            if (key == "enterprise_pleased") {
                                                for (var i in val) {
                                                    // passenger_flow_x.push(val[i].x_data);
                                                    enterprise_pleased.push(val[i].y_data * 100)
                                                }
                                            };
                                            if (key == "passenger_pleased") {
                                                for (var i in val) {
                                                    // passenger_flow_x.push(val[i].x_data);
                                                    passenger_pleased.push(val[i].y_data * 100)
                                                }
                                            }
                                        });
                                        //满意度集
                                        var Satisfaction_query = {
                                            passenger_flow: passenger_flow,
                                            wait_pleased: wait_pleased,
                                            comfortable_pleased: comfortable_pleased,
                                            enterprise_pleased: enterprise_pleased,
                                            passenger_pleased: passenger_pleased
                                        };
                                        self.line_passenger_flow_query(arg_options, line_time_sharing_traffic, Satisfaction_query);

                                    }//success
                                });
                            } else {
                                layer.close(self.layer_index);// 结束LODING   
                                self.line_passenger_flow_query(arg_options, line_time_sharing_traffic, "");
                            }
                        }
                    }//success
                });//$.ajax  end
                layer.close(self.layer_index);// 结束LODING 
            } else if (this.supply.title == "站点分时客流") {
                if (arg_options.plan_way == "when") {
                    //小时
                    $.ajax({
                        type: 'get',
                        // url: "http://192.168.2.121:8080/ltyop/busReport/getStationTimeFlow?apikey=123&line_id=34&city_code=130400&date_end=20170926&date_period=90&direction=0",
                        url: RESTFUL_URL + '/ltyop/busReport/getStationTimeFlow?apikey=123&line_id=' + arg_options.line_id + '&city_code=' + arg_options.city_code + '&date_end=' + arg_options.predict_passenger_flow_time + '&date_period=' + arg_options.history_time + '&direction=' + arg_options.direction + '',
                        // data: {},
                        dataType: 'json',
                        error: function (res) {
                            console.log(res.resultMsg);
                        },
                        success: function (res) {
                            console.log(res.resultMsg);
                            layer.close(self.layer_index);// 结束LODING 
                            //异常处理
                            if (res.result !== 0) {
                                var layer_index = layer.msg(res.resultMsg, { time: 2000, shade: 0.3 });
                                return false;
                            } else {
                                var data = [];                   //total --花图
                                var x_data = [];                 //x+小时时间轴
                                var station_name = [];          //y站点名称
                                var passenger_flow = [];        //y客流
                                var capacity = [];              //y运力
                                $.each(res.response.data, function (key, val) {
                                    x_data.push(val.x_data);
                                    station_name.push(val.y_data[key].station_name);
                                    passenger_flow.push(val.y_data[key].passenger_flow);
                                    capacity.push(val.y_data[key].capacity);
                                    //total --花图
                                    for (var i = 0; i < val.y_data.length; i++) {
                                        if (!val.y_data[i].station_name) {
                                            continue;
                                        }
                                        var y_data = [];
                                        y_data.push(val.x_data);
                                        y_data.push(val.y_data[i].station_name);
                                        y_data.push(val.y_data[i].passenger_flow);
                                        var yunli = val.y_data[i].capacity || 0;
                                        y_data.push(yunli);
                                        data.push(y_data);
                                    }
                                });
                                if (res.response.data.length == 0 || res.response.data.length == "undefined") {
                                    var layer_index = layer.msg("暂无数据...", { time: 1200, shade: 0.3 });
                                } else {
                                    var line_hour_query = {
                                        data: data,
                                        x_data: x_data,
                                        station_name: station_name,
                                        passenger_flow: passenger_flow,
                                        capacity: capacity
                                    };
                                    self.site_passenger_flow_query(arg_options, line_hour_query, "");
                                };//else
                            };//异常处理
                        }//success
                    });//$.ajax  end
                } else {//月周
                    $.ajax({
                        type: 'get',
                        url: RESTFUL_URL + '/ltyop/busReport/getStationTimeFlowByDWM?apikey=wew&line_id=' + arg_options.line_id + '&city_code=' + arg_options.city_code + '&date_end=' + arg_options.predict_passenger_flow_time + '&date_period=' + arg_options.history_time + '&station_id=' + arg_options.platform + '&direction=' + arg_options.direction + '&step=' + arg_options.step + '',
                        // url: "http://192.168.2.121:8080/ltyop/busReport/getStationTimeFlowByDWM?apikey=wew&line_id=34&city_code=130400&date_end=20170926&date_period=90&station_id=197&direction=0&step=1",
                        data: {},
                        dataType: 'json',
                        error: function (res) {
                            console.log(res.resultMsg);
                        },
                        success: function (res) {
                            console.log(res.resultMsg);
                            layer.close(self.layer_index);// 结束LODING 
                            //异常处理
                            if (res.result !== 0) {
                                var layer_index = layer.msg(res.resultMsg, { time: 2000, shade: 0.3 });
                                return false;
                            } else {
                                var x_data = [];                 //x+时间轴
                                var y_data_passenger_flow = [];   //客流
                                $.each(res.response.graph_data, function (key, val) {
                                    for (var i in val) {
                                        x_data.unshift(val[i].x_data);
                                        y_data_passenger_flow.unshift(val[i].y_data_passenger_flow)
                                    }
                                });
                                //异常处理
                                if (res.response.graph_data.length == 0) {
                                    var layer_index = layer.msg("暂无数据...", { time: 2000, shade: 0.3 });
                                } else {
                                    var line_day_mouth = {
                                        x_data: x_data,
                                        y_data_passenger_flow: y_data_passenger_flow
                                    };
                                    self.site_passenger_flow_query(arg_options, "", line_day_mouth);
                                };//else
                            };//else
                        }//success
                    });//$.ajax  end
                };//else           
                // this.site_passenger_flow_query(arg_options);
            } else if (this.supply.title == "各公司分时客流与构成") {
                //各公司分时客流与构成 动态渲染
                $.ajax({
                    type: 'get',
                    url: 'http://192.168.2.121:8080/ltyop/busReport/companyPassengerFlow?apikey=123&line_id=' + arg_options.company + '&city_code=' + arg_options.city_code + '&date_end=' + arg_options.predict_passenger_flow_time + '&date_period=' + arg_options.history_time + '&company_id=' + arg_options.company + '&step=' + arg_options.step + '',
                    // url: RESTFUL_URL + '/ltyop/busReport/companyPassengerFlow?apikey=123&company_id=' + arg_options.company + '&city_code=' + arg_options.city_code + '&date_end=' + arg_options.predict_passenger_flow_time + '&date_period=' + arg_options.history_time + '&step=' + arg_options.step + '',
                    data: {},
                    dataType: 'json',
                    error: function (res) {
                        console.log(res.resultMsg)
                    },
                    success: function (res) {
                        layer.close(self.layer_index);// 结束LODING 
                        //异常处理
                        if (res.result !== 0) {
                            var layer_index = layer.msg(res.resultMsg, { time: 2000, shade: 0.3 });
                            return false;
                        } else {
                            var line_x_data = [],        //x坐标
                                // line_y_data = [],        //y坐标
                                data_name_list = [],     //数据对应名称
                                line_data = [],          //折线图数据
                                pie_chart_data = [];     //圆饼图数据

                            if (res.response.company_id == "-1"){
                                if (res.response.companypieData && res.response.companypieData.length>0){
                                    _.each(res.response.companypieData, function(ui){
                                        var pie_dict_o = {
                                            name: ui.son_name,
                                            value: ui.total_passenger_flow
                                        };
                                        pie_chart_data.push(pie_dict_o);
                                        data_name_list.push(ui.son_name);
                                        var companylineData = res.response.companylineData;
                                        var line_data_list = companylineData[ui.son_name];
                                        var data_o_list = [];
                                        _.each(line_data_list, function(ut){
                                            line_x_data.push(ut.x_data);
                                            data_o_list.push(ut.y_data_passenger_flow);
                                        })
                                        var line_data_o = {
                                            name: ui.son_name,
                                            data: data_o_list
                                        };
                                        line_data.push(line_data_o);
                                   })
                                }
                            }else{
                                if (res.response.piePassengerData && res.response.piePassengerData.length0){
                                    _.each(res.response.piePassengerData, function(ui){
                                        var pie_dict_o = {
                                            name: ui.son_name,
                                            value: ui.passenger_flow
                                        };
                                        pie_chart_data.push(pie_dict_o);
                                        data_name_list.push(ui.son_name);
                                        var companylineData = res.response.linePassengerData;
                                        var line_data_list = companylineData[ui.son_name];
                                        var data_o_list = [];
                                        _.each(line_data_list, function(ut){
                                            line_x_data.push(ut.x_data);
                                            data_o_list.push(ut.y_data_passenger_flow);
                                        })
                                        var line_data_o = {
                                            name: ut.son_name,
                                            data: data_o_list
                                        };
                                        line_data.push(line_data_o);
                                    })
                                }
                            }


                            if (line_data.length == 0 && pie_chart_data.length == 0){
                                var layer_index = layer.msg("暂无数据....", { time: 2000, shade: 0.3 });
                                return false;
                            }
                            var company_passenge_echar_data = {
                                x_data: line_x_data,
                                data_list: line_data,
                                pie_chart_data: pie_chart_data,
                                data_name_list: data_name_list
                            };
                            self.company_passenger_flow_query(arg_options, company_passenge_echar_data);
                        }

                    }//success
                })//$.ajax  end
            } else if (this.supply.title == "分时准点率与滞站客流") {
                //分时准点率与滞站客流 动态渲染
                $.ajax({
                    type: 'get',
                    // url: 'http://192.168.2.121:8080/ltyop/busReport/getPointRatePasFlow?apikey=211&line_id=197&city_code=130400&date_end=20170914&date_period=30&direction=1&station_id=&step=1',
                    url: RESTFUL_URL + '/ltyop/busReport/getPointRatePasFlow?apikey=211&line_id=' + arg_options.line_id + '&city_code=' + arg_options.city_code + '&date_end=' + arg_options.predict_passenger_flow_time + '&date_period=' + arg_options.history_time + '&direction=' + arg_options.direction + '&station_id=' + arg_options.platform + '&step=' + arg_options.step + '',
                    data: {},
                    dataType: 'json',
                    error: function (res) {
                        console.log(res.resultMsg)
                    },
                    success: function (res) {
                        console.log(res.resultMsg)
                        layer.close(self.layer_index);// 结束LODING 
                        //异常处理
                        if (res.result !== 0) {
                            var layer_index = layer.msg(res.resultMsg, { time: 2000, shade: 0.3 });
                            return false;
                        } else {
                            var x_data = [];     //坐标轴
                            var y_data = [];     //准点率
                            var y_lose_data = []; // 滞客
                            $.each(res.response, function (key, val) {
                                if (key == "line_ontime_rate") {
                                    for (var i in val) {
                                        x_data.unshift(val[i].x_data);
                                        y_data.unshift(val[i].y_data);
                                    };
                                };
                                if (key == "line_holdup_people") {
                                    for (var i in val) {
                                        y_lose_data.unshift(val[i].y_data);
                                    }
                                }
                            });
                            //异常处理
                            if (res.response.line_ontime_rate.length == 0 && res.response.line_holdup_people.length == 0) {
                                var layer_index = layer.msg("暂无数据 ...", { time: 2000, shade: 0.3 });
                            } else {
                                var echar_data = {
                                    x_data: x_data,
                                    y_data: y_data,
                                    y_lose_data: y_lose_data,
                                };
                                self.time_place_passenger_flow_query(arg_options, echar_data);
                            };
                        }
                    }//success
                })//$.ajax  end
            }
        },
        // 线路分时客流数据查询渲染
        line_passenger_flow_query: function (arg_options, line_time_sharing_traffic, Satisfaction_query) {
            if (arg_options.plan_way == "when") {
                var line_time_sharing_traffic_data = "";
                var Satisfaction_query_data = "";
                // var Satisfaction_query = {
                //     passenger_flow: passenger_flow,
                //     wait_pleased: wait_pleased,
                //     comfortable_pleased: comfortable_pleased,
                //     enterprise_pleased: enterprise_pleased,
                //     passenger_pleased: passenger_pleased
                // };
                // var line_time_sharing_traffic = {
                //     passenger_flow_x: passenger_flow_x,
                //     pre_passenger_flow_y: pre_passenger_flow_y,
                //     history_passenger_flow_y: history_passenger_flow_y,
                //     history_capacity_y: history_capacity_y,
                //     sugguset_capacity: sugguset_capacity
                // };
                if (line_time_sharing_traffic) {
                    if (line_time_sharing_traffic.pre_passenger_flow_y.length !=0 || line_time_sharing_traffic.history_passenger_flow_y.length!=0 || line_time_sharing_traffic.history_capacity_y.length!=0 || line_time_sharing_traffic.sugguset_capacity.length!=0){
                        line_time_sharing_traffic_data = line_time_sharing_traffic;
                    }
                };
                if (Satisfaction_query) {
                    if (Satisfaction_query.wait_pleased.length !=0 || Satisfaction_query.comfortable_pleased.length !=0 || Satisfaction_query.enterprise_pleased.length !=0 || Satisfaction_query.passenger_pleased.length !=0){
                        Satisfaction_query_data = Satisfaction_query
                    }
                };
                if (!line_time_sharing_traffic_data && !Satisfaction_query_data) {
                    var layer_index = layer.msg("暂无数据...", { time: 2000, shade: 0.3 });
                    return false;
                };
                //线图
                // if (line_time_sharing_traffic != "") {
                //     if (line_time_sharing_traffic.pre_passenger_flow_y.length == 0 && line_time_sharing_traffic.history_passenger_flow_y.length == 0 && line_time_sharing_traffic.history_capacity_y.length == 0 && line_time_sharing_traffic.sugguset_capacity.length == 0) {
                //     } else {
                var passenger_flow_data = {
                    yName: arg_options.line_name,
                    xAxis_data: line_time_sharing_traffic_data.passenger_flow_x,
                    // xAxis_data: ['06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22'],
                    yAxis_data: ['300', '600', '900', '1200', '1500'],
                    series_data_set: { type: "line" },
                    data_list: [
                        {
                            name: "预测客流",
                            lineStyle: {
                                normal: {
                                    color: '#ff0000'
                                }
                            },
                            // data: [800, 850, 930, 1200, 1300, 1250, 1000, 700, 900, 990, 1010, 1050, 920, 1000, 1000, 1000, 1000]
                            data: line_time_sharing_traffic_data.pre_passenger_flow_y
                        },
                        {
                            name: "历史客流",
                            lineStyle: {
                                normal: {
                                    type: 'dashed',
                                    color: '#9d3b9d'
                                }
                            },
                            // data: [700, 750, 830, 1100, 1200, 1150, 900, 600, 800, 890, 910, 950, 820, 900, 900, 900, 900]
                            data: line_time_sharing_traffic_data.history_passenger_flow_y
                        },
                        {
                            name: "建议运力",
                            step: 'middle',
                            lineStyle: {
                                normal: {
                                    color: '#00cc66'
                                }
                            },
                            // data: [900, 1000, 1000, 1200, 1200]
                            data: line_time_sharing_traffic_data.sugguset_capacity
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
                            data: line_time_sharing_traffic_data.history_capacity_y
                        }
                    ],
                };
                // };
                // };
                // y-满意度
                var satisfaction_data = {
                    yName: "满意度",
                    // xAxis_data: ['06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22'],
                    xAxis_data: Satisfaction_query_data.passenger_flow,
                    yAxis_data: ['25', '50', '75', '100',],
                    series_data_set: {
                        stack: "one",
                        type: "bar",
                        // barWidth: '60%',
                        barWidth: '29',
                        barMinHeight: 15,
                    },
                    data_list: [{
                        name: "候车满意度",
                        lineStyle: {
                            normal: {
                                color: '#be5453'
                            }
                        },
                        // data: [5, 6, 8, 9, 10]
                        data: Satisfaction_query_data.wait_pleased,
                    },
                    {
                        name: "乘车舒适满意度",
                        lineStyle: {
                            normal: {
                                color: '#668ea6'
                            }
                        },
                        // data: [5, 6, 8, 9, 10]
                        data: Satisfaction_query_data.comfortable_pleased,
                    },
                    {
                        name: "企业满意度",
                        lineStyle: {
                            normal: {
                                color: '#82b6be'
                            }
                        },
                        // data: [5, 6, 8, 9, 10]
                        data: Satisfaction_query_data.enterprise_pleased,
                    },
                    {
                        name: "乘客满意度",
                        lineStyle: {
                            normal: {
                                color: '#2f4554'
                            }
                        },
                        // data: [5, 6, 8, 9, 10]
                        data: Satisfaction_query_data.passenger_pleased,
                    },
                    ]
                }

                new line_passenger_flow_hour_chart(this, passenger_flow_data, satisfaction_data).appendTo(arg_options.chart_obj);
            } else {//天  月 周部分
                if (line_time_sharing_traffic.pre_passenger_flow_y.length == 0 && line_time_sharing_traffic.history_passenger_flow_y.length == 0 && line_time_sharing_traffic.history_capacity_y.length == 0 && line_time_sharing_traffic.sugguset_capacity.length == 0) {
                    var layer_index = layer.msg("暂无数据...", { time: 2000, shade: 0.3 });
                } else {
                    var passenger_flow_data = {
                        day: {
                            yName: arg_options.line_name,
                            yAxis_data: [3000, 6000, 9000, 12000, 15000],
                            // xAxis_data: ["05-01", "05-02", "05-03", "05-04", "05-05", "05-06", "05-07", "05-08", "05-09", "05-10", "05-11", "05-12", "05-13", "05-14"],
                            xAxis_data: line_time_sharing_traffic.passenger_flow_x,
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
                                    data: line_time_sharing_traffic.history_passenger_flow_y
                                }
                            ],
                        },
                        weeks: {
                            yName: arg_options.line_name,
                            yAxis_data: [30000, 60000, 90000, 120000, 150000],
                            // xAxis_data: ["2017-17周", "2017-18周", "2017-19周", "2017-20周", "2017-21周", "2017-22周"],
                            xAxis_data: line_time_sharing_traffic.passenger_flow_x,
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
                                    data: line_time_sharing_traffic.history_passenger_flow_y
                                }
                            ],
                        },
                        month: {
                            yName: arg_options.line_name,
                            yAxis_data: [30000, 60000, 90000, 120000, 150000],
                            // xAxis_data: ["2017-01", "2017-02", "2017-03", "2017-04", "2017-05", "2017-06"],
                            xAxis_data: line_time_sharing_traffic.passenger_flow_x,
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
                                    data: line_time_sharing_traffic.history_passenger_flow_y
                                }
                            ],
                        },
                    };
                    new line_passenger_flow_chart(this, passenger_flow_data[arg_options.plan_way]).appendTo(arg_options.chart_obj);
                };//else
            }
        },
        // 站点分时客流数据查询渲染
        site_passenger_flow_query: function (arg_options, line_hour_query, line_day_mouth) {
            if (arg_options.plan_way == "when") {
                if (arg_options.platform == "total") {//花图
                    // var data = [
                    //     ['06', '蛇口站', 1, 3],
                    //     ['07', '滨海站', 50, 50],
                    //     ['07', '世界之窗', 780, 300],
                    //     ['08', '下沙', 200, 900],
                    //     ['09', '白石洲', 700, 100],
                    //     ['10', '红树林', 500, 250],
                    //     ['11', '下沙', 300, 700],
                    //     ['12', '蛇口站', 200, 100],
                    //     ['13', '蛇口站', 1, 3],
                    //     ['14', '滨海站', 50, 50],
                    //     ['15', '世界之窗', 780, 300],
                    // ];
                    var data = line_hour_query.data;
                    var itemStyle = {
                        normal: {
                            opacity: 0.8,
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowOffsetY: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    };
                    var chart_parameter_data = {
                        // xAxis_data: ['06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16'],
                        xAxis_data: line_hour_query.x_data,
                        // yAxis_data: ['蛇口站', '滨海站', '世界之窗', '白石洲', '红树林', '下沙', '购物公园'],
                        yAxis_data: line_hour_query.station_name,
                        data_list: [
                            {
                                name: "",
                                type: "scatter",
                                itemStyle: itemStyle,
                                data: this.get_scatter_date(data)
                            }
                        ]
                    };
                    new site_passenger_flow_chart_scatter(this, chart_parameter_data).appendTo(arg_options.chart_obj);
                };
                // else {//时  原型不做
                // var chart_parameter_data = {
                //     yName: arg_options.line_name + '/' + arg_options.platform_name,
                //     yAxis_data: ['50', '100', '150', '200', '250'],
                //     // xAxis_data: ['06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22'],
                //     xAxis_data: line_hour_query.x_data,
                //     series_data_set: {
                //         type: 'line',
                //         symbolSize: 1,
                //     },
                //     data_list: [
                //         {
                //             name: "客流统计",
                //             lineStyle: {
                //                 normal: {
                //                     color: '#6189fe'
                //                 }
                //             },
                //             // data: [50, 55, 140, 230, 115, 100, 60, 135, 148, 140, 120, 105, 240, 105, 85, 78, 65],
                //             data: line_hour_query.passenger_flow
                //         },
                //         {
                //             name: "运力统计",
                //             step: 'middle',
                //             lineStyle: {
                //                 normal: {
                //                     color: '#00cc66'
                //                 }
                //             },
                //             // data: [155, 155, 220, 220, 155, 155, 155, 155, 155, 155, 155, 155, 215, 215, 155, 155, 155],
                //             data: line_hour_query.capacity
                //         },
                //         {
                //             name: "前一日",
                //             lineStyle: {
                //                 normal: {
                //                     color: '#fe7da9'
                //                 }
                //             },
                //             data: [48, 65, 180, 130, 105, 148, 102, 95, 125, 70, 75, 140, 68, 70, 20, 40, 65],
                //         },
                //         {
                //             name: "上周同期",
                //             lineStyle: {
                //                 normal: {
                //                     color: '#fe7da9'
                //                 }
                //             },
                //             data: [70, 82, 206, 140, 128, 125, 100, 95, 125, 118, 100, 130, 158, 98, 75, 40, 25],
                //         },
                //         {
                //             name: "上月同期",
                //             lineStyle: {
                //                 normal: {
                //                     color: '#fe7da9'
                //                 }
                //             },
                //             data: [53, 60, 75, 70, 68, 98, 215, 225, 208, 155, 160, 190, 159, 120, 110, 80, 75],
                //         }
                //     ]
                // };
                //原型不做site_table_data
                // var site_table_data = [];
                // for (var i = 0; i < 100; i++) {
                //     var obj = {
                //         "line": arg_options.line_name,
                //         "site": arg_options.platform_name,
                //         "time": "2017-06-26 06:00",
                //         "on_number": "232",
                //         "capacity": "250",
                //         "out_number": "235"
                //     };
                //     site_table_data.push(obj);
                // }
                // new site_passenger_flow_hour_chart(this, chart_parameter_data, site_table_data).appendTo(arg_options.chart_obj);
            } else {//月周..
                var chart_parameter_data = {
                    day: {
                        yName: arg_options.line_name + '/' + arg_options.platform_name,
                        yAxis_data: [3000, 6000, 9000, 12000, 15000],
                        // xAxis_data: ["05-01", "05-02", "05-03", "05-04", "05-05", "05-06", "05-07", "05-08", "05-09", "05-10", "05-11", "05-12", "05-13", "05-14"],
                        xAxis_data: line_day_mouth.x_data,
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
                                data: line_day_mouth.y_data_passenger_flow
                            }
                        ],
                    },
                    weeks: {
                        yName: arg_options.line_name,
                        yAxis_data: [30000, 60000, 90000, 120000, 150000],
                        // xAxis_data: ["2017-17周", "2017-18周", "2017-19周", "2017-20周", "2017-21周", "2017-22周"],
                        xAxis_data: line_day_mouth.x_data,
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
                                data: line_day_mouth.y_data_passenger_flow
                            }
                        ],
                    },
                    month: {
                        yName: arg_options.line_name,
                        yAxis_data: [30000, 60000, 90000, 120000, 150000],
                        // xAxis_data: ["2017-01", "2017-02", "2017-03", "2017-04", "2017-05", "2017-06"],
                        xAxis_data: line_day_mouth.x_data,
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
                                data: line_day_mouth.y_data_passenger_flow
                            }
                        ],
                    },
                };
                new line_passenger_flow_chart(this, chart_parameter_data[arg_options.plan_way]).appendTo(arg_options.chart_obj);
            }
        },
        // 各公司分时客流与构成渲染
        company_passenger_flow_query: function (arg_options, company_passenge_echar_data) {
            // var xAxis_data_dict = {
            //     // when: ['06点', '08点', '10点', '12点', '14点', '16点', '18点', '22点', '24点'],
            //     when: company_passenge_echar_data.x_data,
            //     // day: ['5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9'],
            //     day: company_passenge_echar_data.x_data,
            //     // weeks: ['2017-17周', '2017-18周', '2017-19周', '2017-20周', '2017-21周', '2017-22周', '2017-23周', '2017-24周', '2017-25周'],
            //     weeks: company_passenge_echar_data.x_data,
            //     // month: ['2017-01', '2017-02', '2017-03', '2017-04', '2017-05', '2017-06', '2017-07', '2017-08', '2017-09']
            //     month: company_passenge_echar_data.x_data,
            // };
            // var company_child_dict = {
            //     "总公司": ["一分公司", "二分公司", "三分公司"],
            //     "一分公司": ["48路", "78路", "18路"],
            //     "二分公司": ["58路", "100路", "123路"],
            //     "三分公司": ["68路", "168路", "25路"]
            // };
            // var company_child_dict = {
            //     "总公司": company_passenge_echar_data.son_name,
            //     // "一分公司": ["48路", "78路", "18路"],
            //     // "二分公司": ["58路", "100路", "123路"],
            //     // "三分公司": ["68路", "168路", "25路"]
            // };
            // var chart_parameter_data = {
            //     company_name: arg_options.company_name,
            //     // xAxis_data: xAxis_data_dict[arg_options.plan_way],
            //     xAxis_data: company_passenge_echar_data.x_data,
            //     yAxis_data: ['0', '3000', '6000', '9000', '12000', '15000'],
            //     series_data_set: { type: 'line', symbolSize: 1, },
            //     // data_list: [{
            //     //     name: company_child_dict[arg_options.company_name][0],
            //     //     // data: [8000, 8500, 9300, 12000, 13000, 12500, 10000, 7000, 9000]
            //     //     data: company_passenge_echar_data.passenger_flow
            //     // },
            //     // {
            //     //     name: company_child_dict[arg_options.company_name][1],
            //     //     // data: [7000, 7500, 8300, 11000, 12000, 11500, 9000, 6000, 8000]
            //     //     data: company_passenge_echar_data.passenger_flow
            //     // },
            //     // {
            //     //     name: company_child_dict[arg_options.company_name][2],
            //     //     // data: [9000, 10000, 10000, 12000, 12000, 12000, 9000, 5000, 6000]
            //     //     data: company_passenge_echar_data.passenger_flow
            //     // },
            //     // ]
            //     data_list: company_passenge_echar_data.data_list
            // };

            var chart_parameter_data_new = {
                company_name: arg_options.company_name,
                xAxis_data: company_passenge_echar_data.x_data,
                yAxis_data: ['0', '3000', '6000', '9000', '12000', '15000'],
                series_data_set: { type: 'line', symbolSize: 1, },
                data_list: company_passenge_echar_data.data_list,
                pie_chart_data: company_passenge_echar_data.pie_chart_data,
                data_name_list: company_passenge_echar_data.data_name_list
            };
            new company_passenger_flow_chart(this, chart_parameter_data_new).appendTo(arg_options.chart_obj);
        },
        //分时准点率与滞站客流渲染
        time_place_passenger_flow_query: function (arg_options, echar_data) {
            var xAxis_data_dict = {//x时间轴
                when: echar_data.x_data,
                day: echar_data.x_data,
                weeks: echar_data.x_data,
                month: echar_data.x_data,
                // when: ['06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22'],
                // day: ['5.1', '5.2', '5.3', '5.4', '5.5', '5.6', '5.7', '5.8', '5.9'],
                // weeks: ['2017-17周', '2017-18周', '2017-19周', '2017-20周', '2017-21周', '2017-22周', '2017-23周', '2017-24周', '2017-25周'],
                // month: ['2017-01', '2017-02', '2017-03', '2017-04', '2017-05', '2017-06', '2017-07', '2017-08', '2017-09']
            };
            var series_data_dict_1 = {//y--准点率
                when: echar_data.y_data,
                day: echar_data.y_data,
                weeks: echar_data.y_data,
                month: echar_data.y_data,
                // when: [61, 63, 72, 88, 72, 62, 65, 60, 55, 49, 76, 88, 56, 68, 65, 61, 67],
                // day: [88, 72, 62, 65, 60, 55, 49, 76, 88],
                // weeks: [63, 72, 88, 72, 62, 65, 60, 55, 49],
                // month: [49, 76, 88, 56, 68, 65, 61, 67, 78]
            };
            var series_data_dict_2 = {//滞留客
                // when: [31, 23, 12, 28, 42, 52, 35, 20, 45, 39, 36, 38, 26, 28, 25, 31, 37],
                when: echar_data.y_lose_data,
                day: echar_data.y_lose_data,
                weeks: echar_data.y_lose_data,
                month: echar_data.y_lose_data,
                // day: [28, 32, 22, 15, 30, 45, 49, 26, 18],
                // weeks: [23, 32, 18, 32, 42, 25, 30, 45, 49],
                // month: [49, 26, 38, 56, 18, 25, 31, 47, 28]
            };
            var yName = arg_options.platform != "total" ? arg_options.platform_name : "线路"
            var passenger_flow_data = {
                yName: yName + '平均准点率',
                xAxis_data: xAxis_data_dict[arg_options.plan_way],
                yAxis_data: ['50', '60', '70', '80', '100'],
                series_data_set: { type: "line", symbolSize: 1 },
                data_list: [
                    {
                        name: "平均准点率",
                        lineStyle: {
                            normal: {
                                color: '#fe2a2a'
                            }
                        },
                        data: series_data_dict_1[arg_options.plan_way]
                    }
                ],
            };
            var satisfaction_data = {
                yName: yName + '平均滞站客流',
                xAxis_data: xAxis_data_dict[arg_options.plan_way],
                yAxis_data: ['10', '20', '30', '40'],
                series_data_set: {
                    stack: "one",
                    type: "bar",
                    barWidth: '29',
                    barMinHeight: 15,
                },
                data_list: [
                    {
                        name: "平均滞站客流",
                        data: series_data_dict_2[arg_options.plan_way]
                    }
                ]
            }

            new time_place_passenger_flow_chart(this, passenger_flow_data, satisfaction_data).appendTo(arg_options.chart_obj);
        },
        // 站点分时客流数据查询渲染
        get_scatter_date: function (data) {
            var new_data = [];
            for (var i = 0, l = data.length; i < l; i++) {
                var color = '#dbff71';
                var d = data[i];
                var kl = d[2];
                var yl = d[3];
                if (kl - yl > 200) {
                    color = '#fe613b';
                } else if (kl > yl) {
                    color = '#fedc52';
                }
                new_data.push({ value: d, itemStyle: { normal: { color: color } } });
            }

            return new_data;
        }
    })
    //线路分时客流 Line odoo extend
    var line_passenger_flow_base = Widget.extend({
        init: function (parent) {
            this._super(parent);
        },
        start: function () {
            var self = this;
            model_city.query().filter([["key", "=", 'city.code']]).all().then(function (citys) {
                model_choseline.query().filter([["state", "=", 'inuse']]).all().then(function (lines) {
                    config_parameter.query().filter([["key", "=", "dispatch.desktop.restful"]]).all().then(function (restful) {
                        RESTFUL_URL = restful[0].value;
                        var options = {
                            cityCode: citys[0].value,
                            lineInfo: lines,
                        };
                        new line_passenger_flow(self, options).appendTo(self.$el);
                    });
                });
            });
        }
    });

    // 线路分时客流 Line
    var line_passenger_flow = Widget.extend({
        template: "supply_template",
        init: function (parent, args) {
            this._super(parent);
            this.lineDate = args.lineInfo;
            this.cityCode = args.cityCode;
        },
        start: function () {
            $(".o_loading").show();
            // var layer_index = layer.msg("加载中...", { time: 0, shade: 0.3 });
            var title = "线路分时客流";
            var history_passenger_flow = [
                { name: "前30天", id: "30" },
                { name: "前60天", id: "60" },
                { name: "前90天", id: "90" },
                { name: "前365天", id: "365" },
                { name: "所有", id: "all" },
            ];
            var predict_passenger_flow_time = "20170731";
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
            var direction = [
                { name: "上行", id: "0" },
                { name: "下行", id: "1" },
            ];
            var data_type = [
                { name: "工作日", id: "d1" },
                { name: "周末", id: "d2" },
                { name: "节假日", id: "d3" },
            ];
            var data_scope = [
                "2017-06-26", "2017-07-31"
            ];
            var dis_set = {
                data_scope: true
            }
            var options = {
                title: title,
                history_passenger_flow: history_passenger_flow,
                predict_passenger_flow_time: predict_passenger_flow_time,
                plan_way: plan_way,
                line_list: line_list,
                direction: direction,
                data_type: data_type,
                data_scope: data_scope,
                dis_set: dis_set,
                city_code: this.cityCode
            };
            // layer.close(layer_index);//9.25 加载LODING            
            new supply_title(this, options).appendTo(this.$('.operate_title'));
        }
    });
    core.action_registry.add('lty_operating_supply.line_passenger_flow', line_passenger_flow_base);

    // 线路分时客流图表(按时方式) Line-hour
    var line_passenger_flow_hour_chart = Widget.extend({
        template: "line_passenger_flow_hour_chart_template",
        init: function (parent, data1, data2) {
            this._super(parent);
            this.chart_parameter_data = data1;
            this.chart_satisfaction_data = data2;
        },
        start: function () {
            // 客流运力图表
            this.chart_passenger_flow();
            // 峰值图表
            this.chart_peak_canvas();
            // 满意度图表
            this.chart_satisfaction();
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
                    left: '3%',
                    bottom: '3%',
                    right: 190,
                    top: '30%',
                    containLabel: true
                },
            }
            if (this.chart_parameter_data && this.chart_parameter_data.data_list[1].data.length != 0) {//10.12判断
                var chart_option = supply_make_chart_options.default_option_set1(this.chart_parameter_data, set_option);
                var mychart = echarts.init(this.$('.chart_passenger_flow')[0]);
                mychart.setOption(chart_option);
            }
        },
        chart_peak_canvas: function () {
            var min = 1200,
                max = 1300;
            if (this.chart_parameter_data && this.chart_parameter_data.data_list[1].data.length != 0) {
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
            } else {
                this.$(".chart_peak").hide()
            };
        },
        chart_satisfaction: function () {
            var set_option = {
                legend: {
                    icon: 'stack',
                    orient: 'vertical',
                    right: '10px',
                    top: '10px',
                    selected: {
                        '候车满意度': true,
                        '乘车舒适满意度': true,
                        '企业满意度': true,
                        '乘客满意度': true,
                    }
                },
                grid: {
                    left: 72,
                    top: '0%',
                    right: 191,
                    containLabel: true
                },
                xAxis: {
                    position: 'top',
                    silent: false,
                    show: true
                },
                yAxis: {
                    inverse: true,
                    max: 100,
                    axisLabel: {
                        formatter: '{value}',
                    },
                }
            };
            if (this.chart_satisfaction_data && this.chart_satisfaction_data.data_list[1].data) {//10.12判断
                var chart_option = supply_make_chart_options.default_option_set1(this.chart_satisfaction_data, set_option);
                var mychart = echarts.init(this.$('.chart_satisfaction')[0]);
                mychart.setOption(chart_option);
                this.switch_chart(mychart);
            } else {
                this.$(".chart_satisfaction_bt").hide()
            };
        },
        switch_chart: function (mychart) {
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
            this.$el.on("click", ".chart_satisfaction_bt label", function () {
                if ($(this).find("input[type='radio']").hasClass("way_1")) {
                    option = option_set_1;
                } else {
                    option = option_set_2;
                }
                mychart.setOption(option);
            });
        }
    });

    // 线路分时客流图表(其它方式) Line-day/weeks/month
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
    //  各公司分时客流chart（与1510 一样？9.29gy）
    // var company_passenger_flow_chart = Widget.extend({
    //     template: "company_passenger_flow_template",
    //     init: function (parent, data) {
    //         this._super(parent);
    //         this.chart_data = data;
    //         // alert(this.chart_data.company_name)
    //     },
    //     start: function () {
    //         // 分时客流展示
    //         this.shunt_chart();
    //         // 总公司客流构成
    //         this.passenger_flow_chart();
    //     },
    //     shunt_chart: function () {
    //         var data_list = this.chart_data.data_list;
    //         this.set_chart_data(data_list)
    //         var set_option = {
    //             legend: {
    //                 icon: 'stack',
    //                 orient: 'vertical',
    //                 right: '10%',
    //                 top: '10px',
    //             },
    //             xAxis: {
    //                 show: true,
    //                 axisLabel: {
    //                     formatter: '{value}'
    //                 },
    //             },
    //             grid: {
    //                 left: '10%',
    //                 bottom: '3%',
    //                 right: '10%',
    //                 top: '25%',
    //                 containLabel: true
    //             },
    //         }
    //         var chart_option = supply_make_chart_options.default_option_set1(this.chart_data, set_option);
    //         var mychart = echarts.init(this.$('.chart_passenger_flow')[0]);
    //         mychart.setOption(chart_option);
    //     },
    //     passenger_flow_chart: function () {
    //         var chart_data = this.chart_data_set;
    //         var pie_option = {
    //             tooltip: {
    //                 trigger: 'item',
    //                 formatter: "{a} <br/>{b} : {c} ({d}%)"
    //             },
    //             series: [{
    //                 name: '访问来源',
    //                 type: 'pie',
    //                 radius: '80%',
    //                 center: ['50%', '60%'],
    //                 label: {
    //                     normal: {
    //                         position: "inner"
    //                     }
    //                 },
    //                 data: chart_data.pie_data
    //             }]
    //         };
    //         var pie_chart = echarts.init(this.$('.chart2')[0]);
    //         pie_chart.setOption(pie_option);
    //     },
    //     set_chart_data: function (data_list) {
    //         var legend_data = [];
    //         var pie_data = [];
    //         for (var i = 0, l = data_list.length; i < l; i++) {
    //             var data = data_list[i];
    //             var series_obj = {
    //                 name: data.name,
    //                 type: 'line',
    //                 symbolSize: 1,
    //                 lineStyle: {
    //                     normal: {
    //                         color: data.color,
    //                     }
    //                 },
    //                 data: data.data
    //             };
    //             var pie_obj = {
    //                 name: data.name,
    //                 value: eval(data.data.join("+")),
    //             }
    //             legend_data.push(data.name);
    //             pie_data.push(pie_obj);
    //         }
    //         this.chart_data_set = { legend_data: legend_data, pie_data: pie_data };
    //     },
    // });

    // 站点分时客流 site odoo extend
    var site_passenger_flow_base = Widget.extend({
        init: function (parent) {
            this._super(parent);
        },
        start: function () {
            var self = this;
            var self = this;
            model_city.query().filter([["key", "=", 'city.code']]).all().then(function (citys) {
                model_choseline.query().filter([["state", "=", 'inuse']]).all().then(function (lines) {
                    model_site.query().filter([["route_id", "=", parseInt(lines[0].id)]]).all().then(function (sites) {
                        config_parameter.query().filter([["key", "=", "dispatch.desktop.restful"]]).all().then(function (restful) {
                            RESTFUL_URL = restful[0].value;      //url-EDN   待提供接口将RESTFUL_URL替换前缀
                            var site_top_list = [];
                            var site_down_list = [];
                            _.each(sites, function (ret) {
                                if (ret.direction == "up") {
                                    site_top_list.push(ret);
                                } else {
                                    site_down_list.push(ret);
                                }
                            });
                            var options = {
                                cityCode: citys[0].value,
                                lineInfo: lines,
                                initSiteInfo: site_top_list
                            };
                            new site_passenger_flow(self, options).appendTo(self.$el);
                        });
                    });
                });
            });
        }
    });
    // 站点分时客流 site
    var site_passenger_flow = Widget.extend({
        template: "supply_template",
        init: function (parent, args) {
            this._super(parent);
            this.lineDate = args.lineInfo;
            this.cityCode = args.cityCode;
            this.siteDate = args.initSiteInfo;
        },
        start: function () {
            $(".o_loading").show();
            // var layer_index = layer.msg("加载中...", { time: 0, shade: 0.3 });
            var title = "站点分时客流";
            // 9.22跟换时间模型
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

            var direction = [
                { name: "上行", id: "0" },
                { name: "下行", id: "1" },
            ];
            var data_type = [
                { name: "工作日", id: "d1" },
                { name: "周末", id: "d2" },
                { name: "节假日", id: "d3" },
            ];
            var data_scope = [
                "2017-06-26", "2017-07-31"
            ];
            // var platform = [
            //     { name: "世界之窗", id: "s1" },
            //     { name: "白石洲", id: "s2" },
            //     { name: "蛇口", id: "s3" },
            //     { name: "人民公园", id: "s4" },
            //     { name: "市政府", id: "s5" },
            //     { name: "白菜花园", id: "s6" },
            //     { name: "酷派信息港", id: "s7" }
            // ];
            var platform = this.siteDate;

            var dis_set = {
                data_scope: true      //9.22
            };
            var options = {
                title: title,
                plan_way: plan_way,
                line_list: line_list,
                direction: direction,
                data_type: data_type,
                data_scope: data_scope,
                platform: platform,
                dis_set: dis_set,
                city_code: this.cityCode,
                history_passenger_flow: history_passenger_flow, //9.22
                predict_passenger_flow_time: predict_passenger_flow_time//9.22
            };
            new supply_title(this, options).appendTo(this.$('.operate_title'));
        }
    });
    core.action_registry.add('lty_operating_supply.site_passenger_flow', site_passenger_flow_base);

    // 站点分时客流 site-按时-全站
    var site_passenger_flow_chart_scatter = Widget.extend({
        template: "site_chart_scatter_template",
        init: function (parent, data) {
            this._super(parent);
            this.chart_data = data;
        },
        start: function () {
            this.scatter_chart();
        },
        scatter_chart: function () {
            var schema = [
                { name: 'date', index: 0, text: '时间' },
                { name: 'site', index: 1, text: '站' },
                { name: 'kl', index: 2, text: '客流' },
                { name: 'yl', index: 3, text: '运力' }
            ];
            this.chart_data.schema = schema;
            var set_option = {
                tooltip: {
                    padding: 10,
                    backgroundColor: '#222',
                    borderColor: '#777',
                    borderWidth: 1,
                    formatter: function (obj) {
                        var value = obj.value;
                        return '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 18px;padding-bottom: 7px;margin-bottom: 7px">' +
                            value[1] + ' ' + value[0] + '点：</div>' +
                            schema[2].text + '：' + value[2] + '<br>' +
                            schema[3].text + '：' + value[3] + '<br>'
                    }
                },
            };
            var chart_option = supply_make_chart_options.default_option_set2(this.chart_data, set_option);
            var mychart = echarts.init(this.$('.chart_passenger_flow')[0]);
            mychart.setOption(chart_option);
        }
    });
    // 站点分时客流 site-按时-单站
    var site_passenger_flow_hour_chart = Widget.extend({
        template: "site_passenger_flow_hour_chart_template",
        init: function (parent, data1) {    //data2如果做添加参数
            this._super(parent);
            this.chart_data = data1;
            // this.site_table_data = data2;
        },
        start: function () {
            // 客流运力图表
            this.chart_parameter_fn();
            // 站点信息
            // this.site_table_info();
        },
        chart_parameter_fn: function () {
            this.chart_data.legend_number = 2;
            var set_option = {
                grid: {
                    left: '3%',
                    bottom: '3%',
                    right: 190,
                    top: '30%',
                    containLabel: true
                },
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
            }
            var chart_option = supply_make_chart_options.default_option_set1(this.chart_data, set_option);
            var mychart = echarts.init(this.$('.chart_passenger_flow')[0]);
            mychart.setOption(chart_option);
            this.switch_chart(mychart);
        },
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
        // this.site_table_data = data2;原型不做
        // site_table_info: function () {
        //     $(".site_info_table").bootstrapTable({
        //         data: this.site_table_data,
        //         pagination: true,
        //         pageNumber: 1,
        //         pageSize: 10,
        //         pageList: [],
        //         paginationLoop: false,
        //         paginationPreText: "上一页",
        //         paginationNextText: "下一页",
        //     })
        // }
    });

    //各公司分时客流 odoo extend
    var companies_are_time_sharing_base = Widget.extend({
        init: function (parent) {
            this._super(parent);
        },
        start: function () {
            var self = this;
            var self = this;
            model_city.query().filter([["key", "=", 'city.code']]).all().then(function (citys) {//城市
                res_company.query().filter([]).all().then(function (companys) {
                    // model_choseline.query().filter([["state", "=", 'inuse']]).all().then(function (lines) {//线路
                        config_parameter.query().filter([["key", "=", "dispatch.desktop.restful"]]).all().then(function (restful) {    //url
                            RESTFUL_URL = restful[0].value;              //url-end
                            var options = {
                                cityCode: citys[0].value,
                                // lineInfo: lines,
                                // company: companys[0].name,
                                company: companys
                            };
                            new company_passenger_flow(self, options).appendTo(self.$el);
                        });
                    // });
                });
            });
        }
    });
    // 各公司分时客流 company
    var company_passenger_flow = Widget.extend({
        template: "supply_template",
        init: function (parent, args) {
            this._super(parent);
            // this.lineDate = args.lineInfo;
            this.cityCode = args.cityCode;
            this.company = args.company;
        },
        start: function () {
            $(".o_loading").show();
            var title = "各公司分时客流与构成";
            // 9.22时间模块跟换
            var history_passenger_flow = [
                { name: "前30天", id: "30" },
                { name: "前60天", id: "60" },
                { name: "前90天", id: "90" },
                { name: "前365天", id: "365" },
                { name: "所有", id: "all" },
            ];
            var predict_passenger_flow_time = "20170926";
            // 
            var data_scope = [
                "2017-06-26", "2017-07-31"
            ];
            var plan_way = [     //9.27
                { name: "按时", en_name: "when", value: 1 },
                { name: "按天", en_name: "day", value: 2 },
                { name: "按周", en_name: "weeks", value: 3 },
                { name: "按月", en_name: "month", value: 4 },
            ];
            // var company_list = [
            //     { name: "总公司", id: "comp1" },
            //     { name: "一分公司", id: "comp2" },
            //     { name: "二分公司", id: "comp3" },
            //     { name: "三分公司", id: "comp4" }
            // ];
            var company_list = this.company;
            var dis_set = {
                data_scope: true          //9.22   
            };
            var options = {
                history_passenger_flow: history_passenger_flow,              //9.22
                predict_passenger_flow_time: predict_passenger_flow_time,    //9.22
                title: title,
                plan_way: plan_way,
                data_scope: data_scope,
                dis_set: dis_set,
                company_list: company_list,
                city_code: this.cityCode
            };
            new supply_title(this, options).appendTo(this.$('.operate_title'));
        }
    });
    core.action_registry.add('lty_operating_supply.company_passenger_flow', companies_are_time_sharing_base);//odoo

    // 各公司分时客流 chart
    var company_passenger_flow_chart = Widget.extend({
        template: "company_passenger_flow_template",
        init: function (parent, data) {
            this._super(parent);
            this.chart_data = data;
        },
        start: function () {
            // 分时客流展示
            this.shunt_chart();
            // 总公司客流构成
            this.passenger_flow_chart();
        },
        shunt_chart: function () {
            var chart_data = {

            };
            var set_option = {
                legend: {
                    icon: 'stack',
                    orient: 'vertical',
                    right: '10%',
                    top: '10px',
                },
                xAxis: {
                    show: true,
                    axisLabel: {
                        formatter: '{value}'
                    },
                },
                grid: {
                    left: '10%',
                    bottom: '3%',
                    right: '10%',
                    top: '25%',
                    containLabel: true
                },
            }
            var chart_option = supply_make_chart_options.default_option_set1(this.chart_data, set_option);
            var mychart = echarts.init(this.$('.chart_passenger_flow')[0]);
            mychart.setOption(chart_option);
        },
        passenger_flow_chart: function () {
            var pie_chart_data = this.chart_data.pie_chart_data;
            var pie_option = {
                tooltip: {
                    trigger: 'item',
                    formatter: "{a} <br/>{b} : {c} ({d}%)"
                },
                series: [{
                    name: '访问来源',
                    type: 'pie',
                    radius: '70%',
                    center: ['50%', '60%'],
                    label: {
                        normal: {
                            position: "inner"
                        }
                    },
                    data: pie_chart_data
                }]
            };
            var pie_chart = echarts.init(this.$('.chart2')[0]);
            pie_chart.setOption(pie_option);
        },
        set_chart_data: function (data_list) {
            var legend_data = [];
            var pie_data = [];
            for (var i = 0, l = data_list.length; i < l; i++) {
                var data = data_list[i];
                var series_obj = {
                    name: data.name,
                    type: 'line',
                    symbolSize: 1,
                    lineStyle: {
                        normal: {
                            color: data.color,
                        }
                    },
                    data: data.data
                };
                var pie_obj = {
                    name: data.name,
                    value: eval(data.data.join("+")),
                }
                legend_data.push(data.name);
                pie_data.push(pie_obj);
            }
            this.chart_data_set = { legend_data: legend_data, pie_data: pie_data };
        },
    });

    // 分时准点率与滞站客流 odoo extend
    var line_passenger_flow_base = Widget.extend({
        init: function (parent) {
            this._super(parent);
        },
        start: function () {
            var self = this;
            model_city.query().filter([["key", "=", 'city.code']]).all().then(function (citys) {
                model_choseline.query().filter([["state", "=", 'inuse']]).all().then(function (lines) {//线路
                    model_site.query().filter([["route_id", "=", parseInt(lines[0].id)]]).all().then(function (sites) {
                        config_parameter.query().filter([["key", "=", "dispatch.desktop.restful"]]).all().then(function (restful) {
                            RESTFUL_URL = restful[0].value;      //url-end
                            var site_top_list = [];
                            var site_down_list = [];
                            _.each(sites, function (ret) {
                                if (ret.direction == "up") {
                                    site_top_list.push(ret);
                                } else {
                                    site_down_list.push(ret);
                                }
                            });
                            var options = {
                                cityCode: citys[0].value,
                                lineInfo: lines,
                                initSiteInfo: site_top_list
                            };
                            new time_place_passenger_flow(self, options).appendTo(self.$el);
                        });
                    });
                });
            });
        }
    });
    // 分时准点率与滞站客流
    var time_place_passenger_flow = Widget.extend({
        template: "supply_template",
        init: function (parent, args) {
            this._super(parent);
            this.lineDate = args.lineInfo;
            this.cityCode = args.cityCode;
            this.siteDate = args.initSiteInfo;
        },
        start: function () {
            // $(".o_loading").show();
            var title = "分时准点率与滞站客流";
            // 9.25跟换时间模型
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
            //     { name: "236路", id: "o1" },
            //     { name: "M231路", id: "o1" },
            //     { name: "229路", id: "o1" },
            //     { name: "298路", id: "o1" },
            // ];
            var line_list = this.lineDate;

            var direction = [
                { name: "上行", id: "0" },
                { name: "下行", id: "1" },
            ];
            var data_scope = [
                "2017-06-26", "2017-07-31"
            ];
            var dis_set = {
                data_scope: true      //9.25
            };
            var data_type = [
                { name: "工作日", id: "d1" },
                { name: "周末", id: "d2" },
                { name: "节假日", id: "d3" },
            ];
            // var platform = [
            //     { name: '蛇口站', id: 'ss1' },
            //     { name: '滨海站', id: 'ss2' },
            //     { name: '世界之窗', id: 'ss3' },
            //     { name: '白石洲', id: 'ss4' },
            //     { name: '红树林', id: 'ss5' },
            //     { name: '下沙', id: 'ss6' },
            //     { name: '购物公园', id: 'ss7' }
            // ];
            var platform = this.siteDate;
            var options = {
                title: title,
                plan_way: plan_way,
                line_list: line_list,
                direction: direction,
                platform: platform,
                dis_set: dis_set,
                data_type: data_type,
                data_scope: data_scope,
                city_code: this.cityCode,
                history_passenger_flow: history_passenger_flow, //9.25
                predict_passenger_flow_time: predict_passenger_flow_time//9.25
            };
            new supply_title(this, options).appendTo(this.$('.operate_title'));
        },
    });
    // core.action_registry.add('lty_operating_supply.time_place_passenger_flow', time_place_passenger_flow);
    core.action_registry.add('lty_operating_supply.time_place_passenger_flow', line_passenger_flow_base);

    // 分时准点率与滞站客流 chart
    var time_place_passenger_flow_chart = Widget.extend({
        template: "time_place_passenger_flow_template",
        init: function (parent, data1, data2) {
            this._super(parent);
            this.chart_parameter_data = data1;
            this.chart_satisfaction_data = data2;
        },
        start: function () {
            // 客流运力图表
            this.chart_passenger_flow();
            // 峰值图表
            // this.chart_peak_canvas();
            // 满意度图表
            this.chart_satisfaction();
        },
        chart_passenger_flow: function () {
            var set_option = {
                grid: {
                    left: '8%',
                    bottom: '3%',
                    right: 170,
                    top: '30%',
                    containLabel: true
                },
                yAxis: {
                    axisLabel: {
                        formatter: '{value}%'
                    },
                }
            }
            var chart_option = supply_make_chart_options.default_option_set1(this.chart_parameter_data, set_option);
            var mychart = echarts.init(this.$('.chart_passenger_flow')[0]);
            mychart.setOption(chart_option);
        },
        chart_satisfaction: function () {
            var set_option = {
                grid: {
                    left: "8%",
                    top: '0%',
                    right: 170,
                    containLabel: true
                },
                xAxis: {
                    position: 'top',
                    silent: false,
                    show: true
                },
                yAxis: {
                    inverse: true,
                    max: 100,
                    axisLabel: {
                        formatter: '{value}人',
                    },
                },
                color: ['#4b8cb4']
            };
            var chart_option = supply_make_chart_options.default_option_set1(this.chart_satisfaction_data, set_option);
            var mychart = echarts.init(this.$('.chart_satisfaction')[0]);
            mychart.setOption(chart_option);
        }
    });
});
