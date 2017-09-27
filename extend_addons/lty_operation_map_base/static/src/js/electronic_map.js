var VEHICLE_INFO_DICT = {};

odoo.define("", function(require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var Model = require('web.Model');
    // 线路
    var model_choseline = new Model('route_manage.route_manage');
    // 车辆
    var fleet_vehicle = new Model('fleet.vehicle');
    // 配置
    var config_parameter = new Model('ir.config_parameter');
    // 地图制作线路记录
    var model_map_line_info = new Model('map.line.production.info');

    //  地图头部
    var map_work_title = Widget.extend({
        template: "map_work_title_template",
        init: function(parent, setInfo) {
            this._super(parent);
            this.setInfo = setInfo;
        },
        start: function() {
            var self = this;
            // 加载日期组件
            self.$(".timeW").datetimepicker({
                format: 'YYYY-MM-DD HH:mm',
                language: 'en',
                pickDate: true,
                pickTime: true,
                stepHour: 1,
                stepMinute: 1,
                inputMask: true
            });

            var vehiclesObj = self.$(".onboard");
            var lineObj = self.$(".line");
            lineObj.on("change", function() {
                vehiclesObj.empty().append('<option value="">--请选择--</option>');
                if (this.value != "") {
                    var id = parseInt($(this).find("option:selected").attr("t_id"));
                    fleet_vehicle.query().filter([
                        ["route_id", "=", id]
                    ]).all().then(function(vehicles) {
                        _.each(vehicles, function(set) {
                            var option = '<option value="' + set.on_boardid + '">' + set.on_boardid + '</option>';
                            vehiclesObj.append(option);
                        });
                    })
                }
            });
        }
    });

    // 电子地图
    var electronic_map = Widget.extend({
        template: "electronic_map_template",
        init: function(parent) {
            this._super(parent);
        },
        start: function() {
            var self = this;
            self.set_map_center = false;
            config_parameter.query().filter([
                ["key", "=", "dispatch.desktop.restful"]
            ]).all().then(function(restful) {
                RESTFUL_URL = restful[0].value;
                self.get_line_info();
            });
        },
        // 获取线路信息
        get_line_info: function() {
            var self = this;
            model_choseline.query().filter([
                ["state", "=", 'inuse']
            ]).all().then(function(lines) {
                var options = { title: '电子地图', type: 'electronic_map', lines };
                new map_work_title(self, options).appendTo(self.$('.map_work_title'));
                self.init_map_fn();
            });
        },
        // 初始化地图
        init_map_fn: function() {
            var map = new AMap.Map(this.$(".map_work_content")[0], {
                resizeEnable: true,
                zoom: 10,
                center: [116.408075, 39.950187]
            });
            this.map_toolBar(map);
            this.load_fn(map);
        },
        // 绑定地图工具
        map_toolBar: function(map) {
            map.plugin(["AMap.ToolBar"], function() {
                map.addControl(new AMap.ToolBar({ locate: false }));
            });
            if (location.href.indexOf('&guide=1') !== -1) {
                map.setStatus({ scrollWheel: false })
            }
        },
        // 加载事件
        load_fn: function(map) {
            var self = this;
            // 定位
            self.$el.on("click", ".localize_bt", function() {
                var options = self.get_map_set_arg();
                if (!options.line_id) {
                    layer.msg("请先选择线路", { shade: 0.3, time: 2000 });
                    return false;
                }
                model_map_line_info.query().filter([
                    ["line_id", "=", parseInt(options.line_id)]
                ]).all().then(function(set_list) {
                    // 默认配置显示
                    var set_dict = {
                        gps_dict: {'0':[],'1':[]},
                        setArg: {
                            c: '#5acbff', //线条颜色
                            w: '4', //线条宽度
                        }
                    }

                    if (set_list.length > 0) {
                        _.each(set_list, function(set) {
                            var direction = set.direction == 'up' ? '0' : '1'
                            set_dict.gps_dict[direction] = JSON.parse(set.map_data)||[];
                        });
                        self.load_his_establishment_line(map, set_dict);
                    }
                })
            });
        },
        // 显示制作的线路
        load_his_establishment_line: function(map, hisObj) {
            var self = this;
            var pos = [];
            var up_gps_list = hisObj.gps_dict['0'],
                down_gps_list = hisObj.gps_dict['1'],
                setArg = hisObj.setArg;
            var gps_list = up_gps_list.concat(down_gps_list);
            if (gps_list.length > 0) {
                if (!self.set_map_center){
                    self.init_map_pos = gps_list[0];
                    if (self.init_map_pos.lng){
                        self.init_map_pos = [gps_list[0].lng, gps_list[0].lat];
                    }
                    self.init_map_center(map);
                }
                var polyline = new AMap.Polyline({
                    path: gps_list,
                    strokeColor: setArg.c,
                    strokeWeight: setArg.w,
                    lineJoin: "round"
                });
                polyline.setMap(map);
                setTimeout(function(){
                    self.map_line_flash(map, polyline, setArg);
                }, 200);
            }
            self.vehicle_position_http(map);
        },
        // 线路闪烁
        map_line_flash: function(map ,polyline, setArg){
            var self = this;
            self.init_map_center(map);
            var i = 0;
            var w = setArg.w;
            var twinkleLineTimer = window.setInterval(function(){
                if (i>=8){
                    window.clearInterval(twinkleLineTimer);
                }
                if (i%2){
                    w = w*2;
                }else{
                    w = setArg.w;
                }
                polyline.setOptions({
                    strokeColor: setArg.c,
                    strokeWeight: w
                });
                i++;
            },200)
        },
        // 定位时发送请求获取车辆初始位置状态
        vehicle_position_http: function(map, setArg) {
            var self = this;
            var options = self.get_map_set_arg();
            var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
            $.ajax({
                url: RESTFUL_URL + '/ltyop/dspGprsData/dspGpsCoordLastPos?apikey=71029270&params={"gprsId":"' + options.gprsId + '","onboardId":"' + options.onboardId + '"}',
                type: 'get',
                dataType: 'json',
                success: function(ret) {
                    layer.close(layer_index);
                    if (ret.respose) {
                        layer.msg(ret.respose.text, { time: 2000, shade: 0.3 });
                    }else{
                        var vehicleInfo = ret[0][options.gprsId];
                        // if (vehicleInfo.length == 0){
                        //     layer.msg("该线路没有车辆", { shade: 0.3, time: 2000 });
                        //     return false;
                        // }
                        self.init_vehicle_position(map, vehicleInfo);
                    }
                }
            })
        },
        // 地图上展示车辆位置状态
        init_vehicle_position: function(map, vehicleInfo){
            var self = this;
            var vehicleInfo = [{
                onboardId: 10017,
                latitude: 36.667814,
                longitude: 114.642147
            }];
            if (vehicleInfo.length > 0){
                var icon = new AMap.Icon({
                    image: '/lty_operation_map_base/static/src/image/vehicle.png',
                    size: new AMap.Size(22, 24)
                });
                _.each(vehicleInfo, function(vehicle, index) {
                    var marker = new AMap.Marker({
                        icon: icon,
                        position: [vehicle.longitude, vehicle.latitude],
                        offset : new AMap.Pixel(-22,-12),
                        autoRotation: true,
                        title: vehicle.onboardId,
                        zindex: 101,
                        map: map
                    });
                    VEHICLE_INFO_DICT[vehicle.onboardId.toString()] = marker;
                    if (index == 0 && !self.set_map_center){
                        self.init_map_pos = [vehicle.longitude, vehicle.latitude];
                        self.init_map_center(map);
                    }
                });
            }
        },
        init_map_center: function(map){
            this.set_map_center = true;
            if (map.getZoom()<12){
                map.setZoom(12);
            }
            if (this.init_map_pos){
                map.setCenter(this.init_map_pos);
            }
        },
        get_map_set_arg: function() {
            var vehiclesObj = this.$(".onboard");
            var lineObj = this.$(".line");
            var startTime = this.$(".startTime");
            var endTime = this.$(".endTime");
            return {
                line_id: lineObj.find("option:selected").attr("t_id"),
                gprsId: lineObj.val(),
                onboardId: vehiclesObj.val(),
                startTime: startTime.val(),
                endTime: endTime.val()
            }
        }
    });

    core.action_registry.add('lty_operation_map_base.electronic_map', electronic_map);



    // 轨迹回放
    var track_playback_map = Widget.extend({
        template: "track_playback_map_template",
        init: function(parent) {
            this._super(parent);
        },
        start: function() {
            var self = this;
            config_parameter.query().filter([
                ["key", "=", "dispatch.desktop.restful"]
            ]).all().then(function(restful) {
                SOCKET_URL = socket[0].value;
                RESTFUL_URL = restful[0].value;
                self.get_line_info();
            });
        },
        get_line_info: function() {
            var self = this;
            model_choseline.query().filter([
                ["state", "=", 'inuse']
            ]).all().then(function(lines) {
                var options = { title: '轨迹回放', type: 'track_playback_map', lines: lines };
                new map_work_title(self, options).appendTo(self.$('.map_work_title'));
                //初始化地图
                self.init_map_fn();
            });
        },
        init_map_fn: function() {
            var map = new AMap.Map(this.$(".map_work_content")[0], {
                resizeEnable: true,
                zoom: 10,
                center: [116.408075, 39.950187]
            });
            this.map_toolBar(map);
            this.load_fn();
        },
        map_toolBar: function(map) {
            map.plugin(["AMap.ToolBar"], function() {
                map.addControl(new AMap.ToolBar({ locate: false }));
            });
            if (location.href.indexOf('&guide=1') !== -1) {
                map.setStatus({ scrollWheel: false })
            }
        },
        load_fn: function(map) {
            var self = this;
            // 轨迹回放
            self.$el.on("click", ".query_bt", function() {
                var options = self.get_map_set_arg();
                var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                $.ajax({
                    url: RESTFUL_URL + '/ltyop/hbaseGps/findGpsInfo?apikey=71029270&params={"gprsId":"' + options.gprsId + '", "terminalNo":"' + options.onboardId + '", "startTime":"' + options.startTime + '", "endTime":"' + options.endTime + '"}',
                    type: 'get',
                    dataType: 'json',
                    success: function(ret) {
                        layer.close(layer_index);
                        if (ret.respose) {
                            layer.msg(ret.respose.text, { time: 2000, shade: 0.3 });
                        }
                        console.log(ret);
                    }
                })
            });
        },
        get_map_set_arg: function() {
            var vehiclesObj = this.$(".onboard");
            var lineObj = this.$(".line");
            var startTime = this.$(".startTime");
            var endTime = this.$(".endTime");
            return {
                line_id: lineObj.find("option:selected").attr("t_id"),
                gprsId: lineObj.val(),
                onboardId: vehiclesObj.val(),
                startTime: startTime.val(),
                endTime: endTime.val()
            }
        }
    });

    core.action_registry.add('lty_operation_map_base.track_playback_map', track_playback_map);
});