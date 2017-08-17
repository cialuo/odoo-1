odoo.define('abc', function (require) {
    "use strict";
    var Model = require('web.Model');
    var model = new Model("scheduleplan.busmovetime");
    var recid = $('#the_rec_id .o_form_field').text();
    model.call("reoppaln2web", [recid]).then(function (data) {
        console.log(JSON.parse(data))
        var a = JSON.parse(data).bus;
        console.log(a[1])
        for(var ts=0;ts<a[1].length;ts++){
            $('.sort_title').append('<li><div>'+ts+'</div><div>'+a[1][ts][2]+'</div></li>')
        }
        alert(Object.keys(a).length)
        for(var bn = 0;bn<Object.keys(a).length;bn++){

        }
        for (var i in a) {
            console.log(a[i].length);
        }
    });
    // var arr = [];
    // for (var i = 0, m = $('.sort_top li').length; i < m; i++) {
    //     if ($('.sort_top li').eq(i).html() != '') {
    //         arr.push($('.sort_top li').eq(i).html());
    //     }
    // }

    function move() {
        $('.opera_sort').on('dblclick', '.sort_top li', function () {
            if (!$(this).hasClass('sort_out') && $(this).html() != '') {
                if ($('.sort_top li.sort_out').length % 4 == 0) {
                    $('.opera_sort').append('<ul class="sort_top"><li></li><li></li><li></li><li></li></ul>')
                    var a = parseInt($('.sort_title li').last().find('div').html()) + 1;
                    $('.sort_title').append('<li><div>' + a + '</div><div>竹-林</div></li>');
                }
                $(this).css('background', 'red').html('').addClass('sort_out');
                for (var i = 0; i < arr.length; i++) {
                    $(".sort_top li:not(.sort_out)").eq(i).html(arr[i]);
                }
            } else if ($(this).hasClass('sort_out')) {

                if ($('.sort_top  li.sort_out').length % 4 == 1) {
                    $('.opera_sort').find('ul:last').remove();
                    $('.sort_title').find('li:last').remove();
                }
                $(this).css('background', 'white').removeClass('sort_out');
                $(".sort_top li:not(.sort_out)").html('');
                for (var i = 0; i < arr.length; i++) {
                    $(".sort_top li:not(.sort_out)").eq(i).html(arr[i]);
                }
            }
            return false;
        });
    }

    move();
    // model_students.call('get_examination_info').then(function (data) {
})
