<?php

class Jcf_Dump_Dump
{
    var $max_size  = 2097152; // 2M
    var $is_short  = false;
    var $offset    = 300;
    var $dump_sql  = '';
    var $sql_num   = 0;
    var $error_msg = '';

    var $db;

    /**
     *  类的构造函数
     *
     * @access  public
     * @param
     *
     * @return void
     */
    function cls_sql_dump($max_size=0)
    {
        //$this->db = &$db;//连接数据库
        
        if ($max_size > 0 )
        {
            $this->max_size = $max_size;
        }

    }
    /**
     * 
     */
    function escape_str($str){
    	return mysql_escape_string($str);
    	//return mysql_real_escape_string($str,$this->db);
    	//return $this->db->_connection->real_escape_string($str);
    	//$newobj = mysqli_init();
    	//return $newobj->real_escape_string($str);
    }
    
    /**
     * 对mysql记录中的null值进行处理
     *
     * @access  public
     * @param   string      $str
     *
     * @return string
     */
    static function dump_null_string($str)
    {
    	if (!isset($str) || is_null($str))
    	{
    		$str = 'NULL';
    	}
    
    	return $str;
    }

    /**
     *  类的构造函数
     *
     * @access  public
     * @param
     *
     * @return void
     */
    function __construct($max_size =0)
    {
    	//连接数据库
        $this->cls_sql_dump($max_size);
    }

    /**
     *  获取指定表的定义
     *
     * @access  public
     * @param   string      $table      数据表名
     * @param   boolen      $add_drop   是否加入drop table
     *
     * @return  string      $sql
     */
    function get_table_df($table, $add_drop = false)
    {
        if ($add_drop)
        {
            $table_df = "DROP TABLE IF EXISTS `$table`;\r\n";
        }
        else
        {
            $table_df = '';
        }

        $tmp_arr = $this->db->fetchAll("SHOW CREATE TABLE `$table`");
        $tmp_sql = $tmp_arr[0]['Create Table'];
        $tmp_sql = substr($tmp_sql, 0, strrpos($tmp_sql, ")") + 1); //去除行尾定义。
       
        $table_df .= $tmp_sql . " ENGINE=MyISAM DEFAULT CHARSET=utf8;\r\n";
       
       

        return $table_df;
    }

    /**
     *  获取指定表的数据定义
     *
     * @access  public
     * @param   string      $table      表名
     * @param   int         $pos        备份开始位置
     *
     * @return  int         $post_pos   记录位置
     */
    function get_table_data($table, $pos)
    {
        $post_pos = $pos;

        /* 获取数据表记录总数 */
       $total = $this->db->fetchOne("SELECT COUNT(*) FROM `$table`");
       

        if ($total == 0 || $pos >= $total)
        {
            /* 无须处理 */
            return -1;
        }

        /* 确定循环次数 */
        $cycle_time = ceil(($total-$pos) / $this->offset); //每次取offset条数。需要取的次数

        /* 循环查数据表 */
        for($i = 0; $i<$cycle_time; $i++)
        {
            /* 获取数据库数据 */
            $data = $this->db->fetchAll("SELECT * FROM $table LIMIT " . ($this->offset * $i + $pos) . ', ' . $this->offset);
            $data_count = count($data);
            $fields = array_keys($data[0]);
            $start_sql = "INSERT INTO `$table` ( `" . implode("`, `", $fields) . "` ) VALUES ";
			
            /* 循环将数据写入 */
            for($j=0; $j< $data_count; $j++)
            {
//             	foreach($data[$j] as $v){
//             		//过滤非法字符
//             		$record[] = $this->escape_str($v);
//             	}
                $record = array_map(array("Jcf_Dump_Dump","escape_str"), $data[$j]);   //过滤非法字符
                $record = array_map(array("Jcf_Dump_Dump","dump_null_string"), $record);     //处理null值

                
                /* 检查是否能写入，能则写入 */
                if ($this->is_short)
                {
                    if ($post_pos == $total-1)
                    {
                        $tmp_dump_sql = " ( '" . implode("', '" , $record) . "' );\r\n";
                    }
                    else
                    {
                        if ($j == $data_count - 1)
                        {
                            $tmp_dump_sql = " ( '" . implode("', '" , $record) . "' );\r\n";
                        }
                        else
                        {
                            $tmp_dump_sql = " ( '" . implode("', '" , $record) . "' ),\r\n";
                        }
                    }

                    if ($post_pos == $pos)
                    {
                        /* 第一次插入数据 */
                        $tmp_dump_sql = $start_sql . "\r\n" . $tmp_dump_sql;
                    }
                    else
                    {
                        if ($j == 0)
                        {
                            $tmp_dump_sql = $start_sql . "\r\n" . $tmp_dump_sql;
                        }
                    }
                }
                else
                {
                    $tmp_dump_sql = $start_sql . " ('" . implode("', '" , $record) . "');\r\n";
                    
                }
                $tmp_str_pos = strpos($tmp_dump_sql, 'NULL');         //把记录中null值的引号去掉
                $tmp_dump_sql = empty($tmp_str_pos) ? $tmp_dump_sql : substr($tmp_dump_sql, 0, $tmp_str_pos - 1) . 'NULL' . substr($tmp_dump_sql, $tmp_str_pos + 5);
                
	                if (strlen($this->dump_sql) + strlen($tmp_dump_sql) > $this->max_size - 32)
	                {
	                    if ($this->sql_num == 0)
	                    {
	                        $this->dump_sql .= $tmp_dump_sql; //当是第一条记录时强制写入
	                        $this->sql_num++;
	                        $post_pos++;
	                        if ($post_pos == $total)
	                        {
	                        	echo 'xxx';
	                            /* 所有数据已经写完 */
	                            return -1;
	                        }
	                    }

	                    return $post_pos;
	                }
	                else
	                {
	                    $this->dump_sql .= $tmp_dump_sql;
	                    $this->sql_num++; //记录sql条数
	                    $post_pos++;
	                }
               

            }
        }

        /* 所有数据已经写完 */
        return -1;
    }

    /**
     *  备份一个数据表
     *
     * @access  public
     * @param   string      $path       保存路径表名的文件
     * @param   int         $vol        卷标
     *
     * @return  array       $tables     未备份完的表列表
     */
    function dump_table($path, $vol)
    {
        $tables = $this->get_tables_list($path);
        if ($tables === false)
        {
            return false;
        }

        if (empty($tables))
        {
            return $tables;
        }

        $this->dump_sql = $this->make_head($vol);

        foreach($tables as $table => $pos)
        {
        	

            if ($pos == -1)
            {
                /* 获取表定义，如果没有超过限制则保存 */
                $table_df = $this->get_table_df($table, true);
                if (strlen($this->dump_sql) + strlen($table_df) > $this->max_size - 32)
                {	
                    if ($this->sql_num == 0)
                    {
                        /* 第一条记录，强制写入 */
                        $this->dump_sql .= $table_df;
                        $this->sql_num +=2;
                        $tables[$table] = 0;
                    }
                    /* 已经达到上限 */

                    break;
                }
                else
                {	
                    $this->dump_sql .= $table_df;
                    $this->sql_num +=2;
                    $pos = 0;
                    
                    //return ;
                }
                
            }
            
            	
            
            /* 尽可能多获取数据表数据 */
            
            	$post_pos = $this->get_table_data($table, $pos);
            
//             if($table =='return'){
//             	echo $table;
//             	return;
//             }
            if ($post_pos == -1)
            {
                /* 该表已经完成，清除该表 */
                unset($tables[$table]);
            }
            else
            {
                /* 该表未完成。说明将要到达上限,记录备份数据位置 */
                $tables[$table] = $post_pos;
                break;
            }
        }
        $this->dump_sql .= '-- END ecshop v2.x SQL Dump Program ';
        $this->put_tables_list($path, $tables);

        return $tables;
    }

    /**
     *  生成备份文件头部
     *
     * @access  public
     * @param   int     文件卷数
     *
     * @return  string  $str    备份文件头部
     */
    function make_head($vol)
    {
        /* 系统信息 */
        $sys_info['os']         = PHP_OS;
        $sys_info['web_server'] = '';
        $sys_info['php_ver']    = PHP_VERSION;
        $sys_info['mysql_ver']  = '';
        $sys_info['date']       = date('Y-m-d H:i:s');

        $head = "-- yl  SQL Dump Program\r\n".
                 "-- " . $sys_info['web_server'] . "\r\n".
                 "-- \r\n".
                 "-- DATE : ".$sys_info["date"]."\r\n".
                 "-- MYSQL SERVER VERSION : ".$sys_info['mysql_ver']."\r\n".
                 "-- PHP VERSION : ".$sys_info['php_ver']."\r\n".
                 "-- Vol : " . $vol . "\r\n";

        return $head;
    }

    /**
     *  获取备份文件信息
     *
     * @access  public
     * @param   string      $path       备份文件路径
     *
     * @return  array       $arr        信息数组
     */
    function get_head($path)
    {
        /* 获取sql文件头部信息 */
        $sql_info = array('date'=>'','vol'=>0);
        $fp = fopen($path,'rb');
        $str = fread($fp, 250);
        fclose($fp);
        $arr = explode("\n", $str);

        foreach ($arr AS $val)
        {
            $pos = strpos($val, ':');
            if ($pos > 0)
            {
                $type = trim(substr($val, 0, $pos), "-\n\r\t ");
                $value = trim(substr($val, $pos+1), "/\n\r\t ");
                if ($type == 'DATE')
                {
                    $sql_info['date'] = $value;
                }
                elseif ($type == 'Vol')
                {
                    $sql_info['vol'] = $value;
                }
            }
        }

        return $sql_info;
    }

    /**
     *  将文件中数据表列表取出
     *
     * @access  public
     * @param   string      $path    文件路径
     *
     * @return  array       $arr    数据表列表
     */
    function get_tables_list($path)
    {
        if (!file_exists($path))
        {
            $this->error_msg = $path . ' is not exists';

            return false;
        }

        $arr = array();
        $str = @file_get_contents($path);

        if (!empty($str))
        {
            $tmp_arr = explode("\n", $str);
            foreach ($tmp_arr as $val)
            {
                $val = trim ($val, "\r;");
                if (!empty($val))
                {
                    list($table, $count) = explode(':',$val);
                    $arr[$table] = $count;
                }
            }
        }
        return $arr;
    }

    /**
     *  将数据表数组写入指定文件
     *
     * @access  public
     * @param   string      $path    文件路径
     * @param   array       $arr    要写入的数据
     *
     * @return  boolen
     */
    function put_tables_list($path, $arr)
    {
        if (is_array($arr))
        {
            $str = '';
            foreach($arr as $key => $val)
            {
                $str .= $key . ':' . $val . ";\r\n";
            }

            if (@file_put_contents($path, $str))
            {
                return true;
            }
            else
            {
                $this->error_msg = 'Can not write ' . $path;

                return false;
            }
        }
        else
        {
            $this->error_msg = 'It need a array';

            return false;
        }
    }

    /**
     *  返回一个随机的名字
     *
     * @access  public
     * @param
     *
     * @return      string      $str    随机名称
     */
    function get_random_name()
    {
        $str = date('Ymd');

        for ($i = 0; $i < 6; $i++)
        {
            $str .= chr(mt_rand(97, 122));
        }

        return $str;
    }

    /**
     *  返回错误信息
     *
     * @access  public
     * @param
     *
     * @return void
     */
    function errorMsg()
    {
        return $this->error_msg;
    }
    
    /**
     * 文件或目录权限检查函数
     *
     * @access          public
     * @param           string  $file_path   文件路径
     * @param           bool    $rename_prv  是否在检查修改权限时检查执行rename()函数的权限
     *
     * @return          int     返回值的取值范围为{0 <= x <= 15}，每个值表示的含义可由四位二进制数组合推出。
     *                          返回值在二进制计数法中，四位由高到低分别代表
     *                          可执行rename()函数权限、可对文件追加内容权限、可写入文件权限、可读取文件权限。
     */
    static public function file_mode_info($file_path)
    {
    	/* 如果不存在，则不可读、不可写、不可改 */
    	if (!file_exists($file_path))
    	{
    		return false;
    	}
    
    	$mark = 0;
    
    	if (strtoupper(substr(PHP_OS, 0, 3)) == 'WIN')
    	{
    		/* 测试文件 */
    		$test_file = $file_path . '/cf_test.txt';
    
    		/* 如果是目录 */
    		if (is_dir($file_path))
    		{
    			/* 检查目录是否可读 */
    			$dir = @opendir($file_path);
    			if ($dir === false)
    			{
    				return $mark; //如果目录打开失败，直接返回目录不可修改、不可写、不可读
    			}
    			if (@readdir($dir) !== false)
    			{
    				$mark ^= 1; //目录可读 001，目录不可读 000
    			}
    			@closedir($dir);
    
    			/* 检查目录是否可写 */
    			$fp = @fopen($test_file, 'wb');
    			if ($fp === false)
    			{
    				return $mark; //如果目录中的文件创建失败，返回不可写。
    			}
    			if (@fwrite($fp, 'directory access testing.') !== false)
    			{
    				$mark ^= 2; //目录可写可读011，目录可写不可读 010
    			}
    			@fclose($fp);
    
    			@unlink($test_file);
    
    			/* 检查目录是否可修改 */
    			$fp = @fopen($test_file, 'ab+');
    			if ($fp === false)
    			{
    				return $mark;
    			}
    			if (@fwrite($fp, "modify test.\r\n") !== false)
    			{
    				$mark ^= 4;
    			}
    			@fclose($fp);
    
    			/* 检查目录下是否有执行rename()函数的权限 */
    			if (@rename($test_file, $test_file) !== false)
    			{
    				$mark ^= 8;
    			}
    			@unlink($test_file);
    		}
    		/* 如果是文件 */
    		elseif (is_file($file_path))
    		{
    			/* 以读方式打开 */
    			$fp = @fopen($file_path, 'rb');
    			if ($fp)
    			{
    				$mark ^= 1; //可读 001
    			}
    			@fclose($fp);
    
    			/* 试着修改文件 */
    			$fp = @fopen($file_path, 'ab+');
    			if ($fp && @fwrite($fp, '') !== false)
    			{
    				$mark ^= 6; //可修改可写可读 111，不可修改可写可读011...
    			}
    			@fclose($fp);
    
    			/* 检查目录下是否有执行rename()函数的权限 */
    			if (@rename($test_file, $test_file) !== false)
    			{
    				$mark ^= 8;
    			}
    		}
    	}
    	else
    	{
    		if (@is_readable($file_path))
    		{
    			$mark ^= 1;
    		}
    
    		if (@is_writable($file_path))
    		{
    			$mark ^= 14;
    		}
    	}
    
    	return $mark;
    }
    /**
     * 将字节转成可阅读格式
     *
     * @access  public
     * @param
     *
     * @return void
     */
    function num_bitunit($num)
    {
    	$bitunit = array(' B',' KB',' MB',' GB');
    	for ($key = 0, $count = count($bitunit); $key < $count; $key++)
    	{
    	if ($num >= pow(2, 10 * $key) - 1) // 1024B 会显示为 1KB
    	{
    	$num_bitunit_str = (ceil($num / pow(2, 10 * $key) * 100) / 100) . " $bitunit[$key]";
    	}
    	}
    
    	return $num_bitunit_str;
    }
    
    /**
     *
     *
     * @access  public
     * @param
     *
     * @return void
     */
    function sql_import($sql_file)
    {    
    	$sql_str = array_filter(file($sql_file), array('Jcf_Dump_Dump','remove_comment'));
    	$sql_str = str_replace("\r", '', implode('', $sql_str));
    
    	$ret = explode(";\n", $sql_str);
    	$ret_count = count($ret);
    
    	/* 执行sql语句 */
    	for($i = 0; $i < $ret_count; $i++)
    	{
    		$ret[$i] = trim($ret[$i], " \r\n;"); //剔除多余信息
    		if (!empty($ret[$i]))
    		{
    			if ((strpos($ret[$i], 'CREATE TABLE') !== false) && (strpos($ret[$i], 'DEFAULT CHARSET='. str_replace('-', '', 'utf8') )=== false))
    			{
    					/* 建表时缺 DEFAULT CHARSET=utf8 */
    					$ret[$i] = $ret[$i] . 'DEFAULT CHARSET='. str_replace('-', '', 'utf8');
    			}
    			if($i < 5000){
    				$this->db->query($ret[$i]);
    			}
    		}
    	}
    	    
    	return true;
    }
    /**
     *
     *
     * @access  public
     * @param
     * @return  void
     */
    static public function remove_comment($var)
    {
    	return (substr($var, 0, 2) != '--');
    }
    

    /**
     * 将上传文件转移到指定位置
     *
     * @param string $file_name
     * @param string $target_name
     * @return blog
     */
    static public function move_upload_file($file_name, $target_name = '')
    {
    	if (function_exists("move_uploaded_file"))
    	{
    		if (move_uploaded_file($file_name, $target_name))
    		{
    			@chmod($target_name,0755);
    			return true;
    		}
    		else if (copy($file_name, $target_name))
    		{
    			@chmod($target_name,0755);
    			return true;
    		}
    	}
    	elseif (copy($file_name, $target_name))
    	{
    		@chmod($target_name,0755);
    		return true;
    	}
    	return false;
    }
    
}