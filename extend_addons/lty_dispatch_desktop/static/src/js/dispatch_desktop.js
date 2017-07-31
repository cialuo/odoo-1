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
        },
        start: function () {
            var self = this;
            new dispatch_desktop(this).appendTo(self.$el);
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
            this.data = {
                component_ids: 13
            };
            this.model = new Model('lty_dispatch_desktop.lty_dispatch_desktop');
            this.model2 = new Model('dispatch.control.desktop.component');
        },
        start: function () {
            var self = this;
            var dis_desk = self.dis_desk;
            self.$el.append(QWeb.render("myConsole"));

            self.model2.query().filter([["desktop_id", "=", 2]]).all().then(function (data) {
                console.log(data);
            });
            self.model.call('dispatch_desktop', [dis_desk]).then(function (data) {
                for (var i = 0; i < data.length; i++) {
                    var num_dispatch_bus = new dispatch_bus(this, data[i]);
                    num_dispatch_bus.appendTo(self.$el);
                }
            });
        },
        events: {
            'click .new_console': 'addLine_click',
            'click .read_console': 'config_click',
            'click .save_console': 'save_click'
        },
        addLine_click: function () {
            var self = this;
            var oneLine = new dispatch_bus(this, '');
            oneLine.appendTo(self.$el);
        },
        config_click: function () {
            var self = this;
            var a = new config(this);
            a.appendTo(self.$el);
            self.$el.find('.modal').modal({backdrop: 'static', keyboard: false});
        },
        save_click: function () {
            var self = this;
            var ab = self.$el.find('.dispatch_desktop');
            var res = []
            for (var i = 0; i < ab.length; i++) {
                var id = ab[i].getAttribute('tid');
                var left = ab[i].offsetLeft;
                var top = ab[i].offsetTop;
                var zIndex = ab[i].style.zIndex;
                var show;
                if (ab[i].style.display === 'block') {
                    show = 'block';
                } else {
                    show = 'none';
                }
                var map = {};
                map.id = id;
                map.left = left;
                map.top = top;
                map.zIndex = zIndex;
                // map.show = show;
                res.push(map);
            }
            self.model2.call("create", [{'line_id': 1, 'position_z_index': res[0].zIndex}]).then(function (data) {
            });
        }
    });
    core.action_registry.add('dispatch_desktop.page', desktop_top);
});