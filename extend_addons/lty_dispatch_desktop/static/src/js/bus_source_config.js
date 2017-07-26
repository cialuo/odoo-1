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
        init: function (parent, context) {
            this._super(parent, context);
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
            'click .position_site':'show_map'
        },
        show_map:function () {

        }

    });
    var driver_map_info = Widget.extend({
            template:"dirver_map_info",
            init:function (parent, context) {
                this._super(parent, context);
            },
            start: function () {
                var self = this;
            }
    })
    core.action_registry.add('bus_source_config.page', bus_source_config);
});