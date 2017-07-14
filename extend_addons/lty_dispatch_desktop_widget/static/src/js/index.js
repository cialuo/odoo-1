odoo.define(function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var Car = Widget.extend({
        template: 'Car',
        events: {
            'click .arrivalTime': 'arrivalTimeFn',
            'click .video': 'videoFn',
            'click .police': 'policeFn',
        },
        init: function(parent){
            this._super(parent);
            this.name = "work";
        },
        start: function(){
            self = this;
            this.arrivalTimeFn();
        },
        arrivalTimeFn: function(e){
            this.$(".carReport").html("");
            var data = {'a':'c'};
            new Car_a(this, data).appendTo(this.$(".carReport"));
        },
        videoFn: function(e){
            this.$(".carReport").html("");
            new Car_video(this).appendTo(this.$(".carReport"));
        },
        policeFn: function(e){
            this.$(".carReport").html("");
            new Car_police(this).appendTo(this.$(".carReport"));
        },

    });
    core.action_registry.add('work.car', Car);

    var Car_a = Widget.extend({
        template: "Car_a",
        init: function(parent,p){
            this._super(parent);
            this.p = p;
        },
        start: function(){
            this.carFGXFn();
        },
        carFGXFn: function(){
            var data = this.p;
            var option = {
                tooltip: {
                    trigger: 'axis',
                },
                color: ['blue', 'yellow', '#d29090'],
                legend: {
                    data:['计划', '预测', '实际']
                },
                grid: {
                    left: '2%',
                    right: '15%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis:  {
                    type: 'category',
                    boundaryGap: false,
                    name: '准点',
                    data: ['深大(8:30)','白石洲(8:37)','世界之窗(8:45)','华侨城(8:51)','车公庙(8:55)','葫芦谷(9:05)','断肠崖(9:15)', '长坂坡(9:30)'],
                    axisLabel:{
                        // interval: 0,
                        // formatter:function(val){
                        //     return val.split("").join("\n");
                        // }
                    },
                },
                yAxis: {
                    type: 'value',
                    min: -15,
                    max: 15,
                    name: '提前(分钟)',
                    axisLabel: {
                        formatter: '{value}'
                    }
                },
                series: [
                    {
                        name:'预测',
                        type:'line',
                        symbolSize:1,
                        data:[1, 1, 5, 3, 2, 3, 0],
                        lineStyle: {
                            normal:{
                                width: 1
                            }
                        },
                    },
                    {
                        name:'实际',
                        type:'line',
                        symbolSize:1,
                        data:[1, 1, -2, -5, 0, -3, -2],
                        lineStyle: {
                            normal:{
                                width: 1
                            }
                        },
                    },
                    {
                        name:'计划',
                        type:'line',
                        symbolSize:1,
                        data:[0, 0, 0, 0, 0, 0, 0],
                        lineStyle: {
                            normal:{
                                width: 1
                            }
                        },
                        markLine: {
                            data: [
                                {type: 'average', name: '平均值'},
                            ]
                        }
                    }
                ]
            };
            var myChart = echarts.init(this.$el.find('.carzxt')[0]);
            myChart.setOption(option);
        }
    });
    core.action_registry.add('work.car_a', Car_a);

    var Car_police = Widget.extend({
        template: "Car_police",
        init: function(parent){
            this._super(parent);
        },
    });
    core.action_registry.add('work.car_police', Car_police);

    var Car_video = Widget.extend({
        template: "Car_video",
        init: function(parent){
            this._super(parent);
        },
    });
    core.action_registry.add('work.car_video', Car_video);

    var Car_map = Widget.extend({
        template: "Car_map",
        init: function(parent){
            this._super(parent);
        },
        start: function(){
            this.addMapImg();
        },
        addMapImg: function(){
            this.$el.find(".carInfoScene").append('<img width="344" height="330" src="http://restapi.amap.com/v3/staticmap?location=114.39973,30.45787&zoom=14&size=344*330&markers=large,,:114.39973,30.45787&key=cf2cefc7d7632953aa19dbf15c194019&scale=2" alt="">')
        }
    });
    core.action_registry.add('work.car_map', Car_map);

    var Car_moreInfo = Widget.extend({
        template: "Car_moreInfo",
        init: function(parent){
            this._super(parent);
        },
    });
    core.action_registry.add('work.car_moreInfo', Car_moreInfo);

    var Car_passenge = Widget.extend({
        template: "Car_passenge",
        init: function(parent){
            this._super(parent);
        },
        start: function(){
            new Car_passengerMap(this).appendTo(this.$(".carPassengerLeft .cont"));
            new Car_passengerMap(this).appendTo(this.$(".carPassengerRight .cont"));
            // this.$(".carPassengerLeft .cont").html(new Car_passengerMap(this));
        }
    });
    core.action_registry.add('work.car_passenge', Car_passenge);

    var Car_passengerMap = Widget.extend({
        template: "Car_passengerMap",
        init: function(parent){
            this._super(parent);
        },
        start: function(){
            this.passengerMapFn();
        },
        passengerMapFn: function(){
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
                color: ['#00dd00', 'red', 'blue', 'gray'],
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
                        symbolSize:1,
                        data: [
                            [-30, 11],[-15, 11],[0, 11],[15, 11],[30, 11],[45, 11],[60, 11],[75, 11],[90, 11],[105, 11],[120, 11]
                        ],
                        lineStyle: {
                            normal:{
                                width: 5
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
                            [-30, 11], [-15, 12], [0, 15], [15, 12], [30, 13], [45, 11], [60, 11], [75, 9], [90, 13], [105, 12], [120, 11]
                        ],
                        lineStyle: {
                            normal:{
                                width: 1
                            }
                        }
                    },
                    {
                        name:'0.5h上车',
                        type:'line',
                        symbolSize:1,
                        data:[
                            [-30, 10], [0, 9],  [30, 9], [60, 8], [90, 10], [120, 10]
                        ],
                        lineStyle: {
                            normal:{
                                width: 1
                            }
                        }
                    },
                    {
                        name:'0.5h下车',
                        type:'line',
                        symbolSize:1,
                        data:[
                            [-30, 5], [0, 6],  [30, 7], [60, 6], [90, 5], [120, 8]
                        ],
                        lineStyle: {
                            normal:{
                                width: 1
                            }
                        }
                
                    },
                ]
            };
            var myChart = echarts.init(this.$el.find('#carPassengerMap')[0]);
            myChart.setOption(option);
        }
    });
    core.action_registry.add('work.car_passengerMap', Car_passengerMap);

    var Car_express = Widget.extend({
        template: "Car_express",
        init: function(parent){
            this._super(parent);
        },
    });
    core.action_registry.add('work.car_express', Car_express);
});

// openerp.oepetstore = function(instance, local) {
//     var _t = instance.web._t,
//         _lt = instance.web._lt;
//     var QWeb = instance.web.qweb;

//     local.Car = instance.Widget.extend({
//         template: "Car",
//         // init: function(parent){
//         //     this._super(parent);
//         //     this.name = "lk";
//         // },
//         start: function() {
            
//         },
//     });

//     instance.web.client_actions.add('work.car', 'instance.oepetstore.Car');
//     // instance.web.client_actions.add('petstore.homepage', 'instance.oepetstore.HomePage');
// }
