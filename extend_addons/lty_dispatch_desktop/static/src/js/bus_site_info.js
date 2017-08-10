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
            'click .get_main_controll_interface':'get_main_controll_interface'
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
                zIndex: zIndex+1
            };
            new digital_map(this, options).appendTo($('body'));
        },
        get_main_controll_interface:function (e) {
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
            var map = new AMap.Map("digital_map", {
                    resizeEnable: true,
                    center: [114.408539, 30.465158],
                    zoom: 14
                });
            var marker = new AMap.Marker({
                            icon: "http://webapi.amap.com/theme/v1.3/markers/n/mark_b.png",
                        });
            var marker_list = [];
            var websocket = null;
            //判断当前浏览器是否支持WebSocket
            if ('WebSocket' in window) {
                websocket = new SockJS("http://127.0.0.1:8766/wstest?userId=45454");
            }
            else {
                alert('当前浏览器 Not support websocket');
            }
            //连接发生错误的回调方法
            websocket.onerror = function () {
                setMessageInnerHTML("WebSocket连接发生错误");
            };
            //连接成功建立的回调方法
            websocket.onopen = function () {
                setMessageInnerHTML("WebSocket连接成功");
            }
            //接收到消息的回调方法
            var controllerId, moduleName, recv;
            websocket.onmessage = function (event) {
                setMessageInnerHTML(event.data);
            };
            //连接关闭的回调方法
            websocket.onclose = function () {
                setMessageInnerHTML("WebSocket连接关闭");
            };
            //监听窗口关闭事件，当窗口关闭时，主动去关闭websocket连接，防止连接还没断开就关闭窗口，server端会抛异常。
            window.onbeforeunload = function () {
                closeWebSocket();
            };
            //将消息显示在网页上
            function setMessageInnerHTML(innerHTML) {
                var a = innerHTML.substring(78, 79);

                if (a) {
                    // 实例化点标记
                    var ab = [114.408 + a + 39, 30.461 + a + 58];
                    function addMarker() {
                        marker.setPosition(ab);
                        marker.setMap(map);
                    }

                    addMarker();
                }
            }

            //关闭WebSocket连接
            function closeWebSocket() {
                websocket.close();
            }

            //发送消息
            function send() {
                var message = document.getElementById('text').value;
                websocket.send(message);
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
        template:'main_controll_interface',
        init:function (parent, data) {
            this._super(parent, data);
            this.location_data = data;
        },
        start:function () {

        },
        events:{
            'click .close_bt':'closeFn',
            'click .bus_list a':'chose_btn'
        },
        closeFn: function () {
            this.destroy();
        },
        chose_btn:function (event) {
            var e = event||window.event;
            var x = e.currentTarget;
            $(x).addClass('active_a').parent().siblings().find('a').removeClass('active_a');
        }
    });
    return bus_site_info;
});