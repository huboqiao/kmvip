<?php
/**
 * 用户登陆模块
 * 
 * 登陆采用md5单向加密
 * 
 * auther huboqiao at 2013-06-11
 */
class Order_OrdershopController extends Jcf_Controller_Action
{
	
	function init(){
		parent::init();
		$this->model = new Order_Model_Ordershop();
	}
	function indexAction(){
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
		$totalCount = count($this->model->queryInfo( $where,$order));
		
		$list = $this->model->queryInfo($where,$order,$numPerPage,$offset);
		//是否有自定义方法
		
		$list = parent::formatTime($list, array('cdate'));
		$this->view->list = parent::formatMoney($list, array('amount'));
		$this->view->module = "订单商城";
		$this->view->totalCount = $totalCount;
		$this->view->numPerPage = $numPerPage;
		$this->view->totalPage = ceil($totalCount/$numPerPage);
		$this->view->currentPage = $pageNum > 0 ? $pageNum : 1;
		$this->view->dbMap = $dbMap;
		$this->view->PageList = parent::formatPage(ceil($totalCount/$numPerPage),$pageNum > 0 ? $pageNum : 1,$totalCount);
		$this->view->location='<h3 class="location"><a class="tohome" href="/index.php">主菜单</a>&gt;<a href="/order/ordershop">订单商城</a></h3>';
		
	}
	
	function infoAction(){
		
		$oid = empty($_REQUEST['id'])?0:$_REQUEST['id'];
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
		
		$where="";
		$order="";
		$dbMap="";
		$totalCount = count($this->model->queryGoods($oid, $where,$order));
		
		$list = $this->model->queryGoods($oid, $where,$order,$numPerPage,$offset);
		//是否有自定义方法
		
		$list = parent::formatTime($list, array('cdate'));
		$this->view->list = parent::formatMoney($list, array('amount'));
		$this->view->module = "订单详情";
		$this->view->totalCount = $totalCount;
		$this->view->numPerPage = $numPerPage;
		$this->view->totalPage = ceil($totalCount/$numPerPage);
		$this->view->currentPage = $pageNum > 0 ? $pageNum : 1;
		$this->view->dbMap = $dbMap;
		$this->view->PageList = parent::formatPage(ceil($totalCount/$numPerPage),$pageNum > 0 ? $pageNum : 1,$totalCount);
		if($list){
			
			$this->view->location='<h3 class="location"><a class="tohome" href="/index.php">主菜单</a>&gt;<a href="/order/ordershop">订单商城</a>&gt;<span>订单购买</span></h3>';
		}
	}
	
	function enoughmoneyAction(){
		
		$user = parent::getUser();
		if (empty($_REQUEST['oid'])) {
			echo json_encode(array('stat'=>false,'message'=>'参数有误'));
		}else{
			$oid = $_REQUEST['oid'];
			if($data = $this->model->enoughmoney($oid,$user['uid'])){
				
				
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
				
				
				$txt="成功操作 [购买订单]: 购买者ID：[".$user['uid']."],订单单号：[".$this->model->queryOdersn($oid)."]";
				
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
	
}
