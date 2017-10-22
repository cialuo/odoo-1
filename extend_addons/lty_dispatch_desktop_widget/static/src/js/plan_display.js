odoo.define("lty_dispatch_desktop_widget.plan_display", function(require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var AutoComplete = require('web.AutoComplete');
    var QWeb = core.qweb;

    var plan_display = Widget.extend({
        template: "plan_display_template",
        events: {
            'click .close_bt': 'closeFn',
        },
        init: function(parent, data) {
            this._super(parent);
            this.location_data = data;
            var uplink_plan = {
                direction: 0,
                data_list: [{
                    id: "plan_1",
                    sendToScreen: 0,
                    sendToBus: 1,
                    planRunTime: new Date().getTime(),
                    planReachTime: new Date().getTime(),
                    selfId: "655",
                    driverName: "刘德华",
                    planState: "0",
                    direction: 0
                }]
            };
            var uplink_yard = {
                direction: 0,
                inField: 1,
                data_list: [{
                    id: "yard_1",
                    checkOut: 0,
                    runState: 1,
                    planRunTime: new Date().getTime(),
                    carNum: "264",
                    line: 16,
                    realReachTime: new Date().getTime(),
                    stopTime: "5",
                    direction: 0,
                    inField: 1
                }]
            };
            var uplink_transit = {
                direction: 0,
                inField: 0,
                data_list: [{
                    id: "transit_1",
                    checkOut: 0,
                    runState: 1,
                    planRunTime: new Date().getTime(),
                    carNum: "264",
                    line: 16,
                    planReachTime: new Date().getTime(),
                    stopTime: "5",
                    direction: 0,
                    inField: 0
                }]
            }
            this.uplink_plan = uplink_plan;
            this.uplink_yard = uplink_yard;
            this.uplink_transit = uplink_transit;
            this.down_plan = uplink_plan;
            this.down_yard = uplink_yard;
            this.down_transit = uplink_transit;
        },
        start: function() {
            var layer_index = layer.msg("加载中...", { time: 0, shade: 0.3 });
            var linePlanParkOnlineModel_set = {
                layer_index: layer_index
            }
            sessionStorage.setItem("linePlanParkOnlineModel_set", JSON.stringify(linePlanParkOnlineModel_set));

            // 订阅线路计划、车场、状态
            var package = {
                type: 2000,
                controlId: this.location_data.controllerId,
                open_modules: ["line_plan"]
            };
            try {
                websocket.send(JSON.stringify(package));
            } catch(e) {
                console.log(e);
            }

            this.load_plan();
        },
        load_plan: function() {
            var self = this;
            console.log(self.location_data.controllerId + '_' + self.location_data.line_id);
            $.ajax({
                url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename:"op_dispatchplan",controlsId:' + self.location_data.controllerId + ',lineId:' + self.location_data.line_id + '}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    console.log(ret.respose);
                    self.uplink_plan = {
                        direction: 0,
                        data_list: ret.respose
                    };
                    self.down_plan = {
                        direction: 1,
                        data_list: ret.respose
                    };
                    $.ajax({
                        url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename:"op_busresource",controlsId:' + self.location_data.controllerId + ',lineId:' + self.location_data.line_id + '}',
                        type: 'get',
                        dataType: 'json',
                        data: {},
                        success: function(data) {
                            console.log(data);
                            sessionStorage.setItem("busResource", JSON.stringify(data.respose));
                            self.uplink_yard = {
                                inField: 1,
                                direction: 0,
                                data_list: data.respose
                            };
                            self.down_yard = {
                                inField: 1,
                                direction: 1,
                                data_list: data.respose
                            };
                            self.uplink_transit = {
                                inField: 0,
                                direction: 0,
                                data_list: data.respose
                            };
                            self.down_transit = {
                                inField: 0,
                                direction: 1,
                                data_list: data.respose
                            };
                            self.cont_info();
                        }
                    });
                }
            });
        },
        cont_info: function() {
            new bus_plan(this, this.uplink_plan).appendTo(this.$(".plan_group"));
            new bus_yard(this, this.uplink_yard).appendTo(this.$(".plan_group"));
            new bus_transit(this, this.uplink_transit).appendTo(this.$(".plan_group"));
            new bus_plan(this, this.down_plan).appendTo(this.$(".plan_group"));
            new bus_yard(this, this.down_yard).appendTo(this.$(".plan_group"));
            new bus_transit(this, this.down_transit).appendTo(this.$(".plan_group"));
            this.load_fn();
        },
        load_fn: function() {
            var self = this;
            var passengerDelayModel_set = JSON.parse(sessionStorage.getItem("linePlanParkOnlineModel_set"));
            layer.close(passengerDelayModel_set.layer_index);
            $('.linePlanParkOnlineModel .section_plan_cont').mCustomScrollbar({
                theme: 'minimal'
            });
            self.$el.removeClass('hide_model');

            // 阻止默认右键
            self.$(".section_plan_cont").on("contextmenu ", ".content_tb .point", function() {
                return false;
            });

            // 点击取消右键弹窗
            $("body").click(function() {
                var plan_display_set = $(".plan_display_set");
                if (plan_display_set.length > 0) {
                    var plan_pid = plan_display_set.attr("plan_pid");
                    var model = plan_display_set.attr("model");
                    $("." + model + " .content_tb .point[pid=" + plan_pid + "]").removeClass("active_tr").removeClass("right");
                    $(".plan_display_set").remove();
                }
            });

            // 回车键触发事件
            document.onkeydown=function(event){
                var e = event || window.event;       
                 if(e && e.keyCode==13){
                     $('.btn-primary').click();
                }
            };

            // 计划，在场，在途手动操作交互事件
            self.linePlanParktransit_bt_fn();
        },
        linePlanParktransit_bt_fn: function() {
            var self = this;
            var plan_display = self.$(".plan_display");
            var controllerId = self.location_data.controllerId;
            var controllerObj = self.$el.parents($(".controller_" + controllerId));
            var lineId = this.location_data.line_id;

            // 车辆计划底部交互事件
            self.plan_bottom_fn();

            // 发送计划都车辆
            plan_display.on("click", ".plan_display_set[model='bus_plan'] li.send_plan_vehicles_bt", function() {
                var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                var obj = $(this).parents(".plan_display_set");
                var options = {
                    obj: obj,
                    id: obj.attr("plan_pid"),
                    direction: obj.attr("direction"),
                    layer_index: layer_index
                };
                self.send_plan_vehicles_fn(options);
            });

            //发送消息
            plan_display.on("click", ".plan_display_set li.send_message_bt", function() {
                var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                var obj = $(this).parents(".plan_display_set");
                var options = {
                    obj: obj,
                    id: obj.attr("plan_pid"),
                    direction: obj.attr("direction"),
                    layer_index: layer_index,
                    model: obj.attr("model")
                };
                self.send_short_msg_fn(options);
            });

            // 添加计划
            plan_display.on("click", ".plan_display_set li.add_plan_bt", function() {
                var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                var obj = $(this).parents(".plan_display_set");
                var options = {
                    id: obj.attr("plan_pid"),
                    layer_index: layer_index,
                    model: obj.attr("model")
                };
                self.add_plan_fn(options);
            });

            // 取消计划
            plan_display.on("click", ".plan_display_set li.cancel_plan_bt", function() {
                var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                var obj = $(this).parents(".plan_display_set");
                var options = {
                    id: obj.attr("plan_pid"),
                    layer_index: layer_index,
                    model: obj.attr("model")
                };
                self.cancel_plan_fn(options);
            });

            // 手动发车
            plan_display.on("click", ".plan_display_set li.manual_start_bt", function() {
                var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                var id = $(this).parents(".plan_display_set").attr("plan_pid");
                var options = {
                    id: id,
                    layer_index: layer_index
                };
                self.manual_start_fn(options);
            });

            // 修改计划
            plan_display.on("click", ".plan_display_set[model='bus_plan'] li.fix_bt", function() {
                var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                var obj = $(this).parents(".plan_display_set");
                var options = {
                    id: obj.attr("plan_pid"),
                    layer_index: layer_index
                };
                self.fix_plan_fn(options);
            });

            // 计划车辆还原时间
            plan_display.on("click", ".plan_display_set[model='bus_plan'] li.reduction_time_bt", function() {
                var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                var obj = $(this).parents(".plan_display_set");
                var options = {
                    obj: obj,
                    id: obj.attr("plan_pid"),
                    direction: obj.attr("direction"),
                    layer_index: layer_index
                };
                self.reduction_time_fn(options);
            });

            // 批量更改车辆或司机
            plan_display.on("click", ".plan_display_set[model='bus_plan'] li.batch_change_drivers_bt", function() {
                var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                var id = $(this).parents(".plan_display_set").attr("plan_pid");
                var options = {
                    id: id,
                    layer_index: layer_index
                };
                self.batch_fix_switch_fn(options);
            });

            // 手动返回
            plan_display.on("click", ".plan_display_set[model='bus_transit'] li.manual_return_bt", function() {
                var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                var id = $(this).parents(".plan_display_set").attr("plan_pid");
                var options = {
                    id: id,
                    layer_index: layer_index
                };
                self.manual_return_fn(options);
            });

            // 司乘签到
            plan_display.on("click", ".plan_display_set[model='bus_yard'] li.sign_in_bt, .plan_display_set[model='bus_transit'] li.sign_in_bt", function() {
                // alert("我是司乘签到");
                var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                var id = $(this).parents(".plan_display_set").attr("plan_pid");
                var options = {
                    id: id,
                    layer_index: layer_index
                };
                self.driver_check_in_fn(options);
            });

            // 编辑车辆
            plan_display.on("click", ".plan_display_set[model='bus_yard'] li.edit_vehicles_bt, .plan_display_set[model='bus_transit'] li.edit_vehicles_bt", function() {
                var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                var id = $(this).parents(".plan_display_set").attr("plan_pid");
                var options = {
                    id: id,
                    layer_index: layer_index
                };
                self.edit_the_vehicle_fn(options);
            });

            // 异常状态
            plan_display.on("click", ".plan_display_set[model='bus_yard'] li.abnormal_state_bt, .plan_display_set[model='bus_transit'] li.abnormal_state_bt", function() {
                var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                var id = $(this).parents(".plan_display_set").attr("plan_pid");
                var options = {
                    id: id,
                    layer_index: layer_index
                };
                self.error_state_fn(options);
            });

            // 进场任务
            plan_display.on("click", ".plan_display_set[model='bus_yard'] li.in_task_bt, .plan_display_set[model='bus_transit'] li.in_task_bt", function() {
                var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                var id = $(this).parents(".plan_display_set").attr("plan_pid");
                var options = {
                    id: id,
                    layer_index: layer_index
                };
                self.in_the_task_fn(options);
            });

            // 立即排班
            plan_display.on("click", ".plan_display_set[model='bus_yard'] li.immediately_scheduling_bt", function() {
                var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                var obj = $(this).parents(".plan_display_set");
                var options = {
                    obj: obj,
                    id: obj.attr("plan_pid"),
                    direction: obj.attr("direction"),
                    layer_index: layer_index
                };
                self.immediate_scheduling_fn(options);
            });

            // 取消排班
            plan_display.on("click", ".plan_display_set[model='bus_yard'] li.cancel_scheduling_bt", function() {
                var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                var obj = $(this).parents(".plan_display_set");
                var options = {
                    obj: obj,
                    id: obj.attr("plan_pid"),
                    direction: obj.attr("direction"),
                    layer_index: layer_index
                };
                self.cancel_scheduling_fn(options);
            });

            // 退出运营
            plan_display.on("click", ".plan_display_set[model='bus_yard'] li.exit_operation_bt", function() {
                var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                var obj = $(this).parents(".plan_display_set");
                var options = {
                    obj: obj,
                    id: obj.attr("plan_pid"),
                    direction: obj.attr("direction"),
                    layer_index: layer_index
                };
                self.exit_operation_fn(options);
            });

            // 搜索-车辆编号
            $("body").on("focus", ".customModal .carNum", function() {
                self.vehicle_search_autocomplete({ evt: this, controlId: controllerId, lineId: lineId });
            });

            // 搜索-司机工号
            // 应用功能: 添加计划、调整计划、批量更改车辆或司机、司乘签到
            $("body").on("focus", ".customModal .workerIdSearch, .customModal .driverNameSearch", function() {
                self.driver_search_autocomplete({ evt: this, controlId: controllerId });
            });

            // 搜索-乘务工号
            // 应用: 添加计划、调整计划、司乘签到
            $("body").on("focus", ".customModal .trainSearch, .customModal .trainNameSearch", function() {
                self.trainman_search_autocomplete({ evt: this, controlId: controllerId });
            });

            // 搜索-计划
            $("body").on("focus", ".customModal .planTimeS", function() {
                self.planTime_search_autocomplete({ evt: this});
            });
        },
        plan_bottom_fn: function() {
            var self = this;
            var plan_display = self.$(".plan_display");
            // 取消计划
            plan_display.on("click", ".bottom_bt .cancel", function() {
                var plan_box = $(this).parents(".plan_box");
                var bus_plan = plan_box.find(".bus_plan");
                // 先去掉右键浮层及active
                self.delete_active_fn(plan_display);
                var active_tr = bus_plan.find(".content_tb tr.active_tr");
                if (active_tr.length == 1) {
                    var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                    var options = {
                        id: active_tr.attr("pid"),
                        layer_index: layer_index
                    };
                    self.cancel_plan_fn(options);
                } else {
                    layer.msg("请选择需要处理的计划", { time: 1000, shade: 0.3 });
                }
            });

            // 上下移动计划
            plan_display.on("click", ".bottom_bt .move_bt", function() {
                var plan_box = $(this).parents(".plan_box");
                var bus_plan = plan_box.find(".bus_plan");
                // 先去掉右键浮层及active
                self.delete_active_fn(plan_display);
                var active_tr = bus_plan.find(".content_tb tr.active_tr");
                if (active_tr.length == 1) {
                    var options = {
                        active_tr: active_tr,
                        type: $(this).attr("name")
                    };
                    self.move_up_or_down_fn(options);
                } else {
                    layer.msg("请选择需要处理的计划", { time: 1000, shade: 0.3 });
                }
            });

            // 修改计划
            plan_display.on("click", ".bottom_bt .fix", function() {
                var plan_box = $(this).parents(".plan_box");
                var bus_plan = plan_box.find(".bus_plan");
                // 先去掉右键浮层及active
                self.delete_active_fn(plan_display);
                var active_tr = bus_plan.find(".content_tb tr.active_tr");
                if (active_tr.length == 1) {
                    var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                    var options = {
                        id: active_tr.attr("pid"),
                        layer_index: layer_index
                    };
                    self.fix_plan_fn(options);
                } else {
                    layer.msg("请选择需要处理的计划", { time: 1000, shade: 0.3 });
                }
            });

            // 调换计划
            plan_display.on("click", ".bottom_bt .adjust", function() {
                var plan_box = $(this).parents(".plan_box");
                var bus_plan = plan_box.find(".bus_plan");
                // 先去掉右键浮层及active
                self.delete_active_fn(plan_display);
                var active_tr = bus_plan.find(".content_tb tr.active_tr");
                if (active_tr.length == 1) {
                    var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                    var options = {
                        id: active_tr.attr("pid"),
                        layer_index: layer_index
                    };
                    self.adjust_plan_fn(options);
                } else {
                    layer.msg("请选择需要处理的计划", { time: 1000, shade: 0.3 });
                }
            });
        },
        delete_active_fn: function(plan_display){
            var r_pid = plan_display.find(".content_tb tr.right").attr("pid");
            plan_display.find(".plan_display_set").remove();
            plan_display.find(".content_tb tr.right").removeClass("active_tr").removeClass("right");
        },
        send_plan_vehicles_fn: function(options) {
            $.ajax({
                url: RESTFUL_URL + '/ltyop/plan/sendPlanToBus?apikey=71029270&params={id: "' + options.id + '"}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(options.layer_index);
                    if (ret.result == 0) {
                        //这里特别说明一下，由于请求成功后，后台会立即触发一次推送websoket，页面状态更新这里将不在做处理
                    }
                    layer.msg(ret.respose.text, { time: 1000, shade: 0.3 });
                }
            });
        },
        send_short_msg_fn: function(options) {
            var self = this;
            var tablename = "op_dispatchplan";
            if (options.model != "bus_plan") {
                tablename = "op_busresource";
            }
            $.ajax({
                url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename: "' + tablename + '",controlsId:' + self.location_data.controllerId + ',lineId:' + self.location_data.line_id + ',id:' + options.id + '}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(options.layer_index);
                    var retData = ret.respose[0];
                    console.log(retData);
                    if (!retData.selfId) {
                        retData.selfId = retData.carNum;
                    }
                    new send_short_msg_msg(self, retData).appendTo($('body'));
                }
            });
        },
        add_plan_fn: function(options) {
            var self = this;
            var tablename = "op_dispatchplan";
            if (options.model != "bus_plan") {
                tablename = "op_busresource";
            }
            $.ajax({
                url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename:"' + tablename + '",controlsId:' + self.location_data.controllerId + ',lineId:' + self.location_data.line_id + ',id:' + options.id + '}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(options.layer_index);
                    var retData = ret.respose[0];
                    console.log(retData);
                    if (!retData.selfId) {
                        retData.selfId = retData.carNum;
                    }
                    var dialog = new add_plan_w(self, retData);
                    dialog.appendTo($('body'));
                }
            });
        },
        manual_start_fn: function(options) {
            var self = this;
            $.ajax({
                url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename:"op_dispatchplan",controlsId:' + self.location_data.controllerId + ',lineId:' + self.location_data.line_id + ',id:' + options.id + '}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(options.layer_index);
                    var op = ret.respose[0];
                    console.log(op);
                    var dialog = new manual_start_w(self, op);
                    dialog.appendTo($('body'));
                }
            });
        },
        reduction_time_fn: function(options) {
            $.ajax({
                url: RESTFUL_URL + '/ltyop/plan/restoreTime?apikey=71029270&params={id: "' + options.id + '"}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(options.layer_index);
                    if (ret.result == 0) {
                        //这里特别说明一下，由于请求成功后，后台会立即触发一次推送websoket，页面状态更新这里将不在做处理
                    }
                    layer.msg(ret.respose.text, { time: 1000, shade: 0.3 });
                }
            });
        },
        batch_fix_switch_fn: function(options) {
            var self = this;
            $.ajax({
                url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename:"op_dispatchplan",controlsId:' + self.location_data.controllerId + ',lineId:' + self.location_data.line_id + ',id:' + options.id + '}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(options.layer_index);
                    var op = ret.respose[0];
                    op.controllerId = self.location_data.controllerId;
                    console.log(op);
                    var dialog = new batch_fix_switch_w(self, op);
                    dialog.appendTo($('body'));
                }
            });
        },
        manual_return_fn: function(options){
            var self = this;
            $.ajax({
                url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename:"op_busresource",controlsId:' + self.location_data.controllerId + ',lineId:' + self.location_data.line_id + ',id:' + options.id + '}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(options.layer_index);
                    var op = ret.respose[0];
                    op.controllerId = self.location_data.controllerId;
                    console.log(op);
                    var dialog = new manual_return_w(self, op);
                    dialog.appendTo($('body'));
                }
            });
        },
        driver_check_in_fn: function(options) {
            var self = this;
            $.ajax({
                url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename:"op_busresource",controlsId:' + self.location_data.controllerId + ',lineId:' + self.location_data.line_id + ',id:' + options.id + '}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(options.layer_index);
                    var op = ret.respose[0];
                    op.controllerId = self.location_data.controllerId;
                    console.log(op);
                    var dialog = new driver_check_in_w(self, op);
                    dialog.appendTo($('body'));
                }
            });
        },
        edit_the_vehicle_fn: function(options) {
            var self = this;
            $.ajax({
                url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename:"op_busresource",controlsId:' + self.location_data.controllerId + ',lineId:' + self.location_data.line_id + ',id:' + options.id + '}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(options.layer_index);
                    var op = ret.respose[0];
                    op.controllerId = self.location_data.controllerId;
                    console.log(op);
                    var dialog = new edit_the_vehicle_w(self, op);
                    dialog.appendTo($('body'));
                }
            });
        },
        error_state_fn: function(options) {
            var self = this;
            $.ajax({
                url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename:"op_busresource",controlsId:' + self.location_data.controllerId + ',lineId:' + self.location_data.line_id + ',id:' + options.id + '}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(options.layer_index);
                    var op = ret.respose[0];
                    op.controllerId = self.location_data.controllerId;
                    console.log(op);
                    var dialog = new error_state_w(self, op);
                    dialog.appendTo($('body'));
                }
            });
        },
        in_the_task_fn: function(options) {
            var self = this;
            $.ajax({
                url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename:"op_busresource",controlsId:' + self.location_data.controllerId + ',lineId:' + self.location_data.line_id + ',id:' + options.id + '}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(options.layer_index);
                    var op = ret.respose[0];
                    op.controllerId = self.location_data.controllerId;
                    console.log(op);
                    var dialog = new in_the_task_w(self, op);
                    dialog.appendTo($('body'));
                }
            });
        },
        immediate_scheduling_fn: function(options) {
            $.ajax({
                url: RESTFUL_URL + '/ltyop/resource/applyPlanById?apikey=71029270&params={id: "' + options.id + '"}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(options.layer_index);
                    layer.msg(ret.respose.text, { time: 1000, shade: 0.3 });
                }
            });
        },
        cancel_scheduling_fn: function(options) {
            $.ajax({
                url: RESTFUL_URL + '/ltyop/resource/cancelWorkPlan?apikey=71029270&params={id: "' + options.id + '"}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(options.layer_index);
                    layer.msg(ret.respose.text, { time: 1000, shade: 0.3 });
                }
            });
        },
        exit_operation_fn: function(options) {
            $.ajax({
                url: RESTFUL_URL + '/ltyop/resource/exitRun?apikey=71029270&params={id: "' + options.id + '"}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(options.layer_index);
                    layer.msg(ret.respose.text, { time: 1000, shade: 0.3 });
                }
            });
        },
        move_up_or_down_fn: function(options) {
            var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
            var active_tr = options.active_tr;
            var id = active_tr.attr("pid");
            var type = options.type;
            var prev_tr = active_tr.prev('tr.point');
            var next_tr = active_tr.next('tr.point');
            if (type == 1 && prev_tr.length == 0) {
                layer.msg("该计划已经是最前面的", { time: 1000, shade: 0.3 });
                return;
            }
            if (type == 2 && next_tr.length == 0) {
                layer.msg("该计划已经是最后面的", { time: 1000, shade: 0.3 });
                return;
            }
            $.ajax({
                url: RESTFUL_URL + '/ltyop/plan/movePlan?apikey=71029270&params={id: "' + id + '", type: "' + type + '"}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(layer_index);
                    layer.msg(ret.respose.text, { time: 1000, shade: 0.3 });
                    if (ret.result == 0) {
                        if (type == 1) {
                            prev_tr.before(active_tr);
                        } else {
                            next_tr.after(active_tr);
                        }
                    }
                }
            });
        },
        cancel_plan_fn: function(options) {
            var self = this;
            $.ajax({
                url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename:"op_dispatchplan",controlsId:' + self.location_data.controllerId + ',lineId:' + self.location_data.line_id + ',id:' + options.id + '}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(options.layer_index);
                    console.log(ret.respose[0]);
                    var dialog = new cancel_plan_w(self, ret.respose[0]);
                    dialog.appendTo($('body'));
                }
            });
        },
        fix_plan_fn: function(options) {
            var self = this;
            $.ajax({
                url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename:"op_dispatchplan",controlsId:' + self.location_data.controllerId + ',lineId:' + self.location_data.line_id + ',id:' + options.id + '}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(options.layer_index);
                    console.log(ret.respose[0]);
                    var dialog = new fix_plan_w(self, ret.respose[0]);
                    dialog.appendTo($('body'));
                }
            });
        },
        adjust_plan_fn: function(options){
            var self = this;
            $.ajax({
                url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename:"op_dispatchplan",controlsId:' + self.location_data.controllerId + ',lineId:' + self.location_data.line_id + ',id:' + options.id + '}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(options.layer_index);
                    console.log(ret.respose[0]);
                    var dialog = new adjust_plan_w(self, ret.respose[0]);
                    dialog.appendTo($('body'));
                }
            });
        },
        vehicle_search_autocomplete: function(data) {
            var self = this;
            var workDate = $(".customModal .modal-body").attr("workDate");
            var options = {
                event: data.evt,
                dateSearch: workDate,
                controlId: data.controlId,
                lineId: data.lineId
            };
            console.log(options);
            $(options.event).autocomplete({
                minLength: 0,
                width: options.event.offsetWidth,
                resultsClass: 'autocomplete_custom_model_class',
                autoFocus: true,
                source: function(request, response) {
                    var carNum = $(options.event).val();
                    if (carNum == "") {
                        return response([]);
                    }
                    $.ajax({
                        url: RESTFUL_URL + '/ltyop/dspSimulationDisPatchPlan/autocompleteBusResourcByControlIdNoCarState?apikey=71029270&params={dateSearch: "' + options.dateSearch + '" ,controlId: "' + options.controlId + '" ,lineId: "' + options.lineId + '" ,carNum: "' + carNum + '"}',
                        dataType: "json",
                        success: function(data) {
                            if (data.length > 0){
                                response(data);
                            }else{
                                response([]);
                            }
                        }
                    });
                },
                focus: function(event, ui) {
                    return false;
                },
                select: function(event, ui) {
                    $(options.event).val(ui.item.carNum);
                    $(".customModal .onBoardId").val(ui.item.onBoardId);
                    return false;
                }
            }).focus(function() {
                $(this).autocomplete("search");
            }).autocomplete("instance")._renderItem = function(ul, item) {
                return $("<li>")
                    .append("<div>" + item.carNum + "</div>")
                    .appendTo(ul);
            }
        },
        driver_search_autocomplete: function(data) {
            var workDate = $(".customModal .modal-body").attr("workDate");
            var gprsid = $(".customModal .modal-body").attr("gprsid");
            var options = {
                event: data.evt,
                dateSearch: workDate,
                controlId: data.controlId,
                gprsid: gprsid
            };
            console.log(options);
            $(options.event).autocomplete({
                minLength: 0,
                width: options.event.offsetWidth,
                resultsClass: 'autocomplete_custom_model_class',
                autoFocus: true,
                source: function(request, response) {
                    var workerId = $(options.event).val();
                    if (workerId == "") {
                        return response([]);
                    }
                    $.ajax({
                        url: RESTFUL_URL + '/ltyop/dspSimulationDisPatchPlan/autocompleteAttendanceByGprsid?apikey=71029270&params={dateSearch: "' + options.dateSearch + '" ,controlId: "' + options.controlId + '" ,gprsid: "' + options.gprsid + '" ,workerId: "' + workerId + '"}',
                        dataType: "json",
                        success: function(data) {
                            if (data.length > 0){
                                response(data);
                            }else{
                                response([]);
                            }
                        }
                    });
                },
                focus: function(event, ui) {
                    return false;
                },
                select: function(event, ui) {
                    // $(options.event).val(ui.item.workerId);
                    $(".customModal .workerIdSearch").val(ui.item.workerId);
                    $(".customModal .driverNameSearch").val(ui.item.driverName);
                    return false;
                },
            }).focus(function() {
                $(this).autocomplete("search");
            }).autocomplete("instance")._renderItem = function(ul, item) {
                return $("<li>")
                    .append("<div>" + item.workerId + "<span style='float:right;padding-right:5px;'>" + item.driverName + "</span></div>")
                    .appendTo(ul);
            }
        },
        trainman_search_autocomplete: function(data) {
            var workDate = $(".customModal .modal-body").attr("workDate");
            var gprsid = $(".customModal .modal-body").attr("gprsid");
            var options = {
                event: data.evt,
                dateSearch: workDate,
                controlId: data.controlId,
                gprsid: gprsid,
            };
            console.log(options);
            $(options.event).autocomplete({
                minLength: 0,
                width: options.event.offsetWidth,
                resultsClass: 'autocomplete_custom_model_class',
                autoFocus: true,
                source: function(request, response) {
                    var workerId = $(options.event).val();
                    if (workerId == "") {
                        return response([]);
                    }
                    $.ajax({
                        url: RESTFUL_URL + '/ltyop/dspSimulationDisPatchPlan/autocompleteTrainAttendanceByGprsid?apikey=71029270&params={dateSearch: "' + options.dateSearch + '" ,controlId: "' + options.controlId + '" ,gprsid: "' + options.gprsid + '" ,workerId: "' + workerId + '"}',
                        dataType: "json",
                        success: function(data) {
                            if (data.length > 0){
                                response(data);
                            }else{
                                response([]);
                            }
                        }
                    });
                },
                focus: function(event, ui) {
                    return false;
                },
                select: function(event, ui) {
                    // $(options.event).val(ui.item.workerId);
                    $(".customModal .trainSearch").val(ui.item.workerId);
                    $(".customModal .trainNameSearch").val(ui.item.driverName);
                    return false;
                }
            }).focus(function() {
                $(this).autocomplete("search");
            }).autocomplete("instance")._renderItem = function(ul, item) {
                return $("<li>")
                    .append("<div>" + item.workerId + "<span style='float:right;padding-right:5px;'>" + item.driverName + "</span></div>")
                    .appendTo(ul);
            };
        },
        planTime_search_autocomplete: function(data) {
            var modal_body = $(".customModal .modal-body")
            var options = {
                event: data.evt,
                id: modal_body.find(".pid").val(),
            };
            console.log(options);
            $(options.event).autocomplete({
                minLength: 0,
                width: options.event.offsetWidth,
                resultsClass: 'autocomplete_custom_model_class',
                autoFocus: true,
                source: function(request, response) {
                    var planRunTime = $(options.event).val();
                    if (planRunTime == ""){
                        return false;
                    }
                    $.ajax({
                        url: RESTFUL_URL + '/ltyop/plan/selectPlan?apikey=71029270&params={id: "' + options.id + '" ,planRunTime: "' + planRunTime + '"}',
                        dataType: "json",
                        success: function(data) {
                            if (data.result == 0){
                                response(data.respose);
                            }else{
                                response([]);
                            }
                        }
                    });
                },
                focus: function(event, ui) {
                    return false;
                },
                select: function(event, ui) {
                    $(options.event).val(new Date(ui.item.planRunTime).toTimeString().slice(0,5).replace("Inval", ""));
                    $(".customModal .switched_pid").val(ui.item.id);
                    $(".customModal .carNum_switched").val(ui.item.onBoardId);
                    $(".customModal .workerId_switched").val(ui.item.workerId);
                    $(".customModal .train_switched").val(ui.item.trainId);
                    return false;
                }
            }).focus(function() {
                $(this).autocomplete("search");
            }).autocomplete("instance")._renderItem = function(ul, item) {
                console.log(item.planRunTime);
                return $("<li>")
                    .append("<div>" + (new Date(item.planRunTime).toTimeString().slice(0,5).replace('Inval', '')) + "</div>")
                    .appendTo(ul);
            };
        },
        closeFn: function() {
            // 取消线路计划、车场、状态
            var package = {
                type: 2001,
                controlId: this.location_data.controllerId,
                open_modules: ["line_plan"]
            };
            if (websocket){
                websocket.send(JSON.stringify(package));
            }
            this.destroy();
        },
    });
    core.action_registry.add('lty_dispatch_desktop_widget.plan_display', plan_display);

    var bus_plan = Widget.extend({
        template: "vehicles_plan_template",
        init: function(parent, data) {
            this._super(parent);
            this.plan_data = data;
        },
        start: function() {
            var self = this;
            // 选中计划
            self.$(".content_tb").on("click", "tr.point", function() {
                $(this).addClass("active_tr").siblings().removeClass('active_tr');
            });

            // 增加icon浮层说明
            self.$(".content_tb .icon").hover(function() {
                var st = $(this).attr("st");
                var txt = "";
                if (st == 0) {
                    txt = "未发送";
                } else if (st == 1) {
                    txt = "已发送未处理";
                } else {
                    txt = "已发送已处理";
                }
                self.layer_f_index = layer.tips(txt, this);
            }, function() {
                layer.close(self.layer_f_index);
            });

            // 右键事件
            self.$(".content_tb").on("mousedown", ".point", function(e) {
                if (e.button == 2) {
                    var pid = $(this).attr("pid");
                    if (self.$(".set_" + pid).length > 0) {
                        return false;
                    }
                    $("body").click();
                    $(this).addClass("active_tr").addClass("right");
                    var parent_obj = $(this).parents(".plan_display")[0];
                    var y = e.clientY + 5 - parseInt(parent_obj.style.top.replace("px", ""));
                    if ((y + 48 * 8) > document.body.clientHeight) {
                        y -= 48 * 6;
                    }

                    var options = {
                        model: "bus_plan",
                        direction: $(this).attr("direction"),
                        pid: pid,
                        x: e.clientX + 5 - parseInt(parent_obj.style.left.replace("px", "")),
                        y: y - 60,
                        zIndex: 1,
                        data_list: [
                            { name: "发送计划到车辆", en_name: "send_plan_vehicles_bt" },
                            { name: "发送消息", en_name: "send_message_bt" },
                            { name: "添加计划", en_name: "add_plan_bt" },
                            { name: "手动发车", en_name: "manual_start_bt" },
                            { name: "修改计划", en_name: "fix_bt" },
                            { name: "批量更改车辆司机", en_name: "batch_change_drivers_bt" },
                            { name: "取消计划", en_name: "cancel_plan_bt" },
                            { name: "还原时间", en_name: "reduction_time_bt" },
                            { name: "电子地图", en_name: "electronic_map_bt" }
                        ]
                    }
                    var dialog = new plan_display_set(self, options);
                    dialog.appendTo(self.$(".section_plan_cont").parents(".plan_display"));
                    return false;
                }
            });
        }
    });

    var bus_yard = Widget.extend({
        template: "vehicles_yard_template",
        init: function(parent, data) {
            this._super(parent);
            this.yard_data = data;
        },
        start: function() {
            var self = this;
            // 增加icon浮层说明
            self.$(".content_tb .icon").hover(function() {
                var txt = "";
                var st = $(this).attr("st");
                if ($(this).hasClass("checkOut")) {
                    txt = (st == 1) ? '已签到' : '未签到'
                }else if ($(this).hasClass("runState")) {
                    txt = (st == 1) ? '在线' : '未在线'
                }else if ($(this).hasClass("carStateIdIcon")){
                    if (st == 1001){
                        txt = "正常";
                    }else if (st == 2003){
                        txt = "休息";
                    }else if (st == 1002){
                        txt = "故障";
                    }else if (st == 2006){
                        txt = "保养";
                    }else if (st == 2010){
                        txt = "空放";
                    }else if (st == 2005){
                        txt = "加油";
                    }else{
                        txt = "其它";
                    }
                }else if ($(this).hasClass("taskIcon")){
                    if (st == 1001){
                        txt = "进场包车开始";
                    }else if (st == 1002){
                        txt = "进场包车结束";
                    }else if (st == 1003){
                        txt = "进场加油开始";
                    }else if (st == 1004){
                        txt = "进场加油结束";
                    }else if (st == 1005){
                        txt = "进场修车开始";
                    }else if (st == 1006){
                        txt = "进场修车结束";
                    }else if (st == 1012){
                        txt = "进场下班，变机动";
                    }
                }
                self.layer_f_index = layer.tips(txt, this);
            }, function() {
                layer.close(self.layer_f_index);
            });
            // 右键事件
            self.$(".content_tb").on("mousedown", ".point", function(e) {
                if (e.button == 2) {
                    var pid = $(this).attr("pid");
                    if (self.$(".set_" + pid).length > 0) {
                        return false;
                    }
                    $("body").click();
                    $(this).addClass("active_tr").addClass("right");
                    var parent_obj = $(this).parents(".plan_display")[0];
                    var y = e.clientY + 5 - parseInt(parent_obj.style.top.replace("px", ""));
                    if ((y + 48 * 10) > document.body.clientHeight) {
                        y -= 48 * 7;
                    }
                    var options = {
                        model: "bus_yard",
                        direction: $(this).attr("direction"),
                        pid: pid,
                        x: e.clientX + 5 - parseInt(parent_obj.style.left.replace("px", "")),
                        y: y - 60,
                        zIndex: 1,
                        data_list: [
                            { name: "添加计划", en_name: "add_plan_bt" },
                            { name: "发送消息", en_name: "send_message_bt" },
                            { name: "司乘签到", en_name: "sign_in_bt" },
                            { name: "编辑车辆", en_name: "edit_vehicles_bt" },
                            { name: "立即排班", en_name: "immediately_scheduling_bt" },
                            { name: "取消排班", en_name: "cancel_scheduling_bt" },
                            { name: "退出运营", en_name: "exit_operation_bt" },
                            { name: "异常状态", en_name: "abnormal_state_bt" },
                            { name: "进场任务", en_name: "in_task_bt" },
                            { name: "电子地图", en_name: "electronic_map_bt" }
                        ]
                    }
                    var dialog = new plan_display_set(self, options);
                    dialog.appendTo(self.$(".section_plan_cont").parents(".plan_display"));
                    return false;
                }
            });
        }
    });

    var bus_transit = Widget.extend({
        template: "vehicles_transit_template",
        init: function(parent, data) {
            this._super(parent);
            this.transit_data = data;
        },
        start: function() {
            var self = this;
            // 增加icon浮层说明
            self.$(".content_tb .icon").hover(function() {
                var txt = "";
                var st = $(this).attr("st");
                if ($(this).hasClass("checkOut")) {
                    txt = (st == 1) ? '已签到' : '未签到'
                }else if ($(this).hasClass("runState")) {
                    txt = (st == 1) ? '在线' : '未在线'
                }else if ($(this).hasClass("carStateIdIcon")){
                    if (st == 1001){
                        txt = "正常";
                    }else if (st == 2003){
                        txt = "休息";
                    }else if (st == 1002){
                        txt = "故障";
                    }else if (st == 2006){
                        txt = "保养";
                    }else if (st == 2010){
                        txt = "空放";
                    }else if (st == 2005){
                        txt = "加油";
                    }else{
                        txt = "其它";
                    }
                }else if ($(this).hasClass("taskIcon")){
                    if (st == 1001){
                        txt = "进场包车开始";
                    }else if (st == 1002){
                        txt = "进场包车结束";
                    }else if (st == 1003){
                        txt = "进场加油开始";
                    }else if (st == 1004){
                        txt = "进场加油结束";
                    }else if (st == 1005){
                        txt = "进场修车开始";
                    }else if (st == 1006){
                        txt = "进场修车结束";
                    }else if (st == 1012){
                        txt = "进场下班，变机动";
                    }
                }
                self.layer_f_index = layer.tips(txt, this);
            }, function() {
                layer.close(self.layer_f_index);
            });
            // 右键事件
            self.$(".content_tb").on("mousedown", ".point", function(e) {
                if (e.button == 2) {
                    var pid = $(this).attr("pid");
                    if (self.$(".set_" + pid).length > 0) {
                        return false;
                    }
                    $("body").click();
                    $(this).addClass("active_tr").addClass("right");
                    var parent_obj = $(this).parents(".plan_display")[0];
                    var y = e.clientY + 5 - parseInt(parent_obj.style.top.replace("px", ""));
                    if ((y + 48 * 8) > document.body.clientHeight) {
                        y -= 48 * 6;
                    }
                    var options = {
                        model: "bus_transit",
                        direction: $(this).attr("direction"),
                        pid: pid,
                        x: e.clientX + 5 - parseInt(parent_obj.style.left.replace("px", "")),
                        y: y - 60,
                        zIndex: 1,
                        data_list: [
                            { name: "添加计划", en_name: "add_plan_bt" },
                            { name: "发送消息", en_name: "send_message_bt" },
                            { name: "手动返回", en_name: "manual_return_bt" },
                            { name: "司乘签到", en_name: "sign_in_bt" },
                            { name: "异常处理", en_name: "abnormal_deal_bt" },
                            { name: "异常状态", en_name: "abnormal_state_bt" },
                            { name: "手动签点", en_name: "manual_sign_bt " },
                            { name: "电子地图", en_name: "electronic_map_bt" }
                        ]
                    }
                    var dialog = new plan_display_set(self, options);
                    dialog.appendTo(self.$(".section_plan_cont").parents(".plan_display"));
                    return false;
                }
            });
        }
    });

    // 右键内容
    var plan_display_set = Widget.extend({
        template: "plan_display_set_template",
        init: function(parent, data) {
            this._super(parent);
            this.location_data = data;
        }
    });

    // 发送消息
    var send_short_msg_msg = Widget.extend({
        template: "send_short_msg_msg",
        init: function(parent, data, styleArgs) {
            this._super(parent);
            this.location_data = data;
            var styleModel = "";
            if (styleArgs){
                var styleArgs_list = styleArgs.split("_");
                styleModel = styleArgs_list[styleArgs_list.length-1];
            }
            this.styleModel = styleModel;
        },
        start: function() {
            this.load_fn();
            this.select_title = this.$el.find('.ready_info').val();
        },
        events: {
            'click .btn_confirm_lty': 'send_msg',
            'change .ready_info': 'ready_msg'
        },
        load_fn: function() {
            var self = this;
            self.$(".modal").on('hide.bs.modal', function() {
                self.destroy();
            });
            self.$(".modal").on('show.bs.modal', function() {
                $(this).css('display', 'block');
                // 是弹出框居中。。。
                var $modal_dialog = $(this).find('.modal-dialog');
                //获取可视窗口的高度
                var clientHeight = (document.body.clientHeight < document.documentElement.clientHeight) ? document.body.clientHeight : document.documentElement.clientHeight;
                //得到dialog的高度
                var dialogHeight = $modal_dialog.height();
                //计算出距离顶部的高度
                var m_top = (clientHeight - dialogHeight) / 2;
                $modal_dialog.css({ 'margin': m_top + 'px auto' });
            });
            self.$(".modal").modal({
                backdrop: 'static',
                keyboard: false
            });
        },
        ready_msg: function() {
            var val_select = this.$el.find('.ready_info');
            if (val_select.val() != this.select_title) {
                this.$el.find('.short_msg_text').val(val_select.val());
            } else {
                this.$el.find('.short_msg_text').val('');
            }
        },
        send_msg: function() {
            var self = this;
            var input_msg = self.$el.find('.short_msg_text').val();
            var laba_msg = self.$el.find('.laba').val();
            var is_check = 0;
            if (self.$el.find('.input-checkbox').is(':checked')) {
                is_check = 1;
            };
            var nodeIdArr = self.location_data.selfId;
            if (self.$el.find('.lineTypeCk').is(':checked')) {
                nodeIdArr = self.$el.find('.lineTypeCk').attr("line_id");
            };
            var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
            if (input_msg != '') {
                $.ajax({
                    //nodeIdArr是设备号
                    url: RESTFUL_URL + '/ltyop/msg/sendMsg2GW?apikey=71029270&params={input:"' + input_msg + '",nodeIdArr:"' + nodeIdArr + '",type:"note",isImport:' + is_check + ',msgChannel:' + laba_msg + '}',
                    type: 'post',
                    dataType: 'json',
                    data: {},
                    success: function(ret) {
                        layer.close(layer_index);
                        layer.msg(ret.respose.text, { time: 1000, shade: 0.3 });
                        if (ret.result == 0) {
                            self.$el.find('.short_msg_content').html('已发送：' + input_msg);
                            self.$el.find('.short_msg_text').val("");
                        }
                    }
                });
            } else {
                layer.msg('请输入短信内容或选择预设短信', { time: 0, shade: 0.3 });
            }
        }
    });

    // 添加计划
    var add_plan_w = Widget.extend({
        template: 'plan_display_add_plan_template',
        init: function(parent, data) {
            this._super(parent);
            this.set_data = data;
        },
        start: function() {
            this.modal_fn();
        },
        modal_fn: function() {
            var self = this;
            self.$el.on('hide.bs.modal', function() {
                self.destroy();
            });
            self.$el.on('show.bs.modal', function() {
                $(this).css('display', 'block');
                // 是弹出框居中。。。
                var $modal_dialog = $(this).find('.modal-dialog');
                //获取可视窗口的高度
                var clientHeight = (document.body.clientHeight < document.documentElement.clientHeight) ? document.body.clientHeight : document.documentElement.clientHeight;
                //得到dialog的高度
                var dialogHeight = $modal_dialog.height();
                //计算出距离顶部的高度
                var m_top = (clientHeight - dialogHeight) / 2;
                $modal_dialog.css({ 'margin': m_top + 'px auto' });
            });
            self.$el.modal({
                backdrop: 'static',
                keyboard: false
            });

            self.$(".planTime input:eq(1)").focus();

            // 提交
            self.$('.btn-primary').on('click', function() {
                self.submit_fn();
            });
        },
        submit_fn: function(isConfirm) {
            var self = this;
            var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
            var confObj = self.$('.modal-body table');
            var params = {
                id: self.set_data.id,
                planTime: confObj.find(".planTime input:eq(0)").val() + ":" + confObj.find(".planTime input:eq(1)").val(),
                planCount: confObj.find(".planCount").val(),
                lineId: confObj.find(".line").val(),
                onBoardId: confObj.find(".onBoardId").val(),
                carNum: confObj.find(".carNum").val(),
                planKm: confObj.find(".planKm").val(),
                direction: confObj.find(".direction").val(),
                driverName: confObj.find(".driverName").val(),
                workerId: confObj.find(".workerId").val(),
                trainId: confObj.find(".train").val(),
                trainName: confObj.find(".trainName").val(),
                addType: confObj.find(".addType").val(),
                addReasonId: confObj.find(".addReason").val(),
                remark: confObj.find(".remark").val(),
                isConfirm: isConfirm || 0
            };
            $.ajax({
                url: RESTFUL_URL + '/ltyop/plan/addPlan?apikey=71029270&params=' + JSON.stringify(params),
                type: 'post',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(layer_index);
                    if (ret.result == 2) {
                        layer.confirm(ret.respose.text, {
                            btn: ['确认', '取消'],
                            title: '消息'
                        }, function() {
                            self.submit_fn(1);
                        });
                        return false;
                    }
                    layer.msg(ret.respose.text, { time: 1000, shade: 0.3 });
                    if (ret.result == 0) {
                        self.$('.btn-default').click();
                    }
                }
            });
        }
    });

    // 手动发车
    var manual_start_w = Widget.extend({
        template: 'manual_start_template',
        init: function(parent, data) {
            this._super(parent);
            this.set_data = data;
        },
        start: function() {
            this.modal_fn();
        },
        modal_fn: function() {
            var self = this;
            self.$el.on('hide.bs.modal', function() {
                self.destroy();
            });
            self.$el.on('show.bs.modal', function() {
                $(this).css('display', 'block');
                // 是弹出框居中。。。
                var $modal_dialog = $(this).find('.modal-dialog');
                //获取可视窗口的高度
                var clientHeight = (document.body.clientHeight < document.documentElement.clientHeight) ? document.body.clientHeight : document.documentElement.clientHeight;
                //得到dialog的高度
                var dialogHeight = $modal_dialog.height();
                //计算出距离顶部的高度
                var m_top = (clientHeight - dialogHeight) / 2;
                $modal_dialog.css({ 'margin': m_top + 'px auto' });
            });
            self.$el.modal({
                backdrop: 'static',
                keyboard: false
            });

            self.$(".realRunTime").focus();

            // 提交
            self.$('.btn-primary').on('click', function() {
                self.submit_fn();
            });
        },
        submit_fn: function() {
            var self = this;
            var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
            var confObj = self.$('.modal-body table');
            var params = {
                id: self.set_data.id,
                onBoardId: confObj.find(".onBoardId").val(),
                realRunTime: confObj.find(".realRunTime").val(),
                lineId: confObj.find(".line").val(),
                abnormalType: confObj.find(".abnormal").val()
            };
            $.ajax({
                url: RESTFUL_URL + '/ltyop/plan/autoOutPlan?apikey=71029270&params=' + JSON.stringify(params),
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(layer_index);
                    layer.msg(ret.respose.text, { time: 1000, shade: 0.3 });
                    if (ret.result == 0) {
                        self.$('.btn-default').click();
                    }
                }
            });
        }
    });

    // 手动返回
    var manual_return_w = Widget.extend({
        template: 'manual_return_template',
        init: function(parent, data, styleArgs) {
            this._super(parent);
            this.set_data = data;
            var styleModel = "";
            if (styleArgs){
                var styleArgs_list = styleArgs.split("_");
                styleModel = styleArgs_list[styleArgs_list.length-1];
            }
            this.styleModel = styleModel;
        },
        start: function() {
            this.modal_fn();
        },
        modal_fn: function() {
            var self = this;
            self.$el.on('hide.bs.modal', function() {
                self.destroy();
            });
            self.$el.on('show.bs.modal', function() {
                $(this).css('display', 'block');
                // 是弹出框居中。。。
                var $modal_dialog = $(this).find('.modal-dialog');
                //获取可视窗口的高度
                var clientHeight = (document.body.clientHeight < document.documentElement.clientHeight) ? document.body.clientHeight : document.documentElement.clientHeight;
                //得到dialog的高度
                var dialogHeight = $modal_dialog.height();
                //计算出距离顶部的高度
                var m_top = (clientHeight - dialogHeight) / 2;
                $modal_dialog.css({ 'margin': m_top + 'px auto' });
            });
            self.$el.modal({
                backdrop: 'static',
                keyboard: false
            });

            self.$(".realRunTime").focus();

            // 提交
            self.$('.btn-primary').on('click', function() {
                self.submit_fn();
            });
        },
        submit_fn: function() {
            var self = this;
            var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
            var confObj = self.$('.modal-body table');
            var params = {
                id: self.set_data.id,
                onBoardId: confObj.find(".onBoardId").val(),
                realReachTime: confObj.find(".realReachTime").val(),
                direction: confObj.find(".retrun_direction").val(),
                opType: confObj.find(".opType").val(),
                type: confObj.find(".type").val()
            };
            $.ajax({
                url: RESTFUL_URL + '/ltyop/resource/handBackBusResourceOp?apikey=71029270&params=' + JSON.stringify(params),
                type: 'post',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(layer_index);
                    layer.msg(ret.respose.text, { time: 1000, shade: 0.3 });
                    if (ret.result == 0) {
                        self.$('.btn-default').click();
                    }
                }
            });
        }
    });

    // 取消计划
    var cancel_plan_w = Widget.extend({
        template: 'plan_display_cancel_plan_template',
        init: function(parent, data) {
            this._super(parent);
            this.set_data = data;
        },
        start: function() {
            this.modal_fn();
        },
        modal_fn: function() {
            var self = this;
            self.$el.on('hide.bs.modal', function() {
                self.destroy();
            });
            self.$el.on('show.bs.modal', function() {
                $(this).css('display', 'block');
                // 是弹出框居中。。。
                var $modal_dialog = $(this).find('.modal-dialog');
                //获取可视窗口的高度
                var clientHeight = (document.body.clientHeight < document.documentElement.clientHeight) ? document.body.clientHeight : document.documentElement.clientHeight;
                //得到dialog的高度
                var dialogHeight = $modal_dialog.height();
                //计算出距离顶部的高度
                var m_top = (clientHeight - dialogHeight) / 2;
                $modal_dialog.css({ 'margin': m_top + 'px auto' });
            });
            self.$el.modal({
                backdrop: 'static',
                keyboard: false
            });

            self.$('.modal-body').on("click", ".selectType .ckIcon", function() {
                $(this).addClass("active").siblings().removeClass('active');
            });

            self.$(".planTime").focus();

            // 提交
            self.$('.btn-primary').on('click', function() {
                self.submit_fn();
            });
        },
        submit_fn: function() {
            var self = this;
            var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
            var confObj = self.$('.modal-body table');
            var params = {
                id: self.set_data.id,
                cancelReasonId: confObj.find(".addReason").val(),
                remark: confObj.find(".remark").val(),
                averageType: confObj.find(".selectType .active").attr("typename"),
                avgBegTime: confObj.find(".avgBegTime").val(),
                avgModeCount: confObj.find(".avgModeCount").val(),
                forwardModeCount: confObj.find(".forwardModeCount").val(),
                forwardInterval: confObj.find(".forwardInterval").val()

            };
            $.ajax({
                url: RESTFUL_URL + '/ltyop/plan/cancelPlan?apikey=71029270&params=' + JSON.stringify(params),
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(layer_index);
                    layer.msg(ret.respose.text, { time: 1000, shade: 0.3 });
                    if (ret.result == 0) {
                        self.$('.btn-default').click();
                    }
                }
            });
        }
    });

    // 修改计划
    var fix_plan_w = Widget.extend({
        template: 'plan_display_fix_plan_template',
        init: function(parent, data) {
            this._super(parent);
            this.set_data = data;
        },
        start: function() {
            this.modal_fn();
        },
        modal_fn: function() {
            var self = this;
            self.$el.on('hide.bs.modal', function() {
                self.destroy();
            });
            self.$el.on('show.bs.modal', function() {
                $(this).css('display', 'block');
                // 是弹出框居中。。。
                var $modal_dialog = $(this).find('.modal-dialog');
                //获取可视窗口的高度
                var clientHeight = (document.body.clientHeight < document.documentElement.clientHeight) ? document.body.clientHeight : document.documentElement.clientHeight;
                //得到dialog的高度
                var dialogHeight = $modal_dialog.height();
                //计算出距离顶部的高度
                var m_top = (clientHeight - dialogHeight) / 2;
                $modal_dialog.css({ 'margin': m_top + 'px auto' });
            });
            self.$el.modal({
                backdrop: 'static',
                keyboard: false
            });

            self.$('.modal-body').on("click", ".selectType .ckIcon", function() {
                $(this).addClass("active").siblings().removeClass('active');
            });

            self.$(".planTime").focus();

            // 提交
            self.$('.btn-primary').on('click', function() {
                self.submit_fn();
            });
        },
        submit_fn: function(isConfirm) {
            var self = this;
            var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
            var confObj = self.$('.modal-body table');
            var params = {
                id: self.set_data.id,
                planTime: confObj.find(".planTime").val(),
                planCount: confObj.find(".planCount").val(),
                lineId: confObj.find(".line").val(),
                runGprsId: confObj.find(".runGprs").val(),
                onBoardId: confObj.find(".onBoardId").val(),
                carNum: confObj.find(".carNum").val(),
                planKm: confObj.find(".planKm").val(),
                direction: confObj.find(".direction").val(),
                driverName: confObj.find(".driverName").val(),
                workerId: confObj.find(".workerId").val(),
                trainId: confObj.find(".train").val(),
                trainName: confObj.find(".trainName").val(),
                addType: confObj.find(".addType").val(),
                addReasonId: confObj.find(".addReasonId").val(),
                isBatchChangePlan: confObj.find(".selectType .active").attr("typename"),
                changePlanCount: confObj.find(".changePlanCount").val(),
                changeInterval: confObj.find(".changeInterval").val(),
                startTime: confObj.find(".startTime").val(),
                endTime: confObj.find(".endTime").val(),
                isConfirm: isConfirm || 0
            };
            $.ajax({
                url: RESTFUL_URL + '/ltyop/plan/updatePlan?apikey=71029270&params=' + JSON.stringify(params),
                type: 'put',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(layer_index);
                    if (ret.result == 2) {
                        layer.confirm(ret.respose.text, {
                            btn: ['确认', '取消'],
                            title: '消息'
                        }, function() {
                            self.submit_fn(1);
                        });
                        return false;
                    }
                    layer.msg(ret.respose.text, { time: 1000, shade: 0.3 });
                    if (ret.result == 0) {
                        self.$('.btn-default').click();
                    }
                }
            });
        }
    });

    // 调换计划
    var adjust_plan_w = Widget.extend({
        template: 'adjust_plan_template',
        init: function(parent, data) {
            this._super(parent);
            this.set_data = data;
        },
        start: function() {
            this.modal_fn();
        },
        modal_fn: function() {
            var self = this;
            self.$el.on('hide.bs.modal', function() {
                self.destroy();
            });
            self.$el.on('show.bs.modal', function() {
                $(this).css('display', 'block');
                // 是弹出框居中。。。
                var $modal_dialog = $(this).find('.modal-dialog');
                //获取可视窗口的高度
                var clientHeight = (document.body.clientHeight < document.documentElement.clientHeight) ? document.body.clientHeight : document.documentElement.clientHeight;
                //得到dialog的高度
                var dialogHeight = $modal_dialog.height();
                //计算出距离顶部的高度
                var m_top = (clientHeight - dialogHeight) / 2;
                $modal_dialog.css({ 'margin': m_top + 'px auto' });
            });
            self.$el.modal({
                backdrop: 'static',
                keyboard: false
            });

            self.$(".planTimeS").focus();

            // 提交
            self.$('.btn-primary').on('click', function() {
                self.submit_fn();
            });
        },
        submit_fn: function() {
            var self = this;
            var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
            var confObj = self.$('.modal-body table');
            var params = {
                planId_1: self.set_data.id,
                planId_2: confObj.find(".switched_pid").val()
            };
            $.ajax({
                url: RESTFUL_URL + '/ltyop/plan/exchangePlan?apikey=71029270&params=' + JSON.stringify(params),
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(layer_index);
                    layer.msg(ret.respose.text, { time: 1000, shade: 0.3 });
                    if (ret.result == 0) {
                        self.$('.btn-default').click();
                    }
                }
            });
        }
    });

    // 批量更改车辆或司机
    var batch_fix_switch_w = Widget.extend({
        template: 'batch_fix_switch_template',
        init: function(parent, data) {
            this._super(parent);
            this.set_data = data;
        },
        start: function() {
            this.modal_fn();
        },
        modal_fn: function() {
            var self = this;
            self.$el.on('hide.bs.modal', function() {
                self.destroy();
            });
            self.$el.on('show.bs.modal', function() {
                $(this).css('display', 'block');
                // 是弹出框居中。。。
                var $modal_dialog = $(this).find('.modal-dialog');
                //获取可视窗口的高度
                var clientHeight = (document.body.clientHeight < document.documentElement.clientHeight) ? document.body.clientHeight : document.documentElement.clientHeight;
                //得到dialog的高度
                var dialogHeight = $modal_dialog.height();
                //计算出距离顶部的高度
                var m_top = (clientHeight - dialogHeight) / 2;
                $modal_dialog.css({ 'margin': m_top + 'px auto' });
            });
            self.$el.modal({
                backdrop: 'static',
                keyboard: false
            });

            self.$('.modal-body').on("click", ".mode_type a", function() {
                $(this).addClass("active").siblings().removeClass('active');
            });
            // 提交
            self.$('.btn-primary').on('click', function() {
                self.submit_fn();
            });
        },
        submit_fn: function() {
            var self = this;
            var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
            var confObj = self.$('.modal-body table');
            var params = {
                controlId: self.set_data.controllerId,
                planId_1: self.set_data.id,
                type: self.$(".mode_type .active").attr("name"),
                onBoardId: confObj.find(".onBoardId").val(),
                selfId: confObj.find(".carNum").val(),
                workerId: confObj.find(".workerId").val(),
                driverName: confObj.find(".driverName").val(),
                startTime: confObj.find(".startTime").val(),
                endTime: confObj.find(".endTime").val(),
            };
            console.log(params);
            $.ajax({
                url: RESTFUL_URL + '/ltyop/plan/batchChangeDriverCar?apikey=71029270&params=' + JSON.stringify(params),
                type: 'post',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(layer_index);
                    layer.msg(ret.respose.text, { time: 1000, shade: 0.3 });
                    if (ret.result == 0) {
                        self.$('.btn-default').click();
                    }
                }
            });
        }
    });

    // 司乘签到
    var driver_check_in_w = Widget.extend({
        template: 'driver_check_in_template',
        init: function(parent, data, styleArgs) {
            this._super(parent, styleArgs);
            this.set_data = data;
            var styleModel = "";
            if (styleArgs){
                var styleArgs_list = styleArgs.split("_");
                styleModel = styleArgs_list[styleArgs_list.length-1];
            }
            this.styleModel = styleModel;
        },
        start: function() {
            this.modal_fn();
        },
        modal_fn: function() {
            var self = this;
            self.$el.on('hide.bs.modal', function() {
                self.destroy();
            });
            self.$el.on('show.bs.modal', function() {
                $(this).css('display', 'block');
                // 是弹出框居中。。。
                var $modal_dialog = $(this).find('.modal-dialog');
                //获取可视窗口的高度
                var clientHeight = (document.body.clientHeight < document.documentElement.clientHeight) ? document.body.clientHeight : document.documentElement.clientHeight;
                //得到dialog的高度
                var dialogHeight = $modal_dialog.height();
                //计算出距离顶部的高度
                var m_top = (clientHeight - dialogHeight) / 2;
                $modal_dialog.css({ 'margin': m_top + 'px auto' });
            });
            self.$el.modal({
                backdrop: 'static',
                keyboard: false
            });

            self.$(".workTime").focus();

            // 提交
            self.$('.btn-primary').on('click', function() {
                self.submit_fn($(this).attr("name"));
            });
        },
        submit_fn: function(name) {
            var self = this;
            var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
            var confObj = self.$('.modal-body table');
            var params = {
                id: self.set_data.id,
                onBoardId: confObj.find(".onBoardId").val(),
                workerId: confObj.find(".workerId").val(),
                driverName: confObj.find(".driverName").val(),
                trainId: confObj.find(".train").val(),
                trainName: confObj.find(".trainName").val(),
                workTime: confObj.find(".workTime").val(),
                opType: name
            };
            $.ajax({
                url: RESTFUL_URL + '/ltyop/resource/busResourceOpAttendance?apikey=71029270&params=' + JSON.stringify(params),
                type: 'post',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(layer_index);
                    layer.msg(ret.respose.text, { time: 1000, shade: 0.3 });
                    if (ret.result == 0) {
                        self.$('.btn-default').click();
                    }
                }
            });
        }
    });

    // 编辑车辆
    var edit_the_vehicle_w = Widget.extend({
        template: 'edit_the_vehicle_template',
        init: function(parent, data) {
            this._super(parent);
            this.set_data = data;
        },
        start: function() {
            this.modal_fn();
        },
        modal_fn: function() {
            var self = this;
            self.$el.on('hide.bs.modal', function() {
                self.destroy();
            });
            self.$el.on('show.bs.modal', function() {
                $(this).css('display', 'block');
                // 是弹出框居中。。。
                var $modal_dialog = $(this).find('.modal-dialog');
                //获取可视窗口的高度
                var clientHeight = (document.body.clientHeight < document.documentElement.clientHeight) ? document.body.clientHeight : document.documentElement.clientHeight;
                //得到dialog的高度
                var dialogHeight = $modal_dialog.height();
                //计算出距离顶部的高度
                var m_top = (clientHeight - dialogHeight) / 2;
                $modal_dialog.css({ 'margin': m_top + 'px auto' });
            });
            self.$el.modal({
                backdrop: 'static',
                keyboard: false
            });

            self.$(".onWorkTime").focus();

            // 提交
            self.$('.btn-primary').on('click', function() {
                self.submit_fn();
            });
        },
        submit_fn: function(name) {
            var self = this;
            var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
            var confObj = self.$('.modal-body table');
            var params = {
                id: self.set_data.id,
                onBoardId: confObj.find(".onBoardId").val(),
                runGprsId: confObj.find(".runGprs").val(),
                direction: confObj.find(".direction").val(),
                onWorkTime: confObj.find(".onWorkTime").val(),
                realCount: confObj.find(".realCount").val(),
            };
            $.ajax({
                url: RESTFUL_URL + '/ltyop/resource/editBusResource?apikey=&params=' + JSON.stringify(params),
                type: 'post',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(layer_index);
                    layer.msg(ret.respose.text, { time: 1000, shade: 0.3 });
                    if (ret.result == 0) {
                        self.$('.btn-default').click();
                    }
                }
            });
        }
    });

    //异常状态
    var error_state_w = Widget.extend({
        template: 'error_state_template',
        init: function(parent, data, styleArgs) {
            this._super(parent, styleArgs);
            this.set_data = data;
            var styleModel = "";
            if (styleArgs){
                var styleArgs_list = styleArgs.split("_");
                styleModel = styleArgs_list[styleArgs_list.length-1];
            }
            this.styleModel = styleModel;
        },
        start: function() {
            this.modal_fn();
        },
        modal_fn: function() {
            var self = this;
            self.$el.on('hide.bs.modal', function() {
                self.destroy();
            });
            self.$el.on('show.bs.modal', function() {
                $(this).css('display', 'block');
                // 是弹出框居中。。。
                var $modal_dialog = $(this).find('.modal-dialog');
                //获取可视窗口的高度
                var clientHeight = (document.body.clientHeight < document.documentElement.clientHeight) ? document.body.clientHeight : document.documentElement.clientHeight;
                //得到dialog的高度
                var dialogHeight = $modal_dialog.height();
                //计算出距离顶部的高度
                var m_top = (clientHeight - dialogHeight) / 2;
                $modal_dialog.css({ 'margin': m_top + 'px auto' });
            });
            self.$el.modal({
                backdrop: 'static',
                keyboard: false
            });
            self.$('.modal-body').on("click", ".selectType .ckIcon", function() {
                self.$(".selectType .ckIcon").removeClass("active");
                $(this).addClass("active").siblings();
                // $(this).toggleClass("active")  //gy切换active 
            });
            // 提交
            self.$('.btn-primary').on('click', function() {
                self.submit_fn();
            });
        },
        submit_fn: function() {
            var self = this;
            var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
            var confObj = self.$('.modal-body ul');
            var params = {
                onBoardId: self.set_data.onBoardId,
                state: self.$(".selectType .active").attr("name")
            };
            console.log(params);
            $.ajax({
                url: RESTFUL_URL + '/ltyop/resource/updateBusResourceState?apikey=71029270&params=' + JSON.stringify(params),
                type: 'post',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(layer_index);
                    layer.msg(ret.respose.text, { time: 1000, shade: 0.3 });
                    if (ret.result == 0) {
                        self.$('.btn-default').click();
                    }
                }
            });
        }
    });

    //进场任务
    var in_the_task_w = Widget.extend({
        template: 'in_the_task_template',
        init: function(parent, data, styleArgs) {
            this._super(parent);
            this.set_data = data;
            var styleModel = "";
            if (styleArgs){
                var styleArgs_list = styleArgs.split("_");
                styleModel = styleArgs_list[styleArgs_list.length-1];
            }
            this.styleModel = styleModel;
        },
        start: function() {
            this.modal_fn();
        },
        modal_fn: function() {
            var self = this;
            self.$el.on('hide.bs.modal', function() {
                self.destroy();
            });
            self.$el.on('show.bs.modal', function() {
                $(this).css('display', 'block');
                // 是弹出框居中。。。
                var $modal_dialog = $(this).find('.modal-dialog');
                //获取可视窗口的高度
                var clientHeight = (document.body.clientHeight < document.documentElement.clientHeight) ? document.body.clientHeight : document.documentElement.clientHeight;
                //得到dialog的高度
                var dialogHeight = $modal_dialog.height();
                //计算出距离顶部的高度
                var m_top = (clientHeight - dialogHeight) / 2;
                $modal_dialog.css({ 'margin': m_top + 'px auto' });
            });
            self.$el.modal({
                backdrop: 'static',
                keyboard: false
            });
            self.$('.modal-body').on("click", ".selectType .ckIcon", function() {
                self.$(".selectType .ckIcon").removeClass("active");
                $(this).addClass("active").siblings();
            });
            // 提交
            self.$('.btn-primary').on('click', function() {
                self.submit_fn();
            });
        },
        submit_fn: function(name) {
            var self = this;
            var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
            var confObj = self.$('.modal-body table');
            var params = {
                onBoardId: self.set_data.onBoardId,
                taskCode: self.$(".selectType .active").attr("name")
            };
            $.ajax({
                url: RESTFUL_URL + '/ltyop/resource/procDevTask?apikey=71029270&params=' + JSON.stringify(params),
                type: 'post',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(layer_index);
                    layer.msg(ret.respose.text, { time: 1000, shade: 0.3 });
                    if (ret.result == 0) {
                        self.$('.btn-default').click();
                    }
                }
            });
        }
    });

    // return plan_display;
    var exports = {
        plan_display: plan_display,
        manual_return_w: manual_return_w,
        driver_check_in_w: driver_check_in_w,
        error_state_w: error_state_w,
        in_the_task_w: in_the_task_w,
        send_short_msg_msg: send_short_msg_msg
    }

    return exports;
});