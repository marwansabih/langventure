from django.db import models
from gapfiller.models import User


class Story(models.Model):
    name = models.TextField()
    finished = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="storys", default="")


class Scene(models.Model):
    story = models.ForeignKey(Story, blank=True, default=None, on_delete=models.CASCADE, related_name="scenes")
    name = models.TextField()
    background = models.ImageField(blank=True, default=None, upload_to="images")


class Actor(models.Model):
    scene = models.ForeignKey(Scene, blank=True, default=None, on_delete=models.CASCADE, related_name="actors")
    name = models.TextField()
    image = models.ImageField(blank=True, default=None, upload_to="images")
    scale = models.TextField(default="scale(1)")
    top = models.TextField(default="0px")
    left = models.TextField(default="0px")


class Dialog(models.Model):
    name = models.TextField()
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name="dialogs")
    bubble = models.TextField()


class Option(models.Model):
    origin = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name="options")
    target = models.ForeignKey(Dialog, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField()


class UserStoryConfig(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stories")
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="configs")
    current_dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)
