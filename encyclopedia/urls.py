from django.urls import path

from . import views

app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    
    # Entry page
    path("wiki/<str:entry>", views.entry, name="entry"),
    
    # Search
    path("search", views.search, name="search"),

    # New page
    path("new", views.new_entry, name="new"),

    # Edit page
    path("edit/<str:entry>", views.edit, name="edit"),

    # Random Page
    path("random", views.random, name="random")
]
