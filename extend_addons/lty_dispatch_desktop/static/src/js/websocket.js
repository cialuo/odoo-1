/**
 * Created by Administrator on 2017/8/5.
 */

var websocket = null;

//判断当前浏览器是否支持WebSocket
if ('WebSocket' in window) {
    // websocket = new SockJS("http://127.0.0.1:8769/wstest?userId=45454");
    // websocket = new WebSocket("ws://202.104.136.228:8085/dispatch-websocket/websocket?userId=2222&token=55e1da6f0fe34f3a98a1faac5b939b68");
    websocket = new WebSocket("ws://202.104.136.228:8085/Dsp_SocketService/websocket?userId=2222&token=55e1da6f0fe34f3a98a1faac5b939b68");
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

var socket_model_info = {};
var socket_model_api_obj = {};
//接收到消息的回调方法
websocket.onmessage = function (event) {
    var eventObj = JSON.parse(event.data);
    var modelName = eventObj.moduleName;
    var controllerId = eventObj.controllerId;
    var controllerObj = $(".controller_" + controllerId);
    var eventData = eventObj.data;
    console.log(eventObj);
    // if ($.inArray(modelName, ['passenger_delay', 'bus_real_state', "line_plan", "line_park", "line_online"])!=-1){
        // console.log(eventObj);
    // }
    //由于车辆上下行计划，车场，在途数据来源于restful，这里只会收到update的推送，由于要做些简单处理，所以在这里直接触发展示
    // linePlanParkOnlineModel_display(controllerObj);

    if (modelName == "line_message") {
        use_odoo_model(event, "line_message");
    } else if (modelName == "passenger_flow") {
        //客流与运力组件
        use_odoo_model(event, "passenger_flow");
    } else if (modelName == "人力资源状态") {

    }else if (modelName == "bus_resource"){
        line_resource(controllerObj, eventData);
    }
    else if (modelName == "bus_real_state") {
        busRealStateModel_socket_fn(controllerObj, eventData);
    }
    else if (modelName == "passenger_delay") {
        passengerDelayModel_socket_fn(controllerObj, eventData);
    } else if ($.inArray(modelName, ["line_plan", "line_park", "line_online"]) != -1) {
        update_linePlanParkOnlineModel_socket_fn(controllerObj, eventData, modelName);
    } else if (modelName == "消息") {
        // console.log('10');
    } else if (modelName == "abnormal") {
        absnormal_del(controllerObj, eventData);
        use_odoo_model(event,"abnormal");
        line_car_src_on_line(controllerObj, eventObj);
        //车辆掉线包
        if (eventObj.type == 1003){
            vehicle_drop(controllerObj, eventData);
        }
    }
    // else if (modelName == "bus_real_state") {
    //     line_car_src_real_state($(".controller_" + controllerId), eventObj.data);
    //     show_electronic_map($(".controller_" + controllerId).find('#digital_map'), eventObj.data, 'elec_map_layer')
    // }
};

//连接关闭的回调方法
websocket.onclose = function () {
    console.log("WebSocket连接关闭");
};
//监听窗口关闭事件，当窗口关闭时，主动去关闭websocket连接，防止连接还没断开就关闭窗口，server端会抛异常。
window.onbeforeunload = function () {
    websocket.close();
};

function use_odoo_model(event, model_name) {
    for (socket_model in socket_model_info) {
        var socket_model_obj = socket_model_info[socket_model];
        if (socket_model.split("__")[0] == model_name) {
            socket_model_obj.fn(event.data, socket_model_obj.arg);
        }
    }
}

// 在线掉线包
function line_car_src_on_line(controllerObj, data_list) {
    var dom = controllerObj.find('.bus_src_config[line_id=' + data_list.line_id + ']');
    // 根据车辆id去进行处理
    if (dom.length > 0 && data_list.type == 1003) {
        dom.find('.line_src_sinal_status').html(data_list.data.status);
    }
}

//根据车辆实时状态修改车辆资源
function line_car_src_real_state(controllerObj, data_list) {
    var dom = controllerObj.find('.bus_src_config[line_id=' + data_list.line_id + ']');
    var bus_no = data_list.bus_no;
    if (dom.length > 0) {
        dom.find('tr[src_id=' + bus_no + ']').find('.line_src_site .position_site').html('(' + data_list.location_lan + ',' + data_list.location_log + ')');
        dom.find('tr[src_id=' + bus_no + ']').find('.line_src_Passanger_number').html(data_list.passenger_number);
        dom.find('tr[src_id=' + bus_no + ']').find('.line_src_Passanger_number').html(data_list.full_load_rate + '%');
        dom.find('tr[src_id=' + bus_no + ']').find('.line_src_speed').html(data_list.speed);
        dom.find('tr[src_id=' + bus_no + ']').find('.line_src_speed').html(data_list.residual_clearance);
    }
}

function line_resource(controllerObj, data_list) {
    var dom = controllerObj.find('.bus_src_config[line_id=' + data_list.line_id + ']');
    // 通过lineid以及资源id拿到信息
    if (dom.length > 0) {
        //遍历车辆资源新增的数据
        var theid = data_list.id;
        var tr_num = $('.table_bus_num').find('tr[src_id=' + theid + ']');
        if (data_list.planRunTime != '') {
            dom.find('.line_src_next_trip_time').html(data_list.planRunTime.split(' ')[1]);
        }
        // if(data_list.data.planRunTime.length>0){
        //     tr_num.find('.line_src' + planRunTime).html(data_list.data.planRunTime);
        // }
        if (tr_num.find('.line_src_sinal_status').html() == '异常') {
            tr_num.find('.line_src_sinal_status').addClass('towarn');
            tr_num.find('.line_src_onBoardId').addClass('towarn');
        }
        else {
            tr_num.find('.line_src_sinal_status').removeClass('towarn');
            tr_num.find('.line_src_onBoardId').removeClass('towarn');
        }
    }
}
// 异常
function absnormal_del(controllerObj, data_list) {
    var dom = controllerObj.find('.updown_line_table[line_id=' + data_list.line_id + ']');
    var dom_singal = controllerObj.find('.dispatch_desktop[line_id=' + data_list.line_id + ']');
    if (dom.length > 0) {
        dom.find('.no_absnormal').eq(0).show().siblings().hide();
        var abnoraml_desc = $('body').find('.absnormal_diaodu .absnormal_type p');
        //车辆掉线
        if (data_list.packageType == 1003) {
            abnoraml_desc.html(data_list.abnormal_description.bus_no + '车辆掉线');
            dom_singal.find('.singalIn span').html(parseInt(dom_singal.find('.singalIn span').html()) - 1);
            dom_singal.find('.singalOut span').html(parseInt(dom_singal.find('.singalOut span').html()) + 1);
        }
        // 出勤异常
        else if (data_list.packageType == 1004) {
            abnoraml_desc.html('（员工）：' + data_list.abnormal_description.staff_name + '考勤异常');
        }
        // 到站准点异常
        else if (data_list.packageType == 1005) {
            abnoraml_desc.html(data_list.abnormal_description.bus_no + '到达站点：' + data_list.abnormal_description.station_name + '与' + data_list.abnormal_description.actual_time + '相差' + data_list.abnormal_description.diff_time);
        }
        // 到站预测准点异常
        else if (data_list.packageType == 1006) {
            abnoraml_desc.html(data_list.abnormal_description.bus_no + '到达站点：' + data_list.abnormal_description.station_name + '与' + data_list.abnormal_description.actual_time + '相差' + data_list.abnormal_description.diff_time);
        }
        // 趟次回场异常包
        else if (data_list.packageType == 1007) {
            abnoraml_desc.html('车辆：' + data_list.abnormal_description.bus_no + ',回场停车时间为：' + data_list.abnormal_description.return_time + ',回场异常');
        }
        // 趟次回场严重异常
        else if (data_list.packageType == 1008) {
            abnoraml_desc.html('车辆：' + data_list.abnormal_description.bus_no + ',回场停车时间为：' + data_list.abnormal_description.return_time + ',回场严重异常');
        }
        // 车越界行驶
        else if (data_list.packageType == 1009) {
            abnoraml_desc.html('车辆：' + data_list.abnormal_description.bus_no + '偏离路线');
        }
        // 异常滞留
        else if (data_list.packageType == 1010) {
            abnoraml_desc.html('车辆：' + data_list.abnormal_description.bus_no + '已在途中停车' + data_list.abnormal_description.bus_stop_time);
        }
        // 前车距离异常
        else if (data_list.packageType == 1011) {
            abnoraml_desc.html('前车辆：' + data_list.abnormal_description.front_bus_no + '与后车' + data_list.abnormal_description.behind_bus_no + ',疑似串车/大间隔');
        }
        // 超速异常
        else if (data_list.packageType == 1012) {
            abnoraml_desc.html('车辆' + data_list.abnormal_description.bus_no + '超速,最高时速为' + data_list.abnormal_description.highest_speed);
        }
        // 事故异常
        else if (data_list.packageType == 1013) {
            abnoraml_desc.html('车辆' + data_list.abnormal_description.bus_no + '员工' + data_list.abnormal_description.employee_name + '疑似发生事故');
        }
        // 扣车异常
        else if (data_list.packageType == 1014) {
            abnoraml_desc.html('车辆' + data_list.abnormal_description.bus_no + '员工' + data_list.abnormal_description.employee_no + '疑似扣车');
        }
        // 抛锚预警
        else if (data_list.packageType == 1015) {
            abnoraml_desc.html('车辆' + data_list.abnormal_description.bus_no + '员工' + data_list.abnormal_description.employee_no + '疑似抛锚');
        }
        // 提前或延后发车
        else if (data_list.packageType == 1016) {
                abnoraml_desc.html('车辆' + data_list.abnormal_description.bus_no + '员工' + data_list.abnormal_description.employee_name + '提前发车,提前' + data_list.abnormal_description.advance_time +'分钟');
        }
        // 到点未发车
        else if (data_list.packageType == 1017) {
            abnoraml_desc.html('车辆' + data_list.abnormal_description.bus_no + '员工' + data_list.abnormal_description.employee_name + '到点未发车,滞后' + data_list.abnormal_description.retention_time+'分钟');
        }
        // 意外高峰
        else if (data_list.packageType == 1018) {
            abnoraml_desc.html(data_list.abnormal_description.date_start.split(' ')[1] + '到' + data_list.abnormal_description.date_end.split(' ')[1] + '产生意外客流高峰');
        }
        // 时段意外低峰
        else if (data_list.packageType == 1019) {
            abnoraml_desc.html(data_list.abnormal_description.date_start.split(' ')[1] + '到' + data_list.abnormal_description.date_end.split(' ')[1] + '产生意外客流高峰');
        }
        // 站点意外高峰
        else if (data_list.packageType == 1020) {
            abnoraml_desc.html('站点:' + data_list.abnormal_description.station + ',' + data_list.abnormal_description.date_start + '到' + data_list.abnormal_description.date_end + '产生意外高峰');
        }
        // 站点意外低峰
        else if (data_list.packageType == 1021) {
            abnoraml_desc.html('站点:' + data_list.abnormal_description.station + ',' + data_list.abnormal_description.date_start + '到' + data_list.abnormal_description.date_end + '产生意外低峰');
        }
        $('body').find('.absnormal_diaodu .absnormal_sug p').html(data_list.suggest);
        dom.addClass('warn').find('.passenger_flow_list').eq(0).find('.abs_info').append($('body').find('.absnormal_diaodu').html());
        var timer_carousel = sessionStorage.getItem('timer' + data_list.line_id);
        clearInterval(timer_carousel);
        dom.find('.carousel_content').addClass('abnormal_active');
        sessionStorage.removeItem('timer' + data_list.line_id);
        //信号在线掉线处理
    }
}

// 电子地图模块
function show_electronic_map(dom, data_list, session_ayer) {
    if (dom.length > 0) {
        var layer_map_close = JSON.parse(sessionStorage.getItem(session_ayer));
        layer.close(layer_map_close.layer_map);
        if (socket_model_api_obj.electronicMapModel.marker) {
            socket_model_api_obj.electronicMapModel.marker.setPosition(new AMap.LngLat(data_list.location_log, data_list.location_lan));
        } else {
            var mapObj = new AMap.Map(dom[0], {zoom: 14, center: [data_list.location_log, data_list.location_lan]});
            var marker = new AMap.Marker({
                map: mapObj,
                position: [data_list.location_log, data_list.location_lan]
            });
            socket_model_api_obj.electronicMapModel.marker = marker;

        }
    }
}

// 车辆掉线
function vehicle_drop(controllerObj, dataObj){
    var dom = controllerObj.find("linePlanParkOnlineModel");
    if (dom.length>0){
        var abnormal_description = dataObj.abnormal_description;
        var vehicle = dom.find(".yard_box .content_tb tr[pid="+abnormal_description.bus_on+"]");
        if (vehicle.length>0){
            vehicle.find(".runState").removeClass("icon2_1").addClass("icon2_0");
        }
    }
}

// 车辆实时状态模块
function busRealStateModel_socket_fn(controllerObj, dataObj) {
    // console.log(dataObj+"_bus")
    var dom = controllerObj.find(".busRealStateModel_"+dataObj.line_id+"_"+dataObj.bus_no);
    if (dom.length > 0) {
        var vehicleInformationObj = dom.find(".popupContent .vehicleInformation");
        var carReportObj = dom.find(".popupContent .carReport");
        var lineInfo = dom.find(".lineInfo");
        vehicleInformationObj.find(".license_number").html("车号：" + dataObj.license_number);
        vehicleInformationObj.find(".license_plate").html(dataObj.license_plate);
        vehicleInformationObj.find(".driver").html("司机：" + dataObj.driver);
        vehicleInformationObj.find(".crew").html("乘务：" + dataObj.conductor);
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
        lineInfo.find(".lineRoad").html('18' + '路');
        lineInfo.find(".trip").html(dataObj.satisfaction_rate);
        lineInfo.find(".total_trip").html(dataObj.satisfaction_rate);

        var busRealStateModel_set = JSON.parse(sessionStorage.getItem("busRealStateModel_set"));
        layer.close(busRealStateModel_set.layer_index);
        dom.removeClass('hide_model');
        var socket_load = carReportObj.find(".socket_load");
        var mapDom = carReportObj.find(".arrival_time_map");
        var chartDom = carReportObj.find(".arrival_time_chart");
        if (mapDom.length > 0) {
            socket_load.remove();
            mapDom.removeClass("hide_model");
            busRealStateModel_map(mapDom[0], dataObj);
        }
        if (chartDom.length > 0) {
            socket_load.remove();
            chartDom.removeClass("hide_model");
        }
    }
}

// 车辆实时状态模块-地理位置
function busRealStateModel_map(dom, gps) {
    if (socket_model_api_obj.busRealStateModel.marker) {
        socket_model_api_obj.busRealStateModel.marker.setPosition(new AMap.LngLat(gps.location_log, gps.location_lan));
    } else {
        var mapObj = new AMap.Map(dom, {zoom: 14, center: [gps.location_log, gps.location_lan]});
        var marker = new AMap.Marker({
            map: mapObj,
            position: [gps.location_log, gps.location_lan]
        });
        socket_model_api_obj.busRealStateModel.marker = marker;
    }
}

// 站点实时状态模块
function passengerDelayModel_socket_fn(controllerObj, dataObj) {
    console.log(dataObj);
    var dom = controllerObj.find(".passengerDelayModel");
    if (dom.length > 0) {

        // var passengerDelayModel_set = JSON.parse(sessionStorage.getItem("passengerDelayModel_set"));
        // layer.close(passengerDelayModel_set.layer_index);
        // dom.removeClass('hide_model');
        var trendObj = dom.find(".trend_chart_single");
        if (dataObj.packageType == 1034){
            trendObj = dom.find(".trend_chart_summary");
        }
        var trend_chart_map = trendObj.find(".trend_chart_map");
        var map_botton_info = trendObj.find(".map_botton_info");
        map_botton_info.find("li:eq(0) span").html(dataObj.station_lag_passengers);
        map_botton_info.find("li:eq(1) span").html(dataObj.down_passengers);
        map_botton_info.find("li:eq(2) span").html(dataObj.up_passengers);
    }
}

// 线路计划，车场，在途模块 显示
function linePlanParkOnlineModel_display(controllerObj) {
    var dom = controllerObj.find(".linePlanParkOnlineModel");
    if (dom.length > 0) {
        var passengerDelayModel_set = JSON.parse(sessionStorage.getItem("linePlanParkOnlineModel_set"));
        layer.close(passengerDelayModel_set.layer_index);
        $('.linePlanParkOnlineModel .section_plan_cont').mCustomScrollbar({
            theme: 'minimal'
        });
        if (dom.find(".mCustomScrollbar").length > 0) {
            dom.removeClass('hide_model');
        }
    }
}

// 线路计划，车场，在途模块 update
// 排序规则：有计划时间的情况下优先计划时间，没有计划时间的情况下按回场时间，都没有的情况下按车辆编号；
// 注意：所有排序规则均升序排列
function update_linePlanParkOnlineModel_socket_fn(controllerObj, dataObj, modelName) {
    var dom = controllerObj.find(".linePlanParkOnlineModel_" + dataObj.line_id);
    if (dom.length > 0 && dataObj.id) {
        var busResource = JSON.parse(sessionStorage.getItem("busResource"));
        if (modelName == "line_plan") {
            // var content_tb_obj = controllerObj.find(".bus_plan[direction=" + dataObj.direction + "] .content_tb");
            // var tr_obj = controllerObj.find(".bus_plan[direction=" + dataObj.direction + "]").find(".content_tb tr[pid=" + dataObj.id + "]");
            // var tr_obj = controllerObj.find(".bus_plan .content_tb tr[pid=" + dataObj.id + "]");
            // update_linePlan(tr_obj, content_tb_obj, dataObj);
            update_linePlan(controllerObj, dataObj);
        }else{
            // console.log(dataObj);
            // console.log(modelName);
            // debugger;
            var active_resource = new Object();
            for (var o = 0, ol = busResource.length; o < ol; o++) {
                var ol_resource = busResource[o];
                if (ol_resource.id == dataObj.id) {
                    active_resource = ol_resource;
                    break;
                }
            }

            if (!active_resource.id) {
                return false;
            }

            $.extend(active_resource, dataObj);
            var tr_obj = controllerObj.find(".content_tb tr[pid=" + dataObj.id + "]");
            var direction = dataObj.direction;
            if (tr_obj.length) {
                direction = tr_obj.attr("direction");
            }

            if (modelName == "line_park") {
                var content_tb_obj = controllerObj.find(".bus_yard[direction=" + direction + "] .content_tb");
                update_linePark(tr_obj, content_tb_obj, active_resource);
            } else {
                var content_tb_obj = controllerObj.find(".bus_transit[direction=" + direction + "] .content_tb");
                update_busTransit(tr_obj, content_tb_obj, active_resource);
            }
        }
        $('.linePlanParkOnlineModel').mCustomScrollbar("update");
    }
}

// 计划更新
function update_linePlan(controllerObj, dataObj) {
    var set_op = {
        id: dataObj.id || "",
        direction: dataObj.direction || "",
        planRunTime: dataObj.planRunTime || "",
        sendToScreen: dataObj.sendToScreen || "",
        sendToBus: dataObj.sendToBus || "",
        planReachTime: dataObj.planReachTime || "",
        selfId: dataObj.selfId || "",
        driverName: dataObj.driverName || ""
    };

    var active_tr_obj = controllerObj.find(".bus_plan .content_tb tr[pid=" + dataObj.id + "]");

    // 已完成的计划移除
    if (dataObj.planState == 2 || dataObj.planState == 3) {
        active_tr_obj.remove();
        return false;
    }

    if (active_tr_obj.length == 0 && typeof dataObj.direction == undefined) {
        console.log(dataObj);
        alert("数据有异常")
        return false;
    }

    if (active_tr_obj.length == 0) {
        // 没有且计划状态非完成则为新增,需按照计划发车时间先后插入
        var content_tb_obj = controllerObj.find(".bus_plan[direction=" + dataObj.direction + "] .content_tb");
        var obj_str =
            '<tr class="point" pid="' + set_op.id + '" direction="' + set_op.direction + '" planRunTime="' + set_op.planRunTime + '">' +
            '<td class="pL">' +
            '<span st="' + set_op.sendToScreen + '" class="icon sendToScreen icon_' + set_op.sendToScreen + '"></span>' +
            '<span st="' + set_op.sendToBus + '" class="icon sendToBus icon_' + set_op.sendToBus + '"></span>' +
            '</td>' +
            '<td class="planRunTime">' +
            new Date(set_op.planRunTime).toTimeString().slice(0, 5).replace('Inval', '') +
            '</td>' +
            '<td class="planReachTime">' +
            new Date(set_op.planReachTime).toTimeString().slice(0, 5).replace('Inval', '') +
            '</td>' +
            '<td class="selfId">' +
            set_op.selfId +
            '</td>' +
            '<td class="driverName">' +
            set_op.driverName +
            '</td>' +
            '<td class="pR planState">' +
            '待发' +
            '</td>' +
            '</tr>';
        var obj_list = content_tb_obj.find("tr.point");
        if (obj_list.length == 0) {
            content_tb_obj.append(obj_str);
            return false;
        }
        for (var i = 0, L = obj_list.length; i < L; i++) {
            var tr_obj = obj_list[i];
            var planRunTime = tr_obj.getAttribute("planRunTime");
            var b_pid = tr_obj.getAttribute("pid");
            //  由于车辆计划行驶表都有计划时间则直接按计划时间升序排列
            if (planRunTime > (new Date(dataObj.planRunTime).getTime())) {
                content_tb_obj.find("tr[pid=" + b_pid + "]").before(obj_str);
                break;
            }
        }
        if (controllerObj.find(".bus_plan[direction=" + dataObj.direction + "] .content_tb tr[pid=" + dataObj.id + "]").length == 0) {
            content_tb_obj.append(obj_str);
        }
        return false;
    }

    if (typeof dataObj.direction!=undefined && active_tr_obj.attr('direction')!=dataObj.direction){
        var content_tb_obj = controllerObj.find(".bus_plan[direction=" + dataObj.direction + "] .content_tb");
        var obj_list = content_tb_obj.find("tr.point");
        for (var i = 0, L = obj_list.length; i < L; i++) {
            var tr_obj = obj_list[i];
            var planRunTime = tr_obj.getAttribute("planRunTime");
            var b_pid = tr_obj.getAttribute("pid");
            //  由于车辆计划行驶表都有计划时间则直接按计划时间升序排列
            if (planRunTime > active_tr_obj.attr("planRunTime")) {
                content_tb_obj.find("tr[pid=" + b_pid + "]").before(obj_str);
                break;
            }
        }
        if (controllerObj.find(".bus_plan[direction=" + dataObj.direction + "] .content_tb tr[pid=" + dataObj.id + "]").length == 0) {
            content_tb_obj.append(active_tr_obj);
        }
        return false;
    }

    // 发送计划到调度屏状态
    if (dataObj.sendToScreen != undefined) {
        if (dataObj.sendToScreen == 1) {
            active_tr_obj.find(".sendToScreen").addClass('icon_1').removeClass('icon_0');
        } else {
            active_tr_obj.find(".sendToScreen").removeClass('icon_1').addClass('icon_0');
        }
    }

    // 发送计划到车辆状态
    if (dataObj.sendToBus != undefined) {
        if (dataObj.sendToBus == 1) {
            active_tr_obj.find(".sendToBus").addClass('icon_1').removeClass('icon_0');
        } else {
            active_tr_obj.find(".sendToBus").removeClass('icon_1').addClass("icon_0");
        }
    }

    // 计划到达时间
    if (dataObj.planRunTime != undefined) {
        active_tr_obj.find(".planRunTime").html(new Date(dataObj.planRunTime).toTimeString().slice(0, 5));
    }

    // 计划到达时间
    if (dataObj.planReachTime != undefined) {
        active_tr_obj.find(".planReachTime").html(new Date(dataObj.planReachTime).toTimeString().slice(0, 5));
    }

    // 车辆
    if (dataObj.selfId != undefined) {
        active_tr_obj.find(".selfId").html(dataObj.selfId);
    }

    // 司机
    if (dataObj.driverName != undefined) {
        obj.find(".driverName").html(dataObj.driverName);
    }

    // 待发状态
    if (dataObj.planState != undefined) {
        var txt = "待发";
        // 以下两种状态不展示，所以不会发生
        if (dataObj.planState == 2) {
            txt = "已完成";
        } else if (dataObj.planState == 3) {
            text = "已取消";
        }
        active_tr_obj.find(".planState").html(txt);
    }
}

// 车场更新
function update_linePark(obj, content_tb_obj, active_resource) {
    if (active_resource.inField == 0) {
        obj.remove();
        return false;
    }

    if (obj.length == 0) {
        // 没有则为新增,需按照计划发车时间先后插入
        var obj_str =
            '<tr class="point" pid="' + active_resource.id + '" direction="' + active_resource.direction + '" planRunTime="' + new Date(active_resource.planRunTime).toTimeString() + '" planReachTime="' + new Date(active_resource.realReachTime).toTimeString() + '">' +
            '<td class="pL">' +
            '<span st="' + active_resource.checkOut + '" class="icon sendToScreen icon1_' + active_resource.checkOut + '"></span>' +
            '<span st="' + active_resource.runState + '" class="icon sendToBus icon2_' + active_resource.runState + '"></span>' +
            '</td>' +
            '<td class="planRunTime">' +
            new Date(active_resource.planRunTime).toTimeString().slice(0, 5).replace("Inval", "") +
            '</td>' +
            '<td class="carNum">' +
            active_resource.carNum +
            '</td>' +
            '<td class="lineName">' +
            active_resource.lineName +
            '</td>' +
            '<td class="realReachTime">' +
            new Date(active_resource.realReachTime).toTimeString().slice(0, 5).replace("Inval", "") +
            '</td>' +
            '<td class="pR stopTime">' +
            active_resource.stopTime +
            '</td>' +
            '</tr>';

        var obj_list = content_tb_obj.find("tr.point");
        if (obj_list.length == 0) {
            content_tb_obj.append(obj_str);
            return;
        }
        for (var i = 0, L = obj_list.length; i < L; i++) {
            var tr_obj = obj_list[i];
            var planRunTime = tr_obj.getAttribute("planRunTime");
            var b_pid = tr_obj.getAttribute("pid");
            if (planRunTime > (new Date(active_resource.planRunTime).getTime())) {
                // tr_obj.before(obj_str);
                content_tb_obj.find("tr[pid=" + b_pid + "]").before(obj_str);
                break;
            }
        }

        if ($(".bus_yard[direction=" + active_resource.direction + "] .content_tb tr[pid=" + active_resource.id + "]").length == 0) {
            content_tb_obj.append(obj_str);
        }
        return false;
    }

    if (obj.attr('direction') != active_resource.direction) {
        obj.remove();
        return false;
    }

    // 司机签到状态
    if (active_resource.checkOut != undefined) {
        if (active_resource.checkOut == 1) {
            obj.find(".checkOut").addClass('icon1_1').removeClass("icon1_0");
        } else {
            obj.find(".checkOut").removeClass('icon1_1').addClass("icon1_0");
        }
    }

    // 车辆在线状态
    if (active_resource.runState != undefined) {
        if (active_resource.runState == 1) {
            obj.find(".runState").addClass('icon2_1').removeClass("icon2_0");
        } else {
            obj.find(".runState").removeClass('icon2_1').addClass("icon2_0");
        }
    }

    // 计划到达时间
    if (active_resource.planRunTime != undefined) {
        obj.find(".planRunTime").html(new Date(active_resource.planRunTime).toTimeString().slice(0, 5));
    }


    // 车辆
    if (active_resource.carNum != undefined) {
        obj.find(".carNum").html(active_resource.carNum);
    }

    // 线路
    if (active_resource.lineName != undefined) {
        obj.find(".lineName").html(active_resource.lineName);
    }

    // 回场时间
    if (active_resource.realReachTime != undefined) {
        obj.find(".realReachTime").html(new Date(active_resource.realReachTime).toTimeString().slice(0, 5));
    }

    // 停车
    if (active_resource.stopTime != undefined) {
        obj.find(".stopTime").html(active_resource.stopTime);
    }
}

// 在途更新
function update_busTransit(obj, content_tb_obj, active_resource) {
    if (active_resource.inField == 1) {
        obj.remove();
        return false;
    }
    if (obj.length == 0) {
        // 没有则为新增,需按照计划发车时间先后插入
        var obj_str =
            '<tr class="point" pid="' + active_resource.id + '" direction="' + active_resource.direction + '" planRunTime="' + new Date(active_resource.planRunTime).toTimeString() + '"  planReachTime="' + new Date(active_resource.planReachTime).toTimeString() + '">' +
            '<td class="pL">' +
            '<span st="' + active_resource.checkOut + '" class="icon sendToScreen icon1_' + active_resource.checkOut + '"></span>' +
            '<span st="' + active_resource.runState + '" class="icon sendToBus icon2_' + active_resource.runState + '"></span>' +
            '</td>' +
            '<td class="planRunTime">' +
            new Date(active_resource.planRunTime).toTimeString().slice(0, 5).replace("Inval", "") +
            '</td>' +
            '<td class="carNum">' +
            active_resource.carNum +
            '</td>' +
            '<td class="lineName">' +
            active_resource.lineName +
            '</td>' +
            '<td class="planReachTime">' +
            new Date(active_resource.planReachTime).toTimeString().slice(0, 5).replace("Inval", "") +
            '</td>' +
            '<td class="pR stopTime">' +
            active_resource.stopTime +
            '</td>' +
            '</tr>';

        var obj_list = content_tb_obj.find("tr.point");
        if (obj_list.length == 0) {
            content_tb_obj.append(obj_str);
            return;
        }
        for (var i = 0, L = obj_list.length; i < L; i++) {
            var tr_obj = obj_list[i];
            var planRunTime = tr_obj.getAttribute("planRunTime");
            var b_pid = tr_obj.getAttribute("pid");
            if (planRunTime > (new Date(active_resource.planRunTime).getTime())) {
                // tr_obj.before(obj_str);
                content_tb_obj.find("tr[pid=" + b_pid + "]").before(obj_str);
                break;
            }
        }

        if ($(".bus_transit[direction=" + active_resource.direction + "] .content_tb tr[pid=" + active_resource.id + "]").length == 0) {
            content_tb_obj.append(obj_str);
        }
        return false;
    }

    if (obj.attr('direction') != active_resource.direction) {
        obj.remove();
        return false;
    }

    // 司机签到状态
    if (active_resource.checkOut != undefined) {
        if (active_resource.checkOut == 1) {
            obj.find(".checkOut").addClass('icon1_1').removeClass("icon1_0");
        } else {
            obj.find(".checkOut").removeClass('icon1_1').addClass("icon1_0");
        }
    }

    // 车辆在线状态
    if (active_resource.runState != undefined){
        if (active_resource.runState == 1){
            obj.find(".runState").addClass('icon2_1').removeClass("icon2_0");
        } else {
            obj.find(".runState").removeClass('icon2_1').addClass("icon2_0");
        }
    }

    // 计划到达时间
    if (active_resource.planRunTime != undefined) {
        obj.find(".planRunTime").html(new Date(active_resource.planRunTime).toTimeString().slice(0, 5));
    }

    // 车辆
    if (active_resource.carNum != undefined) {
        obj.find(".carNum").html(active_resource.carNum);
    }

    // 线路
    if (active_resource.lineName != undefined) {
        obj.find(".lineName").html(active_resource.lineName);
    }

    // 回场时间
    if (active_resource.planReachTime != undefined) {
        obj.find(".planReachTime").html(new Date(active_resource.planReachTime).toTimeString().slice(0, 5));
    }

    // 停车
    if (active_resource.stopTime != undefined) {
        obj.find(".stopTime").html(active_resource.stopTime);
    }
}