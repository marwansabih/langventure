from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from gapfiller.models import User
from .models import Story, Scene, Actor, Dialog, Option
import json
import PIL
import base64


def story(request, id):
    story = Story.objects.get(pk=id)
    current_scene = story.scenes.filter(name="start").first()
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

    current_scene = story.scenes.filter(name="start").first()
    print(current_scene)

    return render(request, "story/create_story.html", {
        "story": story,
        "current_scene": current_scene,
        "current_scene_id": current_scene.id
    })


def actor(request, scene_id):
    if request == "POST":
        return HttpResponse("HEY")
    return render(request, "story/actor.html", {
        "scene_id": scene_id
    })


@csrf_exempt
def dialog(request):
    print(request)
    if request == "POST":
        data = json.loads(request.body)
        print(data)
    return render(request, "story/dialog.html")
    #render(request, "story/success.html")
    #redirect("show", id=1)
    #HttpResponseRedirect(reverse("story", kwargs={"id": 1})) #JsonResponse({"message": "Character successfully created."}, status=201)


@csrf_exempt
def set_background(request, scene_id):
    if request.method == "POST":
        scene = Scene.objects.get(pk=scene_id)
        scene.background = request.FILES.get("image")
        scene.save()
        return render(request, "story/success.html")


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
def set_character_pos_scale(request, char_id):
    if request.method == "POST":
        actor = Actor.objects.get(pk=char_id)
        print(request.POST)
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
        print("HERE HERE")
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
