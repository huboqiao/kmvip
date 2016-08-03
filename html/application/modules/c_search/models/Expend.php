<?
/**
 * create kylin 2014/9/26
 * 
 * 查询模型
 * 
 */
class Search_Model_Expend extends Zend_Db_Table
{
	protected $_name = 'cardzz';
	public $modelname = '查询交易信息模块';
	

	public function querytxInfo($cardid,$wheres,$order,$numPerPage=0,$offset=0){
		// 		$order=' order by '.$order['orderby'].' '.$order['ordersc'].' ';
		$limit = '';
		if ($numPerPage>0) {
			$limit = ' limit '.$offset.','.$numPerPage.' ';
		}
		//order by cdate desc
	
		$sql = "SELECT a1.amount,'' as incomecard,'' as membername,a1.cdate,a1.ctype,a1.txt"
				." FROM cardtx AS a1 "
				." WHERE a1.cardid = ".$cardid
				." ".$wheres.$order.$limit;
		$ctype=array('现金提现','银行卡转账');
		try {
	
			$result = $this->_db->query($sql)->fetchAll();
		} catch (Exception $e) {
			$result=array();
		}
		foreach ($result as $k=>$v){
			$result[$k]['ctype'] = $ctype[$v['ctype']];
		}
	
		return $result;
	}
	public function allcount($cardid){
		$sql = "SELECT sum(a1.amount) as allcount"
				." FROM cardtx AS a1 "
				." WHERE a1.cardid = ".$cardid;
		try {
		
			$result= $this->_db->query($sql)->fetch();
			$allcount = $result['allcount'];
		} catch (Exception $e) {
			$allcount = 0;
		}
		$sql = "SELECT sum(a1.amount) as allcount"
				." FROM cardzz AS a1 "
				." WHERE a1.paycard = ".$cardid;
		try {
		
			$result= $this->_db->query($sql)->fetch();
			$allcount += $result['allcount'];
		} catch (Exception $e) {
			$allcount += $allcount;
		}
		return $allcount;
	}
	public function queryzzInfo($cardid,$wheres,$order,$numPerPage=0,$offset=0){
// 		$order=' order by '.$order['orderby'].' '.$order['ordersc'].' ';
		$limit = '';
		if ($numPerPage>0) {
			$limit = ' limit '.$offset.','.$numPerPage.' ';
		}
		//order by cdate desc 
		
		$sql = "SELECT a1.uid,a1.amount,a1.incomecard,a1.cdate,a1.ctype,a1.txt,a4.membername"
				." FROM cardzz AS a1 "
				.' LEFT JOIN `card` AS a2 ON a1.paycard =a2.noid'
				." LEFT JOIN `card` AS a3 ON a1.incomecard = a3.noid"
				." LEFT JOIN `customer` AS a4 ON a3.uid = a4.id"
				." WHERE a1.paycard = ".$cardid
            	." ".$wheres.$order.$limit;
		$ctype=array('结算中心转账','仓库转账','佣金支付');
		try {

			$result = $this->_db->query($sql)->fetchAll();
		} catch (Exception $e) {
			$result=array();
		}
		foreach ($result as $k=>$v){
			if ($v['ctype'] == 2) {
				$result[$k]['ctype'] = '佣金支付';
			}else if($v['uid'] == 0){
				$result[$k]['ctype'] = '仓库转账';
			}else{
				$result[$k]['ctype'] = '结算中心转账';
			}
		}
		
		return $result;
	}
	
	public function getModuleByModule($module){

		$where = array('module=?'=>$module);
		return $this->fetchRow($where);
	}
}

?>
