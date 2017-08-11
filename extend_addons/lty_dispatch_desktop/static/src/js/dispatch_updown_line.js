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
                var conCls = self.$el.find('.carousel_content')[0].className;
                var content = '.' + conCls;
                carousel({
                    content: content,
                    self: self
                });
            }
            var model_id = 'model_' + 123;
            if (socket_model_info[model_id]) {
                delete socket_model_info[model_id];
            }
            var dataJson = [[120, 152], [220, 182], [150, 232], [320, 332]];
            self.dataJson=dataJson
            socket_model_info[model_id] = {
                arg: {
                    self: self,
                    dataJson:self.dataJson
                }, fn: self.show_echarts
            };
        },
        events: {
            'click .manual': 'manual_process',
            'click .manual.is_check': 'process_chchk',
            'click .min': 'closeFn'
        },
        show_echarts: function (innerHTML, arg) {
            var self = arg.self;
            var dataJson = self.dataJson;
            var absnormalChart = self.$el.find('.absnormal_chart')[0];
            var absnormalChart1 = self.$el.find('.absnormal_chart')[1];
            // 柱状型数据
            var lagstation_chart = self.$el.find('.lagstation_chart')[0];
            for (var i = 0;i<dataJson.length;i++){
                dataJson[i].push(innerHTML.substring(78, 80)+i*3);
            }
            console.log(dataJson);
            chartLineBar(absnormalChart, 1, ["#ff4634", "#4dcfc7", "#ffd275", "#cc2123"], 'line', false, ['实际客流', '预测客流', '计划客流', '调整客流'], optionLineBar, ['5:00', '8:00', '13:00', '16:00', '19:00', '0:00','5:00', '8:00', '13:00', '16:00', '19:00', '0:00','5:00', '8:00', '13:00', '16:00', '19:00', '0:00','5:00', '8:00', '13:00', '16:00', '19:00', '0:00','5:00', '8:00', '13:00', '16:00', '19:00', '0:00','5:00', '8:00', '13:00', '16:00', '19:00', '0:00','5:00', '8:00', '13:00', '16:00', '19:00', '0:00','5:00', '8:00', '13:00', '16:00', '19:00', '0:00','5:00', '8:00', '13:00', '16:00', '19:00', '0:00'], dataJson, '');
            chartLineBar(absnormalChart1, 1, ["#ff4634", "#4dcfc7", "#ffd275", "#cc2123"], 'line', false, ['实际客流', '预测客流', '计划客流', '调整客流'], optionLineBar, ['5:00', '8:00', '13:00', '16:00', '19:00', '0:00','5:00', '8:00', '13:00', '16:00', '19:00', '0:00','5:00', '8:00', '13:00', '16:00', '19:00', '0:00','5:00', '8:00', '13:00', '16:00', '19:00', '0:00','5:00', '8:00', '13:00', '16:00', '19:00', '0:00','5:00', '8:00', '13:00', '16:00', '19:00', '0:00','5:00', '8:00', '13:00', '16:00', '19:00', '0:00','5:00', '8:00', '13:00', '16:00', '19:00', '0:00','5:00', '8:00', '13:00', '16:00', '19:00', '0:00'], dataJson, '');
            chartLineBar(lagstation_chart, 0, ["#ff4634", "#4dcfc7"], 'bar', true, ['滞站客流', '预测滞站'], optionLineBar, ['周一', '周二', '周三', '周四', '周五', '周六'], [[120, 152, 101, 134, 90, 230], [220, 182, 191, 234, 290, 330]], '');
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
            var x = event.currentTarget;
            $(x).html('完成').addClass('is_check').siblings().hide();
        },
        process_chchk: function () {
            this.$el.find('.no_absnormal').show().siblings().hide();
        }
    });
    return dispatch_updown_line;
});