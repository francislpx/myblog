from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    # return HttpResponse('欢迎访问我的Blog')
    return render(request, 'blog/index.html', context={
        'title': '首页',
        'welcome': '欢迎访问我的博客'
    })
