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
            this.desktop_id = this.$el.parents(".back_style").attr("desktop_id");
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
            var zIndex = parseInt(this.$el[0].style.zIndex)+1;
            var e = e || window.event;
            var options = {
                x: e.clientX + 5,
                y: e.clientY + 5,
                zIndex: zIndex,
                controllerId:this.desktop_id
            };
            var layer_map = layer.msg("加载中...", {time: 0, shade: 0.3});
            var elec_map_layer = {
                layer_map: layer_map
            }

            sessionStorage.setItem("elec_map_layer", JSON.stringify(elec_map_layer));
            new digital_map(this, options).appendTo($(".controller_" + options.controllerId));
        },
        get_main_controll_interface: function (e) {
            var zIndex = parseInt(this.$el[0].style.zIndex)+1;
            var options = {
                x: e.clientX + 5,
                y: e.clientY + 5,
                zIndex: zIndex,
                controllerId:this.desktop_id
            };
            new main_controll_interface(this, options).appendTo($(".controller_" + options.controllerId));
        }
    });
    var digital_map = Widget.extend({
        template: "digital_map",
        init: function (parent, data) {
            this._super(parent, data);
            this.location_data = data;
            socket_model_api_obj.electronicMapModel = {};
        },
        start: function () {
            var package_elmap = {
                type: 1000,
                open_modules: ["dispatch-bus_real_state-1"],
                msgId: Date.parse(new Date())
            };
            if (websocket){
                websocket.send(JSON.stringify(package_elmap));
            }
        },
        events: {
            'click .close_bt': 'closeFn'
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
            'click .min':'dis_closeFn',
            'click .bus_list a': 'chose_btn'
        },
        closeFn: function () {
            this.destroy();
        },
        dis_closeFn:function () {
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