from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("show/<int:id>", views.show, name="show"),
    path("create", views.create, name="create"),
    path("choice_selection/<int:id>", views.choice_selection, name="choice_selection"),
    path("translation/<int:id>", views.get_token_translation, name="token_translation")
]
