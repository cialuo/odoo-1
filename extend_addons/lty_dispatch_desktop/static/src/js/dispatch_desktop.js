odoo.define('lty_dispatch_desktop.dispatch_desktop', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var dispatch_bus = require('lty_dispaych_desktop.getWidget');
    //导入模块用户后台交互
    var Model = require('web.Model');
    var config_parameter = new Model('ir.config_parameter');
    // 控制台配置模块
    var config = Widget.extend({
        template: "config",
        init: function (parent, context) {
            this._super(parent, context);
            this.model_config = new Model('dispatch.control.desktop');
        },
        start: function () {
            var self = this;
            this.desktop_id = this.$el.parents(".back_style").attr("desktop_id");
            this.model_config.query().filter([["id", "=", parseInt(this.desktop_id)]]).all().then(function (conf) {
                for (var i = 0, chkLen = $('.src_config').length; i < chkLen; i++) {
                    var chg_name = $('.src_config').eq(i).attr('class').split('conf_')[1];
                    if (conf[0][chg_name] == true) {
                        $('.src_config').eq(i).prop("checked", true);
                    }
                }
                self.$el.find('.src_font_color').val(conf[0].src_font_conf);
            });
            this.$el.on('hide.bs.modal', function () {
                self.destroy();
            });
        },
        events: {
            'click .btn_cancel': 'close_dialog',
            'click .config_btn': 'change_style'
        },
        close_dialog: function () {
            var self = this;
        },
        // 配置修改颜色
        change_style: function () {
            var self = this;
            var chg_sty = {};
            for (var i = 0, chkLen = $('.src_config').length; i < chkLen; i++) {
                var chg_name = $('.src_config').eq(i).attr('class').split('conf_')[1];
                if ($('.src_config').eq(i).is(":checked")) {
                    chg_sty[chg_name] = true;
                } else {
                    chg_sty[chg_name] = false;
                }
            }
            var now_clr_sty = self.$el.find('.src_font_color').val();
            this.model_config.call("write", [parseInt(self.desktop_id),
                {
                    'applycar_num': chg_sty['applycar_num'],
                    'active_car': chg_sty['active_car'],
                    'main_outage': chg_sty['main_outage'],
                    'share_active_car': chg_sty['share_active_car'],
                    'signal_online': chg_sty['signal_online'],
                    'car_driver': chg_sty['car_driver'],
                    'car_attendant': chg_sty['car_attendant'],
                    'trailerNum': chg_sty['trailerNum'],
                    'src_font_conf': now_clr_sty
                }]).then(function (res) {
                self.$el.find('.btn-default').click();
                for (var m = 0, cg_ln = Object.keys(chg_sty); m < cg_ln.length; m++) {
                    if (chg_sty[cg_ln[m]] == true) {
                        $('body').find('.bus_info .show_' + cg_ln[m]).show();
                    } else {
                        $('body').find('.bus_info .show_' + cg_ln[m]).hide();
                    }
                }
                $('body').find('.bus_info>ul>li').css('color', now_clr_sty);
            });
        }
    });
    // 控制台顶部
    var desktop_top = Widget.extend({
        template: 'desktop_top',
        init: function (parent, context) {
            this._super(parent, context);
            this.data = {
                component_ids: 13
            };
        },
        start: function () {
            var self = this;
            $('.desktop_head_deal.dd_person').html("调度员:" + odoo.session_info.name);
            function startTime() {
                var today = new Date();//定义日期对象
                var yyyy = today.getFullYear();//通过日期对象的getFullYear()方法返回年
                var MM = today.getMonth() + 1;//通过日期对象的getMonth()方法返回年
                var dd = today.getDate();//通过日期对象的getDate()方法返回年
                var hh = today.getHours();//通过日期对象的getHours方法返回小时
                var mm = today.getMinutes();//通过日期对象的getMinutes方法返回分钟
                var ss = today.getSeconds();//通过日期对象的getSeconds方法返回秒
                // 如果分钟或小时的值小于10，则在其值前加0，比如如果时间是下午3点20分9秒的话，则显示15：20：09
                MM = checkTime(MM);
                dd = checkTime(dd);
                mm = checkTime(mm);
                ss = checkTime(ss);
                var day; //用于保存星期（getDay()方法得到星期编号）
                if (today.getDay() == 0) day = "星期日 "
                if (today.getDay() == 1) day = "星期一 "
                if (today.getDay() == 2) day = "星期二 "
                if (today.getDay() == 3) day = "星期三 "
                if (today.getDay() == 4) day = "星期四 "
                if (today.getDay() == 5) day = "星期五 "
                if (today.getDay() == 6) day = "星期六 "
                self.$el.find('#nowDateTimeSpan').html(yyyy + "-" + MM + "-" + dd + " " + hh + ":" + mm + ":" + ss + "   " + day);
                setTimeout(startTime, 1000);//每一秒中重新加载startTime()方法
            }

            function checkTime(i) {
                if (i < 10) {
                    i = "0" + i;
                }
                return i;
            }

            startTime();
        }
    });
    //控制台总组件
    var dispatch_desktop = Widget.extend({
        template: 'dispatch_desktop_component',
        init: function (parent, context) {
            this._super(parent, context);
            this.model_line = new Model('dispatch.control.desktop.component');
            layer.close(context);
        },
        start: function () {
            $.getScript("http://webapi.amap.com/maps?v=1.3&key=cf2cefc7d7632953aa19dbf15c194019");
            $.getScript("/lty_dispatch_desktop/static/src/js/websocket.js");
            var self = this;
            if (window.location.href.split("action=")[1].split('&')[0] != undefined) {
                if (window.location.href.split("action=")[1].split('&')[0] == "dispatch_desktop.page") {
                    $('body').find('.o_content').css('overflow', 'hidden');
                }
            }
            self.$el.append(QWeb.render("myConsole"));
            var desktop_id = window.location.href.split("active_id=")[1].split("&")[0];
            self.$el.parent().addClass("controller_" + desktop_id).attr("desktop_id", desktop_id);
            self.model_line.query(["line_id"]).filter([["desktop_id", "=", parseInt(desktop_id)]]).all().then(function (data) {
                var s = [];
                if (data.length > 0) {
                    // 去重
                    for (var i = 0; i < data.length; i++) {
                        if (s.indexOf(data[i].line_id[0]) == -1) {  //判断在s数组中是否存在，不存在则push到s数组中
                            s.push(data[i].line_id[0]);
                        }
                    }
                    // 遍历
                    for (var j = 0; j < s.length; j++) {
                        self.model_line.query().filter([["desktop_id", "=", parseInt(desktop_id)], ["line_id", "=", parseInt(s[j])]]).all().then(function (res) {
                            new dispatch_bus(this, res, 0).appendTo(self.$el);
                        });
                    }
                }
            });
            new desktop_top(this).appendTo(self.$el);
        },
        events: {
            'click .new_console': 'addLine_click',
            'click .read_console': 'config_click',
            'click .save_console': 'save_click'
        },
        addLine_click: function () {
            var self = this;
            new dispatch_bus(this, '', 1).appendTo(self.$el);
        },
        config_click: function () {
            var self = this;
            var config_act = new config(this);
            config_act.appendTo(self.$el);
            self.$el.find('.info_config .modal').modal({backdrop: 'static', keyboard: false});
        },
        save_click: function () {
            var self = this;
            //客流
            var tidNum = self.$el.find('div[tid]');
            if (tidNum.length > 0) {
                for (var i = 0; i < tidNum.length; i++) {
                    var id = tidNum[i].getAttribute('tid');
                    var left = tidNum[i].style.left.split('px')[0];
                    var top = tidNum[i].style.top.split('px')[0];
                    self.model_line.call("write", [parseInt(id),
                        {
                            'position_left': left,
                            'position_top': top,
                            'position_z_index': 0
                        }]).then(function (data) {
                        layer.msg('保存成功');
                    });
                }
            }
        }
    });
    var dispatch_control = Widget.extend({
        template: 'dispatch_control',
        init: function (parent, context) {
            this._super(parent, context);
            this.layer = layer.msg("加载中...", {time: 0, shade: 0.3});
        },
        start: function () {
            this.load_fn();
        },
        load_fn: function () {
            var self = this;
            config_parameter.query().filter([["key", "=", "dispatch.desktop.socket"]]).all().then(function (socket) {
                config_parameter.query().filter([["key", "=", "dispatch.desktop.restful"]]).all().then(function (restful) {
                    SOCKET_URL = socket[0].value;
                    RESTFUL_URL = restful[0].value;
                    new dispatch_desktop(self, self.layer).appendTo(self.$el); 
                });
            });
        }
    });
    core.action_registry.add('dispatch_desktop.page', dispatch_control);
});