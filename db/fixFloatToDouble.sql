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

INSERT INTO `vipbak_3`.`card`(`id`,`cardid`,`stat`,`cdate`,`bdate`,`password`,`uid`,`noid`,`addid`) VALUES ( NULL,'1000000000','1','143148189','1431482566','e10adc3949ba59abbe56e057f20f883e',133,1000000000,1);

INSERT INTO `vipbak_3`.`statu_changes`(`id`,`cdate`,`type`,`cid`,`noid`,`uid`) VALUES ( NULL,'1431482566','0','133','1000000000','1');

INSERT INTO `vipbak_3`.`customerinfo`(`id`,`cid`,`bankcard`,`bankname`,`bankadder`,`bankusername`,`useimg_path`,`cardimg_path`,`cardimgt_path`,`finger1`,`finger2`,`finger3`,`relativesname`,`relativessex`,`relationship`,`relationtem`) VALUES ( NULL,'168',' ',' ','-','金荣','/img/dssd.png','/img/sdafd.png','/img/dsafd.png',' ',' ',' ','黄鹏','1','负责人','13866668888');
