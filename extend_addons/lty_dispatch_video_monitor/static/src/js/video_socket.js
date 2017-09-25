// /**
//  * Created by Administrator on 2017/9/25.
//  */
// var socket_video = null;
// //判断当前浏览器是否支持WebSocket
// if ('WebSocket' in window) {
//     socket_video = new WebSocket("ws://58.82.168.178:8211/lty-video-service/websocket/socketServer.ws?sessionID=ROoOyEijGvmc5y35ZqL15pglIDLjxyUN");
// } else {
//     alert('当前浏览器 Not support websocket')
// }
// //连接发生错误的回调方法
// socket_video.onerror = function () {
//     console.log("WebSocket连接发生错误");
// };
// //连接成功建立的回调方法
// socket_video.onopen = function () {
//     console.log("WebSocket连接成功");
// }
// //接收到消息的回调方法
// socket_video.onmessage = function (event) {
//     console.log(event.data);
// }
// //连接关闭的回调方法
// socket_video.onclose = function () {
//     console.log("WebSocket连接关闭");
// }
// //监听窗口关闭事件，当窗口关闭时，主动去关闭websocket连接，防止连接还没断开就关闭窗口，server端会抛异常。
// window.onbeforeunload = function () {
//     closeWebSocket();
// }
// //关闭WebSocket连接
// function closeWebSocket() {
//     socket_video.close();
// }
// //发送消息
// function send_video_msg() {
//     function buildRequestParam() {
//         //{"msg_type":258,"params":{"bus_id":30000,"channel_id":0 }}
//         return {"msg_type": 258, "params": {"bus_id": 30000, "channel_id": 0}};
//     }
//     socket_video.send(buildRequestParam());
// }
