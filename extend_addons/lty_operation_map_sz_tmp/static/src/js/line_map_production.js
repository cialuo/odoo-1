odoo.define("line_map_production_sz_tmp.line_map_production", function(require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var Model = require('web.Model');
    // 线路
    var model_choseline = new Model('route_manage.route_manage');
    // 站点
    model_site = new Model('opertation_resources_station_platform');
    // 站点信息
    model_station = new Model('opertation_resources_station');
    // 地图线路配置
    var model_map_line_info= new Model('map.line.production.info');
    // 配置文件
    var config_parameter = new Model('ir.config_parameter');
    

    // 加载高德地图组件
    // $.getScript("http://webapi.amap.com/maps?v=1.3&key=cf2cefc7d7632953aa19dbf15c194019");
    // $.getScript("http://webapi.amap.com/maps?v=1.4.1&key=505ae72a86391b207f7e10137f51194a");

    // 获取基础数据
    var line_map_production_base = Widget.extend({
        template: "tmp_map_production_base_template",
        init: function (parent) {
            this._super(parent);
            this.layer = layer.msg("加载中...", {time: 0, shade: 0.3});
        },
        start: function () {
            var self = this;
            model_choseline.query().filter([
                ["state", "=", 'inuse']
            ]).all().then(function(lineData) {
                config_parameter.query().filter([["key", "=", "dispatch.gdmap.service"]]).all().then(function (gdmap) {
                    config_parameter.query().filter([["key", "=", 'city.code']]).all().then(function (citys) {
                        var gdmap_url = gdmap[0].value;
                        var options = {
                            lineData: lineData,
                            cityCode: citys[0].value,
                            layer_index: self.layer
                        };
                        // 加载高德地图组件
                        $.getScript(gdmap_url, function(){
                            new line_map_production_w(self, options).appendTo(self.$el); 
                        });
                    });
                });
            });
        }
    });


    // 加载页面
    var line_map_production_w = Widget.extend({
        template: "tmp_line_map_production_template",
        init: function(parent, options) {
            this._super(parent);
            layer.close(options.layer_index);
            this.lineData = options.lineData;
            this.cityCode = options.cityCode;
            // 默认属性
            this.base_map_set = {
                tools_line_color: '#000000',                  //线条颜色
                tools_line_width: '1',                     //线条宽度
                tools_station_font_family: '宋体',           //站点字体
                tools_station_font_color: '#000000',          //标签颜色
                tools_station_font_style: '●',             //站点样式
                tools_station_font_style_color: '#000000',    //站点样式颜色
                tools_import_trajectory_color: '#000000',     //导入轨迹颜色
                tools_import_trajectory_width: '1',        //导入轨迹宽度
            };
            this.typeInfo = [{
                   name: "围栏点",
                   value: "1"
               },
               {
                   name: "转弯点",
                   value: "2"
               },
               {
                   name: "上下坡",
                   value: "3"
               },
               {
                   name: "交叉路口",
                   value: "4"
               },
               {
                   name: "事故多发",
                   value: "5"
               },
               {
                   name: "换向点",
                   value: "6"
               },
           ];
            this.switch = false;
        },
        start: function() {
            var self = this;
            var tmp_map_page = self.$(".tmp_map_page");
            // 地图层级关系
            var location_set = {
                zoom: 11
            };

            // 初始化地图
            var map = new AMap.Map(tmp_map_page[0], {
                resizeEnable: true,
                zoom: location_set.zoom
            });

            // 根据citycode定位城市中心点
            map.setCity(self.cityCode);
            self.map = map;

            // 获取地图中心点
            mapCenter = map.getCenter();
            location_set.center = [mapCenter.lng, mapCenter.lat];

            // 加载地图工具
            self.map_toolBar(map);

            // 加载地图鼠标位置信息
            self.map_mouse_pos_fn(map);

            // 加载地图工具栏
            new line_map_production_line_set_w(self, self.lineData, location_set, self.base_map_set).appendTo(tmp_map_page);

            // 工具栏事件
            self.operation_map_func(map);

            // 初始化轨迹
            self.load_draw_line_map_screening();
            
        },
        // 工具栏事件
        operation_map_func: function(map){
            var self = this;
            var tmp_map_page = self.$(".tmp_map_page");
            var typeInfo = self.typeInfo;

            // 工具栏切换
            tmp_map_page.on("click", ".nav a", function(){
                $(this).addClass("active_nav").siblings().removeClass("active_nav");
                if ($(this).hasClass("set_line_bt")){
                    self.$(".editMapSetTools").addClass("hide_model");
                    self.$(".editLineMap").removeClass("hide_model");
                }else{
                    self.$(".editLineMap").addClass("hide_model");  
                    self.$(".editMapSetTools").removeClass("hide_model");  
                }
            });

            // 修改线路与方向
            tmp_map_page.on("change", ".line, .direction", function(){
                self.init_map_fn();
            });

            // 画笔开关
            tmp_map_page.on("click", ".hb_bt", function(){
                tmp_map_page.find(".hb_bt").removeClass("active_bt");
                $(this).addClass('active_bt');
                if ($(this).hasClass("start_bt")){
                    self.start_draw_fn();
                }else if ($(this).hasClass("fix_bt")){
                    self.fix_draw_fn(map);
                }else{
                    self.stop_draw_fn();
                }
            });

            // 清除线路轨迹
            tmp_map_page.on("click", ".clear_bt", function(){
                self.clear_draw_info_fn();
            });

            // 轨迹导入
            tmp_map_page.on("click", ".lead_in_bt", function(){
                alert("开发中...");
            });

            // 清除导入轨迹
            tmp_map_page.on("click", ".clear_locus_bt", function(){
                alert("开发中...");
            });

            // 更改路点属性
            tmp_map_page.on("change", ".roadType", function(){
                var gpsKey = $(this).parents("tr").attr("class");
                var type = $(this).val();
                if (!self.point_marker_type_dict[gpsKey]){
                    self.point_marker_type_dict[gpsKey] = {};
                }
                self.point_marker_type_dict[gpsKey].roadType = type;
            });

            // 定位突出
            tmp_map_page.on("click", ".edit_gprs_bt", function(){
                var tr_obj = $(this).parents("tr");
                var lng = tr_obj.attr("lng");
                var lat = tr_obj.attr("lat");
                var map = self.map;
                map.setCenter([lng, lat]);
                map.setZoom(18);
                var marker = new AMap.Marker({
                    content: '<div class="edit_status_marker"></div>',
                    offset : new AMap.Pixel(-15,-15),
                    position: [lng, lat],
                    map: map
                });
                if (self.fix_marker){
                    self.fix_marker.setMap(null);
                }
                self.fix_marker = marker;
                
            });

            // 辅助点显示切换
            tmp_map_page.on("click", ".isShowPoint", function() {
                self.isShowPoint_fn(this.checked);
            });

            // 地图划线配置修改
            tmp_map_page.on("change", ".mapLineSet", function(){
                self.set_map_line_type();
            });

            // 导入轨迹配置修改
            tmp_map_page.on("change", ".mapTrajectoryLineSet", function(){
                self.set_map_trajectory_line_type();
            });

            // 站点显示属性设置
            tmp_map_page.on("change", ".siteTypeSet", function(){
                self.set_map_site_type();
            });

            // 站点显示
            tmp_map_page.on("change", ".siteShowTypeSet", function(){
                self.set_map_site_type();
            });

            // 导出export_file
            tmp_map_page.on("click", ".lead_out_bt", function(){
                alert("开发中...");
            });

            // 保存
            tmp_map_page.on("click", ".save_bt", function(){
                self.save_data_fn();
            });

            // 地图点击事件
            var clickEventListener = map.on('click', function(e) {
                var lnglat = e.lnglat;
                var now_gps = lnglat.lng.toString().replace(".", "d") + "_" + lnglat.lat.toString().replace(".", "d");
                var configurationInfo = self.get_configuration_fn();
                var lineArgs = self.getLineArgs();
                // 如果没有线路信息将终止执行
                if (!lineArgs){
                    return false;
                }
                // 相同的坐标点只采集一次；
                if (self.his_gps && self.his_gps == now_gps){
                    return false;
                }
                if (self.switch) {
                    self.his_gps = now_gps;
                    if (configurationInfo.isShowPoint){
                        self.add_point_fn(map, lnglat);
                    }
                    self.$(".mapGprs").append(QWeb.render("mapGprsTr", {gps: lnglat, typeInfo: typeInfo}));
                    var gpsKey = "gps_"+now_gps;
                    self.point_marker_type_dict[gpsKey] = {};
                    if (self.polyline){
                        var bush_trajectory_marker_list = self.polyline.getPath();
                        bush_trajectory_marker_list.push(lnglat);
                        var set_polyline_gps_list = new Array().concat(bush_trajectory_marker_list);
                        self.polyline.setPath(set_polyline_gps_list);
                    } else {
                        self.polyline = new AMap.Polyline({
                            path: [lnglat],
                            strokeColor: configurationInfo.tools_line_color,
                            strokeWeight: configurationInfo.tools_line_width,
                            lineJoin: "round"
                        });
                        self.polyline.setMap(map);
                        self.bing_map_poly_edit(map);
                    }
                }
            });
        },
        // 初始化地图
        init_map_fn: function(){
            this.map.setCity(this.cityCode);
            // 清楚地图浮层
            this.map.clearMap();
            // 初始化地图站点marker
            this.site_list = [];
            this.site_marker_list = [];
            // 初始化地图辅助点marker
            this.point_marker_list = [];
            this.point_marker_type_dict = {};
            // 初始化地图画笔轨迹
            this.polyline = "";
            this.polylineEditor = "";
            // 初始化修改marker
            this.fix_marker = "";
            // 初始化导入轨迹
            this.trajectory_polyline = "";
            // 加载地图信息
            this.get_draw_line_map_info();
        },
        // 画笔划线
        start_draw_fn: function(){
            this.switch = true;
            if (this.polylineEditor){
                this.polylineEditor.close();
            }
        },
        // 画笔修改
        fix_draw_fn: function(map){
            var self = this;
            self.switch = false;
            if (self.polylineEditor){
                self.polylineEditor.open();
                // 增加历史找对应修改对象
                self.his_path_gps_list = new Array().concat(self.polyline.getPath());
            }
        },
        // 停止画笔
        stop_draw_fn: function(){
            this.switch = false;
            if (this.polylineEditor){
                this.polylineEditor.close();
            }
        },
        // 清除线路轨迹
        clear_draw_info_fn: function(){
            // 清楚地图浮层
            this.map.clearMap();
            // 初始化地图辅助点marker
            this.point_marker_list = [];
            this.point_marker_type_dict = {};
            // 初始化地图画笔轨迹
            this.polyline = "";
            this.polylineEditor = "";
            // 初始化修改marker
            this.fix_marker = "";
            // 初始化划线图表信息
            this.load_draw_line_map_screening();
            // 加载地图信息
            this.load_site_info(this.site_list);
            // 加载导入轨迹
        },
        // 画笔修改绑定相关事件
        load_polylineEditor_fn: function(polylineEditor){
            var self = this;
            // 增加
            polylineEditor.on("addnode", function(e){
                self.update_polyline_data(e);
            });
            // 修改
            polylineEditor.on("adjust", function(e){
                self.update_polyline_data(e);
            });
            // 删除
            polylineEditor.on("removenode", function(e){
                self.update_polyline_data(e);
            });
            // 结束编辑
            polylineEditor.on("end", function(e){
                self.isShowPoint_condition_fn();
            });
        },
        // 更新
        update_polyline_data: function(e){
            var self = this;
            if (self.fix_marker){
                self.fix_marker.setMap(null);
            }
            self.isShowPoint_fn(false);
            var path_gps_list = self.polyline.getPath();
            var configurationInfo = self.get_configuration_fn();
            if (e.type == "adjust"){
                var his_path_gps_list = self.his_path_gps_list;
                for (var i=0,l=path_gps_list.length; i<l;i++){
                    var now_gps = path_gps_list[i];
                    var his_gps = his_path_gps_list[i];
                    var now_gps_key = "gps_"+now_gps.lng.toString().replace('.', 'd')+"_"+now_gps.lat.toString().replace('.', 'd');
                    var his_gps_key = "gps_"+his_gps.lng.toString().replace('.', 'd')+"_"+his_gps.lat.toString().replace('.', 'd');
                    if (now_gps_key!=his_gps_key){
                        self.point_marker_type_dict[now_gps_key] = self.point_marker_type_dict[his_gps_key];
                        delete self.point_marker_type_dict[his_gps_key];
                        break;
                    }
                }
            }
            self.his_path_gps_list = new Array().concat(self.polyline.getPath());
            self.load_draw_line_map(path_gps_list, self.point_marker_type_dict);
        },
        // 根具条件是否显示辅助点
        isShowPoint_condition_fn: function(){
            var configurationInfo = this.get_configuration_fn();
            if (configurationInfo.isShowPoint){
                this.isShowPoint_fn(true);
            }
        },
        // 显示辅助点
        isShowPoint_fn: function(is_checked){
            var self = this;
            var map = self.map;
            if (!self.polyline){
                return false;
            }
            var path_gps_list = self.polyline.getPath();
            if (is_checked){
                _.each(path_gps_list, function(el) {
                    self.add_point_fn(map, el);
                });
            }else{
                var point_marker_list = self.point_marker_list;
                _.each(point_marker_list, function(ol) {
                    ol.setMap(null);
                });
                self.point_marker_list = [];
            }
        },
        // 添加辅助点
        add_point_fn: function(map, pos){
            var marker = new AMap.Marker({
                content: '<div class="ancillary">•</div>',
                position: pos,
                map: map
            });
            this.point_marker_list.push(marker);
        },
        // 根据划线属性渲染划线
        set_map_line_type: function() {
            var configurationInfo = this.get_configuration_fn();
            if (this.polyline) {
                this.polyline.setOptions({
                    strokeColor: configurationInfo.tools_line_color,
                    strokeWeight: configurationInfo.tools_line_width
                });
            }
        },
        // 根据导入轨迹属性渲染划线
        set_map_trajectory_line_type: function() {
            var configurationInfo = this.get_configuration_fn();
            if (this.trajectory_polyline) {
                this.trajectory_polyline.setOptions({
                    strokeColor: configurationInfo.tools_import_trajectory_color,
                    strokeWeight: configurationInfo.tools_import_trajectory_width
                });
            }
        },
        set_map_site_type: function(){
            var configurationInfo = this.get_configuration_fn();
            var site_marker_list = this.site_marker_list;
            _.each(site_marker_list, function(ol) {
                ol.setMap(null);
            });
            this.load_site_info(this.site_list);
        },
        // 获取线路信息
        get_draw_line_map_info: function(){
            var self = this;
            var lineArgs = self.getLineArgs();
            if (!lineArgs){
                self.load_draw_line_map_screening();
                return false;
            }
            self.load_layer = layer.msg("加载中...", { time: 0, shade: 0.3 });
            model_map_line_info.query().filter([
                ["line_id", "=", parseInt(lineArgs.line_id)],
                ["direction", "=", lineArgs.direction],
            ]).all().then(function(trackData) {
                if (trackData.length > 0){
                    var trackInfo = trackData[0];
                    // 渲染工具配置
                    self.set_configuration_fn(trackInfo);
                }   
                model_site.query().order_by("sequence").filter([
                    ["route_id", "=", parseInt(lineArgs.line_id)],
                    ["direction", "=", lineArgs.direction],
                ]).all().then(function(site_list) {
                    self.site_list = site_list;
                    self.load_site_info(site_list);
                    self.load_draw_line_map_screening(trackData);
                });
            });
        },
        // 加载站点信息
        load_site_info: function(site_list){
            var self = this;
            var map = self.map;
            if (site_list == 0){
                layer.close(self.load_layer);
                return false;
            }
            var configurationInfo = self.get_configuration_fn();
            if (!configurationInfo.isShowStation && !configurationInfo.isShowStationName){
                return false;
            }
            for (var i = 0; i < site_list.length; i++) {
                var site_i = site_list[i];
                model_station.query().filter([
                    ["id", "=", parseInt(site_i.station_id)]
                ]).all().then(function(site_l) {
                    var site = site_l[0];
                    var new_gps = CONVERSIONS_GPS.gcj_encrypt(site.latitude, site.longitude);
                    var cont_W = site.name.length * 14 - 12;
                    var site_name_str = "";
                    var site_name_icon_str = "";
                    if (configurationInfo.isShowStationName) {
                        site_name_str = '<p class="siteName" style="position: absolute; z-index: 1; top:-18px; left: -' + cont_W / 2 + 'px; font-family:' + configurationInfo.tools_station_font_family + ';color:' + configurationInfo.tools_station_font_color + ';">' +
                            site.name +
                            '</p>';
                    }
                    if (configurationInfo.isShowStation) {
                        site_name_icon_str = '<p class="siteIcon" style="position: absolute; z-index:1; top: 0; left: 0; color: ' + configurationInfo.tools_station_font_style_color + '">' +
                            configurationInfo.tools_station_font_style +
                            '</p>';
                    }
                    var content_info =
                        '<div class="cont">' +
                        site_name_str +
                        site_name_icon_str + 
                        '</div>';

                    var marker = new AMap.Marker({
                        content: content_info,
                        position: [new_gps.lon, new_gps.lat],
                        offset : new AMap.Pixel(0,-15),
                        map: map,
                    });
                    self.site_marker_list.push(marker);
                    if (i == site_list.length){
                        layer.close(self.load_layer);
                    }
                });
            }
        },
        // 加载线路轨迹数据之前的条件筛选
        load_draw_line_map_screening: function(trackData){
            var gprsInfo = [];
            if (trackData && trackData.length>0){
                trackInfo = trackData[0];
                if (trackInfo.map_data_v2){
                    gprsInfo = JSON.parse(trackInfo.map_data_v2);
                    if (gprsInfo.length>0){
                        this.his_draw_line_map(gprsInfo);
                    }
                }
            }
            this.load_draw_line_map(gprsInfo);
        },
        // 加载线路轨迹数据
        load_draw_line_map: function(gprsInfo, point_marker_type_dict){
            this.$(".mapGprsBox").html("");
            var typeInfo = this.typeInfo;
            new map_gprs_w(this, gprsInfo, typeInfo, point_marker_type_dict).appendTo(this.$(".mapGprsBox"));
        },
        // 渲染画笔轨迹
        his_draw_line_map: function(gprsInfo){
            var self = this;
            var map = self.map;
            var configurationInfo = self.get_configuration_fn();
            var new_gprs_info = [];
            _.each(gprsInfo, function(oe){
                if (oe.azimuthType || oe.roadType){
                    var gpsKey = "gps_"+oe.lng.toString().replace('.', 'd')+"_"+oe.lat.toString().replace('.', 'd');
                    var type_dict = {};
                    if (oe.azimuthType){
                        type_dict.azimuthType = oe.azimuthType;
                    }
                    if (oe.roadType){
                        type_dict.roadType = oe.roadType;
                    }
                    self.point_marker_type_dict[gpsKey] = type_dict;
                }
                new_gprs_info.push([oe.lng, oe.lat]);
            });
            var polyline = new AMap.Polyline({
                path: new_gprs_info,
                strokeColor: configurationInfo.tools_line_color,
                strokeWeight: configurationInfo.tools_line_width,
                lineJoin: "round"
            });
            polyline.setMap(map);
            self.polyline = polyline;
            self.bing_map_poly_edit(map);
        },
        bing_map_poly_edit: function(map){
            var self = this;
            map.plugin(["AMap.PolyEditor"],function(){
                self.polylineEditor = new AMap.PolyEditor(map, self.polyline);
                self.load_polylineEditor_fn(self.polylineEditor);
            });
        },
        save_data_fn: function(){
            var self = this;
            var configuration = self.get_configuration_fn();
            var lineInfo = self.getLineArgs();
            if (!self.polyline){
                var layer_index = layer.msg('没有任何数据可以保存', {time: 1000, shade: 0.3});
                return false;
            }
            model_map_line_info.query().filter([
                ["line_id", "=", parseInt(lineInfo.line_id)],
                ["direction", "=", lineInfo.direction]
            ]).all().then(function(map_line) {
                var gprs_info = self.get_gprs_info();
                var layer_index = layer.msg('保存中...', {time: 0, shade: 0.3});
                if (map_line.length>0){
                    console.log(map_line[0].id);
                    model_map_line_info.call("write", [map_line[0].id,
                    {
                        'map_data_v2': JSON.stringify(gprs_info),
                        'tools_line_color': configuration.tools_line_color,
                        'tools_line_width': configuration.tools_line_width,
                        'tools_station_font_family': configuration.tools_station_font_family,
                        'tools_station_font_color': configuration.tools_station_font_color,
                        'tools_station_font_style': configuration.tools_station_font_style,
                        'tools_station_font_style_color': configuration.tools_station_font_style_color,
                        'tools_import_trajectory_color': configuration.tools_import_trajectory_color,
                        'tools_import_trajectory_width': configuration.tools_import_trajectory_width
                    }]).then(function (res) {
                        layer.close(layer_index);
                        layer.msg('保存成功', {time: 1000, shade: 0.3});
                    });
                }else{
                    model_map_line_info.call("create", [
                        {
                            'line_id': parseInt(lineInfo.line_id),
                            'direction': lineInfo.direction,
                            'map_data_v2': JSON.stringify(gprs_info),
                            'tools_line_color': configuration.tools_line_color,
                            'tools_line_width': configuration.tools_line_width,
                            'tools_station_font_family': configuration.tools_station_font_family,
                            'tools_station_font_color': configuration.tools_station_font_color,
                            'tools_station_font_style': configuration.tools_station_font_style,
                            'tools_station_font_style_color': configuration.tools_station_font_style_color,
                            'tools_import_trajectory_color': configuration.tools_import_trajectory_color,
                            'tools_import_trajectory_width': configuration.tools_import_trajectory_width
                        }]).then(function () {
                        layer.close(layer_index);
                        layer.msg('保存成功', {time: 1000, shade: 0.3});
                    });
                }
            });
        },
        get_gprs_info: function(){
            var self = this;
            var gprs_info = self.polyline.getPath();
            var new_gprs_info = [];
            var point_marker_type_dict = self.point_marker_type_dict;
            for (var i=0,l=gprs_info.length; i<l;i++){
                var gpsObj = gprs_info[i];
                var gps_key = "gps_"+gpsObj.lng.toString().replace('.', 'd')+"_"+gpsObj.lat.toString().replace('.', 'd');
                if (point_marker_type_dict[gps_key]){
                    var typeObj = point_marker_type_dict[gps_key];
                    if (typeObj.azimuthType){
                        gpsObj.azimuthType = typeObj.azimuthType;
                    }
                    if (typeObj.roadType){
                        gpsObj.roadType = typeObj.roadType;
                    }
                }
                new_gprs_info.push(gpsObj);
            }
            return new_gprs_info;
        },
        // 工具配置
        set_configuration_fn: function(trackInfo){
            var base_map_set = this.base_map_set,
                $tools_line_color = this.$(".tools_line_color"),
                $tools_line_width = this.$(".tools_line_width"),
                $tools_import_trajectory_color = this.$(".tools_import_trajectory_color"),
                $tools_import_trajectory_width = this.$(".tools_import_trajectory_width"),
                $tools_station_font_family = this.$(".tools_station_font_family"),
                $tools_station_font_color = this.$(".tools_station_font_color"),
                $tools_station_font_style = this.$(".tools_station_font_style"),
                $tools_station_font_style_color = this.$(".tools_station_font_style_color");
            trackInfo.tools_line_color ? $tools_line_color.val(trackInfo.tools_line_color) : $tools_line_color.val(base_map_set.tools_line_color);
            trackInfo.tools_line_width ? $tools_line_width.val(trackInfo.tools_line_width) : $tools_line_width.val(base_map_set.tools_line_width);
            trackInfo.tools_import_trajectory_color ? $tools_import_trajectory_color.val(trackInfo.tools_import_trajectory_color) : $tools_import_trajectory_color.val(base_map_set.tools_import_trajectory_color);
            trackInfo.tools_import_trajectory_width ? $tools_import_trajectory_width.val(trackInfo.tools_import_trajectory_width) : $tools_import_trajectory_width.val(base_map_set.tools_import_trajectory_width);
            trackInfo.tools_station_font_family ? $tools_station_font_family.val(trackInfo.tools_station_font_family) : $tools_station_font_family.val(base_map_set.tools_station_font_family);
            trackInfo.tools_station_font_color ? $tools_station_font_color.val(trackInfo.tools_station_font_color) : $tools_station_font_color.val(base_map_set.tools_station_font_color);
            trackInfo.tools_station_font_style ? $tools_station_font_style.val(trackInfo.tools_station_font_style) : $tools_station_font_style.val(base_map_set.tools_station_font_style);
            trackInfo.tools_station_font_style_color ? $tools_station_font_style_color.val(trackInfo.tools_station_font_style_color) : $tools_station_font_style_color.val(base_map_set.tools_station_font_style_color);
        },
        // 获取工具配置参数
        get_configuration_fn: function(){
            return {
                tools_line_color : this.$(".tools_line_color").val(),
                tools_line_width : this.$(".tools_line_width").val(),
                tools_import_trajectory_color : this.$(".tools_import_trajectory_color").val(),
                tools_import_trajectory_width : this.$(".tools_import_trajectory_width").val(),
                tools_station_font_family: this.$(".tools_station_font_family").val(),
                tools_station_font_color : this.$(".tools_station_font_color").val(),
                tools_station_font_style : this.$(".tools_station_font_style").val(),
                tools_station_font_style_color : this.$(".tools_station_font_style_color").val(),
                isShowPoint: this.$(".isShowPoint")[0].checked,
                isShowStation: this.$(".isShowStation")[0].checked,
                isShowStationName: this.$(".isShowStationName")[0].checked
            };
        },
        // 获取线路与方向
        getLineArgs: function(){
            var line_id = this.$(".line").val();
            var direction = this.$(".direction").val();
            if (line_id){
                return {
                    line_id: line_id,
                    direction: direction
                };
            }
            return false;
        },
        // 地图鼠标基本事件
        map_mouse_pos_fn:function(map) {
            var self = this;
            // 显示经纬度
            map.on('mousemove', function(e) {
                self.$('.lnglat').html(e.lnglat.getLng() + ',' + e.lnglat.getLat());
            });
            // 显示缩放级别
            map.on('zoomend', function(e) {
                self.$('.map_zoom').html(map.getZoom());
            });
        },
        // 地图工具
        map_toolBar: function(map) {
            map.plugin(["AMap.ToolBar"], function() {
                map.addControl(new AMap.ToolBar({ locate: false }));
            });
            if (location.href.indexOf('&guide=1') !== -1) {
                map.setStatus({ scrollWheel: false });
            }
        }
    });

    core.action_registry.add('lty_line_map_sz_tmp.line_map_production', line_map_production_base);

    // 制作工具栏
    var line_map_production_line_set_w = Widget.extend({
        template: "tmp_line_map_production_line_set_template",
        init: function(parent, lineData, location_set, base_map_set){
            this._super(parent);
            this.lineData = lineData;
            this.location_set = location_set;
            this.family_list = ['宋体', '微软雅黑', '华文细黑', '黑体', 'sans-serif', 'serif'];
            this.station_style_list = ['●', '★', '◆', '◇', '▲'];
            this.base_map_set = base_map_set;
        },
    });

    //  gprs坐标表格
    map_gprs_w = Widget.extend({
        template: "tmp_map_gprs_template",
        init: function(parent, gprsInfo, typeInfo, point_marker_type_dict){
            this._super(parent);
            this.gprsInfo = gprsInfo;
            this.typeInfo = typeInfo;
            this.point_marker_type_dict = point_marker_type_dict;
        }
    });
});