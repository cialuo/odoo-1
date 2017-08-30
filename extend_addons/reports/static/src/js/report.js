odoo.define('roport.test', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;
    //导入模块用户后台交互
    var Model = require('web.Model');

    var WebsocketTest = Widget.extend({
        //template: 'RoportTest',
        start:function () {
            //声明初始化之后的对象
            var self = this;

            //获取后台数据
            self.report_setting = new Model('report_setting');
            self.report_setting.call('get_service_url').then(function (data) {

                debugger
                console.log(data)

                self.$el.append(QWeb.render("search", {}));
                self.$el.append(QWeb.render("RoportTest", {url:data}));
            })
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