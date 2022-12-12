from django.db import migrations, models


def create_definite_article_choices(apps, shema_editor):
    ChoiceSelection = apps.get_model("gapfiller", "ChoiceSelection")
    Choice = apps.get_model("gapfiller", "Choice")
    choices = ChoiceSelection(name="definite_articles")
    choices.save()
    articles = [
        "der",
        "die",
        "das",
        "dem",
        "den"
    ]
    [Choice(choices=choices, choice=article).save() for article in articles]


def create_undefinite_article_choices(apps, shema_editor):
    ChoiceSelection = apps.get_model("gapfiller", "ChoiceSelection")
    Choice = apps.get_model("gapfiller", "Choice")
    choices = ChoiceSelection(name="undefinite_articles")
    choices.save()
    articles = [
        "ein",
        "einer",
        "eines",
        "eine",
        "einem",
        "eine"
    ]
    [Choice(choices=choices, choice=article).save() for article in articles]


def create_conjunction_choices(apps, shema_editor):
    ChoiceSelection = apps.get_model("gapfiller", "ChoiceSelection")
    Choice = apps.get_model("gapfiller", "Choice")
    choices = ChoiceSelection(name="conjunctions")
    choices.save()
    articles = [
        "und",
        "oder",
        "dass",
        "denn",
        "obwohl",
        "trotzdem",
        "sondern",
        "aber",
        "weil",
        "jedoch",
        "dennoch",
        "deswegen",
        "trotz",
        "ob",
        "während",
        "seit",
        "seitdem",
        "wenn",
        "als"
    ]
    [Choice(choices=choices, choice=article).save() for article in articles]


class Migration(migrations.Migration):
    dependencies = [
        ('gapfiller', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_undefinite_article_choices),
        migrations.RunPython(create_definite_article_choices),
        migrations.RunPython(create_conjunction_choices)
    ]
