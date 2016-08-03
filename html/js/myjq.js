//ajax加载数据
function loadRightData(address,requestType,getdata,ani){
	if(!address){
		return;
	}
	if($("#load_data").is(":animated")){
		return;
	}
	
	if(!ani && !$("#load_data").is(":animated")){
		//向下滑动
		$("#load_data").animate({top:$(window).height()-108});
		$('body').animate({scrollTop:0});
	}
	
			$("#loading").show();
	
	$.ajax({
		type:requestType,
		url: address,
		data: getdata,
		deforeSend: function(XMLHttpRequest){
		},
		success: function(data){
			
			$('#load_data').empty();   //清空resText里面的所有内容
			$('#load_data').html(data);
			$('.right_navigation').html($('.location').html());
			$('.location').remove();
			$('.right_navigation a:not(.tohome)').click(function(){
				rightATagClickListener($(this),'');
				return false;
			});
			
			$("#loading").css({"height":$(window).height()-108,"top":"35px"});
			$("#loading_text").css({"margin-top":($(window).height()-108)/2});
			
			//文本不会被拖动选中
			document.body.onselectstart = document.body.ondrag = function(){
			return false;
			}
			
			//向上滑动
			$("#load_data").animate({top:0},"normal",function(){
			
				$("#loading").hide();
				$('body').animate({scrollTop:0});
			});
			//alert($('body').scrollTop());
			//if($('body').scrollTo()<0){
//				$('body').scrollTo(0);
//			}
		},
		error:function(XMLHttpRequest, textStatus, errorThrown){
			$('#load_data').empty();   //清空resText里面的所有内容
			$('#load_data').html("请求失败");
			
			//文本不会被拖动选中
			document.body.onselectstart = document.body.ondrag = function(){
			return false;
			}
			//向上滑动
			$("#load_data").animate({top:0},"normal",function(){
			
				$("#loading").hide();
			});
		}
	});

}

//右侧a标签点击响应事件
function rightATagClickListener(a,data){
	loadRightData(a.attr('href'),'post',data,true);
}

//警告

function jinggao(text){
	$("#load_data").append('<div class="jinggaoout">'+
			'<div class="jinggao">'+
				'<div class="jinggaocontent">'+text+'</div>'+
				'<div class="jinggaobtn">确定</div>'+
			'</div></div>');
	$(".jinggaoout").css("height",$(window).height());
		
}

//验证付款字段输入是否合法
function payLegal(){
	$paycard = $('#paycard').attr('value');

	if($paycard=='' || $paycard==' '){
	
		jinggao("请输入付款卡号");
		$this = $(this);
		$(".jinggaobtn").click(function(){
			$(".jinggaoout").remove();	
			$('#paycard').focus();
		});
		return false;
		
	}


	$receivecard = $('#receivecard').attr('value');

	if($receivecard=='' || $receivecard==' '){
		jinggao("请输入收款卡号");
		$this = $(this);
		$(".jinggaobtn").click(function(){
			$(".jinggaoout").remove();	
			$('#receivecard').focus();
		});
		return false;
	}

	$amount = $('#money').attr('value');
	if ($amount=='' || $amount==' ' || $amount<=0 || isNaN($amount)) {
		jinggao("请输入付款金额");
		$this = $(this);
		$(".jinggaobtn").click(function(){
			$(".jinggaoout").remove();	
			showKeyboardMoney();
		});
		return false;
	}

	return true;

}

function payLegalShop(){

	rate = $('#rate').attr('value');
	if (isNaN(rate) || rate<=0 || rate > 10) {
	
		jinggao("请输入正确折扣");
		$this = $(this);
		$(".jinggaobtn").click(function(){
			$('#rate').focus();
		});
		
		return false;
	}
	return true;
}
//验证用户名卡号是否正确
function isrealCard(cardid,cardname){
	result = checkCard(cardid);
	return result['stat'];
}

//提交支付
function toPay(info,address){
	var result;

	$.ajax({
		type:'post',
		url: address,
		async: false,
		data: info,
		success: function(data){
			eval('result='+data);
		}
	});
	return result;
}

//ajax_post
function ajaxPost(info,address){
	var result;
	$.ajax({
		type:'post',
		url: address,
		async: false,
		data: info,
		success: function(data){
			eval('result='+data);
		}
	});
	return result;
}

function buyOrder(address){
	var result;
	$.ajax({
		type:'get',
		url: address,
		async: false,
		data: '',
		success: function(data){
			eval('result='+data);
		}
	});
	return result;
}

function changeCNAMoney(money){
    //debugger;
    var IntNum,PointNum,IntValue,PointValue,unit,moneyCNY;
    var Number  = "零壹贰叁肆伍陆柒捌玖";
    var NUMUnit = { LING : "零",SHI : "拾",BAI : "佰",QIAN : "仟",WAN : "万",YI : "亿" }
    var CNYUnit = { YUAN : "元",JIAO : "角",FEN : "分",ZHENG : "整" };
    var beforeReplace = 
    {
        Values :
        [
            {Name: NUMUnit.LING + NUMUnit.YI},               // 零亿
            {Name: NUMUnit.LING + NUMUnit.WAN},              // 零万
            {Name: NUMUnit.LING + NUMUnit.QIAN},             // 零千
            {Name: NUMUnit.LING + NUMUnit.BAI},              // 零百
            {Name: NUMUnit.LING + NUMUnit.SHI},              // 零十
            {Name: NUMUnit.LING + NUMUnit.LING},             // 零零
            {Name: NUMUnit.YI + NUMUnit.LING + NUMUnit.WAN}, // 亿零万
            {Name: NUMUnit.LING + NUMUnit.YI},               // 零亿
            {Name: NUMUnit.LING + NUMUnit.WAN},              // 零万
            {Name: NUMUnit.LING + NUMUnit.LING}              // 零零
        ]
    };
    var afterReplace = 
    {
        Values :
        [
            {Name: NUMUnit.YI + NUMUnit.LING}, //亿零
            {Name: NUMUnit.WAN + NUMUnit.LING},//万零
            {Name: NUMUnit.LING},              //零
            {Name: NUMUnit.LING},              //零
            {Name: NUMUnit.LING},              //零
            {Name: NUMUnit.LING},              //零
            {Name: NUMUnit.YI + NUMUnit.LING}, //亿零
            {Name: NUMUnit.YI},                //亿
            {Name: NUMUnit.WAN},               //万
            {Name: NUMUnit.LING}               //零
        ]
    };
    var pointBefore = 
    {
        Values :
        [
            {Name: NUMUnit.LING + CNYUnit.JIAO}, //零角
            {Name: NUMUnit.LING + CNYUnit.FEN},  //零分
            {Name: NUMUnit.LING + NUMUnit.LING}, //零零
            {Name: CNYUnit.JIAO + NUMUnit.LING}  //角零
        ]
    };
    var pointAfter = 
    {
        Values :
        [
            {Name: NUMUnit.LING}, //零
            {Name: NUMUnit.LING}, //零
            {Name: ""},
            {Name: CNYUnit.JIAO}  //角
        ]
    };
    
    /// 递归替换
    var replaceAll = function(inputValue,beforeValue,afterValue)
    {
        while(inputValue.indexOf(beforeValue) > -1)
        {
            inputValue = inputValue.replace(beforeValue,afterValue);
        }
        return inputValue;
    }
    /// 获取输入金额的整数部分
    IntNum = money.indexOf(".") > -1 ? money.substring(0,money.indexOf(".")) : money;
    /// 获取输入金额的小数部分
    PointNum = money.indexOf(".") > -1 ? money.substring(money.indexOf(".")+1) : "";
    IntValue = PointValue = "";
    
    /// 计算整数部分
    for(var i=0;i<IntNum.length;i++)
    {
        /// 获取数字单位
        switch((IntNum.length-i) % 8)
        {
            case 5:
                unit = NUMUnit.WAN; //万
                break;
            case 0:
            case 4:
                unit = NUMUnit.QIAN; //千
                break;
            case 7:
            case 3:
                unit = NUMUnit.BAI; //百
                break;
            case 6:
            case 2:
                unit = NUMUnit.SHI; //十
                break;
            case 1:
                if((IntNum.length-i) > 8)
                {
                    unit = NUMUnit.YI; //亿    
                }
                else { unit = ""; }
                break;
            default:
                unit = "";
                break;
        }
        /// 组成整数部分
        IntValue += Number.substr(parseInt(IntNum.substr(i,1)),1) + unit;
    }
    
    /// 替换零
    for(var i=0;i<beforeReplace.Values.length;i++)
    {
        IntValue = replaceAll(IntValue,beforeReplace.Values[i].Name,afterReplace.Values[i].Name);             
    }
    // 末尾是零则去除
    if(IntValue.substr(IntValue.length-1,1) == NUMUnit.LING) IntValue = IntValue.substring(0,IntValue.length-1);
    // 一十开头的替换为十开头
    if(IntValue.substr(0,2) == Number.substr(1,1) + NUMUnit.SHI) IntValue = IntValue.substr(1,IntValue.length-1);
    
    /// 计算小数部分
    if(PointNum != "")
    {
        PointValue = Number.substr(PointNum.substr(0,1),1) + CNYUnit.JIAO;
        PointValue += Number.substr(PointNum.substr(1,1),1) + CNYUnit.FEN;
        for(var i=0;i<pointBefore.Values.length;i++)
        {
            PointValue = replaceAll(PointValue,pointBefore.Values[i].Name, pointAfter.Values[i].Name);
        }
    }
    moneyCNY = PointValue == "" ? IntValue + CNYUnit.YUAN + CNYUnit.ZHENG : IntValue + CNYUnit.YUAN + PointValue;
    return moneyCNY;
}
function afterPrint(){
	//关闭密码输入框
	$('#paycard,#receivecard,#amount').attr('readonly',false);
	$('#load_data .keyboard_password').remove();
	//清空输入框，清空数据
	$('#payimg').attr('src','/skin/images/fukuanren.png');
	$('#paycard').attr('value','');
	$('#payname').attr('value','');
	$('#receiveimg').attr('src','/skin/images/shoukuanren.png');
	$('#receivecard').attr('value','');
	$('#receivename').attr('value','');
	$('#amount').attr('value','0.00');
	$('#paymoney').attr('value','0.00');
	$('#money').attr('value','0');
	//开启重打印按钮
	$('#btnprint').addClass("btn-success");
	$('#btnprint').removeClass("btn-failed");
	$('#btnprint').addClass("btn-print");
	$('#btnprint').addClass("btn-lg");
	//验证重打印
	
	$('#okprint').attr('value','1');

	$('#paycard').focus();
}

function helloWorld(){
	if($('#okprint').attr('value') == '1'){
		return "1";
	}
	$html='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">';
	$html+='<html xmlns="http://www.w3.org/1999/xhtml">';
    $html+='<head>';
    $html+='<META http-equiv=Content-Type content="text/html; charset=utf-8" />';
    $html+='<TITLE></TITLE>';
    $html+='</head>';
    $html+='<body LEFTMARGIN=0 TOPMARGIN=0 MARGINWIDTH=0 MARGINHEIGHT=0>';
    $html+='<table  border="0" >';
    $html+='<tr>';
    $html+='<td colspan="2">';
    $html+='<div align="center">云南金荣农产品有限公司</div>';
    $html+='</td>';
    $html+='</tr>';
    $html+='<tr>';
    $html+='<td colspan="2">';
    $html+='<div>流水号：1020211</div>';
    $html+='</td>';
    $html+='</tr>';
    $html+='<tr>';
    $html+='<td colspan="2">';
    $html+='<div>交易方式：转账</div>';
    $html+='</td>';
    $html+='</tr>';
    $html+='<tr>';
    $html+='<td colspan="2">';
    $html+='<div>交易日期：</div>';
    $html+='</td>';
    $html+='</tr>';
    $html+='<tr>';
    $html+='<td colspan="2" align="right">';
    $html+='<div>'+formatDate( new Date())+'</div>';
    $html+='</td>';
    $html+='</tr>';
    $html+='<tr>';
    $html+='<td colspan="2">';
    $html+='<div ><hr/></div>';
    $html+='</td>';
    $html+='</tr>';
    $html+='<tr>';
	$html+='<td width="72">转出卡号：</td>';
	$html+='<td align="right" width="120">'+$("#paynoid").attr("value")+'</td>';
    $html+='</tr>';
    $html+='<tr>';
	$html+='<td width="72">转入卡号：</td>';
	$html+='<td align="right">'+$("#receivenoid").attr("value")+'</td>';
    $html+='</tr>';
    $html+='<tr>';
	$html+='<td width="72">金额：</td>';
	$html+='<td align="right">RMB '+$("#amount").attr("value")+'</td>';
    $html+='</tr>';
	$html+='<td colspan="2"></td>';
    $html+='</tr>';
	$html+="</table>";
	$html+="</body></html>";
	return $html;
}

function   formatDate(now)   {     
    var   year=now.getFullYear();     
    var   month=now.getMonth()+1;     
    var   date=now.getDate();     
    var   hour=now.getHours();     
    var   minute=now.getMinutes();     
    var   second=now.getSeconds();     
    return   year+"-"+month+"-"+date+"   "+hour+":"+minute+":"+second;     
}

function countNewOrder(){
	var result;
	$.ajax({
		type:'get',
		url: '/admin/menu/countneworder',
		data: '',
		success: function(data){

			eval('result='+data);
			
			$('.left_nav div a span.newtip').html(result.ordernumber);
			if(result.ordernumber>0){
				
				$('.left_nav div a span.newtip').addClass('newtipshow');
			}else{
				$('.left_nav div a span.newtip').removeClass('newtipshow');
			}

			$('.left_nav div a span.newtip2').html(result.order2number);
			if(result.order2number>0){
				
				$('.left_nav div a span.newtip2').addClass('newtipshow');
			}else{
				$('.left_nav div a span.newtip2').removeClass('newtipshow');
			}
			
			$('.left_nav div a span.newtip3').html(result.order3number);
			if(result.order3number>0){
				
				$('.left_nav div a span.newtip3').addClass('newtipshow');
			}else{
				$('.left_nav div a span.newtip3').removeClass('newtipshow');
			}
			
		}
	});
}

function ajaxKeyboard(address){
	var result;
	$.ajax({
		type:'get',
		url: address,
		async: false,
		data: '',
		success: function(data){
			result = data;
		}
	});
	return result;
}
//判断卡号是否存在
//如果存在返回卡姓名和头像
function checkCard(cardid){
	info= new Object();
	info.cardid = cardid;
	return ajaxPost(info,'/verificate/card/check');
}

//添加购物车 
function addCart(obj){
	return ajaxPost(obj,'/mall/index/addcartgoods');
}


//删除购物车 
function delCart(obj){
	return ajaxPost(obj,'/mall/index/delcartgoods');
}




//删除购物车 
function delOrderGoods(obj){
	return ajaxPost(obj,'/mall/index/delordergoods');
}


//更新购物车数量

function updateCartNumber(obj){
	
	return ajaxPost(obj,'/mall/index/updatecartgoods');
}
//更新订单数量

function updateOrderNumber(obj){
	
	return ajaxPost(obj,'/mall/index/updateordergoods');
}
//显示密码输入框
function showKeyboard(){
	html = ajaxKeyboard('/verificate/card/keyboard');
	$('#load_data').append(html);
}

//显示金额输入框
function showKeyboardMoney(){

	html = ajaxKeyboard('/verificate/card/keyboardmoney');
	$('#load_data').append(html);
}
//验证密码
function checkPassword(info){
	result = ajaxPost(info,'/verificate/card/checkpassword');
	return result['stat'];
}
//提交转账

function toTransfer(info){
	return ajaxPost(info,'/transfer/index/totransfer');
}

//更新商品总价

function countAllMoney(){
	allcount = 0;
	$('.rk_table tr').each(function(){
		$this = $(this);
		count = ($('.buycar_number',$this).attr("value")*parseFloat($('.goods_price',$this).text()));
		if(!isNaN(count)){
			allcount+= count;
		}
	});
	$('.heji_count').text(formatCurrency(allcount));
}



//格式化金钱
function fmoney(s, n) { 
	n = n > 0 && n <= 20 ? n : 2; 
	s = parseFloat((s + "").replace(/[^\d\.-]/g, "")).toFixed(n) + ""; 
	var l = s.split(".")[0].split("").reverse(), r = s.split(".")[1]; 
	t = ""; 
	for (var i = 0; i < l.length; i++) { 
		t += l[i] + ((i + 1) % 3 == 0 && (i + 1) != l.length ? "," : ""); 
	} 
	return t.split("").reverse().join("") + "." + r; 
} 

//保留两位小数
function toFixedTwo(s){
	s = parseFloat((s + "").replace(/[^\d\.-]/g, "")).toFixed(2) + "";
	return s;
}

function slidesome(){

	$(".slide").css("height",($(window).height()-108));

	$(".slide a").hover(
		function(){
			$(this).addClass("on");
			$(this).parent().addClass("slideon");
		},
		function(){
			
			$(this).removeClass("on");
			$(this).parent().removeClass("slideon");
		}
		
	);
}

/**
 * 将数值四舍五入(保留2位小数)后格式化成金额形式
 *
 * @param num 数值(Number或者String)
 * @return 金额格式的字符串,如'1,234,567.45'
 * @type String
 */
function formatCurrency(num) {
    num = num.toString().replace(/\$|\,/g,'');
    if(isNaN(num))
    num = "0";
    sign = (num == (num = Math.abs(num)));
    num = Math.floor(num*100+0.50000000001);
    cents = num%100;
    num = Math.floor(num/100).toString();
    if(cents<10)
    cents = "0" + cents;
    for (var i = 0; i < Math.floor((num.length-(1+i))/3); i++)
    num = num.substring(0,num.length-(4*i+3))+','+
    num.substring(num.length-(4*i+3));
    return (((sign)?'':'-') + num + '.' + cents);
}