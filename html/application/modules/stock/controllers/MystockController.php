<?php
/**
 * 库存管理模块 出库
 * 
 * auther kylin at 2014/10/14
 * 
 */
class Stock_MystockController extends Jcf_Controller_Action
{
	
	function init(){
		parent::init();
		$this->model = new Stock_Model_Mystock();
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
		
		//$list = parent::formatTime($list, array('cdate'));
		//$this->view->list = parent::formatMoney($list, array('amount'));
		$this->view->list = $list;
		$this->view->module = "库存查询";
		$this->view->totalCount = $totalCount;
		$this->view->numPerPage = $numPerPage;
		$this->view->totalPage = ceil($totalCount/$numPerPage);
		$this->view->currentPage = $pageNum > 0 ? $pageNum : 1;
		$this->view->dbMap = $dbMap;
		$this->view->PageList = parent::formatPage(ceil($totalCount/$numPerPage),$pageNum > 0 ? $pageNum : 1,$totalCount);
		$this->view->location='<h3 class="location"><a class="tohome" href="/index.php">主菜单</a>&gt;<a href="/stock/mystock">查看库存</a></h3>';
		
	}
}