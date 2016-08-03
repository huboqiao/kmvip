<?php
/**
 * 商铺交易模块
 * 
 * auther kylin at 2014/9/27
 * 
 */
class Shop_IndexController extends Jcf_Controller_Action
{
	
	function init(){
		parent::init();
		$this->model = new Shop_Model_Shop();
	}
	function indexAction(){
		//获取登录商铺信息
		$user = parent::getUser();
		$this->view->noid = $user['noid'];
		$this->view->username = $this->model->queryUserName($user['uid']);
	}
	
	function payAction(){
// 		echo json_encode($_REQUEST);
		$model = new Verificate_Model_Card();
		if ($model->isrealCard($_REQUEST['paycard'], $_REQUEST['payname'])) {
			
			$arr['paycard'] = $_REQUEST['paycard'];
			$user = parent::getUser();
			$arr['incomecard'] = $user['noid'];
			$arr['amount'] = $_REQUEST['amount']*$_REQUEST['rate']/10;
			$arr['cdate'] = time();
			$arr['ctype'] = 1;
			$arr['uid'] = 0;
			//判断余额是否足够
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
			
		}else{
			echo json_encode(array('stat'=>false,'message'=>'用户名或卡号不对'));
		}
	}
	
}
