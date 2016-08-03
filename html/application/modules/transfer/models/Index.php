<?php 
class Transfer_Model_Index extends Zend_Db_Table{
	
	protected $_name="customer";
	public $modelname = '转账交易模块';
	
	public function queryUserName($uid){
		$where = array('id=?'=>$uid);
		
		try {
			
			$select = $this->select();
			$select->from($this,array('membername'))
			->where('id=?',$uid);
			
			$row = $this->fetchRow($select)->toArray();
			return $row['membername'];
		} catch (Exception $e) {
			
		}
	}
	
	public function pay($arr){
		$db = $this->_db;
		//付款方id
		$model = new Verificate_Model_Card();
		$payuid= $model->getUinfoByNoid($arr['paycard'],'uid');
		//收款方id
		$incomeuid = $model->getUinfoByNoid($arr['incomecard'],'uid');
		$db->beginTransaction();//开启事务
		try {
			
			//修改cardzz表
			$db->insert('cardzz', $arr);
			
			$zzid = $db->lastInsertId();
			//修改付款方余额
			$model = new Verificate_Model_Customer();
			$user = $model->getInfosByUid($payuid, array('amount','freezen'));
			$model->update(array('amount'=>($user['amount']-$arr['amount'])),array('id=?'=>$payuid));
			$db->update('cardzz',
			array('paybalance'=>($user['amount']-$arr['amount']+$user['freezen'])),
			array('id = ?'=>$zzid));
			
			//修改收款方余额
			$user = $model->getInfosByUid($incomeuid, array('amount','freezen'));
			$model->update(array('amount'=>$user['amount']+$arr['amount']),array('id=?'=>$incomeuid));
			$db->update('cardzz',
			array('payeebalance'=>($user['amount']+$arr['amount']+$user['freezen'])),
			array('id = ?'=>$zzid));
		} catch (Exception $e) {
			$db->rollBack();
			return false;
		}
		$db->commit();
		return true;
	}
	
	public function isEnoughAmount($card,$amount){
		
		$model = new Verificate_Model_Card();
		$uid= $model->getUinfoByNoid($card,'uid');
		$model = new Verificate_Model_Customer();
		$uamount = $model->getInfoByUid($uid, 'amount');
		return $uamount>=$amount?true:false;
	}
}
?>