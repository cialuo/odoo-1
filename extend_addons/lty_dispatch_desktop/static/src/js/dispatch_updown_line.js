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
            this.desktop_id = this.$el.parents(".back_style").attr("desktop_id");
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
            var line_id = self.$el.attr('line_id');
            var model_abnormal = 'abnormal__'+line_id;
            var model_chart = 'passenge_flow__'+line_id;
            if (socket_model_info[model_abnormal]) {
                delete socket_model_info[model_abnormal];
            }
            if (socket_model_info[model_chart]) {
                delete socket_model_info[model_chart];
            }
            if (self.$el.find('.absnormal_chart')[0] != undefined) {
                self.absnormalChart = echarts.init(self.$el.find('.absnormal_chart')[0]);
                self.absnormalChart1 = echarts.init(self.$el.find('.absnormal_chart')[1]);
                self.lagstation_chart = echarts.init(self.$el.find('.lagstation_chart')[0]);
                self.dataJson = [[120, 152], [220, 182], [150, 232], [320, 332]];
                var package = {
                    type: 1000,
                    open_modules: ["dispatch-abnormal-" + this.desktop_id],
                    msgId: Date.parse(new Date())
                };
                websocket.send(JSON.stringify(package));
                socket_model_info[model_abnormal] = {
                    arg: {
                        self: self,
                        line_id: line_id,
                    }, fn: self.abnormal_save
                };
                socket_model_info[model_chart] = {
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
        abnormal_save: function (datalist, arg) {
            var self = arg.self;
            var data_use = JSON.parse(datalist);
            // if(data_use.line_id == parseInt(arg.line_id))
            console.log(11)
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
            self.$el.parent().find('.dispatch_desktop').find('.show_right').css('display', 'inline-block');
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
            this.$el.find('.abs_info .absnormal_height').eq(0).remove();
            $.ajax({
                    url: 'http://202.104.136.228:8080/ltyop/resource/exceptionHandle?apikey=71029270&params={onBoardId:15745,exceptKm:10,exceptStationId:13655,exceptReasonId:6}',
                    type: 'post',
                    dataType: 'json',
                    data: {},
                    success: function (data) {

                    }
                }
            )
            if (this.$el.find('.abs_info .absnormal_height').length < 1) {
                $(x_comp).parent().hide().siblings('.handleBtn').show();
                this.$el.removeClass('warn');
                this.$el.find('.normal').show().siblings().hide();
                var content = '.' + this.$el.find('.carousel_content')[0].className;
                carousel({
                    content: content,
                    self: this
                });
            }
            else {
                $(x_comp).parent().hide().siblings().show();
            }

        }
    });
    return dispatch_updown_line;
});