from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .form import AskformovieForm ,CommentForm
from .models import Post, Comment, PIN_POST,Askformovie, Download








def home(request):
    posts = Post.objects.filter(active=True).order_by('-id')
    pins = PIN_POST.objects.filter(active=True).order_by('-id')
    page = request.GET.get('page')
    paginator2 = Paginator(posts, 6)
    last_posts = paginator2.get_page(page)
    if request.method == "POST":
        query = request.POST['q']
        post = Post.objects.filter(Q(title__icontains=query))
    else:
        paginator = Paginator(posts, 4)
        post = paginator.get_page(page)


    last_posts = paginator2.get_page(page)

    return render(request, 'postapp/index.html', {
        'posts': post, 'pins': pins, 'last_post': last_posts

    })

def post_detail(request,slug):
    post = get_object_or_404(Post, slug=slug)
    post.visited = post.visited + 1
    post.save()



    posts = Post.objects.filter(active=True).order_by('-id')
    paginator2 = Paginator(posts, 6)
    page = request.GET.get('page')
    last_posts = paginator2.get_page(page)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)

            reply_obj = None
            try:
                reply_id = int(request.POST.get('reply_id'))
            except:
                reply_id = None
            if reply_id:
                reply_obj = Comment.objects.get(id=reply_id)

            name = comment_form.cleaned_data['name']
            body = comment_form.cleaned_data['body']
            email = comment_form.cleaned_data['email']

            Comment.objects.create(name=name, body=body, reply=reply_obj, email=email, post=post).save()

            return HttpResponseRedirect(slug)

    else:
        comment_form = CommentForm()
        comments = Comment.objects.filter(post=post, reply=None, active=True).order_by('created')
        links_movie = Download.objects.filter(post=post, active=True).order_by('order')
        links_subtitle = Download.objects.filter(post=post, active=False).order_by('order')

    return render(request, 'postapp/article.html', {'post': post, 'comments': comments,
                                                    'comment_form': comment_form, 'new_comment': new_comment,
                                                    'links_movie': links_movie,
                                                    'links_subtitle': links_subtitle, 'last_post': last_posts

                                                    })

def pin_detail(request,slug):
    post = get_object_or_404(PIN_POST, slug=slug)
    post.visited = post.visited + 1
    post.save()

    posts = Post.objects.filter(active=True).order_by('-id')
    paginator2 = Paginator(posts, 6)  #
    page = request.GET.get('page')
    last_posts = paginator2.get_page(page)
    new_comment = None
    if request.method == 'POST':
        comment_form = AskformovieForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)

            reply_obj = None
            try:
                reply_id = int(request.POST.get('reply_id'))
            except:
                reply_id = None
            if reply_id:
                reply_obj = Askformovie.objects.get(id=reply_id)

            name = comment_form.cleaned_data['name']
            body = comment_form.cleaned_data['body']
            email = comment_form.cleaned_data['email']

            Askformovie.objects.create(name=name, body=body, reply=reply_obj, email=email, post=post).save()

            return HttpResponseRedirect(slug)

    else:
        comment_form = AskformovieForm()
        comments = Askformovie.objects.filter(post=post, reply=None, active=True).order_by('created')

    return render(request, 'postapp/pinarticle.html', {'post': post, 'comments': comments,
                                                    'comment_form': comment_form, 'new_comment': new_comment,'last_post': last_posts


                                                    })







