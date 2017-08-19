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
    function render_plan(data) {
        console.log(data);
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
                if (data.bus[bn][bTd][1][1] != null) {
                    var timesHours = checkTime(new Date(data.bus[bn][bTd][1][1].startmovetime).getHours());
                    var timesMin = checkTime(new Date(data.bus[bn][bTd][1][1].startmovetime).getMinutes());
                    var timeaHours = checkTime(new Date(data.bus[bn][bTd][1][1].arrive_time).getHours());
                    var timeaMin = checkTime(new Date(data.bus[bn][bTd][1][1].arrive_time).getMinutes());
                    $('.time_start_arrive_stop').find('tr').eq(bn).append('<td>' + $('.start_over_stop_time').html() + '</td>');
                    $('.time_start_arrive_stop').find('tr').eq(bn).find('td').eq(bTd + 1).attr('direction', data.bus[bn][bTd][1][1].direction)
                    $('.time_start_arrive_stop').find('tr').eq(bn).find('td').eq(bTd + 1).find('.start_time').html('<span>发</span><span class="time_left">' + timesHours + ':' + timesMin + '</span>');
                    $('.time_start_arrive_stop').find('tr').eq(bn).find('td').eq(bTd + 1).find('.over_time').html('<span>达</span><span class="time_left">' + timeaHours + ':' + timeaMin + '</span>');
                    if (data.bus[bn][bTd][4] != undefined) {
                        $('.time_start_arrive_stop').find('tr').eq(bn).find('td').eq(bTd + 1).find('.stop_time').html('<span>停</span><span class="time_left">' + data.bus[bn][bTd][4] + '</span>');
                    }
                } else {
                    $('.time_start_arrive_stop').find('tr').eq(bn).append('<td>' + $('.start_over_stop_time').html() + '</td>');
                }
            }
        }
        if(sessionStorage.getItem('direction')){
            alert(1)
            sessionStorage.removeItem('direction');
        }
        sessionStorage.setItem('direction', JSON.stringify(data.direction));
    }
    model.call("reoppaln2web", [recid]).then(function (data) {
        render_plan(data);
    })
    $('.time_start_arrive_stop').on('dblclick', 'tbody td', function () {
        if (!$(this).hasClass('sort_out') && $(this).html() != '') {
            $(this).css('background', '#cccccc').html('').addClass('sort_out');
            // 点击的index
            var this_index = $(this).index();
            //点击的direction
            var direction = $(this).attr('direction');
            // direction缓存对象
            var directionObj = JSON.parse(sessionStorage.getItem('direction'));
            sessionStorage.removeItem('direction')
            model.call("changeOpplan", [recid, this_index, direction, directionObj, 0]).then(function (res) {
                $('.time_start_arrive_stop').html('<thead><tr><th>班次</th></tr></thead><tbody></tbody>');
                render_plan(res);
            });
        } else if ($(this).hasClass('sort_out')) {
            var bgColor = $(this).parent('tr').css('background');
            $(this).css('background', bgColor).removeClass('sort_out');
        }
        return false;
    });
})
