from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import markdown
from django.utils.html import strip_tags


class Category(models.Model):
    """
    CharField 字符类型
    DateTimeField 日期时间类型
    IntegerField 整数类型
    其他：https://docs.djangoproject.com/en/1.10/ref/models/fields/#field-types
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)
    # 摘要，允许为空
    excerpt = models.CharField(max_length=200, blank=True)

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(User)
    is_delete = models.IntegerField(default=1)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title if len(self.title) > 20 else self.title[:20]

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 重写save方法，此方法并不算好
    # def save(self, *args, **kwargs):
    #     # 没有摘要的情况下
    #     if not self.excerpt:
    #         # 实例化一个Markdown类，渲染body
    #         md = markdown.Markdown(extensions=[
    #             'markdown.extensions.extra',
    #             'markdown.extensions.codehilite',
    #         ])
    #         # 先将Markdown渲染成html
    #         # strip_tags 去掉html里面的html标签，
    #         # 然后截取54个字符赋值给excerpt
    #         self.excerpt = strip_tags(md.convert(self.body))[:54]
    #     # 调用父类的save方法存储数据
    #     super().save(*args, **kwargs)

    class Meta:
        ordering = ['-create_time']
