/**
 * Created by Administrator on 2017/7/20.
 */
odoo.define('lty_dispaych_desktop.updown_line', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var Model = require('web.Model');
    var dispatch_updown_line = Widget.extend({
        template: 'updown_line_table',
        init: function (parent, data,rendr_index) {
            this._super(parent);
            this.dis_desk = data;
            this.model2 = new Model('dispatch.control.desktop.component');
            this.model_abnormal = new Model('dispatch.abnormal.mgt');
            this.rendr_index = rendr_index;
        },
        start: function () {
            this.desktop_id = this.$el.parents(".back_style").attr("desktop_id");
            var self = this;
            var data = this.dis_desk;
            if (data) {
                var content = '.' + self.$el.find('.carousel_content')[0].className;
                carousel({
                    content: content,
                    self: self
                });
            }
            var tid = self.$el.attr('tid');
            self.line_id = self.$el.attr('line_id');
            var model_abnormal = 'abnormal__' + self.line_id;
            var model_chart = 'passenger_flow__' + self.line_id;
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
                var package_abnormal = {
                    type: 2000,
                    controlId: this.desktop_id,
                    open_modules: ["abnormal"]
                };
                websocket.send(JSON.stringify(package_abnormal));
                var package_passenger_flow = {
                    type: 2000,
                    controlId: this.desktop_id,
                    open_modules: ["passenger_flow"]
                };
                websocket.send(JSON.stringify(package_passenger_flow));
                socket_model_info[model_abnormal] = {
                    arg: {
                        self: self,
                        line_id: self.line_id
                    }, fn: self.abnormal_save
                };
                socket_model_info[model_chart] = {
                    arg: {
                        self: self,
                        line_id: self.line_id,
                        desktop_id:self.desktop_id,
                        absnormalChart: self.absnormalChart,
                        absnormalChart1: self.absnormalChart1,
                        lagstation_chart: self.lagstation_chart
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
            var line_c = parseInt(arg.line_id);
            //匹配line_id和desktop_id
            if (line_c == data_use.data.line_id&&data_use.controllerId == this.desktop_id) {
                self.model_abnormal.call("create", [
                    {
                        'line_id':'data_use.line_id',
                        'name': data_use.name,
                        'suggest': data_use.data.suggest,
                        'abnormal_description': data_use.data.abnormal_description,
                        'solution': data_use.data.solution
                    }]).then(function (res) {
                });
            }
        },
        show_echarts: function (data_list, arg) {
            var data_use = JSON.parse(data_list);
            function push_data(data_item, item) {
                var data_time = [];
                for (var i = 0; i < data_item.length; i++) {
                    data_time.push(data_item[i][item]);
                }
                return data_time;
            }
            //匹配line_id和desktop_id
            var line_c = parseInt(arg.line_id);
            if (data_use.data.lineId == line_c && data_use.controllerId == arg.desktop_id) {
                var timer =['8:00','9:00','10:00','11:00','12:00','13:00','14:00','15:00','16:00'];
                var forcast =[32+Math.random()*10+parseInt(data_use.data.lineId),30+Math.random()*12+parseInt(data_use.data.lineId),42+Math.random()*15+parseInt(data_use.data.lineId),45+Math.random()*8+parseInt(data_use.data.lineId),58+Math.random()*10+parseInt(data_use.data.lineId),35+Math.random()*10+parseInt(data_use.data.lineId),61+Math.random()*10+parseInt(data_use.data.lineId),46+Math.random()*10+parseInt(data_use.data.lineId),52+Math.random()*10+parseInt(data_use.data.lineId)];
                var real =[34+Math.random()*10,28+Math.random()*10+parseInt(data_use.data.lineId),41+Math.random()*10+parseInt(data_use.data.lineId),46+Math.random()*10+parseInt(data_use.data.lineId),59+Math.random()*10+parseInt(data_use.data.lineId),32+Math.random()*10+parseInt(data_use.data.lineId),46+Math.random()*10+parseInt(data_use.data.lineId),40+Math.random()*10+parseInt(data_use.data.lineId),38+Math.random()*10+parseInt(data_use.data.lineId)];
                var res = data_use.data.dataList;
                // for(var i = 0;i<res.length;i++){
                //     timer.push(res[i].datetime);
                //     forcast.push(parseInt(res[i].Passenger_flow_forcast)+Math.random()*10);
                //     real.push(parseInt(res[i].Passenger_flow_real)+Math.random()*10);
                // }
                // var data_time = [];
                // var dataJson_passenger_flow_real = [];
                // var dataJson_transport_capacity_plan = [];
                // var dataJson_transport_capacity_suggest = [];
                // for (var i = 0; i < data_use.data.passenger_flow_real.length; i++) {
                //     data_time.push(data_use.data.passenger_flow_real[i].datetime.split(' ')[1]);
                // }
                // push_data(data_use.data.passenger_flow_real, 'passenger_flow');
                // push_data(data_use.data.transport_capacity_plan, 'capacity');
                // push_data(data_use.data.transport_capacity_suggest, 'capacity');
                // for (var j = 0; j < data_use.data.transport_capacity_plan.length; j++) {
                //     dataJson_passenger_flow_real.push(data_use.data.passenger_flow_real[j].passenger_flow);
                // }
                // for (var j = 0; j < data_use.data.transport_capacity_plan.length; j++) {
                //     dataJson_transport_capacity_plan.push(data_use.data.transport_capacity_plan[j].capacity);
                // }
                // for (var k = 0; k < data_use.data.transport_capacity_suggest.length; k++) {
                //     dataJson_transport_capacity_suggest.push(data_use.data.transport_capacity_suggest[k].capacity);
                // }
                chartLineBar(arg.absnormalChart, 1, ["#ff4634", "#4dcfc7", "#ffd275", "#cc2123"], 'line', false, ['预测客流', '实际客流'], optionLineBar, timer, [forcast, real], '',data_use.data.lineId);
                // // 轮播克隆出的的图表
                chartLineBar(arg.absnormalChart1, 1, ["#ff4634", "#4dcfc7", "#ffd275", "#cc2123"], 'line', false, ['预测客流', '实际客流'], optionLineBar, timer, [forcast, real], '',data_use.data.lineId);
                // chartLineBar(arg.lagstation_chart, 0, ["#ff4634", "#4dcfc7"], 'bar', true, ['滞站客流', '预测滞站'], optionLineBar, ['周一', '周二', '周三', '周四', '周五', '周六'], [[120, 152, 101, 134, 90, 230], [220, 182, 191, 234, 290, 330]], '');
            }
        },
        closeFn: function () {
            var self = this;
            var tid = self.$el.attr('tid');
            var line_id = self.$el.attr('line_id');
            self.$el.parent().find('.dispatch_desktop').find('.line_edit').hide();
            self.$el.parent().find('.dispatch_desktop').find('.show_right').css('display', 'inline-block');
            self.model2.call("write", [parseInt(tid),
                {
                    'tem_display': 'none',
                    'position_left': self.$el[0].offsetLeft,
                    'position_top': self.$el[0].offsetTop,
                    'position_z_index': self.$el[0].style.zIndex
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
            this.$el.find('.carousel_content.abnormal_active').removeClass('abnormal_active');
            this.$el.find('.abs_info .absnormal_height').eq(0).remove();
            this.$el.find('.real_time_process').show().css("display", "none");
            // $.ajax({
            //         url: 'http://202.104.136.228:8080/ltyop/resource/exceptionHandle?apikey=71029270&params={onBoardId:15745,exceptKm:10,exceptStationId:13655,exceptReasonId:6}',
            //         type: 'post',
            //         dataType: 'json',
            //         data: {},
            //         success: function (data) {
            //
            //         }
            //     });
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
                this.$el.find('.carousel_content').addClass('abnormal_active');
                $(x_comp).parent().hide().siblings().show();
            }
        }
    });
    return dispatch_updown_line;
});