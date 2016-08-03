<?php 
/**
 * 日志操作
 */
class Jcf_Log_Log extends Jcf_Db_Abstract
{
    protected $_name = 'log';
    protected $_primary = 'id';
    protected $_db;
	public function insertlog($doit,$level) {
        if (isset($_SERVER['HTTP_CLIENT_IP']) && $_SERVER['HTTP_CLIENT_IP']!='unknown') {
            $ip = $_SERVER['HTTP_CLIENT_IP'];
        } elseif (isset($_SERVER['HTTP_X_FORWARDED_FOR']) && $_SERVER['HTTP_X_FORWARDED_FOR']!='unknown') {
            $ip = $_SERVER['HTTP_X_FORWARDED_FOR'];
        } else {
            $ip = $_SERVER['REMOTE_ADDR'];
        }
		$user = Zend_Auth::getInstance()->getIdentity()->getProperties();
		$uid=$user['uid'];
		$date=time();
		$data=array(
					'uid'=>$uid,
					'cdate'=>$date,
					'act'=>$doit,
					'level'=>$level
		);
		$insert=$this->InsertData($data);
    }
    
	public function sqlQuery($where){
    }
    
    public function selectlog($where){
        $this->_db = $this->getAdapter();
        $sql = 'select * from '.$this->_name.$where;
        $result = $this->_db->query($sql);
        $result = $result->fetchALl();
        return $result;
    }
}
