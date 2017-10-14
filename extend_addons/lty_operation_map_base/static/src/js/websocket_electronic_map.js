/**
 * Created by Administrator on 2017/8/5.
 */

var websocket_electronic_map = null;

//判断当前浏览器是否支持WebSocket
if ('WebSocket' in window) {
    // websocket = new SockJS("http://127.0.0.1:8769/wstest?userId=45454");
    // websocket = new WebSocket("ws://202.104.136.228:8085/dispatch-websocket/websocket?userId=2222&token=55e1da6f0fe34f3a98a1faac5b939b68");
    websocket_electronic_map = new WebSocket( SOCKET_URL +"/Dsp_SocketService/websocket?userId=2222&token=55e1da6f0fe34f3a98a1faac5b939b68");
} else {
    alert('当前浏览器 Not support websocket');
}

//连接发生错误的回调方法
websocket_electronic_map.onerror = function () {
    console.log("WebSocket连接发生错误");
    layer.msg('WebSocket连接已经断开', {time: 2000, shade: 0.3});
};
//连接成功建立的回调方法
websocket_electronic_map.onopen = function () {
    console.log("WebSocket连接成功");
}

//接收到消息的回调方法
websocket_electronic_map.onmessage = function (event) {
    var eventData = JSON.parse(event.data);
    console.log(eventData);
    var modelName = eventData.moduleName;
    var oData = eventData.data;
    // debugger;
    if (modelName == "bus_site"){
        if (oData.line_id == TARGET_LINE_ID){
            if (TARGET_VEHICLE){
                if (oData.car_id == TARGET_VEHICLE){
                    update_vehicles_sockt(oData);
                }
                return false;
            }
            update_vehicles_sockt(oData);
        }
    }else if (modelName == "abnormal"){
        //车辆掉线
        if (eventData.packageType == 1003 && oData.line_id == TARGET_LINE_ID) {
            var abnormal_description = oData.abnormal_description;
            var vehicle_on = abnormal_description.bus_on;
            if (VEHICLE_INFO_DICT[vehicle_on.toString()]){
                update_icon(VEHICLE_INFO_DICT[vehicle_on.toString()], oData.status);
            }
        }
    }

};

//连接关闭的回调方法
websocket_electronic_map.onclose = function () {
    console.log("WebSocket连接关闭");
};
//监听窗口关闭事件，当窗口关闭时，主动去关闭websocket连接，防止连接还没断开就关闭窗口，server端会抛异常。
websocket_electronic_map.onbeforeunload = function () {
    websocket.close();
};
//监听窗口链接更改时，主动去关闭websocket连接，防止连接还没断开就关闭窗口，server端会抛异常
websocket_electronic_map.onhashchange = function(){
    websocket.close();
}


function update_vehicles_sockt(eventData){
    if (VEHICLE_INFO_DICT[eventData.car_id.toString()]){
        var carMap = VEHICLE_INFO_DICT[eventData.car_id.toString()];
        carMap.moveTo(new AMap.LngLat(eventData.longitude, eventData.latitude), 5000);
        update_icon(carMap, 1);
        if (eventData.car_id == TARGET_VEHICLE){
            target_vehicle_fn(carMap, eventData.longitude, eventData.latitude);
        }
    }else{
        if (CARMAP){
            var icon = get_icon();
            var marker = new AMap.Marker({
                content: get_content_fn(icon, eventData.car_id),
                position: [eventData.longitude, eventData.latitude],
                offset : new AMap.Pixel(-32,-16),
                autoRotation: true,
                map: CARMAP
            });
            VEHICLE_INFO_DICT[eventData.car_id.toString()] = marker;
            if (eventData.car_id.toString() == TARGET_VEHICLE){
                target_vehicle_fn(marker, eventData.longitude, eventData.latitude);
            }
        }
    }
}


function get_icon(st){
    var icon = '/lty_operation_map_base/static/src/image/vehicle_on.png';
    if (st==0){
        icon = '/lty_operation_map_base/static/src/image/vehicle_off.png';
    }
    return icon;
}

function get_content_fn(icon, onboardId){
    var div = document.createElement('div');
    div.style.display = "block";
    div.style.borderStyle = "none";
    div.style.borderWidth = "0px";
    div.style.position = "absolute";
    div.style.textAlign = "center";
    div.style.width = '70px';
    div.style.height = '32px';
    div.style.zIndex = '1';
    // 车辆编号
    var span = document.createElement("span");
    span.style.lineHeight = "16px";
    span.style.position = "absolute";
    span.style.top = "-16px";
    span.style.textShadow = "-1px 0 #FFFFFF, 0 1px #FFFFFF,1px 0 #FFFFFF, 0 -1px #FFFFFF";
    span.style.color = "#58554e";
    var text = document.createTextNode(onboardId);
    span.appendChild(text);
    setUnselected(span);
    div.appendChild(span);
    // 车辆图标
    var divImg = document.createElement("span");
    divImg.className = "carIcon";
    divImg.style.height = "32px";
    divImg.style.display = "inline-block";
    divImg.style.backgroundImage= "url('"+icon+"')";
    divImg.style.backgroundRepeat = "no-repeat";
    div.appendChild(divImg);
    return div;
}

function setUnselected(a){
    if(a.style&&a.style.MozUserSelect){
       a.style.MozUserSelect="none";
    }else if(a.style&&a.style.WebkitUserSelect){
       a.style.WebkitUserSelect="none";
    }else if(a.unselectable) {
        a.unselectable ="on";
        a.onselectstart =function(){return false};       
    }
}

function update_icon(map, st) {
    var childs = map.getContent().childNodes;
    for (var i = 0, l = childs.length; i<l; i++) {
        var child = childs[i];
        if (child.className == "carIcon") {
            child.style.backgroundImage = "url("+get_icon(st)+")";
        }
    }
}
function target_vehicle_fn(marker, longitude, latitude){
    var map = marker.getMap();
    var dom = marker.getContent();
    dom.style.borderStyle = "solid";
    dom.style.borderColor = "#5acbff";
    dom.style.borderWidth = "2px";
    map.setCenter([longitude, latitude]);
}