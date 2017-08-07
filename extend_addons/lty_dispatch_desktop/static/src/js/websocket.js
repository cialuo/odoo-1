/**
 * Created by Administrator on 2017/8/5.
 */
var websocket = null;
//判断当前浏览器是否支持WebSocket
if ('WebSocket' in window) {
    websocket = new SockJS("http://127.0.0.1:8769/wstest?userId=45454");
}
else {
    alert('当前浏览器 Not support websocket');
}
//连接发生错误的回调方法
websocket.onerror = function () {
    console.log("WebSocket连接发生错误");
};
//连接成功建立的回调方法
websocket.onopen = function () {
    console.log("WebSocket连接成功");
}

// 定义模块调用
// 示例 {model: {status: false, arg: {}, fn: ""}, model_list:[]},
var socket_model_info = {};
//接收到消息的回调方法
websocket.onmessage = function (event) {
    // fn(event.data);
    for (var w=0,w=socket_model_info.model_list.length;w<l;w++){
    	var socket_model = socket_model_info[socket_model_info.model_list[w]];
    	if (socket_model.status){
    		if (socket_model.fn){
    			socket_model.fn(event.data, socket_model.arg);
    		}
    	}
    }
};
model_status.model_1[1]=aaaa
//连接关闭的回调方法
websocket.onclose = function () {
    console.log("WebSocket连接关闭");
};
//监听窗口关闭事件，当窗口关闭时，主动去关闭websocket连接，防止连接还没断开就关闭窗口，server端会抛异常。
window.onbeforeunload = function () {
    closeWebSocket();
};

//关闭WebSocket连接
function closeWebSocket() {
    websocket.close();
}

//发送消息
function send() {
    var message = document.getElementById('text').value;
    websocket.send(message);
}
