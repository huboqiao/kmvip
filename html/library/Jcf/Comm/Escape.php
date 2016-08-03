<?php
/**
 +------------------------------------------------
 * 通用防sql注入转义类
 +------------------------------------------------
 */
class Jcf_Comm_Escape{
	private $obj;
	
	public function jcf_Escape($obj){
		$this->obj = $obj;
		if(is_array($this->obj)){
			return $this->getArray();
		}
		if(is_object($obj)){
			return $this->getObject();
		}
		if(is_string($obj)){
			return $this->getStr();
		}
	}
	/**
	 *在添加数据库之前进行转义
	 * $array是一个数组
	 * return:
	 * 转义后的数组
	 */
	
	private function getArray(){
		$array = array();
		foreach ($this->obj as $key=>$val){
			$array[$key]=htmlspecialchars($val);
		}
		return $array;
	}
	
	private function getObject(){
	
	}
	
	/**
	 * 在添加数据库之前进行转义
	 * $array是一个字符串
	 * return:
	 * 转义后的数组
	 */
	private function getStr(){
		if(!is_array($array)){
			return $array=htmlspecialchars($array);
		}
	}
}