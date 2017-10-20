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
    layer.msg('WebSocket连接已经断开', {time: 1000, shade: 0.3});
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
    if (modelName == "bus_site"){
        if (oData.gprsId == TARGET_LINE_ID){
            if (TARGET_VEHICLE){
                if (oData.terminalNo == TARGET_VEHICLE){
                    electronicMap_update_vehicles_sockt(oData);
                }
                return false;
            }
            electronicMap_update_vehicles_sockt(oData);
        }
    }else if (modelName == "abnormal"){
        //车辆掉线
        if (eventData.packageType == 1003 && oData.gprsId == TARGET_LINE_ID) {
            var abnormal_description = oData.abnormal_description;
            var vehicle_on = abnormal_description.bus_on;
            if (VEHICLE_INFO_DICT[vehicle_on.toString()]){
                electronicMap_update_icon(VEHICLE_INFO_DICT[vehicle_on.toString()], 0);
            }
        }
    }else if (modelName == "bus_real_state"){
        electronicMap_busRealStateModel_socket_fn(oData);
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


function electronicMap_update_vehicles_sockt(eventData){
    var new_gps = CONVERSIONS_GPS.gcj_encrypt(eventData.latitude, eventData.longitude);
    if (VEHICLE_INFO_DICT[eventData.terminalNo.toString()]){
        var carMap = VEHICLE_INFO_DICT[eventData.terminalNo.toString()];
        carMap.moveTo(new AMap.LngLat(new_gps.lon, new_gps.lat), 300);
        electronicMap_update_icon(carMap, 1);
        if (eventData.terminalNo == TARGET_VEHICLE){
            electronicMap_target_vehicle_fn(carMap, new_gps.lon, new_gps.lat);
        }
    }else{
        if (CARMAP){
            var onboardId = eventData.terminalNo.toString();
            if (ONBOARDID_INNERCODE_DICT[onboardId] && ONBOARDID_INNERCODE_DICT[onboardId]!="undefined") {
                var icon = electronicMap_get_icon();
                var marker = new AMap.Marker({
                    content: electronicMap_get_content_fn(icon, eventData.terminalNo.toString()),
                    position: [new_gps.lon, new_gps.lat],
                    offset : new AMap.Pixel(-32,-16),
                    autoRotation: true,
                    map: CARMAP
                });
                VEHICLE_INFO_DICT[eventData.terminalNo.toString()] = marker;
                if (eventData.terminalNo.toString() == TARGET_VEHICLE){
                    electronicMap_target_vehicle_fn(marker, new_gps.lon, new_gps.lat, true);
                }
            }
        }
    }
}


function electronicMap_get_icon(st){
    var icon = '/lty_operation_map_base/static/src/image/vehicle_on.png';
    if (st==0){
        icon = '/lty_operation_map_base/static/src/image/vehicle_off.png';
    }
    return icon;
}

function electronicMap_get_content_fn(icon, onboardId){
    var div = document.createElement('div');
    div.className = "vehicleMapMarker";
    div.setAttribute("onboardId", onboardId);
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
    span.className = "carText";
    span.style.lineHeight = "16px";
    span.style.position = "absolute";
    span.style.top = "-16px";
    span.style.textShadow = "-1px 0 #FFFFFF, 0 1px #FFFFFF,1px 0 #FFFFFF, 0 -1px #FFFFFF";
    span.style.color = "#58554e";
    if (!ONBOARDID_INNERCODE_DICT[onboardId] || ONBOARDID_INNERCODE_DICT[onboardId]=="undefined") {
        console.log(ONBOARDID_INNERCODE_DICT);
        console.log(onboardId);
        debugger;
    }
    var text = document.createTextNode(ONBOARDID_INNERCODE_DICT[onboardId]);
    span.appendChild(text);
    electronicMap_setUnselected(span);
    div.appendChild(span);
    // 车辆图标
    var divImg = document.createElement("span");
    divImg.className = "carIcon";
    divImg.style.width = "32px";
    divImg.style.height = "32px";
    divImg.style.display = "inline-block";
    divImg.style.backgroundImage= "url('"+icon+"')";
    divImg.style.backgroundRepeat = "no-repeat";
    div.appendChild(divImg);
    return div;
}

function electronicMap_setUnselected(a){
    if(a.style&&a.style.MozUserSelect){
       a.style.MozUserSelect="none";
    }else if(a.style&&a.style.WebkitUserSelect){
       a.style.WebkitUserSelect="none";
    }else if(a.unselectable) {
        a.unselectable ="on";
        a.onselectstart =function(){return false};       
    }
}

function electronicMap_update_icon(map, st) {
    var childs = map.getContent().childNodes;
    for (var i = 0, l = childs.length; i<l; i++) {
        var child = childs[i];
        if (child.className == "carIcon") {
            child.style.backgroundImage = "url("+electronicMap_get_icon(st)+")";
        }
    }
}
function electronicMap_target_vehicle_fn(marker, longitude, latitude, is_flash){
    var dom = marker.getContent();
    dom.style.borderStyle = "solid";
    dom.style.borderColor = "#5acbff";
    dom.style.borderWidth = "2px";
    CARMAP.setCenter([longitude, latitude]);
    if (is_flash){
        electronicMap_map_vehicle_flash(marker)
    }
}

// 目标车闪烁
function electronicMap_map_vehicle_flash(marker){
    var marker_dom = marker.getContent();
    var w = marker_dom.style.borderWidth;
    var i = 0;
    var twinkleLineTimer = window.setInterval(function(){
        if (i>=8){
            window.clearInterval(twinkleLineTimer);
        }
        if (i%2){
            w = "4px";
        }else{
            w = "2px";
        }
        marker_dom.style.borderWidth = w;
        i++;
    },200)
}

// 车辆实时状态模块
function electronicMap_busRealStateModel_socket_fn(dataObj) {
    // var dom = controllerObj.find(".busRealStateModel_" + dataObj.line_no + "_" + dataObj.bus_no);
    var controllerObj = $(".map_work_trace electronic_map");
    var dom = controllerObj.find(".busRealStateModel");
    if (dom.length > 0) {
        var vehicleInformationObj = dom.find(".popupContent .vehicleInformation");
        var carReportObj = dom.find(".popupContent .carReport");
        var lineInfo = dom.find(".lineInfo");
        vehicleInformationObj.find(".license_number").html("车号：" + dataObj.license_number);
        vehicleInformationObj.find(".license_plate").html(dataObj.license_plate);
        vehicleInformationObj.find(".driver").html("司机：" + dataObj.driver);
        vehicleInformationObj.find(".crew").html("乘务：" + dataObj.conductor);
        vehicleInformationObj.find(".passenger_number").html(dataObj.full_load_rate);
        vehicleInformationObj.find(".full_load_rate").html(dataObj.passenger_number);
        vehicleInformationObj.find(".satisfaction_rate").html(dataObj.satisfaction_rate);
        vehicleInformationObj.find(".inside_temperature").html(dataObj.inside_temperature);
        vehicleInformationObj.find(".outside_temperature").html(dataObj.outside_temperature);
        vehicleInformationObj.find(".back_door_status").html(dataObj.back_door_status);
        vehicleInformationObj.find(".front_door_status").html(dataObj.front_door_status);
        vehicleInformationObj.find(".current_speed").html(dataObj.speed + 'KM/H');
        vehicleInformationObj.find(".direction").html(dataObj.direction);
        vehicleInformationObj.find(".front_distance").html(dataObj.front_distance + 'KM');
        vehicleInformationObj.find(".back_distance").html(dataObj.back_distance + 'KM');
        vehicleInformationObj.find(".return_time").html(dataObj.return_time.slice(0, 5));
        vehicleInformationObj.find(".next_trip_time").html(dataObj.next_trip_time.slice(0, 5));
        vehicleInformationObj.find(".residual_clearance").html(dataObj.residual_clearance + 'KM');
        // lineInfo.find(".lineRoad").html(dataObj.lineName);
        lineInfo.find(".trip").html(dataObj.satisfaction_rate);
        lineInfo.find(".total_trip").html(dataObj.satisfaction_rate);

        // var busRealStateModel_set = JSON.parse(sessionStorage.getItem("busRealStateModel_set"));
        // layer.close(busRealStateModel_set.layer_index);
        dom.removeClass('hide_model');
        var socket_load = carReportObj.find(".socket_load");
        var mapDom = carReportObj.find(".arrival_time_map");
        var chartDom = carReportObj.find(".arrival_time_chart");
        if (mapDom.length > 0) {
            socket_load.remove();
            mapDom.removeClass("hide_model");
            electronicMap_busRealStateModel_map(mapDom[0], dataObj);
        } else if (chartDom.length > 0) {
            socket_load.remove();
            chartDom.removeClass("hide_model");
            electronicMap_busRealStateModel_chart(chartDom[0], dataObj);
        }
    }
}

// 车辆实时状态模块-地理位置
function electronicMap_busRealStateModel_map(dom, gps) {
    if (!gps.latitude) {
        return false;
    }

    var new_gps = CONVERSIONS_GPS.gcj_encrypt(gps.latitude, gps.longitude);

    if (socket_model_api_obj.busRealStateModel_marker) {
        socket_model_api_obj.busRealStateModel_marker.setPosition(new AMap.LngLat(new_gps.lon, new_gps.lat));
    } else {
        var mapObj = new AMap.Map(dom, {zoom: 14, center: [new_gps.lon, new_gps.lat]});
        var marker = new AMap.Marker({
            map: mapObj,
            position: [new_gps.lon, new_gps.lat]
        });
        socket_model_api_obj.busRealStateModel_marker = marker;
    }
}

// 车辆实时状态模块-到站时刻
function electronicMap_busRealStateModel_chart(dom, dataObj) {
    var site_list = [],
        yuche_data = [],
        shiji_data = [];

    var chartData = dataObj.dataList;
    for (var i = 0, l = chartData.length; i < l; i++) {
        var cObj = chartData[i];
        site_list.push(cObj.stationId);
        yuche_data.push(cObj.predictedTime);
        shiji_data.push(cObj.realTime);
    }

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
            data: ['计划', '预测', '实际']
        },
        animation: false,
        grid: {
            left: '5%',
            right: '10%',
            bottom: '2%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: site_list,
            axisLabel: {
                textStyle: {
                    color: "#fff"
                }
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
            axisTick: {show: false},
            splitLine: {
                lineStyle: {
                    color: ['#454c6c']
                }
            }
        },
        series: [
            {
                name: '计划',
                type: 'line',
                symbolSize: 1,
                data: [0, 0, 0, 0, 0, 0, 0, 0],
                lineStyle: {
                    normal: {
                        width: 1
                    }
                },
            },
            {
                name: '预测',
                type: 'line',
                symbolSize: 1,
                data: yuche_data,
                lineStyle: {
                    normal: {
                        width: 1
                    }
                },
            },
            {
                name: '实际',
                type: 'line',
                symbolSize: 1,
                data: shiji_data,
                lineStyle: {
                    normal: {
                        width: 1
                    }
                },
            }
        ]
    };
    var myChart = echarts.init(dom);
    myChart.setOption(option);
}