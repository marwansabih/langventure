from django.urls import path
from . import views

urlpatterns = [
    path("story/<int:id>", views.story, name="story"),
    path("story_scene/<int:id>/<int:scene_id>", views.story_scene, name="story_scene"),
    path("create_story/", views.create_story, name="create_story"),
    path("actor/<int:scene_id>", views.actor, name="actor"),
    path("collectible/<int:scene_id>", views.collectible, name="collectible"),
    path("edit_actor/<int:actor_id>", views.edit_actor, name="edit_actor"),
    path("get_actor_info/<int:actor_id>", views.get_character_info, name="get_actor"),
    path("create_character/<int:scene_id>", views.create_character, name="create_character"),
    path("create_scene/<int:story_id>", views.create_new_scene, name="create_scene"),
    path("update_character/<int:char_id>", views.update_character, name="update_character"),
    path("dialog", views.dialog, name="dialog"),
    path("background/<int:scene_id>", views.set_background, name="background"),
    path("set_character_pos_scale/<int:char_id>", views.set_character_pos_scale, name="set_character_pos_scale"),
    path("set_collectible_pos_scale/<int:char_id>", views.set_collectible_pos_scale, name="set_collectible_pos_scale"),
    path("get_dialog/<int:char_id>", views.get_dialog, name="get_dialog"),
    path("set_scene_description/<int:scene_id>", views.set_scene_description, name="set_scene_description"),
    path("set_scene_name/<int:scene_id>", views.set_scene_name, name="set_scene_name"),
    path("set_story_name/<int:story_id>", views.set_story_name, name="set_story_name"),
    path("update_story/<int:story_id>", views.update_story, name="update_story"),
    path("update_story_scene/<int:story_id>/<int:scene_id>", views.update_story_scene, name="update_story_scene"),
    path("update_menu", views.update_menu, name="update_menu"),
    path("delete_scene/<int:scene_id>", views.delete_scene, name="delete_scene"),
    path("update_user_knowledge", views.update_user_knowledge, name="update_user_knowledge"),
    path("update_scene_knowledge/<int:scene_id>", views.update_scene_knowledge, name="update_scene_knowledge"),
    path("get_scene_knowledge/<int:scene_id>", views.get_scene_knowledge, name="get_scene_knowledge"),
    path("get_active_scenes/<int:scene_id>", views.get_active_scenes, name="get_active_scenes")
]