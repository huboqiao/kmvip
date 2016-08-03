<?php
/**
 * 用户登陆模块
 * 
 * 登陆采用md5单向加密
 * 
 * auther huboqiao at 2013-06-11
 */
class Search_IndexController extends Jcf_Controller_Action
{
	
	function init(){
		#Zend_Layout::disableLayout();
		$this->model = new Search_Model_Index();
	}
	function indexAction(){
		$user = parent::getUser();
		print_r($user);
		//分页开始
		$numPerPage = 10;

		if (!empty($_POST['orderby'])) {
			$order['orderby'] = $_POST['orderby'];
		}else{
			$order['orderby'] = 'cdate';
		}
		
		if (!empty($_POST['ordersc'])) {
			$order['ordersc'] = $_POST['ordersc']; 
		}else{
			$order['ordersc'] = 'desc'; 
		}
		
		if(!empty($_REQUEST['pageNum'])){
			$pageNum = $_REQUEST['pageNum'];
		}else{
			$pageNum = 1;
		}
		if( !empty( $pageNum) && $pageNum > 0 ){
		$offset = ( $pageNum - 1 ) * $numPerPage;
		}

		if (!empty($_REQUEST['starttime'])) {
			$this->view->starttime = $_REQUEST['starttime'];
			$where = ' and a1.cdate>'.$_REQUEST['starttime'];
		}
		
		if (!empty($_REQUEST['endtime'])) {
			$this->view->endtime = $_REQUEST['endtime'];
			$where .=' and a1.cdate<='.$_REQUEST['endtime'];
		}
		
		
		$totalCount = count($this->model->qeuryCardzz($user['noid'], $where,$order));

		$list = $this->model->qeuryCardzz($user['noid'], $where,$order,$numPerPage,$offset);

		//是否有自定义方法
		
		$list = parent::formatTime($list, array('cdate'));
		$this->view->list = parent::formatMoney($list, array('amount'));
		$this->view->totalCount = $totalCount;
		$this->view->numPerPage = $numPerPage;
		$this->view->totalPage = ceil($totalCount/$numPerPage);
		$this->view->currentPage = $pageNum > 0 ? $pageNum : 1;
		$this->view->dbMap = $dbMap;
		$this->view->PageList = parent::formatPage(ceil($totalCount/$numPerPage),$pageNum > 0 ? $pageNum : 1,$totalCount);
		$this->view->location='<h3 class="location"><a class="tohome" href="/index.php">主页</a>&gt;<a href="/search/index">查询</a></h3>';
		$this->view->orderby = $order['orderby'];	
		$this->view->ordersc = $order['ordersc'];	
	}
}
