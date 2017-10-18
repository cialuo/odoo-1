/**
 * Created by Administrator on 2017/8/5.
 */

var websocket = null;

//判断当前浏览器是否支持WebSocket
if ('WebSocket' in window) {
    // websocket = new SockJS("http://127.0.0.1:8769/wstest?userId=45454");
    // websocket = new WebSocket("ws://202.104.136.228:8085/dispatch-websocket/websocket?userId=2222&token=55e1da6f0fe34f3a98a1faac5b939b68");
    websocket = new WebSocket(SOCKET_URL + "/Dsp_SocketService/websocket?userId=2222&token=55e1da6f0fe34f3a98a1faac5b939b68");
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
    //  链接成功后，订阅打开页面需要的模块
    var package = {
        type: 2000,
        controlId: CONTROLLERID,
        open_modules: ["line_message", "line_online", "line_park", "abnormal", "passenger_flow"]
    };
    websocket.send(JSON.stringify(package));
}

//接收到消息的回调方法
websocket.onmessage = function (event) {
    var eventObj = JSON.parse(event.data);
    var modelName = eventObj.moduleName;
    var controllerId = eventObj.controllerId;
    var controllerObj = $(".controller_" + controllerId);
    var eventData = eventObj.data;
    console.log(eventObj);
    //由于车辆上下行计划，车场，在途数据来源于restful，这里只会收到update的推送，由于要做些简单处理，所以在这里直接触发展示
    // linePlanParkOnlineModel_display(controllerObj);

    if (modelName == "line_message") {
        use_odoo_model(event, "line_message");
        if (eventObj.type == "1044") {
            vehicle_drop(controllerObj, eventData);
        }
    } else if (modelName == "passenger_flow") {
        //客流与运力组件
        use_odoo_model(event, "passenger_flow");
    } else if (modelName == "人力资源状态") {

    } else if (modelName == "bus_resource") {
        line_resource(controllerObj, eventData);
    }
    else if (modelName == "bus_real_state") {
        busRealStateModel_socket_fn(controllerObj, eventData);
        line_car_src_real_state($(".controller_" + controllerId), eventObj.data);
    }
    else if (modelName == "passenger_delay") {
        passengerDelayModel_socket_fn(controllerObj, eventData);
    } else if ($.inArray(modelName, ["line_plan", "line_park", "line_online"]) != -1) {
        update_linePlanParkOnlineModel_socket_fn(controllerObj, eventData, modelName);
    } else if (modelName == "消息") {
        // console.log('10');
    } else if (modelName == "abnormal") {
        absnormal_del(controllerObj, eventData);
        use_odoo_model(event, "abnormal");
        line_car_src_on_line(controllerObj, eventObj);
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
//监听窗口链接更改时，主动去关闭websocket连接，防止连接还没断开就关闭窗口，server端会抛异常
window.onhashchange = function () {
    if ($('body').find('.back_style').length > 0) {
        $('body').find('.o_content').css('overflow', 'hidden');
    } else {
        $('body').find('.o_content').css('overflow', 'auto');
    }
    websocket.close();
}

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
        dom.find('tr[src_id=' + bus_no + ']').find('.line_src_full_load_rate').html(data_list.full_load_rate + '%');
        // 时速
        dom.find('tr[src_id=' + bus_no + ']').find('.line_src_speed').html(data_list.speed);
        // 能源剩余里程
        // dom.find('tr[src_id=' + bus_no + ']').find('.line_src_residual_clearance').html(data_list.residual_clearance);
    }
}

function line_resource(controllerObj, data_list) {
    var dom = controllerObj.find('.bus_src_config[line_id=' + data_list.line_id + ']');
    // 通过lineid以及资源id拿到信息
    if (dom.length > 0) {
        //遍历车辆资源新增的数据
        var theid = data_list.id;
        var tr_num = $('.table_bus_num').find('tr[src_id=' + theid + ']');
        if (data_list.planRunTime != undefined) {
            dom.find('tr[src_id=' + theid + ']').find('.line_src_next_trip_time').html(data_list.planRunTime.split(' ')[1]);
        }
        if (data_list.realReachTime != undefined) {
            dom.find('tr[src_id=' + theid + ']').find('.line_src_return_time').html(data_list.realReachTime.split(' ')[1]);
        }
        if (tr_num.find('.line_src_sinal_status').html() == '异常') {
            tr_num.find('.line_src_sinal_status').addClass('towarn');
            tr_num.find('.line_src_onBoardId').addClass('towarn');
        } else {
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
        if (data_list.packageType == 1003) {
            vehicle_drop(controllerObj, data_list);
        }
        var timer_carousel = sessionStorage.getItem('timer' + data_list.line_id);
        clearInterval(timer_carousel);
        dom.find('.carousel_content').addClass('abnormal_active');
        sessionStorage.removeItem('timer' + data_list.line_id);
        //信号在线掉线处理
    }
}

// 车辆掉线, 在线
function vehicle_drop(controllerObj, dataObj) {
    var dom = controllerObj.find(".linePlanParkOnlineModel_" + dataObj.line_id);
    if (dom.length > 0) {
        var abnormal_description = dataObj.abnormal_description;
        var vehicle = dom.find(".yard_box .content_tb tr[pid=" + abnormal_description.car_id + "]");
        if (vehicle.length > 0) {
            // if (dataObj.status != 0) {
            if (dataObj.packageType == 1044) {
                vehicle.find(".runState").attr('st', dataObj.status).removeClass("icon2_0").addClass("icon2_1");
                return false;
            }
            vehicle.find(".runState").attr('st', dataObj.status).removeClass("icon2_1").addClass("icon2_0");
        }
    }
}

// 车辆实时状态模块
function busRealStateModel_socket_fn(controllerObj, dataObj) {
    console.log(dataObj);
    // var dom = controllerObj.find(".busRealStateModel_" + dataObj.line_no + "_" + dataObj.bus_no);
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
            busRealStateModel_map(mapDom[0], dataObj);
        } else if (chartDom.length > 0) {
            socket_load.remove();
            chartDom.removeClass("hide_model");
            busRealStateModel_chart(chartDom[0], dataObj);
        }
    }
}

// 车辆实时状态模块-地理位置
function busRealStateModel_map(dom, gps) {
    if (!gps.latitude) {
        return false;
    }

    var new_gps = CONVERSIONS_GPS.gcj_encrypt(gps.latitude, gps.longitude);

    if (socket_model_api_obj.busRealStateModel_marker) {
        socket_model_api_obj.busRealStateModel_marker.setPosition(new AMap.LngLat(gps.latitude, gps.longitude));
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
function busRealStateModel_chart(dom, dataObj) {
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

// 站点实时状态模块
function passengerDelayModel_socket_fn(controllerObj, dataObj) {
    console.log(dataObj);
    if (dataObj.packageType == 1033) {
        var dom = controllerObj.find(".passengerDelayModel_" + dataObj.lineId + "_" + dataObj.stationId);
        if (dom.length > 0) {
            var trendObj = dom.find(".trend_chart_single");
            var echartData = dataObj.data;
            passengerDelayModel_socket_set(trendObj, echartData);
        }
    } else {
        var dom = controllerObj.find(".passengerDelayModel[siteId=" + dataObj.stationId + "]");
        if (dom.length > 0) {
            trendObj = dom.find(".trend_chart_summary");
            controllerObj.find(".top_title .mR10").html(dataObj.allLineId);
            echartData = dataObj.dataList;
            passengerDelayModel_socket_set(trendObj, echartData);
        }
    }
}

function passengerDelayModel_socket_set(trendObj, echartData) {
    var currentData = echartData[1];
    var trend_chart_map = trendObj.find(".trend_chart_map");
    var map_botton_info = trendObj.find(".map_botton_info");
    map_botton_info.find("li:eq(0) span").html(currentData.station_lag_passengers);
    map_botton_info.find("li:eq(1) span").html(currentData.down_passengers);
    map_botton_info.find("li:eq(2) span").html(currentData.up_passengers);
    var options = passengerDelayModel_get_echart_option(echartData);
    var myChart = echarts.init(trend_chart_map[0]);
    myChart.setOption(options);
}

// 站点实时状态模块--获取站点图表的option
function passengerDelayModel_get_echart_option(ehartData) {
    var station_lag_passengers_list = [],
        down_passengers_list = [],
        up_passengers_list = [];

    for (var i = 0, l = ehartData.length; i < l; i++) {
        var edata = ehartData[i];
        if (!edata.station_lag_passengers) {
            edata.station_lag_passengers = "";
        }
        if (!edata.down_passengers) {
            edata.down_passengers = "";
        }
        if (!edata.up_passengers) {
            edata.up_passengers = "";
        }
        station_lag_passengers_list.push(edata.station_lag_passengers);
        down_passengers_list.push(edata.down_passengers);
        up_passengers_list.push(edata.up_passengers);
    }
    var option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                show: true,
                type: 'cross',
                lineStyle: {
                    type: 'dashed',
                    width: 1
                }
            },
            formatter: function (params) {
                var hoverTip = '';
                for (var i = 0; i < params.length; i++) {
                    var htip = params[i];
                    if (i === 0) {
                        if (htip.axisValue < 0) {
                            hoverTip = '提前' + Math.abs(htip.axisValue) + '分钟<br/>';
                        } else if (htip.axisValue === 0) {
                            hoverTip = '当前<br/>';
                        } else {
                            hoverTip = htip.axisValue + '分钟后<br/>';
                        }
                    }
                    var tip_totla = htip.seriesName + ": " + htip.value[1] + "<br/>";
                    hoverTip += tip_totla
                }
                return hoverTip;
            }
        },
        animation: false,
        grid: {
            left: '10%',
            right: '10%',
            top: '10%',
            bottom: '0',
            containLabel: true
        },
        calculable: true,
        xAxis: [{
            type: 'value',
            min: -30,
            max: 120,
            axisLabel: {
                formatter: function (value) {
                    if (value == 0) {
                        return '当前';
                    }
                    if (value == 60) {
                        return '1h';
                    }
                    if (value == 120) {
                        return '2h'
                    }
                },
                textStyle: {
                    color: "#fff"
                }
            },
            boundaryGap: '',
            axisTick: {inside: true},
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
        }],
        yAxis: [{
            type: 'value',
            axisLine: {
                lineStyle: {
                    color: '#454c6c',
                }
            },
            axisTick: {show: false},
            axisLabel: {
                show: false
            },
            splitLine: {
                lineStyle: {
                    color: ['#454c6c']
                }
            }
        }],
        series: [
            {
                name: '滞站候车',
                type: 'line',
                symbolSize: 1,
                data: [
                    [-30, station_lag_passengers_list[0]],
                    // [-15, ""],
                    [0, station_lag_passengers_list[1]],
                    // [15, ""],
                    // [30, ""],
                    // [45, ""],
                    [60, station_lag_passengers_list[2]],
                    // [75, ""],
                    // [90, ""],
                    // [105, ""],
                    [120, station_lag_passengers_list[3]]
                ],
                lineStyle: {
                    normal: {
                        width: 1,
                        color: "#f89e93"
                    }
                },
                markLine: {
                    symbol: ['', 'circle'],
                    label: {
                        normal: {
                            position: "start"
                        }
                    },
                    data: [{
                        xAxis: 0,
                        symbol: 'circle',
                        symbolSize: [0, 0],
                        lineStyle: {
                            normal: {
                                type: 'solid',
                                color: '#fff'
                            }
                        },
                        label: {
                            normal: {
                                show: false
                            }
                        }
                    },
                    ]
                },
            },
            {
                name: '0.5h上车',
                type: 'line',
                symbolSize: 1,
                data: [
                    [-30, up_passengers_list[0]],
                    // [-15, ""],
                    [0, up_passengers_list[1]],
                    // [15, ""],
                    // [30, ""],
                    // [45, ""],
                    [60, up_passengers_list[2]],
                    // [75, ""],
                    // [90, ""],
                    // [105, ""],
                    [120, up_passengers_list[3]]
                ],
                lineStyle: {
                    normal: {
                        width: 1,
                        color: "#5093e1"
                    }
                }
            },
            {
                name: '0.5h下车',
                type: 'line',
                symbolSize: 1,
                data: [
                    [-30, down_passengers_list[0]],
                    // [-15, ""],
                    [0, down_passengers_list[1]],
                    // [15, ""],
                    // [30, ""],
                    // [45, ""],
                    [60, down_passengers_list[2]],
                    // [75, ""],
                    // [90, ""],
                    // [105, ""],
                    [120, down_passengers_list[3]]
                ],
                lineStyle: {
                    normal: {
                        width: 1,
                        color: "#ffd276"
                    }
                }
            },
        ]
    }
    return option;
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
            update_linePlan(controllerObj, dataObj);
        } else {
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
            // 合并
            var new_resource = extend_obj_fn(active_resource, dataObj);

            var typeModel = new_resource.inField == 1 ? "bus_yard" : "bus_transit"
            var content_tb_obj = controllerObj.find("." + typeModel + "[direction=" + new_resource.direction + "] .content_tb");
            var active_obj = content_tb_obj.find("tr[pid=" + new_resource.id + "]");

            if (typeModel == "bus_yard") {
                update_linePark(active_obj, content_tb_obj, new_resource, dataObj);
            } else {
                update_busTransit(active_obj, content_tb_obj, new_resource, dataObj);
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
            '<tr class="point" pid="' + set_op.id + '" direction="' + dataObj.direction + '" planRunTime="' + new Date(set_op.planRunTime).getTime() + '">' +
            '<td class="pL">' +
            '<span st="' + dataObj.sendToScreen + '" class="icon sendToScreen icon_' + dataObj.sendToScreen + '"></span>' +
            '<span st="' + dataObj.sendToBus + '" class="icon sendToBus icon_' + dataObj.sendToBus + '"></span>' +
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

    if (typeof dataObj.direction != undefined && active_tr_obj.attr('direction') != dataObj.direction) {
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
            active_tr_obj.find(".sendToScreen").attr('st', 1).addClass('icon_1').removeClass('icon_0').removeClass('icon_2');
        } else if (dataObj.sendToScreen == 2) {
            active_tr_obj.find(".sendToScreen").attr('st', 2).addClass('icon_2').removeClass('icon_0').removeClass('icon_1');
        } else {
            active_tr_obj.find(".sendToScreen").attr('st', 0).addClass('icon_0').removeClass('icon_1').removeClass('icon_2');
        }
    }

    // 发送计划到车辆状态
    if (dataObj.sendToBus != undefined) {
        if (dataObj.sendToBus == 1) {
            active_tr_obj.find(".sendToBus").attr('st', 1).addClass('icon_1').removeClass('icon_0').removeClass('icon_2');
        } else if (dataObj.sendToBus == 2) {
            active_tr_obj.find(".sendToBus").attr('st', 2).addClass('icon_2').removeClass('icon_0').removeClass('icon_1');
        } else {
            active_tr_obj.find(".sendToBus").attr('st', 0).addClass('icon_0').removeClass('icon_1').removeClass('icon_2');
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
        active_tr_obj.find(".driverName").html(dataObj.driverName);
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

    update_linePlanParkOnlineModel_load_fn();
}

// 车场更新
function update_linePark(active_obj, content_tb_obj, new_resource, dataObj) {
    if (active_obj.length == 0) {
        // 没有则为新增,需按照计划发车时间先后插入
        add_linePark(content_tb_obj, new_resource);
        return false;
    }

    if (dataObj.carStateId == 2008) {
        active_obj.remove();
    }

    // 司机签到状态
    if (typeof dataObj.checkOut != "undefined") {
        if (dataObj.checkOut == 1) {
            active_obj.find(".checkOut").attr('st', dataObj.checkOut).addClass('icon1_1').removeClass("icon1_0");
        } else {
            active_obj.find(".checkOut").attr('st', dataObj.checkOut).addClass("icon1_0").removeClass('icon1_1');
        }
    }

    // 车辆在线状态
    if (typeof dataObj.runState != "undefined") {
        if (dataObj.runState == 1) {
            active_obj.find(".runState").attr('st', dataObj.runState).addClass('icon2_1').removeClass("icon2_0");
        } else {
            active_obj.find(".runState").attr('st', dataObj.runState).addClass("icon2_0").removeClass('icon2_1');
        }
    }

    // 异常状态更新
    if (typeof dataObj.carStateId != "undefined") {
        var class_name = "icon carStateIdIcon carStateIdIcon_" + dataObj.carStateId;
        if (dataObj.carStateId == 0) {
            class_name += " disNoneIcon";
        }
        active_obj.find(".carStateIdIcon").attr("st", dataObj.carStateId).removeClass().addClass(class_name);
    }

    // 进场任务更新
    if (typeof dataObj.task != "undefined") {
        var class_name = "icon taskIcon";
        if ($.inArray(dataObj.task, ['1001', '1002', '1003', '1004', '1005', '1006', '1012']) == -1) {
            class_name += " disNoneIcon";
        }
        active_obj.find(".taskIcon").attr("st", dataObj.task).removeClass().addClass(class_name);
    }

    // 计划到达时间
    if (dataObj.planRunTime) {
        active_obj.find(".planRunTime").html(new Date(dataObj.planRunTime).toTimeString().slice(0, 5));
    }


    // 车辆
    if (dataObj.carNum) {
        active_obj.find(".carNum").html(dataObj.carNum);
    }

    // 线路
    if (dataObj.lineName) {
        active_obj.find(".lineName").html(dataObj.lineName);
    }

    // 回场时间
    if (dataObj.realReachTime) {
        active_obj.find(".realReachTime").html(new Date(dataObj.realReachTime).toTimeString().slice(0, 5));
    }

    // // 停车
    // if (dataObj.stopTime) {
    //     active_obj.find(".stopTime").html(dataObj.stopTime);
    // }

    update_linePlanParkOnlineModel_load_fn();
}

// 在途更新
function update_busTransit(active_obj, content_tb_obj, new_resource, dataObj) {
    if (active_obj.length == 0) {
        // 没有则为新增,需按照计划发车时间先后插入
        add_busTransit(content_tb_obj, new_resource);
        return false;
    }

    // 司机签到状态
    if (typeof dataObj.checkOut != "undefined") {
        if (dataObj.checkOut == 1) {
            active_obj.find(".checkOut").attr('st', dataObj.checkOut).addClass('icon1_1').removeClass("icon1_0");
        } else {
            active_obj.find(".checkOut").attr('st', dataObj.checkOut).addClass("icon1_0").removeClass('icon1_1');
        }
    }

    // 车辆在线状态
    if (typeof dataObj.runState != "undefined") {
        if (dataObj.runState == 1) {
            active_obj.find(".runState").attr('st', dataObj.runState).addClass('icon2_1').removeClass("icon2_0");
        } else {
            active_obj.find(".runState").attr('st', dataObj.runState).addClass("icon2_0").removeClass('icon2_1');
        }
    }

    // 异常状态更新
    if (typeof dataObj.carStateId != "undefined") {
        var class_name = "icon carStateIdIcon carStateIdIcon_" + dataObj.carStateId;
        if (dataObj.carStateId == 0) {
            class_name += " disNoneIcon";
        }
        active_obj.find(".carStateIdIcon").attr("st", dataObj.carStateId).removeClass().addClass(class_name);
    }

    // 进场任务更新
    if (typeof dataObj.task != "undefined") {
        var class_name = "icon taskIcon";
        if ($.inArray(dataObj.task, ['1001', '1002', '1003', '1004', '1005', '1006', '1012']) == -1) {
            class_name += " disNoneIcon";
        }
        active_obj.find(".taskIcon").attr("st", dataObj.task).removeClass().addClass(class_name);
    }

    // 计划到达时间
    if (dataObj.planRunTime) {
        active_obj.find(".planRunTime").html(new Date(dataObj.planRunTime).toTimeString().slice(0, 5));
    }

    // 车辆
    if (dataObj.carNum) {
        active_obj.find(".carNum").html(dataObj.carNum);
    }

    // 线路
    if (dataObj.lineName) {
        active_obj.find(".lineName").html(dataObj.lineName);
    }

    // 回场时间
    if (dataObj.planReachTime) {
        active_obj.find(".planReachTime").html(new Date(dataObj.planReachTime).toTimeString().slice(0, 5));
    }

    // 停车
    if (dataObj.stopTime) {
        active_obj.find(".stopTime").html(dataObj.stopTime);
    }

    update_linePlanParkOnlineModel_load_fn();
}

function update_linePlanParkOnlineModel_load_fn() {
    $(".linePlanParkOnlineModel .bus_plan").find(".content_tb .icon").hover(function () {
        var st = $(this).attr("st");
        var txt = "";
        if (st == 0) {
            txt = "未发送";
        } else if (st == 1) {
            txt = "已发送未处理";
        } else {
            txt = "已发送已处理";
        }
        self.layer_f_index = layer.tips(txt, this);
    }, function () {
        layer.close(self.layer_f_index);
    });


    $(".linePlanParkOnlineModel .bus_yard").find(".content_tb .icon").hover(function () {
        var txt = "";
        var st = $(this).attr("st");
        if ($(this).hasClass("checkOut")) {
            txt = (st == 1) ? '已签到' : '未签到'
        } else if ($(this).hasClass("runState")) {
            txt = (st == 1) ? '在线' : '未在线'
        } else if ($(this).hasClass("carStateIdIcon")) {
            if (st == 1001) {
                txt = "正常";
            } else if (st == 2003) {
                txt = "休息";
            } else if (st == 1002) {
                txt = "故障";
            } else if (st == 2006) {
                txt = "保养";
            } else if (st == 2010) {
                txt = "空放";
            } else if (st == 2005) {
                txt = "加油";
            } else {
                txt = "其它";
            }
        } else if ($(this).hasClass("taskIcon")) {
            if (st == 1001) {
                txt = "进场包车开始";
            } else if (st == 1002) {
                txt = "进场包车结束";
            } else if (st == 1003) {
                txt = "进场加油开始";
            } else if (st == 1004) {
                txt = "进场加油结束";
            } else if (st == 1005) {
                txt = "进场修车开始";
            } else if (st == 1006) {
                txt = "进场修车结束";
            } else if (st == 1012) {
                txt = "进场下班，变机动";
            }
        }
        self.layer_f_index = layer.tips(txt, this);
    }, function () {
        layer.close(self.layer_f_index);
    });
}

function add_linePark(content_tb_obj, new_resource) {
    var carState_class = "disNoneIcon",
        task_class = "disNoneIcon";
    if (new_resource.carStateId != 0) {
        carState_class = "";
    }

    if ($.inArray(new_resource.task, ['1001', '1002', '1003', '1004', '1005', '1006', '1012']) != -1) {
        task_class = "";
    }

    var obj_str =
        '<tr class="point" pid="' + new_resource.id + '" direction="' + new_resource.direction + '" planRunTime="' + new Date(new_resource.planRunTime).getTime() + '" planReachTime="' + new Date(new_resource.realReachTime).getTime() + '">' +
        '<td class="pL">' +
        '<span st="' + new_resource.checkOut + '" class="icon sendToScreen icon1_' + new_resource.checkOut + '"></span>' +
        '<span st="' + new_resource.runState + '" class="icon sendToBus icon2_' + new_resource.runState + '"></span>' +
        '<span st="' + new_resource.carStateId + '" class="icon carStateIdIcon ' + carState_class + ' carStateIdIcon_' + new_resource.carStateId + '"></span>' +
        '<span st="' + new_resource.task + '" class="icon ' + task_class + ' taskIcon"></span>' +
        '</td>' +
        '<td class="planRunTime">' +
        new Date(new_resource.planRunTime).toTimeString().slice(0, 5).replace("Inval", "") +
        '</td>' +
        '<td class="carNum">' +
        new_resource.carNum +
        '</td>' +
        '<td class="lineName">' +
        new_resource.lineName +
        '</td>' +
        '<td class="realReachTime">' +
        new Date(new_resource.realReachTime).toTimeString().slice(0, 5).replace("Inval", "") +
        '</td>' +
        // '<td class="pR stopTime">' +
        // new_resource.stopTime +
        // '</td>' +
        '</tr>';

    var obj_list = content_tb_obj.find("tr.point");
    if (obj_list.length == 0) {
        update_tr_delete(new_resource.id);
        content_tb_obj.append(obj_str);
        return;
    }
    for (var i = 0, L = obj_list.length; i < L; i++) {
        var tr_obj = obj_list[i];
        var planRunTime = tr_obj.getAttribute("planRunTime");
        var b_pid = tr_obj.getAttribute("pid");
        if (planRunTime > (new Date(new_resource.planRunTime).getTime())) {
            update_tr_delete(new_resource.id);
            content_tb_obj.find("tr[pid=" + b_pid + "]").before(obj_str);
            break;
        }
    }

    if (content_tb_obj.find("tr[pid=" + new_resource.id + "]").length == 0) {
        update_tr_delete(new_resource.id);
        content_tb_obj.append(obj_str);
    }
}

function add_busTransit(content_tb_obj, new_resource) {
    var carState_class = "disNoneIcon",
        task_class = "disNoneIcon";
    if (new_resource.carStateId != 0) {
        carState_class = "";
    }

    if ($.inArray(new_resource.task, ['1001', '1002', '1003', '1004', '1005', '1006', '1012']) != -1) {
        task_class = "";
    }
    var obj_str =
        '<tr class="point" pid="' + new_resource.id + '" direction="' + new_resource.direction + '" planRunTime="' + new Date(new_resource.planRunTime).getTime() + '"  planReachTime="' + new Date(new_resource.planReachTime).getTime() + '">' +
        '<td class="pL">' +
        '<span st="' + new_resource.checkOut + '" class="icon sendToScreen icon1_' + new_resource.checkOut + '"></span>' +
        '<span st="' + new_resource.runState + '" class="icon sendToBus icon2_' + new_resource.runState + '"></span>' +
        '<span st="' + new_resource.carStateId + '" class="icon carStateIdIcon ' + carState_class + ' carStateIdIcon_' + new_resource.carStateId + '"></span>' +
        '<span st="' + new_resource.task + '" class="icon ' + task_class + ' taskIcon"></span>' +
        '</td>' +
        '<td class="planRunTime">' +
        new Date(new_resource.planRunTime).toTimeString().slice(0, 5).replace("Inval", "") +
        '</td>' +
        '<td class="carNum">' +
        new_resource.carNum +
        '</td>' +
        '<td class="lineName">' +
        new_resource.lineName +
        '</td>' +
        '<td class="planReachTime">' +
        new Date(new_resource.planReachTime).toTimeString().slice(0, 5).replace("Inval", "") +
        '</td>' +
        '<td class="stopTime">' +
        new_resource.stopTime +
        '</td>' +
        '</tr>';

    var obj_list = content_tb_obj.find("tr.point");
    if (obj_list.length == 0) {
        update_tr_delete(new_resource.id);
        content_tb_obj.append(obj_str);
        return;
    }
    for (var i = 0, L = obj_list.length; i < L; i++) {
        var tr_obj = obj_list[i];
        var planRunTime = tr_obj.getAttribute("planRunTime");
        var b_pid = tr_obj.getAttribute("pid");
        if (planRunTime > (new Date(new_resource.planRunTime).getTime())) {
            update_tr_delete(new_resource.id);
            content_tb_obj.find("tr[pid=" + b_pid + "]").before(obj_str);
            break;
        }
    }
    if (content_tb_obj.find("tr[pid=" + new_resource.id + "]").length == 0) {
        update_tr_delete(new_resource.id);
        content_tb_obj.append(obj_str);
    }
}

// 组合
function extend_obj_fn(a, b) {
    var c = new Object();
    var d = new Object();
    $.extend(c, a);
    $.extend(d, b);
    $.extend(c, d);
    return c;
}

// 删除
function update_tr_delete(id) {
    $(".plan_display").find(".content_tb tr[pid=" + id + "]").remove();
    update_linePlanParkOnlineModel_load_fn();
}