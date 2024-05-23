from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from .models import *
from .forms import *
from django.views.generic import ListView, DetailView
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.utils.text import slugify
# from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


# Create your views here.
def home(request):
    return render(request, "blog/homepage.html")


class PostListView(ListView):
    # model = Post
    queryset = Post.published.all()
    paginate_by = 2
    # template_name = "blog/list.html"
    context_object_name = "posts"


# class PostDetailsView(DetailView):
#     model = Post


def post_details(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    comment = None
    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'comment': comment
    }
    return render(request, "blog/post_detail.html", context)


def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Ticket.objects.create(name=cd["name"], subject=cd["subject"],
                                  message=cd["message"], phone=cd["phone"], email=cd["email"])
            return redirect("blog:ticket")

    else:
        form = TicketForm()
    return render(request, template_name='forms/ticket.html', context={"form": form})


@require_POST
def post_comment(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    context = {
        'post': post,
        'form': form,
        'comment': comment
    }
    return render(request, "forms/comments.html", context)


def new_post(request):
    form = NewPostForm()
    if request.method == "POST":
        form = NewPostForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = User.objects.get(id=request.POST['user'])
            post.slug = slugify(post.title, allow_unicode=True)
            des_word = len(post.description.split())
            post.reading_time = (des_word // 230) or 1
            post.save()
    context = {
        'form': form,
        'users': User.objects.all(),
    }
    return render(request, "forms/new_post.html", context)


def show_user(request, id):
    user = User.objects.get(id=id)
    context = {
        'user': user
    }
    return render(request, 'blog/user_show.html', context)


def post_search(request):
    query = None
    result = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_query = SearchQuery(query)
            # result = Post.published.filter(Q(title__contains=query) | Q(description__contains=query))
            # result = Post.published.filter(Q(title__search=query) | Q(description__search=query))
            search_vector = SearchVector('title', weight="B") + SearchVector('description', weight="A")

            result = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)) \
                .filter(rank__gte=0.3).order_by('-rank')

    context = {
        'result': result,
        'query': query
    }
    return render(request, 'blog/search.html', context)
