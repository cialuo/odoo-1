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
                license_plate: '',
                driver: '', 
                crew: '',
                passenger: '',
                full_load_rate: '',
                satisfaction_degree: '',
                carriage_temperature: '',
                outdoor_temperature: '',
                satisfaction_degree_2: '',
                back_door: '',
                front_door: '',
                speed: '',
                sail: '',
                front: '',
                after: '',
                back_field_time: '',
                next_train_departure: '',
                residual_clearance: '',
                line: data.line_id+'路',
                trip: '',
                total_trip: ''
            };
            this.location_data = data;
            this.data = init_data;
        },
        start: function(){
            // var layer_index = layer.msg("加载中...", {time: 0, shade: 0.3});
            // var busRealStateModel_set = {
            //     layer_index: layer_index
            // }
            // sessionStorage.setItem("busRealStateModel_set", JSON.stringify(busRealStateModel_set));

            this.arrivalTimeFn();

            // 订阅车辆实时状态
            var package = {
                type: 2000,
                controlId: this.location_data.controllerId,
                open_modules: ["bus_real_state"]
            };
            websocket.send(JSON.stringify(package));
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
            // if (this.$(".arrival_time_map").length > 0){
            //     return false;
            // }
            var init_data = {
                longitude: '114.39973',
                latitude: '30.45787'
            };
            this.$(".carReport").html("<div class='socket_load'>加载中...</div>");
            new arrival_time_map(this, init_data).appendTo(this.$(".carReport"));
        },
        moreInfo_fn: function(){
            this.$(".carReport").html("");
            new arrival_time_more_info(this).appendTo(this.$(".carReport"));
        },
        arrivalTimeFn: function(e){
            if (this.$(".arrival_time_chart").length > 0){
                return false;
            }
            var init_data = {
                site_list: ['深大(8:30)','白石洲(8:37)','世界之窗(8:45)','华侨城(8:51)','车公庙(8:55)','葫芦谷(9:05)','断肠崖(9:15)', '长坂坡(9:30)'],
                data: [
                    {
                        name: '预测',
                        value: [1, 1, 5, 3, 2, 3]
                    },
                    {
                        name: '实际',
                        value: [1, 1, -2, -5, 0, -3]
                    }
                ]
            };
            var busRealStateModel_set = JSON.parse(sessionStorage.getItem("busRealStateModel_set"));
            layer.close(busRealStateModel_set.layer_index);
            this.$el.removeClass('hide_model');
            this.$(".carReport").html("<div class='socket_load'>加载中...</div>");
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
        socket_fn: function(data, arg){
            var self = arg.self;
            var vehicleInformationObj = self.$(".popupContent .vehicleInformation");
            var carReportObj = self.$(".popupContent .carReport");
            var lineInfo = self.$(".lineInfo");
            var back_door_status = data.slice(83, 84)>8?"<e class='danger'>开启</e>":"关闭"
            var front_door_status = data.slice(84, 85)<8?"<e class='danger'>开启</e>":"关闭"
            var new_date = new Date();
            var date_time = new_date.getHours()+":"+new_date.getMinutes();
            var new_data_2 = new Date(new_date.getTime() + 1000*60*30);
            var date_time_2 = new_data_2.getHours()+":"+new_data_2.getMinutes();
            vehicleInformationObj.find(".passenger_number").html(self.data.passenger+data.slice(78, 79));
            vehicleInformationObj.find(".satisfaction_rate").html(data.slice(78, 80)+"%");
            vehicleInformationObj.find(".inside_temperature").html(data.slice(80, 82));
            vehicleInformationObj.find(".outside_temperature").html(data.slice(82, 84));
            vehicleInformationObj.find(".back_door_status").html(back_door_status);
            vehicleInformationObj.find(".front_door_status").html(front_door_status);
            vehicleInformationObj.find(".current_speed").html(data.slice(84, 86));
            vehicleInformationObj.find(".direction").html(self.data.sail);
            vehicleInformationObj.find(".front_distance").html(data.slice(86, 87));
            vehicleInformationObj.find(".back_distance").html(data.slice(87, 88));
            vehicleInformationObj.find(".return_time").html(date_time);
            vehicleInformationObj.find(".next_trip_time").html(date_time_2);
            vehicleInformationObj.find(".residual_clearance").html(data.slice(76, 78)+'KM/h');
            lineInfo.find(".lineRoad").html('18')
            lineInfo.find(".trip").html(data.slice(76, 77));
            lineInfo.find(".total_trip").html(data.slice(76, 77)+data.slice(77, 78));
            
            self.$el.show();
            if (arg.layer_index){
                layer.close(arg.layer_index);
            }
        },
        closeFn: function(){
            // 取消订阅车辆实时状态
            var package = {
                type: 2001,
                controlId: this.location_data.controllerId,
                open_modules: ["bus_real_state"]
            };
            websocket.send(JSON.stringify(package));
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
                color: ['#4f8ed9', '#e1bc73', '#c98888'],
                legend: {
                    icon: 'stack',
                    textStyle: {
                        color: "#fff"
                    },
                    data:['计划', chart_data.data[0].name, chart_data.data[1].name]
                },
                animation: false,
                grid: {
                    left: '3%',
                    right: '0',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis:  {
                    type: 'category',
                    boundaryGap: false,
                    data: chart_data.site_list,
                    axisLabel:{
                        textStyle: {
                            color: "#fff"
                        }
                        // interval: 0,
                        // formatter:function(val){
                        //     return val.split("").join("\n");
                        // }
                    },
                    splitLine: {
                        show: true,
                        lineStyle: {
                            color: ['#454c6c']
                        }
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#454c6c',
                        }
                    },
                },
                yAxis: {
                    type: 'value',
                    min: -15,
                    max: 15,
                    name: '提前(分钟)',
                    nameTextStyle: {
                        color: "#fff"
                    },
                    axisLabel: {
                        formatter: '{value}',
                        textStyle: {
                            color: "#fff"
                        }
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#454c6c',
                        }
                    },
                    axisTick: {show:false},
                    splitLine: {
                        lineStyle: {
                            color: ['#454c6c']
                        }
                    }
                },
                series: [
                    {
                        name:'计划',
                        type:'line',
                        symbolSize:1,
                        data:[0, 0, 0, 0, 0, 0, 0, 0],
                        lineStyle: {
                            normal:{
                                width: 1
                            }
                        },
                        // markLine: {
                        //     data: [
                        //         {type: 'average', name: '平均值'},
                        //     ]
                        // }
                    },
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
                    }
                ]
            };
            // var myChart = echarts.init(this.$el[0]);
            // myChart.setOption(option);
            $(".carReport .socket_load").remove();
            this.$el.removeClass('hide_model');
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
            // var mapObj = new AMap.Map(self.$el[0], {zoom: 14, center: [self.data.longitude, self.data.latitude]});
            // var marker = new AMap.Marker({
            //     map: mapObj,
            //     position: [self.data.longitude, self.data.latitude]
            // });
            self.$el.removeClass('hide_model');
            $(".carReport .socket_load").remove();
            // self.sokit(marker);
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
        start: function(){
            this.$el.mCustomScrollbar({
                theme: 'minimal'
            });
        }
    });
    // core.action_registry.add('lty_dispatch_desktop_widget.arrival_time_more_info', arrival_time_more_info);

    return bus_real_info;
});

