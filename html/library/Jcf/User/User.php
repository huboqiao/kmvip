<?php
class Jcf_User_User extends Jcf_Model_Dao implements Jcf_User_Interface
{
    public function authenticate($username,$cart)
    {
        $row = $this->_conn
                    ->select()
                    ->from('card')
                    ->where('cardid=?',$username)
                    ->where('stat=?',1)
                    ->limit(1)
                ->query()
                ->fetch();
         if(null == $row){
         	return null;
         	
         }else{
         	
         	$u = new Jcf_Models_User($row);
        	$u->setCart($cart);
        	return $u;
         }
    }

    public function getById($id)
    {
    }

    public function toggleStatus($id)
    {
    }
    public function add($user)
    {
    }
    public function update($user)
    {
    	
    }
    public function updatePassword($user)
    {
    }
    
    public function fid($offset = null, $count = null, $exp = null)
    {

    }

    public function count($exp)
    {
    }
    public function exist($checkFor,$value)
    {
    }
}

?>
