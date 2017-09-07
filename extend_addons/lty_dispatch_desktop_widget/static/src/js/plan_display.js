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
                type: 2000,
                controlId: this.location_data.controllerId,
                open_modules: ["line_plan", "line_park", "line_online"]
            };
            websocket.send(JSON.stringify(package));

            this.load_plan();
        },
        load_plan: function(){
            var self = this;
            console.log(self.location_data.controllerId+'_'+self.location_data.line_id);
            $.ajax({
                url: 'http://202.104.136.228:8888/ltyop/planData/query?apikey=71029270&params={tablename:"op_dispatchplan",controlsId:'+self.location_data.controllerId+',lineId:'+self.location_data.line_id+'}',
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
                        url: 'http://202.104.136.228:8888/ltyop/planData/query?apikey=71029270&params={tablename:"op_busresource",controlsId:'+self.location_data.controllerId+',lineId:'+self.location_data.line_id+'}',
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

            var passengerDelayModel_set = JSON.parse(sessionStorage.getItem("linePlanParkOnlineModel_set"));
            layer.close(passengerDelayModel_set.layer_index);
            $('.linePlanParkOnlineModel .section_plan_cont').mCustomScrollbar({
                theme: 'minimal'
            });
            self.$el.removeClass('hide_model');

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
                    $("."+model+" .content_tb .point[pid="+plan_pid+"]").removeClass("active_tr").removeClass("right");
                    $(".plan_display_set").remove();
                }
            });

            // 计划，在场，在途手动操作交互事件
            self.linePlanParktransit_bt_fn();
        },
        linePlanParktransit_bt_fn: function() {
            var self = this;
            var plan_display = self.$(".plan_display");
            var controllerId = self.location_data.controllerId;
            var controllerObj = self.$el.parents($(".controller_" + controllerId));

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
                    layer_index: layer_index
                };
                self.send_short_msg__fn(options);
            });

            // 添加计划
            plan_display.on("click", ".plan_display_set[model='bus_plan'] li.add_plan_bt", function() {
                var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                var obj = $(this).parents(".plan_display_set");
                var options = {
                    id: obj.attr("plan_pid"),
                    layer_index: layer_index
                };
                self.add_plan_fn(options);
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
                var direction = $(this).parents(".plan_display_set").attr("direction");
                var active_tr = plan_display.find(".bus_plan .content_tb").find("tr.active_tr[direction=" + direction + "][pid=" + id + "]");
                var title_obj = plan_display.find(".closeBox .num");
                var options = {
                    id: id,
                    layer_index: layer_index
                    // direction: direction,
                    // lineId: title_obj.attr("line_id"),
                    // lineName: title_obj.text(),
                    // carNum: active_tr.find("td:eq(3)").text(),
                    // driverName: active_tr.find("td:eq(4)").text()
                };
                self.batch_fix_switch_fn(options);
            });

            // 司乘签到
            plan_display.on("click", ".plan_display_set[model='bus_yard'] li.sign_in_bt, .plan_display_set[model='bus_transit'] li.sign_in_bt", function() {
                alert("我是司乘签到");
            });

            // 编辑车辆
            plan_display.on("click", ".plan_display_set[model='bus_yard'] li.edit_vehicles_bt, .plan_display_set[model='bus_transit'] li.edit_vehicles_bt", function() {
                alert("我是编辑车辆");
            });

            // 异常状态
            plan_display.on("click", ".plan_display_set[model='bus_yard'] li.abnormal_state_bt, .plan_display_set[model='bus_transit'] li.abnormal_state_bt", function() {
                alert("我是异常状态");
            });

            // 异常状态
            plan_display.on("click", ".plan_display_set[model='bus_yard'] li.in_task_bt, .plan_display_set[model='bus_transit'] li.in_task_bt", function() {
                alert("我是进场任务");
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
        },
        plan_bottom_fn: function(){
            var self = this;
            var plan_display = self.$(".plan_display");
            //上下移动计划
            plan_display.on("click", ".bottom_bt .move_bt", function(){
                var plan_box = $(this).parents(".plan_box");
                var bus_plan = plan_box.find(".bus_plan");
                var direction = bus_plan.attr("direction");
                 // 先去掉右键浮层及active
                var r_pid = plan_display.find(".content_tb tr.right").attr("pid");
                plan_display.find(".plan_display_set").remove();
                plan_display.find(".content_tb tr.right").removeClass("active_tr").removeClass("right");
                var active_tr = bus_plan.find(".content_tb tr.active_tr");
                if (active_tr.length == 1) {
                    var options = {
                        active_tr: active_tr,
                        type: $(this).attr("name")
                    };
                    self.move_up_or_down_fn(options);
                }else{
                    layer.msg("请选择需要处理的计划", {time: 1000, shade: 0.3});
                }
            });

            // 修改计划
            plan_display.on("click", ".bottom_bt .fix", function(){
                var plan_box = $(this).parents(".plan_box");
                var bus_plan = plan_box.find(".bus_plan");
                var direction = bus_plan.attr("direction");
                 // 先去掉右键浮层及active
                var r_pid = plan_display.find(".content_tb tr.right").attr("pid");
                plan_display.find(".plan_display_set").remove();
                plan_display.find(".content_tb tr.right").removeClass("active_tr").removeClass("right");
                var active_tr = bus_plan.find(".content_tb tr.active_tr");
                if (active_tr.length == 1) {
                    var layer_index = layer.msg("请求中，请稍后...", {shade: 0.3, time: 0});
                    var options = {
                        id: active_tr.attr("pid"),
                        layer_index: layer_index
                    };
                    self.fix_plan_fn(options);
                }else{
                    layer.msg("请选择需要处理的计划", {time: 1000, shade: 0.3});
                }
            });
        },
        send_plan_vehicles_fn: function(options){
            $.ajax({
                url: 'http://202.104.136.228:8888/ltyop/plan/sendPlanToBus?apikey=71029270&params={id: "'+options.id+'"}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret){
                    layer.close(options.layer_index);
                    if (ret.result == 0){
                        //这里特别说明一下，由于请求成功后，后台会立即触发一次推送websoket，页面状态更新这里将不在做处理
                    }
                    layer.msg(ret.respose.text, {time: 2000, shade: 0.3});
                }
            });
        },
        send_short_msg__fn: function(options) {
            var self = this;
            layer.close(options.layer_index);
            new send_short_msg_msg(self).appendTo(self.$el);
            self.$el.find('.send_short_msg_msg .modal').on('shown.bs.modal', function(e) {
                // 关键代码，如没将modal设置为 block，则$modala_dialog.height() 为零
                $(this).css('display', 'block');
                console.log($(window).height())
                var modalHeight = $(window).height() / 2 - self.$el.find('.send_short_msg_msg .modal').find('.modal-dialog').height() / 2;
                $(this).find('.modal-dialog').css({
                    'margin-top': modalHeight
                });
            });
            self.$el.find('.send_short_msg_msg .modal').modal({ backdrop: 'static', keyboard: false });
        },
        add_plan_fn: function(options){
            var self = this;
            $.ajax({
                url: 'http://202.104.136.228:8888/ltyop/planData/query?apikey=71029270&params={tablename:"op_dispatchplan",controlsId:'+self.location_data.controllerId+',lineId:'+self.location_data.line_id+',id:'+options.id+'}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret){
                    layer.close(options.layer_index);
                    console.log(ret.respose[0]);
                    var dialog = new add_plan_w(self, ret.respose[0]);
                    dialog.appendTo($('body'));
                }
            });
        },
        reduction_time_fn: function(options){
            $.ajax({
                url: 'http://202.104.136.228:8888/ltyop/plan/restoreTime?apikey=71029270&params={id: "'+options.id+'"}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret){
                    layer.close(options.layer_index);
                    if (ret.result == 0){
                        //这里特别说明一下，由于请求成功后，后台会立即触发一次推送websoket，页面状态更新这里将不在做处理
                    }
                    layer.msg(ret.respose.text, {time: 2000, shade: 0.3});
                }
            });
        },
        batch_fix_switch_fn: function(options){
            var self = this;
            $.ajax({
                url: 'http://202.104.136.228:8888/ltyop/planData/query?apikey=71029270&params={tablename:"op_dispatchplan",controlsId:'+self.location_data.controllerId+',lineId:'+self.location_data.line_id+',id:'+options.id+'}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret){
                    layer.close(options.layer_index);
                    var op = ret.respose[0];
                    op.controllerId = self.location_data.controllerId;
                    console.log(op);
                    var dialog = new batch_fix_switch_w(self, op);
                    dialog.appendTo($('body'));
                }
            });
        },
        immediate_scheduling_fn: function(options){
            $.ajax({
                url: 'http://202.104.136.228:8888/ltyop/resource/applyPlanById?apikey=71029270&params={id: "'+options.id+'"}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret){
                    layer.close(options.layer_index);
                    layer.msg(ret.respose.text, {time: 2000, shade: 0.3});
                }
            });
        },
        cancel_scheduling_fn: function(options){
            $.ajax({
                url: 'http://202.104.136.228:8888/ltyop/resource/cancelWorkPlan?apikey=71029270&params={id: "'+options.id+'"}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret){
                    layer.close(options.layer_index);
                    layer.msg(ret.respose.text, {time: 2000, shade: 0.3});
                }
            });
        },
        exit_operation_fn: function(options){
            $.ajax({
                url: 'http://202.104.136.228:8888/ltyop/resource/exitRun?apikey=71029270&params={id: "'+options.id+'"}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret){
                    layer.close(options.layer_index);
                    layer.msg(ret.respose.text, {time: 2000, shade: 0.3});
                }
            });
        },
        move_up_or_down_fn: function(options){
            var layer_index = layer.msg("请求中，请稍后...", {shade: 0.3, time: 0});
            var active_tr = options.active_tr;
            var id = active_tr.attr("pid");
            var type = options.type;
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
                url: 'http://202.104.136.228:8888/ltyop/plan/movePlan?apikey=71029270&params={id: "'+id+'", type: "'+type+'"}',
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
        fix_plan_fn: function(options){
            var self = this;
            $.ajax({
                url: 'http://202.104.136.228:8888/ltyop/planData/query?apikey=71029270&params={tablename:"op_dispatchplan",controlsId:'+self.location_data.controllerId+',lineId:'+self.location_data.line_id+',id:'+options.id+'}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret){
                    layer.close(options.layer_index);
                    console.log(ret.respose[0]);
                    var dialog = new fix_plan_w(self, ret.respose[0]);
                    dialog.appendTo($('body'));
                }
            });
        },
        closeFn: function(){
            // 取消线路计划、车场、状态
            var package = {
                type: 2001,
                controlId: this.location_data.controllerId,
                open_modules: ["line_plan", "line_park", "line_online"]
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

            // 增加icon浮层说明
            self.$(".content_tb .icon").hover(function(){
                var txt = ($(this).attr("st")==1)?'已发送':'未发送'
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
                    $(this).addClass("active_tr").addClass("right");
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
                        y: y-60,
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
        }
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
                    $(this).addClass("active_tr").addClass("right");
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
                        y: y-60,
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
                    $(this).addClass("active_tr").addClass("right");
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
                        y: y-60,
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
    var send_short_msg_msg = Widget.extend({
        template: "send_short_msg_msg",
        init: function(parent, data){
            this._super(parent);
            this.location_data =  data;
        },
        events:{
            'click .modal_lty .close':'closeFn'
        },
        closeFn:function () {
            this.destroy();
            $(".modal-backdrop").remove();
        }
    });

    // 添加计划
    var add_plan_w = Widget.extend({
        template: 'plan_display_add_plan_template',
        init: function(parent, data){
            this._super(parent);
            this.set_data = data;
        },
        start: function(){
            this.modal_fn();
        },
        modal_fn: function(){
            var self = this;
            self.$el.on('hide.bs.modal', function () {
                self.destroy();
            });
            self.$el.on('show.bs.modal', function () {
                $(this).css('display', 'block');
                // 是弹出框居中。。。
                var $modal_dialog = $(this).find('.modal-dialog');
                //获取可视窗口的高度
                var clientHeight = (document.body.clientHeight < document.documentElement.clientHeight) ? document.body.clientHeight: document.documentElement.clientHeight;
                //得到dialog的高度
                var dialogHeight = $modal_dialog.height();
                //计算出距离顶部的高度
                var m_top = (clientHeight - dialogHeight)/2;
                $modal_dialog.css({'margin': m_top + 'px auto'});
            });
            self.$el.modal({
                backdrop: 'static',
                keyboard: false
            });

            // 提交
            self.$('.btn-primary').on('click', function(){
                self.submit_fn();
            });
        },
        submit_fn: function(){
            var self = this;
            var layer_index = layer.msg("请求中，请稍后...", {shade: 0.3, time: 0});
            var confObj = self.$('.modal-body table');
            var params = {
                id: self.set_data.id,
                planTime: confObj.find(".planTime input:eq(0)").val() + ":" + confObj.find(".planTime input:eq(1)").val(),
                planCount: confObj.find(".planCount").val(),
                lineId: confObj.find(".line").val(),
                direction: confObj.find(".direction").val(),
                planKm: confObj.find(".planKm").val(),
                addReasonId: confObj.find(".addReason").val(),
                carNum: confObj.find(".carNum").val(),
                workerId: confObj.find(".worker").val(),
                driverName: confObj.find(".driverName").val(),
                trainId: confObj.find(".train").val(),
                trainName: confObj.find(".trainName").val(),
                addType: confObj.find(".addType").val(),
                remark: confObj.find(".remark").val(),
            };
            $.ajax({
                url: 'http://202.104.136.228:8888/ltyop/plan/addPlan?apikey=71029270&params='+JSON.stringify(params),
                type: 'post',
                dataType: 'json',
                data: {},
                success: function(ret){
                    layer.close(layer_index);
                    layer.msg(ret.respose.text, {time: 2000, shade: 0.3});
                    self.$('.btn-default').click();
                }
            });
        }
    });

    // 修改计划
    var fix_plan_w = Widget.extend({
        template: 'plan_display_fix_plan_template',
        init: function(parent, data){
            this._super(parent);
            this.set_data = data;
        },
        start: function(){
            this.modal_fn();
        },
        modal_fn: function(){
            var self = this;
            self.$el.on('hide.bs.modal', function () {
                self.destroy();
            });
            self.$el.on('show.bs.modal', function () {
                $(this).css('display', 'block');
                // 是弹出框居中。。。
                var $modal_dialog = $(this).find('.modal-dialog');
                //获取可视窗口的高度
                var clientHeight = (document.body.clientHeight < document.documentElement.clientHeight) ? document.body.clientHeight: document.documentElement.clientHeight;
                //得到dialog的高度
                var dialogHeight = $modal_dialog.height();
                //计算出距离顶部的高度
                var m_top = (clientHeight - dialogHeight)/2;
                $modal_dialog.css({'margin': m_top + 'px auto'});
            });
            self.$el.modal({
                backdrop: 'static',
                keyboard: false
            });

            self.$('.modal-body').on("click", ".selectType .ckIcon", function(){
                $(this).addClass("active").siblings().removeClass('active');
            });

            // 提交
            self.$('.btn-primary').on('click', function(){
                self.submit_fn();
            });
        },
        submit_fn: function(){
            var self = this;
            var layer_index = layer.msg("请求中，请稍后...", {shade: 0.3, time: 0});
            var confObj = self.$('.modal-body table');
            var params = {
                id: self.set_data.id,
                planTime: confObj.find(".planTime").val(),
                planCount: confObj.find(".planCount").val(),
                lineId: confObj.find(".line").val(),
                runGprsId: confObj.find(".runGprs").val(),
                carNum: confObj.find(".carNum").val(),
                planKm: confObj.find(".planKm").val(),
                direction: confObj.find(".direction").val(),
                driverName: confObj.find(".driverName").val(),
                changeReason: confObj.find(".changeReason").val(),

                // workerId: confObj.find(".worker").val(),
                // trainId: confObj.find(".train").val(),
                // trainName: confObj.find(".trainName").val(),
                // addType: confObj.find(".addType").val(),
                // remark: confObj.find(".remark").val(),
            };
            $.ajax({
                url: 'http://202.104.136.228:8888/ltyop/plan/updatePlan?apikey=71029270&params='+JSON.stringify(params),
                type: 'post',
                dataType: 'json',
                data: {},
                success: function(ret){
                    layer.close(layer_index);
                    layer.msg(ret.respose.text, {time: 2000, shade: 0.3});
                    self.$('.btn-default').click();
                }
            });
        }
    });

    // 批量更改车辆或司机
    var batch_fix_switch_w = Widget.extend({
        template: 'batch_fix_switch_template',
        init: function(parent, data){
            this._super(parent);
            this.set_data = data;
        },
        start: function(){
            this.modal_fn();
        },
        modal_fn: function(){
            var self = this;
            self.$el.on('hide.bs.modal', function () {
                self.destroy();
            });
            self.$el.on('show.bs.modal', function () {
                $(this).css('display', 'block');
                // 是弹出框居中。。。
                var $modal_dialog = $(this).find('.modal-dialog');
                //获取可视窗口的高度
                var clientHeight = (document.body.clientHeight < document.documentElement.clientHeight) ? document.body.clientHeight: document.documentElement.clientHeight;
                //得到dialog的高度
                var dialogHeight = $modal_dialog.height();
                //计算出距离顶部的高度
                var m_top = (clientHeight - dialogHeight)/2;
                $modal_dialog.css({'margin': m_top + 'px auto'});
            });
            self.$el.modal({
                backdrop: 'static',
                keyboard: false
            });

            self.$('.modal-body').on("click", ".mode_type a", function(){
                $(this).addClass("active").siblings().removeClass('active');
            });
            // 提交
            self.$('.btn-primary').on('click', function(){
                self.submit_fn();
            });
        },
        submit_fn: function(){
            var self = this;
            var layer_index = layer.msg("请求中，请稍后...", {shade: 0.3, time: 0});
            var confObj = self.$('.modal-body table');
            var params = {
                controllerId: self.set_data.controllerId,
                planId_1: self.set_data.id,
                driverId_1: confObj.find(".driverName").attr("workerId"),
                chooseOnboardId: confObj.find(".selfId").attr("onBoardId"),
                lineId: confObj.find(".line").val(),
                startTime: confObj.find(".startTime").val(),
                endTime: confObj.find(".endTime").val(),
                planOnboardId: confObj.find(".replace_vehicles").attr("planOnboardId"),
                driverId_2: confObj.find(".replace_driver").attr("driverId_2"),
                driverName_2: confObj.find(".replace_driver").val(),
                modeType: confObj.find(".mode_type .active").attr("name")
            };
            if (params.modeType == "replace"){
                self.replace_ajax_fn(params, layer_index);
                return;
            }
            self.switch_ajax_fn(params, layer_index);
        },
        replace_ajax_fn: function(op, layer_index){
            $.ajax({
                url: 'http://202.104.136.228:8888/plan/batchReplaceDriverOrCar?apikey=71029270&params='+JSON.stringify(op),
                type: 'post',
                dataType: 'json',
                data: {},
                success: function(ret){
                    layer.close(layer_index);
                    layer.msg(ret.respose.text, {time: 2000, shade: 0.3});
                    self.$('.btn-default').click();
                }
            });
        },
        switch_ajax_fn: function(op, layer_index){
            $.ajax({
                url: 'http://202.104.136.228:8888/plan/batchUpdateDriverOrCar?apikey=71029270&params='+JSON.stringify(op),
                type: 'post',
                dataType: 'json',
                data: {},
                success: function(ret){
                    layer.close(layer_index);
                    layer.msg(ret.respose.text, {time: 2000, shade: 0.3});
                    self.$('.btn-default').click();
                }
            });
        }
    });

    return plan_display;
});

