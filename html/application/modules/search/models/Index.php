<?
/**
 * create kylin 2014/9/26
 * 
 * 查询模型
 * 
 */
class Search_Model_Index extends Zend_Db_Table
{
	protected $_name = 'cardzz';
	public $modelname = '查询交易信息模块';
	
	
	public function queryczInfo($cardid,$wheres,$order,$numPerPage=0,$offset=0){
		// 		$order=' order by '.$order['orderby'].' '.$order['ordersc'].' ';
		$limit = '';
		if ($numPerPage>0) {
			$limit = ' limit '.$offset.','.$numPerPage.' ';
		}
		//order by cdate desc
		
		$sql = "SELECT a1.amount,'' as paycard,'' as membername,a1.cdate,a1.ctype,a1.txt"
			." FROM cardcz AS a1 "
			." WHERE a1.cardid = ".$cardid
			." ".$wheres.$order.$limit;
		$ctype=array('现金充值','刷卡充值');
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

	
	public function queryInfo($cardid,$wheres,$order,$numPerPage=0,$offset=0){      
		
       	$limit = '';
		if ($numPerPage>0) {
			$limit = ' limit '.$offset.','.$numPerPage.' ';
		} 
		
        $selectCz = ' SELECT a3.ctype,a3.amount,a3.cdate,IFNULL(txt,"") as txt,"" AS paycard,"" AS membername
        			FROM cardcz AS a3
					where a3.cardid = '.$cardid;
        
        $selectTx = ' SELECT (a3.ctype+2) as ctype,a3.amount,a3.cdate,IFNULL(txt,"") as txt,"" AS paycard,"" AS membername
        			FROM cardcz AS a3
					where a3.cardid = '.$cardid;
			
		$selectZO = 'SELECT (a3.ctype+4) AS ctype,a3.amount ,a3.cdate,IFNULL(txt,"") as txt,a3.incomecard AS paycard,IFNULL(d.membername,"") AS membername
					FROM cardzz AS a3    
		            LEFT JOIN `card` ON card.noid = a3.incomecard 
					LEFT JOIN `customer` AS d ON d.id = card.uid
					where a3.paycard = '.$cardid;
					  
        $selectZI = 'SELECT (a3.ctype+7) AS ctype,a3.amount ,a3.cdate,IFNULL(txt,"") as txt,a3.paycard,IFNULL(d.membername,"") AS membername
	          		FROM cardzz AS a3    
	          		LEFT JOIN `card` ON card.noid = a3.paycard 
	          		LEFT JOIN `customer` AS d ON d.id = card.uid
					where a3.incomecard = '.$cardid;  
#   
		$order = ' order by c.cdate desc '; 
       	$sql = '
                SELECT c.* FROM ( '.
                $selectCz.' UNION ALL '.
                $selectTx.' UNION ALL '.
				$selectZI.' UNION ALL '.
				$selectZO.' ) AS c '.
				''.$wheres.$order.$limit;
     
    $ctype=array('现金充值','刷卡充值','现金提现','银行卡转账','结算中心转出','终端转出','终端支付','结算中心转入','终端转入');
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
	
	
	
	
	public function queryzzInfo($cardid,$wheres,$order,$numPerPage=0,$offset=0){
		// 		$order=' order by '.$order['orderby'].' '.$order['ordersc'].' ';
		$limit = '';
		if ($numPerPage>0) {
			$limit = ' limit '.$offset.','.$numPerPage.' ';
		}
		//order by cdate desc 
		
		$sql = "SELECT a1.uid,a1.amount,a1.paycard,a1.cdate,a1.ctype,a1.txt,a3.membername"
			." FROM cardzz AS a1 "
			.' LEFT JOIN `card` AS a2 ON a1.paycard =a2.noid'
			." LEFT JOIN `customer` AS a3 ON a2.uid = a3.id"
			." WHERE a1.incomecard = ".$cardid
			." ".$wheres.$order.$limit;
		$ctype=array('结算中心转账','仓库转账','佣金收入');
		try {
			
			$result = $this->_db->query($sql)->fetchAll();
		} catch (Exception $e) {
			$result=array();
		}
		foreach ($result as $k=>$v){
			if ($v['ctype'] == 2) {
				$result[$k]['ctype'] = '佣金收入';
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
