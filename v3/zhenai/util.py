# -*-coding:utf-8-*-

f = open('city.txt')

content = f.read()

citys = content.split(",")

city_code_map = {}

for i in range(len(citys) - 1):
    city = citys[i + 1]
    city = city.replace("c", "").replace("\"", "").replace("{n", "").replace("}", "")
    arr = city.split("::")
    city_code_map[arr[1]] = arr[0]

print(city_code_map)
