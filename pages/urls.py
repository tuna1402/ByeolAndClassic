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
    path(
        "admission/yejung-piano/",
        views.admission_page,
        {"slug": "gwangju-arts-middle-piano-admission"},
        name="admission_yejung_piano",
    ),
    path(
        "admission/yego-piano/",
        views.admission_page,
        {"slug": "gwangju-arts-high-piano-admission"},
        name="admission_yego_piano",
    ),
    path(
        "admission/music-college-piano/",
        views.admission_page,
        {"slug": "music-college-piano-admission"},
        name="admission_music_college_piano",
    ),
    path(
        "admission/graduate-piano/",
        views.admission_page,
        {"slug": "piano-graduate-admission"},
        name="admission_graduate_piano",
    ),
    path("admission/<slug:slug>/", views.admission_page, name="admission_page"),
]
