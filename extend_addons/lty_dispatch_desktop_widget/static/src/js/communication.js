 odoo.define("lty_dispatch_desktop_widget.communication", function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var QWeb = core.qweb;

    var communication = Widget.extend({
        template: "communication_template",
        init: function(parent, data){
            this._super(parent);
            // 控制台用户信息
            var current_info = {
                name: "liangkui",
                id: "001",
                img: ""
            };
            // 沟通窗口信息
            var source_channel = {
                name: "总调度台",
                id: "3",
                is_history: true,
                send_info: [
                    {
                        name: "101车",
                        img: "",
                        id: "b1",
                        cont: "这是发给你的第一条消息",
                        data_time: "2017/07/20 09:46:20",
                    },
                    {
                        name: "102车",
                        img: "",
                        id: "b2",
                        cont: "这是发给你的第二条消息",
                        data_time: "2017/07/20 15:46:20",
                    }
                ]
            }
            // 频道列表
            var channel = [
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
            ];
            // 私信列表
            var direct_messages = [
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
            ];
            this.current_info = current_info;
            this.source_channel = source_channel;
            this.channel = channel;
            this.direct_messages = direct_messages;
        },
        start: function(){
            this.load_fn();
        },
        // 加载事件
        load_fn: function(){
            var self = this;
            // 加载当前窗口数据
            var loadObj = self.$(".chat_info .load_cont");
            new communication_info_window(self, self.source_channel, self.current_info, loadObj).appendTo(self.$(".info_window"));


            // 切换窗口
            self.$(".children_directory .children_o").click(function(){
                self.$(".chat_content").scrollTo(self.$(".chat_content")[0].scrollHeight);
                self.get_active_info($(this));
            });
        },
        // 获取当前窗口的信息资源
        get_active_info: function(obj){
            var self = this;
            var id = obj.attr("id");

            var loadObj = self.$(".chat_info .load_cont");
            var active_window = self.$(".info_window .info_window_child[data_id='data_"+id+"']");

            self.$(".children_directory .children_o").removeClass('op_active');
            obj.addClass("op_active");
            self.$(".info_window .info_window_child").hide();
            if (active_window.length > 0){
                active_window.show();
            }else{
                // 沟通窗口信息
                loadObj.show();
                var test1 = {
                    name: obj.attr("name"),
                    id: id,
                    is_history: true,
                    send_info: [
                        {
                            name: "101车",
                            img: "",
                            id: "b1",
                            cont: "这是发给你的第一条消息",
                            data_time: "2017/07/20 09:46:20",
                        },
                        {
                            name: "102车",
                            img: "",
                            id: "b2",
                            cont: "这是发给你的第二条消息",
                            data_time: "2017/07/20 15:46:20",
                        }
                    ]
                }
                new communication_info_window(self, test1, self.current_info, loadObj).appendTo(self.$(".info_window"));
            }
            
        },
    });
    core.action_registry.add('lty_dispatch_desktop_widget.communication', communication);

    var communication_info_window = Widget.extend({
        template: "info_window_template",
        init: function(parent, source_channel, current_info, loadObj){
            this._super(parent);
            this.source_channel = source_channel;
            this.current_info = current_info;
            this.loadObj = loadObj;
        },
        start: function(){
            var self = this;
            self.$(".o_content_text").focus();
            _.each(self.source_channel.send_info, function(ret){
                self.$(".chat_content .current_info").append(QWeb.render("chat_model_template", {info: ret}));
            });
            setTimeout(function(){
                self.loadObj.hide();
                self.$el.show();
            },1000);
            self.load_fn();
        },
        load_fn: function(){
            var self = this;

            // 键盘发送消息
            document.onkeydown=function(e){
                if (13 == e.keyCode && e.ctrlKey){
                    self.$(".send_chat .send_cont_bt").click();
                }
            };

            // 发送消息
            self.$(".send_chat .send_cont_bt").click(function(){
                self.send_info_fn($(this));
            });

            // 查看历史数据
            self.$(".history_bt").click(function(){
                var oe_self = $(this);
                self.load_history_info_fn(oe_self);
            });
        },
        // 发送信息
        send_info_fn: function(oe_this){
            var info = oe_this.parents(".send_chat").find(".o_content_text").val().replace(/(^\s*)|(\s*$)/g, "");
            var send_id = oe_this.attr("send_id");
            if (info == ""){
                layer.tips("发送内容不能为空", oe_this);
                return false;
            }

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
            var associated_id = oe_self.attr("associated_id");
            var info_window_child = oe_self.parents(".info_window_child");
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
                    info_window_child.find(".current_info_fgx").show();
                    var history_info = info_window_child.find(".history_info");
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

    var communication_tc_box = Widget.extend({
        template: "communication_tc_box_template",
        init: function(parent){
            this._super(parent);
            this.info = {
                cont: "你有消息没有处理",
                id: "111",
            };
        },
        start: function(){
            if (!this.info){
                return false;
            }
            var self = this;
            var layer_1 = layer.open({type:4});
            var mg = 0;
            var mgT = -65, mgL = -180;
            var index = 15;
            new communication_tc(self, {info: self.info, mgt: mg*index+mgT, mgl: mg*index+mgL, layer_1: layer_1}).appendTo(self.$el);
            // self.$el.append(QWeb.render("communication_tc_template", {info: this.info, mgt: mg*index+mgT, mgl: mg*index+mgL}));
            var set1 = setInterval(function(){
                mg += 1;
                if (mg>5){
                    clearInterval(set1);
                    return false;
                }
                new communication_tc(self, {info: self.info, mgt: mg*index+mgT, mgl: mg*index+mgL, layer_1: layer_1}).appendTo(self.$el);
                // self.$el.append(QWeb.render("communication_tc_template", {info: self.info, mgt: mg*index+mgT, mgl: mg*index+mgL}));
            }, 1500);
        }
    });

    var communication_tc = Widget.extend({
        template: "communication_tc_template",
        init: function(parent, data){
            this._super(parent, data);
            this.def_data = data;
        },
        start: function(){
            this.load_fn();
        },
        load_fn: function(){
            var self = this;
            self.$(".cancel_bt").click(function(){
                self.close_fn($(this));
            });

            self.$(".close_bt").click(function(){
               self.close_fn($(this));
            });
        },
        close_fn: function(oe_this){
            oe_this.parents(".message_warned").remove();
            if ($(".message_warned").length == 0){
                layer.close(this.def_data.layer_1);
            }
        }
    });
    core.action_registry.add('lty_dispatch_desktop_widget.communication_tc', communication_tc_box);

    return communication;
});

