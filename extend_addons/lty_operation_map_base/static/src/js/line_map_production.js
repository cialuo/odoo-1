odoo.define("line_map_production.line_map_production", function(require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var Model = require('web.Model');
    // 地图线路配置
    var model_map_line_info= new Model('map.line.production.info');

    // 加载高德地图组件
    $.getScript("http://webapi.amap.com/maps?v=1.3&key=cf2cefc7d7632953aa19dbf15c194019");

    var line_map_production = Widget.extend({
        template: "line_map_production_template",
        init: function(parent) {
            this._super(parent);
        },
        start: function() {
            var self = this;

            // 城市中心点及地图级别
            var location_set = {
                zoom: 10,
                center: [116.408075, 39.950187]
            }

            var map = new AMap.Map(this.$(".mapPage")[0], {
                resizeEnable: true,
                zoom: location_set.zoom,
                center: location_set.center
            });
            this.map_toolBar(map);
            location_set.map = map;

            // 线路
            var model_choseline = new Model('route_manage.route_manage');
            model_choseline.query().filter([
                ["state", "=", 'inuse']
            ]).all().then(function(data) {
                new line_map_production_line_set(self, data, location_set).appendTo(self.$(".mapPage"));
            });
        },
        map_toolBar: function(map) {
            map.plugin(["AMap.ToolBar"], function() {
                map.addControl(new AMap.ToolBar({ locate: false }));
            });
            if (location.href.indexOf('&guide=1') !== -1) {
                map.setStatus({ scrollWheel: false })
            }
        }
    });

    core.action_registry.add('scheduling_parameters.line_map_production', line_map_production);

    var line_map_production_line_set = Widget.extend({
        template: 'line_map_production_line_set_template',
        events: {},
        init: function(parent, lineData, location_set) {
            this._super(parent);
            this.line_data = lineData;
            this.location_set = location_set;
            // 上行下行站点
            this.model_site = new Model('opertation_resources_station_platform');
            // 站点信息
            // this.model_site_info = new Model('map_line_station_info');
        },
        start: function() {
            var self = this;
            var map = self.location_set.map;
            var site_dict = {};
            // 选择线路
            self.$('.mapSetLineDiv').on('change', 'select.line', function() {
                self.line_id = $(this).val();
                self.$('.mapSet').html('');
                if (self.line_id == '') {
                    return;
                }
                model_map_line_info.query().filter([
                    ["line_id", "=", parseInt(self.line_id)]
                ]).all().then(function(set_list) {
                    // 默认配置显示
                    var his_dict = {
                        '0': {
                            gps_list: [],
                            c: '#000',        //线条颜色
                            w: '2',           //线条宽度
                            family: '宋体',   //站点字体
                            f_color: '#000',  //标签颜色
                            style: '●',       //站点样式
                            s_color: '#000'   //站点样式颜色
                        },
                        '1': {
                            gps_list: [],
                            c: '#000',
                            w: '2',
                            family: '宋体',
                            f_color: '#000',
                            style: '●',
                            s_color: '#000'
                        }
                    };
                    if (set_list.length > 0){
                        _.each(set_list, function(set){
                            var direction = set.direction=='up'?'0':'1'
                            his_dict[direction].gps_list = JSON.parse(set.map_data);
                            his_dict[direction].c = set.tools_line_color;
                            his_dict[direction].w = set.tools_line_width;
                            his_dict[direction].family = set.tools_station_font_name;
                            his_dict[direction].f_color = set.tools_station_font_color;
                            his_dict[direction].style = set.tools_station_font_style;
                            his_dict[direction].s_color = set.tools_line_font_style_color;
                        });
                    }
                    self.model_site.query().filter([
                        ["route_id", "=", parseInt(self.line_id)]
                    ]).all().then(function(site_info) {
                        var site_top_list = [];
                        var site_down_list = [];
                        _.each(site_info, function(ret) {
                            console.log(ret);
                            if (ret.direction == "up") {
                                site_top_list.push(ret);
                            } else {
                                site_down_list.push(ret);
                            }
                        });
                        var options = {
                            map: map,
                            site_dict: { '0': site_top_list, '1': site_down_list },
                            his_dict: his_dict,
                            line_id: self.line_id
                        };
                        new line_map_production_set(self, options).appendTo(self.$('.mapSet'));
                    });
                });
            });
            self.map_binding_fn(map);
        },
        map_binding_fn:function(map) {
            var self = this;
            // 显示经纬度
            map.on('mousemove', function(e) {
                self.$('.lnglat').html(e.lnglat.getLng() + ',' + e.lnglat.getLat());
            });
            // 显示缩放级别
            map.on('zoomend', function(e) {
                self.$('.map_zoom').html(map.getZoom());
            });
        }
    });


    var line_map_production_set = Widget.extend({
        template: 'line_map_production_set_template',
        events: {

        },
        init: function(parent, options) {
            this._super(parent);
            this.options = options;
            // 站点信息
            this.model_station = new Model('opertation_resources_station');
            this.family_list = ['宋体', '微软雅黑', '华文细黑', '黑体', 'sans-serif', 'serif'];
            this.station_style_list = ['●', '★', '◆', '◇', '▲'];
        },
        start: function() {
            var self = this;
            self.ancillary_list = [];
            self.isShowPoint = false;
            var map = self.options.map;
            var line_id = self.options.line_id;
            self.direction = self.$("input[name='direction']").val();

            // 地图划线事件
            self.$('.mapSetLineContext').on('click', '.setMapBt input', function() {
                $(this).addClass('active_bt').siblings().removeClass('active_bt');

                if ($(this).hasClass('open_bt')) {
                    self.openBrush(map);
                } else if ($(this).hasClass('close_bt')) {
                    self.closeBrush();
                } else if ($(this).hasClass('del_bt')) {
                    self.delLsatLine();
                } else {
                    self.emptyLine();
                }
            });

            // 辅助点显示切换
            self.$('.mapSetLineContext').on('click', '.isShowPoint', function() {
                self.isShowPoint = false;
                if (this.checked) {
                    self.isShowPoint = true;
                }
                self.isShowPoint_fn(map);
            });

            // 修改站点属性触发事件
            self.$('.stationAttribute').on('change', '.siteType', function() {
                self.set_site_type();
            });

            // 地图划线配置属性
            self.$('.mapSetLineContext').on('change', '.mapLineSet', function() {
                self.set_map_line_type();
            });

            // 上下行切换
            self.$('.mapSetLineContext').on('click', '.direction_bt', function(){
                var v = $(this).val();
                if (self.direction == v){
                    return;
                }
                self.direction = v;
                self.init_map_fn(map, self.direction);
            });

            // 保存
            self.$('.dataSave').on('click', '.save_bt', function(){
                var tools_info = self.getMapLineInfo();
                var site_info = self.getSiteInfo();
                var direction = self.direction==0?'up':'down'
                model_map_line_info.query().filter([
                    ["line_id", "=", parseInt(line_id)],
                    ["direction", "=", direction]
                ]).all().then(function(set_list) {
                    if (set_list.length>0){
                        model_map_line_info.call("write", [set_list[0].id,
                        {
                            'map_data': JSON.stringify(self.polyline_gps_list),
                            'tools_line_color': tools_info.color,
                            'tools_line_width': tools_info.lineW,
                            'tools_station_font_family': site_info.family,
                            'tools_station_font_color': site_info.color,
                            'tools_station_font_style': site_info.lab,
                            'tools_station_font_style_color': site_info.lab_color,
                        }]).then(function (res) {
                            layer.close(layer_index);
                            layer.msg('保存成功', {time: 2000, shade: 0.3});
                        });
                    }else{
                        var layer_index = layer.msg('保存中...', {time: 0, shade: 0.3});
                        model_map_line_info.call("create", [
                            {
                                'line_id': parseInt(line_id),
                                'direction': direction,
                                'map_data': JSON.stringify(self.polyline_gps_list),
                                'tools_line_color': tools_info.color,
                                'tools_line_width': tools_info.lineW,
                                'tools_station_font_family': site_info.family,
                                'tools_station_font_color': site_info.color,
                                'tools_station_font_style': site_info.lab,
                                'tools_station_font_style_color': site_info.lab_color,
                            }]).then(function () {
                            layer.close(layer_index);
                            layer.msg('保存成功', {time: 2000, shade: 0.3});
                        });
                    }
                })
            });

            // 取消
            self.$('.dataSave').on('click', '.back_bt', function(){
                // alert("w");
            });

            // 初始化地图事件
            self.init_map_fn(map, self.direction);
        },
        isShowPoint_fn(map){
            var self = this;
            if (self.isShowPoint) {
                _.each(self.polyline_gps_list, function(ret, index) {
                    var pos = [];
                    if (ret.lng) {
                        pos = [ret.lng, ret.lat];
                    } else {
                        pos = [ret[0], ret[1]];
                    }
                    self.add_point_fn(map, pos);
                });
            } else {
                self.delete_point_fn();
            }
        },
        add_point_fn: function(map, pos){
            var marker = new AMap.Marker({
                content: '<div class="ancillary">•</div>',
                position: pos,
                map: map
            });
            this.ancillary_list.push(marker);
        },
        delete_point_fn: function(index){
            var self = this;
            if (typeof index=="number"){
                self.ancillary_list[index].setMap(null);
                self.ancillary_list.pop();
                return false;
            }
            _.each(self.ancillary_list, function(ret) {
                ret.setMap(null);
            });
            self.ancillary_list = [];
        },
        init_map_fn: function(map, direction){
            var self = this;
            // 地图图层清空;
            map.clearMap();

            // 初始化站点信息
            self.site_line(map, self.options.site_dict[direction]);

            // 初始化历史制定线路
            self.load_his_establishment_line(map, self.options.his_dict[direction], self.options.site_dict[direction]);
        },
        // 打开
        openBrush: function(map) {
            var self = this;
            self.switch = true;
            // var mouseTool = new AMap.MouseTool(map);
            var clickEventListener = map.on('click', function(e) {
                if (self.switch) {
                    // mouseTool.marker({offset:new AMap.Pixel(-14,-11)});
                    var gps = [e.lnglat.getLng(), e.lnglat.getLat()];
                    self.polyline_gps_list.push(gps);
                    self.polyline.setPath(self.polyline_gps_list);
                    if (self.isShowPoint){
                        self.add_point_fn(map, gps);
                    }
                }
            });
        },
        // 关闭
        closeBrush: function() {
            this.switch = false;
        },
        // 删除
        delLsatLine: function() {
            var self = this;
            if (self.polyline_gps_list.length > 1) {
                self.polyline_gps_list.pop();
                self.polyline.setPath(self.polyline_gps_list);
                self.delete_point_fn(self.ancillary_list.length-1);
            }
        },
        // 清空重画-默认第一个点为起始站
        emptyLine: function() {
            var self = this;
            if (self.polyline_gps_list.length > 1) {
                self.polyline_gps_list = [self.polyline_gps_list[0]];
                self.polyline.setPath(self.polyline_gps_list);
                self.delete_point_fn();
            }
        },
        load_his_establishment_line: function(map, hisObj, site_list) {
            var self = this;
            if (hisObj.gps_list.length > 0) {
                var polyline = new AMap.Polyline({
                    path: hisObj.gps_list,
                    strokeColor: hisObj.c,
                    strokeWeight: hisObj.w,
                    lineJoin: "round"
                });
                polyline.setMap(map);
                self.polyline_gps_list = hisObj.gps_list;
                self.polyline = polyline;
            } else {
                // 默认第一个点为起始站
                self.model_station.query().filter([
                    ["id", "=", parseInt(site_list[0].station_id)]
                ]).all().then(function(ret) {
                    self.polyline_gps_list = [
                        [ret[0].longitude, ret[0].latitude]
                    ];
                    var polyline = new AMap.Polyline({
                        path: self.polyline_gps_list,
                        strokeColor: hisObj.c,
                        strokeWeight: hisObj.w,
                        lineJoin: "round"
                    });
                    polyline.setMap(map);
                    self.polyline = polyline;
                });
            }
        },
        set_map_line_type: function() {
            var info = this.getMapLineInfo();
            if (this.polyline) {
                this.polyline.setOptions({
                    strokeColor: info.color,
                    strokeWeight: info.lineW
                });
            }
        },
        set_site_type: function() {
            var contentInfo = this.getSiteInfo();
            var obj = this.$el.parents('.mapPage');
            obj.find('.siteName').css({
                'font-family': contentInfo.family,
                'color': contentInfo.color,
                'display': contentInfo.isShowStationName ? 'block' : 'none'
            });
            obj.find('.siteIcon').html(contentInfo.lab).css({
                'color': contentInfo.lab_color,
                'display': contentInfo.isShowStation ? 'inline-block' : 'none'
            });

        },
        site_line: function(map, site_list) {
            var self = this;
            var contentInfo = self.getSiteInfo();
            var map_i = 0;
            for (var i = 0; i < site_list.length; i++) {
                var site_i = site_list[i];
                self.model_station.query().filter([
                    ["id", "=", parseInt(site_i.station_id)]
                ]).all().then(function(site_l) {
                    var site = site_l[0];
                    if (map_i == 0) {
                        map.setZoom(15);
                        map.setCenter([site.longitude, site.latitude]);
                    }
                    map_i++;
                    var cont_W = site.name.length * 14 - 12;
                    var content_info =
                        '<div class="cont">' +
                        '<p class="siteName" style="position: absolute; z-index: 1; top:-18px; left: -' + cont_W / 2 + 'px; font-family:' + contentInfo.family + ';color:' + contentInfo.color + ';">' +
                        site.name +
                        '</p>' +
                        '<p class="siteIcon" style="position: absolute; z-index:1; top: 0; left: 0; color: ' + contentInfo.lab_color + '">' +
                        contentInfo.lab +
                        '</p>' +
                        '</div>';

                    var marker = new AMap.Marker({
                        content: content_info,
                        position: [site.longitude, site.latitude],
                        offset : new AMap.Pixel(0,-15),
                        map: map,
                    });
                });
            }
        },
        // 获取map线属性
        getMapLineInfo: function() {
            var contentInfo = {
                color: this.$('.mapLineColor').val() || '#000',
                lineW: this.$('.mapLineWidth').val() || '2'
            };
            return contentInfo;
        },
        // 获取站点属性
        getSiteInfo: function() {
            var contentInfo = {
                family: this.$('.mapStationFontFamily').val() || '宋体',
                color: this.$('.mapStationFontColor').val() || '#000',
                lab: this.$('.mapStationIcon').val() || "●",
                lab_color: this.$(".mapStationColor").val(),
                isShowStationName: this.$('.isShowStationName:checked').length,
                isShowStation: this.$('.isShowStation:checked').length,
            };
            return contentInfo;
        }
    });

});