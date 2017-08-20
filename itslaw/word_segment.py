# -*-coding:utf8-*-

import sys
from database.mysql import MySQL
import jieba
import json

reload(sys)
sys.setdefaultencoding('utf-8')

MySQLClient = MySQL()
res = MySQLClient.fetchone("select * from JUGEMENT WHERE CONTENT != ''")
# print(res[2].decode('utf8'))
print(json.loads(res[2])['data']['fullJudgement']['caseNumber'])

# text = "本案中，被异议商标与第3092461号“杜拉维特”商标（简称引证商标）构成近似商标。被异议商标指定使用的“盥洗台（家具）、浴室用支架（家具）”商品与引证商标核定使用的“澡盆、沐浴用设备”等商品在《类似商品和服务区分表》中划分为不同的大类，但上述商品均属卫浴用品或日常生活用品，在功能用途、销售渠道、消费群体等方面基本相同且关联性较强。被异议商标与引证商标分别使用在“盥洗台（家具）、浴室用支架（家具）”等及“澡盆、沐浴用设备”等商品上，客观上容易造成相关公众认为商品是同一主体提供的，或者其提供者之间存在特定联系。被异议商标与引证商标构成类似商品上的相同商标，不应予以核准注册。商标评审委员会相关认定错误，依法应予纠正"
# seg_list = jieba.cut(text)
# print "Default Mode:", '，'.join(seg_list)
