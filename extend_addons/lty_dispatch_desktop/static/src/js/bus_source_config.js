/**
 * Created by Administrator on 2017/7/25.
 */
odoo.define('lty_dispatch_desktop.bus_source_config', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var Model = require('web.Model');
    var bus_source_config = Widget.extend({
        template:"bus_source_config",
        init: function (parent, data) {
            this._super(parent, data);
            this.location_data = data;
        },
        start: function () {
            var self = this;
            // self.$el.append(QWeb.render("config"));
            self.$el.find('.line_src li').click(function () {
                $(this).addClass('active').siblings().removeClass('active');
                self.$el.find('.src_content').find('div').eq($(this).index()).show().siblings().hide();
            });
        },
        events:{
            'click .position_site':'show_map',
            'click .close_bt': 'closeFn'
        },
        closeFn: function(){
            this.destroy();
        },
        show_map:function () {
        }
    });
    return bus_source_config;
});