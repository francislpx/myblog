from django.shortcuts import render, get_object_or_404

from .models import Post
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
