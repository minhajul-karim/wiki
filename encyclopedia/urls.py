from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.display_entry, name="display_entry"),
    path("search", views.search, name="search"),
    path("create-page", views.create_page, name="create_page"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
    path("random-page", views.random_page, name="random_page")
]
