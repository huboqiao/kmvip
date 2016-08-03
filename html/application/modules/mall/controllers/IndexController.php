<?php
/**
 * 用户登陆模块
 * 
 * 登陆采用md5单向加密
 * 
 * auther huboqiao at 2013-06-11
 */
class Mall_IndexController extends Jcf_Controller_Action
{
	
	function init(){
		parent::init();
		$this->model = new Mall_Model_Index();
	}
	
	
	function buycarAction(){
		//获取购物车商品
		$cartgoods = $this->getCartGoods();
		
		//分页开始
		$numPerPage = 100;//每一页显示多少条数据
		$offset = 0;
		
//		//获取商品信息
//		$goodslist = $this->model->getgoodslist($cartgoods);
//		
		
		if(!empty($_REQUEST['pageNum'])){
			$pageNum = $_REQUEST['pageNum'];
		}else{
			$pageNum = 1;
		}
		if( !empty( $pageNum) && $pageNum > 0 ){
			$offset = ( $pageNum - 1 ) * $numPerPage;
		}
		$where = "";
		$order = "";
		$dbMap = "";
		$totalCount = count($this->model->getgoodslist($cartgoods,$where,$order));
		
		
		$list = $this->model->getgoodslist($cartgoods,$where,$order,$numPerPage,$offset);
		
		$this->view->list = parent::formatMoney($list, array('goods_price'));
		$this->view->module = "购物车";
		$this->view->totalCount = $totalCount;
		$this->view->numPerPage = $numPerPage;
		$this->view->totalPage = ceil($totalCount/$numPerPage);
		$this->view->currentPage = $pageNum > 0 ? $pageNum : 1;
		$this->view->dbMap = $dbMap;
		$this->view->PageList = parent::formatPage(ceil($totalCount/$numPerPage),$pageNum > 0 ? $pageNum : 1,$totalCount);
		$this->view->location='<h3 class="location"><a class="tohome" href="/index.php">主菜单</a>&gt;<a href="/mall/index/buycar">购物车</a></h3>';
		
	}
	function indexAction(){
		
		//获取商品分类
		$catList = $this->model->getAllCategory();
		//		print_r($catList);
		
		//分页开始
		$numPerPage = 10;//每一页显示多少条数据
		$offset = 0;
		
		
		
		if(!empty($_REQUEST['pageNum'])){
			$pageNum = $_REQUEST['pageNum'];
		}else{
			$pageNum = 1;
		}
		if( !empty( $pageNum) && $pageNum > 0 ){
			$offset = ( $pageNum - 1 ) * $numPerPage;
		}
		if(!empty($_REQUEST['cat_id']) && $_REQUEST['cat_id'] > 0){
			$cat_id = $_REQUEST['cat_id'];
			$where = " and cat_id = ".$_REQUEST['cat_id'];
		}else{
			$cat_id = 0;
			$where = "";
		}
		
		$order = "";
		$dbMap = "";
		$totalCount = count($this->model->queryInfo( $where,$order));
		
		$list = $this->model->queryInfo($where,$order,$numPerPage,$offset);
//		print_r($list);
		//是否有自定义方法
		
		//查询购物车中已经有的商品
//		$this->view->cartGoods = $this->getCartGoods();
		
//		$list = parent::formatTime($list, array('cdate'));
		$this->view->list = parent::formatMoney($list, array('goods_price'));
		$this->view->module = "商城";
		$this->view->cat_id = $cat_id;
		$this->view->catList = $catList;
		$this->view->totalCount = $totalCount;
		$this->view->numPerPage = $numPerPage;
		$this->view->totalPage = ceil($totalCount/$numPerPage);
		$this->view->currentPage = $pageNum > 0 ? $pageNum : 1;
		$this->view->dbMap = $dbMap;
		$this->view->PageList = parent::formatPage(ceil($totalCount/$numPerPage),$pageNum > 0 ? $pageNum : 1,$totalCount);
		$this->view->location='<h3 class="location"><a class="tohome" href="/index.php">主菜单</a>&gt;<a href="/mall/index">商城</a></h3>';
		
	}
	
	function getCartGoods(){
		//获取购物车商品
		$user = parent::getUser();
		return $user['cart'];
		
	}
	
	
	function addcartgoodsAction(){
		//添加购物车商品
		$goods_id = $_REQUEST["goods_id"];
		$goods_number = $_REQUEST["goods_number"];
		$user = parent::getUser();
		$keys = array_keys($user["cart"]);
//		print_r($keys);
		if (in_array($goods_id,$keys)){
			$user["cart"][$goods_id] += $goods_number;
		}else{
			$user["cart"][$goods_id] = $goods_number;
		}
		$auth = Zend_Auth::getInstance();
		$adapter  = new Jcf_Auth_Auth($user["cardid"],$user["cart"]);
		$auth->authenticate($adapter);
//		print_r(parent::getUser());
		echo json_encode(array('stat'=>true,'message'=>'添加购物车成功！'));
		
	}
	
	
	function updateordergoodsAction(){
		//添加订单商品
		$goods_id = $_REQUEST["goods_id"];
		$goods_number = $_REQUEST["goods_number"];
		$order_id = $_REQUEST["order_id"];
		$this->model->updateordergoods($goods_id,$goods_number,$order_id);
		
	}
	function updatecartgoodsAction(){
		//添加购物车商品
		$goods_id = $_REQUEST["goods_id"];
		$goods_number = $_REQUEST["goods_number"];
		$user = parent::getUser();
		$keys = array_keys($user["cart"]);
//		print_r($keys);
		if (in_array($goods_id,$keys)){
			$user["cart"][$goods_id] = $goods_number;
		}
		
		$auth = Zend_Auth::getInstance();
		$adapter  = new Jcf_Auth_Auth($user["cardid"],$user["cart"]);
		$auth->authenticate($adapter);
//		print_r(parent::getUser());
		echo json_encode(array('stat'=>true,'message'=>'更新购物车成功！'));
		
	}
	
	function addorderbycartAction(){
		//获取购物车所有商品
		$user = parent::getUser();
		//插入订单表,订单详情表
		$orderid = $this->model->addorderbycart($user);
		//清空购物车
		$this->clearcart();
		//显示订单表内容
		$order = $this->model->orderInfo($orderid);
		//分页开始
		$numPerPage = 100;//每一页显示多少条数据
		$offset = 0;
		
//		//获取商品信息
//		$goodslist = $this->model->getgoodslist($cartgoods);
//		
		if($order["pay_time"]>0	){
			$format = array("add_time","pay_time");
		}else{
			$format = array("add_time");	
		}
		
		$list = $order["goods"];
		$this->view->order = parent::formatTimeOne($order,$format);
//		$this->view->order = $order;
		$this->view->list = parent::formatMoney($list, array('goods_price'));
		$this->view->module = "订单详情";
		$this->view->location='<h3 class="location"><a class="tohome" href="/index.php">主菜单</a>&gt;<a href="/mall/index/buycar">购物车</a></h3>';
		
		
	}
	
	
	function addorderbygoodsAction(){
		//获取购物车所有商品
		
		$goods["goods_id"] = $_REQUEST["goods_id"];
		$goods["goods_number"]= $_REQUEST["goods_number"];
		$user = parent::getUser();
		//插入订单表,订单详情表
		$orderid = $this->model->addorderbygoods($user,$goods);
		//显示订单表内容
		$order = $this->model->orderInfo($orderid);
		//分页开始
		$numPerPage = 100;//每一页显示多少条数据
		$offset = 0;
		
//		//获取商品信息
//		$goodslist = $this->model->getgoodslist($cartgoods);
//		
		if($order["pay_time"]>0	){
			$format = array("add_time","pay_time");
		}else{
			$format = array("add_time");	
		}
		
		$list = $order["goods"];
		$this->view->order = parent::formatTimeOne($order,$format);
		$this->view->list = parent::formatMoney($list, array('goods_price'));
		$this->view->module = "订单详情";
		$this->view->location='<h3 class="location"><a class="tohome" href="/index.php">主菜单</a>&gt;<a href="/mall/index/buycar">购物车</a></h3>';
		
		
	}
		
	function orderinfoAction(){
		//获取购物车所有商品
		
		$orderid= $_REQUEST["id"];
		$order = $this->model->orderInfo($orderid);
		//分页开始
		$numPerPage = 100;//每一页显示多少条数据
		$offset = 0;
		
//		//获取商品信息
//		$goodslist = $this->model->getgoodslist($cartgoods);
//		
		if($order["pay_time"]>0	){
			$format = array("add_time","pay_time");
		}else{
			$format = array("add_time");	
		}
		
		$list = $order["goods"];
		$this->view->order = parent::formatTimeOne($order,$format);
		$this->view->list = parent::formatMoney($list, array('goods_price'));
		$this->view->module = "订单详情";
		$this->view->location='<h3 class="location"><a class="tohome" href="/index.php">主菜单</a>&gt;<a href="/mall/index/orderlist">订单列表</a>&gt;<span>订单详情</span></h3>';
		
		
	}
	
		
	function clearcart(){
		//添加购物车商品
		$user = parent::getUser();
		$auth = Zend_Auth::getInstance();
		$adapter  = new Jcf_Auth_Auth($user["cardid"],array());
		$auth->authenticate($adapter);
//		print_r(parent::getUser());
		
	}
	
	function delcartgoodsAction(){
		//添加购物车商品
		$goods_id = $_REQUEST["goods_id"];
		$user = parent::getUser();
		$keys = array_keys($user["cart"]);
//		print_r($keys);
		if (in_array($goods_id,$keys)){
			unset($user["cart"][$goods_id]);
		}
		$auth = Zend_Auth::getInstance();
		$adapter  = new Jcf_Auth_Auth($user["cardid"],$user["cart"]);
		$auth->authenticate($adapter);
//		print_r(parent::getUser());
		echo json_encode(array('stat'=>true,'message'=>'移除购物车成功！'));
		
	}
	
	function delordergoodsAction(){
		//添加购物车商品
		$order_id = $_REQUEST["order_id"];
		$goods_id = $_REQUEST["goods_id"];
		
		$order = $this->model->delordergoods($order_id,$goods_id);
		echo json_encode(array('stat'=>true,'message'=>'移除购物车成功！'));
		
	}
	
	function infoAction(){
		
		$goods_id = empty($_REQUEST['goods_id'])?0:$_REQUEST['goods_id'];
		//获得商品资料
		
		$goods = $this->model->getGoodsinfo($goods_id);
		
		
		//是否有自定义方法
		
		$this->view->module = "商品详情";
		$this->view->goods = $goods;
		$this->view->location='<h3 class="location"><a class="tohome" href="/index.php">主菜单</a>&gt;<a href="/mall/index">商城</a></h3>';
	}
	

	
	function enoughmoneyAction(){
		
		$user = parent::getUser();
		if (empty($_REQUEST['order_id'])) {
			echo json_encode(array('stat'=>false,'message'=>'参数有误'));
		}else{
			$order_id = $_REQUEST['order_id'];
			if($data = $this->model->enoughmoney($order_id,$user['uid'])){
				
				echo json_encode(array('stat'=>true,'message'=>'够余额'));
				
			}else{
				echo json_encode(array('stat'=>false,'message'=>'余额不足'));
			}
		}
	}
	
	function keyboardAction(){
		$this->view->oid = $_REQUEST['oid'];
		$user = parent::getUser();
		$this->view->cardid = $user['cardid'];
		//显示键盘
		$numarr = range(0,9);
		shuffle($numarr);
		$this->view->numarr = $numarr;
	}
	
	
	function buyAction(){
		
		$user = parent::getUser();
		if (empty($_REQUEST['oid'])) {
			echo json_encode(array('stat'=>false,'message'=>'参数有误'));
		}else{
			$oid = $_REQUEST['oid'];
			$data = $this->model->buy($oid,$user);
			if($data['stat']){
				
				
				$txt="成功操作 [购买商品订单]: 购买者ID：[".$user['uid']."],订单单号：[".$this->model->queryOdersn($oid)."]";
				
				try {
					
					$this->log->insertlog($txt,0);
					
				} catch (Exception $e) {
					
					echo json_encode(array('stat'=>false,'message'=>'未知错误'));
				}
				echo json_encode(array('stat'=>true,'message'=>'购买成功'));
				
			}else{
				echo json_encode($data);
			}
		}
	}
	
	function orderlistAction(){
		
		$user = parent::getUser();
		//分页开始
		$numPerPage = 15;//每一页显示多少条数据
		$offset = 0;
	
	
	
		if(!empty($_REQUEST['pageNum'])){
			$pageNum = $_REQUEST['pageNum'];
		}else{
			$pageNum = 1;
		}
		if( !empty( $pageNum) && $pageNum > 0 ){
			$offset = ( $pageNum - 1 ) * $numPerPage;
		}
	
		$where = "";
		$order = "";
		$dbMap = "";
		$totalCount = count($this->model->queryorderList( $user['noid'],$where,$order));
	
		$list = $this->model->queryorderList($user['noid'],$where,$order,$numPerPage,$offset);
		//是否有自定义方法
	
		$list = parent::formatTime($list, array('add_time'));
		$this->view->list = parent::formatMoney($list, array('amount'));
		$this->view->module = "我的商城订单";
		$this->view->totalCount = $totalCount;
		$this->view->numPerPage = $numPerPage;
		$this->view->totalPage = ceil($totalCount/$numPerPage);
		$this->view->currentPage = $pageNum > 0 ? $pageNum : 1;
		$this->view->dbMap = $dbMap;
		$this->view->PageList = parent::formatPage(ceil($totalCount/$numPerPage),$pageNum > 0 ? $pageNum : 1,$totalCount);
		$this->view->location='<h3 class="location"><a class="tohome" href="/index.php">主页</a>&gt;<a href="/mall/index/orderlist">我的商城订单</a></h3>';
		
	}
	
}
