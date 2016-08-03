<?php
/**
 *职称分类
 *$sid 传入的id
 *@auth su at 2013-03-11
 */
class Jcf_View_Helper_Place extends Zend_View_Helper_Abstract
{
	public function Place($sid = 0,$pid=0){
		$mode = new Erp_Model_Place();
		$result = $mode->fetchAll();
		$arr = array();
		foreach($result as $val){
			if($val->id == $sid){$selected = 'selected=selected';}else{$selected = '';} 
			echo "<option value=$val->id $selected>$val->placename</option>";
		}
		
	}
}
?>
