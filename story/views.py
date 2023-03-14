from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from gapfiller.models import User
from gapfiller.helsinki_translator import hel_translate
from .models import Story, Scene, Actor, Dialog, Option, Knowledge
import json
import PIL
import base64

from django.core.files.images import get_image_dimensions


#   TODO
"""
    - speech 
    - items to collect
    - add translation for tokens
    - update character menu
    - add current scene
    - return json responses
    - fix bug after creating new characters with javascript
    - add custom translation
    - add custom speech
    - add enable scenes with knowledge items
    - todo clean up menu 
    - warning if char is incomplete or ill designed
    - publish only available after correcting all mistakes
    - show author of story
"""


@login_required
def story(request, id):
    story = Story.objects.get(pk=id)
    current_scene = story.scenes.all().first()
    user = request.user
    return render(request, "story/show.html", {
        "story": story,
        "current_scene": current_scene,
        "knowledge_items": user.knowledge_items.all()
    })


@login_required
def story_scene(request, id, scene_id):
    story = Story.objects.get(pk=id)
    current_scene = Scene.objects.get(pk=scene_id)
    return render(request, "story/show.html", {
        "story": story,
        "current_scene": current_scene
    })

@csrf_exempt
@login_required
def update_user_knowledge(request):
    if request.method == "POST":
        user = request.user
        story_id = request.POST.get("story_id")
        story = Story.objects.get(pk=story_id)
        item = request.POST.get("item")
        item = Knowledge.objects.filter(story=story, item=item).first()
        item.users.add(user)
        return JsonResponse({"body": "Successfully added item to user knowledge"}, status=201)


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
    story_id = Scene.objects.get(pk=scene_id).story.id
    story = Story.objects.get(pk=story_id)
    if request == "POST":
        return HttpResponse("HEY")
    return render(request, "story/actor.html", {
        "story_id": story_id,
        "scene_id": scene_id,
        "story": story
    })


def edit_actor(request, actor_id):
    actor = Actor.objects.get(pk=actor_id)
    sence_id = actor.scene.id
    story_id = actor.scene.story.id
    return render(request, "story/actor.html", {
        "actor_id": actor_id,
        "name": actor.name,
        "image": actor.image,
        "story_id": story_id,
        "scene_id": sence_id,
        "story": actor.scene.story
    })


@csrf_exempt
def get_character_info(request, actor_id):
    if request.method == "GET":
        actor = Actor.objects.get(pk=actor_id)
        id_to_dialog = {}
        for dialog in actor.dialogs.all():
            dialog_info = {
                "bubble": dialog.bubble,
                "translation": dialog.translation,
                "options": []
            }
            for option in dialog.options.all():
                opt_info = {
                    "content": option.text,
                    "translation": option.translation,
                    "selection": option.target.name,
                    "acquires": None if not option.acquired else option.acquired.item,
                    "requires": [k.item for k in option.required_k_items.all()],
                    "deactivates": [k.item for k in option.disabled_k_items.all()]
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


def save_option(option, id, id_to_m_dialog, story):
    target = option["selection"]
    text = option["content"]
    acquires = option["acquires"]
    requires = option["requires"]
    deactivates = option["deactivates"]
    origin = id_to_m_dialog[id]
    target = id_to_m_dialog[target]
    if "translation" in option and option["translation"]:

        translation = option["translation"]
    else:
        translation = hel_translate(text)

    opt = Option(origin=origin, target=target, text=text, translation=translation)
    opt.save()
    if acquires:
        acq = Knowledge.objects.filter(item=acquires, story=story).first()
        opt.acquired = acq
    if requires:
        reqs = [Knowledge.objects.filter(item=req, story=story).first() for req in requires]
        [opt.required_k_items.add(req) for req in reqs]
    if deactivates:
        deas = [Knowledge.objects.filter(item=dea, story=story).first() for dea in deactivates]
        [opt.disabled_k_items.add(dea) for dea in deas]
    opt.save()


@csrf_exempt
def create_character(request, scene_id):
    print("in update char")
    if request.method == "POST":
        scene = Scene.objects.get(pk=scene_id)
        story = scene.story
        print("HEY HEY")
        knowledge_items = request.POST.get("knowledge_items")
        knowledge_items = json.loads(knowledge_items)
        items = [k_i.item for k_i in story.knowledge_items.all()]
        for item in knowledge_items:
            if item not in items:
                new_item = Knowledge(item=item, story=story)
                new_item.save()

        image = request.FILES.get("image")
        height, width = get_image_dimensions(image)
        scale = str(120.0/height)
        name = request.POST.get("name")
        actor = Actor(scene=scene, name=name, image=image, scale=scale)
        actor.save()
        id_to_dialog = request.POST.get("id_to_dialog")
        dialogs = json.loads(id_to_dialog)
        id_to_m_dialog = {}
        for id in dialogs:
            dialog = dialogs[id]
            translation = hel_translate(dialog["bubble"])
            d = Dialog(name=id, actor=actor, bubble=dialog["bubble"], translation=translation)
            id_to_m_dialog[id] = d
            d.save()
        for id in dialogs:
            options = dialogs[id]["options"]
            for option in options:
                save_option(option, id, id_to_m_dialog, story)
    return render(request, "story/dialog.html", context={
        "scene_id": scene_id,
    })


@csrf_exempt
def update_character(request, char_id):
    if request.method == "POST":
        actor = Actor.objects.get(pk=char_id)
        story = actor.scene.story
        knowledge_items = request.POST.get("knowledge_items")
        print(knowledge_items)
        knowledge_items = json.loads(knowledge_items)
        items = [k_i.item for k_i in story.knowledge_items.all()]
        for item in knowledge_items:
            if item not in items:
                new_item = Knowledge(item=item, story=story)
                new_item.save()
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
            if "translation" in dialog:
                translation = dialog["translation"]
            else:
                translation = hel_translate(dialog["bubble"])
            d = Dialog(name=id, actor=actor, bubble=dialog["bubble"], translation=translation)
            id_to_m_dialog[id] = d
            d.save()
        for id in dialogs:
            options = dialogs[id]["options"]
            for option in options:
                save_option(option, id, id_to_m_dialog, story)

        return JsonResponse({"body": "successfully updated character"}, status= 200)



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
            translation = dialog.translation
            opts = dialog.options.all()

            options = [
                {
                    "content": option.text,
                    "translation": option.translation,
                    "selection": option.target.name,
                    "acquires": None if not option.acquired else option.acquired.item,
                    "requires": [ki.item for ki in option.required_k_items.all()],
                    "deactivates": [ki.item for ki in option.disabled_k_items.all()]
                 }
                for option in opts
            ]

            id_to_dialog[id] = {
                "bubble": bubble,
                "translation": translation,
                "options": options
            }

        dialog_info = {
            "name": actor.name,
            "id_to_dialog": id_to_dialog
        }

        return JsonResponse(dialog_info)
