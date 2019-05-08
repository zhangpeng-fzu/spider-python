# _*_coding:utf-8_*_


from model.models import User


def find_one(account):
    return User.objects.filter(ACCOUNT=account)


def get_list():
    return User.objects.all()
