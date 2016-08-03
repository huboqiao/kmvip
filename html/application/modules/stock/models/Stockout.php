<?php 
class Stock_Model_Stockout extends Zend_Db_Table{
	
	protected $_name="order";
	public $modelname = '商品入库模块';
	
	public function queryInfo($uid,$wheres='',$order='',$numPerPage=0,$offset=0){
		$order='  ';
		$limit = '';
		if ($numPerPage>0) {
			$limit = ' limit '.$offset.','.$numPerPage.' ';
		}
		//order by cdate desc
		
		$sql = "SELECT a1.*,a2.ordersn "
			." FROM `stock_outto` AS a1 "
			." LEFT JOIN `order` AS a2 ON a1.oid = a2.id "
			." WHERE a1.cid =".$uid
			." ".$wheres.$order.$limit;
		try {
			
			$result = $this->_db->query($sql)->fetchAll();
		} catch (Exception $e) {
			$result=array();
		}
		$type = array('采购出库','自主出库');
		foreach($result as $k => $v){
			$result[$k]['type'] = $type[$v['type']];
		}
		return $result;
	}
	
	public function queryGoods($oid,$wheres='',$order='',$numPerPage=0,$offset=0){
		$order='  ';
		$limit = '';
		if ($numPerPage>0) {
			$limit = ' limit '.$offset.','.$numPerPage.' ';
		}
		
		//查询订单表，订单详情表和商品表
		$sql = "SELECT a1.*,"
			." a2.suk,a5.counts as goods_numbers, "
			." a3.pname,"
			." a4.ordersn,a4.price as amount,"
			." a5.price"		
			." FROM `stock_outto` AS a1 "
			." INNER JOIN `order` AS a4 on a1.oid = a4.id"
			." INNER JOIN `stock_into` as a6 on a4.id=a6.oid"
			." INNER JOIN `stock` as a2 on a6.id=a2.sid"
			." INNER JOIN `goods` as a3 on a2.goods_id=a3.id"
			." INNER JOIN `order_info` AS a5 on a1.oid = a5.orderid AND a3.id = a5.goodsid"
			." WHERE a1.id =".$oid." "." ".$wheres
			.$order.$limit;
		try {
			$result = $this->_db->query($sql)->fetchAll();
			
		} catch (Exception $e) {
			$result=array();
		}
		$type=array('采购出库','自主出库');
		foreach($result as $k=>$v){
			$result[$k]['type'] = $type[$v['type']];
			$result[$k]['plus'] = $v['price']*$v['goods_numbers'];
		}
		return $result;
	}
	
	//查询订单编码
	public function queryOdersn($oid){
		$result = $this->fetchRow(array('id=?'=>$oid))->toArray();
		return $result['ordersn'];
	}
	public function output($data){
		$db = $this->_db;
		$oid = $data['oid'];
		
		$sql = "select id from stock_into where oid = ".$oid;
		$result = $db->query($sql)->fetch();
		$sid =  $result['id'];
		//开启事务
		
		$db->beginTransaction();//开启事务
		//修改库存数量
		try{
			$db->update('stock',array('goods_numbers'=>0),array('sid = ?'=>$sid));
		}catch( Exception $e){
			$db->rollBack();
			return false;
		}
		//添加库存表记录
		$insert =array();
		$insert['type'] = $data['type'];
		$insert['oid'] = $data['oid'];
		$insert['stock_on'] = $data['stock_on'];
		$insert['indate'] = time();
		$insert['cdate'] = strtotime($data['cdate']);
		$insert['cid'] =$data['uid'];
		
		try{
			
			$db->insert('stock_outto',$insert);
		}catch( Exception $e){
			$db->rollBack();
			return false;
		}
		//修改订单表，订单状态
		try{
			$db->update('order',array('ostat'=>3),array('id = ?'=>$oid));
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
			.' WHERE ostat = 2 and cid = '.$uid;
		try {
			$data = $this->_db->query($sql)->fetchAll();
			$result = array('stat'=>true,'data'=>$data);
			
		} catch (Exception $e) {
			$result = array('stat'=>false,'msg'=>'无记录');
		}
		
		return $result;
	}
	public function pageoutput($oid){
		$db = $this->_db;
		$sql = 'SELECT a1.ordersn,a1.price as amount ,'
			.' a3.price,a3.unit,a3.counts,a3.goodsid,'
			.' a4.pname,'
			.' a5.suk,a5.sid'
			.' FROM `order` as a1'
			.' left JOIN `stock_into` as a2 ON a1.id = a2.oid'
			.' left JOIN `order_info` as a3 ON a2.oid = a3.orderid'
			.' left JOIN `goods` as a4 ON a3.goodsid  = a4.id'
			.' left JOIN `stock` as a5 ON a2.id  = a5.sid AND a4.id = a5.goods_id'
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