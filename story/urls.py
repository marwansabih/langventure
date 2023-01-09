from django.urls import path
from . import views

urlpatterns = [
    path("story/<int:id>", views.story, name="story"),
    path("actor", views.actor, name="actor"),
    path("dialog", views.dialog, name="dialog")
]