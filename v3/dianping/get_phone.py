# _*_coding:utf-8_*_

import random
import re

import requests
from threadpool import *

head = {
    "Accept": "*/*",
    # "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Content-Type": "charset=UTF-8",
    "Host": "www.dianping.com",
    # "Referer": "http://news.sina.com.cn/society/",
    "Upgrade-Insecure-Requests": '1',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    # 操作cookie
    "Cookie": 'cy=982; cityid=982; cye=minhou; s_ViewType=10; _lxsdk_cuid=161eef1ff9cc8-0608c2dd6957ab-32677b04-13c680-161eef1ff9dc8; _lxsdk=161eef1ff9cc8-0608c2dd6957ab-32677b04-13c680-161eef1ff9dc8; _hc.v=65bc51bb-00dc-a223-98c9-e47b965d62c4.1520132293; cy=14; cye=fuzhou; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=164cc94c7c6-e29-8be-574%7C%7C6'}

old_phone_list = []
new_phone_list = []

flag = 3396


def load_phone():
    f = open("phohe.txt", "r")
    for line in f.readlines():
        if len(line) > 0 and line.replace("\n", "") not in old_phone_list:
            old_phone_list.append(line.replace("\n", ""))
    f.close()


def get_phone_by_Id(shop_id):
    global flag
    url = "http://www.dianping.com/shop/%s" % str(shop_id).strip()
    try:
        # 发起请求,得到响应结果
        r = requests.get(url, headers=head)

        if r.status_code != 200:
            new_flag = random.randint(0, 999999)
            head["User-Agent"] = head["User-Agent"].replace(str(flag), str(new_flag))
            flag = new_flag

        response_content = r.content.decode('utf-8')
        results = re.findall(r"itemprop=\"tel\">.*?</span>", response_content, re.I | re.S | re.M)
        if len(results) == 0:
            new_flag = random.randint(0, 999999)
            head["User-Agent"] = head["User-Agent"].replace(str(flag), str(new_flag))
            print("触发反爬虫，更新User-Agent：" + head["User-Agent"])
            flag = new_flag
            return
        for phone in results:
            phone = phone.replace("itemprop=\"tel\">", "").replace("</span>", "").strip()
            if phone is None:
                continue
            if phone in old_phone_list:
                print("号码【%s】已存在，跳过" % phone)
                return
            if "/" in phone:
                phone_arr = phone.split("/")
                if len(phone_arr[0]) == 11 and "-" not in phone_arr[0] and phone_arr[0] not in old_phone_list:
                    new_phone_list.append(phone_arr[0])
                    print("获取新号码【%s】" % phone_arr[0])
                if len(phone_arr[1]) == 11 and "-" not in phone_arr[1] and phone_arr[1] not in old_phone_list:
                    new_phone_list.append(phone_arr[1])
                    print("获取新号码【%s】" % phone_arr[1])
            else:
                if len(phone) == 11 and "-" not in phone:
                    new_phone_list.append(phone)
                    print("获取新号码【%s】" % phone)
    except Exception as e:
        print("获取手机号码异常!", e)


def get_phone_list(city):
    print("开始抓取商铺手机号码")
    global flag
    page = 1
    is_stop = False
    retry_times = 0
    total = len(old_phone_list)
    # 分页获取列表
    while not is_stop and total <= 50000 and page < 100:
        print("正在抓取第%s页的商铺信息" % page)
        url = "http://www.dianping.com/%s/ch50/g157p%s" % (city, page)
        try:
            # 发起请求,得到响应结果
            r = requests.get(url, headers=head)

            if r.status_code != 200:
                new_flag = random.randint(0, 999999)
                head["User-Agent"] = head["User-Agent"].replace(str(flag), str(new_flag))
                flag = new_flag
                retry_times = retry_times + 1
                if retry_times <= 3:
                    print("获取列表异常，第%s次重试!code=%s" % (retry_times, r.status_code))
                else:
                    print("获取列表异常，终止爬虫!code=%s", r.status_code)
                    is_stop = True
                continue

            response_content = r.content.decode('utf-8')
            results = re.findall(r"notAdShops.*?]", response_content, re.I | re.S | re.M)
            content = ""
            if len(results) > 0:
                content = results[0].replace("notAdShops:", "").replace("[", "").replace("]", "").strip().strip(",")
            ids = content.split(",")
            if len(ids) == 0:
                print("该城市已全部爬取完成")
                return new_phone_list
            my_requests = makeRequests(get_phone_by_Id, ids)
            [pool.putRequest(req) for req in my_requests]
            pool.wait()
            # phone = get_phone_by_Id(search_id)
            total = len(old_phone_list) + len(new_phone_list)
            print("抓取第%s页的新闻完成" % page)
            retry_times = 0
            page = page + 1
        except Exception as e:
            retry_times = retry_times + 1
            if retry_times <= 3:
                print(e)
                print("获取列表异常，第%s次重试!" % retry_times)
                continue
            else:
                print("获取列表异常，终止爬虫!")
                is_stop = True
    return new_phone_list


if __name__ == '__main__':
    load_phone()

    cities = ["taipei", "alashan", "anshan", "anqing",
              "anyang",
              "aba", "anshun", "ali", "ankang", "anguo", "anxin", "anping", "anzhe", "aershan", "antu", "acheng",
              "anda", "anji", "anxi", "anyi", "anyuan", "anfu", "anqiu", "anyangxian", "anlu", "anxiang", "anhua",
              "anren", "anxian", "anyue", "abaxian", "anliu", "anning", "anduo", "angren", "ansai", "akesai",
              "aluqinqi", "aohanqi", "arongqi", "abagaqi", "azuoqi", "ayouqi", "beijing", "baoding", "baotou",
              "bayannaoer", "benxi", "baishan", "baicheng", "bengbu", "bozhou", "binzhou", "beihai", "baise", "bazhong",
              "bijieshi", "baoshan", "baoji", "baiyin", "baisha", "baoting", "bazhou", "boye", "botou", "boxiang",
              "baode", "beipiao", "benxixian", "beining", "binxian", "bayan", "boli", "baiquan", "beian", "baoqing",
              "binhai", "baoying", "boxing", "boai", "baofeng", "miyang", "baokang", "badong", "baojing", "boluo",
              "binyang", "beiliu", "bobai", "bama", "beichuan", "baoxing", "baiyu", "batang", "butuo", "tongren",
              "binchuan", "biru", "bange", "baqing", "basu", "bianba", "linzhixian", "bomi", "bailang", "baishui",
              "binxianshi", "baihe", "banma", "bishan", "bazhouqu", "bazuoqi", "bayouqi", "boao", "baiyunshan",
              "boshan", "baodi", "chengdu", "chongqing", "changchun", "changsha", "chengde", "cangzhou", "changzhi",
              "chifeng", "chaoyang", "changzhou", "chuzhou", "chaohu", "chizhou", "changde", "chenzhou", "chaozhou",
              "chuxiongzhou", "changdudiqu", "changjiang", "chengmai", "chongzuo", "conghua", "changshu", "cixi",
              "changhai", "chicheng", "chongli", "chengdexian", "cangli", "cangxian", "chengan", "cixian",
              "changzhixian", "changzi", "chaoyangxian", "cangtu", "changling", "chengbai", "chunan", "changxing",
              "changshan", "cangnan", "changfeng", "changle", "changting", "chongyi", "chongren", "chiping", "cangyi",
              "cangle", "changdao", "caoxian", "chengwu", "changyuan", "changge", "chibi", "chongyang", "changyang",
              "cili", "chaling", "changning", "chengbu", "chenxi", "chaoan", "cenxi", "cangwu", "cangxi",
              "changningxian", "chishui", "cengong", "congjian", "changshun", "ceheng", "chenggong", "chengjian",
              "cangning", "changyuanxian", "chuxiong", "chaya", "chayu", "cuomei", "cuona", "cuoqin", "chengcheng",
              "changwu", "chunhua", "chenggu", "chongxin", "chengxian", "chenduo", "chengkou", "chenhuqi",
              "chayouqianqi", "chayouzhongqi", "chayouhouqi", "chongmingqu", "changbaishan", "changshou",
              "chaoyangshantou", "chenghai", "changqing", "chashan", "caofeidian", "dalian", "dongguan", "datong",
              "dandong", "daqing", "daxinganling", "dongying", "dezhou", "deyang", "dazhou", "dali", "dehong", "diqing",
              "dingxi", "danzhou", "dingan", "dongfang", "dacheng", "dachang", "dingzhou", "dingxing", "dongguang",
              "daming", "datongxian", "dingxiang", "daixian", "daning", "dengkou", "duolun", "diaobingshan", "dengta",
              "donggang", "dashiqiao", "dawa", "dehui", "daan", "dongfeng", "dongliao", "dunhua", "duerbote",
              "dongning", "donghai", "dongtai", "dafeng", "danyang", "deqing", "daishan", "dongyang", "dongtou",
              "dangshan", "dingyuan", "dangtou", "dongzhi", "datian", "dehua", "dean", "ducang", "dayu", "dingnan",
              "dexing", "dongxiang", "donga", "dongping", "dingtao", "dongming", "dengfeng", "dengzhou", "dancheng",
              "danjiangkou", "dawu", "daye", "dangyang", "dongan", "daoxian", "dongkou", "dongyuan", "dapu",
              "deqingxian", "dianbai", "dongxing", "daxin", "debao", "donglan", "duan", "dahua", "dujiangyan", "dayi",
              "daying", "dazhu", "danleng", "danba", "daofu", "dege", "daocheng", "derong", "decang", "daozhen",
              "dafang", "dejian", "danzhai", "duyun", "dushan", "daguan", "deqin", "dayao", "dangxiong",
              "duilongdeqing", "dazi", "dingqing", "dingri", "dingjie", "dalixian", "dingbian", "danfeng", "dunhuang",
              "dangcang", "dongxiangzu", "diebu", "datongzzxian", "dari", "delingha", "dulan", "dazu", "dianjian",
              "datongqu", "daerhanqi", "dalateqi", "dongwuqinqi", "dalishi", "doumen", "dongkeng", "eerduosi", "ezhou",
              "enshizhou", "eerguna", "erlianhaote", "enshi", "enping", "emeishan", "ebian", "eshan", "eryuan",
              "eqianqi", "eqi", "elunchunqi", "ewenkeqi", "ejinaqi", "fuzhou", "foshan", "fushun", "fuxin", "fuyang",
              "jiangxifuzhou", "fangchenggang", "fenghua", "fuqing", "fengning", "funingqu", "fuping", "fucheng",
              "feixiang", "fanzhi", "fushan", "fenxi", "fengyang", "fangshan", "fengzhen", "fakun", "fuxinxian",
              "lnfushunxian", "fengcheng", "fuyu", "fusong", "fuyuxian", "fujin", "fuyuan", "fengxian", "funingxian",
              "fuyangfy", "feidong", "feixi", "funan", "fengtai", "fengyangxian", "fancang", "fuan", "fuding",
              "fuliang", "fenyi", "fengchengshi", "fengxin", "feixian", "feicheng", "fengqiu", "fanxian", "fangcheng",
              "fugou", "fangxian", "fenghuang", "fogang", "fengshun", "fengkai", "fusui", "fengshan", "fuchuan",
              "fushunxian", "fenggang", "fuquan", "fumin", "fuyuanxian", "fengqing", "fugong", "wszfuning", "fuxian",
              "fupingxian", "fengxiang", "fufeng", "fengxianxian", "fopin", "fugu", "fengdu", "fengjie", "fuchunjiang",
              "fuling", "fulaerji", "guangzhou", "guiyang", "ganzhou", "guilin", "guigang", "guangyuan", "guangan",
              "ganzi", "gannanzhou", "guoluo", "guyuan", "geermu", "gaoyou", "gaocheng", "gaoyi", "guyuanxian", "guan",
              "gaopaidian", "gaoyang", "gucheng", "guangzong", "guangping", "guantao", "gujiao", "guangling", "gaoping",
              "guxian", "guyang", "genhe", "gaizhou", "gongzhuling", "gannan", "gaochun", "ganyu", "guanyun", "guannan",
              "woyang", "guzhen", "guangde", "guangze", "gutian", "guixi", "ganxian", "guangfeng", "guangcang", "gaoan",
              "guanxian", "gaotang", "guangrao", "gaoqing", "gaomi", "gongyi", "guangshan", "gushi", "guchengxian",
              "gongan", "guangshui", "guiyangxian", "guidong", "guzhang", "gaoyao", "guangning", "gaozhou", "guanyang",
              "gongcheng", "guiping", "guanghan", "gulin", "gaoxian", "gongxian", "ganzixian", "ganluo", "guanling",
              "guiding", "genma", "gongshan", "gejiu", "guangnan", "gongjue", "gongbujiangda", "gongga", "gangba",
              "geer", "geji", "gaize", "gaoling", "ganquan", "gaolan", "gangu", "gulang", "anxixian", "gaotai",
              "guanghe", "gangcha", "gande", "gonghe", "guide", "guinan", "gongqingcheng", "gulangyu", "gaoming",
              "hangzhou", "haikou", "haerbin", "hefei", "huhehaote", "handan", "hengshui", "hulunbeier", "huludao",
              "hegang", "heihe", "huaian", "huzhou", "huainan", "huaibei", "huangshan", "heze", "hebi", "huangshi",
              "huanggang", "hengyang", "huaihua", "huizhou", "heyuan", "hezhou", "hechi", "honghe", "hanzhong",
              "haidong", "haibei", "huangnan", "haixi", "huangchuan", "huichun", "hainanzhou", "huaianxian", "huailai",
              "huanghua", "hejian", "haixing", "huairen", "hunyuan", "huguan", "hequ", "heshun", "houma", "huozhou",
              "hongdong", "helingeer", "huolinguole", "huade", "huanren", "haicheng", "heishan", "huadian", "huinan",
              "heliu", "huanan", "huachuan", "hulin", "hailin", "hailun", "huma", "hongze", "haimen", "haian",
              "haining", "haiyan", "huaiyuan", "huaining", "huoqiu", "huoshan", "hanshan", "hexian", "huian", "hukou",
              "huicang", "hengfeng", "huantai", "haiyang", "huimin", "huixian", "huojia", "huaxian", "huaibin",
              "huaiyang", "hanchuan", "hongan", "huangmei", "honghu", "hefeng", "hanshou", "huarong", "hengyangxian",
              "hengnan", "hengshan", "hengdong", "hongjian", "huitong", "huayuan", "heping", "huilai", "haifeng",
              "huidong", "heshan", "huaiji", "huazhoushi", "hengxian", "hepu", "huanjiang", "heshanshi", "huayinshi",
              "hejianxian", "hongya", "hanyuan", "heishui", "hongyuan", "huili", "huidongxian", "hezhang", "huangping",
              "huishui", "huize", "huaning", "huapin", "heqing", "honghexian", "helou", "huxian", "huangliu",
              "huangling", "huayin", "hancheng", "huazhouqu", "heyang", "hengshanqu", "hanyin", "huining", "huanxian",
              "huachi", "heshui", "huating", "huixianxian", "hezheng", "hezuo", "huangyuan", "huangzhong", "huzhu",
              "hualong", "haiyanxian", "henanxian", "helan", "hejin", "hangjinqi", "hangjinhouqi", "haiyuanxian",
              "hengdian", "hongcun", "huashuiwan", "huangguoshu", "huashan", "hechuan", "hekou", "huiyang", "huairou",
              "hannan", "jinan", "jincheng", "jinzhong", "jinzhou", "jilin", "jixi", "jiamusi", "jiaxing", "jinhua",
              "jingdezhen", "jiujiang", "jian", "jining", "jiaozuo", "jinmen", "jingzhou", "jiangmen", "jieyang",
              "jiayuguan", "jinchang", "jiuquan", "jiyuan", "jiangdu", "jiangyin", "jixian", "jinghai", "jinzhoushi",
              "jingjing", "jizhou", "jingxian", "julu", "jizhe", "jingle", "jiexiu", "lfjixian", "jiaokou", "jiaocheng",
              "jianping", "jiancang", "jiutai", "jiaohe", "jianshi", "jingyu", "jiayin", "sysjixianxian", "jidong",
              "jinhu", "jianhu", "jingjian", "jiangyan", "jurong", "jintan", "jiande", "jiashan", "jianshan", "jinyun",
              "jingning", "jieshou", "jinzhai", "jingxianxian", "jingde", "jixixian", "jianou", "jianyangqu", "jiangle",
              "jianning", "jinjiang", "jiujiangxian", "jinxi", "jingan", "jinggangshan", "jianxian", "jishui", "jiyang",
              "juxian", "junan", "jinxiang", "jiaxiang", "juye", "juancheng", "jiaxian", "jingshan", "jiayu",
              "jianling", "jianli", "jianshixian", "jinshi", "jiahe", "jianyong", "jianghua", "jingzhouxian", "jishou",
              "jiaoling", "jiexi", "jingxi", "jinxiu", "jintang", "jiange", "jianyou", "jingyan", "jiajian", "jianan",
              "junlian", "jianyang", "jiuzhaigou", "jinchuan", "jiuliu", "jinyang", "jinsha", "jiankou", "jinping",
              "jianhe", "jinning", "jiangchuan", "jingdong", "jinggu", "jiangcheng", "jianchuan", "jinghong",
              "jianshui", "jinpingxian", "jiali", "jianda", "jiacha", "jianzi", "jilong", "jingyang", "jingbian",
              "jiaxianxian", "jingyuan", "jingtai", "jinta", "jingchuan", "jingningxian", "jishishan", "jianzha",
              "jiuzhi", "jingyuanxian", "jishanxian", "jiangxian", "jinmenxian", "jiuhuashan", "jiagedaqi", "jiawang",
              "jiangjin", "jili", "kunming", "kaifeng", "kangding", "kunshan", "kangbao", "kuancheng", "kelan", "kailu",
              "kangping", "kalaqinzuiyi", "kaiyuan", "kuandian", "keshan", "kedong", "shaoxingxian", "kaihua", "kenli",
              "kaiping", "kaijian", "kaiyang", "kaili", "kaiyuanshi", "changdu", "kangma", "kangxian", "kangle",
              "kaizhouqu", "ketengqi", "keqinqi", "kezuozhongqi", "kezuohouqi", "kulunqi", "keyouqianqi",
              "keyouzhongqi", "lanzhou", "langfang", "linfen", "lvliang", "liaoyang", "liaoyuan", "lianyuangang",
              "lishui", "liuan", "longyan", "laiwu", "linyi", "liaocheng", "luoyang", "luohe", "loudi", "liuzhou",
              "luzhou", "leshan", "liangshan", "liupanshui", "lijiang", "linchang", "lasa", "linzhi", "longnan",
              "linxiazhou", "laibin", "ledong", "lingao", "lingshui", "lishuixian", "luquan", "luancheng", "lingshou",
              "luanping", "longhua", "lulong", "luanxian", "luannan", "leting", "laiyuan", "laishui", "lixian",
              "lincheng", "longrao", "linxi", "linzhang", "loufan", "lingqiu", "lucheng", "licheng", "lingchuan",
              "lingshi", "linxian", "liulin", "lanxian", "linxixian", "liangcheng", "liaozhong", "lingyuan",
              "liaoyangxian", "linghai", "lishu", "liuhe", "linjian", "liujing", "longjiang", "lindian", "luobei",
              "linkou", "lanxixian", "lianshui", "liyang", "linan", "liuyou", "lanxi", "linhai", "liuquan", "lingbi",
              "lixin", "linquan", "laian", "lujian", "langxi", "lianjiangxian", "luoyuan", "liuhai", "liancheng",
              "leping", "lianhua", "luxi", "liunan", "lichuanxian", "lean", "linqing", "leling", "lingxian",
              "linyixian", "lijin", "linqu", "liukou", "laiyang", "laizhou", "lanling", "linshu", "liangshanxian",
              "lingbao", "lushi", "luanchuan", "luoning", "linzhou", "lankao", "linying", "pdslushan", "luoshan",
              "luyi", "laohekou", "luotian", "lichuan", "laifeng", "liuyang", "cdlixian", "linli", "linxiang", "liling",
              "leiyang", "linwu", "lanshan", "longhui", "lengshuijiang", "lianyuan", "xxluxi", "liushan", "lianzhou",
              "lianshan", "liannan", "lecang", "liuchuan", "lianping", "lufeng", "luhe", "liumen", "luoding",
              "lianjian", "leizhou", "longan", "lingchuanxian", "lipu", "longsheng", "liujiang", "liucheng", "luzhai",
              "luchuan", "lingshan", "longzhou", "lingyun", "leye", "longlin", "luocheng", "luojian", "langzhong",
              "linshui", "longcang", "luxian", "lezhi", "yalushan", "ablixian", "luding", "luhuo", "litang", "leibo",
              "liping", "leishan", "libo", "luodian", "liuli", "luquanxian", "luoping", "luliang", "liuling", "ludian",
              "lancang", "lianghe", "longchuan", "lushui", "lanping", "lufengxian", "lvchun", "hhluxi", "linzhouxian",
              "leiwuqi", "luolong", "langxian", "luozha", "longzi", "kalangzi", "lazi", "lantian", "luochuan", "liquan",
              "longxian", "linyou", "lueyang", "liuba", "langao", "luonan", "linze", "lingtai", "lintao", "longxi",
              "lnlixian", "liangdang", "linxia", "linxiaxian", "lintan", "luqu", "lingwu", "longde", "liangping",
              "lushan", "yclinyixian", "luzhi", "longhushan", "luguhu", "linzi", "lanshanqu", "lintong", "mudanjiang",
              "maanshan", "maoming", "meizhou", "mianyang", "meishan", "meihekou", "miyun", "mancheng", "mengcun",
              "manzhouli", "mishan", "muleng", "mingshui", "mohe", "mengcheng", "mingguang", "minhou", "mingxi",
              "mengyin", "shenchixian", "mengjin", "mengzhou", "minquan", "macheng", "miluo", "mayang", "meixian",
              "mashan", "mengshan", "mianzhu", "muchuan", "mabian", "miyi", "maerkang", "maoxian", "mianning", "meigu",
              "muli", "meitan", "majian", "maliu", "mojiang", "menglian", "luxishi", "midu", "moding", "menghai",
              "mengla", "mengzi", "mile", "malipo", "maguan", "muzhugongka", "mangkang", "milin", "motuo", "bjmeixian",
              "mianxian", "mizhi", "minqin", "minle", "minxian", "maqu", "minhe", "menyuan", "maqin", "maduo",
              "molidawaqi", "moganshan", "mingyueshan", "mouping", "mentougou", "mayong", "nanjing", "ningbo",
              "nanchang", "nanning", "nantong", "nanping", "ningde", "nanyang", "neijiang", "nanchong", "nujiang",
              "naqu", "ninghe", "nanpi", "nangong", "neiqiu", "nanhe", "ningjing", "ningwu", "ningcheng", "nongan",
              "nehe", "nengjian", "ningan", "nanling", "ningguo", "ninghua", "nanan", "nanchangxian", "nankang",
              "ningdu", "nancheng", "nanfeng", "ningjin", "ningyang", "neihuang", "nanle", "ningling", "nanzhao",
              "neixiang", "nanzhang", "ningxiang", "nanxian", "ningyuan", "nanxiong", "nanao", "ningming", "napo",
              "nandan", "nanbu", "nanjiang", "ningnan", "nayong", "ninglang", "ninger", "nanjian", "nanhua", "nimu",
              "naquxian", "nierong", "nima", "naidong", "nanmulin", "nielamu", "nanzheng", "ningqiang", "ningshan",
              "ningxian", "nangqian", "ninghai", "naimanqi", "nandaihe", "nanchuan", "nansha", "panjin", "putian",
              "pingxiang", "pingdingshan", "puyang", "panzhihua", "puer", "pingliang", "pulandian", "pingshan",
              "pingquan", "pingxiangxian", "pingding", "pingshun", "pianguan", "pingyao", "puxian", "panshan", "panshi",
              "pizhou", "peixian", "pinghu", "pujiang", "panan", "pingyang", "pingtan", "pucheng", "pingnan", "pengze",
              "poyang", "pingyin", "pingyuan", "penglai", "pingyi", "puyangxian", "pingyu", "pingjian", "pingyuanxian",
              "puning", "pingle", "pingnanxian", "pubei", "pingxiangshi", "pingguo", "pengzhou", "pixian",
              "pujiangxian", "pingwu", "pengan", "pengxi", "pingshanxian", "pingcang", "pengshan", "puge", "panxian",
              "pingba", "puding", "pingtang", "puan", "pingbian", "pulan", "puchengxian", "pingli", "pingan", "pingluo",
              "pengyang", "pengshui", "pingluxian", "putuoshan", "pinggu", "qingdao", "qinhuangdao", "qiqihaer",
              "qitaihe", "quzhou", "quanzhou", "qianjiang", "qingyuan", "qinzhou", "qianxinan", "qiandongnan",
              "qiannan", "qujing", "qingyang", "qionghai", "qiongzhong", "qinglong", "qianan", "qianxi", "bdqingyuan",
              "quyang", "qingxian", "qinghe", "qiuxian", "quzhouxian", "qingxu", "qinxian", "qinyuan", "qinshui",
              "qixian", "quwo", "qingshuihe", "fsqingyuan", "qiananxian", "qianguoerluo", "qinggang", "qingan",
              "qidong", "qingtian", "lsqingyuan", "quanjiao", "qianshan", "qimen", "qingyangxian", "qingliu", "quannan",
              "qianshanxian", "qihe", "qingyun", "qingzhou", "qixia", "qufu", "qinyang", "hbqixian", "qingfeng",
              "kfqixian", "queshan", "qichun", "qidongxian", "qiyang", "quanzhouxian", "qionglai", "qingchuan",
              "jianwei", "quxian", "qingshen", "qingzhen", "bijie", "qianxixian", "qinglongxian", "qiaojia", "qiubei",
              "qushui", "qiongjie", "qusong", "qianxian", "qishan", "qianyang", "qingjian", "qingshui", "qinan",
              "qingcheng", "qilian", "qumalai", "qingtongxia", "qijian", "qiandaohu", "qingchengshan", "qinghaihu",
              "qingbaijiang", "qianjiangcq", "rizhao", "rikazediqu", "raoyang", "renqiu", "renxian", "raohe", "rugao",
              "rudong", "ruian", "ruicang", "ruijin", "rongcheng", "rushan", "ruyang", "ruzhou", "runan", "rucheng",
              "renhua", "ruyuan", "raoping", "rongan", "rongshui", "rongxian", "rongxianxian", "renshou", "rangtang",
              "nuoergai", "renhuai", "rongjian", "ruili", "renbu", "ritou", "rongcang", "rongchengxian", "ruichengxian",
              "shanghai", "suzhou", "shenzhen", "shenyang", "shijiazhuang", "shuozhou", "siping", "songyuan",
              "shuangyashan", "suihua", "suqian", "shaoxing", "anhuisuzhou", "sanming", "shangrao", "sanmenxia",
              "shangqiu", "shiyan", "suizhou", "shaoyang", "shaoguan", "shantou", "shanwei", "suining", "shannan",
              "shangluo", "shizuishan", "sanya", "shennongjia", "shenzhe", "shangyi", "sanhe", "shunping", "shenzhou",
              "suning", "shahe", "shexian", "shanyin", "shenchi", "shouyang", "shilou", "shangdu", "suizhong", "shulan",
              "shuangliao", "shuangcheng", "shangzhi", "sunwu", "suibin", "suifenhe", "suileng", "szsuining", "shuyang",
              "siyang", "sihong", "sheyang", "shengsi", "shangyu", "shengzhou", "sanmen", "suicang", "songyang",
              "sixian", "suixi", "susong", "hsxixian", "shouxian", "shucheng", "shitai", "shaowu", "shuncang", "songxi",
              "shaxian", "shishi", "shanghang", "shouning", "shangli", "shangyou", "shicheng", "shangraoxian",
              "shanggao", "suichuan", "shanghe", "xinxian", "shouguang", "sishui", "danxian", "shanxian", "songxian",
              "suixian", "sheqi", "shangcheng", "shangshui", "shenqiu", "suiping", "shangcha", "shayang", "shishou",
              "songzi", "sangzhi", "shimen", "shaoshan", "shuangpai", "shaodong", "shaoyangxian", "zysuining",
              "shuangfeng", "shixing", "sihui", "suixixian", "shanglin", "sanjiang", "shangsi", "shuangliu", "santai",
              "shifang", "shehong", "shimian", "songpan", "shiqu", "seda", "suiyang", "shiqian", "sinan", "songtao",
              "shibing", "sansui", "sandu", "songming", "shilin", "shizong", "shidian", "suijian", "shuifu",
              "shuangjiang", "shuangbo", "shiping", "shenzha", "suoxian", "sangri", "rikaze", "sajia", "sagaxian",
              "sanyuan", "shenmu", "suide", "shiquan", "shangnan", "shanyang", "subei", "shandan", "sunan", "shizhu",
              "sansha", "shunde", "sanqingshan", "sanxia", "siziwangqi", "suzuoqi", "suyouqi", "szsuixian",
              "shuichengxian", "shuanghuxian", "shuanglang", "shidao", "shangjie", "shijie", "shipai", "shatian",
              "shuangyang", "sanshui", "tianjin", "taiyuan", "tangshan", "tongliao", "tieling", "tonghua", "taizhou",
              "zhejiangtaizhou", "tongling", "taian", "tianmen", "tongrendiqu", "tongchuan", "tianshui", "tunchang",
              "taicang", "tangxian", "tianzhen", "tunliu", "taigu", "tuoketuo", "tuquan", "tielingxian", "taianxian",
              "taonan", "tongyu", "tonghuaxian", "tumen", "tonghe", "tailai", "tieli", "tongjiang", "tangyuan", "tahe",
              "taixing", "tongzhou", "tonglu", "tongxiang", "tiantai", "taishun", "taihe", "tianchang", "tongcheng",
              "taihu", "taining", "tonggu", "taihexian", "tancheng", "tengzhou", "tangyin", "taiqian", "tongxu",
              "tanghe", "tongbo", "taikang", "tuanfeng", "tongchengxian", "tongshanxian", "taoyuanxian", "taojian",
              "tongdao", "taishan", "tengxian", "tiandeng", "tianyang", "tiandong", "tianlin", "tiane", "tongjiangxian",
              "tianquan", "tongzi", "tianzhu", "taijian", "tonghai", "tengchong", "tongguan", "taibai", "tianzhuxian",
              "tongwei", "tongrenxian", "tianjun", "tongxin", "tongnan", "tongliang", "tongde", "tuzuoqi", "tuyouqi",
              "taipusiqi", "tianmuhu", "tongli", "tianmushan", "tianzhushan", "tiantaishan", "wuxi", "wuhan", "wuhai",
              "wulanchabu", "wenzhou", "wuhu", "weifang", "weihai", "wuzhou", "wenshan", "weinan", "wuwei", "wuzhong",
              "wulanhaote", "wanning", "wenchang", "wuzhishan", "wujiang", "wafangdian", "wuji", "wanquan", "weichang",
              "wenan", "wangdu", "wuyi", "wuqiang", "wuqiao", "xtweixian", "wuan", "hdweixian", "wuxiang", "wutai",
              "wuzai", "wenshui", "wuchuanxian", "wuyuanxian", "wangqing", "wuchang", "wudalianchi", "wangkui",
              "wuyixian", "wenling", "wencheng", "wuhe", "wuhuxian", "wangjian", "wuweixian", "wuyishan", "wuping",
              "wuning", "wannian", "wuyuan", "wanzai", "wanan", "wucheng", "wendeng", "wulian", "weishan", "wenshang",
              "wudi", "wuzhi", "wenxian", "weihui", "weishi", "wuyang", "wugang", "wuxue", "wufeng", "wugangshi",
              "wengyuan", "wuhua", "wuchuan", "wuming", "wuxuan", "wangcang", "wusheng", "weiyuan", "wanyuan",
              "wenchuan", "wuchuanzzxian", "weining", "wengan", "wangmo", "weixin", "weixi", "weishanxian", "wuding",
              "wenshanshi", "wuqi", "wugong", "wubao", "wushan", "weiyuanxian", "wenxianxian", "wulan", "wulong",
              "wuxia", "wushanxian", "wuzhen", "wudangshan", "wanrongxian", "wenxixian", "wenteqi", "wushenqi",
              "wuqianqi", "wuzhongqi", "wuhouqi", "weizhoudao", "wenjiang", "wanzhou", "wuqing", "xiamen", "xian",
              "xining", "xingtai", "xinzhou", "xingan", "xilinguole", "xuzhou", "xuancheng", "xinyu", "xinxiang",
              "xuchang", "xinyang", "xiangyang", "xiaogan", "xianning", "xiantao", "xiangtan", "xiangxi",
              "xishuangbanna", "xianyang", "xilinhaote", "xichang", "xinji", "xinle", "xingtang", "xuanhua", "xinglong",
              "xianghe", "xushui", "xiongxian", "xianxian", "xingtaixian", "xinhe", "xiangyuan", "xiyang", "xiangfen",
              "xiangning", "xixian", "xiaoyi", "xingxian", "xinghe", "xinmin", "xifeng", "xinbin", "xiuyan",
              "xingcheng", "xunke", "xinyi", "xuyi", "xiangshui", "xinghua", "xincang", "xianju", "xiaoxian", "xiuning",
              "xiapu", "xiushui", "xingzi", "xinfeng", "xingguo", "xunwu", "xiajian", "jaxinganxian", "xiajin",
              "xintai", "xinzheng", "xinmi", "xingyang", "xinan", "xiuwu", "xinxiangxian", "xunxian", "xiangfuqu",
              "xiayi", "xuchangxian", "xcxiangcheng", "xixia", "xichuan", "xinye", "xyxixian", "xinxianxian",
              "xiangcheng", "xihua", "xiping", "xincha", "xiaocang", "xishui", "xingshan", "xuanen", "xianfeng",
              "xiangyin", "xiangxiang", "xiangtanxian", "xintian", "xinshao", "xinning", "xupu", "xinhuang", "xinhua",
              "xinfengxian", "xingning", "xinxing", "xinyishi", "xuwen", "xinganxian", "xingye", "xilin", "xiangzhou",
              "xincheng", "xinjin", "xichong", "xuyong", "xingwen", "xuanhan", "xiaojin", "xinliu", "gzzxiangcheng",
              "xide", "xiuwen", "xifengxian", "xishuixian", "xingyi", "xingren", "xundian", "xuanwei", "xinping",
              "ximeng", "xianggelila", "xiangyun", "xichou", "xietongmen", "xingping", "xunyi", "xixiang", "xunyang",
              "xihe", "xiahe", "xunhua", "xiji", "xiushan", "xinghai", "xiangshan", "xitang", "xinjiangxian", "xiaxian",
              "chenhuzuoqi", "chenhuyouqi", "xiwuqinqi", "xianghuangqi", "xidi", "xiandu", "xilingxueshan",
              "xijiangqianhu", "xizhou", "xindu", "xinhui", "xuecheng", "xinzhouwh", "yangzhou", "yangquan", "yuncheng",
              "yingkou", "yanbian", "yichun", "yancheng", "yingtan", "jiangxiyichun", "yantai", "yichang", "yueyang",
              "yiyang", "yongzhou", "yangjiang", "yunfu", "guangxiyulin", "yibin", "yaan", "yuxi", "yanan", "yulin",
              "yushu", "yinchuan", "yanji", "yiwu", "yuyao", "yizheng", "yixing", "yanqing", "yuanshi", "weixian",
              "yangyuan", "yutian", "yongqing", "bdyixian", "yanshan", "yongnian", "yangqu", "yingxian", "youyu",
              "yanggao", "yuxian", "yangcheng", "yuanping", "yushe", "yichengxian", "yonghe", "yakeshi", "jzyixian",
              "ccyushushi", "yongjixian", "yitong", "yian", "youyi", "yangzhong", "yongkang", "yuhuan", "yueqing",
              "yongjia", "yunhe", "yingshang", "yianqu", "yuexi", "hsyixian", "yongtai", "yongan", "youxi", "yongchun",
              "yongding", "yongxiu", "yujian", "yudu", "yushan", "sryiyang", "yugan", "yihuang", "yifeng", "yongfeng",
              "yongxin", "yanggu", "yucheng", "yiyuan", "yishui", "yinan", "yanzhou", "yutai", "yangxin",
              "yunchengxian", "yima", "yanshi", "lyyiyang", "yichuan", "yuanyang", "yanjin", "yongcheng", "yuchengxian",
              "yuzhou", "yanling", "yexian", "yunyangqu", "yunxi", "yicheng", "yingcheng", "yunmeng", "yingshan",
              "yangxinxian", "yidu", "yuanan", "yuanjian", "yueyangxian", "youxian", "yanlingxian", "yongxing",
              "yizhang", "yuanling", "yongshun", "yingde", "yangshan", "yunan", "yunanxian", "yangchun", "yangxi",
              "yangdong", "yangsu", "yongfu", "yizhou", "yanting", "yingshanxian", "yilong", "yuechi", "yibinxian",
              "yanbianxian", "yingjing", "yajian", "yanyuan", "yuexixian", "yuqing", "yuping", "yinjiang", "yanhe",
              "yiliang", "yimen", "yuanjiang", "yanjinxian", "yongshan", "yiliangxian", "yongsheng", "yulong",
              "yunxianxian", "yongde", "yingjian", "yongping", "yunliu", "yangbi", "yaoan", "yongren", "yuanmou",
              "yuanyangxian", "yanshanxian", "yadong", "yanchang", "yanchuan", "yichuanxian", "yijun", "yongshou",
              "yangxian", "yongdeng", "yuzhong", "yongcang", "yumen", "yongjing", "yushushi", "yongning", "yanchi",
              "yunyang", "youyang", "yongji", "yiling", "hengquxian", "yijinqi", "yabuli", "yandangshan", "yongchuan",
              "yangling", "yanliang", "zhengzhou", "zhuhai", "zhangjiakou", "zhenjiang", "zhoushan", "zhangzhou",
              "zibo", "zaozhuang", "zhoukou", "zhumadian", "zhuzhou", "zhangjiajie", "zhanjiang", "zhaoqing",
              "zhongshan", "zigong", "ziyang", "zunyi", "zhaotong", "zhangye", "zhongwei", "zhangjiagang", "zhuanghe",
              "zhengding", "zanhuang", "zhaoxian", "zhangbei", "zhuolu", "zunhua", "zhuozhou", "zaoqiang", "zuoyun",
              "zhezhou", "zuoquan", "zhongyang", "zalantun", "zhuozi", "zhangwu", "zhenlai", "zhaozhou", "zhaoyuanxian",
              "zhaodong", "zhuji", "zongyang", "zhenghe", "zhangpu", "zhangping", "zherong", "zhouning", "zixi",
              "zhangshu", "zhangqiu", "zhucheng", "zhaoyuan", "zoucheng", "zhanhua", "zouping", "zhongmo", "zhecheng",
              "zhenping", "zhengyang", "zhushan", "zhuxi", "zaoyang", "zhongxiang", "zhijian", "zigui", "zhuzhouxian",
              "zixing", "zhongfang", "zhijiang", "zijin", "ziyuan", "zhaoping", "zhongshanxian", "zitong", "zhongjian",
              "zizhong", "zhaojue", "zunyixian", "zhengan", "zhenning", "ziyun", "zhijin", "zhenyuan", "zhenfeng",
              "zhanyi", "zhenxiong", "zhenyuanzzxian", "zhenkang", "zuogong", "zhanang", "zhongba", "zhada", "zhouzhi",
              "zichang", "zhidan", "zhenba", "zizhou", "ziyangxian", "zhenpin", "zhenan", "zuoshui", "zhangjiachuan",
              "zhengning", "zhenyuanxian", "zhuanglang", "zhangxian", "zhuoni", "zhouqu", "zekun", "zaduo", "zhiduo",
              "zhongxian", "zhouzhuang", "zhaluteqi", "zhungeerqi", "zhalaiteqi", "zhengbaiqi", "zhenglanqi",
              "zhongningxian", "zhujiajian", "zichuan", "zhoucun", "zhenhai"]
    pool = ThreadPool(5)
    for city in cities:
        print("开始抓取%s的数据" % city)
        phone_list = list(set(get_phone_list(city)))
        print("%s的数据已经爬取完成" % city)
        f = open("phohe.txt", "a+")
        for phone in phone_list:
            if len(phone) == 11 and "-" not in phone and phone not in old_phone_list:
                f.write(phone + "\n")
                old_phone_list.append(phone)
        f.close()
