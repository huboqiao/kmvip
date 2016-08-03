<?php
/**
 * 递归排序类
 * 
 * @author kylin 2014-4-19
 *
 */

class Jcf_Sort_Sort
{
		public $pkey = '';
		public $nkey = '';
		
		/**
		 * 初始化递归条件
		 * 
		 * @param string $pkey	依赖字段
		 * @param string $nkey	递归替换字段
		 * 
		 * @return class	
		 */
		public function conf($pkey='',$nkey=''){
			$this->pkey=$pkey;
			$this->nkey=$nkey;
			return $this;
		}
		
		/**
		 * 递归重新排列该数组
		 * 
		 * @param unknown	$arr	待处理数组
		 * @param number	$p_id	依赖字段值
		 * @param number 	$level	递归深度
		 * 
		 * @return array	$res	返回数组
		 */
		public function resort($arr,$p_id = 0,$level = 0){
			$res = array();
			foreach($arr as $k=>$v){
				if($v[$this->pkey] == $p_id){
					$v['level'] = $level;
					$res[]=$v;
					unset($arr[$k]);
					$res = array_merge($res,self::resort($arr,$v[$this->nkey],$level+1));
				}
			}
			return $res;
		}
}

?>
