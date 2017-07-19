odoo.define(function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;

    // 客流走势
    var passenger_flow = Widget.extend({
        template: "passenger_flow_template",
        events: {
            'click .express_bt': 'send_express_info',
        },
        init: function(parent, data){
            var init_data = [
                {   
                    name: "世界之窗",
                    line_car: [16],
                    data: [
                        {
                            name: "运力",
                            value: "11",
                        },
                        {
                            name: "滞站候车",
                            value: [11, 12, 15, 12, 13, 11, 11, 9, 13, 12, 11]
                        },
                        {
                            name: "0.5h上车",
                            value: [10, 9, 9, 8, 10, 10]
                        },
                        {
                            name: "0.5h下车",
                            value: [5, 6, 7, 6, 5, 8]
                        },
                    ]
                },
                {   
                    name: "",
                    line_car: [16, 23, 45, 38, 54],
                    data: [
                        {
                            name: "运力",
                            value: "11",
                        },
                        {
                            name: "滞站候车",
                            value: [11, 12, 15, 12, 13, 11, 11, 9, 13, 12, 11]
                        },
                        {
                            name: "0.5h上车",
                            value: [10, 9, 9, 8, 10, 10]
                        },
                        {
                            name: "0.5h下车",
                            value: [5, 6, 7, 6, 5, 8]
                        },
                    ]
                },
            ];
            this._super(parent);
            this.passenger_data = data.length ? data : init_data;
        },
        start: function(){
            this.trend_chart_fn();
        },
        send_express_info: function(){
            var passenger_flow_cont = this.$(".trend_chart_single .passenger_flow_cont");
            var express_train_box_obj = passenger_flow_cont.find(".express_train_box");
            var trend_chart_info_obj = passenger_flow_cont.find(".trend_chart_info");
            if (express_train_box_obj.length > 0){
                return;
            }
            trend_chart_info_obj.hide();
            new express_train(this, this.get_express_info()).appendTo(this.$(".trend_chart_single .passenger_flow_cont"));
        },
        station_fn: function(data){
            var result = [];
            for(var i=0,len=data.length;i<len;i+=3){
               result.push(data.slice(i,i+3));
            }
            return result;
        },
        get_express_info: function(){
            var data = {
                name: '世界之窗',
                arrival_time: '13:15',
                vehicle: [
                    {
                        name: '234号 粤B2C32E 司机 游鸿明 最快13:15抵达 我是机动车',
                        id: '123'
                    }
                ],
                waiting_bus: [
                    {
                        name: '234号 粤B2C32E 司机 游鸿明 最快13:15抵达 我是待班车',
                        id: '456'
                    }
                ],
                skip: '3',
                station: [
                    {name: '站点N', id: '1'},
                    {name: '站点N', id: '2'},
                    {name: '站点N', id: '3'},
                    {name: '站点N', id: '4'},
                    {name: '站点N', id: '5'},
                    {name: '站点N', id: '6'},
                    {name: '站点N', id: '7'},
                    {name: '站点N', id: '8'},
                    {name: '站点N', id: '9'},
                ]
            };
            data.station = this.station_fn(data.station);
            return data;
        },
        trend_chart_fn:  function(){
            var passenger_data = this.passenger_data
            for (var i=0,len=passenger_data.length; i<len; i++){
                var trend_chart_obj = passenger_data[i];
                if (trend_chart_obj.name){
                    new trend_chart(this, trend_chart_obj.data).appendTo(this.$(".trend_chart_single .passenger_flow_cont"));
                }else{
                    new trend_chart(this, trend_chart_obj.data).appendTo(this.$(".trend_chart_summary .passenger_flow_cont")); 
                }
            }
        }
    });
    core.action_registry.add('lty_dispatch_desktop_widget.passenger_flow', passenger_flow);

    // 客流走势图表
    var trend_chart = Widget.extend({
        template: "trend_chart_template",
        init: function(parent, data){
            this._super(parent);
            this.passenger_data = data;
        },
        start: function(){
            this.passengerMapFn();
        },
        passengerMapFn: function(){
            var dataArray = this.passenger_data;
            var option = {
                tooltip : {
                    trigger: 'axis',
                    axisPointer:{
                        show: true,
                        type : 'cross',
                        lineStyle: {
                            type : 'dashed',
                            width : 1
                        }
                    },
                    formatter:function(params){
                        var hoverTip = '';
                        for (var i=0;i<params.length;i++){
                            var htip = params[i];
                            if (i===0){
                                if (htip.axisValue<0){
                                    hoverTip = '提前'+Math.abs(htip.axisValue)+'分钟<br/>';
                                }else if(htip.axisValue===0){
                                    hoverTip = '当前<br/>';
                                }else{
                                    hoverTip = htip.axisValue+'分钟后<br/>';
                                }
                            }
                            var tip_totla = htip.seriesName+": "+htip.value[1] + "<br/>";
                            hoverTip += tip_totla
                        }
                        return hoverTip;
                    }
                },
                grid: {
                    left: '3%',
                    right: '10%',
                    top: '10%',
                    bottom: '10%',
                    containLabel: true
                },
                legend: {
                    // data:['运力','滞站候车','0.5h上车','0.5h下车']
                },
                // color: ['#00dd00', 'red', 'blue', 'gray'],
                calculable : true,
                xAxis : [
                    {
                        type: 'value',
                        min: -30,
                        max: 120,
                        axisLabel:{
                            formatter: function(value){
                                if (value == 0){
                                    return '当前';
                                }
                                if (value == 60){
                                    return '1h';
                                }
                                if (value == 120){
                                    return '2h'
                                }
                            }
                        },
                        splitLine:{  
                            show:false  
                        },
                    }
                ],
                yAxis : [
                    {
                        show:false,
                        type: 'value',
                        splitLine:{  
                            show:false  
                        },
                    }
                ],
                series : [
                    {
                        name: '运力',
                        type: 'line',
                        symbolSize: 1,
                        data: [
                            [-30, dataArray[0].value],[-15, dataArray[0].value],[0, dataArray[0].value],[15, dataArray[0].value],[30, dataArray[0].value],[45, dataArray[0].value],[60, dataArray[0].value],[75, dataArray[0].value],[90, dataArray[0].value],[105, dataArray[0].value],[120, dataArray[0].value]
                        ],
                        lineStyle: {
                            normal:{
                                width: 5,
                                color: "#00dd00"
                            }
                        },
                        markLine : {
                            data : [
                                {
                                    xAxis: 0, 
                                    symbol: 'circle',
                                    symbolSize: [0, 0],
                                    lineStyle: {
                                        normal: {
                                            type: 'solid',
                                            color: '#000'
                                        }
                                    },
                                    label: {
                                        normal: {
                                            show: false
                                        }
                                    }
                                },
                                {
                                    yAxis: 0, 
                                    symbol: 'triangle',
                                    lineStyle: {
                                        normal: {
                                            type: 'solid',
                                            color: '#000'
                                        }
                                    },
                                    label: {
                                        normal: {
                                            show: false
                                        }
                                    }
                                }
                                
                            ]
                        }
                    },
                    {
                        name:'滞站候车',
                        type:'line',
                        symbolSize:1,
                        data:[
                            [-30, dataArray[1].value[0]], [-15, dataArray[1].value[1]], [0, dataArray[1].value[2]], [15, dataArray[1].value[3]], [30, dataArray[1].value[4]], [45, dataArray[1].value[5]], [60, dataArray[1].value[6]], [75, dataArray[1].value[7]], [90, dataArray[1].value[8]], [105, dataArray[1].value[9]], [120, dataArray[1].value[10]]
                        ],
                        lineStyle: {
                            normal:{
                                width: 1,
                                color: "red"
                            }
                        }
                    },
                    {
                        name:'0.5h上车',
                        type:'line',
                        symbolSize:1,
                        data:[
                            [-30, dataArray[2].value[0]], [0, dataArray[2].value[1]],  [30, dataArray[2].value[2]], [60, dataArray[2].value[3]], [90, dataArray[2].value[4]], [120, dataArray[2].value[5]]
                        ],
                        lineStyle: {
                            normal:{
                                width: 1,
                                color: "blue"
                            }
                        }
                    },
                    {
                        name:'0.5h下车',
                        type:'line',
                        symbolSize:1,
                        data:[
                            [-30, dataArray[3].value[0]], [0, dataArray[3].value[1]],  [30, dataArray[3].value[2]], [60, dataArray[3].value[3]], [90, dataArray[3].value[4]], [120, dataArray[3].value[5]]
                        ],
                        lineStyle: {
                            normal:{
                                width: 1,
                                color: "gray"
                            }
                        }
                
                    },
                ]
            };
            var myChart = echarts.init(this.$el.find('.trend_chart_map')[0]);
            myChart.setOption(option);
        },
    });

    // 越站快车
    var express_train = Widget.extend({
        template: "express_train_template",
        events: {
            'click .sendbt': 'send_express_fn',
        },
        init: function(parent, express_info){
            this._super(parent);
            this.express_info = express_info;
        },
        send_express_fn: function(){
            var thisObj = this.$el;            
            var bus_mode = thisObj.find('.express_train_info input[type="radio"][name="bus_mode"]').val();
            var time = thisObj.find('.express_train_info input[type="time"]').val();
            var bus = thisObj.find('.express_train_info .select_bus').val();
            var stopping_mode = thisObj.find('.select_part_info input[type="radio"][name="stopping_mode"]').val();
            var skip_num = thisObj.find('.select_part_info .skip_info input[type="number"]').val();
            var station_ck_list = [];
            thisObj.find('.station_info input[type="checkbox"]:checked').each(function(index, el) {
                station_ck_list.push(el.value);
            });
            alert("表单暂时还无法提交");
            this.$el.parents(".passenger_flow_cont").find(".trend_chart_info").show();
            this.$el.remove();
        }
    });

    return passenger_flow;
});

