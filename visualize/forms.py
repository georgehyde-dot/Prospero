# forms.py

from django import forms
from data.models import Game, NounChunk

class CommentSearchForm(forms.Form):
    game_name = forms.ModelChoiceField(queryset=Game.objects.all().order_by('game_name'),required=False, label='Game')
    min_rating = forms.FloatField(required=False, label='Min Rating')
    # max_rating = forms.FloatField(required=False, label='Max Rating')
    comment_keywords = forms.CharField(required=False, label='Keywords in Comment')
    word_cloud_check = forms.BooleanField(required=False, label='Select this to get a word cloud of all selected comments')
    
    def __init__(self, *args, **kwargs):
        super(CommentSearchForm, self).__init__(*args, **kwargs)
        self.fields['game_name'].empty_label = "Select a Game"

        