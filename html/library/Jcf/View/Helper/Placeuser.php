<?php
/**
 *查询当前用户的职称使用量 place.id=placeid
 *$id 传入的id
 *@auth su at 2013-03-11
 */
class Jcf_View_Helper_Placeuser extends Zend_View_Helper_Abstract
{
	public function Placeuser($id){
		$mode = new Erp_Model_User();
		$result = $mode->sumPlace($id);
		return $result.'个雇员';	
	}
}
?>
