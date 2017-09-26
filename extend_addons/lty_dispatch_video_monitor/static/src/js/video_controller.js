/**
 * Created by Administrator on 2017/9/22.
 */
odoo.define('lty_dispatch_video_monitor.video_show', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var Model = require('web.Model');
    var QWeb = core.qweb;
    var video_play = Widget.extend({
        init: function (parent) {
            this._super(parent);
        },
        start: function () {
            window.location.href+='&type=live';
            this.$el.append(QWeb.render("dispatch_desktop_video"));
            var swfVersionStr = "10.3.0";
            var xiSwfUrlStr = "/lty_dispatch_video_monitor/static/src/swfs/playerProductInstall.swf";
            var queryParameters = new Array();

            function getUrlParam(name) {
                name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
                var regexS = "[\\?&]" + name + "=([^&#]*)";
                var regex = new RegExp(regexS);
                var results = regex.exec(window.location.href);
                if (results == null)
                    return "";
                else
                    return unescape(results[1]);
            }

            queryParameters['source'] = getUrlParam('source');
            queryParameters['type'] = getUrlParam('type');
            if (queryParameters['source'] == "") {
                queryParameters['source'] = "rtmp://58.82.168.196:49983/myapp/40134_0";
            }

            if (queryParameters['type'] == "") {
                queryParameters['type'] = "recorded";
            }

            if (queryParameters['idx'] == "") {
                queryParameters['idx'] = "2";
            }
            var soFlashVars = {
                src: queryParameters['source'],
                streamType: queryParameters['type'],
                autoPlay: "true",
                controlBarAutoHide: "true",
                controlBarPosition: "bottom"
            };
            var params = {};
            params.quality = "high";
            params.bgcolor = "#000000";
            params.allowscriptaccess = "sameDomain";
            params.allowfullscreen = "true";
            params.play = false;
            var attributes = {};
            attributes.id = "StrobeMediaPlayback";
            attributes.name = "StrobeMediaPlayback";
            attributes.align = "middle";
            function getSWF(name) {
                var e = document.getElementById(name);
                return (navigator.appName.indexOf("Microsoft") != -1) ? e : e.getElementsByTagName("embed")[0];
            }
            var timeShow = setInterval(function () {
                if ($('body').find('#flashContent').length > 0) {
                    swfobject.embedSWF("/lty_dispatch_video_monitor/static/src/swfs/StrobeMediaPlayback.swf", "flashContent", "640", "377", swfVersionStr, xiSwfUrlStr, soFlashVars, params, attributes);
                    swfobject.createCSS("#flashContent", "display:block;text-align:left;");
                    clearInterval(timeShow);
                }
            }, 1000);
            // send_video_msg()
        },
    });
    core.action_registry.add('lty_dispatch_video_monitor.video_play', video_play);
});