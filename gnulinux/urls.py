from django.urls import path
from .apps import GnulinuxConfig

from .views import *

app_name = GnulinuxConfig.name

urlpatterns = [
    path("category/<str:slug>", HomeView.as_view(), name="category"),
    path("tag/<str:slug>", HomeView.as_view(), name="tag"),
    path("post/<str:slug>", HomeView.as_view(), name="post"),
    path("", HomeView.as_view(), name="home"),
]