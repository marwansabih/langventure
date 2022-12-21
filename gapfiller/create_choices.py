from django.db import migrations, models

definite_article_rules = {
    "name": "definite_article",
    "description": "The definite article is used..."
}

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


undefinite_article_rules = {
    "name": "undefinite_article",
    "description": "The definite article is used..."
}

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

conjunction_rules = {
    "name": "undefinite_article",
    "description": "The conjunction rule is used..."
}

def create_conjunction_choices(apps, shema_editor):
    ChoiceSelection = apps.get_model("gapfiller", "ChoiceSelection")
    Choice = apps.get_model("gapfiller", "Choice")
    choices = ChoiceSelection(name="conjunctions")
    choices.save()
    articles = [
        "und",
        "sowie",
        "sowohl",
        "als auch",
        "entweder",
        "jedoch",
        "sofern",
        "soweit",
        "als",
        "wie",
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
        "wogegen",
        "seit",
        "seitdem",
        "wenn",
        "als",
        "dadurch",
        "indem",
        "wodurch",
        "womit",
        "damit",
        "um",
        "zu",
        "da",
        "weil",
        "zumal",
        "obgleich",
        "obschon",
        "wenngleich",
        "auch",
        "wenn",
        "falls",
        "sofern",
        "soweit",
        "sodass",
        "soviel",
        "soweit",
        "außer dass",
        "als",
        "als ob",
        "je",
        "desto",
        "bevor",
        "bis",
        "ehe",
        "nachdem",
        "seit",
        "seitdem",
        "solange",
        "sooft",
        "wenn",
        "während",
        "wohingegen",
        "anstatt dass",
        "statt dass"
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
