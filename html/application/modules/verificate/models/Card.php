<?
/**
 * create kylin 2014/9/26
 * 
 * 查询模型
 * 
 */
class Verificate_Model_Card extends Zend_Db_Table
{
	protected $_name = 'card';
	public $modelname = '查询交易信息模块';
	
	/**
	 * 判断卡号与用户名是否匹配
	 * @param unknown $cid
	 * @param unknown $cname
	 * @return mixed
	 */
	public function isrealCard($cid){
		if (file_exists(APPLICATION_PATH . '/configs/application.ini'))
		{
			$data = parse_ini_file(APPLICATION_PATH . '/configs/application.ini',true);
			if ($data)
			{
				// 				print_r($data);
			}
		}
		
		$sql = 'select membername,customerinfo.useimg_path,customer.amount,noid from card '
			.'left join customer on card.uid = customer.id '
			.'left join customerinfo on customer.id = customerinfo.cid '
			."where card.cardid='".$cid."' and card.stat=1 and customer.stat=1";
		// 		print $sql;
		try {
			
			$data=$this->_db->query($sql)->fetch();
		} catch (Exception $e) {
			return array('stat'=>false);
		}
		if ($data) {
			$result['stat'] = true;
			$result['membername'] = $data['membername'];
			$result['useimg_path'] = $data['useimg_path'];
			$result['amount'] = sprintf("%.2f", $data['amount']);
			//$result['test'] = $application;
			$result['noid'] = $data['noid'];
		}else{
			$result['stat'] = false;
		}
		
		return $result;
		
	}
	
	/**
	 * 根据noid获取uid
	 */
	public function getUinfoByNoid($noid,$field){
		$select = $this->_db->select();
		$select->from($this->_name, array($field))
		->where('noid=?', $noid);
		$result = $this->_db->fetchRow($select);
		return $result[$field];
		
	}
	
	/**
	 * 根据cardid获取noid
	 */
	public function getNoid($cardid){
		$select = $this->_db->select();
		$select->from($this->_name, array('noid'))
		->where('cardid=?', $cardid);
		$result = $this->_db->fetchRow($select);
		return $result['noid'];
		
	}
	
	public function checkPassword($cardid,$password){
		$select = $this->_db->select();
		$select->from($this->_name, array('count(*) as num'))
		->where('cardid=?', $cardid)
		->where('password=?',md5($password));
		$result = $this->_db->fetchRow($select);
		if ($result['num']>0) {
			return array('stat'=>true);
		}else{
			return array('stat'=>false);
		}
	}
	
}

?>
