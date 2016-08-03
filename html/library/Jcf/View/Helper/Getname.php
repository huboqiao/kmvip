<?php
/*
 * Created on 2014-4-14
 *
 * auther chenyong
 * 参数：$model  		模块名称
 *     $field   	要返回显示的字段名
 *     $id      	默认选中  注：所有的表的自增长为ID值
 *     $fieldid     表的主键自增长字段名 (默认是id)
 * 功能：根据用户ID返回用户名
 */
 
 class Jcf_View_Helper_Getname extends Zend_View_Helper_Abstract
{
	function Getname($model,$field,$id,$fieldid='id'){
		if($id != '' && $model != ''){
			$model = new $model();
			
			$where = array("$fieldid=?"=>$id);
			$result = $model->FetchRow($where);
			if($result){
				return $result->$field;
			}else{
				return '';
			}
		}
	}	
}
 
?>
