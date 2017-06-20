odoo.define('examinationTemplate.test', function (require) {

    var core = require('web.core');

    var Widget = require('web.Widget');

    //导入模块用户后台交互
    var Model = require('web.Model');

    var QWeb = core.qweb;

    var WebsocketTest = Widget.extend({

        //template:'info_title',

        init:function (parent,context) {
            this._super(parent,context);
            //获取参数保存
            if (context.context.active_id) this.student_ids = [context.context.active_id];
            //创建学生对象
            this.model_students = new Model('employees_growth.students');
        },

        start:function () {
            //声明初始化之后的对象
            var self = this;
            var active_ids = self.student_ids;
            //获取后台数据
            self.model_students.call('get_examination_info',[active_ids]).then(function (data) {
                data = eval(data)
                console.log(data)
                self.$el.append(QWeb.render("title_info",{title_info:data}));
                if(data.radio!=null){
                    self.$el.append(QWeb.render("radio_info",{radio_info:data.radio}));
                }
                if(data.multiselect!=null){
                    self.$el.append(QWeb.render("multiselect_info",{multiselect_info:data.multiselect}));
                }
                if(data.judge!=null){
                    self.$el.append(QWeb.render("judge_info",{judge_info:data.judge}));
                }

            });

        },
        events:{
            'click .btn_jiaojuan':'handle_click',
            'change .radio_answer':'radio_answer',
            'change .multiselect_answer':'multiselect_answer',
            'change .judge_answer':'judge_answer'

        },
        handle_click:function () {
            var self = this;
            var answers = $("input.answer")
            var paramet = {};
            for(var i =0;i<answers.length;i++){
                var key = answers[i].id.split("_")[0];
                var id = answers[i].id.split("_")[2];
                var value = answers[i].value;
                var array;
                if(paramet.hasOwnProperty(key)){
                    array = paramet[key];
                }else{
                    array = new Array();
                }

                var map = {};
                map['id'] = id;
                map['type'] = key;
                map['value'] = value;
                array.push(map);
                paramet[key] = array;
           }
           paramet['student_id'] = self.student_ids;
           var json = JSON.stringify(paramet);
           //获取后台数据
           self.model_students.call('test_calculation',[paramet]).then(function (data) {
               //跳转到详情界面
               self.do_action({
                    type: 'ir.actions.act_window',
                    res_model: 'employees_growth.students',
                    res_id: self.student_ids[0],
                    views: [[false, 'form']],
                });
           });

        },
        radio_answer:function () {
           var radios = $('input[type="radio"][class="radio_answer"]:checked'); // 获取一组被选中的radio
           for (var i=0;i<radios.length;i++){
               $("#radio_question_"+radios[i].id.split("_")[1]).val(radios[i].value)
           }

        },
        multiselect_answer:function () {
            var checkboxs = $('input[type="checkbox"][class="multiselect_answer"]:checked'); // 获取一组被选中的checkbox
            this.multiselect_answer_value(checkboxs);
        },
        multiselect_answer_value:function (checkboxs) {

            //组合新的值
            var checkboxMap = new Map();
            for(var i=0;i<checkboxs.length;i++){
                var key = checkboxs[i].name;
                var checkboxArray;
                if(checkboxMap.has(key)){
                    checkboxArray = checkboxMap.get(key);
                }else{
                   checkboxArray = new Array();
                }
                checkboxArray.push(checkboxs[i].value);
                checkboxMap.set(key,checkboxArray);
            }

           checkboxMap.forEach(function( value , key , map ){
               var index = key.split('_')[1];
               var array = checkboxMap.get(key)
               var vallue = "";
               for (var i = 0;i<array.length;i++){
                   vallue+=array[i];
               }
               $("#multiselect_question_"+index).val(vallue);
           })
        },
        judge_answer:function () {
            var radios = $('input[type="radio"][class="judge_answer"]:checked'); // 获取一组被选中的radio
            for (var i=0;i<radios.length;i++){
               $("#judge_question_"+radios[i].id.split("_")[1]).val(radios[i].value)
            }
        }



    });

    //注册
    core.action_registry.add('examinationTemplate_page', WebsocketTest);

    //单纯的渲染界面不需要返回
    //return WebsocketTest;
});