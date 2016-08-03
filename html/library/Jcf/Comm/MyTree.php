<?php
/**
 +------------------------------------------------
 * 通用的树型类
 +------------------------------------------------
 */
class Jcf_Comm_MyTree
{
 
	public $array = array();
	private $html = '';
	public $arr = array();
	function __construct($array)
	{
		$this->array = $array;
		$this->arr = $this->getArray();
	}

	function getChild($id){
		$childs = array();
		foreach($this->array as $k => $v){
			if($v['parentid'] == $id){
				$childs[] = $v;
			}
		}
		return $childs;
	}

	function getArray($id=0){
		$childs = $this->getChild($id);
		if(empty($childs)){
			return null;
		}
		foreach($childs as $k => $v){
			$result = $this->getArray($v['id']);
			if(null != $result){
				$childs[$k]['children'] = $result;
			}
		}
		return $childs;
	}

	function getUl($id=0){
		foreach($childs as $k => $v){
		}
	}

	function getLi($array){
		foreach($array as $k => $v){
		
		}
	}
}

?>
