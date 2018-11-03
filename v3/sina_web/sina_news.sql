/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 50719
 Source Host           : localhost
 Source Database       : sina_news

 Target Server Type    : MySQL
 Target Server Version : 50719
 File Encoding         : utf-8

 Date: 08/19/2018 01:02:57 AM
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
--  Table structure for `news`
-- ----------------------------
DROP TABLE IF EXISTS `news`;
CREATE TABLE `news` (
  `ID` varchar(32) NOT NULL,
  `TITLE` text,
  `SOURCE` varchar(255) DEFAULT NULL,
  `URL` varchar(255) DEFAULT NULL,
  `KEYWORDS` varchar(100) DEFAULT NULL,
  `CREATE_TIME` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Table structure for `users`
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `ACCOUNT` varchar(32) NOT NULL,
  `PASSWORD` varchar(32) NOT NULL,
  `ROLE` varchar(10) DEFAULT NULL,
  `CREATE_TIME` datetime DEFAULT NULL,
  PRIMARY KEY (`ACCOUNT`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
--  Records of `users`
-- ----------------------------
BEGIN;
INSERT INTO `users` VALUES ('admin', 'admin', 'admin', '2018-08-18 19:33:44'), ('test', 'admin', 'user', '2018-08-18 23:53:55');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
