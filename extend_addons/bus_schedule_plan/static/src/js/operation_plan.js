odoo.define('abc', function (require) {
    "use strict";
    var Model = require('web.Model');
    var model = new Model("scheduleplan.busmovetime");
    var recid = $('#the_rec_id .o_form_field').text();

    function checkTime(i) {
        if (i < 10) {
            i = "0" + i;
        }
        return i;
    }

    model.call("reoppaln2web", [recid]).then(function (data) {
        console.log(data)
        var bus_num = Object.keys(data.bus).length;
        var m = 0, n = 0;
        for (var ts = 0; ts < data.bus[1].length; ts++) {
            if (ts % 2 == 0) {
                $('.time_start_arrive_stop thead tr').append('<th><div>' + ts + '</div><div>' + data.upstation.substr(0, 1) + '-' + data.downstation.substr(0, 1) + '</div></th>')
                m++;
                // $('.time_start_arrive_stop thead').append('<ul class="sort_top"></ul>');
            } else {
                $('.time_start_arrive_stop thead tr').append('<th><div>' + ts + '</div><div>' + data.downstation.substr(0, 1) + '-' + data.upstation.substr(0, 1) + '</div></th>')
                n++;
                // $('.time_start_arrive_stop thead').append('<ul class="sort_down"></ul>');
            }
        }
        for (var bn = 1; bn < (bus_num + 1); bn++) {
            $('.time_start_arrive_stop tbody').append('<tr><td>' + bn + '</td></tr>');
            for (var bTd = 0; bTd < data.bus[bn].length; bTd++) {
                if(data.bus[bn][bTd][1][1] !=null){
                    var timesHours = checkTime(new Date(data.bus[bn][bTd][1][1].startmovetime).getHours());
                    var timesMin = checkTime(new Date(data.bus[bn][bTd][1][1].startmovetime).getMinutes());
                    var timeaHours = checkTime(new Date(data.bus[bn][bTd][1][1].arrive_time).getHours());
                    var timeaMin = checkTime(new Date(data.bus[bn][bTd][1][1].arrive_time).getMinutes());
                    $('.time_start_arrive_stop').find('tr').eq(bn).append('<td>'+$('.start_over_stop_time').html()+'</td>');
                    $('.time_start_arrive_stop').find('tr').eq(bn).find('td').eq(bTd+1).find('.start_time').html(timesHours + ':' + timesMin);
                    $('.time_start_arrive_stop').find('tr').eq(bn).find('td').eq(bTd+1).find('.over_time').html(timeaHours + ':' + timeaMin);
                }else{
                    $('.time_start_arrive_stop').find('tr').eq(bn).append('<td>'+$('.start_over_stop_time').html()+'</td>');
                }
            }
        }
    })
    // function move() {
    //     $('.opera_sort').on('dblclick', '.sort_top li', function () {
    //         var startTime = sessionStorage.getItem("start_time");
    //         var arrive_time = sessionStorage.getItem("arrive_time");
    //         var arr_startTime = startTime.split(",");
    //         var arr_arriveTime = arrive_time.split(",");
    //         console.log($(".sort_top li:not(.sort_out)").eq(2).find('start_time').html())
    //         if (!$(this).hasClass('sort_out') && $(this).html() != '') {
    //             if ($('.sort_top li.sort_out').length % 5 == 0) {
    //                 $('.opera_sort').append('<ul class="sort_top"><li></li><li></li><li></li><li></li></ul>')
    //                 var a = parseInt($('.sort_title li').last().find('div').html()) + 1;
    //                 $('.sort_title').append('<li><div>' + a + '</div><div>竹-林</div></li>');
    //             }
    //             $(this).css('background', '#cccccc').html('').addClass('sort_out');
    //             for (var i = 0; i < startTime.length; i++) {
    //                 $(".sort_top li:not(.sort_out)").eq(i).find('.start_time').html(arr_startTime[i]);
    //                 $(".sort_top li:not(.sort_out)").eq(i).find('.over_time').html(arr_arriveTime[i]);
    //                 model.call("reoppaln2web", [recid]).then(function (data) {
    //
    //                 })
    //             }
    //         } else if ($(this).hasClass('sort_out')) {
    //             if ($('.sort_top  li.sort_out').length % 5 == 1) {
    //                 $('.opera_sort').find('ul:last').remove();
    //                 $('.sort_title').find('li:last').remove();
    //             }
    //             $(this).css('background', 'white').removeClass('sort_out');
    //             $(".sort_top li:not(.sort_out)").html('');
    //             for (var i = 0; i < arr.length; i++) {
    //                 $(".sort_top li:not(.sort_out)").eq(i).html(arr[i]);
    //             }
    //         }
    //         return false;
    //     });
    // }
    //
    // move();
    // model_students.call('get_examination_info').then(function (data) {
})
