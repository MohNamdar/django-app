from django import template
from ..models import Post, Comment
from django.db.models import Count, Max, Min
from markdown import markdown
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User

register = template.Library()


@register.simple_tag()
def total_posts():
    return Post.published.count()


@register.inclusion_tag('partials/most_popular_posts.html')
def most_popular_posts(count=3):
    posts = Post.published.annotate(comments_count=Count('comments')).order_by('-comments_count')[:count]
    context = {
        'posts': posts
    }
    return context


@register.simple_tag()
def total_comments():
    return Comment.actived.count()


@register.simple_tag()
def last_post_date():
    return Post.published.first().publish


@register.inclusion_tag('partials/latest_post.html')
def latest_post(count=4):
    l_post = Post.published.order_by('-publish')[:count]
    context = {
        'l_post': l_post
    }
    return context


@register.filter(name='markdown')
def to_markdown(text):
    return mark_safe(markdown(text))


@register.simple_tag()
def longest_reading_time(count=3):
    long_time = Post.published.all().order_by('-reading_time')[:count]
    return long_time


@register.simple_tag()
def shortest_reading_time(count=3):
    short_time = Post.published.all().order_by('reading_time')[:count]
    return short_time


@register.filter()
def censor(text):
    bad_words = ['بیشعور', 'احمق', 'حرومزاده']
    for bad_word in bad_words:
        text = text.replace(bad_word, '***')
    return text


@register.simple_tag()
def most_active_user():
    most_active = User.objects.annotate(post_count=Count('user_post')).order_by('-post_count')[0]
    return most_active


@register.simple_tag()
def post_own_count(user_id):
    post_count = User.objects.get(id=user_id).user_post.all().count()
    return post_count


@register.simple_tag()
def status_name(stat):
    if stat == 'DR':
        return 'منتشر نشده'
    elif stat == 'PD':
        return 'منتشر شده'
    elif stat == 'RJ':
        return 'رد شده'
