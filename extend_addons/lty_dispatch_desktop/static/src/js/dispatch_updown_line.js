/**
 * Created by Administrator on 2017/7/20.
 */
odoo.define('lty_dispaych_desktop.updown_line', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var Model = require('web.Model');
    var dispatch_updown_line = Widget.extend({
        template: 'updown_line_table',
        init: function (parent, data, rendr_index) {
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
            socket_model_info[model_abnormal] = {
                arg: {
                    self: self,
                    line_id: self.line_id
                }, fn: self.abnormal_save
            };
            if (self.$el.find('.absnormal_chart')[0] != undefined) {
                self.absnormalChart = echarts.init(self.$el.find('.absnormal_chart')[0]);
                self.absnormalChart1 = echarts.init(self.$el.find('.absnormal_chart')[1]);
                self.lagstation_chart = echarts.init(self.$el.find('.lagstation_chart')[0]);
                socket_model_info[model_chart] = {
                    arg: {
                        self: self,
                        line_id: self.line_id,
                        desktop_id: self.desktop_id,
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
            'click .min': 'closeFn',
            'click .abnormal_ignore': 'abnormal_ignore',
            'click .abnormal_agree': 'abnormal_agree',
            'click .abnormal_refuse': 'abnormal_refuse',
            'click .is_ignore': 'is_ignore',
            'click .is_agree': 'is_agree',
            'click .is_refuse': 'is_refuse',
            'click .not_ignore': 'not_ignore',
            'click .not_agree': 'not_agree',
            'click .not_refuse': 'not_refuse',

        },
        is_refuse: function (event) {
            stopPropagation(event);
            var send_id = parseInt(this.$el.find('.abs_info .absnormal_height .man_deal').eq(0).attr('id'));
            $.ajax({
                url: RESTFUL_URL + '/ltyop/exchange/processCommand?apikey=71029270&params={warningId:' + send_id + ',agreeTypeId:2}',
                type: 'put',
                dataType: 'json',
                data: {},
                success: function (res) {
                    layer.msg(res.respose.text);
                }
            });
            this.$el.find('.abs_info .absnormal_height').eq(0).remove();
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
                $(x_comp).parent().hide().siblings('.handleBtn').show();
                if (this.$el.find('.abs_info .absnormal_height p').eq(0).hasClass('man_deal')) {
                    $(x_comp).parent().siblings('.handleBtn').find('button').removeAttr('disabled');
                } else {
                    $(x_comp).parent().siblings('.handleBtn').find('button').attr('disabled', 'disabled');
                }
            }
        },
        is_agree: function (event) {
            stopPropagation(event);
            var x_comp = event.currentTarget;
            var send_id = parseInt(this.$el.find('.abs_info .absnormal_height .man_deal').eq(0).attr('id'));
            $.ajax({
                url: RESTFUL_URL + '/ltyop/exchange/processCommand?apikey=71029270&params={warningId:' + send_id + ',agreeTypeId:3}',
                type: 'put',
                dataType: 'json',
                data: {},
                success: function (res) {
                    layer.msg(res.respose.text);
                }
            });
            this.$el.find('.abs_info .absnormal_height').eq(0).remove();
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
                $(x_comp).parent().hide().siblings('.handleBtn').show();
                if (this.$el.find('.abs_info .absnormal_height p').eq(0).hasClass('man_deal')) {
                    $(x_comp).parent().siblings('.handleBtn').find('button').removeAttr('disabled');
                } else {
                    $(x_comp).parent().siblings('.handleBtn').find('button').attr('disabled', 'disabled');
                }
            }
        },
        not_ignore: function (event) {
            stopPropagation(event);
            var x_deal = event.currentTarget;
            $(x_deal).parent().siblings('.abs_info').find('.absnormal_sug h4').eq(0).removeClass('toRed').html('建议');
            $(x_deal).parent().hide().siblings('.handleBtn').show();
        },
        not_agree: function (event) {
            stopPropagation(event);
            var x_deal = event.currentTarget;
            $(x_deal).parent().siblings('.abs_info').find('.absnormal_sug h4').eq(0).removeClass('toRed').html('建议');
            $(x_deal).parent().hide().siblings('.handleBtn').show();
        },
        not_refuse: function (event) {
            stopPropagation(event);
            var x_deal = event.currentTarget;
            $(x_deal).parent().siblings('.abs_info').find('.absnormal_sug h4').eq(0).removeClass('toRed').html('建议');
            $(x_deal).parent().hide().siblings('.handleBtn').show();
        },
        is_ignore: function (event) {
            stopPropagation(event);
            var x_comp = event.currentTarget;
            this.$el.find('.carousel_content.abnormal_active').removeClass('abnormal_active');
            var send_id = parseInt(this.$el.find('.abs_info .absnormal_height .man_deal').eq(0).attr('id'));
            $.ajax({
                url: RESTFUL_URL + '/ltyop/exchange/processCommand?apikey=71029270&params={warningId:' + send_id + ',agreeTypeId:1}',
                type: 'put',
                dataType: 'json',
                data: {},
                success: function (res) {
                    layer.msg(res.respose.text);
                }
            });
            this.$el.find('.abs_info .absnormal_height').eq(0).remove();
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
                $(x_comp).parent().hide().siblings('.handleBtn').show();
                if (this.$el.find('.abs_info .absnormal_height p').eq(0).hasClass('man_deal')) {
                    $(x_comp).parent().siblings('.handleBtn').find('button').removeAttr('disabled');
                } else {
                    $(x_comp).parent().siblings('.handleBtn').find('button').attr('disabled', 'disabled');
                }
            }
        },
        abnormal_ignore: function (event) {
            stopPropagation(event);
            var x_deal = event.currentTarget;
            $(x_deal).parent().siblings('.abs_info').find('.absnormal_sug h4').eq(0).addClass('toRed').html('确定要忽略这个异常？');
            $(x_deal).parent().hide().siblings('.ignore_btn').show();
        },
        abnormal_agree: function (event) {
            stopPropagation(event);
            var x_deal = event.currentTarget;
            $(x_deal).parent().siblings('.abs_info').find('.absnormal_sug h4').eq(0).addClass('toRed').html('确定要同意这个异常吗？');
            $(x_deal).parent().hide().siblings('.agree_btn').show();
        },
        abnormal_refuse: function (event) {
            stopPropagation(event);
            var x_deal = event.currentTarget;
            $(x_deal).parent().siblings('.abs_info').find('.absnormal_sug h4').eq(0).addClass('toRed').html('确定要同意这个异常吗？');
            $(x_deal).parent().hide().siblings('.refuse_btn').show();
        },
        abnormal_save: function (datalist, arg) {
            var self = arg.self;
            var data_use = JSON.parse(datalist);
            // if(data_use.line_id == parseInt(arg.line_id))
            var line_c = parseInt(arg.line_id);
            //匹配line_id和desktop_id

            if (data_use.data.line_id == line_c && data_use.controllerId == self.desktop_id) {
                var dom = self.$el;
                var dom_singal = $('body').find('.dispatch_desktop[line_id=' + data_use.data.line_id + ']');
                dom.find('.no_absnormal').eq(0).show().siblings().hide();
                var abnoraml_desc = $('body').find('.absnormal_diaodu .absnormal_type p');
                abnoraml_desc.removeClass('man_deal');
                //车辆掉线
                if (data_use.data.packageType == 1003) {
                    abnoraml_desc.html('车辆' + data_use.data.abnormal_description.bus_no + '掉线');
                    dom_singal.find('.line_car[bus_no=' + data_use.data.abnormal_description.bus_no + ']').addClass('to_gray').removeClass('.to_red').removeClass('.to_yellow');
                    dom_singal.find('.show_signal_online span').html(parseInt(dom_singal.find('.show_signal_online span').html()) - 1);
                    dom_singal.find('.show_signal_outline span').html(parseInt(dom_singal.find('.show_signal_outline span').html()) + 1);
                }
                // 出勤异常
                else if (data_use.data.packageType == 1004) {
                    abnoraml_desc.html('（员工）' + data_use.data.abnormal_description.staff_name + '：考勤异常');
                }
                // 到站准点异常
                else if (data_use.data.packageType == 1005) {
                    abnoraml_desc.html(data_use.data.abnormal_description.bus_no + '到达站点：' + data_use.data.abnormal_description.station_name + '与' + data_use.data.abnormal_description.actual_time + '相差' + data_use.data.abnormal_description.diff_time);
                }
                // 到站预测准点异常
                else if (data_use.data.packageType == 1006) {
                    abnoraml_desc.html(data_use.data.abnormal_description.bus_no + '到达站点：' + data_use.data.abnormal_description.station_name + '与' + data_use.data.abnormal_description.actual_time + '相差' + data_use.data.abnormal_description.diff_time);
                }
                // 趟次回场异常包
                else if (data_use.data.packageType == 1007) {
                    abnoraml_desc.html('车辆' + data_use.data.abnormal_description.bus_no + ',回场停车时间为：' + data_use.data.abnormal_description.return_time + ',回场异常');
                }
                // 趟次回场严重异常
                else if (data_use.data.packageType == 1008) {
                    abnoraml_desc.html('车辆' + data_use.data.abnormal_description.bus_no + ',回场停车时间为：' + data_use.data.abnormal_description.return_time + ',回场严重异常');
                }
                // 车越界行驶
                else if (data_use.data.packageType == 1009) {
                    abnoraml_desc.html('车辆' + data_use.data.abnormal_description.bus_no + '偏离路线');
                }
                // 异常滞留
                else if (data_use.data.packageType == 1010) {
                    abnoraml_desc.html('车辆' + data_use.data.abnormal_description.bus_no + '已在途中停车' + data_use.data.abnormal_description.bus_stop_time);
                }
                // 前车距离异常
                else if (data_use.data.packageType == 1011) {
                    abnoraml_desc.html('前车辆' + data_use.data.abnormal_description.front_bus_no + '与后车' + data_use.data.abnormal_description.behind_bus_no + ',疑似串车/大间隔');
                }
                // 超速异常
                else if (data_use.data.packageType == 1012) {
                    abnoraml_desc.html('车辆' + data_use.data.abnormal_description.bus_no + '超速,最高时速为' + data_use.data.abnormal_description.highest_speed);
                }
                // 事故异常
                else if (data_use.data.packageType == 1013) {
                    if (data_use.data.abnormal_description.operateFlag == 0) {
                        abnoraml_desc.html('车辆' + data_use.data.abnormal_description.bus_no + '员工' + data_use.data.abnormal_description.employee_name + data_use.data.abnormal_description.log_text).addClass('man_deal').attr('id', data_use.data.abnormal_description.id);
                        if (self.$el.find('.passenger_flow_list .abs_info .absnormal_height').length == 0) {
                            self.$el.find('.handleBtn').find('button').removeAttr('disabled');
                        }
                    } else {
                        self.$el.find('.passenger_flow_list .abs_info .absnormal_height p.man_deal[id=' + data_use.data.abnormal_description.id + ']').parents('.absnormal_height').remove();
                        // 如果不存在异常了
                        if (self.$el.find('.passenger_flow_list .abs_info .absnormal_height').length == 0) {
                            // self.$el.find('.handleBtn').find('button').removeAttr('disabled');
                            self.$el.find('.handleBtn').show();
                            self.$el.removeClass('warn');
                            self.$el.find('.normal').show().siblings().hide();
                            var content = '.' + self.$el.find('.carousel_content')[0].className;
                            carousel({
                                content: content,
                                self: self
                            });
                            // 如果还有异常
                        } else if (self.$el.find('.passenger_flow_list .abs_info .absnormal_height').length > 0) {
                            // 如果这个异常不是手动的
                            if (!self.$el.find('.passenger_flow_list .abs_info .absnormal_height p').eq(0).hasClass('.man_deal')) {
                                self.$el.find('.handleBtn').find('button').attr('disabled', 'disabled');
                            }
                        }
                        return
                    }
                }
                // 扣车异常
                else if (data_use.data.packageType == 1014) {
                    abnoraml_desc.html('车辆' + data_use.data.abnormal_description.bus_no + '员工' + data_use.data.abnormal_description.employee_no + '疑似扣车');
                }
                // 抛锚预警
                else if (data_use.data.packageType == 1015) {
                    abnoraml_desc.html('车辆' + data_use.data.abnormal_description.bus_no + '员工' + data_use.data.abnormal_description.employee_no + '疑似抛锚');
                }
                // 提前或延后发车
                else if (data_use.data.packageType == 1016) {
                    abnoraml_desc.html('车辆' + data_use.data.abnormal_description.bus_no + '员工' + data_use.data.abnormal_description.employee_name + '提前发车,提前' + data_use.data.abnormal_description.advance_time + '分钟');
                }
                // 到点未发车
                else if (data_use.data.packageType == 1017) {
                    if (data_use.data.abnormal_description.retention_time < 0) {
                        abnoraml_desc.html('车辆' + data_use.data.abnormal_description.bus_no + '员工' + data_use.data.abnormal_description.employee_name + '到点未发车,滞后' + (-1 * data_use.data.abnormal_description.retention_time) + '分钟');
                    } else if (data_use.data.abnormal_description.retention_time > 0) {
                        abnoraml_desc.html('车辆' + data_use.data.abnormal_description.bus_no + '员工' + data_use.data.abnormal_description.employee_name + '到点未发车,滞后' + data_use.data.abnormal_description.retention_time + '分钟');
                    }
                }
                // 意外高峰
                else if (data_use.data.packageType == 1018) {
                    abnoraml_desc.html(data_use.data.abnormal_description.date_start + '到' + data_use.data.abnormal_description.date_end + '产生意外客流高峰');
                }
                // 时段意外低峰
                else if (data_use.data.packageType == 1019) {
                    abnoraml_desc.html(data_use.data.abnormal_description.date_start + '到' + data_use.data.abnormal_description.date_end + '产生意外客流高峰');
                }
                // 站点意外高峰
                else if (data_use.data.packageType == 1020) {
                    abnoraml_desc.html('站点' + data_use.data.abnormal_description.station + ',' + data_use.data.abnormal_description.date_start + '到' + data_use.data.abnormal_description.date_end + '产生意外高峰');
                }
                // 站点意外低峰
                else if (data_use.data.packageType == 1021) {
                    abnoraml_desc.html('站点' + data_use.data.abnormal_description.station + ',' + data_use.data.abnormal_description.date_start + '到' + data_use.data.abnormal_description.date_end + '产生意外低峰');
                }
                $('body').find('.absnormal_diaodu .absnormal_sug p').html(data_use.data.suggest);
                dom.addClass('warn').find('.passenger_flow_list').eq(0).find('.abs_info').append($('body').find('.absnormal_diaodu').html());
                self.model_abnormal.call("create", [
                    {
                        'line_id': data_use.data.line_id,
                        'name': data_use.name,
                        'suggest': data_use.data.suggest,
                        'abnormal_description': abnoraml_desc.html(),
                        'solution': data_use.data.solution,
                        'package_type': data_use.data.packageType
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
                var timer_real = [];
                var timer_pre = [];
                var forcast = [];
                var real = [];
                var res = data_use.data;
                for (var i = 0; i < res.realPassengerData.length; i++) {
                    timer_real.push(res.realPassengerData[i].nowtime);
                    real.push(parseInt(res.realPassengerData[i].real_timePassengerFlow));
                }
                for (var j = 0; j < res.predictPassengerData.length; j++) {
                    timer_pre.push(res.predictPassengerData[j].nowtime)
                    forcast.push(parseInt(res.predictPassengerData[j].predictPassengerFlow));
                }
                chartLineBar(arg.absnormalChart, 1, ["#ff4634", "#4dcfc7", "#ffd275", "#cc2123"], 'line', false, ['预测客流', '实际客流'], optionLineBar, timer_pre, [forcast, real], '', res.lineName);
                // // 轮播克隆出的的图表
                chartLineBar(arg.absnormalChart1, 1, ["#ff4634", "#4dcfc7", "#ffd275", "#cc2123"], 'line', false, ['预测客流', '实际客流'], optionLineBar, timer_pre, [forcast, real], '', res.lineName);
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
                    'position_z_index': 0
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
                $(x_comp).parent().siblings('.handleBtn').find('button').attr('disabled', 'disabled');
                var content = '.' + this.$el.find('.carousel_content')[0].className;
                carousel({
                    content: content,
                    self: this
                });
            }
            else {
                this.$el.find('.carousel_content').addClass('abnormal_active');
                $(x_comp).parent().hide().siblings('.handleBtn').show();
                if (this.$el.find('.abs_info .absnormal_height p').eq(0).hasClass('man_deal')) {
                    $(x_comp).parent().siblings('.handleBtn').find('button').removeAttr('disabled');
                } else {
                    $(x_comp).parent().siblings('.handleBtn').find('button').attr('disabled', 'disabled');
                }
                // if(){
                //
                // }
            }
        }
    });
    return dispatch_updown_line;
});