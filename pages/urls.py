from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/greeting/", views.greeting, name="greeting"),
    path("about/profile/", views.profile, name="profile"),
    path("about/awards/", views.awards, name="awards"),
    path("curriculum/", views.curriculum, name="curriculum"),
    path("business/accompanist/", views.accompanist, name="accompanist"),
    path("business/soloist/", views.soloist, name="soloist"),
    path("business/masterclass/", views.masterclass, name="masterclass"),
]
