from django.contrib import admin
from .models import Story, Scene, Actor, Knowledge, Option

# Register your models here.
admin.site.register(Story)
admin.site.register(Scene)
admin.site.register(Actor)
admin.site.register(Knowledge)
admin.site.register(Option)
