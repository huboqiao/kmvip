<?php
class Jcf_Db_Connection_Pdo_Mysql_Connection extends Jcf_Db_Connection_Abstract
{
    protected function _connect($config){
        $db = Zend_Db::factory('Pdo_Mysql',$config);
        $db->setFetchMode(Zend_Db::FETCH_OBJ);
        $db->query('SET CHARACTER SET "utf8"');
        return $db;
    }
    

    public function query($sql)
    {
        $conn = $this->getConnection();
        $conn->query($sql);
    }
}
?>
