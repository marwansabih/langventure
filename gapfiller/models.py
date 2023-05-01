from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser


class Text(models.Model):
    pass


class Entry(models.Model):
    title = models.ForeignKey(Text, on_delete=models.CASCADE)


class Podcast(models.Model):

    audio_file = models.FileField(
        upload_to='podcasts/', null=True, blank=True)
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE, related_name="podcast")


class Paragraph(models.Model):
    text = models.ForeignKey(Text, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="paragraphs")


class ChoiceSelection(models.Model):
    name = models.TextField(blank=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return "local_generated"


class Rule(models.Model):
    rule_type = models.CharField(max_length=25, default="no_name")
    description = models.TextField()


class Choice(models.Model):
    choices = models.ForeignKey(ChoiceSelection, on_delete=models.CASCADE, related_name="choices")
    choice = models.TextField()
    rule = models.ForeignKey(
        Rule,
        blank=True,
        null=True,
        default=None,
        on_delete=models.CASCADE,
        related_name="choices"
    )

    def __str__(self):
        return self.choice


class LocalChoiceSelection(models.Model):
    choice_selection = models.ForeignKey(ChoiceSelection, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)


class Token(models.Model):
    text = models.ForeignKey(Text, on_delete=models.CASCADE, related_name="tokens")
    translation = models.TextField(default="")
    word_translation = models.TextField(default="")
    word = models.TextField()
    is_upper = models.BooleanField(default=False)
    local_choice_selection = models.ForeignKey(LocalChoiceSelection, blank=True, null=True, on_delete=models.CASCADE, related_name="token")


class Language(models.Model):
    name = models.TextField(default="english")
    lang_code = models.TextField(default="en")


class User(AbstractUser):
    org_language = models.ForeignKey(Language, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name="target_language")
    dest_language = models.ForeignKey(Language, on_delete=models.CASCADE, blank=True, default=None, null=True, related_name="mother_language")


class UserEntryChoiceSelConfig(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    choice_selection = models.ForeignKey(ChoiceSelection, on_delete=models.CASCADE)
    enabled = models.BooleanField(default=False)


class UserEntryGapFillerStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="entry_stati")
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, related_name="entry_stati")
    active = models.BooleanField(default=False)
