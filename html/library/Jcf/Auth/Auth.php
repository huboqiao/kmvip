<?php
class Jcf_Auth_Auth implements Zend_Auth_Adapter_Interface
{
    const SUCCESS = 1;
    const NOT_ACTIVE = -1;
    const FAILURE = -2;

    private $_username;
    private $_password;

    public function __construct($username,$cart)
    {
        $this->_username = $username;
        $this->_cart = $cart;
    }

    public function authenticate()
    {
        $password = ($this->_password);
        $conn = Jcf_Db_Connection::factory()->getConnection();
        $u = new Jcf_User_User();
        $u->setDbConnection($conn);

        $user = $u->authenticate($this->_username,$this->_cart);
        if(null == $user){
            return new Zend_Auth_Result(self::FAILURE,null);
        }

        if($user->stat == 0){
			//$auth = Zend_Auth::getInstance();
			//$auth->authenticate($user);
            return new Zend_Auth_Result(self::NOT_ACTIVE,null);
        }
        return new Zend_Auth_Result(self::SUCCESS,$user);
    }

}
?>
