/**
 * Created by Administrator on 2017/7/31.
 */
odoo.define('lty_dispatch_desktop.bus_site_info', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var Model = require('web.Model');
    var bus_site_info = Widget.extend({
        template: "bus_site_info",
        init: function (parent, data) {
            this._super(parent, data);
            this.location_data = data;
        },
        start: function () {
            var self = this;
        },
        events: {
            'click .del': 'bus_site_hide',
            'click .get_digital_map': 'get_digital_map',
            'click .get_main_controll_interface': 'get_main_controll_interface'
        },
        bus_site_hide: function () {
            this.destroy();
        },
        get_digital_map: function (e) {
            var zIndex = this.$el[0].style.zIndex;
            var e = e || window.event;
            var options = {
                x: e.clientX + 5,
                y: e.clientY + 5,
                zIndex: zIndex + 1
            };
            new digital_map(this, options).appendTo($('body'));
        },
        get_main_controll_interface: function (e) {
            var e = e || window.event;
            var options = {
                x: e.clientX + 5,
                y: e.clientY + 5,
                zIndex: 10
            };
            new main_controll_interface(this, options).appendTo($('body'));
        }
    });
    var digital_map = Widget.extend({
        template: "digital_map",
        init: function (parent, data) {
            this._super(parent, data);
            this.location_data = data;
        },
        start: function () {
            var tid = 1
            var map = new AMap.Map("digital_map", {
                resizeEnable: true,
                center: [114.408539, 30.465158],
                zoom: 12
            });
            var marker = new AMap.Marker({
                icon: "http://webapi.amap.com/theme/v1.3/markers/n/mark_b.png",
            });
            var model_id = 'model_' + tid;
            this.marker = marker;
            this.map = map;
            if (socket_model_info[model_id]) {
                delete socket_model_info[model_id];
            }
            socket_model_info[model_id] = {
                arg: {
                    self:this,
                    marker:this.marker,
                    map:this.map

                }, fn: this.setMessageInnerHTML
            };
        },
        events: {
            'click .close_bt': 'closeFn'
        },
        setMessageInnerHTML:function (innerHTML,arg) {
            var self = arg.self;
            var a = innerHTML.substring(78, 79);
                console.log(innerHTML)
                if (a) {
                    // 实例化点标记
                    var ab = [114.408 + a + 39, 30.461 + a + 58];
                    function addMarker() {
                       self.marker.setPosition(ab);
                       self.marker.setMap(self.map);
                    }
                    addMarker();
                }
        },
        closeFn: function () {
            this.destroy();
        }

    });
    var main_controll_interface = Widget.extend({
        template: 'main_controll_interface',
        init: function (parent, data) {
            this._super(parent, data);
            this.location_data = data;
        },
        start: function () {

        },
        events: {
            'click .close_bt': 'closeFn',
            'click .bus_list a': 'chose_btn'
        },
        closeFn: function () {
            this.destroy();
        },
        chose_btn: function (event) {
            var e = event || window.event;
            var x = e.currentTarget;
            $(x).addClass('active_a').parent().siblings().find('a').removeClass('active_a');
        }
    });
    return bus_site_info;
});