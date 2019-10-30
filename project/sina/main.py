# coding=utf-8
from id_generator import *
from get_user_info import *
from get_weibo_list import *
import threading
import sys

reload(sys)

sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
    print("开始获取粉丝和关注者id")
    t1 = threading.Thread(target=start_id_generator, args="210576870")
    t1.start()

    print("开始获取用户信息")
    t2 = threading.Thread(target=start_get_user_info, args=())
    t2.start()
    start_get_user_info()

    print("开始获取微博信息")
    t3 = threading.Thread(target=start_get_weibo_info, args=())
    t3.start()
