/**
 * Created by Administrator on 2017/10/11.
 */
odoo.define('lty_dispatch_broadcast_monitor.broadcast_show', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var Model = require('web.Model');
    var QWeb = core.qweb;
    var ztree_show_dian = Widget.extend({
        template: 'ztree_show_dian',
        init: function (parent) {
            this._super(parent);
        },
        start: function () {
        }

    });
    var broadcast_play = Widget.extend({
        template: 'dispatch_desktop_broadcast',
        init: function (parent) {
            this._super(parent);
            this.model_route_line = new Model('fleet.vehicle');
        },
        start: function () {
            new ztree_show_dian(this).appendTo(this.$el.find('.content-left'));
            var self = this;
            //后期修改
            var channelType = 16;
            var deviceId = 9990;
            var ztreeClick = {};
            this.$el.find('#datetimepicker').datetimepicker({
                format: 'YYYY-MM-DD',
                locale: moment.locale('zh-cn')
            });
            this.model_route_line.query().order_by('route_id').filter([["route_id", "!=", false]]).all().then(function (res) {
                var arr = [];
                for (var i = 0; i < res.length; i++) {
                    arr.push([res[i].route_id, [res[i].on_boardid]]);
                }
                var n = 0;
                var newArr = [];
                for (var j = 0; j < arr.length; j++) {
                    if (arr[j + 1] != undefined) {
                        if (arr[j][0][0] != arr[j + 1][0][0]) {
                            newArr.push(arr.slice(n, j + 1));
                            n = j + 1;
                        } else {
                            arr[n][1].push(arr[j + 1][1][0]);
                        }
                    } else {
                        newArr.push(arr[n]);
                    }

                }
                var end_arr = []
                for (var h = 0; h < newArr.length; h++) {
                    if (h == newArr.length - 1) {
                        end_arr.push(newArr[h]);
                    } else {
                        end_arr.push(newArr[h][0]);

                    }
                }
                var arr_node = [];
                for (var m = 0; m < end_arr.length; m++) {
                    var arr_node_child = [];

                    for (var y = 0; y < end_arr[m][1].length; y++) {
                        arr_node_child.push(
                            {
                                name: end_arr[m][1][y],
                                id: end_arr[m][1][y],
                                children: [{
                                    name: "渠道1",
                                    id: 1,
                                },
                                    {
                                        name: "渠道2",
                                        id: 2,
                                    },
                                    {
                                        name: "渠道3",
                                        id: 3
                                    },
                                    {
                                        name: "渠道4",
                                        id: 4
                                    }
                                ]
                            }
                        );
                    }
                    arr_node.push({
                        name: end_arr[m][0][1],
                        id: end_arr[m][0][1],
                        children: arr_node_child
                    });
                }
                var setting = {
                    view: {
                        showIcon: false,
                        fontCss: setFontCss
                    },
                    data: {
                        simpleData: {
                            enable: true
                        }
                    },
                    callback: {
                        onClick: zTreeOnClick
                    }

                };
                $.fn.zTree.init(self.$el.find("#ztree"), setting, arr_node);
                //进来初始化视频列表

                //websocket初始化
                sendVideoInit()
                //			高亮在线视频列表
                // heigh_light_show_tree(data_tree);
            });
            this.$el.find('.show_broadcast_list').on('click', 'li', function (event) {
                $('.broadcast_player.hide').removeClass('hide');
                $('.content-right').html('');
                var x = event.currentTarget;
                var index = $(x).attr('index');
                $(x).addClass('beChs').siblings().removeClass('beChs');
                var channelId = ztreeClick.treeChanelid;
                $('.content-right').append($('.broadcast_box').html());
                $('.content-right .broadcast_show_box').eq(0).find('.broadcast_box_player').attr('id', 'flashContent0')
                var videoParams = '{"msg_type":17,"params":{"bus_id":' + deviceId + ',"channel_id":' + channelId + ',"index":' + index + ',"minutes":6}}';
                video_socket.send(videoParams); //发送参数
            })
            this.$el.find('.search_date_btn').click(function () {
                if (ztreeClick.treeChanelid != undefined) {
                    var search_date_val = self.$el.find('.datetimepicker').val();
                    if (search_date_val != '') {
                        var date_zz = /^[1-9]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[1-2][0-9]|3[0-1])$/;
                        if (date_zz.test(search_date_val)) {
                            var date_num = search_date_val.split('-');
                            var videoParams = '{"msg_type":' + channelType + ',"params":{"bus_id":' + deviceId + ',"channel_id":' + ztreeClick.treeChanelid + ',"begin":"' + date_num.join('') + '000000","end":"' + date_num.join('') + '235959"}}';
                            video_socket.send(videoParams); //发送参数
                            console.log(videoParams);
                        } else {
                            layer.msg("日期格式不正确");
                        }
                    } else {
                        layer.msg('请输入查询日期');
                    }
                } else {
                    layer.msg('请选择车辆渠道');
                }
            });
            var data_tree = [{
                'id': 9990,
                "channels": [{
                    "online": 0,
                    "channel_id": 1
                }, {
                    "online": 1,
                    "channel_id": 2
                }, {
                    "online": 1,
                    "channel_id": 3
                }]
            },
                {
                    'id': 4103,
                    "channels": [{
                        "online": 1,
                        "channel_id": 1
                    }, {
                        "online": 1,
                        //channel_id
                        "channel_id": 2
                    }, {
                        "online": 1,
                        "channel_id": 3
                    }]
                },
            ];
            //心跳包检测
            var heartCheck = {
                timeout: 10000, //10秒发送一次心跳包
                serverTimeout: 60000, //服务端60秒没有响应重连
                timeoutObj: null,
                serverTimeoutObj: null,
                reset: function () {
                    clearTimeout(this.timeoutObj);
                    clearTimeout(this.serverTimeoutObj);
                    this.start();
                },
                start: function () {
                    var self = this;
                    this.timeoutObj = setTimeout(function () {
                        //发送心跳包
                        video_socket.send('{"msg_type":100}');
                        self.serverTimeoutObj = setTimeout(function () {
                            //如果onclose会执行reconnect，我们执行ws.close()就行了.如果直接执行reconnect 会触发onclose导致重连两次
                            video_socket.close();
                            sendVideoInit();
                        }, self.serverTimeout);

                    }, this.timeout);
                }
            };

            function setFontCss(treeId, treeNode) {
                var css = null;
                if (treeNode.highlight) {
                    css = {color: "#A60000", "font-weight": "bold"};
                    $(this).addClass("highlight");
                } else {
                    css = {color: "#757575", "font-weight": "normal"};
                }
                return css;
            }

//
            //强制转换数字
            function str2Num(str) {
                return str.replace(/\D/g, '');
            }

            //打开websocket
            function onOpen(openEvt) {
                heartCheck.start();
                console.log('websocket connection!');
            }

            //监听到websocket error
            function onError() {
                console.log('websocket error!');
            }

            //监听到websocket close
            function onClose() {
                console.log('websocket close!');
            }

//             //监听到websocket 返回信息
            function onMessage(event) {
                console.log(event.data)
                heartCheck.reset();
                var dataJson = $.parseJSON(event.data);
                if (dataJson.msg_type == '257') { //第一次加载过来推送的在线
                    onlineData = dataJson.result;
                    // heigh_light_show_tree(dataJson.result); //设置在线的状态
                    // getVideoOnlines(onlineData, dataJson.result); //断流重连
                } else if (dataJson.msg_type == 33) { //服务器视频播放的地址
                    console.log(dataJson);
                    var url = dataJson.result.url_wan
                    deal_getData(dataJson);
                    // getVideoOnlines(catDataDid, dataJson.result); //断流重连
                } else if (dataJson.msg_type == 32) { //服务器列表的地址
                    catDataDid = dataJson; //全局存储对象
                    var data_date = dataJson.result;
                    var dom = '';
                    var substart = '';
                    var subend = '';
                    if (data_date.length > 0) {
                        self.$el.find('.show_broadcast_list').html('');
                        for (var i = 0; i < data_date.length; i++) {
                            substart = data_date[i].begin.substring(8, 10) + ':' + data_date[i].begin.substring(10, 12) + ':' + data_date[i].begin.substring(12, 14);
                            subend = data_date[i].end.substring(8, 10) + ':' + data_date[i].end.substring(10, 12) + ':' + data_date[i].end.substring(12, 14);
                            dom += "<li index='" + data_date[i].index + "'><span>" + substart + "</span><span>------</span><span>" + subend + "</span></li>"
                        }
                        self.$el.find('.show_broadcast_list').append(dom);
                    } else {
                        layer.msg('输入日期内暂无视频');
                    }

                }
            }

            //设备渠道断流重新去请求
            function getVideoOnlines(dataJsonVideo, dataChangeVideo) {
                var busIdStr = dataChangeVideo[0].bus_id;
                if (dataJsonVideo && dataJsonVideo.params && dataJsonVideo.params.bus_id && dataJsonVideo.params.bus_id == busIdStr) {
//			busIdStr = busIdStr.substring(1, busIdStr.length);
                    if (dataChangeVideo[0].online == '1') {
                        var channellen = dataChangeVideo[0].channels.length;
                        for (var m = 0; m < channellen; m++) {
                            if (dataChangeVideo[0].channels[m].online == '1') {
                                var channleStr = dataChangeVideo[0].channels[m].channel_id;
                                channleStr = parseInt(channleStr.substr(channleStr.length - 1, 1));
                                var videoParams = '';
                                if (dataJsonVideo.params.channel_id == '-1') { //判断是存在channeld
                                    videoParams = '{"msg_type":' + channelType + ',"params":{"bus_id":' + busIdStr + ',"channel_id":' + dataJsonVideo.params.channel_id + '}}';
                                } else {
                                    if (dataJsonVideo.params.channel_id == channleStr) {
                                        videoParams = '{"msg_type":' + channelType + ',"params":{"bus_id":' + busIdStr + ',"channel_id":' + channleStr + '}}';
                                    }
                                }
                                video_socket.send(videoParams); //发送参数
                            } else {
                                alert('渠道不在线！');
                            }
                        }
                    } else if (dataChangeVideo.online == '0') {
                        alert('设备不在线，无法请求！')
                    }
                }
            }

            function sendVideoInit() {
                var SessionId = genSessionId(32);
                //			端口变量参数
                var webUrl = "ws://202.104.136.228:9001/lty-video-service";
                if ('WebSocket' in window) {
                    video_socket = new ReconnectingWebSocket(webUrl + "/websocket/socketServer.ws?sessionID=" + SessionId);
                    video_socket.timeoutInterval = 12000; //websocket捂手超时时间
                } else if ('MozWebSocket' in window) {
                    video_socket = new MozWebSocket(webUrl + "/websocket/socketServer.ws?sessionID=" + SessionId);
                } else {
                    video_socket = new SockJS(webUrl + "/sockjs/socketServer.do?sessionID=" + SessionId);
                }
                video_socket.onopen = onOpen;
                video_socket.onmessage = onMessage;
                video_socket.onerror = onError;
                video_socket.onclose = onClose;
            }

            //动态生成sessionId
            function genSessionId(length) {
                genSessionId.characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
                var str = genSessionId.characters;
                if (!"0" [0]) { //fix IE67
                    str = str.split("");
                }
                for (var i = 0, id = "", len = str.length; i < length; i++) {
                    id += str[Math.floor(Math.random() * len)];
                }
                return id;
            }

            function heigh_light_show_tree(dataBusIdShow) {
                var time_ztreeobj = setInterval(function () {
                    if ($('#ztree').length > 0) {
                        var zTreeShow = $.fn.zTree.getZTreeObj("ztree");
                        clearInterval(time_ztreeobj)
                        for (var i = 0; i < dataBusIdShow.length; i++) {
                            var node_id = zTreeShow.getNodeByParam("id", dataBusIdShow[i].id, null);
                            if (node_id) {
                                zTreeShow.updateNode(node_id);
                                var node_P = node_id.getParentNode(); //获取父节点
                                dataBusIdShowStatus = dataBusIdShow[i].online;
                                if (node_P) {
                                    zTreeShow.expandNode(node_P, true, false, false, false);
                                }
                                //展开子节点
                                zTreeShow.expandNode(node_id, true, false, false, false);
                                var obj = node_id.tId + "_span";
                                for (var j = 0; j < dataBusIdShow[i].channels.length; j++) {
                                    dataBusIdShow[i].channels[j].channel_id = dataBusIdShow[i].channels[j].channel_id;
                                    var nodeLen = node_id.children.length;
                                    for (var n = 0; n < nodeLen; n++) {
                                        if (dataBusIdShow[i].channels[j].online == 1) {
                                            var objChild = node_id.children[n].tId + '_span';
                                            if (dataBusIdShow[i].channels[j].channel_id == node_id.children[n].id) {
                                                $('#' + objChild).addClass('online');
                                                $('#' + obj).addClass('online');
                                            } else if (dataBusIdShow[i].channels[j].online == '0') {
                                                var objChild = node_id.children[n].tId + "_span";
                                                $('#' + objChild).removeClass('online');
                                                $('#' + obj).removeClass('online');
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }, 300);
            }


            function getUrlParam(name) {
                name = name.replace(/[\[]/, "\\\[").replace(/[\]]/, "\\\]");
                var regexS = "[\\?&]" + name + "=([^&#]*)";
                var regex = new RegExp(regexS);
                var results = regex.exec(window.location.href);

                if (results == null)
                    return "";
                else
                    return unescape(results[1]);

            }

            //点击树初始化视频播放列表
            //channelId 设备id
            //清空数组
            function removeobj() {
                catData = [];
            }

            function deal_getData(dataJson) {
                var deviceId = dataJson.params.bus_id;
                var channelId = dataJson.params.channel_id;
                var arrcut = dataJson.result.url_wan;
                //			即获取的所有渠道
                show_video(arrcut, deviceId, channelId);
            }

            //播放地址列表,bus_id,channel_id
            function show_video(arrcut, deviceId, channelId) {
                var swfVersionStr = "10.3.0";
                var xiSwfUrlStr = "swfs/playerProductInstall.swf";
                var queryParameters = new Array();
                queryParameters['source'] = getUrlParam('source');
                queryParameters['type'] = getUrlParam('type');
                if (queryParameters['source'] == "")
                    queryParameters['source'] = arrcut;
                if (queryParameters['type'] == "")
                    queryParameters['type'] = "recorded";
                if (queryParameters['idx'] == "")
                    queryParameters['idx'] = "2";
                var soFlashVars = {
                    src: queryParameters['source'],
                    streamType: queryParameters['type'],
                    autoPlay: "true",
                    //自动播放功能
                    controlBarAutoHide: "true",
                    controlBarPosition: "bottom"
                };
                var params = {};
                params.quality = "high";
                params.bgcolor = "#000000";
                params.allowscriptaccess = "sameDomain";
                params.allowfullscreen = "true";
                params.scale = "showall";
                var attributes = {};
                attributes.id = "StrobeMediaPlayback";
                attributes.name = "StrobeMediaPlayback";
                attributes.align = "middle";
                attributes.scale = "showall";
                // for(var j = 0;j<$('.video_player').length;j++){
                // 因为数据乃后台返回，无须做处理
                $('#flashContent0').parents('.broadcast_player').find('.show_car').show();
                $('#flashContent0').parents('.broadcast_player').find('.now_play').html('当前车辆号：' + deviceId)
                // }
                $('#flashContent0').parents('.broadcast_player').find('.now_channel').html('当前渠道：' + channelId)
                var timeShow = setInterval(function () {
                    if ($('body').find('#flashContent0').length > 0) {
                        swfobject.embedSWF("/lty_dispatch_video_monitor/static/src/swfs/StrobeMediaPlayback.swf", "flashContent0", "550", "350", swfVersionStr, xiSwfUrlStr, soFlashVars, params, attributes);
                        swfobject.createCSS("#flashContent", "display:block;text-align:left;");
                        // else if (channelId == -1) {
                        //     $('#flashContent' + i).parents('.broadcast_player').find('.show_car').show();
                        //     $('#flashContent' + i).parents('.broadcast_player').find('.now_play').html('当前车辆号：' + deviceId)
                        //     swfobject.embedSWF("/lty_dispatch_video_monitor/static/src/swfs/StrobeMediaPlayback.swf", "flashContent" + i, "550", "350", swfVersionStr, xiSwfUrlStr, soFlashVars, params, attributes);
                        //     swfobject.createCSS("#flashContent", "display:block;text-align:left;");
                        // }
                        clearInterval(timeShow);
                    }
                }, 300);
            }

            //		swfobject.createCSS("#flashContent", "display:block;text-align:left;");
            function showIconForTree(treeId, treeNode) {
                return !treeNode.isParent;
            };
            function zTreeOnClick(event, treeId, treeNode) {
                ztreeClick = {};
                //'{"msg_type":258,"params":{"bus_id":8000,"channel_id":0}}'
                $('.broadcast_player.hide').removeClass('hide');
                $('.content-right').html('');
                // if ($(dom_chose).hasClass('online')) {
                if (treeNode.isParent != true) {
                    //添加播放器盒子
                    ztreeClick.treeBusid = treeNode.getParentNode().id;
                    ztreeClick.treeChanelid = treeNode.id;
                    console.log(ztreeClick)
                }
            };
//             //		websocket链接请求的视频播放

        },
        events: {
            'keypress .search_road': 'show_video_tree',
        },
        show_video_tree: function (event) {
            if (event.keyCode == 13) {
                var searchCondition = this.$el.find('.search_road').val();
                //<2>.得到模糊匹配搜索条件的节点数组集合
                if (searchCondition != "") {
                    var treeObj = $.fn.zTree.getZTreeObj("ztree");
                    treeObj.cancelSelectedNode()
                    var node = treeObj.getNodeByParam('name', searchCondition);//获取id为1的点
                    if (node != null) {
                        treeObj.selectNode(node);
                        var nodes = treeObj.getSelectedNodes();
                        treeObj.expandNode(nodes[0], true, true, true)
                    } else {
                        layer.msg('输入线路或车辆无效');
                    }
                }
            }
        },
    });
    core.action_registry.add('lty_dispatch_broadcast_monitor.broadcast_play', broadcast_play);
});