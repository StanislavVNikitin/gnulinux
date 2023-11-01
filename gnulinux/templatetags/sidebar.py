from operator import attrgetter

from django import template
from django.db.models import Count, Q

from gnulinux.models import Post, Tag, Category

register = template.Library()


@register.inclusion_tag('gnulinux/popular_posts_tpl.html')
def get_popular_sidebar(cnt=3):
    posts = Post.objects.order_by('-views')[:cnt]
    return {"posts": posts}

@register.inclusion_tag('gnulinux/categories_tpl.html')
def get_category_sidebar():
    categories = Category.objects.annotate(cnt=Count('posts',filter=Q(posts__deleted=False,posts__is_published=True))).filter(cnt__gt=0).order_by('title')
    return {"categories": categories}

@register.inclusion_tag('gnulinux/tags_tpl.html')
def get_tags_sidebar():
    tags = Tag.objects.all()
    return {"tags": tags}
