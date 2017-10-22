# -*-coding:utf8-*-

import sys
from database.mysql import MySQL
import jieba
import json

reload(sys)
sys.setdefaultencoding('utf-8')


def check_contain_chinese(check_str):
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

ignore_word = ["成功"]

MySQLClient = MySQL()
count = 0
while True:
    resList = MySQLClient.fetchmany("select * from JUGEMENT WHERE WORDS is null LIMIT " + str(count * 5000) + ",5000")
    if resList is None or len(resList) == 0:
        break
    for res in resList:
        seg_list = jieba.cut(res[2])
        new_list = []
        print res[0]
        for word in seg_list:
            if check_contain_chinese(word) and word not in ignore_word:
                new_list.append(word)
        sql = "UPDATE JUGEMENT SET WORDS='" + " ".join(new_list) + "' WHERE ID='" + res[0] + "'"  # 执行sql语句
        MySQLClient.update(sql)
    count = count + 1
