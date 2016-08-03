<?
/**
 * create kylin 2014/9/26
 * 
 * 查询模型
 * 
 */
class Verificate_Model_Customer extends Zend_Db_Table
{
	protected $_name = 'customer';
	public $modelname = '查询用户信息模块';
	
	/**
	 * 判断卡号与用户名是否匹配
	 * @param unknown $cid
	 * @param unknown $cname
	 * @return mixed
	 */
	public function getInfoByUid($uid,$field){
		$select = $this->_db->select();
		$select->from($this->_name, array($field))
		->where('id=?', $uid);
		$result = $this->_db->fetchRow($select);
		return $result[$field];
		
	}
	public function getInfosByUid($uid,$arr){
		$select = $this->_db->select();
		$select->from($this->_name, $arr)
		->where('id=?', $uid);
		$result = $this->_db->fetchRow($select);
		return $result;
		
	}
	
}

?>
