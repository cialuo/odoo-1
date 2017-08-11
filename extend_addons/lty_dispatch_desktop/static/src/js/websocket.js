/**
 * Created by Administrator on 2017/8/5.
 */

var websocket = null;

//判断当前浏览器是否支持WebSocket
if ('WebSocket' in window) {
    websocket = new SockJS("http://127.0.0.1:8769/wstest?userId=45454");
} else {
    alert('当前浏览器 Not support websocket');
}

//连接发生错误的回调方法
websocket.onerror = function() {
    console.log("WebSocket连接发生错误");
};
//连接成功建立的回调方法
websocket.onopen = function() {
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
//接收到消息的回调方法
var socket_model_info = {};
websocket.onmessage = function(event) {
    for (socket_model in socket_model_info) {
        var socket_model = socket_model_info[socket_model];
        socket_model.fn(event.data, socket_model.arg);
    }
    // var obj = {moduleName:"modelBus",controllerId:"kz123", data: [event.data]};
    //    var modelName = obj.moduleName;
    //    var controllerId = obj.controllerId;
    //    if (modelName == "modelBus"){
    //    	for (buskey in socket_model_info[modelName]){
    //    		var buskey_list = buskey.split("_");
    //    		var contId = buskey_list[1];
    //    		var line_on = buskey_list[2];
    //    		var bus_on = buskey_list[3];
    //    		if (controllerId == contId){
    //    			var buskeyObj = socket_model_info[modelName][buskey];
    //    			var model_data_list = obj.data;
    //     		for (var i=0;i<model_data_list.length;i++){
    //     			var model_data = model_data_list[i];
    //     			// if (model_data.line_on == line_on && model_data.bus_on == bus_on){
    //     				buskeyObj.fn(model_data, buskeyObj.arg);
    //     			// }
    //     		}
    //    		}
    //    	}
    //    }
    // var obj = JSON.parse(event.data);
    var obj = { modelName: "modelBus", controllerId: "kz123", data: [event.data] };
    var modelName = obj.modelName;
    var controllerId = obj.controllerId;

    if (modelName == "线路") {
        console.log('1');
    } else if (modelName == "客流运力") {
        console.log('2');
    } else if (modelName == "车辆资源状态") {
        console.log('3');
    } else if (modelName == "人力资源状态") {
        console.log('4');
    } else if (modelName == "modelBus") {
        modelBus($(".controller_" + controllerId), obj.data);
    } else if (modelName == "滞客信息") {
        console.log('6');
    } else if (modelName == "线路计划") {
        console.log('7');
    } else if (modelName == "线路车场") {
        console.log('8');
    } else if (modelName == "线路在途") {
        console.log('9');
    } else if (modelName == "消息") {
        console.log('10');
    } else if (modelName == "异常") {
        console.log('11');
    }
};

//连接关闭的回调方法
websocket.onclose = function() {
    console.log("WebSocket连接关闭");
};
//监听窗口关闭事件，当窗口关闭时，主动去关闭websocket连接，防止连接还没断开就关闭窗口，server端会抛异常。
window.onbeforeunload = function() {
    closeWebSocket();
};

//关闭WebSocket连接
function closeWebSocket() {
    websocket.close();
}

//发送消息
function send() {
    var message = document.getElementById('text').value;
    websocket.send(message);
}


function modelBus(controllerObj, data_list) {
    for (var i = 0, dl = data_list.length; i < dl; i++) {
        var dataObj = data_list[i];
        // debugger;
        // var dom = controllerObj.find(".modelBus_"+dataObj.line_on+"_"+dataObj.bus_on);
        var data = dataObj;
        var dom = controllerObj.find(".modelBus_1_222");
        if (dom.length > 0) {
        	console.log('come on')
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
            vehicleInformationObj.find(".current_speed").html(data.slice(84, 86));
            vehicleInformationObj.find(".direction").html('大亚湾'+data.slice(88, 89));
            vehicleInformationObj.find(".front_distance").html(data.slice(86, 87));
            vehicleInformationObj.find(".back_distance").html(data.slice(87, 88));
            vehicleInformationObj.find(".return_time").html(date_time);
            vehicleInformationObj.find(".next_trip_time").html(date_time_2);
            vehicleInformationObj.find(".residual_clearance").html(data.slice(76, 78) + 'KM/h');
            lineInfo.find(".lineRoad").html('18')
            lineInfo.find(".trip").html(data.slice(76, 77));
            lineInfo.find(".total_trip").html(data.slice(76, 77) + data.slice(77, 78));
            
            layer.close(sessionStorage.getItem("modelBus_layer"))
            dom.show();
        }
    }
}