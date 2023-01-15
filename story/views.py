from django.shortcuts import render, reverse, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json


def story(request, id):
    print("HI")
    return render(request, "story/show.html")


def create_story(request):
    return render(request, "story/create_story.html")

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
