odoo.define(function(require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var datepicker = require('web.datepicker');

    // 乘客满意度title
    var service_title = Widget.extend({
        template: "supply_title_template",
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
                direction: this.$(".direction option:selected").val(),
                predict_start_time: this.$(".data_scope .start_time").val(),
                predict_end_time: this.$(".data_scope .end_time").val(),
                company: this.$(".company option:selected").val(),
                company_name: this.$(".company option:selected").text()
            };
            var chart_cont_obj = this.$el.parent(".operate_title").next();
            arg_options.chart_obj = chart_cont_obj;
            chart_cont_obj.html("");
            // 暂时都数据加载相同
            
            new service_chart(this).appendTo(arg_options.chart_obj);
        }
    });

    // 服务保障
    var service = Widget.extend({
        template: "supply_template",
        init: function(parent) {
            this._super(parent);
        },
        start: function() {
            $(".o_loading").show();
            var title = "服务保障能力分析";
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
                { name: "集团", id: "g0" },
                { name: "一公司", id: "g1" },
                { name: "二公司", id: "g2" },
                { name: "三公司", id: "g3" },
            ];
            var direction = [
                { name: "上行", id: "c1" },
                { name: "下行", id: "c2" },
            ];
            var dis_set = {
                data_scope: true
            };
            var options = {
                title: title,
                plan_way: plan_way,
                line_list: line_list,
                company_list: company_list,
                direction: direction,
                dis_set: dis_set,
                data_scope: data_scope
            };
            new service_title (this, options).appendTo(this.$('.operate_title'));
        }
    });
    core.action_registry.add('lty_operating_supply.service', service);

    var service_chart = Widget.extend({
        template: "service_chart_template",
        init: function(parent){
            this._super(parent);
        }
    })
});