#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys

from v2.database.mysql import MySQL

MySQLClient = MySQL()

reload(sys)
sys.setdefaultencoding('utf-8')

ignore_words = ["我", "你", "他", "她", "的", "地", "月", "年", "在"]
if __name__ == "__main__":

    word_dict = {}
    count = 0

    while True:
        word_lst = []
        print "正在获取分词数据..."
        resList = MySQLClient.fetchmany(
            "select WORDS from JUGEMENT WHERE WORDS is not null LIMIT " + str(count * 5000) + ",5000")
        if resList is None or len(resList) == 0:
            print "计算完成，正在整理输出词频结果..."
            break
        for res in resList:
            word_lst.extend(res[0].split(" "))
        count = count + 1
        print "已经成功获取" + str(count * 5000) + "条数据"

        print "正在计算词频..."
        for item in word_lst:
            if item not in word_dict:  # 统计数量
                word_dict[item] = 1
            else:
                word_dict[item] += 1

    sorted_dict = sorted(word_dict.items(), key=lambda d: d[1], reverse=True)
    filename = "wordcount.txt"
    fs = open(filename, "w+")
    for i in range(len(sorted_dict)):
        key = sorted_dict[i][0]
        value = sorted_dict[i][1]
        if key is not None and len(key) > 0 and key not in ignore_words:
            fs.write(str(key.decode('utf8')) + ":" + str(value) + "\r")
    fs.close()
    print "词频计算完成，结果请查看" + filename
