from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name = "entry"),
    path("search/", views.search, name = "search"),
    path("createpage/", views.createPage, name = "createpage"),
    path("editpage/<str:title>", views.editPage, name = "editpage"),
    path("random/", views.randomPage, name = "randompage"),
    path("error/<str:message>", views.error, name = "error")
]
