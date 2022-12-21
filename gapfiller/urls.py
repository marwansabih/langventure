from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("show/<int:id>", views.show, name="show"),
    path("create", views.create, name="create"),
    path("choice_selection/<int:id>", views.choice_selection, name="choice_selection"),
    path("display_update/<int:id>", views.get_token_display_updates, name="token_display_update"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("delete_gapfiller/<int:id>", views.delete_gapfiller, name="delete_gapfiller")
]
