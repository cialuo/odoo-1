/**
 * Created by Administrator on 2017/7/12.
 */
function traffic_distance(canvas) {
    var c = canvas.self.find(canvas.id)[0];
    var cxt = c.getContext("2d");
    cxt.clearRect(0, 0, c.width, c.height);
    var dataAllNum = 0;
    //根据数据算出总dataAlNum
    for (var m = 0; m < canvas.subsection.length; m++) {
        dataAllNum += canvas.subsection[m];
    }
    var dataAll=dataLen=dataLenLeft = 0;
    for (var i = 0; i < canvas.color.length; i++) {
        //计算每一段所占位置的百分比
        dataAll += canvas.subsection[i];
        // 算出当前占比-前面占比算出实际px占比
        dataLen = (canvas.subsection[i] / dataAllNum) * 1190;
        dataLenLeft = ((dataAll - canvas.subsection[i]) / dataAllNum) * 1190;
        //渲染每一段距离的颜色
        cxt.beginPath();
        cxt.fillStyle = canvas.color[i];
        //距离左边距离，上边距离，此段长度，高度
        cxt.fillRect(dataLenLeft, canvas.y, dataLen, 2);
        cxt.closePath();
    }
}
//站点的圆圈以及站点名称
function cir_and_text(canvas) {
    var c = canvas.self.find(canvas.id)[0];
    var cxt = c.getContext('2d');
    for (var i = 0; i < canvas.color.length; i++) {
        //渲染每一个圆点对应的站点名称
        cxt.beginPath();//开启关闭每一个画布的渲染
        cxt.fillStyle = "#A3A6AD";
        cxt.font = "12px 微软雅黑";
        //站点文字居中显示
        cxt.textAlign = "center";
        //文字，左距离，上距离，最大px量
        var mySite = canvas.dataSite[i].name;
        var myColor = canvas.dataSite[i].color;
        if (canvas.dataSite[i].status == 0) {
            mySite = '';
            myColor = '#ffffff';
        } else {
            mySite = canvas.dataSite[i].name;
            myColor = canvas.dataSite[i].color;
        }
        cxt.fillText(mySite, canvas.dataCir[i], canvas.testy, 50);
        cxt.closePath();
        //渲染圆环
        var obj_list = [
            {
                cir: 6,
                color: canvas.dataSite[i].color
            },
            {
                cir: 5,
                color: '#ffffff'
            },
            {
                cir: 4,
                color: myColor
            },
        ]
        for (var j = 0; j < obj_list.length; j++) {
            var obj = obj_list[j];
            cxt.beginPath();
            cxt.arc(canvas.dataCir[i], canvas.ciry, obj.cir, 0, 360, false);
            cxt.fillStyle = obj.color;
            cxt.fill();
            cxt.closePath();
        }
    }
}
//左侧canvas图
function can_left_right(canvas) {
    var lineLeft = staCir = 0;
    var c = canvas.self.find(canvas.id)[0];
    var cxt = c.getContext('2d');
    cxt.clearRect(0, 0, c.width, c.height);
    //画圆
    cxt.beginPath();
    //左边圆圈
    cxt.arc(13, 58, 13, 0, 360, false);
    //线条颜色
    cxt.fillStyle = "white";
    cxt.fill();
    cxt.closePath();
    cxt.beginPath();
    cxt.textAlign = "center";
    cxt.fillStyle = "black";
    //文字，左距离，上距离，最大px量
    cxt.fillText(canvas.busNumber+'辆', 13, 64, 50);
    cxt.fill();
    cxt.closePath();
    cxt.beginPath();
    //绘制直线线条
    cxt.lineWidth = 2;
    cxt.strokeStyle = canvas.color;
    cxt.moveTo(canvas.lineLen, canvas.ciry);
    cxt.lineTo(canvas.lineLen + 9, canvas.ciry);
    cxt.stroke();
    cxt.closePath();
    canvas.lineLen == 0 ? lineLeft = 9 : lineLeft = 17;
    //绘制弧线的半圆
    cxt.beginPath();
    cxt.arc(lineLeft, canvas.ciry + canvas.r, canvas.r, canvas.sta * Math.PI, (canvas.sta + 0.5) * Math.PI, false);
    canvas.sta == 1 ? staCir = 1 : staCir = 0.5;
    cxt.stroke();
    cxt.closePath();
    //绘制线条
    cxt.beginPath();
    cxt.moveTo(13, canvas.ciry + canvas.r);
    cxt.lineTo(13, 45);
    cxt.stroke();
    cxt.closePath();
    // 下面的直线
    cxt.beginPath();
    cxt.moveTo(13, 71);
    cxt.lineTo(13, 85);
    cxt.stroke();
    cxt.closePath();
    //绘制下面弧线的半圆
    cxt.beginPath();
    cxt.arc(lineLeft, 85, canvas.r, (staCir - 0.5) * Math.PI, staCir * Math.PI, false);
    cxt.stroke();
    cxt.closePath();
    cxt.beginPath();
    //绘制直线线条
    cxt.moveTo(canvas.lineLen, 89);
    cxt.lineTo(canvas.lineLen + 9, 89);
    cxt.stroke();
    cxt.closePath();
}
//客流走势轮播组件
function carousel(carousel) {
    var self = carousel.self;
    var content = carousel.content;
    var i = 0;
    var firstcarousel_content = self.$(content + '>li').first().clone(); //复制第一张图片
    //将第一张图片放到最后一张图片后，设置ul的宽度为图片张数*图片宽度
    self.$(content).append(firstcarousel_content).width(self.$(content + '>li').length * 600);
    //定时器自动播放
    var timer = setInterval(function () {
        i++;
        if (i == self.$(content + '>li').length) {
            i = 1;
            self.$(content).css({left: 0});
        }
        ;
        self.$(content).stop().animate({left: -i * 600}, 500);
    }, 3000)
    //鼠标移入，暂停自动播放，移出，开始自动播放
    self.$('.carousel').hover(function () {
        clearInterval(timer);
    }, function () {
        timer = setInterval(function () {
            i++;
            if (i == self.$(content + '>li').length) {
                i = 1;
                self.$(content).css({left: 0});
            }
            ;
            self.$(content).stop().animate({left: -i * 600}, 500);
        }, 3000);
    });
};
//渲染车辆实况的cancvas图像
function qrend_desktop(data, domT, domB, domL, domR, selfDom) {
    var traffic_top = {
        id: domT,
        y: 26,
        self: selfDom,
        subsection: data.subsection,
        color: data.color
    };
    var traffic_bottom = {
        id: domB,
        y: 5,
        self: selfDom,
        subsection: data.subsection,
        color: data.color
    };
    traffic_distance(traffic_top);
    traffic_distance(traffic_bottom);

    var cirTop = {
        id: domT,
        ciry: 27,
        testy: 13,
        color: data.color,
        self: selfDom,
        dataCir: data.dataCir,
        dataSite: data.dataSite
    };
    var cirBottom = {
        id: domB,
        ciry: 6,
        testy: 25,
        self: selfDom,
        color: data.color,
        dataCir: data.dataCir,
        dataSite: data.dataSite2
    };
    cir_and_text(cirTop);
    cir_and_text(cirBottom);
    can_left_right(
        {
            id: domL,
            color: data.color[0],
            ciry: 27,
            self: selfDom,
            r: 4,
            lineLen: 17,
            sta: 1,
            busNumber:data.busNumber
        }
    );
    can_left_right(
        {
            id: domR,
            color: data.color[data.color.length - 1],
            ciry: 27,
            self: selfDom,
            r: 4,
            lineLen: 0,
            sta: 1.5,
            busNumber:data.busNumber
        }
    );
}
//防止冒泡
function stopPropagation(e) {
    e = window.event || e;
    if (document.all) {  //只有ie识别
        e.cancelBubble = true;
    } else {
        e.stopPropagation();
    }
}


