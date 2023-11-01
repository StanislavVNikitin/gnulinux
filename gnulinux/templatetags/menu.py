from operator import attrgetter
from django import template
from django.db.models import Count, Q

from gnulinux.models import Category

register = template.Library()

@register.inclusion_tag('gnulinux/menu_top_tpl.html')
def show_menu_top(menu_class='menu'):
    categories = sorted(Category.objects.annotate(cnt=Count('posts', filter=Q(posts__deleted=False,posts__is_published=True))).filter(cnt__gt=0).order_by('-class_name')[:4], key=attrgetter('title'))
    return {"categories": categories, "menu_class": menu_class}
