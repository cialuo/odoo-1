/**
 * Created by Administrator on 2017/10/11.
 */
odoo.define('lty_dispatch_broadcast_monitor.broadcast_show', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var Model = require('web.Model');
    var QWeb = core.qweb;
    var ztree_show_dian = Widget.extend({
        template: 'ztree_show',
        init: function (parent) {
            this._super(parent);
        },
        start: function () {

        }
    });
    var broadcast_play = Widget.extend({
        template: 'dispatch_desktop_broadcast',
        init: function (parent) {
            this._super(parent);
        },
        start: function () {

        }
    });
    core.action_registry.add('lty_dispatch_broadcast_monitor.broadcast_play', broadcast_play);
});