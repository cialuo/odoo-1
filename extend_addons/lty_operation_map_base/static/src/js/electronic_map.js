odoo.define("", function(require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;

    //  地图头部
    var map_work_title = Widget.extend({
        template: "map_work_title_template",
        init: function(parent, setInfo){
            this._super(parent);
            this.setInfo = setInfo;
        },
        start: function(){
            // 加载日期组件
            this.$(".timeW").datetimepicker({
                format: 'YYYY-MM-DD HH:mm',
                language: 'en',
                pickDate: true,
                pickTime: true,
                stepHour: 1,
                stepMinute: 1,
                inputMask: true
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
            var options = {title: '电子地图',type: 'electronic_map'};
            new map_work_title(this, options).appendTo(this.$('.map_work_title'));
            //初始化地图
            this.init_map_fn();
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
            var options = {title: '轨迹回放',type: 'track_playback_map'};
            new map_work_title(this, options).appendTo(this.$('.map_work_title'));
            //初始化地图
            this.init_map_fn();
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