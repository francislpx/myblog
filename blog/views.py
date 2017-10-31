from django.shortcuts import render, get_object_or_404
from comments.forms import CommentForm
from .models import Post, Category
import markdown


def index(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', context={'posts': posts})


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
    posts = Post.objects.filter(create_time__year=year,
                                create_time__month=month
                                )

    return render(request, 'blog/index.html', context={'posts': posts})


def categories(request, pk):
    category = get_object_or_404(Category, pk=pk)
    posts = Post.objects.filter(category=category)
    return render(request, 'blog/index.html', context={'posts': posts})
