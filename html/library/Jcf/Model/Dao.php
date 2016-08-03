<?
abstract class Jcf_Model_Dao{
    protected $_conn;

    public function __construct($conn = null)
    {
        if($conn != null){
            $this->setDbConnection($conn);
        }
    }

    public function setDbConnection($conn)
    {
        $this->_conn = $conn;
        return $this;
    }

    public function getDbConnection(){
        return $this->_conn;
    }
}
?>
