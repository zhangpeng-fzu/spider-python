# _*_coding:utf-8_*_


from model.models import User
from model.models import Role


def find_one(account):
    return User.objects.filter(ACCOUNT=account)


def get_list():
    users = User.objects.all()
    for one_user in users:
        role = Role.objects.filter(ROLE_NAME=one_user.ROLE)
        one_user.ROLE = role[0].DESCRIPTION
    return users


def delete(ids):
    ids_arr = ids.split(",")
    for wid in ids_arr:
        User.objects.filter(id=wid).delete()
