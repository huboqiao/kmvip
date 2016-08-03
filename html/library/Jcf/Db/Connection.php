<?php
class Jcf_Db_Connection
{
    /**
      *数据库工厂类
      *
      *根据当前配置文件访问相应的数据库类,并实例生成句柄
      */
    public static function factory()
    {

    	$config  = new Zend_Config_Ini(APPLICATION_PATH.'/configs/application.ini','production');
        $adapter = $config->resources->db->adapter;
        $adapter = str_replace(' ', '_', ucwords(str_replace('_', ' ', strtolower($adapter))));
        $class   = 'Jcf_Db_Connection_' . $adapter . '_Connection';
        if(!class_exists($class)){
            throw new exception('不能访问' . $adapter);
        }
        $instance = new $class($adapter);
        return $instance;

    }
    
    
    public static function selectdb($dbname){
		$config = new Zend_Config_Ini('./application/configs/application.ini','production');
		$params = array (
				 'host'     => $config->resources->db->params->host,
                 'username' => $config->resources->db->params->username,
                 'password' => $config->resources->db->params->password,
                 'dbname' =>$dbname
                 );
               
        try{

			$db = Zend_Db::factory('PDO_MYSQL', $params);	
			$db->query("SET NAMES 'utf8'");
			return $db;
		
        }catch(Exception $e){
        	return false;
        } 
    }
}
?>

