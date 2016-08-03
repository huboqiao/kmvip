<?php
/**
 *加载产品分类
 * $sid 传入的id
 *@auth su at 2013-03-28
 */
class Jcf_View_Helper_Group extends Zend_View_Helper_Abstract
{
	public function Group($sid = 0,$pid=0){
		$mode = new Erp_Model_Group();
		$result = $mode->fetchAll();
		$arr = array();
		foreach($result as $val){
			if($val->id == $sid){$selected = 'selected=selected';}else{$selected = '';} 
			echo "<option value=$val->id $selected>$val->groupname</option>";
		}
		
	}
}
?>
