odoo.define("lty_dispatch_desktop_widget.plan_display", function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;

    var plan_display = Widget.extend({
        template: "plan_display_template",
        events: {
            'click .close_bt': 'closeFn',
        },
        init: function(parent, data){
            this._super(parent);
            this.location_data = data;
            var uplink_plan = {
                name: "上行",
                data_list: [
                    {
                        id: "plan_1",
                        scheduling_status: 0,
                        vehicles_status: 1,
                        plan_time: "8:15",
                        arrive_time: "9:15",
                        vehicle: "655",
                        driver: "刘德华",
                        start_status: "待发"
                    },
                    {
                        id: "plan_2",
                        scheduling_status: 1,
                        vehicles_status: 1,
                        plan_time: "8:15",
                        arrive_time: "9:15",
                        vehicle: "655",
                        driver: "刘德华",
                        start_status: "待发"
                    },
                    {
                        id: "plan_3",
                        scheduling_status: 1,
                        vehicles_status: 0,
                        plan_time: "8:15",
                        arrive_time: "9:15",
                        vehicle: "655",
                        driver: "刘德华",
                        start_status: "待发"
                    }
                ]
            };
            var uplink_yard = {
                name: "上行",
                data_list: [
                    {
                        id: "yard_1",
                        driver_status: 0,
                        vehicles_status: 1,
                        plan_time: "8:15",
                        vehicle: "264",
                        line: 16,
                        back_time: "8:10",
                        parking: "5"
                    },
                    {
                        id: "yard_1",
                        driver_status: 0,
                        vehicles_status: 1,
                        plan_time: "8:15",
                        vehicle: "264",
                        line: 16,
                        back_time: "8:10",
                        parking: "5"
                    },
                    {
                        id: "yard_1",
                        driver_status: 0,
                        vehicles_status: 1,
                        plan_time: "8:15",
                        vehicle: "264",
                        line: 16,
                        back_time: "8:10",
                        parking: "5"
                    },
                    {
                        id: "yard_1",
                        driver_status: 1,
                        vehicles_status: 0,
                        plan_time: "8:15",
                        vehicle: "264",
                        line: 16,
                        back_time: "8:10",
                        parking: "5"
                    },
                    {
                        id: "yard_1",
                        driver_status: 0,
                        vehicles_status: 1,
                        plan_time: "8:15",
                        vehicle: "264",
                        line: 16,
                        back_time: "8:10",
                        parking: "5"
                    },
                    {
                        id: "yard_1",
                        driver_status: 1,
                        vehicles_status: 1,
                        plan_time: "8:15",
                        vehicle: "264",
                        line: 16,
                        back_time: "8:10",
                        parking: "5"
                    },
                    {
                        id: "yard_1",
                        driver_status: 0,
                        vehicles_status: 1,
                        plan_time: "8:15",
                        vehicle: "264",
                        line: 16,
                        back_time: "8:10",
                        parking: "5"
                    },
                    {
                        id: "yard_1",
                        driver_status: 1,
                        vehicles_status: 0,
                        plan_time: "8:15",
                        vehicle: "264",
                        line: 16,
                        back_time: "8:10",
                        parking: "5"
                    },
                    {
                        id: "yard_1",
                        driver_status: 0,
                        vehicles_status: 1,
                        plan_time: "8:15",
                        vehicle: "264",
                        line: 16,
                        back_time: "8:10",
                        parking: "5"
                    },
                    {
                        id: "yard_1",
                        driver_status: 0,
                        vehicles_status: 1,
                        plan_time: "8:15",
                        vehicle: "264",
                        line: 16,
                        back_time: "8:10",
                        parking: "5"
                    },
                    {
                        id: "yard_1",
                        driver_status: 0,
                        vehicles_status: 1,
                        plan_time: "8:15",
                        vehicle: "264",
                        line: 16,
                        back_time: "8:10",
                        parking: "5"
                    },
                ]
            };
            var uplink_transit = {
                name: "上行",
                data_list: [
                    {
                        id: "yard_1",
                        driver_status: 0,
                        vehicles_status: 1,
                        plan_time: "8:15",
                        vehicle: "264",
                        line: 16,
                        back_time: "8:10",
                        parking: "5"
                    },
                    {
                        id: "yard_1",
                        driver_status: 1,
                        vehicles_status: 1,
                        plan_time: "8:15",
                        vehicle: "264",
                        line: 16,
                        back_time: "8:10",
                        parking: "5"
                    },
                    {
                        id: "yard_1",
                        driver_status: 1,
                        vehicles_status: 1,
                        plan_time: "8:15",
                        vehicle: "264",
                        line: 16,
                        back_time: "8:10",
                        parking: "5"
                    },
                    {
                        id: "yard_1",
                        driver_status: 1,
                        vehicles_status: 0,
                        plan_time: "8:15",
                        vehicle: "264",
                        line: 16,
                        back_time: "8:10",
                        parking: "5"
                    },
                ]
            }
            this.uplink_plan = uplink_plan;
            this.uplink_yard = uplink_yard;
            this.uplink_transit = uplink_transit;
            this.down_plan = uplink_plan ;
            this.down_yard = uplink_yard;
            this.down_transit = uplink_transit;
        },
        start: function(){
            var layer_index = layer.msg("加载中...", {time: 0, shade: 0.3});
            var linePlanParkOnlineModel_set = {
                layer_index: layer_index
            }
            sessionStorage.setItem("linePlanParkOnlineModel_set", JSON.stringify(linePlanParkOnlineModel_set));
            this.cont_info();
        },
        cont_info: function(){
            new bus_plan(this, this.uplink_plan).appendTo(this.$(".plan_group"));
            new bus_yard(this, this.uplink_yard).appendTo(this.$(".plan_group"));
            new bus_transit(this, this.uplink_transit).appendTo(this.$(".plan_group"));
            this.down_plan.name = "下行";
            this.down_yard.name = "下行";
            this.down_transit.name = "下行";
            new bus_plan(this, this.down_plan).appendTo(this.$(".plan_group"));
            new bus_yard(this, this.down_yard).appendTo(this.$(".plan_group"));
            new bus_transit(this, this.down_transit).appendTo(this.$(".plan_group"));
            this.load_fn();
        },
        load_fn: function(){
            var self = this;
            // 阻止默认右键
            self.$(".section_plan_cont").on("contextmenu ", ".content_tb .point", function(){
                return false;
            });

            // 点击取消右键弹窗
            $("body").click(function(){
                var plan_display_set = $(".plan_display_set");
                if (plan_display_set.length>0){
                    var plan_pid = plan_display_set.attr("plan_pid");
                    var model = plan_display_set.attr("model");
                    self.$("."+model+" .content_tb .point[pid="+plan_pid+"]").removeClass("active_tr");
                    $(".plan_display_set").remove();
                }                
            })

            // 重置
            $("body").on("click", ".adjust_box .reset_bt", function(){
                $(".adjust_box .plan_num").val("");
            });

            // 提交
            $("body").on("click", ".adjust_box .ok_bt", function(){
                layer.msg("请求接口还没有给到", {time: 2000, shade: 0.3});
            });

            // 关闭
            $("body").on("click", ".adjust_box .close_bt", function(){
                layer.closeAll();
            });
        },
        closeFn: function(){
            this.destroy();
        },
    });
    core.action_registry.add('lty_dispatch_desktop_widget.plan_display', plan_display);

    var bus_plan = Widget.extend({
        template: "vehicles_plan_template",
        init: function(parent, data){
            this._super(parent);
            this.plan_data = data;
        },
        start: function(){
            var self = this;
            // 选中计划
            self.$(".content_tb").on("click", "tr.point", function(){
                $(this).addClass("active_tr").siblings().removeClass('active_tr');
            });

            // 取消计划
            self.$el.find(".bottom_bt").on("click", ".cancel", function(){
                if (self.$(".active_tr").length == 0){
                    layer.msg("请选择需要处理的计划", {time: 1000, shade: 0.3});
                    return;
                }
                self.$(".active_tr").removeClass("active_tr");
            });

            //上下移动计划
            self.$el.find(".bottom_bt").on("click", ".move_bt", function(){
                var active_tr = self.$(".active_tr");
                if (active_tr.length == 0){
                    layer.msg("请选择需要处理的计划", {time: 1000, shade: 0.3});
                    return;
                }
                var name = $(this).attr("name");
                self.move_fn(active_tr, name);
            });

            // 调整计划
            self.$el.find(".bottom_bt").on("click", ".adjust", function(){
                var init_data = {
                    vehicle:1,
                    direction_of:1,
                    driver:1,
                    adjust_the_reason:1,
                    time:1,
                    line:1,
                    run_line:1,
                    trip_time:1,
                    type:1,
                    mileage:1
                };
                self.layer_index = layer.open({
                    type: 1,
                    title: "调整计划",
                    area: ['600px', ''],
                    resize: false,
                    content: QWeb.render("adjust_the_plan_template", {quota: init_data}),
                });
            });

            // 右键事件
            self.$(".content_tb").on("mousedown", ".point", function(e){
                if (e.button == 2){
                    var pid = $(this).attr("pid");
                    if (self.$(".set_"+pid).length > 0){
                        return false;
                    }
                    $("body").click();
                    $(this).addClass("active_tr")
                    var parent_obj = $(this).parents(".plan_display")[0];
                    var options = {
                        model: "bus_plan",
                        pid: pid,
                        x: e.clientX + 5 - parseInt(parent_obj.style.left.replace("px","")),
                        y: e.clientY + 5 - parseInt(parent_obj.style.top.replace("px","")),
                        zIndex: 1,
                        data_list: [
                            {name: "发送计划到车辆", en_name: "send_plan_vehicles_bt"},
                            {name: "发送消息", en_name: "send_message_bt"},
                            {name: "添加计划", en_name: "add_plan_bt"},
                            {name: "手动发车", en_name: "manual_start_bt"},
                            {name: "修改", en_name: "fix_bt"},
                            {name: "批量更改车辆司机", en_name: "batch_change_drivers_bt"},
                            {name: "还原时间", en_name: "reduction_time_bt"},
                            {name: "电子地图", en_name: "electronic_map_bt"}
                        ]
                    }
                    var dialog = new plan_display_set(self, options);
                    dialog.appendTo(self.$(".section_plan_cont"));
                    return false;
                }
            });
        },
        move_fn: function(active_tr, type){
            if (type == "front"){
                var prev_tr = active_tr.prev ('tr.point');
                if (prev_tr.length > 0){
                    layer.msg("请求中，请稍后...", {shade: 0.3}, function(){
                        prev_tr.before(active_tr);
                    });
                    return;
                }
                layer.msg("该计划已经是最前面的", {time: 1000, shade: 0.3});
            }else{
                var next_tr = active_tr.next ('tr.point');
                if (next_tr.length > 0){
                    layer.msg("请求中，请稍后...", {shade: 0.3}, function(){
                        next_tr.after(active_tr);
                    });
                    return;
                }
                layer.msg("该计划已经是最后面的", {time: 1000, shade: 0.3});
            }
        },
    });

    var bus_yard = Widget.extend({
        template: "vehicles_yard_template",
        init: function(parent, data){
            this._super(parent);
            this.yard_data = data;
        },
        start: function(){
            var self = this;
            // 右键事件
            self.$(".content_tb").on("mousedown", ".point", function(e){
                if (e.button == 2){
                    var pid = $(this).attr("pid");
                    if (self.$(".set_"+pid).length > 0){
                        return false;
                    }
                    $("body").click();
                    $(this).addClass("active_tr")
                    var parent_obj = $(this).parents(".plan_display")[0];
                    var options = {
                        model: "bus_yard",
                        pid: pid,
                        x: e.clientX + 5 - parseInt(parent_obj.style.left.replace("px","")),
                        y: e.clientY + 5 - parseInt(parent_obj.style.top.replace("px","")),
                        zIndex: 1,
                        data_list: [
                            {name: "添加计划", en_name: "add_plan_bt"},
                            {name: "发送消息", en_name: "send_message_bt"},
                            {name: "司乘签到", en_name: "sign_in_bt"},
                            {name: "编辑车辆", en_name: "edit_vehicles_bt"},
                            {name: "立即排班", en_name: "immediately_scheduling_bt"},
                            {name: "取消排班", en_name: "cancel_scheduling_bt"},
                            {name: "退出运营", en_name: "exit_operation_bt"},
                            {name: "异常状态", en_name: "abnormal_state_bt"},
                            {name: "进场任务", en_name: "in_task_bt"},
                            {name: "电子地图", en_name: "electronic_map_bt"}
                        ]
                    }
                    var dialog = new plan_display_set(self, options);
                    dialog.appendTo(self.$(".section_plan_cont"));
                    return false;
                }
            });
        }
    });

    var bus_transit = Widget.extend({
        template: "vehicles_transit_template",
        init: function(parent, data){
            this._super(parent);
            this.transit_data = data;
        },
        start: function(){
            var self = this;
            // 右键事件
            self.$(".content_tb").on("mousedown", ".point", function(e){
                if (e.button == 2){
                    var pid = $(this).attr("pid");
                    if (self.$(".set_"+pid).length > 0){
                        return false;
                    }
                    $("body").click();
                    $(this).addClass("active_tr")
                    var parent_obj = $(this).parents(".plan_display")[0];
                    var options = {
                        model: "bus_transit",
                        pid: pid,
                        x: e.clientX + 5 - parseInt(parent_obj.style.left.replace("px","")),
                        y: e.clientY + 5 - parseInt(parent_obj.style.top.replace("px","")),
                        zIndex: 1,
                        data_list: [
                            {name: "添加计划", en_name: "add_plan_bt"},
                            {name: "发送消息", en_name: "send_message_bt"},
                            {name: "手动返回", en_name: "manual_return_bt"},
                            {name: "司乘签到", en_name: "sign_in_bt"},
                            {name: "异常处理", en_name: "abnormal_deal_bt"},
                            {name: "异常状态", en_name: "abnormal_state_bt"},
                            {name: "手动签点", en_name: "manual_sign_bt "},
                            {name: "电子地图", en_name: "electronic_map_bt"}
                        ]
                    }
                    var dialog = new plan_display_set(self, options);
                    dialog.appendTo(self.$(".section_plan_cont"));
                    return false;
                }
            });
        }
    });

    var plan_display_set = Widget.extend({
        template: "plan_display_set_template",
        init: function(parent, data){
            this._super(parent);
            this.location_data =  data;
        },
    });

    return plan_display;
});

