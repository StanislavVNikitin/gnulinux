from django.core.mail import send_mail
from django.db.models import F, Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView

from django.contrib import messages
from django.conf import settings
from gnulinux.forms import ContactForm
from gnulinux.models import Category, Post, Tag, Page


# Create your views here.
class HomeView(TemplateView):
    template_name = "gnulinux/index-home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_pin = Post.objects.filter(deleted=False,is_published=True, pin=True).order_by('-created_at').first()
        posts = Post.objects.filter(deleted=False,is_published=True).order_by('-views', '-created_at')
        if post_pin:
            posts = posts.exclude(pk=post_pin.pk)
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
        return Post.objects.filter(deleted=False,is_published=True).order_by('-created_at')

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
        post_pin = Post.objects.filter(category__slug=self.kwargs['slug'], deleted=False, is_published=True,
                                       pin=True).order_by('-created_at').first()
        posts = Post.objects.filter(deleted=False,is_published=True, category__slug=self.kwargs['slug'])
        if post_pin:
            return posts.exclude(pk=post_pin.pk)
        return posts


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['slug'])
        post_pin = Post.objects.filter(category__slug=self.kwargs['slug'], deleted=False, is_published=True, pin=True).order_by('-created_at').first()
        if post_pin:
            context['post_pin'] =  post_pin
        context['posts_most_read'] = Post.objects.filter(deleted=False, is_published=True).order_by('-views','-created_at')[:4]
        if category.photo:
            context['category'] = category
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
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
    queryset = Post.objects.filter(deleted=False,is_published=True)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts_most_read'] = Post.objects.filter(deleted=False, is_published=True).exclude(slug=self.kwargs['slug']).order_by('-views',
                                                                                                    '-created_at')[:4]
        self.object.views = F('views')  + 1
        self.object.save()
        self.object.refresh_from_db()
        return context

class PageView(DetailView):
    model = Page
    template_name = 'gnulinux/page.html'
    context_object_name = "page_content"
    queryset = Page.objects.filter(deleted=False)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Page.objects.get(slug=self.kwargs['slug'])
        return context


class Search(ListView):
    template_name = 'gnulinux/search.html'
    context_object_name = "posts"
    paginate_by = 4
    def get_queryset(self):
        return Post.objects.filter(Q(Q(title__icontains=self.request.GET.get('s'))| Q(content__icontains=self.request.GET.get('s'))))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('s')
        context['s'] = f"s={self.request.GET.get('s')}&"
        return context

class ContactViewAndSendMessage(FormView):
    template_name = 'gnulinux/contact.html'
    form_class = ContactForm
    http_method_names = ['get','post']

    def post(self,request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            subject_mail = 'Сообщение с формы Контактов с сайта Gnulinux'
            content_mail = f'Вам отправлено письмо с формы обратной связи сайта Gnulinux\nEmail отправителя: {form.cleaned_data["email"]}\nТекст сообщения: {form.cleaned_data["content"]}'
            mail = send_mail(subject_mail, content_mail, settings.EMAIL_HOST_USER, [settings.ADMIN_MAIL_ADDRESS],
                             fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено!')
                return HttpResponseRedirect('contact')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации')
        return TemplateResponse(request, self.template_name , {"form": form, "page": self.get_post_contact()})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = self.get_post_contact()
        print(context)
        return context

    def get_post_contact(self,page_name='contact'):
        return Page.objects.filter(slug=page_name).first()






