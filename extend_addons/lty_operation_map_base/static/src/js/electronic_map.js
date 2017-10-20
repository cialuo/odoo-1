var CARMAP,
    VEHICLE_INFO_DICT = {},
    TARGET_LINE,
    TARGET_VEHICLE;

odoo.define("electronic_map.electronic_map", function(require) {
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
                format: 'YYYY-MM-DD HH:mm:ss',
                language: 'en',
                pickDate: true,
                pickTime: true,
                stepHour: 1,
                stepMinute: 1,
                secondStep: 1,
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
            self.get_time_fn();
        },

        get_time_fn: function(){
            var myDate = new Date();
            var newDate_end = myDate.getFullYear() + "-" + ("0" + (myDate.getMonth() + 1)).slice(-2) + "-" + myDate.getDate() + " 10:00:00";
            var hisDate = new Date(new Date(newDate_end).getTime() - 86400000);
            var newDate_start = hisDate.getFullYear() + "-" + ("0" + (hisDate.getMonth() + 1)).slice(-2) + "-" + hisDate.getDate() + " 10:00:00";
            this.$(".startTime").val(newDate_start);
            this.$(".endTime").val(newDate_end);
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
            config_parameter.query().filter([["key", "=", "dispatch.desktop.socket"]]).all().then(function (socket) {
                config_parameter.query().filter([["key", "=", "dispatch.desktop.restful"]]).all().then(function (restful) {
                    SOCKET_URL = socket[0].value;
                    RESTFUL_URL = restful[0].value;
                    $.getScript("/lty_operation_map_base/static/src/js/websocket_electronic_map.js", function(){
                        self.get_line_info();
                    });
                });
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
            CARMAP = map;
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
                self.init_map(map);
                if (!options.line_id) {
                    layer.msg("请先选择线路", { shade: 0.3, time: 2000 });
                    return false;
                }
                self.marker_stop_move();
                self.set_map_center = false;
                TARGET_VEHICLE = "";
                TARGET_LINE_ID = "";
                self.subscribe(options.gprsId);

                TARGET_LINE_ID = options.line_id;
                if (options.onboardId){
                    TARGET_VEHICLE = options.onboardId.toString();
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
                    }else{
                        self.vehicle_position_http(map);
                    }
                })
            });
        },
        marker_stop_move: function(){
            for (var tem in VEHICLE_INFO_DICT){
                VEHICLE_INFO_DICT[tem].stopMove();
            }
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
                url: RESTFUL_URL + '/ltyop/dspGprsData/dspGpsCoordLastPos?apikey=71029270&params={"gprsId":"' + options.gprsId + '"}',
                type: 'get',
                dataType: 'json',
                success: function(ret) {
                    layer.close(layer_index);
                    if (ret.respose) {
                        layer.msg(ret.respose.text, { time: 2000, shade: 0.3 });
                    }else{
                        var vehicleInfo = ret[0][options.gprsId];
                        if (vehicleInfo.length == 0){
                            // layer.msg("该线路没有车辆", { shade: 0.3, time: 2000 });
                            return false;
                        }
                        self.init_vehicle_position(map, vehicleInfo);
                    }
                }
            })
        },
        // 地图上展示车辆位置状态
        init_vehicle_position: function(map, vehicleInfo){
            var self = this;
            // var vehicleInfo = [{
            //     onboardId: 10017,
            //     latitude: 36.667814,
            //     longitude: 114.642147
            // }];
            if (vehicleInfo.length > 0){
                // var icon = new AMap.Icon({
                //     image: '/lty_operation_map_base/static/src/image/vehicle_off.png',
                //     size: new AMap.Size(32, 32)
                // });
                var icon = '/lty_operation_map_base/static/src/image/vehicle_off.png';
                _.each(vehicleInfo, function(vehicle, index) {
                    var marker = new AMap.Marker({
                        content: self.get_content_fn(map, icon, vehicle.onboardId.toString()),
                        position: [vehicle.longitude, vehicle.latitude],
                        offset : new AMap.Pixel(-32,-16),
                        autoRotation: true,
                        // title: vehicle.onboardId,
                        map: map
                    });
                    VEHICLE_INFO_DICT[vehicle.onboardId.toString()] = marker;
                    if (TARGET_VEHICLE){
                        if (TARGET_VEHICLE == vehicle.onboardId.toString()){
                            self.init_map_pos = [vehicle.longitude, vehicle.latitude];
                            self.init_map_center(map);
                        }
                    }else{
                        if (index == 0 && !self.set_map_center){
                            self.init_map_pos = [vehicle.longitude, vehicle.latitude];
                            self.init_map_center(map);
                        }
                    }
                });
            }
        },
        get_content_fn: function(map, icon, onboardId){
            var div = document.createElement('div');
            div.style.display = "block";
            if (TARGET_VEHICLE == onboardId){
                div.style.borderStyle = "solid";
                div.style.borderColor = "#5acbff";
                div.style.borderWidth = "2px";
            }else{
                div.style.borderStyle = "none";
                div.style.borderWidth ="0px";
            }
            div.style.position = "absolute";
            div.style.textAlign = "center";
            div.style.width = '70px';
            div.style.height = '32px';
            div.style.zIndex = '1';
            // 车辆编号
            var span = document.createElement("span");
            span.style.lineHeight = "16px";
            span.style.position = "absolute";
            span.style.top = "-16px";
            span.style.textShadow = "-1px 0 #FFFFFF, 0 1px #FFFFFF,1px 0 #FFFFFF, 0 -1px #FFFFFF";
            span.style.color = "#58554e";
            var text = document.createTextNode(onboardId);
            span.appendChild(text);
            this.setUnselected(span);
            div.appendChild(span);
            // 车辆图标
            var divImg = document.createElement("span");
            divImg.className = "carIcon";
            divImg.style.width = "32px";
            divImg.style.height = "32px";
            divImg.style.display = "inline-block";
            divImg.style.backgroundImage= "url('"+icon+"')";
            divImg.style.backgroundRepeat = "no-repeat";
            div.appendChild(divImg);
            return div;
        },
        setUnselected: function(a){
            if(a.style&&a.style.MozUserSelect){
               a.style.MozUserSelect="none";
            }else if(a.style&&a.style.WebkitUserSelect){
               a.style.WebkitUserSelect="none";
            }else if(a.unselectable) {
                a.unselectable ="on";
                a.onselectstart =function(){return false};       
            }
        },
        init_map: function(map){
            map.clearMap();
            map.setZoom(10);
            map.setCenter([116.408075, 39.950187]);
        },
        init_map_center: function(map){
            this.set_map_center = true;
            if (map.getZoom()<14){
                map.setZoom(14);
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
        },
        //订阅
        subscribe: function(gpsId){
            if (self.subscribe_gpsId && self.subscribe_gpsId!=gpsId){
                var package = {
                    type: 2001,
                    gpsId: self.subscribe,
                    open_modules: ["bus_site", "abnormal"]
                };
                websocket_electronic_map.send(JSON.stringify(package));
            }

            if (gpsId){
                var package = {
                    type: 2000,
                    gpsId: gpsId,
                    open_modules: ["bus_site", "abnormal"]
                };
                websocket_electronic_map.send(JSON.stringify(package));
                self.subscribe_gpsId = gpsId;
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
                self.get_vehicles_Info(options);
                
            });
        },
        get_vehicles_Info: function(options){
            var self = this;
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