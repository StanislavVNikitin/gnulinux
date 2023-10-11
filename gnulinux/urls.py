from django.urls import path
from .apps import GnulinuxConfig

from .views import *

app_name = GnulinuxConfig.name

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]