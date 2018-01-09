# -*-coding:utf8-*-

import sys
import json
import time
import urllib
import os
import requests
import threadpool
from database.mysql import MySQL

reload(sys)

sys.setdefaultencoding('utf-8')

MySQLClient = MySQL()
MySQLClient.set_table("guidestar")

head = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'ASP.NET_SessionId=j1nnkwzpqaypnq5kcaznqyxw; _vwo_uuid_v2=CF82AEDFCF3A07291CAD602214800A38|3fae756324fbb19989d68cf9c76496d9; ki_r=; D_IID=94834CDF-C931-3064-B649-41961E3BA689; D_UID=23AF5DAB-95A9-3D5C-8EA2-51C863072D66; D_ZID=97A1EF18-AB6A-37DA-9565-8A7EE917CE19; D_ZUID=DA852CA1-6D8F-30F7-82BD-00D31C90B04F; D_HID=A4B35261-78D7-30A5-B57D-39044DA0BB43; D_SID=218.106.154.158:NrtZxzJf/+Hp+nLBPX4cr5f/6dyOSWUhBj7c1p1nr0Q; _bizo_bzid=35dec6bc-3cc3-4300-9a49-bbd77eb92db3; _bizo_cksm=90E4D32BE01356B3; __hssrc=1; hubspotutk=2685ce170e2683a593dfe0ec91c26ddf; messagesUtk=2685ce170e2683a593dfe0ec91c26ddf; _ga=GA1.2.1002349185.1515415595; _gid=GA1.2.581669412.1515415595; __hstc=126119634.2685ce170e2683a593dfe0ec91c26ddf.1515414630692.1515414630692.1515467274027.2; _bizo_np_stats=; __atuvc=4%7C2; today=1; .gifAuth=8C2BB863824BA5C8206368BB8263C0FAFCF364B1461CD14DA0CF3FE176FEB66AE432B0BEB917137B142C9E12F2487B827F791E3F6150AE2ADA1ED292B1BD1BD57CCA66D84639930A257CE3FAF33886FAC3CA3625734C9FEDFBBD4DDE77AB77D32E131C23E7003594131020E4; NOPCOMMERCE.AUTH=47BF8E5D34189E8BB19895D52BFA8D78202744A58463E28154477CEAB9422E9A4B4BEA866FDE9139D3456CFD17D783CB76BD5955355476D4EB31D2AAA161042B6E30485762D1235B34D1E9CAF3226F925C7A7FC01CE2C444073FE75271601D74392B17B341AC814EFC14ED6DF4BBD6624429BB977E2D49E934DC56E5; Nop.customer=5e5e1df6-de0b-45dd-a640-3e99e58e5aa3; ki_t=1515414415903%3B1515467252882%3B1515473026982%3B2%3B22; mp_5d9e4f46acaba87f5966b8c0d2e47e6e_mixpanel=%7B%22distinct_id%22%3A%20%22663973866%40qq.com%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpap%22%3A%20%5B%5D%7D; mp_mixpanel__c=0',
    'Cookie': 'D_IID=AAAEEF6A-031B-33E8-B2EB-201C9EB49D90; D_UID=E2845C1C-9D7C-3AE0-8D2F-A5C9136E6A1B; D_ZID=052B2157-541D-379D-B4EE-448BF2A6DA23; D_ZUID=9F26DC9F-C7D3-3F3E-8A79-BBF69762A014; D_HID=73469430-BC34-38D2-8EFC-5F3A99C079E6; D_SID=218.106.154.158:NrtZxzJf/+Hp+nLBPX4cr5f/6dyOSWUhBj7c1p1nr0Q; ASP.NET_SessionId=rnmij2q2cc3s3hb515gfxgh1; _vwo_uuid_v2=3701861DA48A2B56D1D5EFE23F7D7D9F|35580c5b8b3c3e1d6fa5c0ec8954eaaf; ki_t=1515492058662%3B1515492058662%3B1515492169144%3B1%3B3; ki_r=; mp_mixpanel__c=0; today=1; .gifAuth=6EAB4F1FB6104AE64C4983C2013CFDFC9CD53A9D72336181D284B06408790AF387BC93DE560ED3065BF72C2E1BDC42A336C0F739EC3908AE6113BF67B7DC8C06BF1A07CA51E758F7C9485ED5261FDB6EA79E5E6A8C73E68B589B8A2D7AD257171E73E83CC6C5A913977ABADD; NOPCOMMERCE.AUTH=E68C2CAE98974078B436B9858F5F96EAD3AB4A3365BC80D4D299DDBC3CBE4EB9AD024A9C25A2022E0AEA2ECC989D76EB85215F2A53FFBC9250EC781FEB31FDF95487F02D98D19BA91BB585FFF0C1A1240260CE1C204A0646C007F65BE1C560ECF28800F5E81EB4EBA012EF66052E09C0D6E0860D1E7F2C90F406F84F; Nop.customer=f69798b7-ce73-4844-a891-1559c9647f0a; mp_5d9e4f46acaba87f5966b8c0d2e47e6e_mixpanel=%7B%22distinct_id%22%3A%20%221025711995%40qq.com%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpap%22%3A%20%5B%5D%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D',
    'Host': 'www.guidestar.org',
    'Origin': 'https://www.guidestar.org',
    'Pragma': 'no-cache',
    'Referer': 'https://www.guidestar.org/search',
    'User-Agent': 'Mozilla/5.0 (Macintoshintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Distil-Ajax': 'yeqrtuwzdusqsacwywcdasev',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Length': '388'
}


def get_ein(page):
    print "正在获取第%s页公司信息" % page
    form_data = {
        "CurrentPage": str(page),
        "SearchType": "org",
        "GroupExemption": "",
        "AffiliateOrgName": "",
        "SelectedCityNav[]": "",
        "SelectedCountyNav[]": "",
        "Eins": "",
        "ul": "",
        "Keywords": "",
        "FirstName": "",
        "LastName": "",
        "ZipRadius": "Zip Only",
        "City": "",
        "Participation": "",
        "revenueRangeLow": "$3,000",
        "revenueRangeHigh": "max",
        "PeopleZipRadius": "Zip Only",
        "PeopleCity": "",
        "PeopleRevenueRangeLow": "$0",
        "PeopleRevenueRangeHigh": "max",
        "PeopleAssetsRangeLow": "$0",
        "PeopleAssetsRangeHigh": "max",
        "Sort": ""
    }
    try:
        r = requests.post("http://www.guidestar.org/search/SubmitSearch", data=form_data, headers=head)
        print r.content
        hits = r.json()["Hits"]
        # if len(hits) == 0:
        #     return 0
        sql = "INSERT INTO company(EIN) VALUES "
        for hit in hits:
            sql = sql + "('%s')," % hit["Ein"]
        sql = sql[0: len(sql) - 1]
        MySQLClient.execute(sql)
        print "获取第%s页公司信息完成" % page
    except Exception, e:
        print e
        print "=====================获取第%s页公司信息异常===========================" % page
        # return 0


get_ein(401)
# pool = threadpool.ThreadPool(4)
# page_list = []
# for page in range(16313):
#     page_list.append(page + 400)
#
# request_list = threadpool.makeRequests(get_ein, page_list)
# [pool.putRequest(req) for req in request_list]
# pool.wait()
# while True:
#
#     res = get_ein("http://www.guidestar.org/search/SubmitSearch", page=page)
#     if res == 0:
#         print "公司编码已爬取完成"
#         break
#     page = page + 1
