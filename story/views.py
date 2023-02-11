from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from gapfiller.models import User
from .models import Story, Scene, Actor, Dialog, Option
import json
import PIL
import base64


#   TODO
"""
    - knowledge items through conversation
    - speech 
    - items to collect
    - add translation
    - update character menu
    - enable new scenes
    - add current scene
    - return json responses
    - fix bug after creating new characters with javascript
"""


@login_required
def story(request, id):
    story = Story.objects.get(pk=id)
    current_scene = story.scenes.all().first()
    return render(request, "story/show.html", {
        "story": story,
        "current_scene": current_scene
    })


@login_required
def story_scene(request, id, scene_id):
    story = Story.objects.get(pk=id)
    current_scene = Scene.objects.get(pk=scene_id)
    return render(request, "story/show.html", {
        "story": story,
        "current_scene": current_scene
    })


@login_required
def create_story(request):
    user = request.user
    story = Story(user=user, finished=False, name="No Title")
    new_story = user.storys.filter(finished=False)
    if new_story:
        story = new_story.first()
    story.save()
    if not story.scenes.all():
        scene = Scene(story=story, name="start")
        scene.save()

    current_scene = story.scenes.all().first()

    return render(request, "story/create_story.html", {
        "story": story,
        "current_scene": current_scene,
        "current_scene_id": current_scene.id
    })



@login_required
def update_menu(request):
    user = request.user
    stories = Story.objects.filter(user=user).all()
    return render(request, "story/update_menu.html", {
        "stories": stories
    })

@login_required
def update_story(request, story_id):
    story = Story.objects.get(pk=story_id)
    current_scene = story.scenes.all().first()

    return render(request, "story/create_story.html", {
        "story": story,
        "current_scene": current_scene,
        "current_scene_id": current_scene.id
    })


@login_required
def update_story_scene(request, story_id, scene_id):
    story = Story.objects.get(pk=story_id)
    current_scene = Scene.objects.get(pk=scene_id)

    return render(request, "story/create_story.html", {
        "story": story,
        "current_scene": current_scene,
        "current_scene_id": current_scene.id
    })


@csrf_exempt
def delete_scene(request, scene_id):
    scene = Scene.objects.get(pk=scene_id)
    scene.delete()
    return render(request, "story/actor.html", {
        "scene_id": scene_id
    })

def actor(request, scene_id):
    if request == "POST":
        return HttpResponse("HEY")
    return render(request, "story/actor.html", {
        "scene_id": scene_id
    })


def edit_actor(request, actor_id):
    actor = Actor.objects.get(pk=actor_id)
    return render(request, "story/actor.html", {
        "actor_id": actor_id,
        "name": actor.name,
        "image": actor.image
    })


@csrf_exempt
def get_character_info(request, actor_id):
    if request.method == "GET":
        actor = Actor.objects.get(pk=actor_id)
        id_to_dialog = {}
        for dialog in actor.dialogs.all():
            dialog_info = {
                "bubble": dialog.bubble,
                "options": []
            }
            for option in dialog.options.all():
                opt_info = {
                    "content": option.text,
                    "selection": option.target.name,
                }
                dialog_info["options"].append(opt_info)
            id_to_dialog[dialog.name] = dialog_info
    return JsonResponse(id_to_dialog)


@csrf_exempt
def set_story_name(request, story_id):
    if request.method == "POST":
        story = Story.objects.get(pk=story_id)
        story.name = request.POST.get("name")
        story.save()
        return render(request, "story/success.html")


@csrf_exempt
def dialog(request):
    print(request)
    if request == "POST":
        data = json.loads(request.body)
    return render(request, "story/dialog.html")


@csrf_exempt
def create_new_scene(request, story_id):
    if request.method == "POST":
        story = Story.objects.get(pk=story_id)
        name = request.POST.get("name")
        print(name)
        scene = Scene(story=story, name=name)
        scene.save()
        return JsonResponse({"scene_id": scene.pk}, status=201)


@csrf_exempt
def set_scene_name(request, scene_id):
    if request.method == "POST":
        scene = Scene.objects.get(pk=scene_id)
        scene.name = request.POST.get("name")
        scene.save()
        return render(request, "story/success.html")


@csrf_exempt
def set_scene_description(request, scene_id):
    if request.method == "POST":
        scene = Scene.objects.get(pk=scene_id)
        scene.description = request.POST.get("description")
        scene.save()
        return render(request, "story/success.html")


@csrf_exempt
def set_background(request, scene_id):
    if request.method == "POST":
        scene = Scene.objects.get(pk=scene_id)
        scene.background = request.FILES.get("image")
        scene.save()
        return JsonResponse({"message": "scene description successfully updated."}, status=201)


@csrf_exempt
def create_character(request, scene_id):
    if request.method == "POST":
        scene = Scene.objects.get(pk=scene_id)
        image = request.FILES.get("image")
        name = request.POST.get("name")
        actor = Actor(scene=scene, name=name, image=image)
        actor.save()
        id_to_dialog = request.POST.get("id_to_dialog")
        dialogs = json.loads(id_to_dialog)
        id_to_m_dialog = {}
        for id in dialogs:
            dialog = dialogs[id]
            d = Dialog(name=id, actor=actor, bubble=dialog["bubble"])
            id_to_m_dialog[id] = d
            d.save()
        for id in dialogs:
            options = dialogs[id]["options"]
            for option in options:
                target = option["selection"]
                text = option["content"]
                origin = id_to_m_dialog[id]
                target = id_to_m_dialog[target]
                opt = Option(origin=origin, target=target, text=text)
                opt.save()

    return render(request, "story/dialog.html", {
        "scene_id": scene_id
    })


@csrf_exempt
def update_character(request, char_id):
    if request.method == "POST":
        actor = Actor.objects.get(pk=char_id)
        #image = request.FILES.get("image")
        name = request.POST.get("name")
        actor.name = name
        actor.save()
        id_to_dialog = request.POST.get("id_to_dialog")
        dialogs = json.loads(id_to_dialog)
        id_to_m_dialog = {}
        for old_dialog in actor.dialogs.all():
            old_dialog.delete()
        for id in dialogs:
            dialog = dialogs[id]
            d = Dialog(name=id, actor=actor, bubble=dialog["bubble"])
            id_to_m_dialog[id] = d
            d.save()
        for id in dialogs:
            options = dialogs[id]["options"]
            for option in options:
                target = option["selection"]
                text = option["content"]
                origin = id_to_m_dialog[id]
                target = id_to_m_dialog[target]
                opt = Option(origin=origin, target=target, text=text)
                opt.save()

    return render(request, "story/dialog.html", {
        "actor_id": char_id
    })


@csrf_exempt
def set_character_pos_scale(request, char_id):
    if request.method == "POST":
        actor = Actor.objects.get(pk=char_id)
        top = request.POST.get("top")
        left = request.POST.get("left")
        scale = request.POST.get("scale")
        actor.top = top
        actor.left = left
        actor.scale = scale
        actor.save()

    return render(request, "story/dialog.html", {
        "scene_id": char_id
    })


@csrf_exempt
def get_dialog(request, char_id):
    if request.method == "GET":
        actor = Actor.objects.get(pk=char_id)
        # could I simply use serialize?
        dialogs = actor.dialogs.all()
        id_to_dialog = {}
        for dialog in dialogs:
            id = dialog.name
            bubble = dialog.bubble
            opts = dialog.options.all()
            options = [{"content": option.text, "selection": option.target.name} for option in opts]
            id_to_dialog[id] = {"bubble": bubble, "options": options}

        dialog_info = {
            "name": actor.name,
            "id_to_dialog": id_to_dialog
        }

        return JsonResponse(dialog_info)
