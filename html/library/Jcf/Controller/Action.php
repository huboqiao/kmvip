<?php
/**
 +------------------------------------------------- 
 *通用封装类
 +-------------------------------------------------
 * 主要功能： 封装了添加、删除、修改、查询、分页
 * 如果查询条件不满足需求，自行在model写一个
 * 自定义方法进行处理。方法名：getDefined(...)
 +-------------------------------------------------
 *@auther huboqiao
 *
 *
 */

#ini_set("error_reporting","E_ALL & ~E_NOTICE");
Class Jcf_Controller_Action extends Zend_Controller_Action{
	public function __construct(
		Zend_Controller_Request_Abstract $request,
		Zend_Controller_Response_Abstract $response,array $invokeArgs = array())
	{
		parent::__construct($request,$response,$invokeArgs);
	}

	public function init(){
		parent::init();
		$this->log = new Jcf_Log_Log();
		$name = $this->_request->getControllerName();
		$this->view->URL = '/'.$this->_request->getModuleName().'/'.$name;
		$this->view->MODULE = $name;
        $auth = Zend_Auth::getInstance();
		$userid = $auth->getIdentity();
		$this->view->user = $userid;
	}

	/**
	 +-------------------------------------------------
	 *匹配当前表的字段与用户传过来的字段进行匹配
	 +-------------------------------------------------
	 *@access protected
	 +-------------------------------------------------
	 *@return array
	 +-------------------------------------------------
	 */
	protected function _dbMap($dbCols = array()){
		print_r($_REQUEST);
		$dbMap = array();
		if(is_array( $dbCols )){
			foreach( $_REQUEST as $key => $val ){
				if( in_array( $key , $dbCols , true ) ){
					$dbMap[$key] = $val;
				}	
			}
		}
		return $dbMap;
	}
	
	/*
	 *
	 * index实始化
	 */
	public function indexAction(){
		$model = $this->getModelClass();
		$dbMap = $this->_dbMap( $model->info( 'cols' ) );
		$where = null;
		$order = null;
		
		if( method_exists( $this, '_filter' )){
			$this->_filter( $dbMap );
		}

		$termCount = 0;

		//搜索条件
		foreach( $dbMap as $key => $val ){
			if( isset( $val ) && trim ( $val ) != ''){
				if( is_array( $val ) && trim( $val[1] ) != '' ){
					$where .= ( $termCount > 0 ? ' and ' : ' ') . $key . ' ' . $val[0] . ' \' ' . trim( $val[1] ) . ' \ ';
					$termCount ++;
				}else if( trim( $val ) != '' ){
					$where .= ( $termCount > 0 ? ' and ' : ' ') . $key . ' like "%' .trim( $val ) . '%"';
				    $termCount ++ ;	
				}
			}	
		}
		#print_r($_REQUEST);exit;
		if( !empty( $_REQUEST ['orderField'])){
			$order = $_REQUEST['orderField'];
			if(empty($_REQUEST['orderDirection'])){
				$order .= ' desc';
			}else{
				$order .= ' '. $_REQUEST['orderDirection'];
			}
		}

		//分页开始
		$numPerPage = 20;//每一页显示多少条数据
		$offset = 0;

		if(!empty($_REQUEST['pageNum'])){
			$pageNum = $_REQUEST['pageNum'];
		}else{
			$pageNum = 1;
		}
		if( !empty( $pageNum) && $pageNum > 0 ){
			$offset = ( $pageNum - 1 ) * $numPerPage;
		}

		$totalCount = count($model->fetchAll($where));

		//是否有自定义方法
		if( method_exists( $model, 'getDefined' )){
			$list = $model->getDefined($where,$order,$numPerPage,$offset);
		}else{
			$list = $model->fetchAll($where,$order,$numPerPage,$offset);
		}
		$this->view->list = $list;
		$this->view->totalCount = $totalCount;
		$this->view->numPerPage = $numPerPage;
		$this->view->currentPage = $pageNum > 0 ? $pageNum : 1;
		$this->view->dbMap = $dbMap;
		$this->thisUser();
	}
	
	/**
	 * 高级搜索
	 */
	 function advancedAction(){
	 	
	 }

	/**
	 * 编辑动作
	 */
	public function editAction(){
		$model = $this->getModelClass();
		$action = isset($_REQUEST['act'])?$_REQUEST['act']:'';
		$this->view->act = $action;
		$this->view->vo = $model->fetchRow('id='.$_REQUEST['id']);
	}
	
	/**
	 * 查看动作
	 */
	 public function infoAction(){
		$model = $this->getModelClass();
		$this->view->vo = $model->fetchRow('id='.$_REQUEST['id']);
	 	
	 }

	/**
	 *初始化添加视图
	 */
	public function addAction(){
	}
	
	/**
	 * 处理添加
	 */
	public function insertAction(){
		try{
			$model = $this->getModelClass();
			$dbMap = $this->_dbMap( $model->info( 'cols' ) );
			$id = $model->insert($dbMap);
			$txt = '操作'.$model->modelname.'模块，添加了一条记录，记录id为：'.$id;
			$this->log->insertlog($txt);
			$this->success('添加记录成功！');
		}catch( Exception $e ){
			print_r($e);
			$this->error('操作失败');
		}	
	}

	/**
	 *  update 
	 */
	public function updateAction(){
		try{
			$model = $this->getModelClass();
			$dbMap = $this->_dbMap( $model->info( 'cols' ) );
			$k = $this->returnid($model);
			$db = $model->getAdapter();

			$where = $db->quoteInto('id=?',$_REQUEST['id']);
			$row_affected = $model->update($dbMap,$where );
			$txt = '操作'.$model->modelname.'模块，修改了一条记录，记录id为：'.$_REQUEST['id'];
			$this->log->insertlog($txt);
			
			$this->success('修改成功');
		}catch( Exception $e ){
			print_r($e);
			$this->error('操作失败');
		}
	}

	/**
	 +-------------------------------------------------
	 *将记录标识更新为1表示为放入回收站，不是真正的删除
	 +-------------------------------------------------
	 *@access public
	 +-------------------------------------------------
	 *@return void
	 +-------------------------------------------------
	 */

	public function deleteAction(){
		try{
			$model = $this->getModelClass();
			$dbMap = $this->_dbMap( $model->info( 'cols' ) );
			$db = $model->getAdapter();

			$where = $db->quoteInto('id=?',$_REQUEST['id']);
			$row_affected = $model->update( array('is_delete' => 1),$where );

		}catch( Exception $e ){
			print_r($e);
			$this->error('操作失败');
		}
	} 
	
	/**
	 +-------------------------------------------------
	 *从表中删除记录
	 +-------------------------------------------------
	 *@access public
	 +-------------------------------------------------
	 *@return json
	 +-------------------------------------------------
	 */ 
	public function foreverdeleteAction(){
		try{
			$model = $this->getModelClass();
			$k = $this->returnid($model);
			$db = $model->getAdapter();
			$select = $model->select();
			$where = $db->quoteInto($k.'=?',$_REQUEST[$k]);
			$row_affected = $model->delete( $where );
			$txt = '操作'.$model->modelname.'模块，删除了一条记录，记录id为：'.$_REQUEST[$k];
			$this->log->insertlog($txt);
			
			$this->success('操作成功');
		}catch( Exception $e ){
			print_r($e);
			$this->error( '操作失败' );
		}
	}
	
	//获取表的主键
	function returnid($model){
		$dbMap = $this->_dbMap( $model->info( 'cols' ) );
		//组合取出单表的主键
		foreach($dbMap as $key=>$val){
			$k = $key;	
		}
		return $k;
	}
	
	/**
	 *批量删除
	 *
	 */
	public function alldeleteAction(){
		if(!empty($_REQUEST['ids'])){
			$idarray = explode(',',$_REQUEST['ids']);
			try{
				$model = $this->getModelClass();
				$db = $model->getAdapter();
				$str = '';
				foreach($idarray as $id){
					$where = $db->quoteInto('id=?',$id);
					$str .= '['.$id.']';
					$row_affected = $model->delete( $where );
				}
				$txt = '操作'.$model->modelname.'模块，批量删除了一些条记录，记录id为：'.$str;
				$this->log->insertlog($txt);
				
				$this->success('操作成功');
			}catch( Exception $e ){
				print_r($e);
				$this->error('操作失败');
			}
		}else{
			$this->error('传参错误');
		}
			
	}

	
	private function thisUser(){
		$user = Zend_Auth::getInstance()->getIdentity()->getProperties();
		$this->view->user = $user;
	}
	
	public function getUser(){

		$user = Zend_Auth::getInstance()->getIdentity()->getProperties();
		return $user;
	}
	/**
	 +-------------------------------------------------
	 *获取当前模块的数据模型层，并且实例化
	 +------------------------------------------------- 
	 *@access private
	 +-------------------------------------------------
	 *@return class
	 +-------------------------------------------------
	 */
	private function getModelClass(){
		$className = ucfirst($this->_request->getModuleName()).'_Model_'.ucfirst($this->_request->getControllerName());
		return new $className();
	}


	protected function isAjax() {
		if (isset ( $_SERVER ['HTTP_X_REQUESTED_WITH'] )) {
			if ('xmlhttprequest' == strtolower ( $_SERVER ['HTTP_X_REQUESTED_WITH'] ))
				return true;
		}
		if (! empty ( $_REQUEST ['ajax'] ))
			// 判断Ajax方式提交
			return true;
		return false;
	}

	
	protected function ajaxReturn($status = 1, $message = '') {
		$result = array ();
		$result ['statusCode'] = $status;
		$result ['navTabId'] = empty($_REQUEST ['navTabId'])?'':$_REQUEST['navTabId'];
		$result ['rel'] = empty($_REQUEST ['rel'])?'':$_REQUEST['rel'];
		$result ['callbackType'] = empty($_REQUEST ['callbackType'])?'':$_REQUEST['callbackType'];
		$result ['forwardUrl'] = empty($_REQUEST ['forwardUrl'])?'':$_REQUEST['forwardUrl'];
		$result ['message'] = $message;
		header ( 'Content-Type:text/html; charset=utf-8' );
		exit ( Zend_Json::encode ( $result ) );
	
	}


	protected function success($message, $ajax = false) {
		$this->ajaxReturn ( 200, $message );
	}

	protected function error($message, $ajax = false) {
		$this->ajaxReturn ( 300, $message );
	}
	


	/**
	 +-------------------------------------------------
	 *格式化时间
	 +-------------------------------------------------
	 *@access private
	 +-------------------------------------------------
	 *@return class
	 +-------------------------------------------------
	 */
	
	public function formatTime($arr,$filed,$format='Y/m/d H:i:s'){
		foreach($arr as $k=>$v){
			foreach($filed as $f){
				$arr[$k][$f] = date($format,$v[$f]);
			}
		}
		return $arr;
	}

	/**
	 +-------------------------------------------------
	 *格式化时间
	 +-------------------------------------------------
	 *@access private
	 +-------------------------------------------------
	 *@return class
	 +-------------------------------------------------
	 */
	
	public function formatTimeOne($arr,$filed,$format='Y/m/d H:i:s'){
		
		foreach($filed as $f){
				$arr[$f] = date($format,$arr[$f]);
		}
		return $arr;
	}
	
	public function formatMoney($arr,$filed){
		foreach($arr as $k=>$v){
			foreach($filed as $f){
				$arr[$k][$f] = number_format($v[$f],2);
			}
		}
		return $arr;
	}
	
	public function formatPage($totalPage,$currentPage,$totalCount,$showPage=10){
		$result['left'] = 1;//第一页
		$result['right'] = $totalPage;//最后一页
		$result['leftdot']=0;
		$result['rightdot']=0;
		if($currentPage == 1){
			$result['left'] = 0;
		}
		if($currentPage == $totalPage){
			$result['right'] = 0;
		}
		$num = $totalPage>$showPage? $showPage:$totalPage;

		$result['list']= array();
		if (!$totalCount) {
			return $result;
		}
		array_push($result['list'],$currentPage);
		
		for ($i = 1; $i < $showPage; $i++) {
			
			if($currentPage - $i >0){
				array_unshift($result['list'],$currentPage - $i);
			}
			if (count($result['list'])>=$num) {
				break;
			}
			if ($currentPage + $i <=$totalPage) {
				
				array_push($result['list'],$currentPage + $i);
			}
			if (count($result['list'])>=$num) {
				break;
			}
			
		}

		if ($result['list'][0]>1) {
			$result['leftdot']=1;
		}
		if ($result['list'][count($result['list'])-1]<$totalPage) {
			$result['rightdot']=1;
		}
		
		return $result;
	}
	
}


?>
