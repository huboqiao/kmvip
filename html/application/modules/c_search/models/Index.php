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
	
	
	public function qeuryCardzz($cardid,$wheres,$order,$numPerPage=0,$offset=0){
		$order=' order by '.$order['orderby'].' '.$order['ordersc'].' ';
		$limit = '';
		if ($numPerPage>0) {
			$limit = ' limit '.$offset.','.$numPerPage.' ';
		}
		//order by cdate desc 
		
		$sql = "SELECT a1.id,a1.amount,a1.incomecard,a3.membername,a1.cdate "
				." FROM cardzz AS a1,card AS a2 ,customer AS a3 "
				."WHERE a1.incomecard = a2.noid AND a2.uid = a3.id AND paycard =".$cardid
            	." ".$wheres.$order.$limit;
		try {

			$result =$result = $this->_db->query($sql)->fetchAll();
		} catch (Exception $e) {
			$result=array();
		}
		
		return $result;
	}
	
	public function getModuleByModule($module){

		$where = array('module=?'=>$module);
		return $this->fetchRow($where);
	}
}

?>
