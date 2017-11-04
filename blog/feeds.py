from django.contrib.syndication.views import Feed
from .models import Post


class AllPostsRssFeed(Feed):
    # 显示在聚合阅读器上的标题
    title = "Simba's Blog"
    # 通过聚合阅读器跳转到网站的地址
    link = '/'
    # 显示在聚合阅读器上的描述信息
    description = "Simba's Blog Django学习"

    def item_title(self, item):
        return '[%s] %s' % (item.category, item.title)

    def item_description(self, item):
        return item.body
