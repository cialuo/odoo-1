/**
 * Created by Administrator on 2017/9/22.
 */
odoo.define('lty_dispatch_video_monitor.video_show', function (require) {
    var core = require('web.core');
    var Widget = require('web.Widget');
    var Model = require('web.Model');
    var QWeb = core.qweb;
    var video_play = Widget.extend({
        template:'dispatch_desktop_video',
        init: function (parent) {
            this._super(parent);
        },
        start: function () {
            var catData = [];
            var websocket = null;
            var catDataDid = {};
            var dataBusIdShowStatus = 0;
            var onlineData = 0; //在线车辆
            var data = [{
                'id': 22,
                "channels": [{
                    "online": 0,
                    "channel_id": 4
                }, {
                    "online": 1,
                    "channel_id": 5
                }, {
                    "online": 1,
                    "channel_id": 6
                }]
            },
                {
                    'id': 33,
                    "channels": [{
                        "online": 1,
                        "channel_id": 7
                    }, {
                        "online": 1,
                        "channel_id": 8
                    }, {
                        "online": 1,
                        "channel_id": 9
                    }]
                },
            ];
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

            }
            var zTreeNodes = [{
                name: "parent_2",
                id: 111,
                children: [{
                    name: "父节点21 - 展开",
                    id: 11,
                    children: [{
                        name: "叶子节点211",
                        id: 1,
                    },
                        {
                            name: "叶子节点212",
                            id: 2,
                        },
                        {
                            name: "叶子节点213",
                            id: 3
                        }
                    ]
                },
                    {
                        name: "父节点22 - 折叠",
                        id: 22,
                        children: [{
                            name: "叶子节点2212",
                            id: 4
                        },
                            {
                                name: "叶子节点222",
                                id: 5
                            },
                            {
                                name: "叶子节点223",
                                id: 6
                            }
                        ]
                    },
                    {
                        name: "父节点23 - 折叠",
                        id: 33,
                        children: [{
                            name: "叶子节点231",
                            id: 7
                        },
                            {
                                name: "叶子节点232",
                                id: 8
                            },
                            {
                                name: "叶子节点233",
                                id: 9
                            }
                        ]
                    }
                ]
            }];
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
                        websocket.send('{"msg_type":100}');
                        self.serverTimeoutObj = setTimeout(function () {
                            //如果onclose会执行reconnect，我们执行ws.close()就行了.如果直接执行reconnect 会触发onclose导致重连两次
                            websocket.close();
                            sendVideoInit();
                        }, self.serverTimeout);

                    }, this.timeout);
                }
            };
//
            function setFontCss(treeId, treeNode) {
                var css = null;
                if (treeNode.highlight) {
                    css = {color: "#A60000", "font-weight": "bold"};
                    $(this).addClass("highlight");
                } else {
                    css = {color: "#757575", "font-weight": "normal"};
                }

                return css;
            };

            //强制转换数字
            function str2Num(str) {
                return str.replace(/\D/g, '');
            };
            //打开websocket
            function onOpen(openEvt) {
                heartCheck.start();
                console.log('websocket connection!')
            }

            //监听到websocket error
            function onError() {
                console.log('websocket error!');
            }

            //监听到websocket close
            function onClose() {
                console.log('websocket close!');
            }

            //监听到websocket 返回信息
            function onMessage(event) {
                heartCheck.reset();
                var dataJson = $.parseJSON(event.data);
                console.log(dataJson)
                if (dataJson.msg_type == '257') { //第一次加载过来推送的在线
                    onlineData = dataJson.result;
                    heigh_light_show_tree(dataJson.result); //设置在线的状态
                    getVideoOnlines(onlineData, dataJson.result); //断流重连
                } else if (dataJson.msg_type == '512') { //推送在线的状态
                    //				setInterShow(dataJson.result); //设置在线的状态
                    getVideoOnlines(catDataDid, dataJson.result); //断流重连
                } else if (dataJson.msg_type == '259') { //服务器返回播放的地址
                    catDataDid = dataJson; //全局存储对象
                    //				showMonflasitor(dataJson); //回应的地址
                    deal_getData(dataJson)
                }

            }

            //设备通道断流重新去请求
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
                                if (dataJsonVideo.params.channel_id == '-1') { //判断是存在channeld
                                    var videoParams = '{"msg_type":' + channelType + ',"params":{"bus_id":' + busIdStr + ',"channel_id":' + dataJsonVideo.params.channel_id + '}}';
                                } else {
                                    if (dataJsonVideo.params.channel_id == channleStr) {
                                        var videoParams = '{"msg_type":' + channelType + ',"params":{"bus_id":' + busIdStr + ',"channel_id":' + channleStr + '}}';
                                    }
                                }
                                websocket.send(videoParams); //发送参数
                            } else {
                                alert('通道不在线！')
                            }
                        }
                    } else if (dataChangeVideo.online == '0') {
                        alert('设备不在线，无法请求！')
                    }
                }
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

            //msg_type 类型
            //deviceId 设备  cId  通道id
            function sendVideoInit() {
                var SessionId = genSessionId(32);
                //			端口变量参数
                var webUrl = "ws://202.104.136.228:9001/lty-video-service";
                if ('WebSocket' in window) {
                    websocket = new ReconnectingWebSocket(webUrl + "/websocket/socketServer.ws?sessionID=" + SessionId);
                    websocket.timeoutInterval = 12000; //websocket捂手超时时间
                } else if ('MozWebSocket' in window) {
                    websocket = new MozWebSocket(webUrl + "/websocket/socketServer.ws?sessionID=" + SessionId);
                } else {
                    websocket = new SockJS(webUrl + "/sockjs/socketServer.do?sessionID=" + SessionId);
                }
                websocket.onopen = onOpen;
                websocket.onmessage = onMessage;
                websocket.onerror = onError;
                websocket.onclose = onClose;
            }

            //展示当前播放器的播放器和渠道
            function videoOnePlay(videoNum, videoOneList, deviceId, channelId) {
                $("#flashContent" + videoNum).parent('.video_player').find('.show_car').text(deviceId);
                if (channelId >= 0) {
                    channelId = channelId + 1;
                } else {
                    channelId = "";
                }
                $("#flashContent" + videoNum).parent('.video_player').find('.show_car').text(channelId);
            }

            //清空数组
            function removeobj() {
                catData = [];
            }

            function heigh_light_show_tree(dataBusIdShow) {
                var zTreeShow = $.fn.zTree.getZTreeObj("ztree");
                for (var i = 0; i < dataBusIdShow.length; i++) {
                    var node_id = zTreeShow.getNodeByParam("id", dataBusIdShow[i].id, null);
                    if (node_id) {
                        zTreeShow.updateNode(node_id);
                        var node_P = node_id.getParentNode() //获取父节点
                        dataBusIdShowStatus = dataBusIdShow[i].online;
                        if (node_P) {
                            //						展开父节点
                            zTreeShow.expandNode(node_P, true, false, false, false)
                        }
                        //展开子节点
                        zTreeShow.expandNode(node_id, true, false, false, false)
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

            function deal_getData(dataJson) {
                var dataUrl = dataJson.result;
                var deviceId = dataJson.params.bus_id;
                var channelId = dataJson.params.channel_id;
                //			即获取的所有通道
                if (channelId == '-1') {
                    //				removeobj(); //清空数组
                    removeobj(); //清空播放数组
                    //				removeJwplayer(); //清空播放器
                    for (var i = 0; i < dataUrl.length; i++) { //点击设备把所有的url存入对象
                        var deviceData = {"deviceId": deviceId, "channelId": i, "videoUrl": dataUrl[i]};
                        catData.push(deviceData);
                    }
                    cutoverTreePlay(4, dataUrl, deviceId, channelId);
                } else {

                }
            }

            //循环创建展示播放器
            function cutoverTreePlay(num, arrlist, deviceId, channelId) {
                var arrcut = [];
                if (arrlist) { //判断是否存在url，不存在创建空的播放器
                    arrcut = arrlist;
                }
                for (var i = 0; i < num; i++) {
                    if (channelId == '-1') {
                        show_video(i, arrcut, deviceId, channelId); //循环创建播放器
                        //					showSreenPlay(num); //依据屏幕数量设置摆放
                    }
                }
            }

            //		i,播放地址列表,bus_id,channel_id
            function show_video(i, arrcut, deviceId, channelId) {
                var swfVersionStr = "10.3.0";
                var xiSwfUrlStr = "swfs/playerProductInstall.swf";
                var queryParameters = new Array();
                queryParameters['source'] = getUrlParam('source');
                queryParameters['type'] = getUrlParam('type');
                if (queryParameters['source'] == "")
                    queryParameters['source'] = arrcut[0];
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
                var attributes = {};
                attributes.id = "StrobeMediaPlayback";
                attributes.name = "StrobeMediaPlayback";
                attributes.align = "middle";
                $('#flashContent' + i).parent().find('.show_car').show();
                $('#flashContent' + i).parent().find('.now_play').html('当前车辆号：' + deviceId)
                var qudao = i + 1;
                $('#flashContent' + i).parent().find('.now_channel').html('当前渠道：' + qudao)

                var timeShow = setInterval(function () {
                    if ($('body').find('#flashContent').length > 0) {
                        swfobject.embedSWF("/lty_dispatch_video_monitor/static/src/swfs/StrobeMediaPlayback.swf", "flashContent" + i, "650", "350", swfVersionStr, xiSwfUrlStr, soFlashVars, params, attributes);
                        swfobject.createCSS("#flashContent", "display:block;text-align:left;");
                        clearInterval(timeShow);
                    }
                }, 300);
            }

            //		swfobject.createCSS("#flashContent", "display:block;text-align:left;");
            function showIconForTree(treeId, treeNode) {
                return !treeNode.isParent;
            };
//
            function zTreeOnClick(event, treeId, treeNode) {
                var p_name = treeNode.name;
                //			webSocketVideo(channelType, deviceId, channeld)
                //'{"msg_type":258,"params":{"bus_id":8000,"channel_id":0}}'
                var channelType = 258;
                var deviceId = 8000;
                var channelId = -1;
                $('.video_player').addClass('hide');
                if (treeNode.isParent == true) {
                    $('.video_player').removeClass('hide');
                } else {
                    $('.video_player.hide').eq(0).removeClass('hide');
                }
                // webSocketVideo(channelType, deviceId, channelId);
            };
//
//             //		websocket链接请求的视频播放
            function webSocketVideo(channelType, deviceId, channeld) {
                var webzTreeShow = $.fn.zTree.getZTreeObj("ztree");
                var deviceIdscoket = deviceId;
                var nodesocket = webzTreeShow.getNodeByParam("id", 8, null);
                var objsocket = nodesocket.tId + "_span";
                //			如果是有online的才发送请求
                //			if($('#' + objsocket).hasClass('online')) {
                if (channelType == '258') { //点击树请求参数
                    if (!(channeld === '')) { //判断是存在channeld
                        var videoParams = '{"msg_type":' + channelType + ',"params":{"bus_id":' + deviceId + ',"channel_id":' + channeld + '}}';
                    } else {
                        channeld = -1;
                        var videoParams = '{"msg_type":' + channelType + ',"params":{"bus_id":' + deviceId + ',"channel_id":' + channeld + '}}';
                    }
                } else if (channelType == '264') { //通知设备上传日志
                    var videoParams = '{"msg_type":' + channelType + ',"params":{"bus_id":' + deviceId + '}}';
                }
                //				websocket.send('{"msg_type":258,"params":{"bus_id":8000,"channel_id":0}}');
                websocket.send(videoParams); //发送参数
                //			}
            }
                //进来初始化视频列表
                 var timeTree = setInterval(function () {
                    if ($('body').find('#ztree').length > 0) {
                        $.fn.zTree.init($("#ztree"), setting, zTreeNodes)
                        clearInterval(timeTree);
                    }
                }, 300);
                $.fn.zTree.init($("#ztree"), setting, zTreeNodes)
                //websocket初始化
                // sendVideoInit()
                //			高亮在线视频列表
                // heigh_light_show_tree(data)
            // send_video_msg()
        },
    });
    core.action_registry.add('lty_dispatch_video_monitor.video_play', video_play);
});