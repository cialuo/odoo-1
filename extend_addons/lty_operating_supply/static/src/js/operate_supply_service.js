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
            });//self

            // 时间筛选方式
            // self.$(".plan_way").on("click", "li", function () {
            //     $(this).addClass("active").siblings().removeClass('active');
            // })
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
            // 公司线路切换联动事件
            self.$(".company").change(function () {
                // var self = this;
                var company = self.$(".company");
                if (company.length == 0) {
                    return false;
                }
                var line_id = self.$(".company option:selected").val();
                res_company.query().filter([]).all().then(function (obj) {
                    console.log(obj);
                    self.$(".company").find("option").remove();
                    var options = "";
                    for (var i = 0; i < obj.length; i++) {
                        // <option name="tjw测试线路" value="10">tjw测试线路</option>
                        var item = obj[i];
                        options += "<option name='" + item.line_name + "' value='" + item.id + "' >" + item.line_name + "</option>";
                    };
                    self.$(".company").html(options);
                })
            }); //self.$
        },//start
        // 服务天周月切换
        service_switch: function (name) {
            var self = this;
            if (name == "when") {
                self.$(".history_passenger_flow").parent().removeClass("dis_none");
                self.$(".predict_passenger_flow_time").parent().removeClass("dis_none");
                self.$(".data_scope").addClass("dis_none");
                self.$(".data_type").parent().removeClass("dis_none");
                self.$(".direction").removeClass("dis_none");
                self.$(".company").parent().removeClass('dis_none');
                self.$(".platform").parent().addClass("dis_none");
            } else {
                self.$(".history_passenger_flow").parent().removeClass("dis_none");
                self.$(".predict_passenger_flow_time").parent().removeClass("dis_none");
                self.$(".company").parent().removeClass("dis_none");
                self.$(".data_scope").addClass("dis_none");
                self.$(".data_type").parent().removeClass("dis_none");
                self.$(".direction").addClass("dis_none");
                self.$(".company").parent().addClass('dis_none');
                self.$(".platform").parent().removeClass("dis_none");
            }
        },
        // gy-9.26
        get_filter_fn: function () {
            var arg_options = {
                history_time: this.$(".history_passenger_flow").val(),//9.26
                predict_passenger_flow_time: this.$(".predict_passenger_flow_time").val(),//9.26
                plan_way: this.$(".plan_way li.active").attr("name"),
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
            // 服务保障能力分析
            $.ajax({
                type: 'get',
                url: '',
                data: {},
                dataType: 'json',
                error: function (res) {
                    console.log(res.resultMsg);
                },
                success: function (res) {
                    console.log("数据成功")
                }//success
            });//$.ajax
            new service_chart(this).appendTo(arg_options.chart_obj);
        }
    });

    //服务保障能力分析 odoo extend
    var service_base = Widget.extend({
        init: function (parent) {
            this._super(parent);
        },
        start: function () {
            var self = this;
            model_city.query().filter([["key", "=", 'city.code']]).all().then(function (citys) {//城市
                res_company.query().filter([]).all().then(function (companys) {//公司单位
                    model_choseline.query().filter([["state", "=", 'inuse']]).all().then(function (lines) {//线路
                        config_parameter.query().filter([["key", "=", "dispatch.desktop.restful"]]).all().then(function (restful) {//url
                            RESTFUL_URL = restful[0].value;              //url-end
                            var options = {
                                cityCode: citys[0].value,
                                lineInfo: lines,
                                // company: companys[0].name,
                                // initSiteInfo: site_top_list
                                company: companys
                            };
                            new service(self, options).appendTo(self.$el);
                        });
                    });
                });
            });
            // 月周
            model_city.query().filter([["key", "=", 'city.code']]).all().then(function (citys) {//城市
                model_choseline.query().filter([["state", "=", 'inuse']]).all().then(function (lines) {//线路
                    model_site.query().filter([["route_id", "=", parseInt(lines[0].id)]]).all().then(function (sites) {
                        config_parameter.query().filter([["key", "=", "dispatch.desktop.restful"]]).all().then(function (restful) {//url
                            RESTFUL_URL = restful[0].value;              //url-end
                            var options = {
                                cityCode: citys[0].value,
                                lineInfo: lines,
                                // company: companys[0].name,
                                initSiteInfo: site_top_list
                            };
                            new service(self, options).appendTo(self.$el);
                        });
                    });
                });
            });
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
            this.siteDate = args.initSiteInfo;
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
            var predict_passenger_flow_time = "2017-07-31";
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
            var platform = this.siteDate;
            var company_list = this.company;
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
    core.action_registry.add('lty_operating_supply.service', service_base);

    var service_chart = Widget.extend({
        template: "service_chart_template",
        init: function (parent) {
            this._super(parent);
        }
    })
});