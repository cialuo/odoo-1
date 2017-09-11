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
    console.log(eventObj)
    var controllerId = eventObj.controllerId;

    //由于车辆上下行计划，车场，在途数据来源于restful，这里只会收到update的推送，由于要做些简单处理，所以在这里直接触发展示
    linePlanParkOnlineModel_display($(".controller_" + controllerId));

    if (modelName == "line_message") {
        use_odoo_model(event,"line_message");
    } else if (modelName == "passenger_flow") {
        //客流与运力组件
        use_odoo_model(event,"passenger_flow");
        passenger_flow_capacity($(".controller_" + controllerId), eventObj.data);
    } else if (modelName == "人力资源状态") {
    }
    else if (modelName == "bus_real_state") {
        busRealStateModel_socket_fn($(".controller_" + controllerId), eventObj.data);
    }
    else if (modelName == "passenger_delay") {
        passengerDelayModel_socket_fn($(".controller_" + controllerId), eventObj.data);
    } else if ($.inArray(modelName, ["line_plan", "bus_resource"]) != -1) {
        if (modelName != "line_plan") {
            line_resource($(".controller_" + controllerId), eventObj.data);
        }
        update_linePlanParkOnlineModel_socket_fn($(".controller_" + controllerId), eventObj.data, modelName);
    } else if (modelName == "线路车场") {
        // console.log('8');
    } else if (modelName == "线路在途") {
        // console.log('9');
    } else if (modelName == "消息") {
        // console.log('10');
    } else if (modelName == "abnormal") {
        absnormal_del($(".controller_" + controllerId), eventObj.data);
        use_odoo_model(event,"abnormal");
        line_car_src_on_line($(".controller_" + controllerId), eventObj);
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

function use_odoo_model(event,model_name) {
    for (socket_model in socket_model_info) {
        var socket_model_obj = socket_model_info[socket_model];
        if(socket_model.split("__")[0] == model_name){
            socket_model_obj.fn(event.data, socket_model_obj.arg);
        }
    }
}

// 在线掉线包
function line_car_src_on_line(controllerObj, data_list) {
    var dom = controllerObj.find('.bus_src_config[line_id=1]');
    // 根据车辆id去进行处理
    if (dom.length > 0 && data_list.type == 1003) {
        dom.find('.line_src_sinal_status').html(data_list.data.status);
    }
}

//根据车辆实时状态修改车辆资源
function line_car_src_real_state(controllerObj, data_list) {
    var dom = controllerObj.find('.bus_src_config[line_id=1]');
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
    var dom = controllerObj.find('.bus_src_config[line_id=1]');
    // 通过lineid以及资源id拿到信息
    if (dom.length > 0) {
        //遍历车辆资源新增的数据
        var theid = data_list.id;
        var tr_num = $('.table_bus_num').find('tr[src_id=' + theid + ']');
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
    var dom = controllerObj.find('.updown_line_table[line_id=1]');
    var dom_singal = controllerObj.find('.dispatch_desktop[line_id=1]');
    if (dom.length > 0) {
        dom.find('.no_absnormal').show().siblings().hide();
        $('body').find('.absnormal_diaodu .absnormal_type p').html(data_list.abnormal_description.bus_no);
        $('body').find('.absnormal_diaodu .absnormal_sug p').html(data_list.suggest);
        dom.addClass('warn').find('.passenger_flow_list').eq(0).find('.abs_info').append($('body').find('.absnormal_diaodu').html());
        var timer_carousel = sessionStorage.getItem('timer1');
        clearInterval(timer_carousel);
        dom.find('.carousel_content').css({left: 0});
        //信号在线掉线处理
        if (data_list.packageType == "1003") {
            dom_singal.find('.singalIn span').html(parseInt(dom_singal.find('.singalIn span').html()) - 1);
            dom_singal.find('.singalOut span').html(parseInt(dom_singal.find('.singalOut span').html()) + 1);
        }

    }
}

// function absnormal_del(controllerObj, data_list) {
//     if (controllerObj.find('.updown_line_table[line_id=1]').length > 0) {
//         if (data_list[0].substring(78, 79) > 3) {
//             controllerObj.find('.updown_line_table[line_id=1]').find('.no_absnormal').show().siblings().hide();
//             controllerObj.find('.updown_line_table[line_id=1]').find('.passenger_flow_list .absnormal_type  p').html('有危险');
//             controllerObj.find('.updown_line_table[line_id=1]').addClass('warn');
//             var timer_carousel = sessionStorage.getItem('timer1');
//             clearInterval(timer_carousel);
//             controllerObj.find('.updown_line_table[line_id=1]').find('.carousel_content').css({left: 0});
//         }
//     }
//     if (controllerObj.find('.updown_line_table[line_id=2]').length > 0) {
//         if (data_list[0].substring(78, 79) > 3) {
//             controllerObj.find('.updown_line_table[line_id=2]').find('.no_absnormal').show().siblings().hide();
//             var timer_carouse2 = sessionStorage.getItem('timer2');
//             clearInterval(timer_carouse2);
//             controllerObj.find('.updown_line_table[line_id=2]').find('.carousel_content').css({left: 0});
//         }
//     }
// }

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
    var dom = controllerObj.find(".busRealStateModel_5_1");
    if (dom.length > 0) {
        var vehicleInformationObj = dom.find(".popupContent .vehicleInformation");
        var carReportObj = dom.find(".popupContent .carReport");
        var lineInfo = dom.find(".lineInfo");
        vehicleInformationObj.find(".license_number").html(dataObj.license_number);
        vehicleInformationObj.find(".license_plate").html(dataObj.license_plate);
        vehicleInformationObj.find(".driver").html(dataObj.driver);
        vehicleInformationObj.find(".crew").html(dataObj.conductor);
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
        lineInfo.find(".lineRoad").html('18' + '路')
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

// 站点实时状态模块
function passengerDelayModel_socket_fn(controllerObj, data_list) {
    var dom = controllerObj.find(".passengerDelayModel");
    if (dom.length > 0) {
        var passengerDelayModel_set = JSON.parse(sessionStorage.getItem("passengerDelayModel_set"));
        layer.close(passengerDelayModel_set.layer_index);
        dom.removeClass('hide_model');
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
function update_linePlanParkOnlineModel_socket_fn(controllerObj, dataObj, modelName) {
    var dom = controllerObj.find(".linePlanParkOnlineModel_1");
    if (dom.length > 0) {
        if (modelName == "line_plan") {
            var tr_obj_list = controllerObj.find(".bus_plan[direction=" + dataObj.direction + "] .content_tb tr.point");
            var tr_obj = controllerObj.find(".bus_plan[direction=" + dataObj.direction + "]").find(".content_tb tr[pid=" + dataObj.id + "]");
            update_linePlan(tr_obj, tr_obj_list, dataObj);
            // 模块划分更改之前的丢弃
            // }else if (modelName == "line_park"){
            //     var tr_obj_list = controllerObj.find(".bus_yard[direction="+dataObj.direction+"] .content_tb tr.point");
            //     var tr_obj = controllerObj.find(".bus_yard[direction="+dataObj.direction+"]").find(".content_tb tr[pid="+dataObj.id+"]");
            //     update_linePark(tr_obj, dataObj, tr_obj_list);
            // }else{
            //     var tr_obj_list = controllerObj.find(".bus_transit[direction="+dataObj.direction+"] .content_tb tr.point");
            //     var tr_obj = controllerObj.find(".bus_transit[direction="+dataObj.direction+"]").find(".content_tb tr[pid="+dataObj.id+"]");
            //     update_busTransit(tr_obj, dataObj, tr_obj_list);
            // }
        } else {
            // 模块合并
            update_busResource(controllerObj, dataObj);
        }
        $('.linePlanParkOnlineModel').mCustomScrollbar("update");
    }
}


// 计划更新
function update_linePlan(obj, obj_list, dataObj) {
    // 没有且计划状态非完成则为新增,需按照计划发车时间先后插入
    if (obj.length == 0) {
        if (dataObj.planState != 3) {
            var obj_str =
                '<tr class="point" pid="' + dataObj.id + '" direction="' + dataObj.direction + '" planRunTime="' + dataObj.planRunTime + '">' +
                '<td class="pL">' +
                '<span st="' + dataObj.sendToScreen + '" class="icon sendToScreen icon_' + dataObj.sendToScreen + '"></span>' +
                '<span st="' + dataObj.sendToBus + '" class="icon sendToBus icon_' + dataObj.sendToBus + '"></span>' +
                '</td>' +
                '<td class="planRunTime">' +
                new Date(dataObj.planRunTime).toTimeString().slice(0, 8) +
                '</td>' +
                '<td class="planReachTime">' +
                new Date(dataObj.planReachTime).toTimeString().slice(0, 8) +
                '</td>' +
                '<td class="selfId">' +
                dataObj.selfId +
                '</td>' +
                '<td class="driverName">' +
                dataObj.driverName +
                '</td>' +
                '<td class="pR planState">' +
                '待发' +
                '</td>' +
                '</tr>';
            for (var i = 0, L = obj_list.length; i < L; i++) {
                var tr_obj = obj_list[i];
                var planRunTime = tr_obj.getAttribute("planRunTime");
                if (planRunTime > dataObj.planRunTime) {
                    tr_obj.before(obj_str);
                    break;
                }
            }
        }
        return false;
    }

    // 已完成的计划移除
    if (dataObj.planState == 3) {
        obj.remove();
        return false;
    }

    // 发送计划到调度屏状态
    if (dataObj.sendToScreen != undefined) {
        if (dataObj.sendToScreen == 1) {
            obj.find(".sendToScreen").addClass('icon_1').removeClass('icon_0');
        } else {
            obj.find(".sendToScreen").removeClass('icon_1').addClass('icon_0');
        }
    }

    // 发送计划到车辆状态
    if (dataObj.sendToBus != undefined) {
        if (dataObj.sendToBus == 1) {
            obj.find(".sendToBus").addClass('icon_1').removeClass('icon_0');
        } else {
            obj.find(".sendToBus").removeClass('icon_1').addClass("icon_0");
        }
    }

    // 计划到达时间
    if (dataObj.planRunTime != undefined) {
        obj.find(".planRunTime").html(new Date(dataObj.planRunTime).toTimeString().slice(0, 8));
    }

    // 计划到达时间
    if (dataObj.planReachTime != undefined) {
        obj.find(".planReachTime").html(new Date(dataObj.planReachTime).toTimeString().slice(0, 8));
    }

    // 车辆
    if (dataObj.selfId != undefined) {
        obj.find(".selfId").html(dataObj.selfId);
    }

    // 司机
    if (dataObj.driverName != undefined) {
        obj.find(".driverName").html(dataObj.driverName);
    }

    // 待发状态
    if (dataObj.planState != undefined) {
        var txt = "待发";
        if (dataObj.planState == 2) {
            txt = "已完成"
        }
        obj.find(".planState").html(txt);
    }
}

// 车场在途更新
function update_busResource(controllerObj, dataObj) {
    var busResource_sectionPlanCont_list = controllerObj.find(".section_plan_cont").not(controllerObj.find(".bus_plan"));
    var active_tr = busResource_sectionPlanCont_list.find("tr[pid=" + dataObj.id + "]");
    if (dataObj.carStateId == 2008) {
        active_tr.remove();
    } else {
        if (active_tr.length > 0) {
            update_update_busResource_fn(controllerObj, dataObj, active_tr);
        } else {
            if (dataObj.direction != undefined && dataObj.inField != undefined) {
                var tr_list = controllerObj.find(".section_plan_cont[direction=" + dataObj.direction + "][inField=" + dataObj.inField + "] .content_tb tr.point");
                add_busResource(controllerObj, tr_list, dataObj)
            }
        }
    }
}

function add_busResource(controllerObj, obj_list, dataObj) {
    var td_str = '';
    if (dataObj.inField == 0) {
        td_str = '<td class="planReachTime">' + new Date(dataObj.planReachTime).toTimeString().slice(0, 8).replace('Invalid', '') + '</td>';
    } else {
        td_str = '<td class="realReachTime">' + new Date(dataObj.realReachTime).toTimeString().slice(0, 8).replace('Invalid', '') + '</td>';
    }
    var op_dict = {
        checkOut: dataObj.checkOut || "0",
        runState: dataObj.runState || "0",
        selfId: dataObj.selfId || "",
        lineName: dataObj.lineName || "",
        stopTime: dataObj.stopTime || "",
    };
    var obj_str =
        '<tr class="point" pid="' + dataObj.id + '" direction="' + dataObj.direction + '" inField' + dataObj.inField + ' planRunTime="' + dataObj.planRunTime + '">' +
        '<td class="pL">' +
        '<span st="' + op_dict.checkOut + '" class="icon sendToScreen icon1_' + op_dict.checkOut + '"></span>' +
        '<span st="' + op_dict.runState + '" class="icon sendToBus icon2_' + op_dict.runState + '"></span>' +
        '</td>' +
        '<td class="planRunTime">' +
        new Date(dataObj.planRunTime).toTimeString().slice(0, 8).replace('Invalid', '') +
        '</td>' +
        '<td class="selfId">' +
        op_dict.selfId +
        '</td>' +
        '<td class="lineName">' +
        op_dict.lineName +
        '</td>' +
        td_str +
        '<td class="pR stopTime">' +
        op_dict.stopTime +
        '</td>' +
        '</tr>';


    if (obj_list.length == 0) {
        controllerObj.find(".section_plan_cont[direction=" + dataObj.direction + "][inField=" + dataObj.inField + "] .content_tb").append(obj_str);
        return false;
    }

    // 排序规则
    // 先根据计划时间排序，如果没有计划时间则根据回场时间排序，如果两者都没有则根据车辆编号进行，前三者都没有给到，则添加末尾
    for (var i = 0; i < obj_list.length; i++) {
        var obj = obj_list[i];
        if (dataObj.planRunTime) {
            if (obj.getAttribute("planRunTime")) {
                if (obj.getAttribute("planRunTime") > dataObj.planRunTime) {
                    obj.before(obj_str);
                    break;
                }
            } else {
                obj.after(obj_str);
                break;
            }
        } else {
            if (!obj.getAttribute("planRunTime")) {
                if (dataObj.planReachTime || dataObj.realReachTime) {
                    if (obj.getAttribute('realReachTime') || obj.getAttribute('realReachTime')) {
                        var time_1 = dataObj.planReachTime || dataObj.realReachTime;
                        var time_2 = obj.getAttribute('realReachTime') || obj.getAttribute('realReachTime');
                        if (time_2 > time_1) {
                            obj.before(obj_str);
                            break;
                        }
                    } else {
                        abj.before(obj_str);
                        break;
                    }
                } else {
                    if (!(obj.getAttribute('realReachTime') || obj.getAttribute('realReachTime'))) {
                        if (dataObj.carNum) {
                            if (obj.getAttribute('carNum') > dataObj.carNum) {
                                abj.before(obj_str);
                                break;
                            }
                        }
                    }
                }
            }
        }
    }
    if (controllerObj.find(".section_plan_cont").find("tr[pid=" + dataObj.id + "]").length == 0) {
        controllerObj.find(".section_plan_cont[direction=" + dataObj.direction + "][inField=" + dataObj.inField + "] .content_tb").append(obj_str);
    }
}

function update_update_busResource_fn(controllerObj, dataObj, active_tr) {
    var ac_abj = active_tr.parents(".section_plan_cont");
    var ac_direction = ac_abj.attr("direction");
    var ac_inField = ac_abj.attr("inField");
    if (dataObj.direction != undefined && dataObj.inField != undefined) {

    } else {
        if (dataObj.direction != undefined) {

        } else if (dataObj.inField != undefined) {

        } else {

        }
    }
}

// 车场更新 模块最初定义跟后台不符合丢弃暂时保存，防止需求变更
// function update_linePark(obj, dataObj, obj_list){
//     if (obj.length == 0){
//         // 没有则为新增,需按照计划发车时间先后插入
//         var obj_str =
//             '<tr class="point" pid="'+dataObj.id+'" direction="'+dataObj.direction+'" planRunTime="'+dataObj.planRunTime+'">' +
//                 '<td class="pL">' +
//                     '<span st="'+dataObj.checkOut+'" class="icon sendToScreen icon_'+dataObj.checkOut+'"></span>' +
//                     '<span st="'+dataObj.runState+'" class="icon sendToBus icon_'+dataObj.runState+'"></span>' +
//                 '</td>' +
//                 '<td class="planRunTime">' +
//                     new Date(dataObj.planRunTime).toTimeString().slice(0,8) +
//                 '</td>' +
//                 '<td class="selfId">' +
//                     dataObj.selfId +
//                 '</td>' +
//                 '<td class="lineName">' +
//                     dataObj.lineName +
//                 '</td>' +
//                 '<td class="realReachTime">' +
//                     new Date(dataObj.realReachTime).toTimeString().slice(0,8) +
//                 '</td>' +
//                 '<td class="pR stopTime">' +
//                     dataObj.stopTime +
//                 '</td>' +
//             '</tr>';
//         for (var i=0, L=obj_list.length; i<L; i++){
//             var tr_obj  = obj_list[i];
//             var planRunTime = tr_obj.getAttribute("planRunTime");
//             if (planRunTime>dataObj.planRunTime){
//                 tr_obj.before(obj_str);
//                 break;
//             }
//         }
//         return false;
//     }

//     // 司机签到状态
//     if (dataObj.checkOut != undefined){
//         if (dataObj.checkOut == 1){
//             obj.find(".checkOut").addClass('icon1_1').removeClass("icon1_0");
//         }else{
//             obj.find(".checkOut").removeClass('icon1_1').addClass("icon1_0");    
//         }
//     }

//     // 车辆在线状态
//     if (dataObj.runState != undefined){
//         if (dataObj.runState == 0){
//             obj.find(".runState").addClass('icon2_1').removeClass("icon2_0");
//         }else{
//             obj.find(".runState").removeClass('icon2_1').addClass("icon2_0");   
//         }
//     }

//     // 计划到达时间
//     if (dataObj.planRunTime != undefined){
//         obj.find(".planRunTime").html(new Date(dataObj.planRunTime).toTimeString().slice(0,8));
//     }


//     // 车辆
//     if (dataObj.carNum != undefined){
//         obj.find(".carNum").html(dataObj.carNum);
//     }

//     // 线路
//     if (dataObj.lineName != undefined){
//         obj.find(".lineName").html(dataObj.lineName);
//     }

//     // 回场时间
//     if (dataObj.realReachTime != undefined){
//         obj.find(".realReachTime").html(new Date(dataObj.realReachTime).toTimeString().slice(0,8));
//     }

//     // 停车
//     if (dataObj.stopTime != undefined){
//         obj.find(".stopTime").html(new Date(dataObj.stopTime).toTimeString().slice(0,8));
//     }
// }


// 在途更新 模块最初定义跟后台不符合丢弃暂时保存，防止需求变更
// function update_busTransit(obj, dataObj){
//     if (obj.length == 0){
//         // 没有则为新增,需按照计划发车时间先后插入
//         var obj_str =
//             '<tr class="point" pid="'+dataObj.id+'" direction="'+dataObj.direction+'" planRunTime="'+dataObj.planRunTime+'">' +
//                 '<td class="pL">' +
//                     '<span st="'+dataObj.checkOut+'" class="icon sendToScreen icon_'+dataObj.checkOut+'"></span>' +
//                     '<span st="'+dataObj.runState+'" class="icon sendToBus icon_'+dataObj.runState+'"></span>' +
//                 '</td>' +
//                 '<td class="planRunTime">' +
//                     new Date(dataObj.planRunTime).toTimeString().slice(0,8) +
//                 '</td>' +
//                 '<td class="carNum">' +
//                     dataObj.carNum +
//                 '</td>' +
//                 '<td class="lineName">' +
//                     dataObj.lineName +
//                 '</td>' +
//                 '<td class="planReachTime">' +
//                     new Date(dataObj.planReachTime).toTimeString().slice(0,8) +
//                 '</td>' +
//                 '<td class="pR stopTime">' +
//                     dataObj.stopTime +
//                 '</td>' +
//             '</tr>';
//         for (var i=0, L=obj_list.length; i<L; i++){
//             var tr_obj  = obj_list[i];
//             var planRunTime = tr_obj.getAttribute("planRunTime");
//             if (planRunTime>dataObj.planRunTime){
//                 tr_obj.before(obj_str);
//                 break;
//             }
//         }
//         return false;
//     }

//     // 司机签到状态
//     if (dataObj.checkOut != undefined){
//         if (dataObj.checkOut == 1){
//             obj.find(".checkOut").addClass('icon1_1').removeClass("icon1_0");
//         }else{
//             obj.find(".checkOut").removeClass('icon1_1').addClass("icon1_0");
//         }
//     }

//     // 车辆在线状态
//     if (dataObj.runState != undefined){
//         if (dataObj.runState == 0){
//             obj.find(".runState").addClass('icon2_1').removeClass("icon2_0");
//         }else{
//             obj.find(".runState").removeClass('icon2_1').addClass("icon2_0");   
//         }
//     }

//     // 计划到达时间
//     if (dataObj.planRunTime != undefined){
//         obj.find(".planRunTime").html(new Date(dataObj.planRunTime).toTimeString().slice(0,8));
//     }


//     // 车辆
//     if (dataObj.carNum != undefined){
//         obj.find(".carNum").html(dataObj.carNum);
//     }

//     // 线路
//     if (dataObj.lineName != undefined){
//         obj.find(".lineName").html(dataObj.lineName);
//     }

//     // 回场时间
//     if (dataObj.planReachTime != undefined){
//         obj.find(".planReachTime").html(new Date(dataObj.planReachTime).toTimeString().slice(0,8));
//     }

//     // 停车
//     if (dataObj.stopTime != undefined){
//         obj.find(".stopTime").html(new Date(dataObj.stopTime).toTimeString().slice(0,8));
//     }
// }