odoo.define(function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;

    var plan_display = Widget.extend({
        template: "plan_display_template",
        init: function(parent){
            this._super(parent);
            var init_data = {
                uplink_plan: [
                    {plan: "8:15", arrive: "9:15", vehicle: "655", driver: "刘德华", status: "待发"}, 
                    {plan: "9:20", arrive: "10:20", vehicle: "444", driver: "张晓峰", status: "待发"}, 
                    {plan: "9:35", arrive: "10:35", vehicle: "666", driver: "里得水", status: "待发"}, 
                    {plan: "8:15", arrive: "9:15", vehicle: "655", driver: "刘德华", status: "待发"}, 
                    {plan: "8:15", arrive: "9:15", vehicle: "655", driver: "刘德华", status: "待发"}, 
                    {plan: "8:15", arrive: "9:15", vehicle: "655", driver: "刘德华", status: "待发"}, 
                    {plan: "8:15", arrive: "9:15", vehicle: "655", driver: "刘德华", status: "待发"}, 
                    {plan: "8:15", arrive: "9:15", vehicle: "655", driver: "刘德华", status: "待发"}, 
                ],
                uplink_yard: [
                    {plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                ],
                uplink_on_the_way: [
                    {down_plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {down_plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {down_plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {down_plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {down_plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {down_plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {down_plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {down_plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                ],
                down_plan: [
                    {plan: "8:15", arrive: "9:15", vehicle: "655", driver: "刘德华", status: "待发"}, 
                    {plan: "9:20", arrive: "10:20", vehicle: "444", driver: "张晓峰", status: "待发"}, 
                    {plan: "9:35", arrive: "10:35", vehicle: "666", driver: "里得水", status: "待发"}, 
                    {plan: "8:15", arrive: "9:15", vehicle: "655", driver: "刘德华", status: "待发"}, 
                    {plan: "8:15", arrive: "9:15", vehicle: "655", driver: "刘德华", status: "待发"}, 
                    {plan: "8:15", arrive: "9:15", vehicle: "655", driver: "刘德华", status: "待发"}, 
                    {plan: "8:15", arrive: "9:15", vehicle: "655", driver: "刘德华", status: "待发"}, 
                    {plan: "8:15", arrive: "9:15", vehicle: "655", driver: "刘德华", status: "待发"}, 
                ],
                down_yard: [
                    {plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                ],
                down_on_the_way: [
                    {down_plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {down_plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {down_plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {down_plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {down_plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {down_plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {down_plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                    {down_plan: "8:15", vehicle: "264", line: 16, campo_atra: "8:10", parking: "5"},
                ],

            };
            this.plan_data = this.disposal_data(init_data);
        },
        start: function(){
            this.load_fn();
        },
        load_fn: function(){
            var self = this;
            self.$el.find(".plan_display .content_tb").on("click", "tr.point", function(){
                $(this).addClass("active_tr").siblings().removeClass('active_tr');
            });

            self.$el.find(".plan_display .uplink_plan").on("click", ".bottom_bt .cancel", function(){
                $(this).parents(".uplink_plan").find(".content_tb tr").removeClass("active_tr");
            });

            self.$el.find(".plan_display .uplink_plan").on("click", ".bottom_bt .move_bt", function(){
                var active_tr = $(this).parents(".uplink_plan").find(".content_tb tr.active_tr");
                if (active_tr.length == 0){
                    alert("请选择需要处理的计划");
                    // layer.msg("请选择需要处理的计划", {time: 1000, shade: 0.3});
                    return;
                }
                var name = $(this).attr("name");
                self.move_fn(active_tr, name);
            });

            self.$el.find(".plan_display .uplink_plan").on("click", ".bottom_bt .adjust", function(){
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
                layer.open({
                    type: 1,
                    title: "调整计划",
                    area: ['500px', ''],
                    resize: false,
                    content: QWeb.render("adjust_the_plan_template", {quota: init_data})
                });
            });

            $("body").on("click", ".adjust_box .reset_bt", function(){
                $(".adjust_box input[type='number']").val("");
            });

            $("body").on("click", ".adjust_box .ok_bt", function(){
                layer.msg("请求接口还没有给到", {time: 2000, shade: 0.3});
            });

            $("body").on("click", ".adjust_box .close_bt", function(){
                layer.closeAll();
            });

        },
        move_fn: function(active_tr, type){
            if (type == "front"){
                var prev_tr = active_tr.prev ('tr.point');
                if (prev_tr.length > 0){
                    alert("发生请求后才显示‘确认按钮’后的东西");
                    prev_tr.before(active_tr);
                    return;
                }
                alert("该计划已经是最前面的");
            }else{
                var next_tr = active_tr.next ('tr.point');
                if (next_tr.length > 0){
                    alert("发生请求后才显示‘确认按钮’后的东西");
                    next_tr.after(active_tr);
                    return;
                }
                alert("该计划已经是最后面的");
            }
        },
        disposal_data: function(data){
            var uplink_plan = data.uplink_plan;
            var uplink_yard = data.uplink_yard;
            var uplink_on_the_way = data.uplink_on_the_way;

            var down_plan = data.down_plan;
            var down_yard = data.down_yard;
            var down_on_the_way = data.down_on_the_way;

            var new_uplink_plan = [];
            var new_uplink_yard = [];
            var new_uplink_on_the_way = [];

            var new_down_plan = [];
            var new_down_yard = [];
            var new_down_on_the_way = [];
            for (var i=0; i<20; i++){
                if (uplink_plan.length > i){
                    new_uplink_plan.push(uplink_plan[i]);
                }
                if (uplink_plan.length <= i){
                    new_uplink_plan.push({});
                }

                if(uplink_yard.length > i){
                    new_uplink_yard.push(uplink_yard[i]);
                }
                if (uplink_yard.length <= i){
                    new_uplink_yard.push({});
                }

                if(uplink_on_the_way.length > i){
                    new_uplink_on_the_way.push(uplink_on_the_way[i]);
                }
                if (uplink_on_the_way.length <= i){
                    new_uplink_on_the_way.push({});
                }

                if(down_yard.length > i){
                    new_down_yard.push(down_yard[i]);
                }
                if (down_yard.length <= i){
                    new_down_yard.push({});
                }

                if(down_plan.length > i){
                    new_down_plan.push(down_plan[i]);
                }
                if (down_plan.length <= i){
                    new_down_plan.push({});
                }

                if(down_on_the_way.length > i){
                    new_down_on_the_way.push(down_on_the_way[i]);
                }
                if (down_on_the_way.length <= i){
                    new_down_on_the_way.push({});
                }
            }
            data.uplink_plan = new_uplink_plan;
            data.uplink_yard = new_uplink_yard;
            data.uplink_on_the_way = new_uplink_on_the_way;
            data.down_plan = new_down_plan;
            data.down_yard = new_down_yard;
            data.down_on_the_way = new_down_on_the_way;
            return data;
        },
    });
    core.action_registry.add('lty_dispatch_desktop_widget.plan_display', plan_display);
});

