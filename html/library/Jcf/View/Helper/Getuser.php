<?php
/**
 * 获取用户名
 *@auth hu at 2013-03-11
 */
class Jcf_View_Helper_Getuser extends Zend_View_Helper_Abstract
{
		function Getuser($name,$id=''){
			$html = '<select name="'.$name.'" class="combox">';
			$html .= '<option value="">请选择</option>';
			$model = new Sys_Model_User;
			$result = $model->fetchAll();
			foreach($result as $key=>$val){
				
				//如果传入ID就将该ID设为己选择
				if($id != '' && $val['id'] == $id){
					$html .= '<option value="'.$val['id'].'" selected>'.$val['username'].'</option>';
				}else{
					$html .= '<option value="'.$val['id'].'" >'.$val['username'].'</option>';
				}
			}
			
			$html .= '</select>';
			return $html;
		
			
		}
	
}