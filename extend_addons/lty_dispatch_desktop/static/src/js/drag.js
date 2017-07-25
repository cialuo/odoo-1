/*-------------------------- +
  获取id, class, tagName
 +-------------------------- */
var get = {
	byId: function(id) {
		return typeof id === "string" ? document.getElementById(id) : id
	},
	byClass: function(sClass, oParent) {
		var aClass = [];
		var reClass = new RegExp("(^| )" + sClass + "( |$)");
		var aElem = this.byTagName("*", oParent);
		for (var i = 0; i < aElem.length; i++) reClass.test(aElem[i].className) && aClass.push(aElem[i]);
		return aClass
	},
	byTagName: function(elem, obj) {
		return (obj || document).getElementsByTagName(elem);
	}
};
var dragMinWidth = 250;
var dragMinHeight = 124;
/*-------------------------- +
  拖拽函数
 +-------------------------- */
function drag(oDrag, handle) {
    var disX = dixY = 0;
    var oMin = get.byClass("min", oDrag)[0];
    handle = handle || oDrag;
    handle.style.cursor = "move";
    handle.onmousedown = function (event) {
        var event = event || window.event;
        disX = event.clientX - oDrag.offsetLeft;
        disY = event.clientY - oDrag.offsetTop;

        document.onmousemove = function (event) {
            var event = event || window.event;
            var iL = event.clientX - disX;
            var iT = event.clientY - disY;
            var maxL = document.documentElement.clientWidth - oDrag.offsetWidth;
            var maxT = document.documentElement.clientHeight - oDrag.offsetHeight;
            iL <= 0 && (iL = 0);
            iT <= 0 && (iT = 0);
            iL >= maxL && (iL = maxL);
            iT >= maxT-50 && (iT = maxT-50);
            oDrag.style.marginTop = 0 + "px";
            oDrag.style.marginLeft = 0 + "px";
            oDrag.style.left = iL + "px";
            oDrag.style.top = iT + "px";
            return false
        };

        document.onmouseup = function () {
            document.onmousemove = null;
            document.onmouseup = null;
            this.releaseCapture && this.releaseCapture();
        };
        this.setCapture && this.setCapture();
        return false
    };
    //最大化按钮
    if(oMin){
        oMin.onclick  = function () {
            oDrag.style.display = "none";
        };
    }
    //阻止冒泡

    //最小化按钮


}
function dragFn(parent, title) {
	var k = 1;
	var c_class = "."+parent + " ." + title;
	$("body").on('mouseover', c_class, function () {
		oDrag = $(this).parents("." + parent)[0];
        if ($.inArray("nofix", oDrag.classList)==-1){
            if ($.inArray("layer_defined", oDrag.classList)!=-1){
                oDrag.style.zIndex = 20000001;
            }else{
                oDrag.style.zIndex = k;
            }
        }
        var oTitle = get.byClass(title, oDrag);
        for (var i=0, l=oTitle.length;i<l;i++){
            drag(oDrag, oTitle[i]);
        }
	});
	$("body").on('mouseout', c_class, function () {
        if ($.inArray("nofix", oDrag.classList)!=-1){
            return false;
        }
        if ($.inArray("layer_defined", oDrag.classList)!=-1){
            oDrag.style.zIndex = 20000000;
            return false;
        }
	    oDrag.style.zIndex = 0;
    })
}
window.onload = window.onresize = function () {
    dragFn("dragContent", "dragArea");
};





