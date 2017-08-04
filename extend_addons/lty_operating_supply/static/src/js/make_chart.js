var supply_make_chart_options = {
    default_option_set1: function(arg, set_option) {
    	var series_data = arg.data_list;
    	var series_data_set = arg.series_data_set;
        var legend_data = [];  	// 图表每条数据说明
        var color = []; 		// 图表每条数据颜色
       	var new_series_data = [];
        for (var d = 0, dl = series_data.length; d < dl; d++) {
            var data = series_data[d];
            legend_data.push(data.name);
            if (data.lineStyle){
            	color.push(data.lineStyle.normal.color);
            }
            if (series_data_set){
            	new_series_data.push($.extend(data, series_data_set));
            }
        }

        if (arg.legend_number){
        	legend_data = legend_data.slice(0, arg.legend_number);
        	color = color.slice(0, arg.legend_number);
        }

        series_data = new_series_data.length>0 ? new_series_data: series_data

        var option = {
            tooltip: {
                trigger: 'axis'
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                show: false,
                axisLabel: {
                    formatter: '{value}点'
                },
                data: arg.xAxis_data,
                axisLine: {
                    show: false,
                },
                axisTick: {
                    show: false
                },
            },
            yAxis: {
                type: 'value',
                name: arg.yName,
                nameGap: 32,
                nameTextStyle: {
                    fontSize: 16
                },
                offset: 20,
                axisLabel: {
                    formatter: '{value}人/次',
                },
                data: arg.yAxis_data,
                axisLine: {
                    show: false,
                },
                axisTick: {
                    show: false
                },
                splitLine: {
                    lineStyle: {
                        type: 'dashed'
                    }
                }
            },
            series: series_data
        };
        if (set_option.legend){
        	set_option.legend.data = legend_data;
        	if (color.length > 0){
        		set_option.color = color;
        	}
        }
        if (set_option){
        	$.extend(true, option, set_option);
        }
        
        return option;
    },
    default_option_set2: function(arg, set_option) {
    	var series_data = arg.data_list;
    	var schema = arg.schema;
    	var option = {
                grid: {
                    left: '8%',
                    bottom: '8%',
                    right: '8%',
                    top: '8%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: arg.xAxis_data,
                    boundaryGap: false,
                    splitLine: {
                        show: true,
                        lineStyle: {
                            color: '#999',
                            type: 'dashed'
                        }
                    },
                    axisLabel: {
                        formatter: '{value}点',
                    },
                    axisLine: {
                        show: false
                    },
                    axisTick: {
                        show: false
                    },
                },
                yAxis: {
                    type: 'category',
                    data: arg.yAxis_data,
                    axisLine: {
                        show: false
                    },
                    axisTick: {
                        show: false
                    },
                    offset: 30
                },
                visualMap: [{
                    left: 'right',
                    top: '10%',
                    show: false,
                    dimension: 2,
                    min: 0,
                    max: 1000,
                    itemWidth: 30,
                    itemHeight: 120,
                    calculable: true,
                    precision: 0.1,
                    textGap: 30,
                    textStyle: {
                        color: '#000'
                    },
                    inRange: {
                        symbolSize: [10, 70]
                    },
                    outOfRange: {
                        symbolSize: [10, 70],
                    }
                }],
                series: series_data
            };
   
        if (set_option){
        	$.extend(true, option, set_option);
        }
        
        return option;
    },
}