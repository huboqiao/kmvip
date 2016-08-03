<?php
interface Jcf_User_Interface
{
    public function authenticate($username,$password);

    public function getById($id);
    
    /**
     * ToggleStatus 获取用户账号是否激活
     *
     * @param ini $id 用户id
     * @return int
     */
    public function toggleStatus($id);
    
    /**
     * 添加用户
     *
     * @param Jcf_User  $user
     * @return int
     */
    public function add($user);

    public function update($user);

    public function updatePassword($user);

    public function fid($offset = null, $count = null, $exp = null);

    public function count($exp);

    public function exist($checkFor,$value);
}

?>
