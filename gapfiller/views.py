from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .models import Text, Token, Entry, Choice, ChoiceSelection, Paragraph, Rule, Podcast, UserEntryChoiceSelConfig, UserEntryGapFillerStatus, LocalChoiceSelection, User
from gtts import gTTS
from django.core.files import File
from pathlib import Path
import spacy
from django.contrib.auth.decorators import login_required
from .helsinki_translator import hel_translate
import random

nlp = spacy.load('de_core_news_sm')


# Create your views here.

# todo add conversation mode with two heads speaking ( a true langventure )
# todo picture for words
# todo add verb choices
# todo add noun choices
# todo filter choices by word type
# todo add specific and unspecific rules
# todo add support for a second language
# todo write tests
# todo clean up javascript
# todo clean up code
# todo add save status
# todo make model more efficient
# todo add state save so that you don't need to redo an exercise
# todo own audio
# todo add number of gaps
# todo conjunctions consisting out of more than one word
# todo add rules
# todo enhance translation
# todo enhance graphics
# todo add word marking sentence marking (for token clicked)
# todo add word translation
# todo smarter model structure (sentence translation)
# todo add information for gapfiller (author title and timestamp)
# todo correct punctuation behaviour of gapfiller
# todo enable corrections for translation
# todo cleanup rest of css
# todo add delete to posts
# todo add edit to posts
# todo add better userspecific behaviour (delete, add, edit gapfiller)
# todo enhance admin panel
# todo empty gaps in gapfiller (e.g. ein for plural)
# todo corret mistakes in conjunctions

def gen_local_selection(choice_selection, correct_choice, nr_choices):
    local_selection = LocalChoiceSelection(choice_selection=choice_selection)
    local_selection.save()
    choices = random.sample(list(choice_selection.choices.all()), nr_choices)
    if correct_choice not in choices:
        choices[random.randint(1, nr_choices-1)] = correct_choice
    for choice in choices:
        choice = Choice.objects.filter(choice=choice).first()
        local_selection.choices.add(choice)

    return local_selection


def create_entry(title, text):
    paragraphs = text.split("\n")
    definite_articles = ChoiceSelection.objects.filter(name="definite_articles")[0]
    undefinite_articles = ChoiceSelection.objects.filter(name="undefinite_articles")[0]
    conjunctions = ChoiceSelection.objects.filter(name="conjunctions")[0]
    #article_rule = Rule.objects.filter(name="articles").first()
    #conjunction_rule = Rule.objects.filter(name="conjunctions").first()
    audio = gTTS(text=text, lang="de", slow=False)
    audio_path = Path("media/podcasts/" + title + ".mp3")
    audio.save("media/podcasts/" + title + ".mp3")

    def generate_text(content):
        text = Text()
        text.save()
        doc = nlp(content)
        sentences = list(doc.sents)
        nouns = []
        for toks in sentences:
            if not str(toks).strip():
                continue
            translation = hel_translate(str(toks))
            for token in toks:
                tok = str(token)
                choice_selection = None
                rule = None
                articles = [a.choice for a in definite_articles.choices.all()]
                if tok.lower() in articles:
                    choice_selection = gen_local_selection(definite_articles, tok.lower(), 5)
                    #rule = article_rule
                articles = [a.choice for a in undefinite_articles.choices.all()]
                if tok.lower() in articles:
                    choice_selection = gen_local_selection(undefinite_articles, tok.lower(), 5)
                    #rule = article_rule
                cons = [c.choice for c in conjunctions.choices.all()]
                if tok.lower() in cons and (token.pos_ == "SCONJ" or token.pos_ == "CCONJ"):
                    choice_selection = gen_local_selection(conjunctions, tok.lower(), 5)
                    #rule = conjunction_rule
                if tok.strip():
                    token = Token(
                        text=text,
                        word=tok,
                        word_translation=hel_translate(tok),
                        local_choice_selection=choice_selection,
                        is_upper=tok[0].isupper(),
                        #rule=rule,
                        translation=translation
                    )
                    token.save()
        return text

    title = generate_text(title)

    entry = Entry(title=title)
    entry.save()

    with audio_path.open(mode='rb') as f:
        podcast = Podcast(entry=entry, audio_file=File(f, name=audio_path.name))
        podcast.save()

    paragraphs = [generate_text(p) for p in paragraphs]

    for p in paragraphs:
        paragraph = Paragraph(text=p, entry=entry)
        paragraph.save()


def index(request):
    if not request.user:
        HttpResponseRedirect(reverse("login"))
    entries = Entry.objects.all()
    return render(request, "gapfiller/index.html", {
        'entries': entries,
    })


def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        text = request.POST["text"]
        if not title or not text:
            return render(request, "gapfiller/create.html", {
                "message": "Warning Text couldn't be created: missing title or text!"
            })
        else:
            create_entry(title, text)
            return HttpResponseRedirect(reverse("index"))
    return render(request, "gapfiller/create.html", {
    })


def show(request, id):
    entry = Entry.objects.filter(pk=id).first()
    title = entry.title.tokens.all()
    paragraphs = entry.paragraphs.all()
    #rules = Rule.objects.all()
    #paras = [rule.rule.split("\n") for rule in rules]
    #names = [rule.name for rule in rules]
    #rules = [{"name": name, "paragraphs": para} for name, para in zip(names, paras)]
    user = request.user

    status = UserEntryGapFillerStatus.objects.filter(user=user, entry=entry).count()
    if status == 0:
        status = UserEntryGapFillerStatus(user=user, entry=entry)
        status.active = True
        status.save()
        return HttpResponseRedirect(reverse("choice_selection", args={id}))

    configs = UserEntryChoiceSelConfig.objects.filter(user=user, entry=entry)
    enabled_choices = [c.choice_selection for c in configs if c.enabled]

    podcast = entry.podcast

    return render(request, "gapfiller/show.html", {
        "title": title,
        "paragraphs": paragraphs,
        #"rules": rules,
        "podcast": podcast,
        "enabled_choices": enabled_choices,
        "id": entry.id
    })


def choice_selection(request, id):
    selections = ChoiceSelection.objects.all()

    if request.method == "POST":
        entry = Entry.objects.filter(pk=id).first()
        user = request.user
        s_names = [s.name for s in selections]
        for name in s_names:
            choice_selection = ChoiceSelection.objects.filter(name=name).first()
            if name in request.POST:
                config, created = UserEntryChoiceSelConfig.objects.update_or_create(
                    entry=entry,
                    user=user,
                    choice_selection=choice_selection,
                )
                config.enabled = True
                config.save()
            else:
                config, created = UserEntryChoiceSelConfig.objects.update_or_create(
                    entry=entry,
                    user=user,
                    choice_selection=choice_selection,
                )
                config.enabled = False
                config.save()
        return HttpResponseRedirect(reverse("show", args={id}))

    return render(request, "gapfiller/choice_selection.html", {
        "selections": selections,
        "id": id,
    })


def get_token_display_updates(request, id):
    token = Token.objects.get(pk=id)
    rules = []
    if token.local_choice_selection:
        choices = token.local_choice_selection.choices.all()
        rules = list(set([choice.rule.description for choice in choices]))
    return JsonResponse({
        "translation": token.translation,
        "word_translation": token.word_translation,
        "rules": rules
    })



def delete_gapfiller(request, id):
    entry = Entry.objects.get(pk=id)
    entry.delete()
    return HttpResponseRedirect(reverse("index"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "gapfiller/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "gapfiller/login.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "gapfiller/register.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
