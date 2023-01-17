from django.urls import path
from . import views

urlpatterns = [
    path("story/<int:id>", views.story, name="story"),
    path("create_story/", views.create_story, name="create_story"),
    path("actor", views.actor, name="actor"),
    path("dialog", views.dialog, name="dialog"),
    path("background/<int:story_id>", views.set_background, name="background")
]