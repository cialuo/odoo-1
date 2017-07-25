/**
 * Created by Administrator on 2017/7/12.
 */
function traffic_distance(canvas) {
    var cId = canvas.id;
    var y = canvas.y;
    var self = canvas.self;
    var subsection = canvas.subsection;
    var color = canvas.color;
    var c = self.find(cId)[0];
    var cxt = c.getContext("2d");
    var dataAllNum = 0;
    //根据数据算出总dataAlNum
    for (var m = 0; m < subsection.length; m++) {
        dataAllNum += subsection[m];
    }
    var dataAll = datalen = dataLenLeft = 0;
    for (var i = 0; i < color.length; i++) {
        //计算每一段所占位置的百分比
        dataAll += subsection[i];
        // 算出当前占比-前面占比算出实际px占比
        dataLen = (subsection[i] / dataAllNum) * 1190;
        dataLenLeft = ((dataAll - subsection[i]) / dataAllNum) * 1190;
        //渲染每一段距离的颜色
        cxt.beginPath();
        cxt.fillStyle = color[i];
        //距离左边距离，上边距离，此段长度，高度
        cxt.fillRect(dataLenLeft, y, dataLen, 2);
        cxt.closePath();
    }
}
//站点的圆圈以及站点名称
function cir_and_text(canvas) {
    var cId = canvas.id;
    var ciry = canvas.ciry;
    var testy = canvas.testy;
    var self = canvas.self;
    var color = canvas.color;
    var dataCir = canvas.dataCir;
    var dataSite = canvas.dataSite;
    var c = self.find(cId)[0];
    var cxt = c.getContext('2d');
    for (var i = 0; i < color.length; i++) {
        //渲染每一个圆点对应的站点名称
        cxt.beginPath();//开启关闭每一个画布的渲染
        cxt.fillStyle = "#A3A6AD";
        cxt.font = "12px 微软雅黑";
        //站点文字居中显示
        cxt.textAlign = "center";
        //文字，左距离，上距离，最大px量
        var mySite = dataSite[i].name;
        var myColor = dataSite[i].color;
        if (dataSite[i].status == 0) {
            mySite = '';
            myColor = '#ffffff';
        } else {
            mySite = dataSite[i].name;
            myColor = dataSite[i].color;
        }
        cxt.fillText(mySite, dataCir[i], testy, 50);
        cxt.closePath();
        //渲染圆环
        var obj_list = [
            {
                cir: 6,
                color: dataSite[i].color
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
            cxt.arc(dataCir[i], ciry, obj.cir, 0, 360, false);
            cxt.fillStyle = obj.color;
            cxt.fill();
            cxt.closePath();
        }
    }
}
//左侧canvas图
function can_left(canvas) {
    // canvas的id
    var cId = canvas.id;
    // 线条颜色
    var color = canvas.color;
    // 距离Y轴距离
    var ciry = canvas.ciry;
    var self = canvas.self;
    // 圆弧的半径
    var r = canvas.r;
    //线条起点
    var lineLen = canvas.lineLen;
    var sta = canvas.sta;
    var lineLeft = staCir = 0;
    var c = self.find(cId)[0];
    var cxt = c.getContext('2d');
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
    cxt.fillText('3辆', 13, 64, 50);
    cxt.fill();
    cxt.closePath();
    cxt.beginPath();
    //绘制直线线条
    cxt.lineWidth = 2;
    cxt.strokeStyle = color;
    cxt.moveTo(lineLen, ciry);
    cxt.lineTo(lineLen + 9, ciry);
    cxt.stroke();
    cxt.closePath();
    lineLen == 0 ? lineLeft = 9 : lineLeft = 17;
    //绘制弧线的半圆
    cxt.beginPath();
    cxt.arc(lineLeft, ciry + r, r, sta * Math.PI, (sta + 0.5) * Math.PI, false);
    sta == 1 ? staCir = 1 : staCir = 0.5;
    cxt.stroke();
    cxt.closePath();
    //绘制线条
    cxt.beginPath();
    cxt.moveTo(13, ciry + r);
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
    cxt.arc(lineLeft, 85, r, (staCir - 0.5) * Math.PI, staCir * Math.PI, false);
    cxt.stroke();
    cxt.closePath();
    cxt.beginPath();
    //绘制直线线条
    cxt.moveTo(lineLen, 89);
    cxt.lineTo(lineLen + 9, 89);
    cxt.stroke();
    cxt.closePath();
}
//客流走势轮播组件
function carousel(carousel) {
    var self =carousel.self;
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
function qrend_desktop(data, domT, domB, domL, domR,selfDom) {
    var dataCir = data.oneline.site_to_startpoint;
    var color = data.oneline.plan_feedback;
    var dataSite = data.oneline.siteTop;
    var dataSite2 = data.oneline.siteBottom;
    var subsection = data.oneline.traffic_distance;
    var traffic_top = {
        id: domT,
        y: 26,
        self: selfDom,
        subsection: subsection,
        color: color
    };
    var traffic_bottom = {
        id: domB,
        y: 5,
        self: selfDom,
        subsection: subsection,
        color: color
    };
    traffic_distance(traffic_top);
    traffic_distance(traffic_bottom);

    var cirTop = {
        id: domT,
        ciry: 27,
        testy: 13,
        color: color,
        self: selfDom,
        dataCir: dataCir,
        dataSite: dataSite
    };
    var cirBottom = {
        id: domB,
        ciry: 6,
        testy: 25,
        self: selfDom,
        color: color,
        dataCir: dataCir,
        dataSite: dataSite2
    };
    cir_and_text(cirTop);
    cir_and_text(cirBottom);
    can_left(
        {
            id: domL,
            color: color[0],
            ciry: 27,
            self: selfDom,
            r: 4,
            lineLen: 17,
            sta: 1
        }
    );
    can_left(
        {
            id: domR,
            color: color[color.length - 1],
            ciry: 27,
            self: selfDom,
            r: 4,
            lineLen: 0,
            sta: 1.5,
        }
    );
}
//防止冒泡
function stopPropagation(e){
    e=window.event||e;
    if(document.all){  //只有ie识别
        e.cancelBubble=true;
    }else{
        e.stopPropagation();
    }
}