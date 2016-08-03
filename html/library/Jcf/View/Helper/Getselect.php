<?php
/**
 * 获取用户名
 * 参数：	$tbname  模块名称
 *      $name    列表name值
 *      $field   要返回显示的字段名
 *      $id      默认选中  注：所有的表的自增长为ID
 *      $required 是否必选 默认为不是必须，如果需要必选传一个1过来
 *      $fieldid 表的主键自增长字段名（默认为id）
 *@auth chenyong at 2014-04-14
 */
class Jcf_View_Helper_Getselect extends Zend_View_Helper_Abstract
{
		function Getselect($tbname,$name,$field,$id='',$required='',$fieldid='id'){
			if($required == ''){
				$html = '<select name="'.$name.'" class="combox">';
			}else{
				$html = '<select name="'.$name.'" class="required combox">';
			}
			$html .= '<option value="">请选择</option>';
			$model = new $tbname();
			$result = $model->fetchAll();
			foreach($result as $key=>$val){
				
				//如果传入ID就将该ID设为己选择
				if($id != '' && $val["$fieldid"] == $id){
					$html .= '<option value="'.$val["$fieldid"].'" selected>'.$val[$field].'</option>';
				}else{
					$html .= '<option value="'.$val["$fieldid"].'" >'.$val[$field].'</option>';
				}
			}
			
			$html .= '</select>';
			return $html;
		
			
		}
	
}