 odoo.define("lty_dispatch_desktop_widget.communication", function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;

    var communication = Widget.extend({
        template: "communication_template_box",
        events: {
            "click .send_cont_bt": "send_info_fn",
        },
        init: function(parent, data){
            this._super(parent);
            var current_info = {
                name: "liangkui",
                id: "001",
                img: ""
            };
            var channel_info = {
                source_channel: {
                    name: "总调度台",
                    id: "3",
                    is_history: true,
                },
                channel: [
                    {
                        name: "604调度台",
                        id: "1",
                        type: "multiple",
                    },
                    {
                        name: "M214调度台",
                        id: "2",
                        type: "multiple",
                    },
                    {
                        name: "总调度台",
                        id: "3",
                        type: "total",
                    },
                ],
                direct_messages: [
                    {
                        name: "101车",
                        id: "01",
                        type: "single",
                    },
                    {
                        name: "102车",
                        id: "02",
                        type: "single",
                    },
                    {
                        name: "103车",
                        id: "03",
                        type: "single",
                    },
                ],
            }
            this.current_info = current_info;
            this.channel_info = channel_info;
        },
        start: function(){
            this.$el.append(QWeb.render("communication_template", {channel_info: this.channel_info}));
            this.load_fn();
        },
        // 加载事件
        load_fn: function(){
            var self = this;
            // 键盘事件
            document.onkeydown=function(e){
                if (13 == e.keyCode && e.ctrlKey){
                    self.send_info_fn();
                }
            };

            // 当前窗口事件
            self.$(".children_directory .children_o").click(function(){
                self.get_active_info($(this));
            });

            // 查看历史数据
            self.$(".history_bt").click(function(){
                var oe_self = $(this);
                self.load_history_info_fn(oe_self);
            });

        },
        // 整理信息
        send_info_fn: function(){
            var info = this.$(".o_content_text").val().replace(/(^\s*)|(\s*$)/g, "");

            var options = {
                name: this.current_info.name,
                img: this.current_info.img,
                cont: info,
                data_time: this.getNowFormatDate(),
            };
            this.send_callback(options);
        },
        // 发送回调
        send_callback: function(options){
            // alert("请求接口");
            this.$(".current_info").append(QWeb.render("chat_model_template", {info: options}));
            this.$(".chat_content").scrollTo(this.$(".chat_content")[0].scrollHeight);
            this.$(".o_content_text").val("");

        },
        // 加载历史数据
        load_history_info_fn: function(oe_self){
            var self = this;
            oe_self.hide();
            oe_self.next().show();
            var associated_id = oe_self.attr("id");
            setTimeout(function(){
                var history_options = 
                    {
                        total_history: 4,
                        history_list: [
                            {
                                name: "张三",
                                img: "",
                                id: "a0",
                                cont: "今天星期几?",
                                data_time: "2017/07/21 09:46:20",
                            },
                            {
                                name: "李四",
                                img: "",
                                id: "a1",
                                cont: "二楞，今天星期五了",
                                data_time: "2017/07/21 09:47:13",
                            },
                            {
                                name: "张三",
                                img: "",
                                id: "a3",
                                cont: "那不是又要放假了，兄弟们明天怎么安排？",
                                data_time: "2017/07/21 09:47:55",
                            },
                            {
                                name: "liangkui",
                                img: "",
                                id: "a4",
                                cont: "明天钓鱼去不去?",
                                data_time: "2017/07/21 09:48:22",
                            },

                        ],
                        existing_history_id_list: ["a1", "a2", "a3", "a4"]

                    }
                oe_self.next().hide(function(){
                    self.$(".current_info_fgx").show();
                    var history_info = self.$(".history_info");
                    for (var i=0, len=history_options.history_list.length;i<len; i++){
                        history_info.append(QWeb.render("chat_model_template", {info: history_options.history_list[i]}));
                    }
                    self.$(".chat_content").scrollTo(0);
                    if (history_options.total_history > history_options.existing_history_id_list.length){
                        oe_self.show();
                    }
                });
            },2000);

        },
        // 获取当前窗口的信息资源
        get_active_info: function(obj){
            // alert("发生请求");
            self.$(".children_directory .children_o").removeClass('op_active');
            obj.addClass("op_active");
        },
        // 获取当前时间-组织格式
        getNowFormatDate: function () {
            var date = new Date();
            var seperator1 = "-";
            var seperator2 = ":";
            var month = date.getMonth() + 1;
            var strDate = date.getDate();
            if (month >= 1 && month <= 9) {
                month = "0" + month;
            }
            if (strDate >= 0 && strDate <= 9) {
                strDate = "0" + strDate;
            }
            var currentdate = date.getFullYear() + seperator1 + month + seperator1 + strDate
                    + " " + date.getHours() + seperator2 + date.getMinutes()
                    + seperator2 + date.getSeconds();
            return currentdate;
        },
    });
    core.action_registry.add('lty_dispatch_desktop_widget.communication', communication);

    return communication;
});

