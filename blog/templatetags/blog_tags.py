from django import template
from ..models import Post, Category, Tag
import markdown
from django.utils.html import strip_tags
from django.db.models.aggregates import Count

register = template.Library()


@register.simple_tag()
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-create_time')[:num]


@register.simple_tag()
def archives():
    return Post.objects.dates('create_time', 'month', order='DESC')


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.filter
def get_excerpt(excerpt, body):
    """
    如果文章没有摘要，自动截取文章内容前n个字符作为摘要
    :param excerpt: 摘要
    :param body: 文章内容
    :return:
    """

    if not excerpt:
        # 实例化一个Markdown类，渲染body
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        # 先将Markdown渲染成html
        # strip_tags 去掉html里面的html标签，
        # 然后截取54个字符赋值给excerpt
        auto_excerpt = strip_tags(md.convert(body))[:54]
        return auto_excerpt
    else:
        return excerpt


@register.simple_tag()
def get_category_count():
    # Count 计算分类下的文章数，其接受的参数为需要计数的模型的名称
    return Category.objects.annotate(num_post=Count('post')).filter(num_posts__gt=0)


@register.simple_tag()
def get_tags():
    return Tag.objects.annotate(num_post=Count('post'))
