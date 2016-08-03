<?php
class Admin_MenuController extends Jcf_Controller_Action
{

	public function init()
	{
		/* Initialize action controller here */

		parent::init();
		$this->model = new Admin_Model_Modules();
	}

	public function indexAction()
	{
		$this->view->modules = $this->model->getAllModules();
		$this->view->module = $this->model->getModuleByModule($_GET['m'],$_GET['a']);
	}

	public function countneworderAction(){
		$user = parent::getUser();
		$arr['order2number'] = $this->model->countneworder2();
		$arr['order3number'] = $this->model->countneworder3($user['uid']);
		$arr['ordernumber'] = $arr['order2number']+$arr['order3number'];
		echo json_encode($arr);
	}
	
}
