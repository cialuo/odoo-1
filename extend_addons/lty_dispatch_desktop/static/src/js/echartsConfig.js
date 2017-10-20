var optionLineBar = {
    title: {
        left: '35%',
        textStyle: {
            color: 'white',
            fontSize: 14
        },
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross',
            label: {}
        }
        // backgroundColor:'white',
        // borderColor:'#ccc',
        // borderWidth:1,
        // textStyle:{
        //     color:'#666',
        //     fontSize:16
        // }

    },
    textStyle: {
        color: '#a3a5ab'
    },
    legend: {
        data: '',
        orient: 'vertical',
        right: "10px",
        top: '10px',
        textStyle: {
            color: 'white',
            fontSize: 12
        },
        icon: 'stack'
    },
    // toolbox: {
    //     top:'2.3%',
    //     right:'2.5%',
    //     feature: {
    //         magicType: {show: true, type: ['line', 'bar']}
    //     }
    // },
    grid: {
        left: '3%',
        right: '105px',
        bottom: '3%',
        top: "23%",
        show: true,
        containLabel: true,
        borderColor: "#3F4663"

    },
    xAxis: [
        {
            axisLabel: {
                rotate: '',
                interval: 0,     //表示x轴长度除以n 若为2则x轴数量除以2
            },
            textStyle: {
                fontSize: '',
                fontStyle: ''
            },
            type: 'category',
            data: [],
            axisLine: {
                lineStyle: {
                    color: '#3F4663'        //左边线的颜色
                }
            },
            boundaryGap: '',
            splitLine: {
                show: true,
                lineStyle: {
                    // 使用深浅的间隔色,可用来设置横坐标的颜色
                    color: ['#3F4663']
                }
            }
        }
    ],
    yAxis: [
        {
            type: 'value',
            name: '人力',
            axisLine: {
                lineStyle: {
                    color: '#3F4663'          //左边线的颜色
                }
            },
            splitLine: {
                lineStyle: {
                    // 使用深浅的间隔色,可用来设置横坐标的颜色
                    color: ['#3F4663']
                }
            }
        }
    ],
    series: ''
};

var chartLineBar = function (dom,border_width, color, lineOrbar, boundaryGap, title, option, keyJson, dataJson, stackType,line_num) {
    option.xAxis[0].data = keyJson;
    option.xAxis[0].boundaryGap = boundaryGap;
    option.legend.data = title;
    option.title.text=line_num+'·客流与动力';
    option.series = function () {
        var res = [];
        for (var i = 0, size = dataJson.length; i < size; i++) {
            res.push({
                stack: stackType,
                type: lineOrbar,
                smooth: true,
                symbol: 'none',
                name: title[i],
                data: dataJson[i],
                lineStyle: {
                    normal: {
                        width: border_width
                    }
                },
                itemStyle: {
                    normal: {
                        color: color[i]
                    }
                }

            });
        }
        return res;
    }();
    dom.setOption(option);
    dom.hideLoading();
    // window.addEventListener("resize", function () {
    //     myChart.resize();
    // });
};
