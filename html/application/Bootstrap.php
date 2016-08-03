<?php
class Bootstrap extends Zend_Application_Bootstrap_Bootstrap {

    
    protected function _initPlugin(){
        $front = Zend_Controller_Front::getInstance();
        $front->registerPlugin(new Jcf_Controller_Plugin_Login());
		Zend_Session::start();

    }
    
}