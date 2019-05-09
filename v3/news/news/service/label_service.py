# _*_coding:utf-8_*_


from model.models import Label


def get_list():
    return Label.objects.all()


def save(name,description):
    label_db = Label(NAME=name,DESCRIPTION=description)
    label_db.save()


def delete(ids):
    ids_arr = ids.split(",")
    for wid in ids_arr:
        Label.objects.filter(id=wid).delete()
