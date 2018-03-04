# -*-coding:utf8-*-

import sys

import requests
import threadpool

from v2.database.mysql import MySQL

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
    'Cookie': 'D_SID=218.106.154.158:NrtZxzJf/+Hp+nLBPX4cr5f/6dyOSWUhBj7c1p1nr0Q; ASP.NET_SessionId=amawt25xz05imognypl1gi53; _vwo_uuid_v2=4B725826543816CDEEAF23246A720113|4921158b8831650568cb284b74298e65; ki_r=; D_IID=94834CDF-C931-3064-B649-41961E3BA689; D_UID=23AF5DAB-95A9-3D5C-8EA2-51C863072D66; D_ZID=97A1EF18-AB6A-37DA-9565-8A7EE917CE19; D_ZUID=DA852CA1-6D8F-30F7-82BD-00D31C90B04F; D_HID=A4B35261-78D7-30A5-B57D-39044DA0BB43; today=1; .gifAuth=F0950F8EA7CE3FE231C301281D4E437291E08C4364BF4BD5EE38D3130ABD77A1C64670A58ED56E73FAD44E75FE0472FA8D744C3F4A835932023068E3D31E942F3ABB6CF4768DCCE411B16D66383C3BB6A0D67762A616320B0C41C48279B056E7DF1A7CB2597B7CFD8636197A; NOPCOMMERCE.AUTH=C328A0B2DCEDB48D2069CD8F050BDCB5CAC193557D204DCCE967E4680A09E9B94D021DBDEC416E89063C74ECB175E1272DC013120615C8BF9744C7976AE99A95E8D392D306253113E09D1C4E908ECC1BF6B094EDF932CDAE43CB1F30EC069B620906002394FBF3F67086525E30BC733452A73729B5AC5C1B998260D8; Nop.customer=f69798b7-ce73-4844-a891-1559c9647f0a; mp_5d9e4f46acaba87f5966b8c0d2e47e6e_mixpanel=%7B%22distinct_id%22%3A%20%221025711995%40qq.com%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.guidestar.org%2F%22%2C%22%24initial_referring_domain%22%3A%20%22www.guidestar.org%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpap%22%3A%20%5B%5D%7D; ki_t=1515495454400%3B1515548393911%3B1515548431544%3B2%3B9; mp_mixpanel__c=0',
    'Host': 'www.guidestar.org',
    'Origin': 'https://www.guidestar.org',
    'Pragma': 'no-cache',
    'Referer': 'https://www.guidestar.org/search',
    'User-Agent': 'Mozilla/5.0 (Macintoshintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Distil-Ajax': 'yeqrtuwzdusqsacwywcdasev',
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Length': '388'
}

intervel = 2500


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
        "revenueRangeLow": "$" + str(start),
        "revenueRangeHigh": "$" + str(end),
        "PeopleZipRadius": "Zip Only",
        "PeopleCity": "",
        "PeopleRevenueRangeLow": "$0",
        "PeopleRevenueRangeHigh": "max",
        "PeopleAssetsRangeLow": "$0",
        "PeopleAssetsRangeHigh": "max",
        "Sort": ""
    }
    r = None
    try:
        r = requests.post("http://www.guidestar.org/search/SubmitSearch", data=form_data, headers=head)
        hits = r.json()["Hits"]
        count = 0
        if page == 1:
            count = r.json()['TotalHits']
        if count > 10000:
            return count

        if len(hits) == 0:
            return
        sql = "INSERT INTO company(EIN) VALUES "
        for hit in hits:
            sql = sql + "('%s')," % hit["Ein"]
        sql = sql[0: len(sql) - 1]
        MySQLClient.execute(sql)

        print "获取第%s页公司信息完成" % page
        return count
    except Exception, e:
        print e
        print r.content
        print "=====================获取第%s页公司信息异常===========================" % page
        # return 0


global start
global end

start = 3000
end = start + intervel

while True:

    count = get_ein(1)
    while count > 10000:
        end = end - 1000
        count = get_ein(1)

    pages = int(count / 25) + 1

    pool = threadpool.ThreadPool(4)
    page_list = []
    for page in range(pages):
        page_list.append(page + 2)

    request_list = threadpool.makeRequests(get_ein, page_list)
    [pool.putRequest(req) for req in request_list]
    pool.wait()

    start = end
    end = end + intervel
