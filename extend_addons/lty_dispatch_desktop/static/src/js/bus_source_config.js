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
        init: function (parent, data) {
            this._super(parent, data);
            this.location_data = data;
        },
        start: function () {
            var self = this;
            self.$el.find('.line_src li').click(function () {
                $(this).addClass('active').siblings().removeClass('active');
                console.log($(this).index())
                self.$el.find('.src_content>div').eq($(this).index()).show().siblings().hide();
            });
            var signal_status = this.$el.find('.signal_status');
            for(var i =0;i<signal_status.length;i++){
                if(signal_status[i].innerHTML == '异常'){
                signal_status[i].style.color = '#BE4151';
            }else{
                signal_status[i].style.color = '#5D90D1';
            }
            }

        },
        events: {
            'click .position_site': 'show_map',
            'click .dis_close_bt': 'closeFn',
            'click .add_btn':'change_set',
            'click .config_bus_source div a':'close_set'
        },
        change_set:function () {
            this.$el.find('.config_bus_source').slideDown();
        },
        closeFn: function () {
            this.destroy();
        },
        close_set:function () {
            this.$el.find('.config_bus_source').slideUp();
        },
        show_map: function () {
            var self = this;
            new map(this).appendTo(self.$el);
        }
    });
    var map = Widget.extend({
        template: "WidgetGaodeCoordinates",
        init: function (parent, data) {
            this._super(parent, data);
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

    })
    return bus_source_config;
});