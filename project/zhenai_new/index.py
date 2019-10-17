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
    "Cookie": "__xsptplus14=14.6.1521125876.1521125946.6%234%7C%7C%7C%7C%7C%23%23PiM_P0KFVLViZVwwF0KDwPopxzArRDWo%23; sid=3d07e217-fd6a-4a87-b886-9df60e299d18; token=1952838706.1571231265016.65b40f412b891a35b923455ecf6d5383; FSSBBIl1UgzbN7N443S=wCK.1J2vT332IGUuhX.yCNSo0yP0AD4nKO9mvN0eqcpUTROOSKl2uCS6LbBgoqLj; Hm_lvt_2c8ad67df9e787ad29dbd54ee608f5d2=1571231312; FSSBBIl1UgzbN7N443T=4FJSHnTk6pChT8fCirDlCiCPbMyqN9lXccL8pJOKjuSXYAbW4QNh1wRPT9PffglccInk4Ti1QEsyuseHzib.y9Ku6LK7t2Tqb2VFvDW17Lk21.VxhpAiaHtrtco9p3jvrf2wD1W9o2fl3.Am_c6x.jZxJXXaSqGQ0zC6ahK33HYLoDQGstM7AJQcmfjKE0YtLKEkLbRW07W85R5dc8T88q_F.Jy.IEuZdb4eSr.ydmcSLY_t0SorWM81CjKQwgE1th1Htu0U4Nd5doULGXuXHyVIgwfdJvi.Y.M..fwNsrht7jSfDeAQ2OyM3Ki_lvBKOU37; Hm_lpvt_2c8ad67df9e787ad29dbd54ee608f5d2=1571327969",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1"
}

retry_time = 0
user_dir = "female"


# 通过关键词获取公司列表信息
def get_user_info(uid):
    print("开始请求用户【%s】信息" % uid)

    global retry_time
    global user_dir
    ua = "h5%2F1.0.0%2F1%2F0%2F0%2F0%2F0%2F0%2F%2F0%2F0%2F3ea14c2a-7d17-44bb-8e11-d1ab8cb849f1%2F0%2F0%2F1992332163"
    url = "https://album.zhenai.com/api/profile/getObjectProfile.do?objectID=%s&ua=%s" % (uid, ua)
    try:

        r = requests.get(url, headers=head, verify=False)

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

        download_file(user_data["avatarURL"], user_dir + "/header/" + uid + ".jpg")

        for photo in user_data["photos"]:
            download_file(photo["photoURL"], user_dir + "/photo/" + str(photo["photoID"]) + ".jpg")
        print("请求用户【%s】信息成功" % uid)
    except Exception as e:
        print(e)


def get_moment(uid):
    print("开始请求用户【%s】动态" % uid)
    global user_dir

    global retry_time
    url = "https://api.zhenai.com/moment/getPersonalMoments.do?objectID=%s&limit=%s&timestamp=%s" % (uid, 15, 0)
    try:
        head1 = {
            "content-type": "application/x-www-form-urlencoded",
            "channelid": "902684",
            "accept	": "*/*",
            "reqnum": "623",
            "accept-encoding": "gzip, deflate, br",
            "platform": "3",
            "accept-language": "zh-Hans-CN;q=1, en-CN;q=0.9",
            "subchannelid": "2",
            "user-agent	": "zhenaiwang/6.22.1 (iPhone; iOS 13.2; Scale/2.00)",
            "ua": "zhenai/6.22.1/18/13.2/iPhone11,8/0f607264fc6318a92b9e13c65db7cd3c/902684/2/www.zhenaidefault.com/1792/828/7333E44D-24A8-41EC-B5EB-DB513AB6384F/3/ac1df04409af217cee4a9a5f33332afd95f5ef0d/c8c6d31de7121fa7ff917f08e3efa58f/992137EB-1860-475C-87D7-BBC323219CBF",
            "cookie	": "oneClickRegisterSwitch=91239; oneclickLoginSwitch=95152; openHttpDnsNum=6962609; ad2flag=1; token=1952838706.1571236115918.6566fd9980babb79aa8c47c7c991c480; sid=tuIEaz4bWCl9WOo5s7kB"}
        r = requests.post(url, {}, headers=head1, verify=False)

        response_json = r.json()
        if response_json["isError"]:
            if retry_time <= 3:
                retry_time = retry_time + 1
                print(response_json["errorMessage"] + ",正在进行第%s次重试" % retry_time)
                time.sleep(5)
                get_moment(uid)
            else:
                print("请求用户动态失败")
            return
        user_data = response_json["data"]
        user_dir = user_dir + "/" + uid
        for moment in user_data["list"]:
            download_file(str(moment), user_dir + "/json/" + str([moment["moment"]["momentID"]]) + ".json")
            download_file(moment["contents"][0]["url"],
                          user_dir + "/moment/" + str([moment["moment"]["momentID"]]) + ".jpg")
        print("请求用户【%s】动态成功" % uid)
    except Exception as e:
        print(e)


def download_file(url, path):
    if url is None:
        return
    if url.startswith("http") or url.startswith("https"):
        r = requests.get(url, verify=False)
        with open(path, "wb") as code:
            code.write(r.content)
    else:
        with open(path, "w") as code:
            code.write(url)


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
    uids = ["1326663057", "1751980267", "109805850", "1917717446", "97640747", "1422423649", "1227512972", "1515273775",
            "1693898709", "100983623"]
    for uid in uids:
        user_dir = "female"
        retry_time = 0
        # get_user_info(uid)
        get_moment(uid)
