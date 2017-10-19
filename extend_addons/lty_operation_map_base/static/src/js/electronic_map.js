var CARMAP,
    VEHICLE_INFO_DICT = {},
    ONBOARDID_INNERCODE_DICT = {},
    TARGET_LINE_ID,
    TARGET_VEHICLE;

odoo.define("electronic_map.electronic_map", function(require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var Model = require('web.Model');
    var bus_real_info = require('lty_dispatch_desktop_widget.bus_real_info');
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
                ONBOARDID_INNERCODE_DICT = {};
                vehiclesObj.empty().append('<option value="">--请选择--</option>');
                if (this.value != "") {
                    var id = parseInt($(this).find("option:selected").attr("t_id"));
                    fleet_vehicle.query().filter([
                        ["route_id", "=", id]
                    ]).all().then(function(vehicles) {
                        _.each(vehicles, function(set) {
                            if (set.on_boardid){
                                ONBOARDID_INNERCODE_DICT[set.on_boardid] = set.inner_code;
                                var option = '<option value="'+set.on_boardid+'" inner_code="' + set.inner_code + '">' + set.inner_code + '</option>';
                                vehiclesObj.append(option);
                            }
                        });
                    })
                }
            });
            self.get_time_fn();
        },

        get_time_fn: function(){
            var myDate = new Date();
            var newDate = myDate.getFullYear() + "-" + ("0" + (myDate.getMonth() + 1)).slice(-2) + "-" + myDate.getDate() + " 00:00:00";
            var hisDate = new Date(new Date(newDate).getTime() - 86400000);
            var newDate_start = hisDate.getFullYear() + "-" + ("0" + (hisDate.getMonth() + 1)).slice(-2) + "-" + hisDate.getDate() + " 00:00:00";
            var newDate_end = hisDate.getFullYear() + "-" + ("0" + (hisDate.getMonth() + 1)).slice(-2) + "-" + hisDate.getDate() + " 23:59:59";
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
            this.map_toolBar(map);
            this.load_fn(map);
        },
        // 绑定地图工具
        map_toolBar: function(map) {
            map.plugin(["AMap.ToolBar"], function() {
                map.addControl(new AMap.ToolBar({ locate: false }));
            });
            if (location.href.indexOf('&guide=1') !== -1) {
                map.setStatus({ scrollWheel: false });
            }
        },
        // 加载事件
        load_fn: function(map) {
            var self = this;
            // 定位
            self.$el.on("click", ".localize_bt", function() {
                var options = self.get_map_set_arg();
                self.marker_stop_move();
                self.init_map(map);
                TARGET_VEHICLE = "";
                TARGET_LINE_ID = "";
                if (!options.line_id) {
                    layer.msg("请先选择线路", { shade: 0.3, time: 2000 });
                    return false;
                }
                self.set_map_center = false;
                self.subscribe(options.gprsId);

                TARGET_LINE_ID = options.gprsId;
                if (options.onboardId){
                    TARGET_VEHICLE = options.onboardId;
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
            

            // 查看车详情
            // line_id: lineObj.find("option:selected").attr("t_id"),
            // gprsId: lineObj.val(),
            // onboardId: vehiclesObj.val(),
            // inner_code: vehiclesObj.find("option:selected").attr("inner_code"),
            // startTime: startTime.val(),
            // endTime: endTime.val()
            self.$(".map_work_content").on("click", ".vehicleMapMarker", function(e){
                var inner_code = $(this).find(".carText").text();
                var onBoardId = $(this).attr("onboardId");
                var args = self.get_map_set_arg();
                var options = {
                    x: e.clientX + 5,
                    y: e.clientY + 5,
                    zIndex: 2,
                    line_id: args.line_id,
                    line_name: args.line_name,
                    car_num: inner_code,
                    onBoardId: onBoardId,
                    controllerId: "",
                    fix_style: "bus_real_info_electronicMap"
                };
                $(".busRealStateModel").remove();
                var dialog = new bus_real_info(self, options);
                dialog.appendTo($("body"));
            });
        },
        marker_stop_move: function(){
            for (var tem in VEHICLE_INFO_DICT){
                VEHICLE_INFO_DICT[tem].stopMove();
            }
            VEHICLE_INFO_DICT = {};
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
                if (!TARGET_VEHICLE){
                    setTimeout(function(){
                        self.map_line_flash(map, polyline, setArg);
                    }, 200);
                }
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
                            layer.msg("没有查到车辆初始位置信息", { shade: 0.3, time: 2000 });
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
                    var new_gps = CONVERSIONS_GPS.gcj_encrypt(vehicle.latitude, vehicle.longitude);
                    if (TARGET_VEHICLE){
                        if (TARGET_VEHICLE == vehicle.onboardId){
                            var marker = new AMap.Marker({
                                content: self.get_content_fn(map, icon, vehicle.onboardId.toString()),
                                position: [new_gps.lon, new_gps.lat],
                                offset : new AMap.Pixel(-32,-16),
                                autoRotation: true,
                                // title: vehicle.onboardId,
                                map: map
                            });
                            VEHICLE_INFO_DICT[vehicle.onboardId.toString()] = marker;
                            self.init_map_pos = [new_gps.lon, new_gps.lat];
                            self.init_map_center(map);
                            self.map_vehicle_flash(marker);
                            return false;
                        }
                    }else{
                        if (index == 0 && !self.set_map_center){
                            var marker = new AMap.Marker({
                                content: self.get_content_fn(map, icon, vehicle.onboardId.toString()),
                                position: [new_gps.lon, new_gps.lat],
                                offset : new AMap.Pixel(-32,-16),
                                autoRotation: true,
                                // title: vehicle.onboardId,
                                map: map
                            });
                            VEHICLE_INFO_DICT[vehicle.onboardId.toString()] = marker;
                            self.init_map_pos = [new_gps.lon, new_gps.lat];
                            self.init_map_center(map);
                        }
                    }
                });
            }
        },
        // 目标车闪烁
        map_vehicle_flash: function(marker){
            var self = this;
            var marker_dom = marker.getContent();
            var w = marker_dom.style.borderWidth;
            var i = 0;
            var twinkleLineTimer = window.setInterval(function(){
                if (i>=8){
                    window.clearInterval(twinkleLineTimer);
                }
                if (i%2){
                    w = "4px";
                }else{
                    w = "2px";
                }
                marker_dom.style.borderWidth = w;
                i++;
            },200)
        },
        get_content_fn: function(map, icon, onboardId){
            var div = document.createElement('div');
            div.style.display = "block";
            div.className = "vehicleMapMarker";
            div.setAttribute("onboardId", onboardId);
            if (ONBOARDID_INNERCODE_DICT[onboardId] == TARGET_VEHICLE){
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
            span.className = "carText";
            span.style.lineHeight = "16px";
            span.style.position = "absolute";
            span.style.top = "-16px";
            span.style.textShadow = "-1px 0 #FFFFFF, 0 1px #FFFFFF,1px 0 #FFFFFF, 0 -1px #FFFFFF";
            span.style.color = "#58554e";
            var text = document.createTextNode(ONBOARDID_INNERCODE_DICT[onboardId]);
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
            CARMAP = map;
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
                line_name: lineObj.find("option:selected").html(),
                gprsId: lineObj.val(),
                onboardId: vehiclesObj.val(),
                inner_code: vehiclesObj.find("option:selected").attr("inner_code"),
                startTime: startTime.val(),
                endTime: endTime.val()
            }
        },
        //订阅
        subscribe: function(gpsId){
            try {
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
            } catch(e) {
                // statements
                console.log(e);
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
            this.map = map;
            this.map_toolBar(map);
            this.load_fn(map);
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
            // 查询
            self.$el.on("click", ".query_bt", function() {
                var options = self.get_map_set_arg();
                self.init_map(map);
                self.get_vehicles_Info(options);
            });

            // 播放/停止
            self.$(".video_progress").on("click", ".partIcon", function(){
                self.play_status_fn();
            });

            // 停止
            self.$el.on("click", ".stop_bt", function(){
                self.$(".video_progress .partIcon").addClass("start_bt");
                self.play_stop();
            })
        },
        init_map: function(map){
            if (this.marker){
                this.marker.stopMove();
                this.marker = "";
            }
            map.clearMap();
            map.setZoom(10);
            map.setCenter([116.408075, 39.950187]);
            this.play_time = 0;
            if (this.play_Interval){
                window.clearInterval(this.play_Interval);
            }
            this.marker_point_info = [];
            this.marker_trajectory_gprs_info = [];
            this.polyline = "";
        },
        play_status_fn: function(){
            var partIcon = this.$(".video_progress .partIcon");
            partIcon.toggleClass("start_bt");
            if (!partIcon.hasClass("start_bt")){
                this.play_start();
            }else{
                this.play_stop();
            }
        },
        // 开始播放
        play_start: function(){
            var self = this;
            self.bus_trajectory_point_init();
            self.play_Interval  = window.setInterval(function(){
                if ((self.play_time)>=self.gprsInfo.length){
                    self.ProgressBar.SetValue(self.play_time);
                    window.clearInterval(self.play_Interval);
                    self.play_time = 0;
                    self.play_stop();
                    return false;
                }
                var act = self.gprsInfo[self.play_time];
                var new_gps = CONVERSIONS_GPS.gcj_encrypt(act.latitude, act.longitude);
                self.marker.moveTo(new AMap.LngLat(new_gps.lon, new_gps.lat), 500000);
                self.add_bus_trajectory_point(act);
                self.ProgressBar.SetValue(self.play_time);
                self.play_time += 1;
            }, 1000);
        },
        play_stop: function(){
            if (this.play_Interval){
                console.log(this.play_time);
                window.clearInterval(this.play_Interval);
                console.log(this.play_time);
                var partIcon = this.$(".video_progress .partIcon");
                partIcon.addClass("start_bt");
            }
        },
        // 添加点标记及运行轨迹
        add_bus_trajectory_point: function(ret){
            var self = this;
            self.bus_trajectory_point(ret);
            self.polyline.setPath(self.marker_trajectory_gprs_info);
        },
        // 删除点标记及运行轨迹
        del_bus_trajectory_point: function(){
            var self = this;
            self.marker_trajectory_gprs_info = [];
            if (self.polyline){
                self.polyline.setPath(self.marker_trajectory_gprs_info);
            }
            _.each(self.marker_point_info, function(ret) {
                ret.setMap(null);
            });
        }, 
        // 车运行gprs点标记
        bus_trajectory_point_init: function(){
            var self = this;
            var gprsInfo = self.gprsInfo;
            var play_time = self.play_time;
            var act = gprsInfo[play_time];
            var new_gps = CONVERSIONS_GPS.gcj_encrypt(act.latitude, act.longitude);
            self.marker.setPosition(new AMap.LngLat(new_gps.lon, new_gps.lat));
            self.del_bus_trajectory_point(play_time);
            _.each(gprsInfo, function(ret, index){
                if (index<=play_time){
                    self.bus_trajectory_point(ret);
                }
            })
            self.bus_trajectory();
        },
        // 添加车运行gprs点标记
        bus_trajectory_point: function(ret){
            var self = this;
            var new_gps = CONVERSIONS_GPS.gcj_encrypt(ret.latitude, ret.longitude);
            var marker = new AMap.Marker({
                content: '<div class="markerPoint"></div>',
                position: [new_gps.lon, new_gps.lat],
                offset : new AMap.Pixel(0,-2),
                map: self.map
            });
            self.marker_point_info.push(marker);
            self.marker_trajectory_gprs_info.push([new_gps.lon, new_gps.lat]);
        },
        // 车运行轨迹
        bus_trajectory: function(){
            var self = this;
            var map = self.map;
            var marker_trajectory_gprs_info = self.marker_trajectory_gprs_info;
            if (marker_trajectory_gprs_info.length>0){
                var polyline = new AMap.Polyline({
                    path: marker_trajectory_gprs_info,
                    strokeColor: "#1aba9b",
                    strokeWeight: "1",
                    lineJoin: "round"
                });
                polyline.setMap(map);
                self.polyline = polyline;
            }
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
                    if (ret.result && ret.result!=0) {
                        layer.msg(ret.respose.text, { time: 2000, shade: 0.3 });
                        return false;
                    }
                    if (ret.length==0){
                        layer.msg("无轨迹数据", { time: 2000, shade: 0.3 });
                        return false;
                    }
                    // 初始化车辆行驶轨迹
                    self.play_trajectory = [];
                    // 获取gprs总信息
                    self.gprsInfo = ret;
                    self.$(".map_work_content").css("bottom", "200px");
                    self.$(".video_progress").show();
                    self.$(".video_progress").html("");
                    new map_progress_info(self, ret).appendTo(self.$(".video_progress"));
                    // 初始化地图线路
                    self.init_line_map(options.line_id);
                    // 初始化车辆位置-车辆就绪
                    self.init_bus_location(ret[0], options.inner_code);
                    // 视频播放时间
                    self.$(".video_progress .totalTime").html(self.init_play_time(ret.length));
                    // 视频初始化
                    self.init_video_set(ret.length);
                    // 初始化播放进度
                    self.ProgressBar = {
                        maxValue: self.gprsInfo.length,
                        value: 0,
                        SetValue: function(aValue) {
                            this.value=aValue;
                            if (this.value >= this.maxValue) this.value = this.maxValue;
                            if (this.value <= 0) this.value = 0;
                            var mWidth=this.value/this.maxValue*self.$(".progress_bar").width()+"px";
                            self.$(".progress_cn").css("width",mWidth);
                            self.$(".progress_icon").css("margin-left", mWidth);
                            self.$(".video_progress .playTime").html(self.init_play_time(this.value));
                        }
                    }
                }
            })
        },
        // 查询制作线路信息
        init_line_map: function(lineId){
            var self = this;
            model_map_line_info.query().filter([
                ["line_id", "=", parseInt(lineId)]
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
                    self.load_his_establishment_line(self.map, set_dict);
                }
            })
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
                var polyline = new AMap.Polyline({
                    path: gps_list,
                    strokeColor: setArg.c,
                    strokeWeight: setArg.w,
                    lineJoin: "round"
                });
                polyline.setMap(map);
            }
        },
        // 车就绪-初始位置
        init_bus_location: function(ret, onboardId){
            var self = this;
            var map = self.map;
            var new_gps = CONVERSIONS_GPS.gcj_encrypt(ret.latitude, ret.longitude);
            // 初始以车为中心点
            self.init_map_center(new_gps);

            var icon = '/lty_operation_map_base/static/src/image/vehicle_on.png';
            var marker = new AMap.Marker({
                content: self.get_content_fn(map, icon, onboardId),
                position: [new_gps.lon, new_gps.lat],
                offset : new AMap.Pixel(-32,-16),
                autoRotation: true,
                map: map
            });
            self.marker = marker;
        },
        get_content_fn: function(map, icon, onboardId){
            var div = document.createElement('div');
            div.style.display = "block";
            div.style.borderStyle = "none";
            div.style.borderWidth ="0px";
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
        // 计算播放时间 注意点：由于每秒运行一次，所以有多少数据就有多少秒
        init_play_time: function(time){
            this.play_time = time;
            var hh;
            var mm;
            var ss;
           //传入的时间为空或小于0
            if(time==null||time<0){
                return;
            }
            //得到小时
            hh=time/3600|0;
            time=parseInt(time)-hh*3600;
            if(parseInt(hh)<10){
                  hh="0"+hh;
            }
            //得到分
            mm=time/60|0;
            //得到秒
            ss=parseInt(time)-mm*60;
            if(parseInt(mm)<10){
                 mm="0"+mm;    
            }
            if(ss<10){
                ss="0"+ss;      
            }
            return hh+":"+mm+":"+ss;
        },
        init_map_center: function(gprsObj){
            var map = this.map;
            if (map.getZoom()<14){
                map.setZoom(14);
            }
            map.setCenter([gprsObj.lon, gprsObj.lat]);
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
                inner_code: vehiclesObj.find("option:selected").attr("inner_code"),
                startTime: startTime.val(),
                endTime: endTime.val()
            }
        },
        // 初始化视频
        init_video_set: function(max){
            var self = this;
            var ScrollBar = {
                value: 0,
                maxValue: max,
                step: 1,
                currentX: 0,
                $scroll_Track: self.$(".progress_cn"),
                $scroll_Thumb: self.$(".progress_icon"),
                $scrollBar: self.$(".progress_bar"),
                Initialize: function() {
                    if (this.value > this.maxValue) {
                        return;
                    }
                    this.GetValue();
                    ScrollBar.$scroll_Track.css("width", this.currentX + 2 + "px");
                    ScrollBar.$scroll_Thumb.css("margin-left", this.currentX + "px");
                    this.Value();
                    self.$(".video_progress .playTime").html(self.init_play_time(ScrollBar.value));
                },
                Value: function() {
                    var valite = false;
                    var currentValue = 0;
                    ScrollBar.$scroll_Thumb.mousedown(function() {
                        valite = true;
                        ScrollBar.$scroll_Thumb.mousemove(function(event) {
                            if (valite == false) return;
                            var changeX = event.clientX - ScrollBar.currentX;
                            currentValue = changeX - ScrollBar.currentX - ScrollBar.$scrollBar.offset().left;
                            ScrollBar.$scroll_Thumb.css("margin-left", currentValue + "px");
                            ScrollBar.$scroll_Track.css("width", currentValue + "px");
                            if ((currentValue) >= ScrollBar.$scrollBar.width()) {
                                ScrollBar.$scroll_Thumb.css("margin-left", ScrollBar.$scrollBar.width()+ "px");
                                ScrollBar.$scroll_Track.css("width", ScrollBar.$scrollBar.width() + "px");
                                ScrollBar.value = ScrollBar.maxValue;
                            } else if (currentValue <= 0) {
                                ScrollBar.$scroll_Thumb.css("margin-left", "0px");
                                ScrollBar.$scroll_Track.css("width", "0px");
                            } else {
                                ScrollBar.value = Math.round(ScrollBar.maxValue * (currentValue / ScrollBar.$scrollBar.width()));
                            }
                        });
                    });
                    ScrollBar.$scroll_Thumb.mouseup(function() {
                        ScrollBar.value = Math.round(ScrollBar.maxValue * (currentValue / ScrollBar.$scrollBar.width()));
                        valite = false;
                        if (ScrollBar.value >= ScrollBar.maxValue) ScrollBar.value = ScrollBar.maxValue;
                        if (ScrollBar.value <= 0) ScrollBar.value = 0;
                        self.$(".video_progress .playTime").html(self.init_play_time(ScrollBar.value));
                        self.play_stop();
                        self.bus_trajectory_point_init();
                    });
                },
                GetValue: function() {
                    this.currentX = ScrollBar.$scrollBar.width() * (this.value / this.maxValue);
                }
            };
            //初始化
            self.ScrollBar = ScrollBar;
            self.ScrollBar.Initialize();
        }
    });
    // 轨迹回放车辆信息
    var map_progress_info = Widget.extend({
        template: "track_playback_map_progress_info_template",
        init: function(parent, data) {
            this._super(parent);
            this.busInfo = data;
        },
    })

    core.action_registry.add('lty_operation_map_base.track_playback_map', track_playback_map);
});