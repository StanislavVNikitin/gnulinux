from django.urls import path
from .apps import GnulinuxConfig

from .views import *

app_name = GnulinuxConfig.name

urlpatterns = [
    path("search/", Search.as_view(), name="search"),
    path("contact", ContactViewAndSendMessage.as_view(), name="contact"),
#    path("sendcontact", SendContactMessage.as_view(), name="sendcontact"),
    path("category/<str:slug>", PostByCategory.as_view(), name="category"),
    path("tag/<str:slug>", PostByTag.as_view(), name="tag"),
    path("post/<str:slug>", SinglePostView.as_view(), name="post"),
    path("page/<str:slug>", PageView.as_view(), name="page"),
    path("allposts", AllPostsListView.as_view(), name="allposts"),
    path("", HomeView.as_view(), name="home"),
]