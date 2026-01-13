from django.urls import path
from . import views

urlpatterns = [
    path("", views.form, name="contact_form"),
]
