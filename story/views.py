from django.shortcuts import render


def story(request, id):
    return render(request, "story/show.html")


def actor(request):
    return render(request, "story/actor.html")
