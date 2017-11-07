/**
 * Created by Administrator on 2017/10/31.
 */
odoo.define('lty_station_gps_collect.gps_collect', function (require) {
    "use strict";
    var core = require('web.core');
    var Model = require('web.Model');
    var Widget = require('web.Widget');
    // 引入地图js文件
    $.getScript("http://webapi.amap.com/maps?v=1.3&key=cf2cefc7d7632953aa19dbf15c194019");
    var gps_content = Widget.extend({
        template: 'gps_content',
        //data_len为父widget继承下来的数据
        init: function (parent, data_len) {
            this._super(parent);
            this.pa = parent;
            this.gps_data = data_len;
            //声明需要的关系表
            this.model_gps_data = new Model('station.collected.gps.info');
        },
        start: function () {
            var geolocation;
            this.json_arr = {};
            this.json_posi = {};
            this.json_cir = {};
            this.cir_chk = {};
            this.change_id = '';
            this.click_map = false;
            //声明此站台或此页面的关联id
            this.re_cid = $('#the_rec_id').find('.o_form_field').html();
            //加载地图，调用浏览器定位服务
            this.map = new AMap.Map(this.$(".map_container")[0], {
                zoom: 13,
                resizeEnable: true
            });
            var self = this;
            //添加高德地图工具插件
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
            // 渲染站场名称   $('h1 span.o_form_field.o_form_required').html()这个是直接从页面拿到站场，这个也可以从表里面那
            this.$el.find('.op_content_tt>li').eq(1).html($('h1 span.o_form_field.o_form_required').html())
            // 通过station_id（站场关联id）查表渲染标注和半径功能
            this.model_gps_data.query().filter([['station_id', '=', parseInt(this.re_cid)]]).all().then(function (data_res) {
                for (var mq = 0; mq < data_res.length; mq++) {
                    //标注渲染
                    var marker = new AMap.Marker({
                        position: [data_res[mq].longitude, data_res[mq].latitude],
                        map: self.map
                    });
                    // 为标注和半径做库处理
                    self.json_arr['change' + data_res[mq].name] = marker;
                    self.json_posi['change' + data_res[mq].name] = [data_res[mq].longitude, data_res[mq].latitude];
                    // this.json_arr[] = {};
                    // 半径渲染
                    self.cir_chk['change' + data_res[mq].name] = new AMap.Circle({
                        center: [data_res[mq].longitude, data_res[mq].latitude],
                        radius: $('.to_change[cid=change' + data_res[mq].name + ']').parent().parent().find('.cir>input').val(),
                        fillOpacity: 0.2,
                        strokeWeight: 1
                    });
                    //半径
                    self.cir_chk['change' + data_res[mq].name].setMap(self.map);
                    //将此半径对象存储
                    self.json_cir['change' + data_res[mq].name] = self.cir_chk['change' + data_res[mq].name];
                    // this.json_posi = {};
                }
            });

            //点击地图事件
            this.map.on('click', function (e) {

                //已经点击修改并且不是连点状态
                if (self.change_id != '' && self.click_map == false) {
                    // 移除当前标注
                    if (self.change_id != '') {
                        if (self.json_arr[self.change_id]) {
                            self.map.remove(self.json_arr[self.change_id]);
                        }
                        //移除掉当前半径圈
                        if (self.json_cir[self.change_id]) {
                            self.map.remove(self.json_cir[self.change_id]);
                        }
                    }
                    $('.to_change[cid=' + self.change_id + ']').addClass('not_null').parent().parent().find("td.lon").html(e.lnglat.lng).parent().find("td.lat").html(e.lnglat.lat);
                    var marker = new AMap.Marker({
                        position: [e.lnglat.lng, e.lnglat.lat]
                    });
                    // 是否已经存在半径属性,做判断
                    if ($(".ipc[type='checkbox']").is(':checked')) {
                        // 点击给上圆圈
                        self.cir_chk[self.change_id] = new AMap.Circle({
                            center: [e.lnglat.lng, e.lnglat.lat],
                            radius: $('.to_change[cid=' + self.change_id + ']').parent().parent().find('.cir>input').val(),
                            fillOpacity: 0.2,
                            strokeWeight: 1
                        });
                        //半径
                        self.cir_chk[self.change_id].setMap(self.map);
                        //将此半径对象存储
                        self.json_cir[self.change_id] = self.cir_chk[self.change_id];
                    }
                    // 添加地图标注
                    marker.setMap(self.map);
                    self.json_arr[self.change_id] = marker;
                    // 保存所处的经纬度位置
                    self.json_posi[self.change_id] = [e.lnglat.lng, e.lnglat.lat];
                    //不是修改状态并且处于连点状态
                } else if (self.click_map == true) {
                    if ($('.to_change:not(.not_null)').length > 0) {
                        self.change_id = $('.to_change:not(.not_null)').eq(0).attr('cid');
                        $('.to_change:not(.not_null)').eq(0).addClass('not_null').parent().parent().find("td.lon").html(e.lnglat.lng).parent().find("td.lat").html(e.lnglat.lat);
                        var marker = new AMap.Marker({
                            position: [e.lnglat.lng, e.lnglat.lat]
                        });
                        // 是否已经存在半径属性,做判断
                        if ($(".ipc[type='checkbox']").is(':checked')) {
                            // 点击给上圆圈
                            self.cir_chk[self.change_id] = new AMap.Circle({
                                center: [e.lnglat.lng, e.lnglat.lat],
                                radius: $('.to_change[cid=' + self.change_id + ']').parent().parent().find('.cir>input').val(),
                                fillOpacity: 0.2,
                                strokeWeight: 1
                            });
                            //半径
                            self.cir_chk[self.change_id].setMap(self.map);
                            //将此半径对象存储
                            self.json_cir[self.change_id] = self.cir_chk[self.change_id];
                        }
                        // 添加地图标注
                        marker.setMap(self.map);
                        self.json_arr[self.change_id] = marker;
                        // 保存所处的经纬度位置
                        self.json_posi[self.change_id] = [e.lnglat.lng, e.lnglat.lat];
                    } else {
                        var layer_index = layer.msg("已设点完毕", {shade: 0.3, time: 800});
                    }

                }

            });
        },
        events: {
            'click .to_change': 'change_gps',
            'click .ipc': 'ipc',
            'click .save_gps': 'save_gps',
            'click .reset_gps': 'reset_gps',
            'click .point_gps': 'point_gps',
            'blur .cir>input': 'change_radius'
        },
        change_radius: function (event) {
            var x = event.currentTarget;
            var self = this;
            this.to_change_dom = $(x).parents('tr').find('.to_change');
            this.c_id = parseInt($(x).parents('tr').find('.to_change').attr('gps_name'));
            if ($(x).val() != '') {
                var parnt = /^[1-9]\d*$/;
                // 如果不为空，即时修改
                if (parnt.test($(x).val())) {
                    self.model_gps_data.call("write", [self.c_id,
                        {
                            'radius': $(x).val(),
                        }]).then(function (res) {
                        // 如果此时有选中状态并且已有经纬度标记则修改半径大小
                        if ($(".ipc[type='checkbox']").is(':checked') && self.to_change_dom.hasClass('not_null')) {
                            self.map.remove(self.json_cir[self.to_change_dom.attr('cid')]);
                            self.cir_chk[self.to_change_dom.attr('cid')] = new AMap.Circle({
                                center: self.json_posi[$(x).parents('tr').find('.to_change').attr('cid')],
                                radius: $(x).val(),
                                fillOpacity: 0.2,
                                strokeWeight: 1
                            });
                            //半径
                            self.cir_chk[self.to_change_dom.attr('cid')].setMap(self.map);
                            //将此半径对象存储
                            self.json_cir[self.to_change_dom.attr('cid')] = self.cir_chk[self.to_change_dom.attr('cid')];
                        }
                    });
                } else {
                    layer.msg("请输入正整数", {shade: 0.3, time: 800});
                }
            } else {
                //如果为空，重新赋值
                this.model_gps_data.query().filter([['station_id', '=', parseInt(this.re_cid)], ['id', '=', self.c_id]]).all().then(function (data) {
                    $(x).val(data[0].radius);
                });
            }
        },
        //选中标记按钮
        point_gps: function (event) {
            var x = event.currentTarget;
            var self = this;
            this.change_id = '';
            if (!$(x).hasClass('point')) {
                $(x).addClass('point').find('img').attr('src', '/lty_station_gps_collect/static/src/img/point_out.png');
                self.click_map = true;
            } else {
                $(x).removeClass('point').find('img').attr('src', '/lty_station_gps_collect/static/src/img/point_in.png');
                self.click_map = false;
            }
        },
        //重置功能
        reset_gps: function () {
            var self = this;
            this.unlink_dom = this.$el.find('.to_change[cid]');
            $.each(this.unlink_dom, function (key, value) {
                //是否有经纬度添加
                if (self.unlink_dom.eq(key).parent().parent().find('.lon').html() != '') {
                    // 通过绑定的gps_name判断此经纬度是否存储过在数据库分别处理
                    if (self.unlink_dom.eq(key).attr('gps_name') == undefined) {
                        //清空
                        self.unlink_dom.eq(key).removeClass('not_null').parent().parent().find('.lon').html('').parent().find('.lat').html('');
                        self.map.remove(self.json_arr[self.unlink_dom.eq(key).attr('cid')]);
                        if ($(".ipc[type='checkbox']").is(':checked')) {
                            self.map.remove(self.json_cir[self.unlink_dom.eq(key).attr('cid')]);
                        }
                    } else {
                        self.model_gps_data.call("unlink", [parseInt(self.unlink_dom.eq(key).attr('gps_name'))]).then(function (res_un) {
                            self.unlink_dom.eq(key).removeClass('not_null').removeAttr('gps_name').parent().parent().find('.lon').html('').parent().find('.lat').html('');
                            self.map.remove(self.json_arr[self.unlink_dom.eq(key).attr('cid')]);
                            if ($(".ipc[type='checkbox']").is(':checked')) {
                                self.map.remove(self.json_cir[self.unlink_dom.eq(key).attr('cid')]);
                            }
                        });
                    }
                }
            });
        },
        //保存功能
        save_gps: function () {
            var self = this;
            var dom = this.$el.find('.to_change');
            for (var m = 0; m < dom.length; m++) {
                // 是否有经纬度
                if (dom.eq(m).parent().parent().find('.lon').html() == '') {

                } else {
                    // 有经纬度并且无name属性即为新加
                    if (dom.eq(m).attr('gps_name') == undefined) {
                        console.log(m)
                        var a = m;
                        //新加
                        self.model_gps_data.call("create", [
                            {
                                'station_id': self.re_cid,
                                'radius': dom.eq(a).parent().parent().find('.cir>input').val(),
                                'name': dom.eq(a).parent().parent().find('.gps_index').html(),
                                'longitude': dom.eq(a).parent().parent().find('.lon').html(),
                                'latitude': dom.eq(a).parent().parent().find('.lat').html()
                            }]).then(function (res) {
                            self.close_gps(a, dom);
                        });
                    } else {
                        //更新
                        var a = m;
                        self.model_gps_data.call("write", [parseInt(dom.eq(m).attr('gps_name')),
                            {
                                'longitude': dom.eq(a).parent().parent().find('.lon').html(),
                                'latitude': dom.eq(a).parent().parent().find('.lat').html(),
                                'radius': dom.eq(a).parent().parent().find('.cir>input').val(),
                            }]).then(function (res) {
                            self.close_gps(a, dom);
                        });
                    }
                }
            }
            self.close_gps(9);
        },
        //因为直接操作表而需要循环创建或更新数据，解决异步造成的数据保存问题
        close_gps: function (a, dom) {
            if (a == 9) {
                //销毁部件
                this.destroy();
                $(".modal-dialog .close").click();
                //刷新页面
                setTimeout(function () {
                    window.location.reload();
                }, 1000);
            } else {
                var close_or_no = true;
                for (var b = a + 1; b < 9; b++) {
                    if (dom.eq(b).parent().parent().find('.lon').html() != '') {
                        close_or_no = false;
                        break;
                    } else {
                        close_or_no = true;
                    }
                }
                if (close_or_no == true) {
                    $(".modal-dialog .close").click();
                    setTimeout(function () {
                        window.location.reload();
                    }, 1000);
                }
            }
        },
        ipc: function () {
            var self = this;
            //选择checkbox的判断是否给出半径
            if ($(".ipc[type='checkbox']").is(':checked')) {
                //json_arr标注的集合
                for (var i in self.json_arr) {
                    // 给所有存在的标注给上半径
                    self.cir_chk[i] = new AMap.Circle({
                        center: self.json_posi[i],
                        radius: parseInt($('[cid=' + i + ']').parent().parent().find('.cir>input').val()),
                        fillOpacity: 0.2,
                        strokeWeight: 1
                    });
                    self.cir_chk[i].setMap(self.map);
                    self.json_cir[i] = self.cir_chk[i];
                }
            } else {
                for (var j in self.json_arr) {
                    // 移除所有的半径
                    self.map.remove(self.json_cir[j]);
                }
            }
        },
        //绑定change_id即修改的值
        change_gps: function (event) {
            // 获取点击dom
            var x = event.currentTarget;
            if (this.click_map == false) {
                this.change_id = $(x).attr('cid');
            } else {
                this.change_id = '';
                layer.msg("请先关闭设点按钮", {shade: 0.3, time: 800});
            }
        }
    });
    var gps_control = Widget.extend({
        template: 'gps_control',
        init: function (parent, context) {
            this._super(parent, context);
            this.model_gps_data = new Model('station.collected.gps.info');
        },
        start: function () {
            this.re_cid = $('#the_rec_id').find('.o_form_field').html();
            var self = this;
            var data_len = new Array(10);
            for (var i = 0; i < data_len.length; i++) {
                data_len[i] = '';
            }
            //通过关联id拿到上次存储的记录
            this.model_gps_data.query().filter([['station_id', '=', parseInt(this.re_cid)]]).all().then(function (data) {
                for (var i = 0; i < data.length; i++) {
                    data_len.splice((data[i].name - 1), 1, data[i]);
                }
                //将子模块引入
                new gps_content(self, data_len).appendTo(self.$el);
            });
        }
    });
    // 注册gps_control部件
    core.action_registry.add('gps_control.page', gps_control);
})
;