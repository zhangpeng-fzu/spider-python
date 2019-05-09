# _*_coding:utf-8_*_


from model.models import WhiteIP


def get_list():
    return WhiteIP.objects.all()


def save(ip, name):
    whiteip_db = WhiteIP(IP=ip, NAME=name)
    whiteip_db.save()


def delete(ids):
    ids_arr = ids.split(",")
    for wid in ids_arr:
        WhiteIP.objects.filter(id=wid).delete()
