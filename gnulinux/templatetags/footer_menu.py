from django import template

from gnulinux.models import Category

register = template.Library()

@register.inclusion_tag('gnulinux/categories_footer_tpl.html')
def get_category_footer(cnt=4):
    posts = Category.objects.all()[:cnt]
    return {"categories": posts}