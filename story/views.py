from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from gapfiller.models import User
from .models import Story, Scene
import json



def story(request, id):
    print("HI")
    return render(request, "story/show.html")


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
        "current_scene_id": current_scene.id
    })


def actor(request):
    if request == "POST":
        return HttpResponse("HEY")
    return render(request, "story/actor.html")


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


def set_background(request, scene_id):
    if request == "Post":
        data = json.loads(request.body)
