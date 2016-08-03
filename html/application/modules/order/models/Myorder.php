<?php 
class Order_Model_Myorder extends Zend_Db_Table{
	
	protected $_name="order";
	public $modelname = '订单模块';
	
	public function queryInfo($uid,$wheres='',$order='',$numPerPage=0,$offset=0){
		$arr = array('关闭','未入库','已入库','发货中','完成');
		$pstat = array('指派','竞价');
		$order=' order by cdate desc ';
		$limit = '';
		if ($numPerPage>0) {
			$limit = ' limit '.$offset.','.$numPerPage.' ';
		}
		//order by cdate desc
		
		$sql = "SELECT a1.* ,sum(a2.price*a2.counts) as amount"
				." FROM `order` AS a1 "
				." LEFT JOIN `order_info` as a2 ON a1.id = a2.orderid"
				." WHERE a1.cid = ".$uid
				." ".$wheres
				." GROUP BY a1.id "
				.$order.$limit;
		try {
		
			$result = $this->_db->query($sql)->fetchAll();
		} catch (Exception $e) {
			$result=array();
		}
		foreach($result as $k => $v){
			$result[$k]['color'] = "white";
			$cstat=array('red','yellow','green');
			if($v['pstat'] == 0){
				if ($v['cstat'] == 0) {
					$result[$k]['color'] = 'red';
				}else{
					$result[$k]['color'] = 'yellow';
				}
				if ($v['ostat'] == 2 ||$v['ostat'] == 3) {

					$result[$k]['color'] = 'blue';
				}
				if ($v['ostat'] == 4) {

					$result[$k]['color'] = 'green';
				}
			}
			
			$result[$k]['pstat'] = $pstat[$v['pstat']];
			if($v['cstat']==0 && $v['pstat'] == 0){

				$result[$k]['ostat'] = '未接受';
			}else{

				$result[$k]['ostat'] = $arr[$v['ostat']];
			}
		}
		return $result;
	}
	
	//查询订单编码
	public function queryOdersn($oid){
		$result = $this->fetchRow(array('id=?'=>$oid))->toArray();
		return $result['ordersn'];
	}
	

	public function enoughmoney($oid,$uid){
		$db = $this->_db;
		//查询订单佣金
	
		$sql = "SELECT price FROM `order` WHERE id=".$oid;
		$result = $this->_db->query($sql)->fetch();
		$yongjin = $result['price'];
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
	
	public function queryGoods($oid,$wheres='',$order='',$numPerPage=0,$offset=0){
		$arr = array('关闭','未入库','已入库','发货中','完成');
		$order='  ';
		$limit = '';
		if ($numPerPage>0) {
			$limit = ' limit '.$offset.','.$numPerPage.' ';
		}
		
		//查询订单表，订单详情表和商品表
		$sql = "SELECT a1.id,a1.ordersn,a1.price as amount,a1.cdate,a1.ostat,a1.pstat,a1.cstat,"
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
			$result[$k]['ostat'] = $arr[$v['ostat']];
			$result[$k]['plus'] = $v['price']*$v['counts'];
		}
		return $result;
	}
	
	public function accept($oid,$user){

		$db = $this->_db;
		//查询订单佣金
		
		$sql = "SELECT price,ordersn FROM `order` WHERE id=".$oid;
		$result = $this->_db->query($sql)->fetch();
		$yongjin = $result['price'];
		$ordersn = $result['ordersn'];
		
		//查询用户余额
		$sql = "SELECT amount FROM `customer` WHERE id=".$user['uid']." and stat = 1 ";
		$result = $this->_db->query($sql)->fetch();
		$yue = $result['amount'];
		
		//查询卡号为0的用户
		
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
				return false;
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
				$data['txt'] = '接受'.$ordersn.'订单支付'.$yongjin.'佣金';
				$db->insert('cardzz',$data);
								
				$zzid = $db->lastInsertId();
				$model = new Verificate_Model_Customer();
				$user = $model->getInfosByUid($user['uid'], array('amount','freezen'));
				$db->update('cardzz',
				array('paybalance'=>($user['amount']+$user['freezen'])),
				array('id = ?'=>$zzid));
				
				$user = $model->getInfosByUid($biguid, array('amount','freezen'));
				$db->update('cardzz',
				array('payeebalance'=>($user['amount']+$user['freezen'])),
				array('id = ?'=>$zzid));

			} catch (Exception $e) {
				$db->rollBack();
				return false;
			}
		}

		//修改订单表，订单所有者
		try{

			$db->update('order',array('cstat'=>1),array('id = ?'=>$oid));
		}catch( Exception $e){
			$db->rollBack();
			return false;
		}
		
		$db->commit();
		return true;
	}
}

?>