odoo.define('examinationTemplate.test', function (require) {

    var core = require('web.core');

    var Widget = require('web.Widget');

    //导入模块用户后台交互
    var Model = require('web.Model');

    var QWeb = core.qweb;

    var WebsocketTest = Widget.extend({

        init:function (parent,context) {
            this._super(parent,context);
            console.log(context.context)
            //获取参数保存
            if (context.context.active_id) this.student_ids = [context.context.active_id];
            //创建学生对象
            this.model_students = new Model('employees_growth.students');
        },

        start:function () {
            //声明初始化之后的对象
            var self = this;
            var active_ids = self.student_ids;
            var result_set = ['1','2'];
            console.log(result_set);
            //获取后台数据
            self.model_students.call('get_examination_info',[active_ids]).then(function (data) {
                console.log(data);
                result_set.push(data);
                console.log('result_set:'+result_set);
            });

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