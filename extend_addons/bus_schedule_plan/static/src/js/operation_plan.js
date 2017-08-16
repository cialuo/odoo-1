odoo.define('abc',function (require) {
    "use strict";
    var Model = require('web.Model');
        var model =  new Model("scheduleplan.busmovetime");
        model.call("reoppaln2web").then(function (data) {
            console.log(data);
        });
    // var arr = [];
    // for (var i = 0, m = $('.abcde li').length; i < m; i++) {
    //     if ($('.abcde li').eq(i).html() != '') {
    //         arr.push($('.abcde li').eq(i).html());
    //     }
    // }
    var arr =[1,2,3,6,5,4,7,8,9,3,1,2,3,6,11,15];
    $('body').on('dblclick', '.abcd .abcde li', function () {
        if (!$(this).hasClass('abc') && $(this).html() != '') {
            if ($('.abcde li.abc').length % 4 == 0) {
                $('.abcd').append('<ul class="abcde"><li></li><li></li><li></li><li></li></ul>')
                var a = parseInt($('.title1 li').last().find('div').html()) + 1;
                $('.title1').append('<li><div>' + a + '</div><div>竹-竹</div></li>');
            }
            $(this).css('background', 'red').html('').addClass('abc');
            for (var i = 0; i < arr.length; i++) {
                $(".abcde li:not(.abc)").eq(i).html(arr[i]);
            }
        } else if ($(this).hasClass('abc')) {
            if ($('.abcde  li.abc').length % 4 == 1) {
                $('.abcd').find('ul:last').remove();
                $('.title1').find('li:last').remove();
            }
            $(this).css('background', 'white').removeClass('abc');
            $(".abcde li:not(.abc)").html('');
            for (var i = 0; i < arr.length; i++) {
                $(".abcde li:not(.abc)").eq(i).html(arr[i]);
            }
        }
    })
    // model_students.call('get_examination_info').then(function (data) {
})
