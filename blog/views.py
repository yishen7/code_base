from django.shortcuts import render, get_object_or_404
from .models import Post
import markdown
from .models import Post, Category
from comments.forms import CommentForm

def index(request):
    post_list = Post.objects.all()
    return render(request, 'blog/index.html', context={'post_list':post_list})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 每次打开文章时阅读量 +1
    post.increase_views()

    post.body = markdown.markdown(post.body,
                                  extensions=[
                                    'markdown.extensions.extra',
                                    'markdown.extensions.codehilite',
                                    'markdown.extensions.toc',
                                  ])
    form = CommentForm()
    comment_list = post.comment_set.all()
    # 获取这篇 post 下的全部评论
    context = {'post': post,
                'form': form,
                'comment_list': comment_list,
                }
    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    return render(request, 'blog/detail.html', context=context)

def archives(request, year, month):
    # 注意这里 created_time 是 Python 的 date 对象，其有一个 year 和 month 属性,
    # Python 中类实例调用属性的方法通常是 created_time.year，但是由于这里作为函数的参数列表，
    # 所以 Django 要求我们把点替换成了两个下划线，即 created_time__year。
    post_list = Post.objects.filter(created_time__year=year, created_time__month=month).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list':post_list})

def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate)
    return render(request, 'blog/index.html', context={'post_list':post_list})