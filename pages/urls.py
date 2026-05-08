from .views import academy_video
from django.urls import path
from . import views

urlpatterns = [
    path("video/academy-intro/", academy_video, name="academy_video"),
    path("", views.home, name="home"),
    path("about/greeting/", views.greeting, name="greeting"),
    path("about/profile/", views.profile, name="profile"),
    path("about/awards/", views.awards, name="awards"),
    path("curriculum/", views.curriculum, name="curriculum"),
    path("admission/<slug:slug>/", views.admission_page, name="admission_page"),
]
