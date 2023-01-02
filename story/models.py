from django.db import models
from gapfiller.models import User


class Story(models.Model):
    pass


class Scene(models.Model):
    name = models.TextField()
    description = models.TextField()


class Actor(models.Model):
    #scence = models.ForeignKey(Scene, on_delete=models.CASCADE, related_name="actors")
    name = models.TextField()


class Dialog(models.Model):
    name = models.TextField(unique=True)
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
