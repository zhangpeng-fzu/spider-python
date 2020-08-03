# _*_coding:utf-8_*_


from model.models import News


def delete(news_id):
    news = News.objects.get(NEWS_ID=news_id)
    news.delete()


def delete_all():
    News.objects.all().delete()


def get_list():
    return News.objects.all()
