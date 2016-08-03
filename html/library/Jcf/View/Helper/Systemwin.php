<?php
/*
 * Created on 2013-08-19
 *
 * auther chenyong
 * 功能：判断用户所在组，根据其权限，给出快捷设置
 */
 
 class Jcf_View_Helper_Systemwin extends Zend_View_Helper_Abstract
{
	function Systemwin(){
		$auth = Zend_Auth::getInstance();
		$user = ($auth->getIdentity());
		$role = $user->gid;
		$id=$user->id;
		if($role==5){
			echo '<a href="'.$this->url().'/admin/systemwin" target="dialog" width="600">设置</a>';	
		}else{
			echo '<a href="'.$this->url().'/sys/user/viewpwdedit?id='.$id.'" target="dialog" width="600">修改密码</a>';
		}
	}
	function url(){
			$config = new Zend_Config_Ini('./application/configs/application.ini','production');
			return $config->resources->view->assign->baseUrl;
		}	
}
 
?>
