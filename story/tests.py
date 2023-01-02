from django.test import TestCase, Client
from .models import Story, UserStoryConfig, Dialog, Actor, Option

# Create your tests here.

dialogs = {
    "intro": "Hallo Mario, hast du schon die Sache von Peach gehört?",
    "Thing about Peach": "Der DNA-Mann kommt jetzt zu ihr. Ihr Mann Luigi meint ihre Tochter wäre nicht vom ihm.",
    "suspicion of luigi": "Luigi glaubt, dass du der Vater bist, die kleine bevorzugt rote Mützen wie du und nicht"
                          "grüne wie er.",
    "end": "Ja, finde ich auch.",
}

opts = [
    ("intro", "Thing about Peach", "Wovon redest du, Toad?"),
    ("intro", "Thing about Peach", "Was meinst du, Toad?"),
    ("intro", "Thing about Peach", "Hm ist ihr etwas passiert, Toad?"),
    ("Thing about Peach", "suspicion of luigi", "Wie kommt er nur darauf?"),
    ("suspicion of luigi", "end", "Ist Luigi denn verrückt geworden, ich soll der Vater? Das ist ja verrückt.")
]


class TestStory(TestCase):

    def setUp(self):
        actor = Actor(name="Test_speaker")
        actor.save()
        for dialog in dialogs:
            d = Dialog(actor=actor, bubble=dialogs[dialog], name=dialog)
            d.save()

        for option in opts:
            source = option[0]
            target = option[1]
            d1 = Dialog.objects.filter(name=source)[0]
            d2 = Dialog.objects.filter(name=target)[0]
            o = Option(origin=d1, target=d2, text=option[2])
            o.save()

        dialog = actor.dialogs.all()[0]
        options = dialog.options.all()

        while options:
            print(dialog.bubble)
            for i, option in enumerate(options):
                print(f"{i}. {option.text}")
            idx = int(input("Your choice: "))
            chosen_option = options[idx]
            dialog = chosen_option.target
            options = dialog.options.all()

        print(dialog.bubble)

    def test_dialog(self):
        pass



