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
                direction: 0,
                data_list: [
                    {
                        id: "plan_1",
                        sendToScreen: 0,
                        sendToBus: 1,
                        planRunTime: new Date().getTime(),
                        planReachTime: new Date().getTime(),
                        selfId: "655",
                        driverName: "刘德华",
                        planState: "0",
                        direction: 0
                    }
                ]
            };
            var uplink_yard = {
                direction: 0,
                inField: 1,
                data_list: [
                    {
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
                    }
                ]
            };
            var uplink_transit = {
                direction: 0,
                inField: 0,
                data_list: [
                    {
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
                    }
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

            // 订阅线路计划、车场、状态
            var package = {
                type: 1000,
                open_modules: ["dispatch-line_plan-"+this.location_data.controllerId, "dispatch-line_park-"+this.location_data.controllerId, "dispatch-line_online-"+this.location_data.controllerId],
                msgId: Date.parse(new Date())
            };
            websocket.send(JSON.stringify(package));

            this.load_plan();
        },
        load_plan: function(){
            var self = this;
            $.ajax({
                url: 'http://202.104.136.228:8888/ltyop/planData/query?apikey=71029270&params={tablename:"op_dispatchplan",controlsId:2032,gprsId:161}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret){
                    self.uplink_plan = {
                        direction: 0,
                        data_list: ret.respose
                    };
                    self.down_plan = {
                        direction: 1,
                        data_list: ret.respose
                    };
                    $.ajax({
                        url: 'http://202.104.136.228:8888/ltyop/planData/query?apikey=71029270&params={tablename:"op_busresource",controlsId:2032,gprsId:161}',
                        type: 'get',
                        dataType: 'json',
                        data: {},
                        success: function(data){
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
        cont_info: function(){
            new bus_plan(this, this.uplink_plan).appendTo(this.$(".plan_group"));
            new bus_yard(this, this.uplink_yard).appendTo(this.$(".plan_group"));
            new bus_transit(this, this.uplink_transit).appendTo(this.$(".plan_group"));
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

            // 计划右键菜单相关事件
            self.bus_plan_set_fn();

            // 车场右键菜单相关事件
            self.bus_yard_set_fn();

            // 在途右键菜单相关事件
            self.bus_transit_set_fn();
        },
        bus_plan_set_fn: function(){
            var self = this;
            // 发送计划都车辆
            self.$(".plan_display").on("click", ".plan_display_set[model='bus_plan'] li.send_plan_vehicles_bt", function(){
                var layer_index = layer.msg("请求中，请稍后...", {shade: 0.3, time: 0});
                var obj = $(this).parents(".plan_display_set");
                var id = obj.attr("plan_pid");
                var direction = obj.attr("direction");
                $.ajax({
                    url: 'http://10.1.254.122:8080/ltyop/plan/sendPlanToBus?apikey=71029270&params={id: "'+id+'"}',
                    type: 'get',
                    dataType: 'json',
                    data: {},
                    success: function(ret){
                        layer.close(layer_index);
                        if (ret.result == 0){
                            //这里特别说明一下，由于请求成功后，后台会立即触发一次推送websoket，页面状态更新这里将不在做处理
                        }
                        layer.msg(ret.respose.text, {time: 2000, shade: 0.3});
                    }
                });
            });

            // 计划车辆还原时间
            self.$(".plan_display").on("click", ".plan_display_set[model='bus_plan'] li.reduction_time_bt", function(){
                var layer_index = layer.msg("请求中，请稍后...", {shade: 0.3, time: 0});
                var obj = $(this).parents(".plan_display_set");
                var id = obj.attr("plan_pid");
                $.ajax({
                    url: 'http://10.1.254.122:8080/ltyop/plan/restoreTime?apikey=71029270&params={id: "'+id+'"}',
                    type: 'get',
                    dataType: 'json',
                    data: {},
                    success: function(ret){
                        layer.close(layer_index);
                        if (ret.result == 0){
                            //这里特别说明一下，由于请求成功后，后台会立即触发一次推送websoket，页面状态更新这里将不在做处理
                        }
                        layer.msg(ret.respose.text, {time: 2000, shade: 0.3});
                    }
                });
            });
        },
        bus_yard_set_fn: function(){
            var self = this;
            // 立即排班
            self.$(".plan_display").on("click", ".plan_display_set[model='bus_yard'] li.immediately_scheduling_bt", function(){
                var layer_index = layer.msg("请求中，请稍后...", {shade: 0.3, time: 0});
                var obj = $(this).parents(".plan_display_set");
                var id = obj.attr("plan_pid");
                var direction = obj.attr("direction");
                $.ajax({
                    url: 'http://10.1.254.122:8080/ltyop/resource/applyPlanById?apikey=71029270&params={id: "'+id+'"}',
                    type: 'get',
                    dataType: 'json',
                    data: {},
                    success: function(ret){
                        layer.close(layer_index);
                        layer.msg(ret.respose.text, {time: 2000, shade: 0.3});
                    }
                });
            });

            // 取消排班
            self.$(".plan_display").on("click", ".plan_display_set[model='bus_yard'] li.cancel_scheduling_bt", function(){
                var layer_index = layer.msg("请求中，请稍后...", {shade: 0.3, time: 0});
                var obj = $(this).parents(".plan_display_set");
                var id = obj.attr("plan_pid");
                $.ajax({
                    url: 'http://10.1.254.122:8080/ltyop/resource/cancelWorkPlan?apikey=71029270&params={id: "'+id+'"}',
                    type: 'get',
                    dataType: 'json',
                    data: {},
                    success: function(ret){
                        layer.close(layer_index);
                        layer.msg(ret.respose.text, {time: 2000, shade: 0.3});
                    }
                });
            });

            // 退出运营
            self.$(".plan_display").on("click", ".plan_display_set[model='bus_yard'] li.exit_operation_bt", function(){
                var layer_index = layer.msg("请求中，请稍后...", {shade: 0.3, time: 0});
                var obj = $(this).parents(".plan_display_set");
                var id = obj.attr("plan_pid");
                $.ajax({
                    url: 'http://10.1.254.122:8080/ltyop/resource/exitRun?apikey=71029270&params={id: "'+id+'"}',
                    type: 'get',
                    dataType: 'json',
                    data: {},
                    success: function(ret){
                        layer.close(layer_index);
                        layer.msg(ret.respose.text, {time: 2000, shade: 0.3});
                    }
                });
            });
        },
        bus_transit_set_fn: function(){
            var self = this;
        },
        closeFn: function(){
            // 取消线路计划、车场、状态
            var package = {
                type: 1001,
                open_modules: ["dispatch-line_plan-"+this.location_data.controllerId, "dispatch-line_park-"+this.location_data.controllerId, "dispatch-line_online-"+this.location_data.controllerId],
                msgId: Date.parse(new Date())
            };
            websocket.send(JSON.stringify(package));
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

            // 增加icon浮层说明
            self.$(".content_tb .icon").hover(function(){
                var txt = ($(this).attr("st")==1)?'已发送':'未发送'
                self.layer_f_index = layer.tips(txt, this);
            },function(){
                layer.close(self.layer_f_index);
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
                    var y = e.clientY + 5 - parseInt(parent_obj.style.top.replace("px",""));
                    if ((y + 48*8)>document.body.clientHeight){
                        y -= 48*6;
                    }

                    var options = {
                        model: "bus_plan",
                        direction: $(this).attr("direction"),
                        pid: pid,
                        x: e.clientX + 5 - parseInt(parent_obj.style.left.replace("px","")),
                        y: y,
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
                    dialog.appendTo(self.$(".section_plan_cont").parents(".plan_display"));
                    return false;
                }
            });
        },
        move_fn: function(active_tr, type){
            var layer_index = layer.msg("请求中，请稍后...", {shade: 0.3, time: 0});
            var id = active_tr.attr('pid');
            var prev_tr = active_tr.prev ('tr.point');
            var next_tr = active_tr.next ('tr.point');
            if (type == 1 && prev_tr.length == 0){
                layer.msg("该计划已经是最前面的", {time: 1000, shade: 0.3});
                return;
            }
            if (type == 2 && next_tr.length == 0){
                layer.msg("该计划已经是最后面的", {time: 1000, shade: 0.3});
                return;
            }
            $.ajax({
                url: 'http://10.1.254.122:8080/ltyop/plan/movePlan?apikey=71029270&params={id: "'+id+'", type: "'+type+'"}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret){
                    layer.close(layer_index);
                    layer.msg(ret.respose.text, {time: 2000, shade: 0.3});
                    if (ret.result == 0){
                        if (type == 1){
                            prev_tr.before(active_tr);
                        }else{
                            next_tr.after(active_tr);
                        }
                    }
                }
            });
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
            // 增加icon浮层说明
            self.$(".content_tb .icon").hover(function(){
                if ($(this).hasClass("checkOut")){
                    var txt = ($(this).attr("st")==1)?'已签到':'未签到'
                }else{
                    var txt = ($(this).attr("st")==1)?'在线':'未在线'
                }
                self.layer_f_index = layer.tips(txt, this);
            },function(){
                layer.close(self.layer_f_index);
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
                    var y = e.clientY + 5 - parseInt(parent_obj.style.top.replace("px",""));
                    if ((y + 48*10)>document.body.clientHeight){
                        y -= 48*7;
                    }
                    var options = {
                        model: "bus_yard",
                        direction: $(this).attr("direction"),
                        pid: pid,
                        x: e.clientX + 5 - parseInt(parent_obj.style.left.replace("px","")),
                        y: y,
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
                    dialog.appendTo(self.$(".section_plan_cont").parents(".plan_display"));
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
                    var y = e.clientY + 5 - parseInt(parent_obj.style.top.replace("px",""));
                    if ((y + 48*8)>document.body.clientHeight){
                        y -= 48*6;
                    }
                    var options = {
                        model: "bus_transit",
                        direction: $(this).attr("direction"),
                        pid: pid,
                        x: e.clientX + 5 - parseInt(parent_obj.style.left.replace("px","")),
                        y: y,
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
                    dialog.appendTo(self.$(".section_plan_cont").parents(".plan_display"));
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

