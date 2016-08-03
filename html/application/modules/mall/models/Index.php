<?php 
class Mall_Model_Index extends Zend_Db_Table{
	
	protected $_name="ecs_category";
	public $modelname = '商城模块';
	
	public function getAllCategory(){
		
		$sql = "select * from ecs_category where parent_id = 0" ;
		try {
			
			$result = $this->_db->query($sql)->fetchAll();
		} catch (Exception $e) {
			$result=array();
		}
		return $result;
		
	}
	
	
	
	public function getgoodslist($cartgoods,$wheres='',$order='',$numPerPage=0,$offset=0){
		
		$order='  ';
		$limit = '';
		if ($numPerPage>0) {
			$limit = ' limit '.$offset.','.$numPerPage.' ';
		}
		//order by cdate desc
		
		$goodslist = array_keys($cartgoods);
		$sql = "select g.*,c.cat_name from `ecs_goods` as g ".
				"left join `ecs_category` as c on c.cat_id = g.cat_id ".
				"where g.goods_id in (".implode($goodslist,",").")"
				." ".$wheres
				.$order.$limit;
		try {
			
			$result = $this->_db->query($sql)->fetchAll();
			foreach($result as $i=>$v){
				foreach($cartgoods as $j=>$k){
					if($v['goods_id'] == $j){
						$result[$i]["cart_number"] = $k;
					}
				}
			}
		} catch (Exception $e) {
			$result=array();
		}
		 return $result;
	}
	
	public function addorderbygoods($user,$goods){
		
		$db = $this->_db;
			
		$db->beginTransaction();//开启事务
		
		try {
		//添加商城订单记录
			$data=array();
			$data['order_sn'] = "OD_".time();
			$data['noid'] = $user["noid"];
			$data['order_status'] = 0;
			$data['pay_status'] = 0;
			$data['add_time'] = time();
			$data['pay_time'] = 0;
			$db->insert('ecs_order_info',$data);
			$orderid = $db->lastInsertId();
			//添加订单详情
			
			$data=array();
			$data['order_id'] = $orderid;
			$data['goods_id'] = $goods['goods_id'];
			$data['goods_number'] = $goods['goods_number'];
			$data['goods_price'] = 0;
			$db->insert('ecs_order_goods',$data);
				
		} catch (Exception $e) {
			$db->rollBack();
			return false;
		}
		
			$db->commit();
			return $orderid;
	}
	
	public function addorderbycart($user){
		
		$db = $this->_db;
			
		$db->beginTransaction();//开启事务
		
		try {
		//添加商城订单记录
			$data=array();
			$data['order_sn'] = "OD_".time();
			$data['noid'] = $user["noid"];
			$data['order_status'] = 0;
			$data['pay_status'] = 0;
			$data['add_time'] = time();
			$data['pay_time'] = 0;
			$db->insert('ecs_order_info',$data);
			$orderid = $db->lastInsertId();
		//添加订单详情
			foreach($user["cart"] as $i=>$v){
				$data=array();
				$data['order_id'] = $orderid;
				$data['goods_id'] = $i;
				$data['goods_number'] = $v;
				$data['goods_price'] = 0;
				$db->insert('ecs_order_goods',$data);
				
			}
			
		} catch (Exception $e) {
			$db->rollBack();
			return false;
		}
		
			$db->commit();
			return $orderid;
		
		
	}
	
	public function queryorderList($noid,$wheres='',$order='',$numPerPage=0,$offset=0){
		$order='  ';
		$limit = '';
		if ($numPerPage>0) {
			$limit = ' limit '.$offset.','.$numPerPage.' ';
		}
		//order by cdate desc
		
		
			
		try {
			$sql = "SELECT o.* ".
				"from `ecs_order_info` as o ".
				" WHERE o.noid = ".$noid.
				" ".$wheres.
			$order.$limit;
			$result = $this->_db->query($sql)->fetchAll();
			$orderstat = array("未完成","完成","取消");
			$paystat = array("未支付","已支付");
			foreach($result as $i=>$v){
				$result[$i]['order_status']= $orderstat[$v['order_status']];
				$result[$i]['pay_status']= $paystat[$v['pay_status']];
				if($v["pay_status"] == 1){
					$sql = "select sum(og.goods_number * og.goods_price) as amount ".
							"from `ecs_order_goods` as og ".
							"where og.order_id = ".$v["id"];
					
					$tmp = $this->_db->query($sql)->fetch();
					$result[$i]['amount'] = $tmp['amount'];
				}else{
					$sql = "select sum(og.goods_number * g.goods_price) as amount ".
							"from `ecs_order_goods` as og ".
							"left join `ecs_goods` as g on og.goods_id = g.goods_id ".
							"where og.order_id = ".$v["id"];
					
					$tmp = $this->_db->query($sql)->fetch();
					$result[$i]['amount'] = $tmp['amount'];
				}
				
			}
		} catch (Exception $e) {
			$result=array();
		}
		return $result;
	}
	
	
	
	
	public function queryInfo($wheres='',$order='',$numPerPage=0,$offset=0){
		$order='  ';
		$limit = '';
		if ($numPerPage>0) {
			$limit = ' limit '.$offset.','.$numPerPage.' ';
		}
		//order by cdate desc
		
		$sql = "SELECT a1.goods_id,a1.goods_name,a1.goods_number,a1.goods_price,a1.unit "
			." FROM `ecs_goods` AS a1 "
			." WHERE a1.is_active = 0 "
			." ".$wheres
			.$order.$limit;
			
		try {
			
			$result = $this->_db->query($sql)->fetchAll();
		} catch (Exception $e) {
			$result=array();
		}
		return $result;
	}	
	
	//查询订单编码
	public function getGoodsinfo($goods_id){
		$sql = "select g.*,c.cat_name from `ecs_goods` as g ".
				"left join `ecs_category` as c on g.cat_id = c.cat_id ".
				"where g.goods_id = ".$goods_id;
				$result = $this->_db->query($sql)->fetch();
				return $result;
	}
	
	
	public function enoughmoney($oid,$uid){
		$db = $this->_db;
		
		//查询订单佣金
		
		$sql = "SELECT sum(og.goods_number * g.goods_price) as price FROM `ecs_order_goods` as og ".
				" left join `ecs_goods` as g on og.goods_id = g.goods_id ".
				"WHERE order_id=".$oid;
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
	
	public function allmoney($oid){
		$db = $this->_db;
		
		//查询订单佣金
		
		$sql = "SELECT sum(og.goods_number * g.goods_price) as price ".
				"FROM `ecs_order_goods` as og ".
				" left join `ecs_goods` as g on og.goods_id = g.goods_id ".
				"WHERE order_id=".$oid;
		$result = $this->_db->query($sql)->fetch();
		
		$sql = "select og.goods_id,g.goods_price,(g.goods_number-og.goods_number) as gnumber ".
				"FROM `ecs_order_goods` as og ".
				" left join `ecs_goods` as g on og.goods_id = g.goods_id ".
				" WHERE order_id=".$oid;
		$result2 = $this->_db->query($sql)->fetchAll();
		return array("price"=>$result['price'],"goods"=>$result2);
	}

	public function orderInfo($orderid){
		$sql = "select * from `ecs_order_info` where id = ".$orderid;
		$result = $this->_db->query($sql)->fetch();
		if($result["pay_status"] == 1){
			$sql="select og.goods_id,og.goods_number as cart_number,og.goods_price,g.goods_number,g.goods_name,c.cat_name ".
			" from `ecs_order_goods` as og ".
			" left join `ecs_goods` as g on og.goods_id = g.goods_id ".
			" left join `ecs_category` as c on g.cat_id = c.cat_id ".
			" where og.order_id = ".$orderid;
			
		}else{
			$sql="select og.goods_id,og.goods_number as cart_number,g.goods_price,g.goods_number,g.goods_name,c.cat_name ".
			" from `ecs_order_goods` as og ".
			" left join `ecs_goods` as g on og.goods_id = g.goods_id ".
			" left join `ecs_category` as c on g.cat_id = c.cat_id ".
			" where og.order_id = ".$orderid;	
		}
		$goods = $this->_db->query($sql)->fetchAll();
		$result["goods"] = $goods;
//		$result["add_time"] = intval($result["add_time"]/100);
//		$result["pay_time"] = intval($result["pay_time"]/100);
		return $result;
		
		
	}
	
	public function delordergoods($order_id,$goods_id){
		$sql = "delete from `ecs_order_goods` where order_id = ".$order_id.
				" and goods_id = ".$goods_id;
		$rowcount = $this->_db->query($sql)->rowCount();
		if($rowcount > 0 ){
			return true;
		}else{
			return false;
		}
	}
	
	public function queryOdersn($order_id){
		$sql = "select order_sn from `ecs_order_info` where id=".$order_id;
		$order = $this->_db->query($sql)->fetch();
		return $order['order_sn'];
		
	}
	
	public function updateordergoods($goods_id,$goods_number,$order_id){
		
		$db = $this->_db;
		$db->update('ecs_order_goods',
			array('goods_number'=>$goods_number),
			array('order_id = ?'=>$order_id,'goods_id = ?'=>$goods_id));
				
		
	}
	
	public function enoughstore($oid){
		
		$db = $this->_db;
		
		$sql = "select (g.goods_number - og.goods_number) as shengyu,g.goods_name ".
				"from `ecs_order_goods` as og ".
				"left join `ecs_goods` as g on g.goods_id = og.goods_id ".
				"where og.order_id = ".$oid;
				
		$goods = $this->_db->query($sql)->fetchAll();
		foreach($goods as $i=>$v){
			if($i["shengyu"] < 0 ){
				return array("stat"=>false,"msg"=>$i["goods_name"]."库存不足");
			}
		}
		
		return array("stat"=>true,"msg"=>"库存足够！");
			
	}
	
	public function buy($oid,$user){
		
		//查询余额
		if(!$this->enoughmoney($oid,$user["uid"])){
			return array('stat'=>false,'message'=>'金额不足！');
		}
		
		//查询库存是否足够
		$info = $this->enoughstore($oid);
		if(!$info["stat"]){
			return array('stat'=>false,'message'=>$info["msg"]);
		}
		
		$db = $this->_db;
		//查询用户类型
		$sql = "SELECT ugroup from `customer` where id=".$user['uid'];
		$result = $this->_db->query($sql)->fetch();
		$ugroup = $result['ugroup'];
		if($ugroup == 0){
			return array('stat'=>false,'message'=>'农户不可以购买订单！');
		}
		//查询订单佣金
		$sql = "SELECT pay_status,order_sn FROM `ecs_order_info` WHERE id=".$oid;
		$res = $this->_db->query($sql)->fetch();
		$ordersn = $res["order_sn"];
		if($res['pay_status'] == 1){
			return array('stat'=>false,'message'=>'订单已支付');
		}
		$resultt  = $this->allmoney($oid);
		$yongjin = $resultt['price'];
		$goods = $resultt['goods'];
		
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
			//修改用户余额，
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
				$data['txt'] = '购买商城订单'.$ordersn.'支付'.$yongjin.'元';
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
				return array('stat'=>false,'message'=>'未知trrr错误');
			}
		}
		
		//修改订单状态
		try{
		$db->update('ecs_order_info',
			array('order_status'=>1,'pay_status'=>1,'pay_time'=>time()),
			array('id = ?'=>$oid));
		}catch( Exception $e){
			$db->rollBack();
			return array('stat'=>false,'message'=>'未知11错误');
		}
		
		
		try{
			foreach($goods as $i=>$v){
				//修改订单商品价格
				$db->update('ecs_order_goods',
					array('goods_price'=>$v['goods_price']),
					array('goods_id = ?'=>$v['goods_id'],'order_id = ?'=>$oid));
				//修改库存
				
				$db->update('ecs_goods',
					array('goods_number'=>$v['gnumber']),
					array('goods_id = ?'=>$v['goods_id']));
			}
		}catch( Exception $e){
			$db->rollBack();
			return array('stat'=>false,'message'=>'未知错误');
		}
		
		$db->commit();
		return array('stat'=>true,'message'=>'购买成功');
	}
}

?>