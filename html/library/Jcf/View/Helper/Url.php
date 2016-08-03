<?php
/**
 *@auth hu at 2013-03-11
 */
class Jcf_View_Helper_Url extends Zend_View_Helper_Abstract
{
		function url(){
			$config = new Zend_Config_Ini('./application/configs/application.ini','production');
			return $config->resources->view->assign->baseUrl;
		}
	
}