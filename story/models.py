from django.db import models
from gapfiller.models import User
from gtts import gTTS
import io
from django.core.files.base import ContentFile
import tempfile
import os


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
    top = models.TextField(default="10px")
    left = models.TextField(default="50px")


class Dialog(models.Model):
    name = models.TextField()
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, related_name="dialogs")
    bubble = models.TextField()
    audio = models.FileField(
        upload_to='podcasts/', null=True, blank=True)
    translation = models.TextField(default="")

    def save_audio(self):
        tts = gTTS(self.bubble, lang='de')  # Change lang as needed
        audio_buffer = io.BytesIO()

        # Create a temporary file
        temp_file_path = f'tmp_dialog_audio_{self.pk}.mp3'
        tts.save(temp_file_path)

        # Read the temporary file into the audio_buffer
        with open(temp_file_path, 'rb') as temp_file:
            audio_buffer.write(temp_file.read())

        audio_buffer.seek(0)
        audio_file_name = f'dialog_audio_{self.pk}.mp3'
        self.audio.save(audio_file_name, ContentFile(audio_buffer.read()))

        # Remove the temporary file
        os.remove(temp_file_path)


class Knowledge(models.Model):
    item = models.CharField(max_length=50)
    story = models.ForeignKey(Story, on_delete=models.CASCADE, blank=True, null=True, related_name="knowledge_items")
    users = models.ManyToManyField(User, blank=True, related_name="knowledge_items")
    required_scenes = models.ManyToManyField(Scene, blank=True, related_name="requires")
    deactivated_scenes = models.ManyToManyField(Scene, blank=True, related_name="deactivates")


class Collectible(models.Model):
    scene = models.ForeignKey(Scene, blank=True, default=None, on_delete=models.CASCADE, related_name="collectibles")
    name = models.CharField(max_length=50)
    knowledge_item = models.ForeignKey(Knowledge, on_delete=models.CASCADE, related_name="collectible")
    image = models.ImageField(blank=True, default=None, upload_to="images")
    scale = models.TextField(default="scale(1)")
    top = models.TextField(default="10px")
    left = models.TextField(default="50px")

    def __str__(self):
        return self.name


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
    audio = models.FileField(
        upload_to='podcasts/', null=True, blank=True)

    def save_audio(self):
        tts = gTTS(self.text, lang='de')  # Change lang as needed
        audio_buffer = io.BytesIO()

        # Create a temporary file
        temp_file_path = f'tmp_option_audio_{self.pk}.mp3'
        tts.save(temp_file_path)

        # Read the temporary file into the audio_buffer
        with open(temp_file_path, 'rb') as temp_file:
            audio_buffer.write(temp_file.read())

        audio_buffer.seek(0)
        audio_file_name = f'dialog_option_audio_{self.pk}.mp3'
        self.audio.save(audio_file_name, ContentFile(audio_buffer.read()))

        # Remove the temporary file
        os.remove(temp_file_path)


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

