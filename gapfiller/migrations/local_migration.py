from django.db import migrations, models

def gen_rule(apps, props):
    Rule = apps.get_model("gapfiller", "Rule")
    rule = Rule(rule_type=props["name"], description=props["description"])
    rule.save()
    return rule

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

    rule = gen_rule(
        apps,
        definite_article_rules
    )
    rule.save()

    [Choice(choices=choices, choice=article, rule=rule).save() for article in articles]


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
    rule = gen_rule(
        apps,
        undefinite_article_rules
    )
    rule.save()
    [Choice(choices=choices, choice=article, rule=rule).save() for article in articles]


conjunction_rules = {
    "und": "und - and: connects to main clauses or part of sentences <br> e.g: My brother went shopping and I relaxed at home."
           " Mein Bruder ging einkaufen und ich entspannte mich zu Hause."
           " <br>Attention in german main clauses the verb has to be in the second position",
    "sowie": "sowie - as soon as: connects a subordinate clause to a main sentence <br> "
             " <br> As soon as she arrived at home, she took a shower. "
             " Sowie sie zu Hause ankam, duschte sie sich (nahm sie eine Dusche). <br> "
             "<br> Attention in german subordinate clauses the verb stands at the end.",
    "sowohl": "sowohl ... als auch - both ... and: normally used to connect to parts of a sentence <br>"
              "She spoke both english and german. Sie sprach sowohl Englisch als auch Deutsch",
    "entweder": "entweder ... oder - either ... or",
    "jedoch": "jedoch - but: connects to main clauses and expresses a limitation or an constraint. <br>"
              "Same meaning as the german word aber, but with different order of words. <br>"
              "I lay down in bed, but I could not sleep. Ich legte mich ins Bett, jedoch konnte ich nicht schlafen. "
              "(Same meaning but different word order using aber.) Ich legte mich ins Bett, aber ich konnte nicht schlafen."
              " <br> Attention in german main clauses the verb has to be in second position",
    "sofern": "sofern - provided (that): Usually connects a main clause with a subordinate clause. Gives a condition for the main clause. <br>"
              "I will fly to London, if my boss approves. Ich fliege nach London, sofern mein Chef es genehmigt."
              "<br> Attention in german subordinate clauses the verb stands at the end.",
    "soweit": "soweit - as far as: Usually connects a main with a subordinate clause. <br>"
              "Adds a contraint to the main clause, only if the constraint of the subordinate clause applies, the content of the main clause"
              "is to be applied.<br>"
              "The weather will be nice tomorrow. as far es I know. Das Wetter wird morgen schön, soweit ich weiß."
              "<br> Attention in german subordinate clauses the verb stands at the end.",
    "als": "als - when: Usually connects a main clause with a subordinate clause. <br>"
           "The subordinate clause gives information about the time, when the main clause happens. <br>"
           "When I opened my eyes, I realized it was only a dream. <br> Als ich die Augen öffnete, stellte ich fest es war nur ein Traum."
           "<br> Attention in german subordinate clauses the verb stands at the end.",
    "wie": "wie as: Usually used to compare parts of sentences. Not to be confused with als. <br>"
           "als is used to compare using the german Komperativ of adjectives, wie is used to compare everything else (nouns, adjectives not in comperative etc.)"
           "<br> He is strong as a bear. Er ist stark wie ein Bär. He is stronger than a bear. Er ist stärker als ein Bär.",
    "oder": "oder - or: usually connects parts of sentence to mark alternatives. Do we take the bus or the train. Nehmen wir den Zug oder den Bus",
    "als auch": "als auch - as well as",
    "dass": "dass - that",
    "denn": "denn - because",
    "obwohl": "obwohl - although",
    "trotzdem": "trotzdem - despite",
    "sondern": "sondern - but",
    "aber": "aber - but",
    "weil": "weil - because",
    "dennoch": "dennocn - nonetheless",
    "deswegen": "deswegen - because of this",
    "trotz": "trotz - despite",
    "ob": "ob - if",
    "während": "während - while",
    "wogegen": "wogegen - against what",
    "seit": "seit - since",
    "seitdem": "since",
    "wenn": "wenn - when, wether, if ...",
    "dadurch": "dadurch - thereby",
    "indem": "indem - by",
    "wodurch": "wodurch - whereby",
    "womit": "womit - whereby, with what",
    "damit": "damit - thereby",
    "um": "um ... zu - in oder to ",
    "zu": "um ... zu - in oder to",
    "da": "da - because",
    "weil": "weil - because",
    "zumal": "zumal - the more so as",
    "obgleich": "obgleich - though, even though",
    "obschon": "obschon - wether, albeit, though, if",
    "wenngleich": "wenngleich - even though",
    "auch": "sowohl ... als auch",
    "wenn": "wenn - if, when, by the time",
    "falls": "falls - if",
    "sodass": "sodass - so that",
    "soviel": "soviel - as far as",
    "soweit": "soweit - as far as",
    "außer": "außer dass - except that",
    "als ob": "als ob - as if",
    "je": "je ... desto - the ... the",
    "desto": "je ... desto - the ... the",
    "bevor": "bevor - before",
    "bis": "bis - till",
    "ehe": "ehe - before",
    "nachdem": "nachdem - after",
    "seit": "seit - since",
    "seitdem": "seitdem - ever since, since",
    "solange": "solange - as long as",
    "sooft": "sooft - whenever",
    "während": "während - during, while",
    "wohingegen": "wohingegen - whereas",
    "anstatt dass": "anstatt - instead of",
    "statt dass": "statt - instead of"
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
    rule = gen_rule(
        apps,
        undefinite_article_rules
    )
    rule.save()
    def gen_props(article):
        props = {
            "name": "conjunction",
            "description": conjunction_rules[article]
        }
        return props
    [Choice(choices=choices, choice=article, rule=gen_rule(apps, gen_props(article))).save() for article in articles]


class Migration(migrations.Migration):
    dependencies = [
        ('gapfiller', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_undefinite_article_choices),
        migrations.RunPython(create_definite_article_choices),
        migrations.RunPython(create_conjunction_choices)
    ]