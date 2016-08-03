<?php
/**
 * 库存管理模块 出库
 * 
 * auther kylin at 2014/10/14
 * 
 */
class Stock_StockoutController extends Jcf_Controller_Action
{
	
	function init(){
		parent::init();
		$this->model = new Stock_Model_Stockout();
		$this->view->list=array();
	}
	
	function indexAction(){
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
		$totalCount = count($this->model->queryInfo($user['uid'], $where,$order));
		
		$list = $this->model->queryInfo($user['uid'], $where,$order,$numPerPage,$offset);
		
		//是否有自定义方法
		
		$list = parent::formatTime($list, array('cdate','indate'));
		$this->view->list = $list;
		$this->view->module = "出库列表";
		$this->view->totalCount = $totalCount;
		$this->view->numPerPage = $numPerPage;
		$this->view->totalPage = ceil($totalCount/$numPerPage);
		$this->view->currentPage = $pageNum > 0 ? $pageNum : 1;
		$this->view->dbMap = $dbMap;
		$this->view->PageList = parent::formatPage(ceil($totalCount/$numPerPage),$pageNum > 0 ? $pageNum : 1,$totalCount);
		$this->view->location='<h3 class="location"><a class="tohome" href="index.php">主菜单</a>&gt;<a href="/stock/stockout">商品出库</a></h3>';
		
	}
	
	function orderlistAction(){
		$user = parent::getUser();
		$result = $this->model->getOrderlist($user['uid']);
		echo json_encode($result);
	}
	
	
	function infoAction(){
		$oid = empty($_REQUEST['id'])?0:$_REQUEST['id'];
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
		$totalCount = count($this->model->queryGoods($oid, $where,$order));
		
		$list = $this->model->queryGoods($oid, $where,$order,$numPerPage,$offset);
		//是否有自定义方法
		
		$list = parent::formatTime($list, array('cdate','indate'));
		$this->view->list = parent::formatMoney($list, array('amount'));
		$this->view->module = "出库详情";
		$this->view->totalCount = $totalCount;
		$this->view->numPerPage = $numPerPage;
		$this->view->totalPage = ceil($totalCount/$numPerPage);
		$this->view->currentPage = $pageNum > 0 ? $pageNum : 1;
		$this->view->dbMap = $dbMap;
		$this->view->PageList = parent::formatPage(ceil($totalCount/$numPerPage),$pageNum > 0 ? $pageNum : 1,$totalCount);
		if ($list) {
			$this->view->location='<h3 class="location"><a class="tohome" href="/index.php">主菜单</a>&gt;<a href="/stock/stockout">商品出库</a>&gt;<span>出库详情</span></h3>';
		}
		
	}
	
	
	function outputAction(){
		$user = parent::getUser();
		$_REQUEST['uid']=$user['uid'];
		if (empty($_REQUEST['oid'])) {
			echo json_encode(array('stat'=>false,'message'=>'参数有误'));
		}else{
			if($data = $this->model->output($_REQUEST)){
				
				$txt="成功操作 [出库]: 出库单号：[".$_REQUEST['stock_on']."]";
				
				try {
					
					$this->log->insertlog($txt,0);
					
				} catch (Exception $e) {
					
					echo json_encode(array('stat'=>false,'message'=>'未知错误'));
				}
				echo json_encode(array('stat'=>true,'message'=>'出库成功'));
				
			}else{
				echo json_encode(array('stat'=>false,'message'=>'操作失败'));
			}
		}
	}
	
	function pageoutputAction(){
		$type=array('采购出库','自主出库');
		$result = $this->model->pageoutput($_REQUEST['oid']);
		$this->view->oid = $_REQUEST['oid'];//订单号
		$this->view->inputtype = $type[$_REQUEST['type']];//入库类型
		$this->view->type = $_REQUEST['type'];//入库类型
		$this->view->stock_on=time().rand(100, 999); //入库单号
		$this->view->cdate = date('Y/m/d H:i:s',time());//创建时间
		$this->view->list = $result;
		$this->view->module = "出库详情";
		
	}
}
