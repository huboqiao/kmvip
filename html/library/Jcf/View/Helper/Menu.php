<?php
/**
 *动态加载系统菜单
 *@auth hu at 2013-03-11
 */
class Jcf_View_Helper_Menu extends Zend_View_Helper_Abstract
{
	public function Menu($catid=0){
		$model = new Admin_Model_Menu();
		$html = '';
		$where = 'parent_id = '.$catid.' and is_active = 1 AND action ="index"';
		$order = ' sortid asc';
		$result = $model->fetchAll($where,$order);
		foreach($result as $val){
			$html .= '<div class="accordionHeader"><h2><span>Folder</span>'.$val->re_name.'</h2></div> ';
			$where = 'parent_id ='.$val->id.' and is_active = 1 AND action ="index"';
			$arr = array();
			try{
				$row = $model->fetchAll($where,$order);
			}catch(Exception $e){
				print_r($e);
			}
			if(count($row)){
				$html .= '<div class="accordionContent">';
				$html .= '<ul  class="tree treeFolder">';
				foreach($row as $val2){
					$where2 = 'parent_id = '.$val2->id.' and is_active = 1 AND action ="index"';
					$row2 = $model->fetchAll($where2,$order);
					if(count($row2)){
						$html .= '<li><a >'.$val2->re_name.'</a>';
						$html .= '<ul>';
						foreach($row2 as $val3){
							$html .= '<li><a href="/'.$val3->module.'/'.$val3->controller.'" target="navTab" rel="'.$val3->controller.'">'.$val3->re_name.'</a></li>';
						}
						$html .= '</ul></li>';
					}else{
						$html .= '<li><a rel="'.$val2->controller.'"  href="/'.$val2->module.'/'.$val2->controller.'" target="navTab">'.$val2->re_name.'</a></li>';
					}
				}
				$html .= '</ul>';
				$html .= '</div>';
			}
		}
		return $html;
	}
}
?>
