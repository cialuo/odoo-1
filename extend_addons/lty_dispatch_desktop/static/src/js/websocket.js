/**
 * Created by Administrator on 2017/8/5.
 */




var websocket = null;

//判断当前浏览器是否支持WebSocket
if ('WebSocket' in window) {
    // websocket = new SockJS("http://127.0.0.1:8769/wstest?userId=45454");
    // websocket = new WebSocket("ws://202.104.136.228:8085/dispatch-websocket/websocket?userId=2222&token=55e1da6f0fe34f3a98a1faac5b939b68");
    websocket = new WebSocket("ws://10.1.254.9:8085/dispatch-websocket/websocket?userId=2222&token=55e1da6f0fe34f3a98a1faac5b939b68");
} else {
    alert('当前浏览器 Not support websocket');
}

//连接发生错误的回调方法
websocket.onerror = function () {
    console.log("WebSocket连接发生错误");
};
//连接成功建立的回调方法
websocket.onopen = function () {
    console.log("WebSocket连接成功");
}

// 定义模块调用
// 示例 {model: {fn: "", arg: ""}},
// 解释 model:打开的模块, fn:渲染执行函数, arg:所需参数
// var socket_model_info = {
// 	'异常':{},
// 	'消息':{},
// 	'线路':{},
// 	'客流运力':{},
// 	'modelBus':{}, //车辆实时状态
// 	'滞客信息':{},
// 	'线路行计划':{},
// 	'线路车场状态':{},
// 	'线路在途状态':{},
// 	'车辆资源状态':{},
// 	'人力资源状态':{}
// };
var socket_model_info = {};
var socket_model_api_obj = {}; // 记录创建的地图，echart图表
// var package = {
//     type: 1001,
//     open_modules: "dispatch-line_message-4",
//     msgId: Date.parse(new Date())
// };
// websocket.send(JSON.stringify(package));
websocket.onmessage = function (event) {
    // console.log(event)
    // for (socket_model in socket_model_info) {
    //     var socket_model_obj = socket_model_info[socket_model];
    //     socket_model_obj.fn(event.data, socket_model_obj.arg);
    // }
    // var obj = {modelName: "bus_real_state", controllerId: "1", data: [event.data]};
    // console.log('随机数为'+event.data.slice(78, 80));
    // if (event.data.slice(78, 80) < 15) {
    //     obj.modelName = "passenger_delay";
    // } else if (event.data.slice(78, 80) < 30) {
    //     // line_plan line_park line_online
    //     obj.modelName = "linePlanParkOnlineModel";
    // } else if (event.data.slice(78, 80) < 45) {
    //     obj.modelName = "passenger_flow_capacity";
    // } else if (event.data.slice(78, 80) < 60) {
    //     obj.modelName = "absnormal";
    // }
    // var modelName = obj.modelName;
    // if (!event.data){
    // 	return false;
    // }
    var eventObj = JSON.parse(event.data);
    console.log(eventObj.data);
    var modelName = eventObj.moduleName;
    var controllerId = eventObj.controllerId;
    for (socket_model in socket_model_info) {
        var socket_model_obj = socket_model_info[socket_model];
        socket_model_obj.fn(event.data, socket_model_obj.arg);
    }

    //由于车辆上下行计划，车场，在途数据来源于restful，这里只会收到update的推送，由于要做些简单处理，所以在这里直接触发展示
    linePlanParkOnlineModel_display($(".controller_" + controllerId));

    if (modelName == "线路") {
    } else if (modelName == "passenger_flow_capacity") {
        //客流与运力组件
        passenger_flow_capacity($(".controller_" + controllerId), eventObj.data);
    } else if (modelName == "车辆资源状态") {
        // console.log('3');
    } else if (modelName == "人力资源状态") {
        // console.log('4');
    } else if (modelName == "bus_real_state") {
        // console.log('5');
        busRealStateModel_socket_fn($(".controller_" + controllerId), eventObj.data);
    } else if (modelName == "passenger_delay") {
        // console.log('6');
        passengerDelayModel_socket_fn($(".controller_" + controllerId), eventObj.data);
    } else if ($.inArray(modelName, ["line_plan", "line_park", "line_online"])!=-1) {
        // console.log('7');
        update_linePlanParkOnlineModel_socket_fn($(".controller_" + controllerId), eventObj.data, modelName);
    } else if (modelName == "线路车场") {
        // console.log('8');
    } else if (modelName == "线路在途") {
        // console.log('9');
    } else if (modelName == "消息") {
        // console.log('10');
    } else if (modelName == "absnormal") {
        // console.log(event.data[0].substring(78, 80))
        absnormal_del($(".controller_" + controllerId), eventObj.data);
    }
};

//连接关闭的回调方法
websocket.onclose = function () {
    console.log("WebSocket连接关闭");
};
//监听窗口关闭事件，当窗口关闭时，主动去关闭websocket连接，防止连接还没断开就关闭窗口，server端会抛异常。
window.onbeforeunload = function () {
    websocket.close();
};
// 异常
function absnormal_del(controllerObj, data_list) {
    if (controllerObj.find('.updown_line_table[line_id=1]').length > 0) {
        if (data_list[0].substring(78, 79) > 3) {
            controllerObj.find('.updown_line_table[line_id=1]').find('.no_absnormal').show().siblings().hide();
            var timer_carousel = sessionStorage.getItem('timer1');
            clearInterval(timer_carousel);
            controllerObj.find('.updown_line_table[line_id=1]').find('.carousel_content').css({left: 0});
        }
    }
    if (controllerObj.find('.updown_line_table[line_id=2]').length > 0) {
        if (data_list[0].substring(78, 79) > 3) {
            controllerObj.find('.updown_line_table[line_id=2]').find('.no_absnormal').show().siblings().hide();
            var timer_carouse2 = sessionStorage.getItem('timer2');
            clearInterval(timer_carouse2);
            controllerObj.find('.updown_line_table[line_id=2]').find('.carousel_content').css({left: 0});
        }
    }
}
//客流运力
function passenger_flow_capacity(controllerObj, data_list) {
    if (controllerObj.find('.bus_src_config[line_id=1]').find('.src_line_number').length > 0) {
        controllerObj.find('.bus_src_config[line_id=1]').find('.src_line_number').html(data_list[0].substring(78, 80));

    }
    if (controllerObj.find('.bus_src_config[line_id=2]').find('.src_line_number').length > 0) {
        controllerObj.find('.bus_src_config[line_id=2]').find('.src_line_number').html(12334);
    }
}

// 车辆实时状态模块
function busRealStateModel_socket_fn(controllerObj, dataObj) {
    // var dom = controllerObj.find(".busRealStateModel_"+dataObj.line_on+"_"+dataObj.bus_on);
    var dom = controllerObj.find(".busRealStateModel_1_222");
    if (dom.length > 0) {
        var vehicleInformationObj = dom.find(".popupContent .vehicleInformation");
        var carReportObj = dom.find(".popupContent .carReport");
        var lineInfo = dom.find(".lineInfo");
        vehicleInformationObj.find(".passenger_number").html(dataObj.passenger_number);
        vehicleInformationObj.find(".satisfaction_rate").html(dataObj.satisfaction_rate);
        vehicleInformationObj.find(".inside_temperature").html(dataObj.inside_temperature);
        vehicleInformationObj.find(".outside_temperature").html(dataObj.outside_temperature);
        vehicleInformationObj.find(".back_door_status").html(dataObj.back_door_status);
        vehicleInformationObj.find(".front_door_status").html(dataObj.front_door_status);
        vehicleInformationObj.find(".current_speed").html(dataObj.current_speed + 'KM/H');
        vehicleInformationObj.find(".direction").html(dataObj.direction);
        vehicleInformationObj.find(".front_distance").html(dataObj.front_distance + 'KM');
        vehicleInformationObj.find(".back_distance").html(dataObj.back_distance + 'KM');
        vehicleInformationObj.find(".return_time").html(dataObj.return_time);
        vehicleInformationObj.find(".next_trip_time").html(dataObj.next_trip_time);
        vehicleInformationObj.find(".residual_clearance").html(dataObj.residual_clearance + 'KM');
        lineInfo.find(".lineRoad").html('18'+'路')
        lineInfo.find(".trip").html(dataObj.satisfaction_rate);
        lineInfo.find(".total_trip").html(dataObj.satisfaction_rate);

        var busRealStateModel_set = JSON.parse(sessionStorage.getItem("busRealStateModel_set"));
        layer.close(busRealStateModel_set.layer_index);
        dom.removeClass('hide_model');
        var socket_load = carReportObj.find(".socket_load");
        var mapDom = carReportObj.find(".arrival_time_map");
        var chartDom = carReportObj.find(".arrival_time_chart");
        if (mapDom.length>0){
        	socket_load.remove();
        	mapDom.removeClass("hide_model");
        	busRealStateModel_map(mapDom[0], dataObj);
        }
        if (chartDom.length > 0){
        	socket_load.remove();
        	chartDom.removeClass("hide_model");
        }
    }
}

// 车辆实时状态模块-地理位置
function busRealStateModel_map(dom, gps){
	if (socket_model_api_obj.busRealStateModel.marker){
		socket_model_api_obj.busRealStateModel.marker.setPosition(new AMap.LngLat(gps.location_log, gps.location_lan));
	}else{
		var mapObj = new AMap.Map(dom, {zoom: 14, center: [gps.location_log, gps.location_lan]});
		var marker = new AMap.Marker({
	        map: mapObj,
	        position: [gps.location_log, gps.location_lan]
	    });
	    socket_model_api_obj.busRealStateModel.marker = marker;
	}
}

// 站点实时状态模块
function passengerDelayModel_socket_fn(controllerObj, data_list){
	var dom = controllerObj.find(".passengerDelayModel");
	if (dom.length>0){
		var passengerDelayModel_set = JSON.parse(sessionStorage.getItem("passengerDelayModel_set"));
        layer.close(passengerDelayModel_set.layer_index);
        dom.removeClass('hide_model');
	}
}

// 线路计划，车场，在途模块 显示
function linePlanParkOnlineModel_display(controllerObj){
	var dom = controllerObj.find(".linePlanParkOnlineModel");
	if (dom.length > 0){
		var passengerDelayModel_set = JSON.parse(sessionStorage.getItem("linePlanParkOnlineModel_set"));
        layer.close(passengerDelayModel_set.layer_index);
        $('.linePlanParkOnlineModel .section_plan_cont').mCustomScrollbar({
            theme: 'minimal'
        });
        if ($('.linePlanParkOnlineModel .mCustomScrollbar').length>0){
            // 增加一个判断滑动js加载后展示
            dom.removeClass('hide_model');
        }
	}
}

// 线路计划，车场，在途模块 update
function update_linePlanParkOnlineModel_socket_fn(controllerObj, dataObj, modelName){
	var dom = controllerObj.find(".linePlanParkOnlineModel_1");
	if (dom.length>0){
		if (modelName == "line_plan"){
            var tr_obj_list = controllerObj.find(".bus_plan[direction="+dataObj.direction+"] .content_tb tr.point");
			var tr_obj = controllerObj.find(".bus_plan[direction="+dataObj.direction+"]").find(".content_tb tr[pid="+dataObj.id+"]");
			update_linePlan(tr_obj, dataObj, tr_obj_list);
		}else if (modelName == "line_park"){
            var tr_obj_list = controllerObj.find(".bus_yard[direction="+dataObj.direction+"] .content_tb tr.point");
            var tr_obj = controllerObj.find(".bus_yard[direction="+dataObj.direction+"]").find(".content_tb tr[pid="+dataObj.id+"]");
            update_linePark(tr_obj, dataObj, tr_obj_list);
		}else{
            var tr_obj_list = controllerObj.find(".bus_transit[direction="+dataObj.direction+"] .content_tb tr.point");
            var tr_obj = controllerObj.find(".bus_transit[direction="+dataObj.direction+"]").find(".content_tb tr[pid="+dataObj.id+"]");
            update_busTransit(tr_obj, dataObj, tr_obj_list);
		}
		
	}
}


// 计划更新
function update_linePlan(obj, dataObj, obj_list){
    if (obj.length == 0){
        // 没有则为新增,需按照计划发车时间先后插入
        var status_txt = "已完成";
        if (dataObj.planState!=2){
            status_txt = "待发"
        }
        var obj_str =
            '<tr class="point" pid="'+dataObj.id+'" direction="'+dataObj.direction+'" planRunTime="'+dataObj.planRunTime+'">' +
                '<td class="pL">' +
                    '<span st="'+dataObj.sendToScreen+'" class="icon sendToScreen icon_'+dataObj.sendToScreen+'"></span>' +
                    '<span st="'+dataObj.sendToBus+'" class="icon sendToBus icon_'+dataObj.sendToBus+'"></span>' +
                '</td>' +
                '<td class="planRunTime">' +
                    new Date(dataObj.planRunTime).toTimeString().slice(0,8) +
                '</td>' +
                '<td class="planReachTime">' +
                    new Date(dataObj.planReachTime).toTimeString().slice(0,8) +
                '</td>' +
                '<td class="selfId">' +
                    dataObj.selfId +
                '</td>' +
                '<td class="driverName">' +
                    dataObj.driverName +
                '</td>' +
                '<td class="pR planState">' +
                    status_txt +
                '</td>' +
            '</tr>';
        for (var i=0, L=obj_list.length; i<L; i++){
            var tr_obj  = obj_list[i];
            var planRunTime = tr_obj.getAttribute("planRunTime");
            if (planRunTime>dataObj.planRunTime){
                tr_obj.before(obj_str);
                break;
            }
        }
        return false;
    }

	// 发送计划到调度屏状态
	if (dataObj.sendToScreen != undefined){
		if (dataObj.sendToScreen == 1){
			obj.find(".sendToScreen").addClass('icon_1');
		}else{
			obj.find(".sendToScreen").removeClass('icon_1');
		}
	}

	// 发送计划到车辆状态
	if (dataObj.sendToBus != undefined){
		if (dataObj.sendToBus == 1){
			obj.find(".sendToBus").addClass('icon_1');
		}else{
			obj.find(".sendToBus").removeClass('icon_1');	
		}
	}

	// 计划到达时间
	if (dataObj.planRunTime != undefined){
		obj.find(".planRunTime").html(new Date(dataObj.planRunTime).toTimeString().slice(0,8));
	}

	// 计划到达时间
	if (dataObj.planReachTime != undefined){
		obj.find(".planReachTime").html(new Date(dataObj.planReachTime).toTimeString().slice(0,8));
	}

	// 车辆
	if (dataObj.selfId != undefined){
		obj.find(".selfId").html(dataObj.selfId);
	}

	// 司机
	if (dataObj.driverName != undefined){
		obj.find(".driverName").html(dataObj.driverName);
	}

	// 待发状态
	if (dataObj.planState != undefined){
		var txt = "待发";
		if (dataObj.planState == 2){
			txt = "已完成"
		}
		obj.find(".planState").html(txt);
	}
}

// 车场更新
function update_linePark(obj, dataObj, obj_list){
    if (obj.length == 0){
        // 没有则为新增,需按照计划发车时间先后插入
        var obj_str =
            '<tr class="point" pid="'+dataObj.id+'" direction="'+dataObj.direction+'" planRunTime="'+dataObj.planRunTime+'">' +
                '<td class="pL">' +
                    '<span st="'+dataObj.checkOut+'" class="icon sendToScreen icon_'+dataObj.checkOut+'"></span>' +
                    '<span st="'+dataObj.runState+'" class="icon sendToBus icon_'+dataObj.runState+'"></span>' +
                '</td>' +
                '<td class="planRunTime">' +
                    new Date(dataObj.planRunTime).toTimeString().slice(0,8) +
                '</td>' +
                '<td class="selfId">' +
                    dataObj.selfId +
                '</td>' +
                '<td class="lineName">' +
                    dataObj.lineName +
                '</td>' +
                '<td class="realReachTime">' +
                    new Date(dataObj.realReachTime).toTimeString().slice(0,8) +
                '</td>' +
                '<td class="pR stopTime">' +
                    dataObj.stopTime +
                '</td>' +
            '</tr>';
        for (var i=0, L=obj_list.length; i<L; i++){
            var tr_obj  = obj_list[i];
            var planRunTime = tr_obj.getAttribute("planRunTime");
            if (planRunTime>dataObj.planRunTime){
                tr_obj.before(obj_str);
                break;
            }
        }
        return false;
    }

    // 司机签到状态
    if (dataObj.checkOut != undefined){
        if (dataObj.checkOut == 1){
            obj.find(".checkOut").addClass('icon1_1');
        }else{
            obj.find(".checkOut").removeClass('icon1_1');    
        }
    }

    // 车辆在线状态
    if (dataObj.runState != undefined){
        if (dataObj.runState == 0){
            obj.find(".runState").addClass('icon2_1');
        }else{
            obj.find(".runState").removeClass('icon2_1');   
        }
    }

    // 计划到达时间
    if (dataObj.planRunTime != undefined){
        obj.find(".planRunTime").html(new Date(dataObj.planRunTime).toTimeString().slice(0,8));
    }


    // 车辆
    if (dataObj.carNum != undefined){
        obj.find(".carNum").html(dataObj.carNum);
    }

    // 线路
    if (dataObj.lineName != undefined){
        obj.find(".lineName").html(dataObj.lineName);
    }

    // 回场时间
    if (dataObj.realReachTime != undefined){
        obj.find(".realReachTime").html(new Date(dataObj.realReachTime).toTimeString().slice(0,8));
    }

    // 停车
    if (dataObj.stopTime != undefined){
        obj.find(".stopTime").html(new Date(dataObj.stopTime).toTimeString().slice(0,8));
    }
}


// 在途更新
function update_busTransit(obj, dataObj){
    if (obj.length == 0){
        // 没有则为新增,需按照计划发车时间先后插入
        var obj_str =
            '<tr class="point" pid="'+dataObj.id+'" direction="'+dataObj.direction+'" planRunTime="'+dataObj.planRunTime+'">' +
                '<td class="pL">' +
                    '<span st="'+dataObj.checkOut+'" class="icon sendToScreen icon_'+dataObj.checkOut+'"></span>' +
                    '<span st="'+dataObj.runState+'" class="icon sendToBus icon_'+dataObj.runState+'"></span>' +
                '</td>' +
                '<td class="planRunTime">' +
                    new Date(dataObj.planRunTime).toTimeString().slice(0,8) +
                '</td>' +
                '<td class="carNum">' +
                    dataObj.carNum +
                '</td>' +
                '<td class="lineName">' +
                    dataObj.lineName +
                '</td>' +
                '<td class="planReachTime">' +
                    new Date(dataObj.planReachTime).toTimeString().slice(0,8) +
                '</td>' +
                '<td class="pR stopTime">' +
                    dataObj.stopTime +
                '</td>' +
            '</tr>';
        for (var i=0, L=obj_list.length; i<L; i++){
            var tr_obj  = obj_list[i];
            var planRunTime = tr_obj.getAttribute("planRunTime");
            if (planRunTime>dataObj.planRunTime){
                tr_obj.before(obj_str);
                break;
            }
        }
        return false;
    }

    // 司机签到状态
    if (dataObj.checkOut != undefined){
        if (dataObj.checkOut == 1){
            obj.find(".checkOut").addClass('icon1_1');
        }else{
            obj.find(".checkOut").removeClass('icon1_1');    
        }
    }

    // 车辆在线状态
    if (dataObj.runState != undefined){
        if (dataObj.runState == 0){
            obj.find(".runState").addClass('icon2_1');
        }else{
            obj.find(".runState").removeClass('icon2_1');   
        }
    }

    // 计划到达时间
    if (dataObj.planRunTime != undefined){
        obj.find(".planRunTime").html(new Date(dataObj.planRunTime).toTimeString().slice(0,8));
    }


    // 车辆
    if (dataObj.carNum != undefined){
        obj.find(".carNum").html(dataObj.carNum);
    }

    // 线路
    if (dataObj.lineName != undefined){
        obj.find(".lineName").html(dataObj.lineName);
    }

    // 回场时间
    if (dataObj.planReachTime != undefined){
        obj.find(".planReachTime").html(new Date(dataObj.planReachTime).toTimeString().slice(0,8));
    }

    // 停车
    if (dataObj.stopTime != undefined){
        obj.find(".stopTime").html(new Date(dataObj.stopTime).toTimeString().slice(0,8));
    }
}


setTimeout(function(){
    linePlanParkOnlineModel_display($(".controller_1"));
}, 8000)