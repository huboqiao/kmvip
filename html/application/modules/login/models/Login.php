<?php
/*
 * Created on 2013-6-11
 * 用户模块，视图初始化
 * auter huboqiao at 2013-06-11
 */
class Login_Model_Login
{
	function setView($model){
		//初始化视图及路径
		$viewRenderer = Zend_Controller_Action_HelperBroker::getStaticHelper('viewRenderer');
		if (null === $viewRenderer->view) {
			$viewRenderer->initView();
		}
		$view = $viewRenderer->view;
		//设置module为登陆模块
		$moduleName = $model;
		
		//设置视图模块完整跳径
		$basePath = dirname(Zend_Controller_Front::getInstance()->getModuleDirectory());
		$template = isset($view->{$moduleName}['template']) ? $view->{$moduleName}['template'] : 'default';
		
		if ($view->simpleModule) {
			$basePath =  $basePath.'/'. $moduleName . '/views/'. $template ;
		} else {
			$basePath = APPLICATION_PATH . '/templates/'.$moduleName.'/'. $template ;
		}
		$view->setScriptPath($basePath . '/scripts');
		
	} 	
	
}
?>
