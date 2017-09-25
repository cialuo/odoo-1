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

    //  地图头部
    var map_work_title = Widget.extend({
        template: "map_work_title_template",
        init: function(parent, setInfo){
            this._super(parent);
            this.setInfo = setInfo;
        },
        start: function(){
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
            lineObj.on("change", function(){
                vehiclesObj.empty().append('<option value="">--请选择--</option>');
                if (this.value != ""){
                    var id = parseInt($(this).find("option:selected").attr("t_id"));
                    fleet_vehicle.query().filter([
                        ["route_id", "=", id]
                    ]).all().then(function(vehicles) {
                        _.each(vehicles, function(set){
                            var option = '<option value="' + set.on_boardid + '">'+set.on_boardid+'</option>';
                            vehiclesObj.append(option);
                        });
                    })
                }
            });

            self.$(".localize_bt").click(function(){
                var options = {
                    gprsId: lineObj.val(),
                    onboardId: vehiclesObj.val(),
                }
                var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
                $.ajax({
                    url: RESTFUL_URL+'/ltyop/dspGprsData/dspGpsCoordLastPos?apikey=71029270&params={"gprsId":"'+options.gprsId+'","onboardId":"'+options.onboardId+'"}',
                    type: 'get',
                    dataType: 'json',
                    success: function(ret) {
                        layer.close(layer_index);
                        if (ret.respose){
                            layer.msg(ret.respose.text, { time: 2000, shade: 0.3 });
                        }
                        console.log(ret);
                    }
                })
                
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
            config_parameter.query().filter([["key", "=", "dispatch.desktop.socket"]]).all().then(function (socket) {
                config_parameter.query().filter([["key", "=", "dispatch.desktop.restful"]]).all().then(function (restful) {
                    SOCKET_URL = socket[0].value;
                    RESTFUL_URL = restful[0].value;
                    self.get_line_info();
                });
            });
        },
        get_line_info: function(){
            var self = this;
            model_choseline.query().filter([
                ["state", "=", 'inuse']
            ]).all().then(function(lines) {
                var options = {title: '电子地图',type: 'electronic_map', lines};
                new map_work_title(self, options).appendTo(self.$('.map_work_title'));
                //初始化地图
                self.init_map_fn();
            });
        },
        init_map_fn: function(){
            var map = new AMap.Map(this.$(".map_work_content")[0], {
                resizeEnable: true,
                zoom: 10,
                center: [116.408075, 39.950187]
            });
            this.map_toolBar(map);
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

    core.action_registry.add('lty_operation_map_base.electronic_map', electronic_map);



    // 轨迹回放
    var track_playback_map = Widget.extend({
        template: "track_playback_map_template",
        init: function(parent) {
            this._super(parent);
        },
        start: function() {
            var self = this;
            config_parameter.query().filter([["key", "=", "dispatch.desktop.socket"]]).all().then(function (socket) {
                config_parameter.query().filter([["key", "=", "dispatch.desktop.restful"]]).all().then(function (restful) {
                    SOCKET_URL = socket[0].value;
                    RESTFUL_URL = restful[0].value;
                    self.get_line_info();
                });
            });
        },
        get_line_info: function(){
            var self = this;
            model_choseline.query().filter([
                ["state", "=", 'inuse']
            ]).all().then(function(lines) {
                var options = {title: '轨迹回放',type: 'track_playback_map', lines:lines};
                new map_work_title(self, options).appendTo(self.$('.map_work_title'));
                //初始化地图
                self.init_map_fn();
            });
        },
        init_map_fn: function(){
            var map = new AMap.Map(this.$(".map_work_content")[0], {
                resizeEnable: true,
                zoom: 10,
                center: [116.408075, 39.950187]
            });
            this.map_toolBar(map);
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

    core.action_registry.add('lty_operation_map_base.track_playback_map', track_playback_map);
});