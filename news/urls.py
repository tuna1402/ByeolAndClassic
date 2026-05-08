from django.urls import path
from . import views

urlpatterns = [
    path("notice/", views.notice_list, name="notice_list"),
    path("info/", views.guide_info, name="guide_info"),
    path("<slug:category_code>/", views.category_list, name="news_category"),
    path("<slug:category_code>/<slug:slug>/", views.detail, name="news_detail"),
]
