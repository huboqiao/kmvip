<?php
/**
*数据公用抽像类
*该抽像类主要是用于对单表数据处理的的公共操作，如果需对单表进行相应的操作，需要继承该类
*并且按自己的要求实现他给出的方法
**/
abstract class Jcf_Db_Abstract extends Zend_Db_Table_Abstract implements Jcf_Db_Interface{
    public $row;
    public $selects;
	public $inserts;

	Abstract function  aaa(){
		$s = '123';
		$d = 'sss';
	}
	
	
    public function Getdata($where=null,$order='',$limit=array(),$group=''){
        $this->selects = $this->select();
	   if(is_numeric($where)) $this->row = $this->find($where);
	   
        if($order) $this->selects->order($order);
        if(is_array($limit) && count($limit) > 0 ){
            $this->selects->limit($limit[0],$limit[1]);
        }else{
            $this->selects->limit($limit);
        }
		if($group) $this->selects->group($group);
		if(is_array($where)){

            foreach($where as $key=>$val){
            	if($val!=''){
                	$this->selects->where($key.'='.$val);
            	}
            }
        //echo $this->selects->__toString();exit;
        //echo $this->selects;exit;
            $this->row = $this->fetchAll($this->selects);
		//print_r($this->row);exit;
            return $this->row;
        }
        //echo $this->selects->__toString();exit;
        $this->row = $this->fetchAll($this->selects);
		//print_r($this->row);exit;
        return $this->row;
    }
    public function Updatedata($set=array(),$where){
        $update = $this->update($set,$where);
        return $update;
    }

    public function DelData($where=array()){
        $del = $this->delete($where);
        return $del;
    }

    public function InsertData($data){
	//print_r($data);exit;
		$r = $this->insert($data);
        return $r;
    }
	
	public function all($db,$where=''){
        $this->_db = $this->getAdapter();
        $sql = "select * from ".$db." ".$where;
		//echo $sql;exit;
        $result = $this->_db->query($sql);
        $result = $result->fetchAll();
        return $result;
    }
	
	public function group($term='*',$db='',$group){
		$this->_db=$this->getAdapter();
		$sql= "select ".$term." from ".$db.$group;
		//echo $sql;exit;
		$result = $this->_db->query($sql);
        $result = $result->fetchALl();
        return $result;
	}
	
	public function add($db,$term,$data){
		$this->_db=$this->getAdapter();
		$sql= "insert into ".$db." (".$term.") values (".$data.")";
		//echo $sql;exit;
		$result = $this->_db->query($sql);
        return $result;
	}
	
	public function query($table,$set,$where){
		$this->_db=$this->getAdapter();
		$sql= "update ".$table." ".$set.$where;
		//echo $sql;exit;
		$result = $this->_db->query($sql);
        return $result;
	}

	public function DeleteData($db,$where){
	try 
	{ 
		$this->_db=$this->getAdapter();
		$sql= "delete from ".$db." ".$where;
		//echo $sql;exit;
		$result = $this->_db->query($sql);
        return $result;
	} 
	catch(Exception $e) 
	{ 
		print $e->getMessage();
	}
	}
	
	public function tx($table,$where){
		$this->_db=$this->getAdapter();
		$sql= "update ".$table." set tx=1 ".$where;
		//echo $sql;exit;
		$result = $this->_db->query($sql);
        return $result;
	}
	
	public function getlastid(){
		return $this->_db->lastInsertId();
	}
	public function existsDatabase($where)
	{
		$this->_db=$this->getAdapter();
		$sql = "SELECT SCHEMA_NAME FROM information_schema.SCHEMATA where SCHEMA_NAME ='".$where."'";
		$result = $this->_db->query($sql);
		$result =$result->fetchAll();
        return $result;
	}
}
