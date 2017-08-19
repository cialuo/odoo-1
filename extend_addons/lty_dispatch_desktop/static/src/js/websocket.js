/**
 * Created by Administrator on 2017/8/5.
 */




var websocket = null;

//判断当前浏览器是否支持WebSocket
if ('WebSocket' in window) {
    websocket = new SockJS("http://127.0.0.1:8769/wstest?userId=45454");
    // websocket = new WebSocket("ws://202.104.136.228:8085/dispatch-websocket/websocket?userId=2222&token=55e1da6f0fe34f3a98a1faac5b939b68");
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
var socket_model_api_obj = {};
//接收到消息的回调方法
	// console.log(event.data);
	// return false;

websocket.onmessage123 = function (event) {
	console.log(event.data);
}

// var package = {
//     type: 1001,
//     open_modules: "dispatch-line_message-4",
//     msgId: Date.parse(new Date())
// };
// websocket.send(JSON.stringify(package));
websocket.onmessage = function (event) {
    // console.log(event.data)
    for (socket_model in socket_model_info) {
        var socket_model_obj = socket_model_info[socket_model];
        socket_model_obj.fn(event.data, socket_model_obj.arg);
    }
    var obj = {modelName: "bus_real_state", controllerId: "1", data: [event.data]};
    console.log('随机数为'+event.data.slice(78, 80));
    if (event.data.slice(78, 80) < 15) {
        obj.modelName = "passenger_delay";
    } else if (event.data.slice(78, 80) < 30) {
        // line_plan line_park line_online
        obj.modelName = "linePlanParkOnlineModel";
    } else if (event.data.slice(78, 80) < 45) {
        obj.modelName = "passenger_flow_capacity";
    } else if (event.data.slice(78, 80) < 60) {
        obj.modelName = "absnormal";
    }
    var modelName = obj.modelName;
    var controllerId = obj.controllerId;

    if (modelName == "线路") {
    } else if (modelName == "passenger_flow_capacity") {
        //客流与运力组件
        passenger_flow_capacity($(".controller_" + controllerId), obj.data);
    } else if (modelName == "车辆资源状态") {
        // console.log('3');
    } else if (modelName == "人力资源状态") {
        // console.log('4');
    } else if (modelName == "bus_real_state") {
        // console.log('5');
        busRealStateModel_socket_fn($(".controller_" + controllerId), obj.data);
    } else if (modelName == "passenger_delay") {
        // console.log('6');
        passengerDelayModel_socket_fn($(".controller_" + controllerId), obj.data);
    } else if (modelName == "linePlanParkOnlineModel") {
        // console.log('7');
        linePlanParkOnlineModel_socket_fn($(".controller_" + controllerId), obj.data);
    } else if (modelName == "线路车场") {
        // console.log('8');
    } else if (modelName == "线路在途") {
        // console.log('9');
    } else if (modelName == "消息") {
        // console.log('10');
    } else if (modelName == "absnormal") {
        // console.log(event.data[0].substring(78, 80))
        absnormal_del($(".controller_" + controllerId), obj.data);
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

var map_i = 0;
// 车辆实时状态模块
function busRealStateModel_socket_fn(controllerObj, data_list) {
    for (var i = 0, dl = data_list.length; i < dl; i++) {
        var dataObj = data_list[i];
        // debugger;
        // var dom = controllerObj.find(".busRealStateModel_"+dataObj.line_on+"_"+dataObj.bus_on);
        var data = dataObj;
        var map_list = [
            {longitude: 114.39973, latitude: 30.45787},
            {longitude: 114.398595, latitude: 30.457569},
            {longitude: 114.39948, latitude: 30.457231},
            {longitude: 114.400939, latitude: 30.45688},
            {longitude: 114.402237, latitude: 30.45639},
            {longitude: 114.402977, latitude: 30.457102},
            {longitude: 114.403675, latitude: 30.457823}
        ];
        var dom = controllerObj.find(".busRealStateModel_1_222");
        if (dom.length > 0) {
            console.log('come on');
            var vehicleInformationObj = dom.find(".popupContent .vehicleInformation");
            var carReportObj = dom.find(".popupContent .carReport");
            var lineInfo = dom.find(".lineInfo");
            var back_door_status = data.slice(83, 84) > 8 ? "<e class='danger'>开启</e>" : "关闭"
            var front_door_status = data.slice(84, 85) < 8 ? "<e class='danger'>开启</e>" : "关闭"
            var new_date = new Date();
            var date_time = new_date.getHours() + ":" + new_date.getMinutes();
            var new_data_2 = new Date(new_date.getTime() + 1000 * 60 * 30);
            var date_time_2 = new_data_2.getHours() + ":" + new_data_2.getMinutes();
            vehicleInformationObj.find(".passenger_number").html('62' + data.slice(78, 79));
            vehicleInformationObj.find(".satisfaction_rate").html(data.slice(78, 80) + "%");
            vehicleInformationObj.find(".inside_temperature").html(data.slice(80, 82));
            vehicleInformationObj.find(".outside_temperature").html(data.slice(82, 84));
            vehicleInformationObj.find(".back_door_status").html(back_door_status);
            vehicleInformationObj.find(".front_door_status").html(front_door_status);
            vehicleInformationObj.find(".current_speed").html(data.slice(84, 86) + 'KM/H');
            vehicleInformationObj.find(".direction").html('大亚湾'+data.slice(88, 89));
            vehicleInformationObj.find(".front_distance").html(data.slice(86, 87) + 'KM');
            vehicleInformationObj.find(".back_distance").html(data.slice(87, 88) + 'KM');
            vehicleInformationObj.find(".return_time").html(date_time);
            vehicleInformationObj.find(".next_trip_time").html(date_time_2);
            vehicleInformationObj.find(".residual_clearance").html(data.slice(76, 78) + 'KM');
            lineInfo.find(".lineRoad").html('18'+'路')
            lineInfo.find(".trip").html(data.slice(76, 77));
            lineInfo.find(".total_trip").html(data.slice(76, 77) + data.slice(77, 78));

            var busRealStateModel_set = JSON.parse(sessionStorage.getItem("busRealStateModel_set"));
            layer.close(busRealStateModel_set.layer_index);
            dom.removeClass('hide_model');
            var socket_load = carReportObj.find(".socket_load");
            var mapDom = carReportObj.find(".arrival_time_map");
            var chartDom = carReportObj.find(".arrival_time_chart");
            if (mapDom.length>0){
            	socket_load.remove();
            	mapDom.removeClass("hide_model");
	            if (map_i<6){
	            	map_i+=1;
	            	busRealStateModel_map(mapDom[0], map_list[map_i]);
	            	console.log('我是i'+map_i);
	            }
            }
            if (chartDom.length > 0){
            	socket_load.remove();
            	chartDom.removeClass("hide_model");
            }
        }
    }
}

function busRealStateModel_map(dom, gps){
	if (socket_model_api_obj.busRealStateModel.marker){
		socket_model_api_obj.busRealStateModel.marker.setPosition(new AMap.LngLat(gps.longitude, gps.latitude));
	}else{
		var mapObj = new AMap.Map(dom, {zoom: 14, center: [gps.longitude, gps.latitude]});
		var marker = new AMap.Marker({
	        map: mapObj,
	        position: [gps.longitude, gps.latitude]
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

// 线路计划，车场，在途模块
function linePlanParkOnlineModel_socket_fn(controllerObj, data_list){
	var dom = controllerObj.find(".linePlanParkOnlineModel");
	if (dom.length>0){
		var passengerDelayModel_set = JSON.parse(sessionStorage.getItem("linePlanParkOnlineModel_set"));
        layer.close(passengerDelayModel_set.layer_index);
        $('.linePlanParkOnlineModel .section_plan_cont').mCustomScrollbar(); 
        dom.removeClass('hide_model');
	}
}