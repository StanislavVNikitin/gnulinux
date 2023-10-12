from operator import attrgetter
from django.views.generic import TemplateView

from gnulinux.models import Category, Post, Tag


# Create your views here.
class HomeView(TemplateView):
    template_name = "gnulinux/index-home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.filter(deleted=False)
        tags = Tag.objects.filter(posts__deleted=False)
        context['categories_menu'] = sorted(categories.order_by('-class_name')[:4], key=attrgetter('title'))
        post_pin = Post.objects.filter(deleted=False,is_published=True, pin=True).order_by('-created_at').first()
        posts = Post.objects.filter(deleted=False,is_published=True).exclude(pk=post_pin.pk).order_by('-views', '-created_at')
        if post_pin:
            context['post_pin'] =  post_pin
        if posts.exists():
            context['posts_most_read'] = posts[:4]
            if posts.count() > 4:
                context['posts_most_read_next'] = posts[4:8]
            if categories.exists():
                context['categories'] = categories
            if tags.exists():
                context['tags'] = tags
        return context