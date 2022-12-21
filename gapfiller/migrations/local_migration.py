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
    "und": "<b>und - and</b>: connects two main clauses or part of sentences "
           "<br> Example:"
           "<br> My brother went shopping and I relaxed at home."
           "<br> Mein Bruder ging einkaufen und ich entspannte mich zu Hause."
           "<br> <b>Attention in german main clauses the verb has to be in the second position</b>",
    "sowie": "<b>sowie - as soon as</b>: connects a subordinate clause to a main sentence"
             "<br> Example:"
             "<br> As soon as she arrived at home, she took a shower. "
             "<br> Sowie sie zu Hause ankam, duschte sie sich (nahm sie eine Dusche). "
             "<br> <b>Attention in german subordinate clauses the verb stands at the end.</b>",
    "sowohl": "<b>sowohl ... als - auch - both ... and</b>: normally used to connect to equal parts of a sentence "
              "<br> Example:"
              "<br> She spoke both english and german. "
              "<br> Sie sprach sowohl Englisch als auch Deutsch",
    "entweder": "<b>entweder ... oder - either ... or<b>: Connects to main clauses or part of sentences, "
                "which represent another excluding possibilities."
                "<br> Example:"
                "<br> Either you come, or I drive without you."
                "<br> Entweder kommst du jetzt oder ich fahre ohne dich los."
                "<br> Du kommst jetzt entweder oder ich fahre ohne dich los."
                "<br> <b>Attention in german main clauses the verb has to be in the second position</b>",
    "jedoch": "<b>jedoch - but</b>: connects to main clauses and expresses a limitation or an constraint. "
              "<br> Same meaning as the german word aber, but with different order of words."
              "<br> Example:"
              "<br> I lay down in bed, but I could not sleep. "
              "<br> Ich legte mich ins Bett, jedoch konnte ich nicht schlafen. "
              "<br> (Same meaning but different word order using aber.) "
              "<br> Ich legte mich ins Bett, aber ich konnte nicht schlafen."
              "<br> Attention in german main clauses the verb has to be in second position",
    "sofern": "<b>sofern - provided (that)<b>: Usually connects a main clause with a subordinate clause. "
              "Gives a condition for the main clause. "
              "<br> Example:"
              "<br> I will fly to London, if my boss approves. "
              "<br> Ich fliege nach London, sofern mein Chef es genehmigt."
              "<br> <b>Attention in german subordinate clauses the verb stands at the end.</b>",
    "soweit": "soweit - as far as: Usually connects a main with a subordinate clause. "
              "<br> Adds a constraint to the main clause: only if the constraint of the subordinate clause applies, "
              "the meaning of the main clause is affirmed."
              "<br> Example:"
              "<br>The weather will be nice tomorrow. as far es I know. "
              "<br> Das Wetter wird morgen schön, soweit ich weiß."
              "<br> <b>Attention in german subordinate clauses the verb stands at the end.</b>",
    "als": "als - when: Usually connects a main clause with a subordinate clause. "
           "<br> The subordinate clause gives information about the time, when the main clause happens. <br>"
           "<br> When I opened my eyes, I realized it was only a dream. "
           "<br> Als ich die Augen öffnete, stellte ich fest es war nur ein Traum."
           "<br> <b>Attention in german subordinate clauses the verb stands at the end.</b>",
    "wie": "wie as: Usually used to compare parts of sentences. Not to be confused with als. "
           "<br> als is used to compare using the german Komperativ of adjectives, "
           "wie is used to compare everything else (nouns, adjectives not in comperative etc.)"
           "example:"
           "<br> He is strong as a bear. "
           "<br> Er ist stark wie ein Bär. "
           "<br> He is stronger than a bear. "
           "<br> Er ist stärker als ein Bär.",
    "oder": "<b>oder - or</b>: usually connects parts of sentence to mark alternatives. "
            "<br>Examples:"
            "<br>Do we take the bus or the train."
            "<br>Nehmen wir den Zug oder den Bus",
    "als auch": "als auch - as well as: Connects parts of sentences similar to and."
                "<br> Examples:"
                "<br> We need butter as well breads. "
                "<br> Wir brauchen Butter and Brot.",
    "dass": "<b>dass - that<b>: connects a main clause and a subordinate clause. "
            "The subordinate clause describes the consequences of the action of the main clause."
            "<br> Example:"
            "<br> I was so sad, that i had to cry."
            "<br> Ich war so traurig, dass ich weinen musste."
            "<br> <b>Attention in german subordinate clauses the verb stands at the end.</b>",
    "denn": "<b>denn - because</b>: connects two main phrases. "
            "<br>The subordinate clause gives a reason for the main clause. Not be confused with weil."
            "<br>weil has the same meaning like denn, but connects a main clause with a subordinate clause."
            "<br> I took an umbrella, because it rained."
            "<br> Ich nahm einen Regenschirm, denn es regnete."
            "<br> Ich nahm einen Regenschirm, weil es regnete."
            "<br> <b>Attention in german main clauses the verb has to be in second position</b>",
    "obwohl": "<b>obwohl - although</b>: connects a main sentence with a subordinate clause."
              "Mostly used to describe doing something, although something speaks against it."
              "<br> Example: "
              "<br> He said yes, although he meant no."
              "<br> Er sagt ja, obwohl er nein meint."
              "<br> <b>Attention in german subordinate clauses the verb stands at the end.</b>",
    "trotzdem": "<b>trotzdem - nevertheless</b>: connects two main clauses and is mostly used"
                "that something is done, despite something speaking against it."
                "<br> Examples:"
                "<br> It's raining, nevertheless we go for a walk."
                "<br> Es regnet, trotzdem gehn wir spazieren."
                "<br> <b>Attention in german main clauses the verb has to be in second position</b>",
    "sondern": "<b>sondern - but:</b>: connects two main clauses or parts of sentences"
               "and is similary used to aber. But where "
               "aber is used to give a general discrepancy, sondern is used to correct a wrong assumption. "
               "See the examples."
               "<br> Examples:"
               "<br> I don't take the bus, but the train."
               "<br> Ich nehme nicht den Bus, sondern den Zug."
               "<br> Tomorow it will rain, but i don't have an umbrella."
               "<br> Morgen wird es regnen, aber ich habe keinen Regenschirm."
               "<br> <b>Attention in german main clauses the verb has to be in second position</b>",
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