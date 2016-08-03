<?php
/**
 
 */
class Verificate_CardController extends Jcf_Controller_Action
{
	
	function init(){
		parent::init();
		$this->model = new Verificate_Model_Card();
	}
	function indexAction(){
	}
	function checkAction(){
		//验证卡是否合法
		$cardid = $_POST['cardid'];
		$model = new Verificate_Model_Card();
		$result = $model->isrealCard($cardid);
		echo json_encode($result);
	}
	
	function keyboardAction(){
		//显示键盘
		$numarr = range(0,9);
		shuffle($numarr);
		$this->view->numarr = $numarr;
		
	}
	function keyboardmoneyAction(){
		//显示键盘
		$numarr = range(1,9);
		$numarr[] = 0;
		$this->view->numarr = $numarr;
		
	}
	
	function checkpasswordAction(){
		//验证密码是否争取
		$cardid = $_POST['cardid'];
		$password = $_POST['password'];
		$model = new Verificate_Model_Card();
		$result = $model->checkPassword($cardid,$password);
		echo json_encode($result);
	}
}
