<?php 
class Order_Model_Ordershop extends Zend_Db_Table{
	
	protected $_name="order";
	public $modelname = '订单模块';
	
	public function queryInfo($wheres='',$order='',$numPerPage=0,$offset=0){
		$order='  ';
		$limit = '';
		if ($numPerPage>0) {
			$limit = ' limit '.$offset.','.$numPerPage.' ';
		}
		//order by cdate desc
		
		$sql = "SELECT a1.* ,sum(a2.price*a2.counts) as amount"
				." FROM `order` AS a1 "
				." LEFT JOIN `order_info` AS a2 ON a1.id = a2.orderid"
				." WHERE a1.cid =0 and a1.ostat=1 and a1.pstat=1 "
				." ".$wheres
				." GROUP BY a1.id "
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

		} catch (Exception $e) {
			$result=array();
		}
		$result[0]['aamount'] = 0;
		foreach($result as $k=>$v){
			$result[0]['aamount'] += $v['price']*$v['counts'];
			$result[$k]['plus'] = $v['price']*$v['counts'];
		}
		return $result;
	}
	
	public function enoughmoney($oid,$uid){
		$db = $this->_db;
		//查询订单佣金
		
		$sql = "SELECT price FROM `order` WHERE id=".$oid;
		$result = $this->_db->query($sql)->fetch();
		$yongjin = $result['price'];
		
		//查询用户余额
		
		$sql = "SELECT amount,stat FROM `customer` WHERE id=".$uid;
		$result = $this->_db->query($sql)->fetch();
		$yue = $result['amount'];
		$stat = $result['stat'];
		if($yue - $yongjin<0 || $stat != 1 ){
			return false;	
		}else{
			return true;
		}
		
	}
	
	public function buy($oid,$user){

		$db = $this->_db;
		
		//查询用户类型
		$sql = "SELECT ugroup from `customer` where id=".$user['uid'];
		$result = $this->_db->query($sql)->fetch();
		$ugroup = $result['ugroup'];
		if($ugroup == 0){
			return array('stat'=>false,'message'=>'农户不可以购买订单！');
		}
		
		//查询订单佣金
		$sql = "SELECT price,ordersn,cid FROM `order` WHERE id=".$oid;
		$result = $this->_db->query($sql)->fetch();
		$yongjin = $result['price'];
		$ordersn = $result['ordersn'];
		if($result['cid'] != 0){
			return array('stat'=>false,'message'=>'订单已被购买');
		}
		
		//查询用户余额
		$sql = "SELECT amount FROM `customer` WHERE id=".$user['uid']." and stat = 1 ";
		$result = $this->_db->query($sql)->fetch();
		$yue = $result['amount'];
		
		//查询卡号为100000的用户
		
		$sql = "SELECT a1.uid,a2.amount FROM `card` AS a1 LEFT JOIN `customer` AS a2 ON a1.uid = a2.id WHERE cardid=1000000000 or noid=1000000000";
		$result = $this->_db->query($sql)->fetch();
		$biguid = $result['uid'];
		$bigamount = $result['amount'];
		
// 		return false;
		//开启事务
		
		$db->beginTransaction();//开启事务
		
		if ($yongjin>0) {
			//修改订单余额，
			try {
				$db->update('customer',array('amount'=>($yue-$yongjin)),array('id = ?'=>$user['uid']));
				$db->update('customer',array('amount'=>($yongjin+$bigamount)),array('id = ?'=>$biguid));
					
			} catch (Exception $e) {
				$db->rollBack();
				return array('stat'=>false,'message'=>'未知错误');
			}
			//添加转账记录
			
			try {
				$data=array();
				$data['paycard'] = $user['noid'];
				$data['incomecard'] = 1000000000;
				$data['amount'] = $yongjin;
				$data['cdate'] = time();
				$data['ctype'] = 2;
				$data['uid'] = 0;
				$data['txt'] = '购买'.$ordersn.'订单支付'.$yongjin.'佣金';
				$db->insert('cardzz',$data);
				
				$zzid = $db->lastInsertId();
				$model = new Verificate_Model_Customer();
				$u = $model->getInfosByUid($user['uid'], array('amount','freezen'));
				$db->update('cardzz',
				array('paybalance'=>($u['amount']+$u['freezen'])),
				array('id = ?'=>$zzid));
				
				$u = $model->getInfosByUid($biguid, array('amount','freezen'));
				$db->update('cardzz',
				array('payeebalance'=>($u['amount']+$u['freezen'])),
				array('id = ?'=>$zzid));
				

			} catch (Exception $e) {
				$db->rollBack();
				return array('stat'=>false,'message'=>'未知错误');
			}
		}

		//修改订单表，订单所有者
		try{

			$db->update('order',array('cid'=>$user['uid']),array('id = ?'=>$oid));
		}catch( Exception $e){
			$db->rollBack();
			return array('stat'=>false,'message'=>'未知错误');
		}
		
		$db->commit();
		return array('stat'=>true,'message'=>'购买成功');
	}
}

?>