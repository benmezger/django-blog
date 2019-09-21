from django.urls import path

from blog import views

urlpatterns = [
    path("", views.PostList.as_view(), name="home"),
    path("post/<slug:slug>/", views.PostDetail.as_view(), name="post_detail"),
    path("page/<slug:slug>/", views.PageDetail.as_view(), name="page_detail"),
]
