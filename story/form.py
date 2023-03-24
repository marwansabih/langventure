from django import forms
from .models import Collectible


class CollectibleForm(forms.ModelForm):
    class Meta:
        model = Collectible
        fields = ['name', 'knowledge_item', 'image']