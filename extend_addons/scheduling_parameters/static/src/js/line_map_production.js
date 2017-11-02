odoo.define("", function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var Model = require('web.Model');

    // 加载高德地图组件
    $.getScript("http://webapi.amap.com/maps?v=1.3&key=cf2cefc7d7632953aa19dbf15c194019");

    var line_map_production = Widget.extend({
        template: "line_map_production_template",
        init: function(parent){
            this._super(parent);
        },
        start: function(){
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
            model_choseline = new Model('route_manage.route_manage');
            model_choseline.query().filter([["state", "=", 'inuse']]).all().then(function (data){
                new line_map_production_line_set(self, data, location_set).appendTo(self.$(".mapPage"));
            });
        },
        map_toolBar: function(map){
            map.plugin(["AMap.ToolBar"], function() {
                map.addControl(new AMap.ToolBar({locate: false}));
            });
            if(location.href.indexOf('&guide=1')!==-1){
                map.setStatus({scrollWheel:false})
            }
        }
    });

    core.action_registry.add('scheduling_parameters.line_map_production', line_map_production);

    var line_map_production_line_set = Widget.extend({
        template: 'line_map_production_line_set_template',
        events: {         
        },
        init: function(parent, lineData, location_set){
            this._super(parent);
            this.line_data = lineData;
            this.location_set = location_set;
            // 上行站点
            this.model_site_top = new Model('opertation_resources_station_up');
            // 下行站点
            this.model_site_down = new Model('opertation_resources_station_down');
        },
        start: function(){
            var self = this;
            var map = self.location_set.map;
            // 选择线路
            self.$('.mapSetLineDiv').on('change', 'select.line', function(){
                var line_id = $(this).val();
                self.$('.mapSet').html('');
                if (line_id==''){
                    return;
                }
                self.line_id = line_id;
                self.model_site_top.query().filter([["route_id", "=", parseInt(self.line_id)]]).all().then(function (site_top_list) {
                    var site_top_list = site_top_list;
                    self.model_site_down.query().filter([["route_id", "=", parseInt(self.line_id)]]).all().then(function (site_down_list) {
                        new line_map_production_set(self, map, site_top_list, site_down_list).appendTo(self.$('.mapSet'));
                    })
                });
            });
            self.map_binding_fn(map);
        },
        map_binding_fn:function(map){
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
        init: function(parent, map, site_top_list, site_down_list){
            this._super(parent);
            this.map = map;
            this.site_top_list = site_top_list;
            this.site_down_list = site_down_list;
            // 站点信息
            this.model_station = new Model('opertation_resources_station');
        },
        start: function(){
            var self = this;
            // 初始化站点信息
            self.site_line(self.site_top_list); 


            //修改站点属性触发事件
            self.$('.stationAttribute').on('change', '.siteType', function(){
                self.set_site_type();
            });
        },
        set_site_type: function(){

            var contentInfo = this.getContInfo();

            console.log(contentInfo.isShowStationName+"_"+contentInfo.isShowStation);
            var obj = this.$el.parents('.mapPage');
            obj.find('.siteName').css({
                'font-family': contentInfo.family,
                'color': contentInfo.color,
                'display': contentInfo.isShowStationName?'block':'none'
            });
            obj.find('.siteIcon').html(contentInfo.lab).css({
                'color': contentInfo.lab_color,
                'display': contentInfo.isShowStation?'inline-block':'none'
            });

        },
        site_line: function(site_list){
            var self = this;
            var contentInfo = self.getContInfo();
            var map = self.map;
            var map_i = 0;
            for (var i = 0; i < site_list.length; i++) {
                var site_i = site_list[i];
                self.model_station.query().filter([["id", "=", parseInt(site_i.station_id)]]).all().then(function (site_l) {
                    var site = site_l[0];
                    if (map_i==0){
                        map.setZoom(15);
                        map.setCenter([site.longitude, site.latitude]);
                    }
                    map_i ++;
                    var cont_W = site.name.length*14-10;
                    var content_info = 
                        '<div class="cont">' +
                            '<p class="siteName" style="position: absolute; z-index: 1; top:-18px; left: -' + cont_W/2 + 'px; font-family:' + contentInfo.family + ';color:'+contentInfo.color+';">' +
                                site.name +
                            '</p>' +
                            '<p class="siteIcon" style="position: absolute; z-index:1; top: 0; left: 0; color: '+ contentInfo.lab_color +'">' + 
                                contentInfo.lab +
                            '</p>' +
                        '</div>';

                    var marker = new AMap.Marker({
                        // content: '<div class="cont"><p class="siteName" style="font-family:'+contentInfo.family+';color:'+contentInfo.color+';">'+site.name+'</p><p class="siteIcon"><span style="color:'+contentInfo.lab_color+'">'+contentInfo.lab+'</span></p></div>',
                        content: content_info,
                        position: [site.longitude, site.latitude],
                        map: map,
                    });
                });
            }
        },
        // 获取站点属性
        getContInfo: function(){
            var contentInfo = {
                family:  this.$('.mapStationFontFamily').val() || '宋体',
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

