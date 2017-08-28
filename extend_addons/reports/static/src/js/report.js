odoo.define('roport.test', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    var WebsocketTest = Widget.extend({
        //template: 'RoportTest',
        start:function () {
            //声明初始化之后的对象
            var self = this;
            self.$el.append(QWeb.render("search", {}));
            self.$el.append(QWeb.render("RoportTest", {}));
        },
         events:{
             'click .btn_chaxun':'handle_click',

        },
        handle_click:function () {
            var type = $('#type').val();

            alert($('#report'));
        }

    });

    core.action_registry.add('report.page', WebsocketTest);

});