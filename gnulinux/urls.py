from django.urls import path
from .apps import GnulinuxConfig

from .views import *

app_name = GnulinuxConfig.name

urlpatterns = [
    path("category/<str:slug>", PostByCategory.as_view(), name="category"),
    path("tag/<str:slug>", PostByTag.as_view(), name="tag"),
    path("post/<str:slug>", SinglePostView.as_view(), name="post"),
    path("allposts", AllPostsListView.as_view(), name="allposts"),
    path("", HomeView.as_view(), name="home"),
]