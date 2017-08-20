# -*-coding:utf8-*-

from pyExcelerator import *
import sys
from database.mysql import MySQL
import math

reload(sys)

sys.setdefaultencoding('utf-8')

MySQLClient = MySQL()
count = 0
filename = "export-" + str(count) + ".xls"
w = Workbook()
ws = w.add_sheet("sheet1")
while True:
    sql = "select * from JUGEMENT WHERE CONTENT != '""' LIMIT " + str(count * 5000) + ",5000"
    info = MySQLClient.fetchmany(sql)
    row = -1
    for ii in info:
        try:
            row = row + 1
            ws.write(row, 0, ii[0])
            ws.write(row, 1, ii[1])
            data = ii[2].decode('utf8')
            size = math.ceil(len(data) / 2000)
            if size > 1:
                for j in range(int(size)):
                    ws.write(row, 2 + j, data[j * 2000:(j + 1) * 2000])
            else:
                ws.write(row, 2, ii[2].decode('utf8'))
        except:
            ws.write(row, 0, "")
            ws.write(row, 1, "")
            ws.write(row, 2, "")
    print(filename)
    w.save(filename)  # 保存
    count = count + 1
    if len(info) >= 5000:
        filename = "export-" + str(count) + ".xls"
        w = Workbook()
        ws = w.add_sheet("sheet1")
    else:
        break
MySQLClient.close()
