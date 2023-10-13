from django.db.models import F
from django.views.generic import TemplateView, ListView, DetailView

from gnulinux.models import Category, Post, Tag


# Create your views here.
class HomeView(TemplateView):
    template_name = "gnulinux/index-home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pin = Post.objects.filter(deleted=False,is_published=True, pin=True).order_by('-created_at').first()
        posts = Post.objects.filter(deleted=False,is_published=True).exclude(pk=post_pin.pk).order_by('-views', '-created_at')
        if post_pin:
            context['post_pin'] =  post_pin
        if posts.exists():
            context['posts_most_read'] = posts[:4]
            if posts.count() > 4:
                context['posts_most_read_next'] = posts[4:8]
        return context

class AllPostsListView(ListView):
    template_name = "gnulinux/view_posts.html"
    context_object_name = "posts"
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(deleted=False).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts_most_read'] = Post.objects.filter(deleted=False,is_published=True).order_by('-views', '-created_at')[:4]
        context['title'] = 'Все новости'
        return context

class PostByCategory(ListView):
    template_name = "gnulinux/view_posts.html"
    context_object_name = "posts"
    paginate_by = 4
    allow_empty= False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts_most_read'] = Post.objects.filter(deleted=False, is_published=True).order_by('-views','-created_at')[:4]
        context["title"] = Category.objects.get(slug=self.kwargs['slug'])
        return context

class PostByTag(ListView):
    template_name = "gnulinux/view_posts.html"
    context_object_name = "posts"
    paginate_by = 4
    allow_empty= False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts_most_read'] = Post.objects.filter(deleted=False, is_published=True).order_by('-views','-created_at')[:4]
        context["title"] = "#" + Tag.objects.get(slug=self.kwargs['slug']).title
        return context

class SinglePostView(DetailView):
    model = Post
    template_name = 'gnulinux/single-post.html'
    context_object_name = "post"
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views')  + 1
        self.object.save()
        self.object.refresh_from_db()
        return context