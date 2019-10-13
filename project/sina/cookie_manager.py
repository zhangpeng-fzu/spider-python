# coding=utf-8
cookies = [
    # zp
    "_T_WM=95ca63e574bf94d74fc0c9b284d1d582; SCF=AgZ3xgmGREeWkID4FJDNeBET7xC7a-N4i1y2RR-cI7XNMJ2UkRROd4470sA4a_8BAagRQ35CFRBkQG202WKtoP8.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh8NFjpvNEKOTAnQY.eSFS05JpX5K-hUgL.FoepSoq7eoeNeK22dJLoIEqLxKnLB.qLBoMLxKnLBoMLB-qLxK-L1h-L1hnLxKqLBKeLB-HS-ntt; TMPTOKEN=mLS5FNHln0fiVTugDOg7DW6rmlkxM65vbYwCzsMhWUOGuizLAN5d4KSaRFXhjdC6; SUB=_2A253VZYZDeRhGeVP7VQR8i3Lyj2IHXVUuTpRrDV6PUJbkdBeLVXHkW1NTV9JKZsb4CZxW7iiSiiUXIc4M-pkO3CJ; SUHB=0auw69TGouzIZi; SSOLoginState=1515316809",
    # #cyf
    "_T_WM=7db9f6a159c6163cc912e5fe5eceda9b; ALF=1517926202; SCF=AnygRqCOmGy3bfPLKd9S21f7w8k4BzHTyPtaJb64K0rfD2Z4ngmgMriDVhoh2XimjzCvMfNECtIBd-KLDaEh-Ts.; SUB=_2A253VlpqDeRhGeRL6FcR8CzFyj6IHXVUuWYirDV6PUNbktANLRb3kW1NUyp-6Cq7QWwukRFf_mqOIeaOYulX-JOL; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWd8wDlb_7TN44zVYsY6HMa5JpX5KMhUgL.Fozfe0-7ehz4eKz2dJLoIp7LxK-L1K5LB-Ski--4iKLFi-2Ri--fi-20i-z7; SUHB=0gHTpgqhKNaMVD",
    # xsz
    # "_T_WM=a64dc3026a0289b8d698df582c1f4de2; SCF=AtzUrkbiiF7FZ_IRN79BOHd6NcNVe09cLeUhFKpvrDHGKYV83SX5aa94LM3_VvgQV_9T-U5qL2pDnC_g_zVKifo.; SUB=_2A253QPxiDeRhGeNI4lIS8S7MzTiIHXVUyoQqrDV6PUJbkdBeLXLekW1NSA8q0yVyFhzkR2ovySdZacusOX0yqTD_; SUHB=0bt8VNX2GFSaha; SSOLoginState=1514441778",
    # tt
    "_T_WM=560e2ecafa50b9e3cd89962fbbf2b0a8; SUB=_2A253VZjJDeRhGeRH71cQ-C_LzjuIHXVUuTiBrDV6PUJbkdBeLVfNkW1NTaR0dxzpsrJKjBk3pWXm3A5RoJtMWFQW; SUHB=05iKnfyFU6HX78; SCF=Ar1jL_FsjDN87trHlWetu2fJS8z6XG0mKPsIKCPEmqsiaHjmTMr8nK2DKeszkOS7vhLu5Ggi6I3DzZNyB7zB2fQ.; SSOLoginState=1515317401"
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
    print("当前cookie:" + cookies[offset])
    offset = offset + 1
    if offset >= len(cookies):
        offset = 0


def get_head():
    return head
