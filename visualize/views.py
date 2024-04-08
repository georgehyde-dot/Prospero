from django.shortcuts import render, redirect
from data.models import APIMethod, APIMethodModifier
from .bokeh_plot import create_base_flowchart,update_flowchart_with_metadata
from bokeh.embed import components 
from data.models import Game, Comment, Rating
from .forms import CommentSearchForm
from .tasks import import_word_cloud
import spacy
from collections import Counter
from django.contrib import messages
from django.contrib.auth.decorators import login_required

nlp = spacy.load('en_core_web_md')



# Create your views here.
@login_required
def visualize(request):
    apiMethods = APIMethod.objects.all()
    apiMethodModifiers = APIMethodModifier.objects.all()
    apiValues = {
        'apiMethods':apiMethods,
        'apiMethodModifiers':apiMethodModifiers
    }
    return render(request, 'visualize/visualize.html', apiValues)

@login_required
def graphic(request):
    # Example metadata
    metadata = {
        'labels': ['Start', 'Middle', 'End']
    }

    # Create base plot
    plot, source = create_base_flowchart()

    # Update plot with metadata
    update_flowchart_with_metadata(plot, source, metadata)

    script, div = components(plot)

    context = {'script': script, 'div': div}
    return render(request, 'visualize/graphic.html', context)

@login_required
def comment_search(request):
    form = CommentSearchForm(request.GET or None)
    results = None
    comments_results = None
    word_cloud = False

    if form.is_valid():
        create_word_cloud = form.cleaned_data.get('create_word_cloud', True)
        print(f"Create Word Cloud: {create_word_cloud}")

        game_name = form.cleaned_data.get('game_name')
        min_rating = form.cleaned_data.get('min_rating')
        comment_keywords = form.cleaned_data.get('comment_keywords')
        split_keywords = comment_keywords.split()
        keyword_list = [word for word in split_keywords]
        
        if min_rating:
            query = Rating.objects.filter(rating__gte=min_rating)
            if comment_keywords:
                query = query.filter(comment__icontains=comment_keywords)
        
        else: 
            query = Comment.objects.all()
            if comment_keywords:
                query = query.filter(comment__icontains=comment_keywords)
            comments_results = list(query)
        if game_name:
            query = query.filter(game__game_name__icontains=game_name)

        results = query
        print(create_word_cloud)
        if create_word_cloud:
            
            comments_text = " ".join(comment.comment for comment in results)
            word_cloud = import_word_cloud(comments_text)
            
        

    return render(request, 'visualize/comment_search.html', {'form': form, 
                                                             'results': results,
                                                             'word_cloud': word_cloud
                                                             })


@login_required
def display_chunks(request):
    ...

@login_required
def get_my_data():
    return {
        'x_values': [1, 2, 3],
        'y_values': [4, 5, 6],
        'texts': ['A', 'B', 'C'],
        'numbers': [10, 20, 30]
    }
