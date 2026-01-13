from django.urls import path
from . import views

urlpatterns = [
    path("<slug:category_code>/", views.category_list, name="news_category"),
    path("<slug:category_code>/<slug:slug>/", views.detail, name="news_detail"),
]
