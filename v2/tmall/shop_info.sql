/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50628
Source Host           : 127.0.0.1:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50628
File Encoding         : 65001

Date: 2018-04-01 22:38:27
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for shop_info
-- ----------------------------
DROP TABLE IF EXISTS `shop_info`;
CREATE TABLE `shop_info` (
  `id` varchar(50) DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of shop_info
-- ----------------------------
INSERT INTO `shop_info` VALUES ('105089828', '努比亚官方旗舰店', 'https://nubia.tmall.com');
INSERT INTO `shop_info` VALUES ('149493505', '酷派官方旗舰店', 'https://coolpad.tmall.com');
INSERT INTO `shop_info` VALUES ('145902373', 'ZTE中兴官方旗舰店', 'https://zte.tmall.com');
INSERT INTO `shop_info` VALUES ('104682877', '魅族官方旗舰店', 'https://meizu.tmall.com');
INSERT INTO `shop_info` VALUES ('71799145', 'vivo官方旗舰店', 'https://vivo.tmall.com');
INSERT INTO `shop_info` VALUES ('72217984', 'oppo手机官方旗舰店', 'https://oppo.tmall.com');
INSERT INTO `shop_info` VALUES ('104736810', '小米官方旗舰店', 'https://xiaomi.tmall.com');
INSERT INTO `shop_info` VALUES ('101717810', '荣耀官方旗舰店', 'https://huawei.tmall.com');
INSERT INTO `shop_info` VALUES ('150920153', '华为官方旗舰店', 'https://huaweistore.tmall.com');
