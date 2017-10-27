from django.shortcuts import render, get_object_or_404

from .models import Post, Category
import markdown


def index(request):
    posts = Post.objects.all().order_by('-create_time')
    return render(request, 'blog/index.html', context={'posts': posts})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # markdown渲染detail
    post.body = markdown.markdown(post.body,
                                  extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc', ])
    return render(request, 'blog/detail.html', context={'post': post})


def archives(request, year, month):
    posts = Post.objects.filter(create_time__year=year,
                                create_time__month=month
                                ).order_by('-create_time')
    return render(request, 'blog/index.html', context={'posts': posts})


def categories(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(category=category).order_by('-create_time')
    return render(request, 'blog/index.html', context={'posts': posts})