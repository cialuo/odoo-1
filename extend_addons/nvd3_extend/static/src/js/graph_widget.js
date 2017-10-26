odoo.define('nvd3_extend.GraphWidget', function (require) {
    "use strict";
    var config = require('web.config');
    var core = require('web.core');
    var Model = require('web.DataModel');
    var formats = require('web.formats');
    var Widget = require('web.Widget');
    var GraphWidget = require('web.GraphWidget');
    var QWeb = core.qweb;
    var _t = core._t;

    GraphWidget.include({
        display_pie1: function () {
            var number=(new Date()).valueOf();
            var myId="myCharts"+number;
          $(this.$el[0]).append('<div id="'+myId+'" class="myCharts"></div>');
        var myChart = echarts.init(document.getElementById(myId));
        var data = genData(this.data);
        console.log(this.data)
        var option = {
            tooltip : {
                trigger: 'item',
                formatter: "{b} : {c} ({d}%)"
            },
            legend: {
                type: 'scroll',
                orient: 'vertical',
                right: 10,
                top: 20,
                bottom: 20,
                data:data.legendData
            },
            series : [
                {
                    type: 'pie',
                    radius : ['25%','55%'],
                    center: ['40%', '50%'],
                    data: data.seriesData,
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        };
        myChart.setOption(option);

        function genData(data) {
            var legendData = [];
            var seriesData = [];
            $.each(data,function (idx,val) {
                if(val.labels.length==1){
                    var subval=val.labels[0];
                }else{
                    var subval=val.labels[0]+'/'+val.labels[1];
                }
                legendData.push(subval);
                    seriesData.push({
                        name: subval,
                        value: val.value
                    });
            });

            return {
                legendData: legendData,
                seriesData: seriesData
            };
        }
        },
        display_pie: function () {
            var number=(new Date()).valueOf();
            var myId="myCharts"+number;
          $(this.$el[0]).append('<div id="'+myId+'" class="myCharts"></div>');
        var myChart = echarts.init(document.getElementById(myId));
        var data = genData(this.data);
        console.log(this.data)
        var option = {
            tooltip : {
                trigger: 'item',
                formatter: "{b} : {c} ({d}%)"
            },
            legend: {
                type: 'scroll',
                orient: 'vertical',
                right: 10,
                top: 20,
                bottom: 20,
                data:data.legendData
            },
            series : [
                {
                    type: 'pie',
                    radius : '55%',
                    center: ['40%', '50%'],
                    data: data.seriesData,
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        };
        myChart.setOption(option);

        function genData(data) {
            var legendData = [];
            var seriesData = [];
            $.each(data,function (idx,val) {
                if(val.labels.length==1){
                    var subval=val.labels[0];
                }else{
                    var subval=val.labels[0]+'/'+val.labels[1];
                }
                legendData.push(subval);
                    seriesData.push({
                        name: subval,
                        value: val.value
                    });
            });

            return {
                legendData: legendData,
                seriesData: seriesData
            };
        }
        },
    })
});