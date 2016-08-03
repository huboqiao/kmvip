<?php
/**
 * 用户登陆模块
 * 
 * 登陆采用md5单向加密
 * 
 * auther huboqiao at 2013-06-11
 */
class Login_IndexController extends Zend_Controller_Action
{
	
	function init(){
		#Zend_Layout::disableLayout();
	}
	function indexAction(){
		if (!empty($_REQUEST['id']) && $_REQUEST['id'] == '9aa04016a565adcfbd3cae29e292657d') {
//		if (true) {
			
			$request = $this->getRequest();
			
			$auth = Zend_Auth::getInstance();
			
			//判断是否登陆，如果登陆了就跳内页
			if($auth->hasIdentity()){
				header("Location: /");
			}
			$this->view->login = true;
			
			//如果用户提交就进行验证处理
			if($request->isPost()){
				$username = $request->getPost('username');
				$password = md5($request->getPost('password'));
				
				$adapter  = new Jcf_Auth_Auth($username,array());
				$result   = $auth->authenticate($adapter);
				
				
				switch($result->getCode()){
					case Jcf_Auth_Auth::NOT_ACTIVE:
						$this->view->error = '用户被禁止登陆,请联系管理员!';
					break;
					case Jcf_Auth_Auth::SUCCESS:
						$user = $auth->getIdentity();
					header("Location: /");
					break;
					case Jcf_Auth_Auth::FAILURE:
						$this->view->error = '此卡不可用';
					break;
				}
			}
		}else{
			
			$this->view->login = false;
		}
		
	}
	
	
	function uuuAction(){
		print_r($_REQUEST);
	}
	
	function loginoutAction(){
		Zend_Auth::getInstance()->clearIdentity();
		$this->redirect('/login/index');
	}
	
}
