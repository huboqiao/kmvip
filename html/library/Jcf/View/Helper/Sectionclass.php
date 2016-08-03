<?php
/**
 *加载部门分类
 *@auth hu at 2013-03-11
 */
class Jcf_View_Helper_Sectionclass extends Zend_View_Helper_Abstract
{
	public function Sectionclass($sid = 0,$pid=0){
		$mode = new Erp_Model_Section();
		$where = '';
		$result = $mode->fetchAll();
		$arr = array();
		foreach($result as $val){
			if($val->id != $pid){
				$arr[$val->id] = array('id'=>$val->id,'parentid'=>$val->parentid,'sectionname'=>$val->sectionname);
			}
		}
		$tree = new Jcf_Comm_Tree($arr);
		$str = "<option value=\$id \$selected> \$spacer\$sectionname</option>"; 
		return $tree->get_tree_multi(0,$str,$sid);
		
	}
}
?>
