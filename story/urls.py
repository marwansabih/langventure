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
    path("get_dialog/<int:char_id>", views.get_dialog, name="get_dialog"),
    path("set_scene_description/<int:scene_id>", views.set_scene_description, name="set_scene_description"),
    path("set_scene_name/<int:scene_id>", views.set_scene_name, name="set_scene_name"),
    path("update_story/<int:story_id>", views.update_story, name="update_story"),
    path("update_menu", views.update_menu, name="update_menu")
]