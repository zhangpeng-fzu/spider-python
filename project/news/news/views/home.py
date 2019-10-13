from django.http import HttpResponseRedirect


def index(request):
    return HttpResponseRedirect('/static/index.html')
