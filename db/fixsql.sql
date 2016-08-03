-- MySQL dump 10.13  Distrib 5.5.35, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: vip_2
-- ------------------------------------------------------
-- Server version	5.5.35-1ubuntu1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

ALTER TABLE cardcz CHANGE amount amount FLOAT(15,2) DEFAULT 0 COMMENT '充值金额';

ALTER TABLE cardcz ADD balance FLOAT(15,2) DEFAULT 0 COMMENT '充值后余额';

ALTER TABLE cardtx CHANGE amount amount FLOAT(15,2) DEFAULT 0 COMMENT '提现金额';

ALTER TABLE cardtx ADD balance FLOAT(15,2) DEFAULT 0 COMMENT '提现后余额';

ALTER TABLE cardzz CHANGE amount amount FLOAT(15,2) DEFAULT 0 COMMENT '转账金额';

ALTER TABLE `user` ADD righter TINYINT(1) DEFAULT 0 NOT NULL COMMENT '是否有业务授权权限,0：无,1:有';

ALTER TABLE cardzz ADD paybalance FLOAT(15,2) DEFAULT 0 COMMENT '转账后转出卡余额';

ALTER TABLE cardzz ADD payeebalance FLOAT(15,2) DEFAULT 0 COMMENT '转账收款卡余额';

ALTER TABLE customer CHANGE amount amount FLOAT(15,2) DEFAULT 0 COMMENT '账户余额（不包括被冻结的金额）';

ALTER TABLE customer ADD freezen FLOAT(15,2) DEFAULT 0 COMMENT '账户被冻结金额';

ALTER TABLE customer ADD storagenumber MEDIUMINT(8) COMMENT '仓库号数id';

ALTER TABLE customer ADD typeid MEDIUMINT(8) COMMENT '仓库类型';

UPDATE customer SET ugroup = 2 WHERE ugroup = 0;

ALTER TABLE customerinfo CHANGE store finger1 TEXT COMMENT '指纹1'; 

ALTER TABLE customerinfo CHANGE regiona finger2 TEXT COMMENT '指纹2';

ALTER TABLE customerinfo CHANGE storename finger3 TEXT COMMENT '指纹3';

UPDATE customerinfo SET finger1 = '',finger2 = '', finger3 = '';

ALTER TABLE rates ADD latest_date INT(10) DEFAULT 0 NOT NULL COMMENT '最近一次结算利息的时间';

UPDATE modules SET is_show = 1 WHERE module_name = '金荣商城';

UPDATE modules SET is_show = 0 WHERE module_name = '订单管理';

DROP TABLE IF EXISTS `customercategory`;
CREATE TABLE `customercategory` (
   `id` MEDIUMINT(8) NOT NULL AUTO_INCREMENT,
   `name` VARCHAR(50) COLLATE utf8_bin NOT NULL COMMENT '业务权限名称',
   `isactive` TINYINT(1) NOT NULL DEFAULT '1' COMMENT '是否启用，0不启用，1启用',
   `cdate` INT(10) NOT NULL COMMENT '创建时间',
   PRIMARY KEY  (`id`)
 ) ENGINE=INNODB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='utf8_general_ci';
 UPDATE cardzz SET amount = 15360.56 WHERE id = 102;

DROP TABLE IF EXISTS `customergroup`;
CREATE TABLE `customergroup` (
   `id` MEDIUMINT(8) NOT NULL AUTO_INCREMENT,
   `name` VARCHAR(20) COLLATE utf8_bin NOT NULL COMMENT '类别名',
   `typelist` TEXT COLLATE utf8_bin NOT NULL COMMENT '业务权限列表',
   `isactive` TINYINT(1) NOT NULL DEFAULT '1' COMMENT '是否启用，0未启用，1启用',
   `isstorage` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '是否有铺面或者冷库地址（一般只有冷库老板或者大棚老板才有地址）0无 1有',
   `cdate` INT(10) NOT NULL COMMENT '创建时间',
   PRIMARY KEY  (`id`)
 ) ENGINE=INNODB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='utf8_general_ci';
 
DROP TABLE IF EXISTS `msglist`;
 CREATE TABLE `msglist` (
   `id` INT(8) NOT NULL AUTO_INCREMENT,
   `cid` MEDIUMINT(8) NOT NULL COMMENT '用户id',
   `stype` VARCHAR(50) COLLATE utf8_bin NOT NULL COMMENT '充值，提现，转入，转出，利息结算等',
   `mtel` VARCHAR(11) COLLATE utf8_bin NOT NULL COMMENT '发送短息电话',
   `content` TEXT COLLATE utf8_bin COMMENT '发送文本息信',
   `wtype` VARCHAR(100) COLLATE utf8_bin DEFAULT '1' COMMENT '是否发送成功(以短息接口文档为标准)',
   `cdate` INT(10) DEFAULT NULL COMMENT '发送时间',
   PRIMARY KEY  (`id`)
 ) ENGINE=INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='utf8_general_ci';
 
DROP TABLE IF EXISTS `shortset`;
 CREATE TABLE `shortset` (
   `id` MEDIUMINT(8) NOT NULL AUTO_INCREMENT,
   `url` VARCHAR(220) COLLATE utf8_bin NOT NULL COMMENT '地址',
   `username` VARCHAR(50) COLLATE utf8_bin NOT NULL COMMENT '用户名',
   `password` VARCHAR(50) COLLATE utf8_bin NOT NULL COMMENT '密码',
   `type` TINYINT(1) NOT NULL DEFAULT '1' COMMENT '1为post，0为get',
   `content` TEXT COLLATE utf8_bin COMMENT '发送文件模板',
   `isactive` TINYINT(1) NOT NULL DEFAULT '1' COMMENT '是否开启短息平台0为开启，1为未开启',
   PRIMARY KEY  (`id`)
 ) ENGINE=INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='utf8_general_ci';
 
DROP TABLE IF EXISTS `storage_hs`;
 CREATE TABLE `storage_hs` (
   `id` MEDIUMINT(8) NOT NULL AUTO_INCREMENT,
   `qid` MEDIUMINT(8) NOT NULL COMMENT '冷库区域ID',
   `name` VARCHAR(40) COLLATE utf8_bin NOT NULL COMMENT '名称',
   `stat` TINYINT(1) NOT NULL DEFAULT '1' COMMENT '是否启用，0未启用，1启用',
   `cdate` INT(10) NOT NULL COMMENT '创建时间',
   PRIMARY KEY  (`id`)
 ) ENGINE=INNODB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='utf8_general_ci';
 
DROP TABLE IF EXISTS `storage_qy`;
 CREATE TABLE `storage_qy` (
   `id` MEDIUMINT(8) NOT NULL AUTO_INCREMENT,
   `sid` MEDIUMINT(8) NOT NULL COMMENT '冷库ID',
   `name` VARCHAR(40) COLLATE utf8_bin NOT NULL COMMENT '属性值',
   `isactive` TINYINT(1) NOT NULL DEFAULT '1' COMMENT '是否启用1为启用，0为未启用',
   `cdate` INT(10) NOT NULL COMMENT '建立时间',
   PRIMARY KEY  (`id`)
 ) ENGINE=INNODB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='utf8_general_ci';
 
DROP TABLE IF EXISTS `storagetype`;
 CREATE TABLE `storagetype` (
   `id` MEDIUMINT(8) NOT NULL AUTO_INCREMENT,
   `name` VARCHAR(200) COLLATE utf8_bin NOT NULL COMMENT '类型名称',
   `stat` TINYINT(1) NOT NULL COMMENT '1启用 0未启用',
   `cdate` INT(10) NOT NULL COMMENT '记录时间',
   PRIMARY KEY  (`id`)
 ) ENGINE=INNODB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='utf8_general_ci';

DROP TABLE IF EXISTS `ecs_category`;
CREATE TABLE `ecs_category` (
   `cat_id` SMALLINT(5) UNSIGNED NOT NULL AUTO_INCREMENT,
   `cat_name` VARCHAR(90) NOT NULL DEFAULT '',
   `parent_id` SMALLINT(5) UNSIGNED NOT NULL DEFAULT '0',
   PRIMARY KEY  (`cat_id`),
   KEY `parent_id` (`parent_id`)
 ) ENGINE=MYISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='utf8_general_ci';
 
DROP TABLE IF EXISTS `ecs_goods`;
 CREATE TABLE `ecs_goods` (
   `goods_id` MEDIUMINT(8) UNSIGNED NOT NULL AUTO_INCREMENT,
   `cat_id` SMALLINT(5) UNSIGNED NOT NULL DEFAULT '0',
   `goods_sn` VARCHAR(60) NOT NULL DEFAULT '',
   `goods_name` VARCHAR(120) NOT NULL DEFAULT '',
   `goods_number` SMALLINT(5) UNSIGNED NOT NULL DEFAULT '0',
   `goods_price` FLOAT(10,2) UNSIGNED NOT NULL DEFAULT '0.00',
   `goods_desc` TEXT NOT NULL,
   `goods_img` VARCHAR(255) NOT NULL DEFAULT '',
   `add_time` INT(10) UNSIGNED NOT NULL DEFAULT '0',
   `last_update` INT(10) UNSIGNED NOT NULL DEFAULT '0',
   `suppliers_id` SMALLINT(5) UNSIGNED DEFAULT '0',
   `is_active` TINYINT(1) NOT NULL DEFAULT '1',
   `unit` VARCHAR(60) DEFAULT '',
   PRIMARY KEY  (`goods_id`),
   KEY `goods_sn` (`goods_sn`),
   KEY `cat_id` (`cat_id`),
   KEY `last_update` (`last_update`),
   KEY `goods_number` (`goods_number`)
 ) ENGINE=MYISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 COMMENT='utf8_general_ci';
 
DROP TABLE IF EXISTS `ecs_order_goods`;
 CREATE TABLE `ecs_order_goods` (
   `id` MEDIUMINT(8) UNSIGNED NOT NULL AUTO_INCREMENT,
   `order_id` MEDIUMINT(8) UNSIGNED NOT NULL DEFAULT '0',
   `goods_id` MEDIUMINT(8) UNSIGNED NOT NULL DEFAULT '0',
   `goods_number` SMALLINT(5) UNSIGNED NOT NULL DEFAULT '1',
   `goods_price` FLOAT(10,2) NOT NULL DEFAULT '0.00',
   PRIMARY KEY  (`id`),
   KEY `order_id` (`order_id`),
   KEY `goods_id` (`goods_id`)
 ) ENGINE=MYISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8 COMMENT='utf8_general_ci';
 
DROP TABLE IF EXISTS `ecs_order_info`;
 CREATE TABLE `ecs_order_info` (
   `id` MEDIUMINT(8) UNSIGNED NOT NULL AUTO_INCREMENT,
   `order_sn` VARCHAR(20) NOT NULL DEFAULT '',
   `noid` VARCHAR(50) NOT NULL DEFAULT '',
   `order_status` TINYINT(1) UNSIGNED NOT NULL DEFAULT '0',
   `pay_status` TINYINT(1) UNSIGNED NOT NULL DEFAULT '0',
   `add_time` INT(10) NOT NULL DEFAULT '0',
   `pay_time` INT(10) NOT NULL DEFAULT '0',
   PRIMARY KEY  (`id`),
   UNIQUE KEY `order_sn` (`order_sn`),
   KEY `user_id` (`noid`),
   KEY `order_status` (`order_status`),
   KEY `pay_status` (`pay_status`)
 ) ENGINE=MYISAM AUTO_INCREMENT=14 DEFAULT CHARSET=utf8 COMMENT='utf8_general_ci';
 
DROP TABLE IF EXISTS `ecs_supplier`;
 CREATE TABLE `ecs_supplier` (
   `suppliers_id` INT(11) NOT NULL AUTO_INCREMENT,
   `suppliers_name` VARCHAR(64) DEFAULT '' COMMENT '供应商名称',
   `tel` VARCHAR(30) DEFAULT '' COMMENT '电话',
   `mobile` VARCHAR(50) DEFAULT '' COMMENT '手机',
   `email` VARCHAR(50) DEFAULT '' COMMENT '邮箱',
   `address` VARCHAR(120) DEFAULT '' COMMENT '地址',
   `linkman` VARCHAR(20) DEFAULT '' COMMENT '联系人',
   `ctdate` INT(11) DEFAULT NULL COMMENT '创建时间',
   `mddate` INT(11) DEFAULT NULL COMMENT '修改时间',
   `is_check` VARCHAR(1) DEFAULT '1' COMMENT '是否停用标识 0为停用',
   `suppliers_desc` TEXT COMMENT '备注',
   PRIMARY KEY  (`suppliers_id`),
   KEY `name` (`suppliers_name`)
 ) ENGINE=INNODB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8 COMMENT='utf8_general_ci';
 
DROP TABLE IF EXISTS `shop_stock_in`;
 CREATE TABLE `shop_stock_in` (
   `id` MEDIUMINT(8) NOT NULL AUTO_INCREMENT,
   `cdate` INT(10) NOT NULL COMMENT '入库日期',
   `cid` MEDIUMINT(8) NOT NULL COMMENT '入库员',
   PRIMARY KEY  (`id`)
 ) ENGINE=INNODB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COMMENT='utf8_general_ci';
 
DROP TABLE IF EXISTS `shop_stock_in_info`;
 CREATE TABLE `shop_stock_in_info` (
   `id` MEDIUMINT(8) NOT NULL AUTO_INCREMENT,
   `sid` INT(20) NOT NULL COMMENT '订单id',
   `goods_id` MEDIUMINT(8) NOT NULL COMMENT '产品ID',
   `goods_numbers` INT(10) NOT NULL DEFAULT '0' COMMENT '入库数量',
   `remarks` VARCHAR(200) DEFAULT '' COMMENT '备注',
   PRIMARY KEY  (`id`)
 ) ENGINE=INNODB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8 COMMENT='utf8_general_ci';
 
 UPDATE customer SET storagenumber = 1, typeid = 1 WHERE ugroup = 1;
 
 TRUNCATE TABLE customercategory;
 INSERT INTO customercategory VALUES(1, '充值', 1, UNIX_TIMESTAMP());
 TRUNCATE TABLE customergroup;
 INSERT INTO customergroup VALUES(1, '商户', '1,', 1, 1, UNIX_TIMESTAMP());
 INSERT INTO customergroup VALUES(2, '农户', '1,', 1, 0, UNIX_TIMESTAMP());
 UPDATE customer SET storagenumber = 1, typeid = 1 WHERE ugroup = 1;
 ALTER TABLE `vipbak_3`.`cardtx`     
	ADD COLUMN `bankname` VARCHAR(50) NULL COMMENT '转入行名称' AFTER `balance`,     
	ADD COLUMN `bankusername` VARCHAR(50) NULL COMMENT '开户行名称' AFTER `bankname`,     
	ADD COLUMN `bankcard` VARCHAR(50) NULL COMMENT '转入银行卡号' AFTER `bankusername`;
	
DROP TABLE IF EXISTS `statu_changes`;
CREATE TABLE `statu_changes` (
   `id` MEDIUMINT(8) NOT NULL AUTO_INCREMENT,
   `cdate` INT(10) NOT NULL DEFAULT '0' COMMENT '状态变更时间',
   `type` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '变更类型：0绑卡，1挂失，2冻结，3注销',
   `cid` MEDIUMINT(8) COMMENT '客户id',
   `noid` VARCHAR(50) COLLATE utf8_bin  COMMENT '卡noid',
   `uid` MEDIUMINT(8) NOT NULL COMMENT '操作员工id',
   PRIMARY KEY  (`id`)
 ) ENGINE=INNODB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COLLATE='utf8_general_ci';

DROP TABLE IF EXISTS `interests` ;
 CREATE TABLE `interests` (
   `id` MEDIUMINT(8) NOT NULL AUTO_INCREMENT,
   `cid` MEDIUMINT(8) NOT NULL COMMENT '客户id',
   `date` INT(10) NOT NULL DEFAULT '0' COMMENT '日期',
   `amount` DOUBLE(15,2) NOT NULL DEFAULT '0.00' COMMENT '当日余额',
   `rate` DOUBLE(10,5) NOT NULL DEFAULT '0.00000' COMMENT '当日利率',
   `payed` TINYINT(1) NOT NULL DEFAULT '0' COMMENT '时候结算：0未结算，1已结算',
   PRIMARY KEY  (`id`)
 ) ENGINE=INNODB AUTO_INCREMENT=131 DEFAULT CHARSET=utf8 COLLATE='utf8_general_ci';

DROP TABLE IF EXISTS `payplan` ;
CREATE TABLE `payplan` (
   `id` int(8) NOT NULL auto_increment,
   `cid` mediumint(8) NOT NULL COMMENT '选择的缴费用户',
   `uid` tinyint(4) default '0' COMMENT '订单处理人，如果前端缴费，cid为0，结算中心缴费就为当前操作员id',
   `typeid` int(8) NOT NULL COMMENT '缴费类别',
   `amount` double NOT NULL default '0' COMMENT '缴费金额',
   `txt` text COMMENT '缴费备注',
   `paytype` tinyint(1) default '1' COMMENT '缴费渠道，1为终端机，0为结算中心',
   `ismessage` tinyint(1) default '0' COMMENT '是否短息通知，0为不知通，1为发送短息',
   `cdate` int(10) NOT NULL COMMENT '生成日期',
   `edate` int(10) NOT NULL COMMENT '到期日期',
   `paydate` int(10) default NULL COMMENT '缴费日期',
   `payact` tinyint(1) default '1' COMMENT '缴费方式，1：现金，2：金荣卡转账，3银行卡转账',
   PRIMARY KEY  (`id`)
 ) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `paytype`;
CREATE TABLE `paytype` (
   `id` int(8) NOT NULL auto_increment,
   `typename` varchar(40) NOT NULL COMMENT '缴费类型名称',
   `stat` tinyint(1) NOT NULL default '1' COMMENT '是否启用',
   `cdate` int(10) NOT NULL COMMENT '类别创建时间',
   PRIMARY KEY  (`id`)
 ) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;

truncate table `paytype`;

DROP TABLE IF EXISTS `shop_stock_in`;
CREATE TABLE `shop_stock_in` (
  `id` mediumint(8) NOT NULL auto_increment,
  `cdate` int(10) NOT NULL COMMENT 'å…¥åº“æ—¥æœŸ',
  `cid` mediumint(8) NOT NULL COMMENT 'å…¥åº“å‘˜',
  `stock_on` varchar(20) NOT NULL default '',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COMMENT='utf8_general_ci';

insert into `shop_stock_in`(`id`,`cdate`,`cid`,`stock_on`) values (5,1427169455,25,''),(6,1427169648,25,''),(7,1427184418,25,''),(8,1427187831,25,'1427187802.81434'),(9,1427187878,25,'1427187849454'),(10,1427258753,25,'1427258712289');

ALTER TABLE cardcz CHANGE amount amount DOUBLE(15,2) DEFAULT 0;

ALTER TABLE cardcz CHANGE balance balance DOUBLE(15,2) DEFAULT 0;

ALTER TABLE cardtx CHANGE amount amount DOUBLE(15,2) DEFAULT 0;

ALTER TABLE cardtx CHANGE balance balance DOUBLE(15,2) DEFAULT 0;

ALTER TABLE cardzz CHANGE amount amount DOUBLE(15,2) DEFAULT 0;

ALTER TABLE cardzz CHANGE paybalance paybalance DOUBLE(15,2) DEFAULT 0;

ALTER TABLE cardzz CHANGE payeebalance payeebalance DOUBLE(15,2) DEFAULT 0;

ALTER TABLE customer CHANGE amount amount DOUBLE(15,2) DEFAULT 0;

ALTER TABLE customer CHANGE freezen freezen DOUBLE(15,2) DEFAULT 0;

ALTER TABLE ecs_goods CHANGE goods_price goods_price DOUBLE(15,2) DEFAULT 0;

ALTER TABLE ecs_order_goods CHANGE goods_price goods_price DOUBLE(15,2) DEFAULT 0;

ALTER TABLE goodslist CHANGE price price DOUBLE(15,2) DEFAULT 0;

DROP TABLE IF EXISTS `shop_stock_in`;

CREATE TABLE `shop_stock_in` (
   `id` MEDIUMINT(8) NOT NULL AUTO_INCREMENT,
   `cdate` INT(10) NOT NULL COMMENT 'å…¥åº“æ—¥æœŸ',
   `cid` MEDIUMINT(8) NOT NULL COMMENT 'å…¥åº“å‘˜',
   `stock_on` VARCHAR(20) NOT NULL DEFAULT '',
   PRIMARY KEY  (`id`)
 ) ENGINE=INNODB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COMMENT='utf8_general_ci';

ALTER TABLE interest CHANGE Interest Interest DOUBLE(15,2) DEFAULT 0;

ALTER TABLE `order` CHANGE price price DOUBLE(15,2) DEFAULT 0;

ALTER TABLE order_info CHANGE price price DOUBLE(15,2) DEFAULT 0;

ALTER TABLE outbound_info CHANGE counts counts DOUBLE(15,2) DEFAULT 0;

ALTER TABLE outbound_info CHANGE price price DOUBLE(15,2) DEFAULT 0;

ALTER TABLE rates CHANGE rates rates DOUBLE(15,5) DEFAULT 0;

ALTER TABLE stock CHANGE goods_numbers goods_numbers DOUBLE(15,2) DEFAULT 0;

ALTER TABLE stock CHANGE outsocket outsocket DOUBLE(15,2) DEFAULT 0;

TRUNCATE TABLE channel ;
TRUNCATE TABLE customercategory ;
INSERT INTO `vipbak_3`.`customercategory`(`id`,`name`,`isactive`,`cdate`) VALUES ( NULL,'充值','1','1431419267');

TRUNCATE TABLE customergroup ; 
INSERT INTO `vipbak_3`.`customergroup`(`id`,`name`,`typelist`,`isactive`,`isstorage`,`cdate`) VALUES ( NULL,'商户','1,','1','1','1431419267');
INSERT INTO `vipbak_3`.`customergroup`(`id`,`name`,`typelist`,`isactive`,`isstorage`,`cdate`) VALUES ( NULL,'农户','1,','1','0','1431419267');

TRUNCATE TABLE ecs_category;
TRUNCATE TABLE ecs_goods;
TRUNCATE TABLE ecs_order_goods;
TRUNCATE TABLE ecs_order_info ;
TRUNCATE TABLE ecs_supplier ;
TRUNCATE TABLE goodslist ;
TRUNCATE TABLE interests;
TRUNCATE TABLE msglist;
TRUNCATE TABLE `order`;
TRUNCATE TABLE order_info;
TRUNCATE TABLE outbound;
TRUNCATE TABLE outbound_info;
TRUNCATE TABLE party;
TRUNCATE TABLE rates;
INSERT INTO `vipbak_3`.`rates`(`id`,`rates`,`rates_date`,`latest_date`) VALUES ( NULL,'0.0002','1','1431419267');

TRUNCATE TABLE shop_stock_in;
TRUNCATE TABLE shop_stock_in_info;
TRUNCATE TABLE shortset;
TRUNCATE TABLE statu_changes;
TRUNCATE TABLE stock;
TRUNCATE TABLE stock_outto;
TRUNCATE TABLE storage;
INSERT INTO `vipbak_3`.`storage`(`id`,`name`,`stat`,`cdate`) VALUES ( NULL,'金荣冷库','1','1431419267');

TRUNCATE TABLE storage_hs;
INSERT INTO `vipbak_3`.`storage_hs`(`id`,`qid`,`name`,`stat`,`cdate`) VALUES ( NULL,'1','1','1','1431419267');

TRUNCATE TABLE storage_qy;
INSERT INTO `vipbak_3`.`storage_qy`(`id`,`sid`,`name`,`isactive`,`cdate`) VALUES ( NULL,'1','A','1','1431419267');

TRUNCATE TABLE storagetype;
INSERT INTO `vipbak_3`.`storagetype`(`id`,`name`,`stat`,`cdate`) VALUES ( NULL,'冷库','1','1431419267');
INSERT INTO `vipbak_3`.`storagetype`(`id`,`name`,`stat`,`cdate`) VALUES ( NULL,'大鹏','1','1431419267');

TRUNCATE TABLE rates;
INSERT INTO `vipbak_3`.`rates`(`id`,`rates`,`rates_date`,`latest_date`) VALUES ( NULL,'0.0002','1','1404871761');


TRUNCATE TABLE storer;

INSERT INTO `vipbak_3`.`customer`(`id`,`membername`,`sex`,`nation`,`tel`,`idcard`,`carddate`,`adduser`,`amount`,`adder`,`stat`,`cdate`,`ugroup`,`lasttime`,`actdate`,`freezen`,`storagenumber`,`typeid`) VALUES ( 168,'金荣','1','汉','13666668888','123456200101011234','4070880000','1','0.00','金荣服务中心','1','1431419267','1',NULL,NULL,'0.00','1','1');

INSERT INTO `vipbak_3`.`card`(`id`,`cardid`,`stat`,`cdate`,`bdate`,`password`,`uid`,`noid`,`addid`) VALUES ( NULL,'1000000000','1','143148189','1431482566','e10adc3949ba59abbe56e057f20f883e',168,1000000000,1);

INSERT INTO `vipbak_3`.`statu_changes`(`id`,`cdate`,`type`,`cid`,`noid`,`uid`) VALUES ( NULL,'1431482566','0','168','1000000000','1');

INSERT INTO `vipbak_3`.`customerinfo`(`id`,`cid`,`bankcard`,`bankname`,`bankadder`,`bankusername`,`useimg_path`,`cardimg_path`,`cardimgt_path`,`finger1`,`finger2`,`finger3`,`relativesname`,`relativessex`,`relationship`,`relationtem`) VALUES ( NULL,'168',' ',' ','-','金荣','/img/dssd.png','/img/sdafd.png','/img/dsafd.png',' ',' ',' ','黄鹏','1','负责人','13866668888');

DROP TABLE IF EXISTS `payplan`;

CREATE TABLE `payplan` (
  `id` int(8) NOT NULL auto_increment,
  `cid` mediumint(8) NOT NULL COMMENT '选择的缴费用户',
  `uid` tinyint(4) default '0' COMMENT '订单处理人，如果前端缴费，cid为0，结算中心缴费就为当前操作员id',
  `typeid` int(8) NOT NULL COMMENT '缴费类别',
  `amount` double NOT NULL default '0' COMMENT '缴费金额',
  `txt` text COMMENT '缴费备注',
  `paytype` tinyint(1) default '1' COMMENT '缴费渠道，1为终端机，0为结算中心',
  `ismessage` tinyint(1) default '0' COMMENT '是否短息通知，0为不知通，1为发送短息',
  `cdate` int(10) NOT NULL COMMENT '生成日期',
  `edate` int(10) NOT NULL COMMENT '到期日期',
  `paydate` int(10) default NULL COMMENT '缴费日期',
  `payact` tinyint(1) default '1' COMMENT '缴费方式，1：现金，2：金荣卡转账，3银行卡转账',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

UPDATE `vipbak_3`.`rates` SET `latest_date`=UNIX_TIMESTAMP();

/*Data for the table `payplan` */

/*Table structure for table `paytype` */

DROP TABLE IF EXISTS `paytype`;

CREATE TABLE `paytype` (
  `id` int(8) NOT NULL auto_increment,
  `typename` varchar(40) NOT NULL COMMENT '缴费类型名称',
  `stat` tinyint(1) NOT NULL default '1' COMMENT '是否启用',
  `cdate` int(10) NOT NULL COMMENT '类别创建时间',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `resource`;

CREATE TABLE `resource` (
  `id` int(10) NOT NULL auto_increment,
  `parent_id` int(10) NOT NULL default '0',
  `re_name` varchar(40) NOT NULL default '',
  `action` varchar(150) default '',
  `is_active` smallint(1) default '1',
  `sortid` tinyint(4) default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8;

/*Data for the table `resource` */

LOCK TABLES `resource` WRITE;

insert  into `resource`(`id`,`parent_id`,`re_name`,`action`,`is_active`,`sortid`) values (1,0,'权限管理','',1,0),(2,1,'账户管理','',1,0),(3,1,'金荣卡管理','',1,0),(4,1,'资金管理','',1,0),(5,1,'报表管理','',1,0),(6,1,'利息管理','',1,0),(7,1,'缴费管理','',1,0),(8,1,'基本资料设置','',1,0),(9,1,'系统设置','',1,0),(10,1,'商城管理','',1,0),(11,2,'开户','',1,0),(12,2,'客户查询','',1,0),(13,2,'修改客户资料','',1,0),(14,2,'修改客户密码','',1,0),(15,2,'注销','',1,0),(16,3,'添加','',1,0),(17,3,'绑定','',1,0),(18,3,'查询','',1,0),(19,3,'卡挂失','',1,0),(20,4,'充值','',1,0),(21,4,'提现','',1,0),(22,4,'转账','',1,0),(23,5,'公司资金管理','',1,0),(24,5,'客户资金管理','',1,0),(25,5,'流水账','',1,0),(26,5,'销售管理','',1,0),(27,6,'设置利息','',1,0),(28,6,'查看利息','',1,0),(29,6,'利息结算','',1,0),(30,8,'类别设置','',1,0),(31,8,'用户组','',1,0),(32,8,'用户','',1,0),(33,8,'仓库列表','',1,0),(34,8,'修改客户资料','',1,0),(35,8,'短信管理','',1,0),(36,9,'本机设置','',1,0),(37,9,'修改用户密码','',1,0),(38,9,'系统更新','',1,0),(39,9,'锁屏','',1,0),(40,2,'客户资料 修改','',1,0),(41,1,'缴 费 管 理','',1,0),(42,41,'缴费项目设置','',1,0),(43,8,'仓库类型列表','',1,0),(44,8,'短信设置','',1,0);

UNLOCK TABLES;