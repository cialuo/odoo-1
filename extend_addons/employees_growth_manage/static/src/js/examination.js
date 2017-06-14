odoo.define('examinationTemplate.test', function (require) {

    var core = require('web.core');

    var Widget = require('web.Widget');

    var QWeb = core.qweb;

    var WebsocketTest = Widget.extend({

        //template: 'examinationTemplate',
        
        init:function (parent) {
            this._super(parent);
        },

        start:function () {
            var self = this;
            var active_ids = self.id;
            console.log('active_ids:'+active_ids)


            //var model = new Model("message_of_the_day");
            var msgList = [{'name':'李白姓什么?','a':'李','b':'张','c':'赵','d':'钱'},
                {'name':'杜甫姓什么?','a':'杜','b':'肖','c':'凃','d':'向'},
                {'name':'李牧是谁？','a':'李白的粑粑','b':'李白的仔','c':'赵国人士','d':'外星人'}];

             self.$el.append(QWeb.render("messages",{msgList:msgList}));
        },
        events:{
            'click .btn_jiaojuan':'handle_click'
        },
        handle_click:function () {
            alert('结束考试...');
        }



    });

    //注册
    core.action_registry.add('examinationTemplate_page', WebsocketTest);

    //单纯的渲染界面不需要返回
    //return WebsocketTest;
});