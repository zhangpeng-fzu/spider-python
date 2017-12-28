# coding=utf-8
cookies = [
    #zp
    "_T_WM=95ca63e574bf94d74fc0c9b284d1d582; H5_INDEX_TITLE=%E8%BF%B7%E8%B7%AF%E5%85%88%E6%A3%AEMR; H5_INDEX=2; ALF=1517065575; SCF=AgZ3xgmGREeWkID4FJDNeBET7xC7a-N4i1y2RR-cI7XNMJ2UkRROd4470sA4a_8BAagRQ35CFRBkQG202WKtoP8.; SUB=_2A253QX32DeRhGeVP7VQR8i3Lyj2IHXVUygO-rDV6PUJbktANLUbDkW1NTV9JKaAOi_1FhwzvB3JAFLWIfwjl0puu; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh8NFjpvNEKOTAnQY.eSFS05JpX5K-hUgL.FoepSoq7eoeNeK22dJLoIEqLxKnLB.qLBoMLxKnLBoMLB-qLxK-L1h-L1hnLxKqLBKeLB-HS-ntt; SUHB=0rrLolyy9Zlt-f; SSOLoginState=1514474918",
    #cyf
    "_T_WM=23704b00f5091c499c99d05cd0463c78; _T_WL=1; _WEIBO_UID=2535002912; ALF=1517033759; SCF=Auy9Jjb3emibplWvgNUYK3_zziW0b-tHpNbvRndNmStWjeu8FusFEPE_mL-NDrgf1oQxYjaoQZjccsXcJlKfw3Y.; SUB=_2A253QPxwDeRhGeRL6FcR8CzFyj6IHXVUyoQ4rDV6PUNbktBeLWr6kW1NUyp-6FuhZWCWlNM8q5JbmZZTsaXSAYC2; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWd8wDlb_7TN44zVYsY6HMa5JpX5KMhUgL.Fozfe0-7ehz4eKz2dJLoIp7LxK-L1K5LB-Ski--4iKLFi-2Ri--fi-20i-z7; SUHB=00xYsLQkTubt2t; SSOLoginState=1514441760",
    #xsz
    "_T_WM=a64dc3026a0289b8d698df582c1f4de2; SCF=AtzUrkbiiF7FZ_IRN79BOHd6NcNVe09cLeUhFKpvrDHGKYV83SX5aa94LM3_VvgQV_9T-U5qL2pDnC_g_zVKifo.; SUB=_2A253QPxiDeRhGeNI4lIS8S7MzTiIHXVUyoQqrDV6PUJbkdBeLXLekW1NSA8q0yVyFhzkR2ovySdZacusOX0yqTD_; SUHB=0bt8VNX2GFSaha; SSOLoginState=1514441778",
    #tt
    "SSOLoginState=1514443018; ALF=1517035017; SCF=AvmdBey9PCywGrDVSWhqbx84-vkT3NzoWW7xGpeCT6WeNr9NSAnG7nw85ItwBjtBRZBYOAHTkGl0cOgCFepxr8U.; SUB=_2A253QOFaDeRhGeRH71cQ-C_LzjuIHXVUyo8SrDV6PUNbktBeLXmgkW1NTaR0dyOGHPGExoEzX9NtTtgPAujBmvjE; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF7ElhQkzKU5.1bJyRg3b_-5JpX5KMhUgL.Foz4Sh-p1h2NSKM2dJLoIEBLxKnLB.qLB.BLxKqLBKzLBKqLxKqL1KnL1-qLxK-LBK.LBoMt; SUHB=0V5Va398GVjzD5; _T_WM=6c341a293c081f630505682c405857ba"
    ]
head = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': cookies[0],
    'Pragma': 'no-cache',
    'Referer': 'https://login.sina.com.cn/sso/login.php?url=https%3A%2F%2Fweibo.cn%2F3166023711%2Finfo&_rand=1514206231.9481&gateway=1&service=sinawap&entry=sinawap&useticket=1&returntype=META&sudaref=&_client_version=0.6.26',
    'User-Agent': 'Mozilla/5.0 (Macintoshintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Request': 'json',
    'X-Requested-With': 'XMLHttpRequest'
}

offset = 0


def change_cookie():
    global offset
    head['Cookie'] = cookies[offset]
    offset = offset + 1
    if offset >= len(cookies):
        offset = 0


def get_head():
    return head
