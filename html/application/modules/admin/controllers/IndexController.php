<?php
class Admin_IndexController extends Jcf_Controller_Action
{
	
	public function init()
		{
		/* Initialize action controller here */
		parent::init();
		$this->model = new Admin_Model_Modules();
		}
	
	public function indexAction()
		{
		//验证可调用模块
		//获取模块数据
		$modules = $this->model->getFirstModules();
		$this->view->modules = $modules;
		}
	
}
