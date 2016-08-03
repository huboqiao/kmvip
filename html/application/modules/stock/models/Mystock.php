<?php 
class Stock_Model_Mystock extends Zend_Db_Table{
	
	protected $_name="order";
	public $modelname = '商品入库模块';
	
	public function queryInfo($uid,$wheres='',$order='',$numPerPage=0,$offset=0){
		$order='  ';
		$limit = '';
		if ($numPerPage>0) {
			$limit = ' limit '.$offset.','.$numPerPage.' ';
		}
		//order by cdate desc
		
		$sql = "SELECT a1.id,a2.goods_id,SUM(a2.goods_numbers) as goods_numbers,a3.pname ,a3.unit"
			." FROM `order` AS a1 "
			." INNER JOIN `stock_into` AS a4 on a1.id = a4.oid "
			." INNER JOIN `stock` AS a2 on a4.id = a2.sid "
			." INNER JOIN `goods` AS a3 on a2.goods_id = a3.id"
			." WHERE a1.cid = ".$uid
			." ".$wheres
			."  GROUP BY goods_id "
			.$order.$limit;
		try {
			$result = $this->_db->query($sql)->fetchAll();
		} catch (Exception $e) {
			$result=array();
		}
		return $result;
	}	
	
	//查询订单编码
	public function queryOdersn($oid){
		$this->fetchRow(array('id=?'=>$oid))->toArray();
		return $result['ordersn'];
	}
	
	public function queryGoods($oid,$wheres='',$order='',$numPerPage=0,$offset=0){
		$order='  ';
		$limit = '';
		if ($numPerPage>0) {
			$limit = ' limit '.$offset.','.$numPerPage.' ';
		}
		
		//查询订单表，订单详情表和商品表
		$sql = "SELECT a1.id,a1.ordersn,a1.price as amount,a1.cdate,"
			." a2.price,a2.unit,a2.counts, "
			." a3.pname "		
			." FROM `order` AS a1 "
			." INNER JOIN `order_info` as a2 on a1.id=a2.orderid"
			." INNER JOIN `goods` as a3 on a2.goodsid=a3.id"
			." WHERE a1.id =".$oid." "." ".$wheres
			.$order.$limit;
		try {
			$result = $this->_db->query($sql)->fetchAll();
			echo '848383';
			
		} catch (Exception $e) {
			$result=array();
		}
		
		foreach($result as $k=>$v){
			$result[$k]['plus'] = $v['price']*$v['counts'];
		}
		return $result;
	}
	
	public function input($oid){
		
		$db = $this->_db;
		//查询订单详情表
		$sql='SELECT a1.goodsid,a1.counts '
			.' FROM `order_info` as a1 '
			.' WHERE a1.orderid ='.$oid;
		
		try {
			
			$result = $db->query($sql)->fetchAll();
		}catch( Exception $e){
			return false;
		}
		
		
		
		//开启事务
		
		$db->beginTransaction();//开启事务
		//修改库存表
		foreach ($result as $k=>$v){
			$insert['orderid'] = $oid;
			$insert['goods_id'] = $v['goodsid'];
			$insert['goods_numbers'] = $v['counts'];
			$insert['cdate'] = time();
			try{
				
				$db->insert('stock',$insert);
			}catch( Exception $e){
				$db->rollBack();
				return false;
			}
		}
		//修改订单表，订单状态
		try{
			
			$db->update('order',array('ostat'=>2),array('id = ?'=>$oid));
		}catch( Exception $e){
			$db->rollBack();
			return false;
		}
		$db->commit();
		return true;
	}
}

?>