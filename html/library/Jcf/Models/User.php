<?php
class Jcf_Models_User extends Jcf_Model_Entity
{
    protected $_properties = array(
            'id'   =>    null,
            'cardid'     =>    null,
            'cdate'  =>    null,
            'bdate'  =>    null,
            'password'   =>    null,
            'uid'  =>    null,
            'noid'   =>    null,
            'stat' =>    null,
            'cart' => array()
    );
    
    public function setCart($cart){
    	$this->_properties['cart'] = $cart;
    }
}
?>
