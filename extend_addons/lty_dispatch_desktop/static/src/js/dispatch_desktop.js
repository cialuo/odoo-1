odoo.define('lty_dispatch_desktop.dispatch_desktop', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var dispatch_bus = require('lty_dispaych_desktop.getWidget');
    //导入模块用户后台交互
    var Model = require('web.Model');
    var config = Widget.extend({
        template: "config",
        init: function (parent, context) {
            this._super(parent, context);
        },
        start: function () {
            var self = this;
            // self.$el.append(QWeb.render("config"));
        },
        events: {
            'click .btn_cancel': 'close_dialog',
            'click .config_btn': 'change_style'
        },
        close_dialog: function () {
            var self = this;
            self.$el.find('.modal').modal('hide');
            $(".modal-backdrop").remove();
            self.$el.remove();
        },
        change_style: function () {
            var self = this;
            var font_color = self.$el.find('.src_font_color').val();
        }

    });
    var desktop_top = Widget.extend({
        template: 'desktop_top',
        init: function (parent, context) {
            this._super(parent, context);
            this.data = {
                component_ids: 13
            };
        },
        start: function () {
            // 动态加载高德地图api
            $.getScript("http://webapi.amap.com/maps?v=1.3&key=cf2cefc7d7632953aa19dbf15c194019");
            var self = this;
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
    var dispatch_desktop = Widget.extend({
        template: 'dispatch_desktop_component',
        init: function (parent, context) {
            this._super(parent, context);
            this.model2 = new Model('dispatch.control.desktop.component');
        },
        start: function () {
            var self = this;
            self.$el.addClass('back_style');
            self.$el.append(QWeb.render("myConsole"));
            self.model2.query(["line_id"]).filter([["desktop_id", "=", 2]]).all().then(function (data) {
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
                        self.model2.query().filter([["line_id", "=", parseInt(s[j])]]).all().then(function (res) {
                            new dispatch_bus(this, res,0).appendTo(self.$el);
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
            new dispatch_bus(this, '',1).appendTo(self.$el);
        },
        config_click: function () {
            var self = this;
            var a = new config(this);
            a.appendTo(self.$el);
            self.$el.find('.modal').modal({backdrop: 'static', keyboard: false});
        },
        save_click: function () {
            var self = this;
            //客流
                var tidNum = self.$el .find('div[tid]');
                if (tidNum.length>0) {
                    for (var i = 0; i < tidNum.length; i++) {
                        var id = tidNum[i].getAttribute('tid');
                        var left = tidNum[i].style.left.split('px')[0];
                        var top = tidNum[i].style.top.split('px')[0];
                        var zIndex = parseInt(tidNum[i].style.zIndex);
                        self.model2.call("write", [parseInt(id),
                            {
                                'position_left': left,
                                'position_top': top,
                                'position_z_index': zIndex,
                            }]).then(function (data) {

                        });
                    }
                }
        }
    });
    core.action_registry.add('dispatch_desktop.page', dispatch_desktop);
});