from ..models import Post, Comment, User
from django import template
from django.db.models import Count
from markdown import markdown
from django.utils.safestring import mark_safe

from django.db.models import Max, Min , Sum

register = template.Library()


@register.simple_tag()
def post_tag():
    t = Post.published.count()
    return t


@register.simple_tag()
def comment_tag():
    t = Comment.objects.filter(active=True).count()
    return t


@register.simple_tag()
def post_publish_tag():
    t = Post.objects.last()
    return t.publish


@register.simple_tag()
def best_post(count=2):
    return Post.published.annotate(comments_count=Count('reading_time')).order_by('comments_count')[:count]


@register.inclusion_tag("blog/latest_post.html")
def latest_post(count=4):
    l_posts = Post.published.order_by("-publish")[:count]
    context = {
        "l_posts": l_posts,
    }
    # return {'test': lposts}
    return context


@register.filter(name='markdown')
def to_markdown(text):
    return mark_safe(markdown(text))


@register.inclusion_tag('blog/m_and_n.html')
def m_and_n():
    ma = Post.published.aggregate(Max('reading_time'))
    mi = Post.published.aggregate(Min('reading_time'))
    context = {
        'min': mi['reading_time__min'],
        'max': ma['reading_time__max']
    }
    return context


@register.filter(name='sansor')
def sansor(text):
    l = ['بیشعور', 'عوضی', 'کثافت', 'تخمی ', 'حرومزاده']
    t = text.split()
    for index, word in enumerate(t):
        if word in l:
            t[index] = len(word) * '*'
    final_text = ' '.join(t)
    return final_text


@register.simple_tag()
def best_user():
    users = User.objects.annotate(n_posts=Sum('user_posts'))
    b_u = users.aggregate(Max('n_posts'))
    final_user = users.filter(n_posts=b_u['n_posts__max'])
    f_u = final_user.first()
    return f_u.username




