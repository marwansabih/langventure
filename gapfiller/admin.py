from django.contrib import admin
from .models import Choice, ChoiceSelection, Token, Text, Entry, Paragraph, Rule, Podcast, UserEntryGapFillerStatus, UserEntryChoiceSelConfig, User, Language

# Register your models here.

admin.site.register(Paragraph)
admin.site.register(Choice)
admin.site.register(ChoiceSelection)
admin.site.register(Token)
admin.site.register(Text)
admin.site.register(Entry)
admin.site.register(Rule)
admin.site.register(Podcast)
admin.site.register(UserEntryGapFillerStatus)
admin.site.register(UserEntryChoiceSelConfig)
admin.site.register(User)
admin.site.register(Language)
