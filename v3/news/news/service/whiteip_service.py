# _*_coding:utf-8_*_


from model.models import WhiteIP


def get_list():
    return WhiteIP.objects.all()


def save(ip, name):
    whiteip_db = WhiteIP(IP=ip, NAME=name)
    whiteip_db.save()


def check_ip(ip):
    ip_list = WhiteIP.objects.filter(IP=ip)
    if len(ip_list) > 0:
        return True
    return False


def delete(ids):
    ids_arr = ids.split(",")
    for wid in ids_arr:
        WhiteIP.objects.filter(id=wid).delete()
