<?php
header("Content-type: text/html; charset=utf-8");
/**
 * 
 * 功能：整站权控制类
 * 
 * 
 * auth :huboqiao at 2013-05-31
 * 
 */
class Jcf_Acl_Acl extends Zend_Acl{
	function __construct(){
		$this->acl = new Zend_Acl();
		$this->role = new Sys_Model_Group;
		$this->resources = new Sys_Model_Resource;
		$this->setRole();
		$this->setResource();
		$this->setPower();
	}
	
	/**
	 * 功能说明：检测用户是否有权限进行本次操作
	 * 参数说明：
	 * 	$role：用户所在组，
	 * 	$cont：控制器名，
	 * 	$action：用户要进行的动作，
	 * 	$module：对那个模块进行操作
	 * 还回值：
	 * 	1：表示您没有执行该命令的权限
	 *	2：表示您访问的地址不在权限范围内
	 */
	function check($role,$cont,$action,$module){
		if(!($cont=="index"&&$action=="index"&&$module=="admin")&&!($cont=="index"&&$action=="loginout"&&$module=="login")&&!($cont=="systemwin"&&$action=="index"&&$module=="admin")){
			if($this->acl->has(new Zend_Acl_Resource($module.':'.$cont.':'.$action))){
				if($this->acl->isAllowed($role, $module.':'.$cont.':'.$action,$action)){
					echo '';
				}else{
					return 1;
				}
			}else{
				return 2;
			}
		}
	}
	//注册角色
	function setRole(){
		$where = '1 =1';
		$this->roledata = $this->role->fetchAll($where)->toArray();
		foreach($this->roledata as $key=>$val){
			$this->acl->addRole(new Zend_Acl_Role($val['id']));
		}
		
	}
	//注册资源
	function setResource(){
		$where = '1=1';
		$this->resdata = $this->resources->fetchAll($where)->toArray();	
		foreach($this->resdata as $key=>$val){
			if($val['controller'] != '' && $val['action'] != ''){
				$re=$this->acl-> add(new Zend_Acl_Resource($val['module'].':'.$val['controller'].':'.$val['action']));	
			}
			//强制添加提交、修改权限
			//提交：isupdate
			//修改：isname
			//$this->acl->add(new Zend_Acl_Resource($val['controller'].':isupdate'));	
			//$this->acl->add(new Zend_Acl_Resource($val['controller'].':isname'));	
			
		}
	}
	//注册权限
	function setPower(){
		//获取角色与资源的关联信息
		//setup one :获取角色的权限表
		foreach($this->roledata as $val){
			#echo $val['role_list'].'</br>';
			$resource = explode(';',$val['role_list']);
			foreach($resource as $key=>$val2){
				#echo $val2.'</br>';
				//setup tow:根据角色的权限ID去查找资源
				if($val2 != ''){
					$where = 'id = '.$val2;
					$res = $this->resources->fetchAll($where)->toArray();	
					foreach($res as $v1){
						if($v1['controller'] != '' && $v1['action'] != ''){
							$this->acl->allow($val['id'],$v1['module'].':'.$v1['controller'].':'.$v1['action'],$v1['action']);
						}
						//$this->acl->allow($val['role_id'],$v1['controller'].':isupdate','isupdate');
						//$this->acl->allow($val['role_id'],$v1['controller'].':isname','isname');
					}
					
				}else{
					
				}
			}
		}
	}
}    
?>
