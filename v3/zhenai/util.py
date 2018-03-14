# -*-coding:utf-8-*-

import csv

f = open('city.txt')

city_code_map = {}
for line in f.readlines():
    citys = line.split(",")
    for i in range(len(citys) - 1):
        city = citys[i + 1]
        city = city.replace("c", "").replace("\"", "").replace("{n", "").replace("}", "")
        arr = city.split("::")
        try:
            city_code_map[arr[1]] = arr[0]
        except Exception as e:
            print(e)

# 打开文件，追加a
out = open('out_csv.csv', 'a', newline='')
# 设定写入模式
csv_write = csv.writer(out, dialect='excel')

csv_file = csv.reader(open("area_info.csv", "r"))
for obj in csv_file:
    for d, x in city_code_map.items():
        if d in obj[1]:
            obj.append(x)
    csv_write.writerow(obj)
