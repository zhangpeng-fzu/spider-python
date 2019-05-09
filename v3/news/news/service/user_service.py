# _*_coding:utf-8_*_


from model.models import User


def find_one(account):
    return User.objects.filter(ACCOUNT=account)


def get_list():
    return User.objects.all()


def delete(ids):
    ids_arr = ids.split(",")
    for wid in ids_arr:
        User.objects.filter(id=wid).delete()
