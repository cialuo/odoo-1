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
        },
        start: function () {
            var self = this
            var data = this.dis_desk;
            console.log(data);
            if (data) {
                var conCls = self.$el.find('.carousel_content')[0].className;
                var content = '.' + conCls;
                carousel({
                    content: content,
                    self: self
                });
                var absnormalChart = self.$el.find('.absnormal_chart')[0];
                var absnormalChart1 = self.$el.find('.absnormal_chart')[1];
                var lagstation_chart = self.$el.find('.lagstation_chart')[0];
                chartLineBar(absnormalChart, 1, ["#ff4634", "#4dcfc7", "#ffd275", "#cc2123"], 'line', false, ['实际客流', '预测客流', '计划客流', '调整客流'], optionLineBar, ['5:00', '8:00', '13:00', '16:00', '19:00', '0:00'], [[120, 152, 101, 134, 90, 230, 210], [220, 182, 191, 234, 290, 330, 310], [150, 232, 201, 154, 190, 330, 410], [320, 332, 301, 334, 390, 330, 320]], '');
                chartLineBar(absnormalChart1, 1, ["#ff4634", "#4dcfc7", "#ffd275", "#cc2123"], 'line', false, ['实际客流', '预测客流', '计划客流', '调整客流'], optionLineBar, ['5:00', '8:00', '13:00', '16:00', '19:00', '0:00'], [[120, 152, 101, 134, 90, 230, 210], [220, 182, 191, 234, 290, 330, 310], [150, 232, 201, 154, 190, 330, 410], [320, 332, 301, 334, 390, 330, 320]], '');
                chartLineBar(lagstation_chart, 0, ["#ff4634", "#4dcfc7"], 'bar', true, ['滞站客流', '预测滞站'], optionLineBar, ['周一', '周二', '周三', '周四', '周五', '周六'], [[120, 152, 101, 134, 90, 230], [220, 182, 191, 234, 290, 330]], '');
            }
        },
    });
    return dispatch_updown_line;
});