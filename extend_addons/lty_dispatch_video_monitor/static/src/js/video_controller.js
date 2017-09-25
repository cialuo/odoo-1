/**
 * Created by Administrator on 2017/9/22.
 */
odoo.define('', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var Model = require('web.Model');
    var video_play = Widget.extend({
        template:'dispatch_desktop_video',
        init:function (parent) {
            this._super(parent);
        },
        start:function () {
        }
    });
    core.action_registry.add('lty_dispatch_video_monitor.video_play', video_play);
});