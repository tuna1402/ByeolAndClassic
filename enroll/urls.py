from django.urls import path
from . import views

urlpatterns = [
    path("", views.form, name="enroll_form"),
]
