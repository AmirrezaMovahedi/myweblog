from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import HttpRequest, Http404, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import *

from .forms import *

import random


def index(request):
    posts = Post.published.all()
    num = random.randrange((posts.count() - 1))
    post = posts[num]
    return render(request, "blog/index.html", context={'post': post})


def post_list(request, category=None):
    if category is not None:
        posts = Post.published.filter(category=category)
    else:
        posts = Post.published.all()
    page_number = request.GET.get('page', 1)
    try:
        paginator = Paginator(posts, 2)
        posts = paginator.page(page_number)
    # except EmptyPage:
    #     posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    context = {
        "posts": posts,
        "category": category
    }

    return render(request, 'blog/post_list.html', context)


# class PostListView(ListView):
#     queryset = Post.published.all()
#     context_object_name = "posts"
#     paginate_by = 2
#     template_name = 'blog/post_list.html'


def post_detail(request, pk):
    post = Post.objects.get(id=pk)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {
        "post": post,
        "comments": comments,
        "form": form
    }

    return render(request, 'blog/post_detail.html', context)


# class PostDetailView(DetailView):
#     model = Post
#     template_name = 'blog/post_detail.html'


def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket_obj = Ticket.objects.create()
            cd = form.cleaned_data
            ticket_obj.message = cd['message']
            ticket_obj.name = cd['name']
            ticket_obj.phone = cd['phone']
            ticket_obj.email = cd['email']
            ticket_obj.subject = cd['subject']
            ticket_obj.save()
            return redirect("blog:index")

    else:
        form = TicketForm()
    return render(request, "forms/ticket.html", {"form": form})


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    form = CommentForm(data=request.POST)
    comment = None
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        "post": post,
        "form": form,
        "comment": comment

    }

    return render(request, "forms/comment.html", context)


def post_form(request):
    if request.method == "POST":
        pform = PostForm(data=request.POST)
        if pform.is_valid():
            cd = pform.cleaned_data
            post_object = Post.objects.create(author=cd["author"], reading_time=cd["reading_time"])
            # post_object.author = cd["author"]
            post_object.title = cd["title"]
            post_object.description = cd["description"]
            post_object.slug = cd["slug"]
            post_object.status = cd["status"]
            post_object.publish = cd["publish"]
            # post_object.reading_time = cd["reading_time"]
            post_object.save()
            return redirect("blog:post_list")
    else:
        pform = PostForm()
    return render(request, "forms/postform.html", {"pform": pform})


def post_search_view(request):
    query = None
    result = []
    if "query" in request.GET:
        form = SearchFrom(request.GET)
        if form.is_valid():
            # query = form.cleaned_data['query']
            # result1 = Post.published.filter(description__icontains=query)
            # result2 = Post.published.filter(title__icontains=query)
            # result = result1 | result2

            # Use Q objects
            # query = form.cleaned_data['query']
            # result = Post.objects.filter(Q(description__icontains=query) | Q(title__icontains=query))

            # Use FTS
            # query = form.cleaned_data['query']
            # search_query = SearchQuery(query)
            # search_vector = SearchVector('title', 'description')
            # result = Post.objects.annotate(search=search_vector, search_rank=SearchRank(search_vector,search_query)).filter(search=search_query).order_by('-search_rank')

            # Use trgm
            query = form.cleaned_data['query']
            result1 = Post.objects.annotate(trgm=TrigramSimilarity('title', query)).filter(trgm__gt=0.1)
            result2 = Post.objects.annotate(trgm=TrigramSimilarity('description', query)).filter(trgm__gt=0.1)
            result3 = Image.objects.annotate(trgm=TrigramSimilarity('title', query)).filter(trgm__gt=0.1)
            result4 = Image.objects.annotate(trgm=TrigramSimilarity('description', query)).filter(trgm__gt=0.1)
            result_mg = (result3 | result4)
            result_mg2 = Post.published.filter(images__in=result_mg)

            result = ((result1 | result2 | result_mg2).order_by('-trgm'))

    return render(request, 'forms/search_post.html', {'query': query, 'result': result, 'reslult_mg': result_mg})


@login_required()
def profile(request):
    user = request.user
    posts = Post.published.filter(author=user)
    page_number = request.GET.get('page', 1)
    try:
        paginator = Paginator(posts, 3)
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    return render(request, 'blog/profile.html', {'posts': posts})


@login_required()
def create_post(request):
    if request.method == "POST":
        user = request.user
        form = CreatePost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.save()
            Image.objects.create(post=post, image_file=form.cleaned_data['image'])
            return redirect('blog:profile')

    else:
        form = CreatePost()
    return render(request, 'forms/create_post.html', {'form': form, 'name': 'create '})


def post_delete(request, pk):
    if request.method == "POST":
        post = get_object_or_404(Post, id=pk)
        post.delete()
        return redirect('blog:profile')
    else:
        post = get_object_or_404(Post, id=pk)
        return render(request, 'forms/post_delete.html', {'post': post})


def post_update(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == "POST":
        user = request.user
        form = CreatePost(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post.save()
            Image.objects.create(post=post, image_file=form.cleaned_data['image'])
            return redirect('blog:profile')


    else:
        form = CreatePost(instance=post)
    return render(request, 'forms/create_post.html', {'form': form, 'post': post, 'name': 'update'})


def image_delete(request, image_id):
    image = Image.objects.get(id=image_id)
    image.delete()
    return redirect('blog:profile')


# def user_login(request):
#     if request.method == "POST":
#         form = User_Login(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect('blog:profile')
#                 else:
#                     return HttpResponse('You are not logged in ')
#             else:
#                 return HttpResponse('it was not exist')
#
#     else:
#         form = User_Login()
#         return render(request,'forms/login.html', {'form': form})


def user_register_view(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            Account.objects.create(user=user)
            return render(request, 'registration/register_done.html', {'user': user})

    else:
        form = UserRegister()
    return render(request, 'registration/register_form.html', {'form': form})


@login_required()
def account_edit(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        account_form = AccountForm(request.POST, request.FILES, instance=request.user.account)

        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()
            return redirect('blog:profile')

    else:
        user_form = UserForm(instance=request.user)
        account_form = AccountForm(instance=request.user.account)
    return render(request, 'registration/account_edit.html', {'user_form': user_form, 'account_form': account_form})


def account_view(request, u):
    account = get_object_or_404(Account, user_id=u)
    posts = Post.published.filter(author_id=u)

    return render(request, 'blog/account_view.html', {'account': account, 'posts': posts})
