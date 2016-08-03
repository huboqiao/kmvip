<?php
/**
 * 库存管理模块 出库
 * 
 * auther kylin at 2014/10/14
 * 
 */
class Search_ExpendController extends Jcf_Controller_Action
{
	
	function init(){
		parent::init();
		$this->model = new Search_Model_Expend();
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
		$totalCounttx = count($this->model->querytxInfo($user['noid'], $where,$order));
		$totalCountzz = count($this->model->queryzzInfo($user['noid'], $where,$order));
		$totalCount = $totalCounttx+$totalCountzz;
		if($totalCounttx>$offset){
			if($totalCounttx>=$offset+$numPerPage){
				
				$list= $this->model->querytxInfo($user['noid'], $where,$order,$numPerPage,$offset);
			}else{
				
				$list= $this->model->querytxInfo($user['noid'], $where,$order,$numPerPage,$offset);
				$listzz = $this->model->queryzzInfo($user['noid'], $where,$order,$numPerPage-count($list),0);
				$list = array_merge($list,$listzz);
			}
		}else{
			
			
			$offsetb = $offset-$totalCounttx;
			$list= $this->model->queryzzInfo($user['noid'], $where,$order,$numPerPage,$offsetb);
		}
		
		//是否有自定义方法
		
		$list = parent::formatTime($list, array('cdate'));
		$this->view->allcount = $this->model->allcount($user['noid']);
		$this->view->offset = $offset;
		$this->view->module = "支出明细";
		$this->view->list = $list;
		$this->view->totalCount = $totalCount;
		$this->view->numPerPage = $numPerPage;
		$this->view->totalPage = ceil($totalCount/$numPerPage);
		$this->view->currentPage = $pageNum > 0 ? $pageNum : 1;
		$this->view->dbMap = $dbMap;
		$this->view->PageList = parent::formatPage(ceil($totalCount/$numPerPage),$pageNum > 0 ? $pageNum : 1,$totalCount);
		$this->view->location='<h3 class="location"><a class="tohome" href="/index.php">主菜单</a>&gt;<a href="/search/expend">支出明细</a></h3>';
		
	}
	
	
}
