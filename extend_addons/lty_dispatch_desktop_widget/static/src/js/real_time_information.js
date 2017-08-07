odoo.define("lty_dispatch_desktop_widget.bus_real_info", function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var communication = require('lty_dispatch_desktop_widget.communication');

    var bus_real_info = Widget.extend({
        template: 'bus_real_info_template',
        events: {
            'click .operationNav .back_to_the_field': 'back_to_the_field_fn',
            'click .operationNav .handle_exceptions': 'handle_exceptions_fn',
            'click .operationNav .schedule_a_return': 'schedule_a_return_fn',
            'click .operationNav .can_line': 'can_line_fn',
            'click .operationNav .sign': 'sign_fn',
            'click .operationNav .news, .InformationInteraction': 'news_fn',
            'click .geographicalPosition' : 'geographicalPosition_fn',
            'click .moreInfo' : 'moreInfo_fn',
            'click .operationNav .notice': 'notice_fn',
            'click .operationNav .conversation': 'conversation_fn',
            'click .arrivalTime': 'arrivalTimeFn',
            'click .video': 'videoFn',
            'click .police': 'policeFn',
            'click .close_bt': 'closeFn'
        },
        init: function(parent, data){
            this._super(parent);
            var init_data = {
                license_number: data.car_num,
                license_plate: '粤K·92823',
                driver: '李素华', 
                crew: '张雯',
                passenger: '62',
                full_load_rate: '90%',
                satisfaction_degree: '20%',
                carriage_temperature: '23',
                outdoor_temperature: '32',
                satisfaction_degree_2: '95%',
                back_door: '关闭',
                front_door: '开启',
                speed: '36km/h',
                sail: '大亚湾',
                front: '4km',
                after: '3km',
                back_field_time: '12:43',
                next_train_departure: '12:30',
                residual_clearance: '239KM',
                line: '16',
                trip: '4',
                total_trip: '10'
            };
            this.location_data = data;
            this.data = init_data;
        },
        start: function(){
            this.arrivalTimeFn();
        },
        handle_exceptions_fn: function(){
            alert('这里将发起处理异常状态请求');
        },
        schedule_a_return_fn: function(){
            alert('这里将发起安排回场任务请求');
        },
        can_line_fn: function(){
            alert('这里将发起CAN总线请求');
        },
        back_to_the_field_fn: function(){
            alert('这里将发起回场请求');
        },
        start_fn: function(){
            alert('这里将发起发车请求');
        },
        sign_fn: function(){
            alert('这里将发起签到请求');
        },
        news_fn: function(){
            var dialog = new communication(this);
            dialog.appendTo($("body"));
        },
        notice_fn: function(){
            alert('这里将发起通知请求');
        },
        conversation_fn: function(){
            alert('这里将发起通话请求');
        },
        geographicalPosition_fn: function(){
            var init_data = {
                longitude: '114.39973',
                latitude: '30.45787'
            };
            this.$(".carReport").html("");
            new arrival_time_map(this, init_data).appendTo(this.$(".carReport"));
        },
        moreInfo_fn: function(){
            this.$(".carReport").html("");
            new arrival_time_more_info(this).appendTo(this.$(".carReport"));
        },
        arrivalTimeFn: function(e){
            this.$(".carReport").html("");
            var init_data = {
                site_list: ['深大(8:30)','白石洲(8:37)','世界之窗(8:45)','华侨城(8:51)','车公庙(8:55)','葫芦谷(9:05)','断肠崖(9:15)', '长坂坡(9:30)'],
                data: [
                    {
                        name: '实际',
                        value: [1, 1, -2, -5, 0, -3]
                    },
                    {
                        name: '预测',
                        value: [1, 1, 5, 3, 2, 3]
                    }
                ]
            };
            new bus_real_info_arrival_time_chart(this, init_data).appendTo(this.$(".carReport"));
        },
        videoFn: function(e){
            this.$(".carReport").html("");
            new arrival_time_video(this).appendTo(this.$(".carReport"));
        },
        policeFn: function(e){
            this.$(".carReport").html("");
            new arrival_time_police(this).appendTo(this.$(".carReport"));
        },
        closeFn: function(){
            this.destroy();
        }
    });
    core.action_registry.add('lty_dispatch_desktop_widget.bus_real_info', bus_real_info);

    var bus_real_info_arrival_time_chart = Widget.extend({
        template: "arrival_time_chart_template",
        init: function(parent, data){
            this._super(parent);
            this.chart_data = data;
        },
        start: function(){
            this.carFGXFn();
        },
        carFGXFn: function(){
            var chart_data = this.chart_data;
            var option = {
                tooltip: {
                    trigger: 'axis',
                },
                color: ['blue', 'yellow', '#d29090'],
                legend: {
                    data:['计划', chart_data.data[0].name, chart_data.data[1].name]
                },
                grid: {
                    left: '2%',
                    right: '15%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis:  {
                    type: 'category',
                    boundaryGap: false,
                    name: '准点',
                    data: chart_data.site_list,
                    axisLabel:{
                        // interval: 0,
                        // formatter:function(val){
                        //     return val.split("").join("\n");
                        // }
                    },
                },
                yAxis: {
                    type: 'value',
                    min: -15,
                    max: 15,
                    name: '提前(分钟)',
                    axisLabel: {
                        formatter: '{value}'
                    }
                },
                series: [
                    {
                        name: chart_data.data[0].name,
                        type:'line',
                        symbolSize:1,
                        data: chart_data.data[0].value,
                        lineStyle: {
                            normal:{
                                width: 1
                            }
                        },
                    },
                    {
                        name: chart_data.data[1].name,
                        type:'line',
                        symbolSize:1,
                        data: chart_data.data[1].value,
                        lineStyle: {
                            normal:{
                                width: 1
                            }
                        },
                    },
                    {
                        name:'计划',
                        type:'line',
                        symbolSize:1,
                        data:[0, 0, 0, 0, 0, 0],
                        lineStyle: {
                            normal:{
                                width: 1
                            }
                        },
                        markLine: {
                            data: [
                                {type: 'average', name: '平均值'},
                            ]
                        }
                    }
                ]
            };
            var myChart = echarts.init(this.$el.find('.carzxt')[0]);
            myChart.setOption(option);
        }
    });

    var arrival_time_police = Widget.extend({
        template: "arrival_time_police_template",
        init: function(parent){
            this._super(parent);
        },
        events: {
            'click .onBt' : 'send_police_fn'
        },
        send_police_fn: function(){
            alert("这里将发起报警请求");
        }
    });

    var arrival_time_video = Widget.extend({
        template: "arrival_time_video_template",
        init: function(parent){
            this._super(parent);
        },
    });

    var arrival_time_map = Widget.extend({
        template: "arrival_time_map_template",
        init: function(parent, data){
            this._super(parent);
            this.data = data;
        },
        start: function(){
            var self = this;
            var mapObj = new AMap.Map(self.$('.carInfoScene')[0], {zoom: 16, center: [self.data.longitude, self.data.latitude]});
            var marker = new AMap.Marker({
                map: mapObj,
                position: [self.data.longitude, self.data.latitude]
            });
            this.sokit(marker);
        },
        sokit: function(marker){
            var pos_list = [
                {longitude: 114.398595, latitude: 30.457569},
                {longitude: 114.39948, latitude: 30.457231},
                {longitude: 114.400939, latitude: 30.45688},
                {longitude: 114.402237, latitude: 30.45639},
                {longitude: 114.402977, latitude: 30.457102},
                {longitude: 114.403675, latitude: 30.457823}
            ];
            var i = 0;
            var self = this;
            function test_fn(){
                if (i>5){
                    return;
                }
                var pos = pos_list[i];
                marker.setPosition(new AMap.LngLat(pos.longitude, pos.latitude));
                i++;
                setTimeout(test_fn, 2000);    
            }
            test_fn();
        }
    });

    var arrival_time_more_info = Widget.extend({
        template: "arrival_time_more_info_template",
        init: function(parent){
            this._super(parent);
        },
    });
    // core.action_registry.add('lty_dispatch_desktop_widget.arrival_time_more_info', arrival_time_more_info);

    return bus_real_info;
});

