/**
 * Created by Administrator on 2017/7/20.
 */
odoo.define('lty_dispaych_desktop.updown_line', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var Model = require('web.Model');
    var dispatch_updown_line = Widget.extend({
        template: 'updown_line_table',
        init: function (parent, data) {
            this._super(parent);
            this.dis_desk = data;
            this.model2 = new Model('dispatch.control.desktop.component');
        },
        start: function () {
            var self = this
            var data = this.dis_desk;
            if (data) {
                var content = '.' + self.$el.find('.carousel_content')[0].className;
                carousel({
                    content: content,
                    self: self
                });
            }
            var tid = self.$el.attr('tid');
            var model_id = 'model_' + tid;
            if (socket_model_info[model_id]) {
                delete socket_model_info[model_id];
            }
            if (self.$el.find('.absnormal_chart')[0] != undefined) {
                self.absnormalChart = echarts.init(self.$el.find('.absnormal_chart')[0]);
                self.absnormalChart1 = echarts.init(self.$el.find('.absnormal_chart')[1]);
                self.lagstation_chart = echarts.init(self.$el.find('.lagstation_chart')[0]);
                self.dataJson = [[120, 152], [220, 182], [150, 232], [320, 332]];
                // var package = {
                //     type: 1022,
                //     open_modules: "dispatch-line_message-4",
                //     msgId: Date.parse(new Date())
                // };
                // websocket.send(JSON.stringify(package));
                socket_model_info[model_id] = {
                    arg: {
                        self: self,
                        dataJson: self.dataJson,
                        absnormalChart: self.absnormalChart,
                        absnormalChart1: self.absnormalChart1,
                        lagstation_chart: self.lagstation_chart,
                    }, fn: self.show_echarts
                };
            }
        },
        events: {
            'click .manual': 'manual_process',
            'click .finishBtn .is_check': 'process_chchk',
            'click .min': 'closeFn'
        },
        show_echarts: function (innerHTML, arg) {
            var self = arg.self;
            var dataJson = self.dataJson;
            for (var i = 0; i < dataJson.length; i++) {
                dataJson[i].push(innerHTML.substring(78, 80) + i * 3);
            }
            chartLineBar(self.absnormalChart, 1, ["#ff4634", "#4dcfc7", "#ffd275", "#cc2123"], 'line', false, ['实际客流', '预测客流', '计划客流', '调整客流'], optionLineBar, ['5:00', '8:00', '13:00', '16:00', '19:00', '0:00', '5:00', '8:00', '13:00', '16:00', '19:00', '0:00', '5:00', '8:00', '13:00', '16:00', '19:00', '0:00', '5:00', '8:00', '13:00', '16:00', '19:00', '0:00', '5:00', '8:00', '13:00', '16:00', '19:00', '0:00', '5:00', '8:00', '13:00', '16:00', '19:00', '0:00', '5:00', '8:00', '13:00', '16:00', '19:00', '0:00', '5:00', '8:00', '13:00', '16:00', '19:00', '0:00', '5:00', '8:00', '13:00', '16:00', '19:00', '0:00'], dataJson, '');
            chartLineBar(self.absnormalChart1, 1, ["#ff4634", "#4dcfc7", "#ffd275", "#cc2123"], 'line', false, ['实际客流', '预测客流', '计划客流', '调整客流'], optionLineBar, ['5:00', '8:00', '13:00', '16:00', '19:00', '0:00', '5:00', '8:00', '13:00', '16:00', '19:00', '0:00', '5:00', '8:00', '13:00', '16:00', '19:00', '0:00', '5:00', '8:00', '13:00', '16:00', '19:00', '0:00', '5:00', '8:00', '13:00', '16:00', '19:00', '0:00', '5:00', '8:00', '13:00', '16:00', '19:00', '0:00', '5:00', '8:00', '13:00', '16:00', '19:00', '0:00', '5:00', '8:00', '13:00', '16:00', '19:00', '0:00', '5:00', '8:00', '13:00', '16:00', '19:00', '0:00'], dataJson, '');
            chartLineBar(self.lagstation_chart, 0, ["#ff4634", "#4dcfc7"], 'bar', true, ['滞站客流', '预测滞站'], optionLineBar, ['周一', '周二', '周三', '周四', '周五', '周六'], [[120, 152, 101, 134, 90, 230], [220, 182, 191, 234, 290, 330]], '');
        },
        closeFn: function () {
            var self = this;
            var tid = this.$el.attr('tid');
            var line_id = this.$el.attr('line_id');
            self.$el.parent().find('.dispatch_desktop').find('.line_edit').hide();
            self.$el.parent().find('.dispatch_desktop').find('.show_right').show();
            self.model2.call("write", [parseInt(tid),
                {
                    'tem_display': 'none',
                    'position_left': self.$el[0].offsetLeft,
                    'position_top': self.$el[0].offsetTop,
                    'position_z_index': self.$el[0].style.zIndex,
                }]).then(function (res) {
                self.$el.hide();
            });
        },
        manual_process: function (event) {
            this.$el.find('.real_time_process').show().css("display", "inline-block");
            var x_deal = event.currentTarget;
            $(x_deal).parent().hide().siblings('.finishBtn').show();
        },
        process_chchk: function (event) {
            stopPropagation(event);
            var x_comp = event.currentTarget;
            $(x_comp).parent().hide().siblings('.handleBtn').show();
            var self = this;
            this.$el.find('.normal').show().siblings().hide();
            var content = '.' + self.$el.find('.carousel_content')[0].className;
            carousel({
                content: content,
                self: self
            });
        }
    });
    return dispatch_updown_line;
});