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
        }
    });
    core.action_registry.add('lty_dispatch_desktop_widget.plan_display', plan_display);
});

