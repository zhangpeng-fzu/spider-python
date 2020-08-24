import requests
import os
import time
import stat
import shutil
import urllib3
import random

urllib3.disable_warnings()

# 用户token
token = "1833497308.1571658270403.c9b518aa6136d99035d1635f834bb821"
head = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    # "Cookie": "sid=c50b1dab-607f-42b0-8a86-0f90678911b1; __channelId=900122%2C0; oneclickLoginSwitch=60204; oneClickRegisterSwitch=57932; login_health=77cc4d3bf20ab494c3077a46f4572adaff374851eef84d09ae0c1f8b822f99c59ff7d7a8ea38d6d53783a56ba82aa1b20c4f917a3d0c97062983e12928d7a8ec; _pc_login_validate_isUnconnectByAdmin=; token=1952838706.1571626811836.91f7117c4ffb07d13d7306ee48f113a7; _pc_myzhenai_showdialog_=1; _pc_myzhenai_memberid_=%22%2C1952838706%22; Hm_lvt_2c8ad67df9e787ad29dbd54ee608f5d2=1571626826; Hm_lpvt_2c8ad67df9e787ad29dbd54ee608f5d2=1571639155",
    "Cookie": "sid=c50b1dab-607f-42b0-8a86-0f90678911b1; oneclickLoginSwitch=60204; oneClickRegisterSwitch=57932; _pc_login_validate_isUnconnectByAdmin=; _pc_myzhenai_showdialog_=1; Hm_lvt_2c8ad67df9e787ad29dbd54ee608f5d2=1571626826; __channelId=900122%2C0; login_health=7c9ba365d98344c5c92ab4f1f67fb384e4854054c4e54af44ff28d76f899892c8ef31a1a0f7d83a5659e3626ae15376105c230a239ade0c1b35ce654ff4f4572; token=" + token + "; _pc_login_validate_sec=59; _pc_myzhenai_memberid_=%22%26%23x22%3B%2C1952838706%26%23x22%3B%2C1833497308%22",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
}


# 用户列表
def get_user_list(page, retry):
    url = "https://www.zhenai.com/api/search/getConditionData.do?page=%s&pageSize=100&ageBegin=20&ageEnd=25&workCity=10107073" \
          "&heightBegin=-1&heightEnd=-1&multiEducation=-1&salaryBegin=-1&salaryEnd=-1&body=-1&ua=%s" % (
              page, get_ua())
    try:

        r = requests.get(url, headers=head, verify=False)

        response_json = r.json()
        if response_json["isError"]:
            if retry <= 2:
                retry = retry + 1
                print(response_json["errorMessage"] + ",正在进行第%s次重试" % retry)
                time.sleep(2)
                get_user_list(page, retry)
            else:
                print("请求用户信息失败")
            return

        user_data = response_json["data"]["list"]

        for user in user_data:
            uid = str(user["objectID"])
            gender = "male"
            if user["gender"] == 1:
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

            download_file(user["avatarURL"], user_dir + "/header/" + uid + ".jpg")
            get_album(uid, user_dir + "/photo/", 0)
            get_moment(uid, user_dir, 0)

            print("请求用户【%s】信息成功" % uid)
    except Exception as e:
        print(e)


# 获取相册和内心独白
def get_album(uid, path, retry):
    url = "https://album.zhenai.com/api/photo/getPhotoList.do?objectID=%s&page=1&pageSize=3&_=1571644817932&ua=%s" % (
        uid, get_ua())
    try:
        r = requests.get(url, headers=head, verify=False)
        response_json = r.json()
        if response_json["isError"]:
            if retry <= 2:
                retry = retry + 1
                print(response_json["errorMessage"] + ",正在进行第%s次重试" % retry)
                time.sleep(2)
                get_album(uid, path, retry)
            else:
                print("请求用户信息失败")
            return

        photo_data = response_json["data"]["list"]
        for photo in photo_data:
            download_file(photo["photoURL"], path + str(photo["photoID"]) + ".jpg")
        print("请求用户【%s】相册成功" % uid)
    except Exception as e:
        print(e)


# 获取用户动态
def get_moment(uid, user_dir, retry):
    url = "https://api.zhenai.com/moment/getPersonalMoments.do?objectID=%s&limit=%s&timestamp=%s" % (str(uid), 15, 0)
    try:
        head["contentType"] = "application/x-www-form-urlencoded"
        head["ua"] = get_ua()
        head[
            "cookie"] = "sid=c50b1dab-607f-42b0-8a86-0f90678911b1; oneclickLoginSwitch=60204; oneClickRegisterSwitch=57932; " \
                        "_pc_login_validate_isUnconnectByAdmin=; _pc_myzhenai_showdialog_=1; Hm_lvt_2c8ad67df9e787ad29dbd54ee608f5d2=1571626826; " \
                        "__channelId=900122%2C0; login_health=7c9ba365d98344c5c92ab4f1f67fb384e4854054c4e54af44ff28d76f899892c8ef31a1a0f7d83a5659e3626ae15376105c230a239ade0c1b35ce654ff4f4572; token=1833497308.1571658270403.c9b518aa6136d99035d1635f834bb821; _pc_login_validate_sec=59; _pc_myzhenai_memberid_=%22%26%23x22%3B%2C1952838706%26%23x22%3B%2C1833497308%22"
        r = requests.post(url, {}, headers=head, verify=False)
        response_json = r.json()
        if response_json["isError"]:
            if retry <= 2:
                retry = retry + 1
                print(response_json["errorMessage"] + ",正在进行第%s次重试" % retry)
                time.sleep(2)
                get_moment(uid, user_dir, retry)
            else:
                print("请求用户动态失败")
                return
        user_data = response_json["data"]
        for moment in user_data["list"]:
            download_file(str(moment), user_dir + "/json/" + str([moment["moment"]["momentID"]]) + ".json")
            try:
                if moment["contents"] is not None and moment["contents"][0]["url"] is not None:
                    download_file(moment["contents"][0]["url"],
                                  user_dir + "/moment/" + str([moment["moment"]["momentID"]]) + ".jpg")
            except Exception as e:
                print(e)
        print("请求用户【%s】动态成功" % uid)
        time.sleep(1)

    except Exception as e:
        print(e)


# 下载文件
def download_file(url, path):
    if url is None:
        return
    if url.startswith("http") or url.startswith("https"):
        r = requests.get(url, verify=False)
        with open(path, "wb") as code:
            code.write(r.content)
    else:
        with open(path, "w") as code:
            code.write(
                url.replace("'", "\"").replace("True", "true").replace("False", "false").replace("\"{", "{").replace(
                    "}\"", "}"))


# 删除目录
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


def get_uuid():
    ch = ""
    for i in range(6):
        ch = ch + chr(random.randrange(ord('0'), ord('9') + 1))
    return "e9ea2745-842f-485d-ba38-191a16" + ch


def get_acsrf_token(e, t):
    n = e + t
    r = 5381
    if n:
        for o in range(len(n)):
            r = r + (r << 5) + ord(n[o])
    return 2147483647 & r


def get_ua():
    uuid = get_uuid()
    return "h5/1.0.0/1/0/0/0/0/0//0/0/%s/0/0/%s" % (
        uuid,
        get_acsrf_token(token, "1.0.01" + uuid))


if __name__ == '__main__':
    for i in range(100):
        get_user_list(i + 1, 0)
