<?php
/**
 * 转账模块
 * 
 * auther kylin at 2014/9/28
 */
class Transfer_IndexController extends Jcf_Controller_Action {
	function init() {
		parent::init();
		$this->model = new Transfer_Model_Index();
	}
	
	function indexAction() {
		
		$this->view->location='<h3 class="location"><a class="tohome" href="/index.php">主菜单</a>&gt;<a href="/transfer/index">转账</a></h3>';
		
	}
	
	
	function totransferAction(){
		
		$model = new Verificate_Model_Card ();
		$arr ['paycard'] = $model->getNoid($_POST ['cardid']);
		$arr ['incomecard'] = $model->getNoid($_POST ['receivecard']);
		$arr ['amount'] = $_REQUEST ['amount'];
		$arr ['cdate'] = time ();
		$arr ['ctype'] = 1;
		$arr ['uid'] = 0;
		if(!$this->model->isEnoughAmount($arr['paycard'],$arr['amount'])){
			
			echo json_encode(array('stat'=>false,'message'=>'余额不足'));
			return;
		}
		
		if($this->model->pay($arr)){
			$txt="成功操作 [转账]: [".$arr['paycard']."] 转入[".$arr['incomecard']."] 充值现金 [".$arr['amount'] ."]";
			
			try {
				
				$this->log->insertlog($txt,0);
			} catch (Exception $e) {
				
				echo json_encode(array('stat'=>false,'message'=>'未知错误'));
			}
			echo json_encode(array('stat'=>true,'message'=>'支付成功'));
		}else{
			echo json_encode(array('stat'=>false,'message'=>'操作失败'));
		}
	}
}
