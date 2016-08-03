<?
class Admin_Model_Modules extends Zend_Db_Table
{
	protected $_name = 'modules';
	public $modelname = '模块信息表模块';

	public function getFirstModules(){
		$result = $this->fetchAll(array('is_show=?'=>1,'parent=?'=>0))->toArray();
		foreach($result as $i=>$v){
			
			$result[$i]['child'] = array();
			$subresult = $this->fetchRow(array('is_show=?'=>1,'parent=?'=>$v['id']));
			if ($subresult) {
				$result[$i]['child'] = $subresult->toArray();
			}
			//子类
			
		}
		return $result;
	}
	
	public function getAllModules(){
		$result = $this->fetchAll(array('is_show=?'=>1,'parent=?'=>0))->toArray();
		foreach($result as $i=>$v){
			$subresult = $this->fetchAll(array('is_show=?'=>1,'parent=?'=>$v['id']))->toArray();
			//子类
			$result[$i]['child'] = $subresult;
			
		}
		return $result;
	}
	
	public function getModuleByModule($module,$submodule){
		
		$href=$module.'/'.$submodule;
		if ($submodule == 'index') {
			$where = array('module=?'=>$module);
		}else{
			$where = array('module=?'=>$submodule);
		}
		$result = $this->fetchRow($where)->toArray();
		$result['href'] = $href;
		return $result;
	}
	
	public function countneworder2(){
		
		$sql = "SELECT count(*) as ordernumber"
			." FROM `order` AS a1 "
			." WHERE a1.cid =0 and a1.ostat=1 and a1.pstat=1 ";
		try {
			
			$result = $this->_db->query($sql)->fetch();
			return $result['ordernumber'];
		} catch (Exception $e) {
			return 0;
		}
		
	}
	
	public function countneworder3($uid){
		
		$sql = "SELECT count(*) as ordernumber"
			." FROM `order` AS a1 "
			." WHERE a1.cid =".$uid." and a1.ostat=1 and a1.pstat=0 and cstat=0";
		try {
			
			$result = $this->_db->query($sql)->fetch();
			return $result['ordernumber'];
		} catch (Exception $e) {
			return 0;
		}
		
	}
	
}

?>
