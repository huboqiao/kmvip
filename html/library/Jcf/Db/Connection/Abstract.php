<?php
abstract class Jcf_Db_Connection_Abstract
{
    const KEY        = 'Jcf_Db_Connection_Abstract_KEY';
    const PREFIX_KEY = 'Jcf_Db_Connection_Abstract_TablePrefix';
    const DEFAULT_PREFIX = '';
    protected $_adapter;

    public function __construct($adapter)
    {
        $this->_adapter = $adapter;
    }

    public function getAdapter()
    {
        return $this->_adapter;
    }

    public function getConnection()
    {
        return $this->_setConnection();
    }
    

    protected function _setConnection()
    {
        $config = new Zend_Config_Ini(APPLICATION_PATH.'/configs/application.ini','production');
        $db = $config->resources->db->params;
        return $this->_connect($db);
    }

    protected abstract function _connect($config);

    public abstract function query($sql);

}
?>
