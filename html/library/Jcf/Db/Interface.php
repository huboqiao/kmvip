<?php
/**
*数据公用接口
**/
interface Jcf_Db_Interface {
    
    /**
    *获取数据
    *@where     array       该条件可以为int,array,当为int就会只查询以当然primary的一条数据;
    *@order     string      按指定字段排序
    *@limit     array       分页字段
    *@group     string      分组
    *@return    dbrow       数据集
    **/
    public function Getdata($where=null,$order='',$limit=array(),$group='');
    
    /**    
    *更新
    *@set       array
    *@where     array 
    *@return    void
    **/
    public function Updatedata($set=array(),$where);

    /**
    *删除
    *@where     array
    *@return    void
    **/
    public function DelData($where=array());

    /**
    *插入
    *@data      array
    *@return    void
    **/
    public function InsertData($data);
	
    
}

