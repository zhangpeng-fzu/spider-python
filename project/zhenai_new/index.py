import requests
import os
import time
import stat
import shutil

head = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Cookie": "__xsptplus14=14.6.1521125876.1521125946.6%234%7C%7C%7C%7C%7C%23%23PiM_P0KFVLViZVwwF0KDwPopxzArRDWo%23; sid=3d07e217-fd6a-4a87-b886-9df60e299d18; token=1952838706.1571231265016.65b40f412b891a35b923455ecf6d5383; _pc_myzhenai_showdialog_=1; _pc_myzhenai_memberid_=%22%2C1952838706%22; FSSBBIl1UgzbN7N443S=wCK.1J2vT332IGUuhX.yCNSo0yP0AD4nKO9mvN0eqcpUTROOSKl2uCS6LbBgoqLj; Hm_lvt_2c8ad67df9e787ad29dbd54ee608f5d2=1571231312; Hm_lpvt_2c8ad67df9e787ad29dbd54ee608f5d2=1571232099; FSSBBIl1UgzbN7N443T=4d9.RUQRf0IpO4E739B8G.Iga5AFdrz0VvrloLtWZK30kTHKzyqplgagOrh46wz3V_MRzAvEtz_O2CVY4.HSBrdNfOaZBRS.yNS6iE0cC5dQQUKYyTrkZnzjawvHvqwHbn9L3tcXf5Cp1gO.jn8xEdFxxIFgZjxtuecXgRBTcCn3vA9k5JDqWTdzu_pJdbwTNUJN2_EFj86f9nl.0MSdRtc3DUCnCSgAD4ViS_v29l7vjm7PnoNSPuw_sl13MGixBO2UlIGK5DROsSWA32J6wkwcHb5Qmz97XtnfG.AXeAnG64G6ZOiratBJ7TNpyvlVMwJbxSZKK6HeN4K76mPyiyqCatR4btDqzUwy9GU_hDVPPqniVGwGn07fAGSqGIpfmzvA",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
}

retry_time = 0


# 通过关键词获取公司列表信息
def get_user_info(uid):
    print("开始请求用户【%s】信息" % uid)

    global retry_time
    ua = "h5%2F1.0.0%2F1%2F0%2F0%2F0%2F0%2F0%2F%2F0%2F0%2Ff2f47c8d-0419-4a78-8415-c72a017ee727%2F0%2F0%2F1894479819"
    url = "https://album.zhenai.com/api/profile/getObjectProfile.do?objectID=%s&ua=%s" % (uid, ua)
    try:

        r = requests.get(url, headers=head)

        response_json = r.json()
        if response_json["isError"]:
            if retry_time <= 3:
                retry_time = retry_time + 1
                print(response_json["errorMessage"] + ",正在进行第%s次重试" % retry_time)
                time.sleep(5)
                get_user_info(uid)
            else:
                print("请求用户信息失败")
            return

        user_data = response_json["data"]

        gender = "male"
        if user_data["gender"] == 1:
            gender = "female"

        if not os.path.isdir(gender):
            os.makedirs(gender)

        user_dir = gender + "/" + uid
        if os.path.isdir(user_dir):
            delete_file(user_dir)
        os.makedirs(user_dir)

        child_dir_arr = ["header", "json", "moment", "photo"]
        for child_dir in child_dir_arr:
            os.makedirs(user_dir + "/" + child_dir)

        download_photo(user_data["avatarURL"], user_dir + "/header/" + uid + ".jpg")

        for photo in user_data["photos"]:
            download_photo(photo["photoURL"], user_dir + "/photo/" + str(photo["photoID"]) + ".jpg")
        print("请求用户【%s】信息成功" % uid)
    except Exception as e:
        print(e)


def download_photo(url, path):
    r = requests.get(url)
    with open(path, "wb") as code:
        code.write(r.content)


def delete_file(file_path):
    if os.path.exists(file_path):
        for fileList in os.walk(file_path):
            for name in fileList[2]:
                os.chmod(os.path.join(fileList[0], name), stat.S_IWRITE)
                os.remove(os.path.join(fileList[0], name))
        shutil.rmtree(file_path)
        return "delete ok"
    else:
        return "no filepath"


if __name__ == '__main__':
    get_user_info("1326663057")
