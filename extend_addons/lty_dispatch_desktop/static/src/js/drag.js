/*-------------------------- +
 获取id, class, tagName
 +-------------------------- */
var get = {
    byId: function (id) {
        return typeof id === "string" ? document.getElementById(id) : id
    },
    byClass: function (sClass, oParent) {
        var aClass = [];
        var reClass = new RegExp("(^| )" + sClass + "( |$)");
        var aElem = this.byTagName("*", oParent);
        for (var i = 0; i < aElem.length; i++) reClass.test(aElem[i].className) && aClass.push(aElem[i]);
        return aClass
    },
    byTagName: function (elem, obj) {
        return (obj || document).getElementsByTagName(elem);
    }
};
/*-------------------------- +
 拖拽函数
 +-------------------------- */
function drag(oDrag, handle, maxL, maxT) {
    var disX  = 0;
    var disY = 0;
    handle = handle || oDrag;
    handle.style.cursor = "move";
    handle.onmousedown = function (e) {
        var event = e || window.event;
        disX = event.clientX - oDrag.offsetLeft;
        disY = event.clientY - oDrag.offsetTop;

        document.onmousemove = function (e) {
            var event = e || window.event;
            var iL = event.clientX - disX;
            var iT = event.clientY - disY;
            if (maxL) {
                var maxdL = maxL;
            } else {
                var maxdL = document.documentElement.clientWidth - oDrag.offsetWidth;
            }
            if (maxT) {
                var maxdT = maxT;
            } else {
                var maxdT = document.documentElement.clientHeight - oDrag.offsetHeight;
            }
            if(maxT){
                var mindL =- oDrag.offsetWidth;
            }else{
                var mindL = 0;
            }
            iL <= mindL && (iL = mindL );
            iT <= 50 && (iT = 50 );
            iL >= maxdL && (iL = maxdL );
            iT >= maxdT - 50 && (iT = maxdT - 50 );
            oDrag.style.marginTop = 0 + "px";
            oDrag.style.marginLeft = 0 + "px";
            oDrag.style.left = iL + "px";
            oDrag.style.top = iT + "px";
            return false;
        };

        document.onmouseup = function (e) {
            e.stopPropagation();
            document.onmousemove = null;
            document.onmouseup = null;
            this.releaseCapture && this.releaseCapture();
        };
        this.setCapture && this.setCapture();
        return false;
    };
}
var timmerHandle = null;
var isDrag = false;
var k = 1;
function dragFn(parent, title, maxL, maxT) {
    var c_class = "." + parent + " ." + title;
    var p_class = "." + parent;
    $("body").on('mouseover', c_class, function () {
        var oDrag = $(this).parents("." + parent)[0];
        // var oDrag = $(this).parents(parent)[0];
        if ($.inArray("nofix", oDrag.classList) == -1) {
            if ($.inArray("layer_defined", oDrag.classList) != -1) {
                oDrag.style.zIndex = 20000001;
            } else {
                // oDrag.style.zIndex = 2;
            }
        }
        var oTitle = get.byClass(title, oDrag);
        for (var i = 0, l = oTitle.length; i < l; i++) {
            drag(oDrag, oTitle[i], maxL, maxT);
        }
    });
    $("body").on('mousedown', p_class, function (e) {
        if (typeof($(this).attr("click")) == "undefined") {
            k++;
        }
        $('*[click="yes"]').removeAttr('click');
        $(this).attr("click", "yes");
        var oDrag = $(this)[0];
        oDrag.style.zIndex = k;
    });
    function setDragTrue() {
        isDrag = true;
    }

    $("body").on('mousedown', c_class, function () {
        isDrag = false;
        timmerHandle = setTimeout(setDragTrue, 200);
    });
}
window.onload = window.onresize = function () {
    dragFn("dragContent", "dragArea", document.documentElement.clientWidth, document.documentElement.clientHeight);
    dragFn("dragContent", "dragAreaDesk");
};





