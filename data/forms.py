from django import forms
from .models import APIMethod, Thread, Game
from django.db.models import Max

class APISearchForm(forms.Form):
    method = forms.ModelChoiceField(queryset=APIMethod.objects.all(), label="Select API Method", to_field_name="name")

    def __init__(self, *args, **kwargs):
        super(APISearchForm, self).__init__(*args, **kwargs)
        # The modifier field is no longer needed here

class ThreadCollectorForm(forms.Form):
    thread = forms.IntegerField()


class ThreadSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ThreadSearchForm, self).__init__(*args, **kwargs)
        unique_articles = Thread.objects.order_by('article', '-id').distinct('article')
        self.fields['thread'] = forms.ModelChoiceField(
            queryset=unique_articles,
            label="Select Thread by Article",
            to_field_name="article"
        )

    title_words = forms.CharField(required=False)
    content_words = forms.CharField(required=False)


class NounChunkCreateForm(forms.Form):
    game_name = forms.ModelChoiceField(queryset=Game.objects.all().order_by('game_name'), required=True, label='Game')
    exclusion_words = forms.CharField(required=False, label='Choose words to exclude from chunks')

    def __init__(self, *args, **kwargs):
        super(NounChunkCreateForm, self).__init__(*args, **kwargs)
        self.fields['game_name'].empty_label = 'Select A Game'