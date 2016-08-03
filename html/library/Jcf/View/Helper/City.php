<?php
	/**
	 * 省市区三级联动助手
	 */
class Jcf_View_Helper_City extends Zend_View_Helper_Abstract{
	
	public function City($id=null){
		$model = new Supplier_Model_Area;
		$where = 'parent_id=1';
		$result = $model->fetchAll($where);
		
		$html = '<select id="province" name=province_id class="required">';
		$html .= '<option value="">请选择</option>';
		
		foreach ($result as $val){
			$html .='<option value="'.$val[region_id].'">'.$val[region_name].'</option>';
		}
		
		$html .= '</select>';
		return $html;
	}
}
?>