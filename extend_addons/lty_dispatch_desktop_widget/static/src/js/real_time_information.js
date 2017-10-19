odoo.define("lty_dispatch_desktop_widget.bus_real_info", function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var communication = require('lty_dispatch_desktop_widget.communication');
    var plan_exports = require('lty_dispatch_desktop_widget.plan_display');

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
            var options = {
                x: "",
                y: "",
                zIndex: 2,
                line_id: "",
                line_name: "",
                car_num: "",
                car_id: "",
                onBoardId: "",
                controllerId: "",
                fix_style: ""
            };
            $.extend(options, data);
            this.location_data = options;
            this.data = init_data;
        },
        start: function(){
            var self = this;
            // var layer_index = layer.msg("加载中...", {time: 0, shade: 0.3});
            // var busRealStateModel_set = {
            //     layer_index: layer_index
            // }
            // sessionStorage.setItem("busRealStateModel_set", JSON.stringify(busRealStateModel_set));


            // 搜索-司机工号
            // 应用功能: 添加计划、调整计划、批量更改车辆或司机、司乘签到
            $("body").on("focus", ".customModal .workerIdSearch, .customModal .driverNameSearch", function() {
                self.driver_search_autocomplete({ evt: this, controlId: CONTROLLERID });
            });

            // 搜索-乘务工号
            // 应用: 添加计划、调整计划、司乘签到
            $("body").on("focus", ".customModal .trainSearch, .customModal .trainNameSearch", function() {
                self.trainman_search_autocomplete({ evt: this, controlId: CONTROLLERID });
            });


            self.arrivalTimeFn();

            // 订阅车辆实时状态
            // var package = {
            //     type: 2000,
            //     controlId: CONTROLLERID,
            //     open_modules: ["bus_real_state"]
            // };
            // if (websocket){
            //     websocket.send(JSON.stringify(package));
            // }
        },
        // 处理异常状态
        handle_exceptions_fn: function(){
            var self = this;
            var carInfo = self.location_data;
            var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
            var busInfoId_str = 'id:' + carInfo.car_id;
            if (carInfo.onBoardId){
                busInfoId_str = 'onBoardId:' + carInfo.onBoardId;
            }
            if (carInfo.controllerId){
                busInfoId_str = busInfoId_str + "," + carInfo.controllerId;
            }
            $.ajax({
                url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename:"op_busresource",lineId:' + carInfo.line_id + ','+busInfoId_str+'}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(layer_index);
                    var op = ret.respose[0];
                    console.log(op);
                    var dialog = new plan_exports.error_state_w(self, op);
                    dialog.appendTo($('body'));
                }
            });
        },
        // 安排回场任务
        schedule_a_return_fn: function(){
            var self = this;
            var carInfo = self.location_data;
            var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
            var busInfoId_str = 'id:' + carInfo.car_id;
            if (carInfo.onBoardId){
                busInfoId_str = 'onBoardId:' + carInfo.onBoardId;
            }
            if (carInfo.controllerId){
                busInfoId_str = busInfoId_str + "," + carInfo.controllerId;
            }
            $.ajax({
                url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename:"op_busresource",lineId:' + carInfo.line_id + ','+busInfoId_str+'}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(layer_index);
                    var op = ret.respose[0];
                    console.log(op);
                    var dialog = new plan_exports.in_the_task_w(self, op);
                    dialog.appendTo($('body'));
                }
            });
        },
        can_line_fn: function(){
            alert('这里将发起CAN总线请求');
        },
        // 手动回场
        back_to_the_field_fn: function(){
            var self = this;
            var carInfo = self.location_data;
            var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
            var busInfoId_str = 'id:' + carInfo.car_id;
            if (carInfo.onBoardId){
                busInfoId_str = 'onBoardId:' + carInfo.onBoardId;
            }
            if (carInfo.controllerId){
                busInfoId_str = busInfoId_str + "," + carInfo.controllerId;
            }
            $.ajax({
                url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename:"op_busresource",lineId:' + carInfo.line_id + ','+busInfoId_str+'}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(layer_index);
                    var op = ret.respose[0];
                    console.log(op);
                    var dialog = new plan_exports.manual_return_w(self, op);
                    dialog.appendTo($('body'));
                }
            });
        },
        // 手动签点
        sign_fn: function(){
            var self = this;
            var carInfo = self.location_data;
            var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
            var busInfoId_str = 'id:' + carInfo.car_id;
            if (carInfo.onBoardId){
                busInfoId_str = 'onBoardId:' + carInfo.onBoardId;
            }
            if (carInfo.controllerId){
                busInfoId_str = busInfoId_str + "," + carInfo.controllerId;
            }
            $.ajax({
                url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename:"op_busresource",lineId:' + carInfo.line_id + ','+busInfoId_str+'}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(layer_index);
                    var op = ret.respose[0];
                    console.log(op);
                    var dialog = new plan_exports.driver_check_in_w(self, op);
                    dialog.appendTo($('body'));
                }
            });
        },
        // 消息
        news_fn: function(){
            var self = this;
            var carInfo = self.location_data;
            var layer_index = layer.msg("请求中，请稍后...", { shade: 0.3, time: 0 });
            var busInfoId_str = 'id:' + carInfo.car_id;
            if (carInfo.onBoardId){
                busInfoId_str = 'onBoardId:' + carInfo.onBoardId;
            }
            if (carInfo.controllerId){
                busInfoId_str = busInfoId_str + "," + carInfo.controllerId;
            }
            $.ajax({
                url: RESTFUL_URL + '/ltyop/planData/query?apikey=71029270&params={tablename: "op_busresource",lineId:' + carInfo.line_id + ','+busInfoId_str+'}',
                type: 'get',
                dataType: 'json',
                data: {},
                success: function(ret) {
                    layer.close(layer_index);
                    var retData = ret.respose[0];
                    if (!retData.selfId) {
                        retData.selfId = retData.carNum;
                    }
                    console.log(retData);
                    new plan_exports.send_short_msg_msg(self, retData).appendTo($('body'));
                }
            });
            // var dialog = new communication(this);
            // dialog.appendTo($("body"));
        },
        conversation_fn: function(){
            var layer_index = layer.msg("后续将会开放该功能，敬请关注。", { shade: 0.3, time: 2000 });
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
            // if (this.$(".arrival_time_chart").length > 0){
            //     return false;
            // }
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
            // var busRealStateModel_set = JSON.parse(sessionStorage.getItem("busRealStateModel_set"));
            // layer.close(busRealStateModel_set.layer_index);
            this.$el.removeClass('hide_model');
            this.$(".carReport").html("<div class='socket_load'>加载中...</div>");
            new bus_real_info_arrival_time_chart(this, init_data).appendTo(this.$(".carReport"));
        },
        videoFn: function(e){
            var layer_index = layer.msg("后续将会开放该功能，敬请关注。", { shade: 0.3, time: 2000 });
            // this.$(".carReport").html("");
            // new arrival_time_video(this).appendTo(this.$(".carReport"));
        },
        policeFn: function(e){
            var layer_index = layer.msg("后续将会开放该功能，敬请关注。", { shade: 0.3, time: 2000 });
            // this.$(".carReport").html("");
            // new arrival_time_police(this).appendTo(this.$(".carReport"));
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
        driver_search_autocomplete: function(data) {
            var workDate = $(".customModal .modal-body").attr("workDate");
            var gprsid = $(".customModal .modal-body").attr("gprsid");
            var options = {
                event: data.evt,
                dateSearch: workDate,
                controlId: data.controlId,
                gprsid: gprsid
            };
            console.log(options);
            $(options.event).autocomplete({
                minLength: 0,
                width: options.event.offsetWidth,
                resultsClass: 'autocomplete_custom_model_class',
                autoFocus: true,
                source: function(request, response) {
                    var workerId = $(options.event).val();
                    if (workerId == "") {
                        return response([]);
                    }
                    $.ajax({
                        url: RESTFUL_URL + '/ltyop/dspSimulationDisPatchPlan/autocompleteAttendanceByGprsid?apikey=71029270&params={dateSearch: "' + options.dateSearch + '" ,controlId: "' + options.controlId + '" ,gprsid: "' + options.gprsid + '" ,workerId: "' + workerId + '"}',
                        dataType: "json",
                        success: function(data) {
                            if (data.length > 0){
                                response(data);
                            }else{
                                response([]);
                            }
                        }
                    });
                },
                focus: function(event, ui) {
                    return false;
                },
                select: function(event, ui) {
                    // $(options.event).val(ui.item.workerId);
                    $(".customModal .workerIdSearch").val(ui.item.workerId);
                    $(".customModal .driverNameSearch").val(ui.item.driverName);
                    return false;
                },
            }).focus(function() {
                $(this).autocomplete("search");
            }).autocomplete("instance")._renderItem = function(ul, item) {
                return $("<li>")
                    .append("<div>" + item.workerId + "<span style='float:right;padding-right:5px;'>" + item.driverName + "</span></div>")
                    .appendTo(ul);
            }
        },
        trainman_search_autocomplete: function(data) {
            var workDate = $(".customModal .modal-body").attr("workDate");
            var gprsid = $(".customModal .modal-body").attr("gprsid");
            var options = {
                event: data.evt,
                dateSearch: workDate,
                controlId: data.controlId,
                gprsid: gprsid,
            };
            console.log(options);
            $(options.event).autocomplete({
                minLength: 0,
                width: options.event.offsetWidth,
                resultsClass: 'autocomplete_custom_model_class',
                autoFocus: true,
                source: function(request, response) {
                    var workerId = $(options.event).val();
                    if (workerId == "") {
                        return response([]);
                    }
                    $.ajax({
                        url: RESTFUL_URL + '/ltyop/dspSimulationDisPatchPlan/autocompleteTrainAttendanceByGprsid?apikey=71029270&params={dateSearch: "' + options.dateSearch + '" ,controlId: "' + options.controlId + '" ,gprsid: "' + options.gprsid + '" ,workerId: "' + workerId + '"}',
                        dataType: "json",
                        success: function(data) {
                            if (data.length > 0){
                                response(data);
                            }else{
                                response([]);
                            }
                        }
                    });
                },
                focus: function(event, ui) {
                    return false;
                },
                select: function(event, ui) {
                    // $(options.event).val(ui.item.workerId);
                    $(".customModal .trainSearch").val(ui.item.workerId);
                    $(".customModal .trainNameSearch").val(ui.item.driverName);
                    return false;
                }
            }).focus(function() {
                $(this).autocomplete("search");
            }).autocomplete("instance")._renderItem = function(ul, item) {
                return $("<li>")
                    .append("<div>" + item.workerId + "<span style='float:right;padding-right:5px;'>" + item.driverName + "</span></div>")
                    .appendTo(ul);
            };
        },
        closeFn: function(){
            // 取消订阅车辆实时状态
            // var package = {
            //     type: 2001,
            //     controlId: this.location_data.controllerId,
            //     open_modules: ["bus_real_state"]
            // };
            // if (websocket){
            //     websocket.send(JSON.stringify(package));
            // }
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

