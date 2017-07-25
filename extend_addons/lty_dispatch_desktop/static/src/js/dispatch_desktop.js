odoo.define('lty_dispatch_desktop.dispatch_desktop', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var dispatch_bus = require('lty_dispaych_desktop.getWidget');
    //导入模块用户后台交互
    var Model = require('web.Model');
    var config = Widget.extend({
        template:"config",
        init: function (parent, context) {
            this._super(parent, context);
        },
        start: function () {
            var self = this;
            // self.$el.append(QWeb.render("config"));
        },
        events: {
            'click .btn_cancel': 'close_dialog',
            'click .config_btn':'change_style'
        },
        close_dialog:function () {
            var self = this;
            self.$el.find('.modal').modal('hide');
            $(".modal-backdrop").remove();
            self.$el.remove();
        },
        change_style:function () {
            var self = this;
            var font_color=self.$el.find('.src_font_color').val();

        }

    });
    var dispatch_desktop = Widget.extend({
        init: function (parent, context) {
            this._super(parent, context);
            this.model = new Model('lty_dispatch_desktop.lty_dispatch_desktop');

        },
        start: function () {
            var self = this;
            var dis_desk = self.dis_desk;
            self.$el.append(QWeb.render("myConsole"));
            // self.model.call('unlink',[[4]]).then(function (data) {
            //     console.log(data);
            // });
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
        save_click:function () {
            var self = this;
            var ab = self.$el.find('.dispatch_desktop');
            var res=[]
            for (var i = 0;i<ab.length;i++){
                var id = ab[i].getAttribute('tid');
                var left = ab[i].offsetLeft;
                var top = ab[i].offsetTop;
                var zIndex = ab[i].style.zIndex;
                var show;
                if(ab[i].style.display==='block'){
                    show = 'block';
                }else{
                    show='none';
                }
                var map = {};
                map.id=id;
                map.left=left;
                map.top=top;
                map.zIndex=zIndex;
                map.show = show;
                res.push(map);
            }
            console.log(res);
        }
    })
    core.action_registry.add('dispatch_desktop.page', dispatch_desktop);
})