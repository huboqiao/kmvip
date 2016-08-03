<?php
/**
 *采购订单审核与反审核
 *auther:ivan at 2013-06-25
 */
class Jcf_View_Helper_Orderreview extends Zend_View_Helper_Abstract
{
	public function Orderreview($id,$flag=true){
		$model = new Pur_Model_Po;
		
		$where = array('id=?'=>$id);
		$result = $model->fetchRow($where);
		if($flag){
			if($result['ckflag']==0){
				echo '<input type="checkbox" name="ckflag" value="1" />审核通过';
			}else{
				echo '<span style="color:green">已审核通过</span>&nbsp;|&nbsp;<input type="checkbox" name="ckflag" value="0" />反审核';
			}
		}else{
			if($result['ckflag']==0){
				echo '<span style="color:red">没有通过审核</span>';
			}else{
				echo '<span style="color:green">已审核通过</span>';
			}
			
		}
		
	}
}
?>
