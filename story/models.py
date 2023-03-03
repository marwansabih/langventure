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
    description = models.TextField(default="")


class Actor(models.Model):
    scene = models.ForeignKey(Scene, blank=True, default=None, on_delete=models.CASCADE, related_name="actors")
    name = models.TextField()
    image = models.ImageField(blank=True, default=None, upload_to="images")
    scale = models.TextField(default="scale(1)")
    top = models.TextField(default="100px")
    left = models.TextField(default="50px")


class Dialog(models.Model):
    name = models.TextField()
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name="dialogs")
    bubble = models.TextField()
    translation = models.TextField(default="")


class Knowledge(models.Model):
    item = models.CharField(max_length=50)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, blank=True, null=True, related_name="knowledge_items")
    users = models.ManyToManyField(User, related_name="knowledge_items")


class Option(models.Model):
    origin = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name="options")
    target = models.ForeignKey(Dialog, on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField()
    translation = models.TextField(default="")
    acquired = models.ForeignKey(
        Knowledge,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="acquire_options"
    )
    required_k_items = models.ManyToManyField(
        Knowledge,
        blank=True,
        related_name="require_options"
    )
    disabled_k_items = models.ManyToManyField(
        Knowledge,
        blank=True,
        related_name="disabled_options"
    )


class UserStoryConfig(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stories")
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name="configs")
    current_dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE)


class OptionTokens(models.Model):
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="tokens")
    word = models.CharField(max_length=50)


class DialogTokens(models.Model):
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name="tokens")
    word = models.CharField(max_length=50)

