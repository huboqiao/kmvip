/*
SQLyog 企业版 - MySQL GUI v8.14 
MySQL - 5.0.67-community-nt : Database - vipbak_3
*********************************************************************
*/
/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`vipbak_3` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `vipbak_3`;

/*Table structure for table `payplan` */


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

/*Data for the table `paytype` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
