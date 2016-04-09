from django.shortcuts import render
from .models import Post
from django.contrib.auth.models import User
from django.utils import timezone
from .forms import PostForm
from django.shortcuts import redirect, get_object_or_404



def post_list(request):
    today=timezone.now()
    posts=Post.objects.filter(published_date__lte=today)
    users=User.objects.all()


    return render(request,'blog/post_list.html', {'posts':posts, 'users':users})
# Create your views here.

def post_detail(request, pk):
    today=timezone.now()
    posts=Post.objects.filter(published_date__lte=today)
    users=User.objects.all()
    post=posts.get(pk=pk)


    return render(request,'blog/post_detail.html', {'post':post})
def post_new(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
    else:
        form = PostForm()
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.published_date = timezone.now()
        post.save()
        return redirect('post_detail', pk=post.pk)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
