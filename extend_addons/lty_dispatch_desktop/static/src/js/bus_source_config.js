/**
 * Created by Administrator on 2017/7/25.
 */
odoo.define('lty_dispatch_desktop.bus_source_config', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var Model = require('web.Model');
    var bus_source_config = Widget.extend({
        template: "bus_source_config",
        init: function (parent,options,data) {
            this._super(parent,options,data);
            this.location_data = options;
            this.line_src = data;
        },
        start: function () {
            this.desktop_id = this.$el.parents(".back_style").attr("desktop_id");
            var self = this;
            var package_send = {
                type: 1000,
                open_modules: ["dispatch-abnormal-"+this.desktop_id,"dispatch-bus_real_state-"+this.desktop_id,"dispatch-bus_resource-"+this.desktop_id],
                msgId: Date.parse(new Date())
            };
            websocket.send(JSON.stringify(package_send));
            $('.table_bus_num_tbody').mCustomScrollbar({
                theme: 'minimal'
            });
            self.$el.find('.line_src li').click(function () {
                $(this).addClass('active').siblings().removeClass('active');
                self.$el.find('.src_content>div').eq($(this).index()).show().siblings().hide();
            });
            var signal_status = this.$el.find('.signal_status');
            for (var i = 0; i < signal_status.length; i++) {
                if (signal_status[i].innerHTML == '异常') {
                    signal_status[i].style.color = '#BE4151';
                    this.$el.find('.bus_license')[i].style.color = '#BE4151';
                } else {
                    signal_status[i].style.color = '#5D90D1';
                    this.$el.find('.bus_license')[i].style.color = '#5D90D1';
                }
            }

        },
        events: {
            'click .position_site': 'show_map',
            'click .min': 'closeFn',
            'click .add_btn': 'change_set',
            'click .config_bus_source div a': 'close_set'
        },

        change_set: function () {
            this.$el.find('.config_bus_source').slideDown();
        },
        closeFn: function () {
            this.destroy();
        },
        close_set: function () {
            this.$el.find('.config_bus_source').slideUp();
        },
        show_map: function (e) {
            var e = e || window.event;
            var zIndex = parseInt(this.$el[0].style.zIndex);
            var options = {
                x: e.clientX + 5,
                y: e.clientY + 5,
                zIndex: zIndex + 1,
                controllerId: this.desktop_id
            };
            var layer_map = layer.msg("加载中...", {time: 0, shade: 0.3});
            var driver_map_layer = {
                layer_map: layer_map
            }
            sessionStorage.setItem("elec_map_layer", JSON.stringify(driver_map_layer));
            new map(this, options).appendTo($(".controller_" + options.controllerId));
        }
    });
    var map = Widget.extend({
        template: "WidgetGaodeCoordinates",
        init: function (parent, data) {
            this._super(parent, data);
            this.location_data = data;
            // socket_model_api_obj.line_resource = {};
        },
        start: function () {


            var marker, map = new AMap.Map("container", {
                resizeEnable: true,
                center: [114.406839, 30.461158],
                zoom: 14
            });
            // 实例化点标记
            function addMarker() {
                marker = new AMap.Marker({
                    icon: "http://webapi.amap.com/theme/v1.3/markers/n/mark_b.png",
                    position: [114.406839, 30.461158]
                });
                marker.setMap(map);
            }

            addMarker();
        },
        events: {
            'click .map_destory': 'close_map'
        },
        close_map: function () {
            this.destroy();
        },
    })
    return bus_source_config;
});