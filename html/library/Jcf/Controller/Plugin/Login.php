<?php
class Jcf_Controller_Plugin_Login extends Zend_Controller_Plugin_Abstract{
    public function preDispatch(Zend_Controller_Request_Abstract $request){

         $viewRenderer = Zend_Controller_Action_HelperBroker::getStaticHelper('viewRenderer');
         if(null == $viewRenderer){
            $viewRenderer->initView();
         }
         $auth = Zend_Auth::getInstance();
		//判断用户是否登陆
         if(!$auth->hasIdentity()){
         	//初始化视图及路径
	        $viewRenderer = Zend_Controller_Action_HelperBroker::getStaticHelper('viewRenderer');
	        if (null === $viewRenderer->view) {
	            $viewRenderer->initView();
	        }
	        $view = $viewRenderer->view;
	        //设置module为登陆模块
	        $moduleName = 'login';
	        
	        //设置视图模块完整跳径
	        $basePath = dirname(Zend_Controller_Front::getInstance()->getModuleDirectory());
	        $template = isset($view->{$moduleName}['template']) ? $view->{$moduleName}['template'] : 'default';

	        if ($view->simpleModule) {
	            $basePath =  $basePath.'/'. $moduleName . '/views/'. $template ;
	        } else {
	            $basePath = APPLICATION_PATH . '/templates/'.$moduleName.'/'. $template ;
	        }
	        $view->setScriptPath($basePath . '/scripts');

			//页面跳转
         	$request->setModuleName('login');
         	$request->setControllerName('index');
         	$request->setActionName('index');
        } else {
        	/*
        	//权限控制
        	$user = ($auth->getIdentity());
          	$acl = new Jcf_Acl_Acl();
         	$role = $user->gid;
			$action = $this->getRequest()->getActionName();
			$module=$this->getRequest()->getModuleName();
			$cont=$this->getRequest()->getControllerName();
         	if($module!=''&&$cont !='error' && $action !='erro'){	//排除错误页的控制器和动作
         		try{
					$res=$acl->check($role,$cont,$action,$module);     //开启关闭权限验证      
					switch ($res){
						case 1:
							$this->error("您没有执行该命令的权限");
							break;
						case 2:
							$this->error("您访问的地址不在权限范围内！");
							break;
						default:
							echo '';
					}
         		}catch(Exception $e){
					//echo $cont.'---'.$action.'</br>';
    				echo $e;     			
         		}
         	}
        */
        }
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
	protected function error($message, $ajax = false) {
		$this->ajaxReturn ( 300, $message );
	}
}
?>
