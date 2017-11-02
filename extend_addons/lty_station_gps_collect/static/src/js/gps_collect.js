/**
 * Created by Administrator on 2017/10/31.
 */
odoo.define('lty_station_gps_collect.gps_collect', function (require) {
    "use strict";
    var core = require('web.core');
    var Model = require('web.Model');
    var Widget = require('web.Widget');
    $.getScript("http://webapi.amap.com/maps?v=1.3&key=cf2cefc7d7632953aa19dbf15c194019");
    var gps_content = Widget.extend({
        template: 'gps_content',
        init: function (parent, context) {
            this._super(parent, context);
        },
        start: function () {
            var geolocation;
            // 存储标注
            // this.arr = [];
            // 存储圆圈
            // this.arrCir = [];
            // 存储圆圈的坐标
            // this.posi = [];
            this.json_arr = {};
            this.json_posi = {};
            this.json_cir = {};
            this.cir_chk = {};
            //加载地图，调用浏览器定位服务
            this.map = new AMap.Map(this.$(".map_container")[0], {
                zoom: 13,
                resizeEnable: true
            });
            var self = this;
            this.map.plugin('AMap.Geolocation', function () {
                geolocation = new AMap.Geolocation({
                    enableHighAccuracy: true, //是否使用高精度定位，默认:true
                    timeout: 10000, //超过10秒后停止定位，默认：无穷大
                    buttonOffset: new AMap.Pixel(10, 20), //定位按钮与设置的停靠位置的偏移量，默认：Pixel(10, 20)
                    zoomToAccuracy: true, //定位成功后调整地图视野范围使定位位置及精度范围视野内可见，默认：false
                    buttonPosition: 'RB'
                });
                self.map.addControl(geolocation);
            });
        },
        events: {
            'click .to_change': 'change_gps',
            'click .ipc': 'ipc'
        },
        ipc: function () {
            var self = this;
            console.log(self.posi)
            //当选中时
            if ($(".ipc[type='checkbox']").is(':checked')) {
                // 如果目前没有半径，且有一个标注，就给上一个半径
                if (self.arrCir.length == 0) {
                    self.cir_chk = new AMap.Circle({
                        center: self.posi[0],
                        radius: 100,
                        fillOpacity: 0.2,
                        strokeWeight: 1
                    });
                    self.cir_chk.setMap(self.map);
                    self.arrCir.push(self.cir_chk);
                }
            } else {
                if (self.arrCir.length > 0) {
                    // 清除圆圈以及圆圈经纬度
                    self.map.remove(self.arrCir);
                    self.arrCir = [];
                }
            }
        },
        change_gps: function (event) {
            // 获取点击dom
            var x = event.currentTarget;
            var change_id = $(x).attr('cid');
            var self = this;
            this.map.on('click', function (e) {
                // 移除标注,圆圈
                if (self.json_arr[change_id]) {
                    self.map.remove(self.json_arr[change_id]);
                    self.map.remove(self.json_posi[change_id]);
                }
                $(x).parent().parent().find("td.lon").html(e.lnglat.lng);
                $(x).parent().parent().find("td.lat").html(e.lnglat.lat);
                var marker = new AMap.Marker({
                    position: [e.lnglat.lng, e.lnglat.lat]
                });
                //清空上一次记录
                self.posi = [];
                self.arr = [];
                self.arrCir = [];
                if ($(".ipc[type='checkbox']").is(':checked')) {
                    // 点击给上圆圈
                    self.cir_chk = new AMap.Circle({
                        center: [e.lnglat.lng, e.lnglat.lat],
                        radius: 100,
                        fillOpacity: 0.2,
                        strokeWeight: 1
                    });
                    self.cir_chk.setMap(self.map);
                    self.json_cir[change_id] = self.cir_chk;
                    // self.arrCir.push(self.json_cir);
                }
                marker.setMap(self.map);
                self.json_arr[change_id] = marker;
                self.json_posi[change_id] = [e.lnglat.lng, e.lnglat.lat];
                // self.arr.push(self.json_arr);
                // 保存横纵坐标
                // self.posi.push(self.json_posi);
            });
        }

    })
    var gps_control = Widget.extend({
        template: 'gps_control',
        init: function (parent, context) {
            this._super(parent, context);
        },
        start: function () {
            new gps_content(this).appendTo(this.$el);
        }
    });

    core.action_registry.add('gps_control.page', gps_control);

})
;