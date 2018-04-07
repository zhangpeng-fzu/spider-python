/*
Navicat MySQL Data Transfer

Source Server         : mysql
Source Server Version : 50628
Source Host           : 127.0.0.1:3306
Source Database       : test

Target Server Type    : MYSQL
Target Server Version : 50628
File Encoding         : 65001

Date: 2018-04-01 22:38:11
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for phone_info
-- ----------------------------
DROP TABLE IF EXISTS `phone_info`;
CREATE TABLE `phone_info` (
  `id` varchar(50) DEFAULT NULL,
  `shop_id` varchar(50) DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `url` varchar(100) DEFAULT NULL,
  `img` varchar(100) DEFAULT NULL,
  `sold` varchar(100) DEFAULT NULL,
  `totalSoldQuantity` varchar(100) DEFAULT NULL,
  `price` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of phone_info
-- ----------------------------
INSERT INTO `phone_info` VALUES ('554777854540', '105089828', '【特惠200 仅2299元】nubia/努比亚 Z17 无边框6+64g变焦双摄手机', 'https://detail.m.tmall.com/item.htm?id=554777854540', '//img.alicdn.com/bao/uploaded/i2/1677335387/TB1q5t7apooBKNjSZFPXXXa2XXa_!!0-item_pic.jpg', '2148', '27955', '2299.00');
INSERT INTO `phone_info` VALUES ('548999134257', '105089828', '【特惠300 仅1299】nubia/努比亚 Z17mini 6G版1300万双摄手机', 'https://detail.m.tmall.com/item.htm?id=548999134257', '//img.alicdn.com/bao/uploaded/i3/1677335387/TB1g94xatknBKNjSZKPXXX6OFXa_!!0-item_pic.jpg', '3620', '30362', '1299.00');
INSERT INTO `phone_info` VALUES ('559612504297', '105089828', '【特惠300】nubia/努比亚 Z17 8+64GB无边框变焦双摄全网通手机', 'https://detail.m.tmall.com/item.htm?id=559612504297', '//img.alicdn.com/bao/uploaded/i1/1677335387/TB1bsx5arZnBKNjSZFGXXbt3FXa_!!0-item_pic.jpg', '1808', '5586', '2499.00');
INSERT INTO `phone_info` VALUES ('559378766802', '105089828', '【直降200 低至1499】nubia/努比亚 Z17minis四摄6+64g大内存手机', 'https://detail.m.tmall.com/item.htm?id=559378766802', '//img.alicdn.com/bao/uploaded/i1/1677335387/TB16f9YcN9YBuNjy0FfXXXIsVXa_!!0-item_pic.jpg', '1926', '4386', '1499.00');
INSERT INTO `phone_info` VALUES ('559017773532', '105089828', '【领券减200】nubia/努比亚 z17s 全面屏无边框全网通大内存手机', 'https://detail.m.tmall.com/item.htm?id=559017773532', '//img.alicdn.com/bao/uploaded/i3/1677335387/TB1CA2IhVuWBuNjSspnXXX1NVXa_!!0-item_pic.jpg', '792', '9590', '2999.00');
INSERT INTO `phone_info` VALUES ('547561600523', '105089828', '【特惠400】nubia/努比亚 z17 mini 1300万后置双摄4+64g手机', 'https://detail.m.tmall.com/item.htm?id=547561600523', '//img.alicdn.com/bao/uploaded/i3/1677335387/TB1aW5VcL5TBuNjSspmXXaDRVXa_!!0-item_pic.jpg', '365', '33748', '1099.00');
INSERT INTO `phone_info` VALUES ('553415671027', '105089828', '【直降700 低至2699】nubia/努比亚 Z17黑金无边框6+128G手机', 'https://detail.m.tmall.com/item.htm?id=553415671027', '//img.alicdn.com/bao/uploaded/i3/1677335387/TB1zF6Lh1uSBuNjSsziXXbq8pXa_!!0-item_pic.jpg', '364', '2343', '2699.00');
INSERT INTO `phone_info` VALUES ('565698351249', '105089828', '【新品首发】nubia/努比亚 V18全面屏4+64G大内存智能官方手机', 'https://detail.m.tmall.com/item.htm?id=565698351249', '//img.alicdn.com/bao/uploaded/i2/1677335387/TB1o9xbbYorBKNjSZFjXXc_SpXa_!!0-item_pic.jpg', '2081', '2077', '1299.00');
INSERT INTO `phone_info` VALUES ('555993987319', '105089828', '【直降700 低至2699】nubia/努比亚 Z17烈焰红6+128G变焦双摄手机', 'https://detail.m.tmall.com/item.htm?id=555993987319', '//img.alicdn.com/bao/uploaded/i3/1677335387/TB1q_HshY1YBuNjSszeXXablFXa_!!0-item_pic.jpg', '136', '2717', '2699.00');
INSERT INTO `phone_info` VALUES ('558193225702', '105089828', '【直降1000】nubia/努比亚 Z17极光蓝/黑金8+128G变焦双摄手机', 'https://detail.m.tmall.com/item.htm?id=558193225702', '//img.alicdn.com/bao/uploaded/i4/1677335387/TB1M2WKhkSWBuNjSszdXXbeSpXa_!!0-item_pic.jpg', '1', '499', '3999.00');
INSERT INTO `phone_info` VALUES ('543073250747', '149493505', '[三期免息]Coolpad/酷派 Cool S1 4/6+64G全网通4G学生智能手机', 'https://detail.m.tmall.com/item.htm?id=543073250747', '//img.alicdn.com/bao/uploaded/i4/2815133273/TB13GJ5b.OWBKNjSZKzXXXfWFXa_!!0-item_pic.jpg', '351', '4591', '2728.00');
INSERT INTO `phone_info` VALUES ('564350841621', '145902373', '【12期免息】ZTE/中兴 Z999 天机Axon M全网通4G折叠双屏智能手机', 'https://detail.m.tmall.com/item.htm?id=564350841621', '//img.alicdn.com/bao/uploaded/i3/2765414748/TB2L9oHhXGWBuNjy0FbXXb4sXXa_!!2765414748-0-item_pic.jpg', '154', '176', '3888.00');
INSERT INTO `phone_info` VALUES ('553413351754', '145902373', '12期免息 ZTE/中兴 A2018天机7s 4+128G全网通安全加密手机', 'https://detail.m.tmall.com/item.htm?id=553413351754', '//img.alicdn.com/bao/uploaded/i1/2765414748/TB1.KKio_vI8KJjSspjXXcgjXXa_!!0-item_pic.jpg', '2', '24', '4599.00');
INSERT INTO `phone_info` VALUES ('560401421483', '145902373', '直降100元 人脸识别 ZTE/中兴 A3 Blade双摄三卡全网通4G智能手机', 'https://detail.m.tmall.com/item.htm?id=560401421483', '//img.alicdn.com/bao/uploaded/i2/2765414748/TB24Dhkh49YBuNjy0FfXXXIsVXa_!!2765414748-0-item_pic.jpg', '2510', '6855', '699.00');
INSERT INTO `phone_info` VALUES ('541253007590', '145902373', 'ZTE/中兴 BA910电信版（A910）全网通支持多种NFC智能4G手机', 'https://detail.m.tmall.com/item.htm?id=541253007590', '//img.alicdn.com/bao/uploaded/i3/2765414748/TB2NcgIhXGWBuNjy0FbXXb4sXXa_!!2765414748-0-item_pic.jpg', '38', '370', '699.00');
INSERT INTO `phone_info` VALUES ('527214344081', '145902373', '【晒图有惊喜】ZTE/中兴 Q529T 远航3移动4G双卡大电池 5英寸手机', 'https://detail.m.tmall.com/item.htm?id=527214344081', '//img.alicdn.com/bao/uploaded/i2/2765414748/TB1eY36oL2H8KJjy0FcXXaDlFXa_!!0-item_pic.jpg', '0', '40', '799.00');
INSERT INTO `phone_info` VALUES ('554831845009', '145902373', 'ZTE/中兴 V0840 小鲜5 全网通4G指纹 3G运行 美颜拍照 双摄手机', 'https://detail.m.tmall.com/item.htm?id=554831845009', '//img.alicdn.com/bao/uploaded/i1/2765414748/TB182t8cFuWBuNjSspnXXX1NVXa_!!0-item_pic.jpg', '4', '117', '999.00');
INSERT INTO `phone_info` VALUES ('557156077822', '104682877', '【领券低至919元】Meizu/魅族 魅蓝 Note6 疾速双摄 快充大电池', 'https://detail.m.tmall.com/item.htm?id=557156077822', '//img.alicdn.com/bao/uploaded/i2/1695308781/TB1NaiPcL9TBuNjy1zbXXXpepXa_!!0-item_pic.jpg', '20442', '228057', '999.00');
INSERT INTO `phone_info` VALUES ('558540134751', '104682877', '【领券立减50低至649】Meizu/魅族 魅蓝6 八核AI加速800万前置美', 'https://detail.m.tmall.com/item.htm?id=558540134751', '//img.alicdn.com/bao/uploaded/i1/1695308781/TB1_ui2cGmWBuNjy1XaXXXCbXXa_!!0-item_pic.jpg', '13079', '144120', '699.00');
INSERT INTO `phone_info` VALUES ('563484952650', '104682877', 'Meizu/魅族 魅蓝 S6全面屏 三星游戏CPU 指纹解锁 全网通学生手机', 'https://detail.m.tmall.com/item.htm?id=563484952650', '//img.alicdn.com/bao/uploaded/i4/1695308781/TB1GheCcNSYBuNjSsphXXbGvVXa_!!0-item_pic.jpg', '12375', '63601', '999.00');
INSERT INTO `phone_info` VALUES ('555850828895', '104682877', '【领券减100元】Meizu/魅族 PRO 7 全网通OLED屏4G智能手机pro7', 'https://detail.m.tmall.com/item.htm?id=555850828895', '//img.alicdn.com/bao/uploaded/i4/1695308781/TB1qNe9ggmTBuNjy1XbXXaMrVXa_!!0-item_pic.jpg', '3362', '32015', '1999.00');
INSERT INTO `phone_info` VALUES ('556026351191', '104682877', '领券减150元 Meizu/魅族 PRO 7 Plus全网通OLED屏智能手机pro7', 'https://detail.m.tmall.com/item.htm?id=556026351191', '//img.alicdn.com/bao/uploaded/i4/1695308781/TB168N7c9CWBuNjy0FhXXb6EVXa_!!0-item_pic.jpg', '959', '9676', '2799.00');
INSERT INTO `phone_info` VALUES ('549066366714', '104682877', '【到手829起】Meizu/魅族 魅蓝E2 全网通正面指纹快充4G智能手机', 'https://detail.m.tmall.com/item.htm?id=549066366714', '//img.alicdn.com/bao/uploaded/i4/1695308781/TB1fRuvhmtYBeNjSspkXXbU8VXa_!!0-item_pic.jpg', '2358', '113154', '899.00');
INSERT INTO `phone_info` VALUES ('543285442762', '104682877', '【16G礼盒领券减100】Meizu/魅族 魅蓝Note5全网通快充智能手机', 'https://detail.m.tmall.com/item.htm?id=543285442762', '//img.alicdn.com/bao/uploaded/i1/1695308781/TB1_fR8arZnBKNjSZFKXXcGOVXa_!!0-item_pic.jpg', '2143', '256926', '999.00');
INSERT INTO `phone_info` VALUES ('559989778357', '104682877', '【满1299领券立减150】Meizu/魅族 魅蓝 Note6 航海王限定版', 'https://detail.m.tmall.com/item.htm?id=559989778357', '//img.alicdn.com/bao/uploaded/i4/1695308781/TB1n6S_dLal9eJjSZFzXXaITVXa_!!0-item_pic.jpg', '1203', '2800', '999.00');
INSERT INTO `phone_info` VALUES ('559015373981', '104682877', '【满899领券立减70】Meizu/魅族 魅蓝6 正面指纹八核智能学生机', 'https://detail.m.tmall.com/item.htm?id=559015373981', '//img.alicdn.com/bao/uploaded/i3/1695308781/TB1Noi0cQCWBuNjy0FaXXXUlXXa_!!0-item_pic.jpg', '988', '10276', '699.00');
INSERT INTO `phone_info` VALUES ('542325634260', '104682877', '【领券到手价899元】Meizu/魅族 魅蓝X全网通电信版4G智能手机', 'https://detail.m.tmall.com/item.htm?id=542325634260', '//img.alicdn.com/bao/uploaded/i3/1695308781/TB1xUNGgFGWBuNjy0FbXXb4sXXa_!!0-item_pic.jpg', '168', '22162', '999.00');
INSERT INTO `phone_info` VALUES ('545204639851', '104682877', 'Meizu/魅族 魅蓝5s合约机4G+全网通移动定制版', 'https://detail.m.tmall.com/item.htm?id=545204639851', '//img.alicdn.com/bao/uploaded/i2/1695308781/TB1c0L3k_TI8KJjSsphXXcFppXa_!!0-item_pic.jpg', '200', '1026', '699.00');
INSERT INTO `phone_info` VALUES ('564297023090', '104682877', '魅蓝 Stay true 潮范真我时尚保护壳双色可选魅蓝S6/note6手机壳', 'https://detail.m.tmall.com/item.htm?id=564297023090', '//img.alicdn.com/bao/uploaded/i3/1695308781/TB1_uTjnx6I8KJjSszfXXaZVXXa_!!0-item_pic.jpg', '505', '2529', '49.00');
INSERT INTO `phone_info` VALUES ('559930461705', '104682877', '【领券立减100】Meizu/魅族 魅蓝6移动4G+定制版 正面指纹高颜值', 'https://detail.m.tmall.com/item.htm?id=559930461705', '//img.alicdn.com/bao/uploaded/i3/1695308781/TB1ri4Zogn.PuJjSZFkXXc_lpXa_!!0-item_pic.jpg', '141', '616', '899.00');
INSERT INTO `phone_info` VALUES ('543503011875', '104682877', 'Meizu/魅族 魅蓝S6 魅蓝6 魅蓝E3pro7plus高透保护膜手机贴膜防刮', 'https://detail.m.tmall.com/item.htm?id=543503011875', '//img.alicdn.com/bao/uploaded/i1/1695308781/TB1skv8ilDH8KJjSszcXXbDTFXa_!!0-item_pic.jpg', '290', '5270', '19.00');
INSERT INTO `phone_info` VALUES ('559263716289', '104682877', '【16G到手699】Meizu/魅族 魅蓝5s 全网通4G电信定制版智能机', 'https://detail.m.tmall.com/item.htm?id=559263716289', '//img.alicdn.com/bao/uploaded/i3/1695308781/TB1xMlVgH1YBuNjSszeXXablFXa_!!0-item_pic.jpg', '82', '137', '699.00');
INSERT INTO `phone_info` VALUES ('543888801550', '104682877', '【16G到手799元】Meizu/魅族 魅蓝note5 双卡双待 4000mAh大电池', 'https://detail.m.tmall.com/item.htm?id=543888801550', '//img.alicdn.com/bao/uploaded/i3/1695308781/TB10CTRabGYBuNjy0FoXXciBFXa_!!0-item_pic.jpg', '253', '9356', '799.00');
INSERT INTO `phone_info` VALUES ('559480019984', '104682877', '【领券减100元】Meizu/魅族 PRO 7 全网通OLED屏4G智能手机pro7', 'https://detail.m.tmall.com/item.htm?id=559480019984', '//img.alicdn.com/bao/uploaded/i1/1695308781/TB2mrwEg1uSBuNjSsplXXbe8pXa_!!1695308781-0-item_pic.jpg', '0', '3', '2399.00');
INSERT INTO `phone_info` VALUES ('558197055865', '71799145', '【6期免息赠礼】vivo X20全网通4G智能全面屏正品手机vivox20', 'https://detail.m.tmall.com/item.htm?id=558197055865', '//img.alicdn.com/bao/uploaded/i1/883737303/TB1X_NjhmtYBeNjSspaXXaOOFXa_!!0-item_pic.jpg', '6588', '173237', '2798.00');
INSERT INTO `phone_info` VALUES ('565342088185', '71799145', '【新品享豪礼】vivo X21全面屏智能全网通4G手机全新正品vivox21', 'https://detail.m.tmall.com/item.htm?id=565342088185', '//img.alicdn.com/bao/uploaded/i3/883737303/TB1aLkwg9CWBuNjy0FhXXb6EVXa_!!0-item_pic.jpg', '9697', '10687', '3198.00');
INSERT INTO `phone_info` VALUES ('562658733506', '71799145', '3期免息/vivo Y75千元全面屏面部识别全网通4G智能手机vivoy75', 'https://detail.m.tmall.com/item.htm?id=562658733506', '//img.alicdn.com/bao/uploaded/i3/883737303/TB1cvTug4SYBuNjSsphXXbGvVXa_!!0-item_pic.jpg', '5360', '27419', '1498.00');
INSERT INTO `phone_info` VALUES ('559858377418', '71799145', '【6期免息】vivo Y79全面屏智能4G手机全网通面部识别vivoy79', 'https://detail.m.tmall.com/item.htm?id=559858377418', '//img.alicdn.com/bao/uploaded/i3/883737303/TB1obDDg9CWBuNjy0FhXXb6EVXa_!!0-item_pic.jpg', '4133', '13250', '1998.00');
INSERT INTO `phone_info` VALUES ('566175799630', '71799145', '【新品6期免息】vivo Y85全面屏双摄全网通4G智能正品手机vivoy85', 'https://detail.m.tmall.com/item.htm?id=566175799630', '//img.alicdn.com/bao/uploaded/i2/883737303/TB13D6.g25TBuNjSspmXXaDRVXa_!!0-item_pic.jpg', '5426', '6270', '1598.00');
INSERT INTO `phone_info` VALUES ('559778877551', '71799145', '【6期免息】vivo X20plus全面屏智能4G手机全网通vivox20plus', 'https://detail.m.tmall.com/item.htm?id=559778877551', '//img.alicdn.com/bao/uploaded/i1/883737303/TB1osAcgYSYBuNjSspfXXcZCpXa_!!0-item_pic.jpg', '1292', '17094', '3198.00');
INSERT INTO `phone_info` VALUES ('565661039920', '71799145', '【稀缺限量】vivo X21屏幕指纹版智能全网通4G手机vivox21', 'https://detail.m.tmall.com/item.htm?id=565661039920', '//img.alicdn.com/bao/uploaded/i2/883737303/TB2P4jzg3aTBuNjSszfXXXgfpXa_!!883737303-0-item_pic.jpg', '10864', '12499', '3598.00');
INSERT INTO `phone_info` VALUES ('566086018489', '71799145', '【直降200】vivo Y69全网通4G智能手机全新官方正品vivoy69 y66', 'https://detail.m.tmall.com/item.htm?id=566086018489', '//img.alicdn.com/bao/uploaded/i2/883737303/TB1ZGpihmtYBeNjSspaXXaOOFXa_!!0-item_pic.jpg', '1935', '2432', '999.00');
INSERT INTO `phone_info` VALUES ('554570074264', '71799145', '【6期免息】vivo X9s Plus前置双摄全网通4G智能手机x9splus', 'https://detail.m.tmall.com/item.htm?id=554570074264', '//img.alicdn.com/bao/uploaded/i1/883737303/TB1sA3RbHZnBKNjSZFKXXcGOVXa_!!0-item_pic.jpg', '1221', '34113', '2498.00');
INSERT INTO `phone_info` VALUES ('541929707682', '71799145', '【6期免息】vivo XPlay6 曲面屏双摄6G运存全网通智能手机', 'https://detail.m.tmall.com/item.htm?id=541929707682', '//img.alicdn.com/bao/uploaded/i1/883737303/TB1nzkUbHsrBKNjSZFpXXcXhFXa_!!0-item_pic.jpg', '485', '20091', '3498.00');
INSERT INTO `phone_info` VALUES ('539365805409', '71799145', '【购机有礼】vivo Y55全网通4G智能拍照正品手机vivoy55vivo Y55A', 'https://detail.m.tmall.com/item.htm?id=539365805409', '//img.alicdn.com/bao/uploaded/i4/883737303/TB1hSn3gY5YBuNjSspoXXbeNFXa_!!0-item_pic.jpg', '1274', '30884', '999.00');
INSERT INTO `phone_info` VALUES ('539133784537', '71799145', '【3期免息】vivo y67全网通指纹识别美颜拍照4G智能手机vivoY67', 'https://detail.m.tmall.com/item.htm?id=539133784537', '//img.alicdn.com/bao/uploaded/i4/883737303/TB1ah6Hg7OWBuNjSsppXXXPgpXa_!!0-item_pic.jpg', '607', '53812', '1598.00');
INSERT INTO `phone_info` VALUES ('542949246497', '71799145', '【购机有礼】vivo y66全网通美颜拍照智能4G手机官方正品vivo66', 'https://detail.m.tmall.com/item.htm?id=542949246497', '//img.alicdn.com/bao/uploaded/i2/883737303/TB1QBY.g4WYBuNjy1zkXXXGGpXa_!!0-item_pic.jpg', '479', '93081', '1198.00');
INSERT INTO `phone_info` VALUES ('559249313163', '71799145', '【6期免息】vivo X20plus新年礼盒全面屏智能4G全网通手机plus', 'https://detail.m.tmall.com/item.htm?id=559249313163', '//img.alicdn.com/bao/uploaded/i2/883737303/TB14nwQbHArBKNjSZFLXXc_dVXa_!!0-item_pic.jpg', '100', '3365', '3198.00');
INSERT INTO `phone_info` VALUES ('563365981702', '71799145', '【购机有礼】vivo X20全面屏面部识别4G全网通智能手机vivox20', 'https://detail.m.tmall.com/item.htm?id=563365981702', '//img.alicdn.com/bao/uploaded/i4/883737303/TB1lJD6gY5YBuNjSspoXXbeNFXa_!!0-item_pic.jpg', '183', '535', '3198.00');
INSERT INTO `phone_info` VALUES ('541888888509', '72217984', '【爆款直降100元】OPPO A57全网通前置1600万指纹识别拍照手机', 'https://detail.m.tmall.com/item.htm?id=541888888509', '//img.alicdn.com/bao/uploaded/i1/901409638/TB1CFRAcbuWBuNjSszgXXb8jVXa_!!0-item_pic.jpg', '9759', '174317', '1099.00');
INSERT INTO `phone_info` VALUES ('560372057846', '72217984', '【直降100元】OPPO R11S新年版前后2000万全面屏拍照手机oppor11s', 'https://detail.m.tmall.com/item.htm?id=560372057846', '//img.alicdn.com/bao/uploaded/i4/901409638/TB1JgbbcmBYBeNjy0FeXXbnmFXa_!!0-item_pic.jpg', '5555', '70859', '2799.00');
INSERT INTO `phone_info` VALUES ('563382155465', '72217984', '【1日10点直降100元】OPPO A83全面屏4GB+32GB拍照4G手机oppoa83', 'https://detail.m.tmall.com/item.htm?id=563382155465', '//img.alicdn.com/bao/uploaded/i2/901409638/TB1dijzcntYBeNjy1XdXXXXyVXa_!!0-item_pic.jpg', '5188', '20349', '1299.00');
INSERT INTO `phone_info` VALUES ('561770065203', '72217984', '【领券减100】OPPO A79前后1600万全面屏闪充拍照4G手机oppoa79', 'https://detail.m.tmall.com/item.htm?id=561770065203', '//img.alicdn.com/bao/uploaded/i3/901409638/TB1Yo4IceuSBuNjy1XcXXcYjFXa_!!0-item_pic.jpg', '2454', '9473', '2099.00');
INSERT INTO `phone_info` VALUES ('561570639641', '72217984', '【直降400元】OPPO R11s Plus前后2000万全面屏拍照手机r11splus', 'https://detail.m.tmall.com/item.htm?id=561570639641', '//img.alicdn.com/bao/uploaded/i4/901409638/TB1SqGGdNGYBuNjy0FnXXX5lpXa_!!0-item_pic.jpg', '1687', '11079', '3299.00');
INSERT INTO `phone_info` VALUES ('562730169870', '72217984', '【高配版上市】OPPO A73超清全面屏前置1600万拍照4G手机oppoa73', 'https://detail.m.tmall.com/item.htm?id=562730169870', '//img.alicdn.com/bao/uploaded/i4/901409638/TB1tN0Och9YBuNjy0FfXXXIsVXa_!!0-item_pic.jpg', '2093', '8784', '1799.00');
INSERT INTO `phone_info` VALUES ('565573818599', '72217984', '【新品开售】OPPO R15 超视野全面屏 智能拍照手机oppor15', 'https://detail.m.tmall.com/item.htm?id=565573818599', '//img.alicdn.com/bao/uploaded/i1/901409638/TB2HFYNhFuWBuNjSspnXXX1NVXa_!!901409638-0-item_pic.jpg', '10419', '12326', '2999.00');
INSERT INTO `phone_info` VALUES ('565385888478', '72217984', '【新品开售】OPPO R15梦镜版超视野全面屏智能拍照手机oppor15', 'https://detail.m.tmall.com/item.htm?id=565385888478', '//img.alicdn.com/bao/uploaded/i3/901409638/TB2FnTPhL9TBuNjy1zbXXXpepXa_!!901409638-0-item_pic.jpg', '8894', '10568', '3299.00');
INSERT INTO `phone_info` VALUES ('560538155798', '72217984', '【直降100元】OPPO R11S新年版全面屏拍照4G手机oppor11s r11s', 'https://detail.m.tmall.com/item.htm?id=560538155798', '//img.alicdn.com/bao/uploaded/i1/901409638/TB1aZxmcgmTBuNjy1XbXXaMrVXa_!!0-item_pic.jpg', '850', '28123', '2799.00');
INSERT INTO `phone_info` VALUES ('546337019338', '72217984', '【爆款直降100元】OPPO A57黑色前置1600万指纹识别拍照手机', 'https://detail.m.tmall.com/item.htm?id=546337019338', '//img.alicdn.com/bao/uploaded/i3/901409638/TB1c6_hcmtYBeNjSspaXXaOOFXa_!!0-item_pic.jpg', '1407', '9084', '1099.00');
INSERT INTO `phone_info` VALUES ('565788240706', '72217984', '【新品开售】OPPO A1 4+64GB大内存全面屏人脸识别手机oppoa1', 'https://detail.m.tmall.com/item.htm?id=565788240706', '//img.alicdn.com/bao/uploaded/i3/901409638/TB1S8EjbqQoBKNjSZJnXXaw9VXa_!!0-item_pic.jpg', '0', '1083', '1399.00');
INSERT INTO `phone_info` VALUES ('562553130709', '104736810', 'Xiaomi/小米 红米5 plus千元全面屏骁龙学生智能机拍照自拍手机5P', 'https://detail.m.tmall.com/item.htm?id=562553130709', '//img.alicdn.com/bao/uploaded/i3/1714128138/TB1SEaabWmWBuNkHFJHXXaatVXa_!!0-item_pic.jpg', '58854', '282684', '999.00');
INSERT INTO `phone_info` VALUES ('558208723934', '104736810', 'Xiaomi/小米 小米NOTE 3拍照自拍大屏蓝note3游戏商务智能手机', 'https://detail.m.tmall.com/item.htm?id=558208723934', '//img.alicdn.com/bao/uploaded/i4/1714128138/TB1Rt28hNSYBuNjSspjXXX73VXa_!!0-item_pic.jpg', '16299', '115249', '1799.00');
INSERT INTO `phone_info` VALUES ('560135062971', '104736810', 'Xiaomi/小米 红米5A新品老人机拍照官网性比价高小巧简约智能手机', 'https://detail.m.tmall.com/item.htm?id=560135062971', '//img.alicdn.com/bao/uploaded/i2/1714128138/TB1pjzXbYorBKNjSZFjXXc_SpXa_!!0-item_pic.jpg', '25390', '219512', '599.00');
INSERT INTO `phone_info` VALUES ('541222089489', '104736810', 'Xiaomi/小米 红米手机4A超长待机学生分期降价经典老年直板智能机', 'https://detail.m.tmall.com/item.htm?id=541222089489', '//img.alicdn.com/bao/uploaded/i4/1714128138/TB1x6IybYsrBKNjSZFpXXcXhFXa_!!0-item_pic.jpg', '66133', '1314570', '549.00');
INSERT INTO `phone_info` VALUES ('555589089023', '104736810', 'Xiaomi/小米 小米5X指纹解锁经典时尚官方正品大屏智能拍照手机', 'https://detail.m.tmall.com/item.htm?id=555589089023', '//img.alicdn.com/bao/uploaded/i4/1714128138/TB1VMoyhoR1BeNjy0FmXXb0wVXa_!!0-item_pic.jpg', '18194', '324419', '1499.00');
INSERT INTO `phone_info` VALUES ('557348439362', '104736810', 'Xiaomi/小米 红米NOTE 5A超长待机5.5英寸大屏智能美颜拍照手机', 'https://detail.m.tmall.com/item.htm?id=557348439362', '//img.alicdn.com/bao/uploaded/i2/1714128138/TB10SQMhCtYBeNjSspkXXbU8VXa_!!0-item_pic.jpg', '16782', '186276', '669.00');
INSERT INTO `phone_info` VALUES ('562390304003', '104736810', 'Xiaomi/小米 红米5新款全面屏青春学生机超长待机薄游戏智能手机', 'https://detail.m.tmall.com/item.htm?id=562390304003', '//img.alicdn.com/bao/uploaded/i3/1714128138/TB1X0zzhk9WBuNjSspeXXaz5VXa_!!0-item_pic.jpg', '12556', '63409', '799.00');
INSERT INTO `phone_info` VALUES ('549049522944', '104736810', 'Xiaomi/小米 小米手机6变焦双摄正品官方大内存商务拍照智能手机', 'https://detail.m.tmall.com/item.htm?id=549049522944', '//img.alicdn.com/bao/uploaded/i4/1714128138/TB1IOAyhoR1BeNjy0FmXXb0wVXa_!!0-item_pic.jpg', '22613', '341062', '2299.00');
INSERT INTO `phone_info` VALUES ('557759288520', '104736810', 'Xiaomi/小米 小米mix 2全面屏5.99英寸大屏幕商务骁龙835智能手机', 'https://detail.m.tmall.com/item.htm?id=557759288520', '//img.alicdn.com/bao/uploaded/i1/1714128138/TB1EpzJhFuWBuNjSspnXXX1NVXa_!!0-item_pic.jpg', '7780', '68655', '2999.00');
INSERT INTO `phone_info` VALUES ('551744205393', '104736810', 'Xiaomi/小米 小米max2平板智能6.44英寸屏幕大电量全网通游戏手机', 'https://detail.m.tmall.com/item.htm?id=551744205393', '//img.alicdn.com/bao/uploaded/i3/1714128138/TB1LqOXbYZnBKNjSZFKXXcGOVXa_!!0-item_pic.jpg', '6905', '173932', '1399.00');
INSERT INTO `phone_info` VALUES ('558353183430', '104736810', 'Xiaomi/小米 小米NOTE 3 手机全网通智能手机小米官拍照旗舰手机', 'https://detail.m.tmall.com/item.htm?id=558353183430', '//img.alicdn.com/bao/uploaded/i4/1714128138/TB15xnObWAoBKNjSZSyXXaHAVXa_!!0-item_pic.jpg', '3351', '27098', '1799.00');
INSERT INTO `phone_info` VALUES ('552307331062', '104736810', 'Xiaomi/小米 小米Max2 4+64G/32G/128G全网通大屏大电量智能手机', 'https://detail.m.tmall.com/item.htm?id=552307331062', '//img.alicdn.com/bao/uploaded/i2/1714128138/TB1kZjxhmCWBuNjy0FhXXb6EVXa_!!0-item_pic.jpg', '692', '7321', '1399.00');
INSERT INTO `phone_info` VALUES ('560808788200', '104736810', 'Xiaomi/小米 小米mix 2全陶瓷尊享版全面屏手机MXI2智能手机大屏', 'https://detail.m.tmall.com/item.htm?id=560808788200', '//img.alicdn.com/bao/uploaded/i3/1714128138/TB1re0bhCBYBeNjy0FeXXbnmFXa_!!0-item_pic.jpg', '897', '5120', '4299.00');
INSERT INTO `phone_info` VALUES ('563114770766', '104736810', '小米 红米5 Plus 钢化玻璃贴膜 标准高透贴膜', 'https://detail.m.tmall.com/item.htm?id=563114770766', '//img.alicdn.com/bao/uploaded/i2/1714128138/TB1sazYjhHI8KJjy1zbXXaxdpXa_!!0-item_pic.jpg', '839', '3150', '19.00');
INSERT INTO `phone_info` VALUES ('566080658196', '104736810', 'Xiaomi/小米 红米note5 标准高透贴膜极清高透防指纹全机身保护膜', 'https://detail.m.tmall.com/item.htm?id=566080658196', '//img.alicdn.com/bao/uploaded/i2/1714128138/TB13B4Fd1uSBuNjSsplXXbe8pXa_!!0-item_pic.jpg', '325', '362', '19.00');
INSERT INTO `phone_info` VALUES ('565832414291', '104736810', '小米MIX2标准高透贴膜 高透光高硬度零延迟原厂原装高还原', 'https://detail.m.tmall.com/item.htm?id=565832414291', '//img.alicdn.com/bao/uploaded/i3/1714128138/TB1mRM_c1uSBuNjSsziXXbq8pXa_!!0-item_pic.jpg', '205', '239', '39.00');
INSERT INTO `phone_info` VALUES ('563049977512', '104736810', '小米 红米5 plus防摔保护套保护套 纯色', 'https://detail.m.tmall.com/item.htm?id=563049977512', '//img.alicdn.com/bao/uploaded/i4/1714128138/TB1unAujnnI8KJjy0FfXXcdoVXa_!!0-item_pic.jpg', '308', '1100', '39.00');
INSERT INTO `phone_info` VALUES ('566154063552', '104736810', '小米 红米note 5 极简防摔保护壳男款女款硅胶原厂韩式保护套', 'https://detail.m.tmall.com/item.htm?id=566154063552', '//img.alicdn.com/bao/uploaded/i3/1714128138/TB1IE3WaFkoBKNjSZFkXXb4tFXa_!!0-item_pic.jpg', '176', '184', '39.00');
INSERT INTO `phone_info` VALUES ('565759425609', '104736810', '小米Note 3 硅胶保护套 硅胶防摔软手感极佳简约清新商务便携保护', 'https://detail.m.tmall.com/item.htm?id=565759425609', '//img.alicdn.com/bao/uploaded/i2/1714128138/TB1sMNfdb5YBuNjSspoXXbeNFXa_!!0-item_pic.jpg', '102', '108', '49.00');
INSERT INTO `phone_info` VALUES ('563044713387', '104736810', '小米 红米5标准高透贴膜', 'https://detail.m.tmall.com/item.htm?id=563044713387', '//img.alicdn.com/bao/uploaded/i4/1714128138/TB1C0vQjcjI8KJjSsppXXXbyVXa_!!0-item_pic.jpg', '135', '568', '19.00');
INSERT INTO `phone_info` VALUES ('563191399445', '104736810', '小米 红米5保护套保护壳防摔抗污 纯色', 'https://detail.m.tmall.com/item.htm?id=563191399445', '//img.alicdn.com/bao/uploaded/i4/1714128138/TB1yH7ljf6H8KJjSspmXXb2WXXa_!!0-item_pic.jpg', '71', '330', '29.00');
INSERT INTO `phone_info` VALUES ('559441419648', '101717810', '【最高省200】华为honor/荣耀 畅玩7X全网通全面屏手机官方旗舰店', 'https://detail.m.tmall.com/item.htm?id=559441419648', '//img.alicdn.com/bao/uploaded/i3/1114511827/TB2rhP3hKySBuNjy1zdXXXPxFXa_!!1114511827-0-item_pic.jpg', '43264', '640969', '1249.00');
INSERT INTO `phone_info` VALUES ('562948989464', '101717810', '[最高省200]华为honor/荣耀 荣耀9青春版全面屏手机7x官方旗舰店', 'https://detail.m.tmall.com/item.htm?id=562948989464', '//img.alicdn.com/bao/uploaded/i3/1114511827/TB28xUihH9YBuNjy0FgXXcxcXXa_!!1114511827-0-item_pic.jpg', '30780', '143455', '1099.00');
INSERT INTO `phone_info` VALUES ('552919553653', '101717810', '【低至1899】华为honor/荣耀 荣耀9智能全网通手机官方旗舰V10', 'https://detail.m.tmall.com/item.htm?id=552919553653', '//img.alicdn.com/bao/uploaded/i1/1114511827/TB1G7PKb5QnBKNjSZFmXXcApVXa_!!0-item_pic.jpg', '20498', '405397', '1899.00');
INSERT INTO `phone_info` VALUES ('562003579553', '101717810', '【限时直降】华为honor/荣耀 荣耀V10全面屏智能手机官方旗舰店', 'https://detail.m.tmall.com/item.htm?id=562003579553', '//img.alicdn.com/bao/uploaded/i4/1114511827/TB2dF2ihQKWBuNjy1zjXXcOypXa_!!1114511827-0-item_pic.jpg', '26951', '131707', '2499.00');
INSERT INTO `phone_info` VALUES ('565264660443', '101717810', '新品华为honor/荣耀 畅玩7C全面屏手机智能手机官方旗舰店正品7X', 'https://detail.m.tmall.com/item.htm?id=565264660443', '//img.alicdn.com/bao/uploaded/i4/1114511827/TB1SAumhCtYBeNjSspaXXaOOFXa_!!0-item_pic.jpg', '35998', '37860', '899.00');
INSERT INTO `phone_info` VALUES ('557901899994', '101717810', '【直降50】华为honor/荣耀 畅玩6全网通老人手机官方旗舰店', 'https://detail.m.tmall.com/item.htm?id=557901899994', '//img.alicdn.com/bao/uploaded/i1/1114511827/TB12c_Ib8jTBKNjSZFwXXcG4XXa_!!0-item_pic.jpg', '13305', '290213', '549.00');
INSERT INTO `phone_info` VALUES ('563074125414', '101717810', '[最高省200]华为honor/荣耀 荣耀9青春版全面屏手机7x官方旗舰店8', 'https://detail.m.tmall.com/item.htm?id=563074125414', '//img.alicdn.com/bao/uploaded/i4/1114511827/TB2rLDDhSCWBuNjy0FhXXb6EVXa_!!1114511827-0-item_pic.jpg', '16314', '24623', '1099.00');
INSERT INTO `phone_info` VALUES ('562048649686', '101717810', '【限时特惠】华为honor/荣耀 荣耀V10全面屏手机智能官方旗舰店', 'https://detail.m.tmall.com/item.htm?id=562048649686', '//img.alicdn.com/bao/uploaded/i2/1114511827/TB2G8b.hNWYBuNjy1zkXXXGGpXa_!!1114511827-0-item_pic.jpg', '8196', '22852', '2499.00');
INSERT INTO `phone_info` VALUES ('565622721123', '101717810', '新品华为honor/荣耀 畅玩7C全面屏手机智能手机官方旗舰店正品7X', 'https://detail.m.tmall.com/item.htm?id=565622721123', '//img.alicdn.com/bao/uploaded/i3/1114511827/TB1WFA_heuSBuNjSsziXXbq8pXa_!!0-item_pic.jpg', '5235', '5505', '899.00');
INSERT INTO `phone_info` VALUES ('552856496808', '101717810', '【低至1899】华为honor/荣耀 荣耀9全网通智能手机正品官方', 'https://detail.m.tmall.com/item.htm?id=552856496808', '//img.alicdn.com/bao/uploaded/i1/1114511827/TB17meShTtYBeNjy1XdXXXXyVXa_!!0-item_pic.jpg', '2918', '47021', '1899.00');
INSERT INTO `phone_info` VALUES ('552856804867', '101717810', '【低至2399】华为honor/荣耀 荣耀9全网通标配/高配/尊享手机', 'https://detail.m.tmall.com/item.htm?id=552856804867', '//img.alicdn.com/bao/uploaded/i1/1114511827/TB1WGDIb5MnBKNjSZFzXXc_qVXa_!!0-item_pic.jpg', '1779', '28555', '2399.00');
INSERT INTO `phone_info` VALUES ('559858981500', '101717810', '【最高可省200】华为honor/荣耀 畅玩7X全网通全面屏官方手机', 'https://detail.m.tmall.com/item.htm?id=559858981500', '//img.alicdn.com/bao/uploaded/i3/1114511827/TB2TH.ihH9YBuNjy0FgXXcxcXXa_!!1114511827-0-item_pic.jpg', '1406', '63298', '1249.00');
INSERT INTO `phone_info` VALUES ('558113781705', '101717810', '【直降50】华为honor/荣耀 畅玩6全网通学生手机官方旗舰店', 'https://detail.m.tmall.com/item.htm?id=558113781705', '//img.alicdn.com/bao/uploaded/i4/1114511827/TB1n8ZThr1YBuNjSszhXXcUsFXa_!!0-item_pic.jpg', '1614', '77825', '549.00');
INSERT INTO `phone_info` VALUES ('561008172632', '101717810', '【包邮】美逸华为honor/荣耀畅玩7X钢化膜全屏覆盖手机保护贴膜', 'https://detail.m.tmall.com/item.htm?id=561008172632', '//img.alicdn.com/bao/uploaded/i4/1114511827/TB1r6RgjmfD8KJjSszhXXbIJFXa_!!0-item_pic.jpg', '827', '6498', '39.00');
INSERT INTO `phone_info` VALUES ('560660374556', '101717810', 'honor/荣耀 荣耀9 移动4G+版 全网通高配6G+64G', 'https://detail.m.tmall.com/item.htm?id=560660374556', '//img.alicdn.com/bao/uploaded/i4/1114511827/TB1CNTLb26H8KJjy0FjXXaXepXa_!!0-item_pic.jpg', '11', '31', '2699.00');
INSERT INTO `phone_info` VALUES ('558468474286', '101717810', '华为 honor/荣耀 畅玩6保护壳商务手机壳官方正品防摔', 'https://detail.m.tmall.com/item.htm?id=558468474286', '//img.alicdn.com/bao/uploaded/i3/1114511827/TB16mwlfXcJL1JjSZFOXXcWlXXa_!!2-item_pic.png', '102', '430', '39.00');
INSERT INTO `phone_info` VALUES ('554919155557', '150920153', '【抢天猫券减100领券再减100】Huawei/华为 畅享7 32G 全网通手机', 'https://detail.m.tmall.com/item.htm?id=554919155557', '//img.alicdn.com/bao/uploaded/i3/2838892713/TB2Cw0Qh3mTBuNjy1XbXXaMrVXa_!!2838892713-0-item_pic.jpg', '41378', '350288', '999.00');
INSERT INTO `phone_info` VALUES ('562798601815', '150920153', '【抢天猫券减100领券再减100】Huawei/华为 畅享7S 64GB 智能手机', 'https://detail.m.tmall.com/item.htm?id=562798601815', '//img.alicdn.com/bao/uploaded/i2/2838892713/TB2.UeahVGWBuNjy0FbXXb4sXXa_!!2838892713-0-item_pic.jpg', '17668', '50140', '1699.00');
INSERT INTO `phone_info` VALUES ('562335315406', '150920153', '【最高直降300】Huawei/华为 nova 2s 全面屏四镜头官方正品手机', 'https://detail.m.tmall.com/item.htm?id=562335315406', '//img.alicdn.com/bao/uploaded/i4/2838892713/TB2QULXhCBYBeNjy0FeXXbnmFXa_!!2838892713-0-item_pic.jpg', '15608', '63744', '2599.00');
INSERT INTO `phone_info` VALUES ('549098235923', '150920153', '【抢天猫券减100领券再减100】Huawei/华为 畅享7 Plus 高配 手机', 'https://detail.m.tmall.com/item.htm?id=549098235923', '//img.alicdn.com/bao/uploaded/i1/2838892713/TB29VyChY5YBuNjSspoXXbeNFXa_!!2838892713-0-item_pic.jpg', '7665', '171272', '1499.00');
INSERT INTO `phone_info` VALUES ('560952413462', '150920153', '【抢天猫券减100领券再减100】Huawei/华为 Mate 10 Pro 智能手机', 'https://detail.m.tmall.com/item.htm?id=560952413462', '//img.alicdn.com/bao/uploaded/i1/2838892713/TB2Z2Wdh7OWBuNjSsppXXXPgpXa_!!2838892713-0-item_pic.jpg', '5767', '85887', '4899.00');
INSERT INTO `phone_info` VALUES ('560065171365', '150920153', '【抢天猫券减100领券再减100】Huawei/华为 Mate 10 6G+128G 手机', 'https://detail.m.tmall.com/item.htm?id=560065171365', '//img.alicdn.com/bao/uploaded/i3/2838892713/TB2e8dShYSYBuNjSspiXXXNzpXa_!!2838892713-0-item_pic.jpg', '4907', '73356', '4499.00');
INSERT INTO `phone_info` VALUES ('559845752539', '150920153', '【抢天猫券减100领券再减100】Huawei/华为 Mate 10 4G+64G 手机', 'https://detail.m.tmall.com/item.htm?id=559845752539', '//img.alicdn.com/bao/uploaded/i2/2838892713/TB2_y1FhY1YBuNjSszhXXcUsFXa_!!2838892713-0-item_pic.jpg', '3529', '56425', '3899.00');
INSERT INTO `phone_info` VALUES ('558760588039', '150920153', '【领券减200】Huawei/华为 麦芒6 官方正品4G手机', 'https://detail.m.tmall.com/item.htm?id=558760588039', '//img.alicdn.com/bao/uploaded/i4/2838892713/TB2IjGCh1uSBuNjSsziXXbq8pXa_!!2838892713-0-item_pic.jpg', '3966', '37777', '2199.00');
INSERT INTO `phone_info` VALUES ('566146837804', '150920153', '【3期免息】Huawei/华为 nova 3e 4G全面屏自然美妆正品智能手机', 'https://detail.m.tmall.com/item.htm?id=566146837804', '//img.alicdn.com/bao/uploaded/i1/2838892713/TB2PlJ5hmBYBeNjy0FeXXbnmFXa_!!2838892713-0-item_pic.jpg', '16677', '18283', '1999.00');
INSERT INTO `phone_info` VALUES ('566603286049', '150920153', '【定金999元火爆预售中】Huawei/华为 P20 4G全面屏徕卡双摄手机', 'https://detail.m.tmall.com/item.htm?id=566603286049', '//img.alicdn.com/bao/uploaded/i1/2838892713/TB2eOjggVuWBuNjSspnXXX1NVXa_!!2838892713-0-item_pic.jpg', '1005', '1152', '9999.00');
INSERT INTO `phone_info` VALUES ('566605082411', '150920153', '【定金999元火爆预售中】Huawei/华为 P20 Pro 4G全面屏手机', 'https://detail.m.tmall.com/item.htm?id=566605082411', '//img.alicdn.com/bao/uploaded/i1/2838892713/TB2A0bJgWmWBuNjy1XaXXXCbXXa_!!2838892713-0-item_pic.jpg', '5462', '5763', '9999.00');
INSERT INTO `phone_info` VALUES ('566826119103', '150920153', '【预定专享 立省50元】Huawei/华为 畅享8 Plus 全面屏正品手机', 'https://detail.m.tmall.com/item.htm?id=566826119103', '//img.alicdn.com/bao/uploaded/i2/2838892713/TB2qaM9hkCWBuNjy0FaXXXUlXXa_!!2838892713-0-item_pic.jpg', '690', '1045', '1699.00');