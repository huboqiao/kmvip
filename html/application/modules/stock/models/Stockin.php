<?php 
class Stock_Model_Stockin extends Zend_Db_Table{
	
	protected $_name="stock_into";
	public $modelname = '商品入库模块';
	
	public function queryInfo($uid,$wheres='',$order='',$numPerPage=0,$offset=0){
		$order='  ';
		$limit = '';
		if ($numPerPage>0) {
			$limit = ' limit '.$offset.','.$numPerPage.' ';
		}
		//order by cdate desc
		
		$sql = "SELECT a1.*,a2.ordersn "
			." FROM `stock_into` AS a1 "
			." LEFT JOIN `order` AS a2 ON a1.oid = a2.id "
			." WHERE a1.cid =".$uid
			." ".$wheres.$order.$limit;
		try {
			
			$result = $this->_db->query($sql)->fetchAll();
		} catch (Exception $e) {
			$result=array();
		}
		$type = array('采购入库','自主入库');
		foreach($result as $k => $v){
			$result[$k]['type'] = $type[$v['type']];
		}
		return $result;
	}	
	
	//查询订单编码
	public function queryOdersn($oid){
		$result = $this->fetchRow(array('id=?'=>$oid))->toArray();
		return $result['ordersn'];
	}
	
	public function queryGoods($oid,$wheres='',$order='',$numPerPage=0,$offset=0){
		$order='  ';
		$limit = '';
		if ($numPerPage>0) {
			$limit = ' limit '.$offset.','.$numPerPage.' ';
		}
		
		//查询订单表，订单详情表和商品表
		$sql = "SELECT a1.*,"
			." a2.suk,a5.counts as goods_numbers,"
			." a3.pname,"
			." a4.ordersn,a4.price as amount,"
			." a5.price"		
			." FROM `stock_into` AS a1 "
			." INNER JOIN `order` AS a4 on a1.oid = a4.id"
			." INNER JOIN `stock` as a2 on a1.id=a2.sid"
			." INNER JOIN `goods` as a3 on a2.goods_id=a3.id"
			." INNER JOIN `order_info` AS a5 on a1.oid = a5.orderid AND a3.id = a5.goodsid"
			." WHERE a1.id =".$oid." "." ".$wheres
			.$order.$limit;
		try {
			$result = $this->_db->query($sql)->fetchAll();
			
		} catch (Exception $e) {
			$result=array();
		}
		$type=array('采购入库','自主入库');
		foreach($result as $k=>$v){
			$result[$k]['type'] = $type[$v['type']];
			$result[$k]['plus'] = $v['price']*$v['goods_numbers'];
		}
		return $result;
	}
	
	public function input($data){
		
		$db = $this->_db;
		$oid = $data['oid'];
		$g = $data['g'];
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
		
		//添加库存表记录
		$insert =array();
		$insert['type'] = $data['type'];
		$insert['oid'] = $data['oid'];
		$insert['stock_on'] = $data['stock_on'];
		$insert['indate'] = time();
		$insert['cdate'] = strtotime($data['cdate']);
		$insert['cid'] =$data['uid'];
		
		try{
			
			$db->insert('stock_into',$insert);
			$sid = $db->lastInsertId();
		}catch( Exception $e){
			$db->rollBack();
			return false;
		}
		
		
		//修改库存表
		$insert = array();
		foreach ($result as $k=>$v){
			$insert['sid'] = $sid;
			$insert['goods_id'] = $v['goodsid'];
			$insert['goods_numbers'] = $v['counts'];
			$insert['suk'] = $g[$v['goodsid']];
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
	
	public function getOrderlist($uid){
		$db = $this->_db;
		$sql = 'SELECT id,ordersn '
			.' FROM `order` '
			.' WHERE (ostat = 1 and cid = '.$uid.' and pstat = 1)'
			.' or (ostat = 1 and cid = '.$uid.' and pstat = 0 and cstat=1)';
		try {
			$data = $this->_db->query($sql)->fetchAll();
			$result = array('stat'=>true,'data'=>$data);
			
		} catch (Exception $e) {
			$result = array('stat'=>false,'msg'=>'无记录');
		}
		
		return $result;
	}
	public function pageinput($oid){
		$db = $this->_db;
		$sql = 'SELECT a1.ordersn,a1.price as amount ,'
			.' a2.price,a2.unit,a2.counts,a2.goodsid,'
			.' a3.pname'
			.' FROM `order` as a1'
			.' INNER JOIN `order_info` as a2 ON a1.id = a2.orderid'
			.' INNER JOIN `goods` as a3 ON a2.goodsid  = a3.id'
			.' WHERE a1.id = '.$oid;
		try {
			$result = $this->_db->query($sql)->fetchAll();
			
		} catch (Exception $e) {
			$result = array();
		}
		foreach($result as $k=>$v){
			
			$result[$k]['plus'] = $v['price']*$v['counts'];
		}
		return $result;
	}
}

?>