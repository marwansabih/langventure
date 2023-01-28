from django.urls import path
from . import views

urlpatterns = [
    path("story/<int:id>", views.story, name="story"),
    path("create_story/", views.create_story, name="create_story"),
    path("actor/<int:scene_id>", views.actor, name="actor"),
    path("create_character/<int:scene_id>", views.create_character, name="create_character"),
    path("dialog", views.dialog, name="dialog"),
    path("background/<int:scene_id>", views.set_background, name="background"),
    path("set_character_pos_scale/<int:char_id>", views.set_character_pos_scale, name="set_character_pos_scale"),
    path("get_dialog/<int:char_id>", views.get_dialog, name="get_dialog")
]