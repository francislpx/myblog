from django.shortcuts import render, get_object_or_404
from comments.forms import CommentForm
from .models import Post, Category, Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import markdown


def index(request):
    all_posts = Post.objects.all()
    return posts_paginator(all_posts, request)


def posts_paginator(all_posts, request):
    """ 文章分页 """

    # 10篇文章分页
    paginator = Paginator(all_posts, 10)
    page = request.GET.get('page')
    try:
        page = int(page) if page else 1
    except TypeError:
        page = 1
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:  # 如果页码太大，没有相应的记录
        posts = paginator.page(paginator.num_pages)  # 取最后一页的记录
    page_data = get_page_data(paginator.num_pages, page)
    return render(request, 'blog/index.html', context={'posts': posts, 'page': page_data})


def get_page_data(total, current_page_number):
    """ 计算分页相关数据 """

    # 上一页按钮是否可以按
    pre_button = True if int(current_page_number) > 1 else False
    # 下一页按钮是否可以按
    next_button = True if int(current_page_number) < total else False
    # 左侧显示的页数列表
    left_page_numbers = range(1, 4)
    # 右侧显示的页数列表
    right_page_numbers = [total - 2, total - 1, total]
    middle_page_numbers = []
    # 左侧省略号是否显示
    left_ellipsis = True
    # 右侧省略号是否显示
    right_ellipsis = False
    if total < 10:
        left_page_numbers = range(1, total + 1)
        left_ellipsis = False
        right_page_numbers = []

    else:
        if current_page_number < 6:
            if current_page_number > 2:
                left_page_numbers = range(1, current_page_number + 2)
                # if total - 2 > current_page_number:
                left_ellipsis = False
                right_ellipsis = True

        elif total - current_page_number > 4:
            right_ellipsis = True
            middle_page_numbers = [current_page_number - 1, current_page_number, current_page_number + 1]
        else:
            right_page_numbers = range(current_page_number - 1, total + 1)

    pre_page_number = current_page_number - 1 if current_page_number > 1 else 1
    next_page_number = current_page_number + 1 if current_page_number < total else total

    page_data = {'current_page': current_page_number, 'pre_button': pre_button, 'next_button': next_button,
                 'left_page_numbers': left_page_numbers, 'middle_page_numbers': middle_page_numbers,
                 'right_page_numbers': right_page_numbers, 'left_ellipsis': left_ellipsis,
                 'right_ellipsis': right_ellipsis, 'pre_page_number': pre_page_number,
                 'next_page_number': next_page_number}
    return page_data


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 阅读量+1
    post.increase_views()
    # markdown渲染detail
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc', ])
    form = CommentForm()
    comments = post.comments_set.all()
    context = {'post': post,
               'form': form,
               'comments': comments}
    return render(request, 'blog/detail.html', context=context)


def archives(request, year, month):
    """ 归档（按照年月） """
    posts = Post.objects.filter(create_time__year=year,
                                create_time__month=month
                                )
    return posts_paginator(posts, request)


def categories(request, pk):
    """ 目录 """
    category = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(category=category)
    return posts_paginator(posts, request)


def get_posts_by_tag(request, pk):
    """ 标签 """
    tag = get_object_or_404(Tag, pk=pk)
    posts = Post.objects.filter(tags=tag)
    return posts_paginator(posts, request)