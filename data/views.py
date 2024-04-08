from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .libs.boardgamegeek import BGGClient
from .forms import APISearchForm, ThreadCollectorForm, ThreadSearchForm, NounChunkCreateForm
from django.http import JsonResponse
from .libs.bgg_api_form_request import call_bgg
from .libs import thread_parser, analyze_thread_sentiment, chunk_parser
import json
# Create your views here.
from django.http import HttpResponse, JsonResponse
from .models import APIMethodModifier, APIMethod, SearchLog, Thread, NounChunk
from django.db.models import Max
from .tasks import process_search_log
import logging

logger = logging.getLogger(__name__)

@login_required
def search_history(request):
    logs = SearchLog.objects.all().order_by('-created_at')
    return render(request, 'data/search_history.html', {'logs': logs})

@login_required
def get_modifiers_for_method(request, method_name):
    modifiers = APIMethodModifier.objects.filter(method__name=method_name).values('modifier_name', 'modifier_type')
    return JsonResponse(list(modifiers), safe=False)

@login_required
def data(request):
    if request.method == 'POST':
        if not request.body:
            return JsonResponse({'error': 'Empty request body'}, status=400)
        
        modifiers = {}
        method_name = request.POST.get('method')
        method = APIMethod.objects.get(name=method_name)

        for key, value in request.POST.items():
            if key != 'csrfmiddlewaretoken' and key != 'method':
                modifier = APIMethodModifier.objects.filter(modifier_name=key, method=method).first()
                if modifier:
                    modifier_type = modifier.modifier_type
                    
                    modifiers[key] = convert_modifier_value(modifier_type, value)
        #print(f'Method Name: {method_name}, Modifiers: {modifiers}')
        bgg_response = call_bgg(method_name, modifiers)
        
        search_data = {key: value for key, value in request.POST.items() if key != 'csrfmiddlewaretoken'}
        # Log the search in the SearchLog model
        search_log = SearchLog(
            search_request=json.dumps(search_data),
            search_response=json.dumps(bgg_response),
            source = "BGG"
        )
        search_log.save()

        check_value = process_search_log.delay(search_log_id=search_log.id)
       #print(f"Search Log Checks {check_value}")
        context = {
            'form': APISearchForm(request.POST or None),
            'bgg_response': bgg_response
        }
        return render(request, 'data/data.html', context)
    else:
        form = APISearchForm()
        return render(request, 'data/data.html', {'form': form})


@login_required
def bgg_view(request):
    bgg = BGGClient()
    hot_games = bgg.hot_items("boardgame")
    return render(request, 'data/bgg_page.html', {'hot_games':hot_games})

def convert_modifier_value(modifier_type, value):
    converters = {
        'int': lambda v: int(v) if v.isdigit() else v,
        'bool': lambda v: v.lower() == 'true',
        'text': lambda v: v
    }

    return converters.get(modifier_type, lambda v: v)(value)

@login_required
def thread_collector(request):
    if request.method == 'POST':
        form = ThreadCollectorForm(request.POST)
        if form.is_valid():  
            thread_id = request.POST.get('thread')
            attempt = thread_parser.main(thread_id)  
            if attempt:
                messages.success(request, f'Thread {thread_id} Processed')
                thread_data = Thread.objects.filter(thread_id=thread_id) 
                context = {
                    'form': form,
                    'thread_data': thread_data
                }
            else:
                messages.error(request, 'Thread Collector Failed')
                context = {
                    'form': form,
                    'thread_data': "Thread Collector Failed"
                }
            return render(request, 'data/thread_collector.html', context)
    else:
        form = ThreadCollectorForm()
    
    return render(request, 'data/thread_collector.html', {'form': form})

@login_required
def thread_analyzer(request):
    if request.method =='POST':
        form = ThreadSearchForm(request.POST)
        if form.is_valid():  
            thread_id = request.POST.get('thread')
            title_words =request.POST.get('title_words')
            content_words =request.POST.get('content_words') 
            input = {
                "thread_id": thread_id,
                "title_words": title_words,
                "content_words": content_words
            }
            analysis = analyze_thread_sentiment.main(input)

            context = {
                'form': form,  # Include the form in the context
                'analysis': analysis  # Your analysis data
            }
            return render(request, 'data/thread_analyzer.html', context)

    else:
       form = ThreadSearchForm(request.POST or None)
    
    return render(request, 'data/thread_analyzer.html', {'form': form})


@login_required
def noun_chunker(request):
    if request.method == 'POST':
        form = NounChunkCreateForm(request.POST)
        if form.is_valid():
            game = form.cleaned_data['game_name']
            
            exclusion_words = form.cleaned_data.get('exclusion_words', '').split()
            
            comments_text = " ".join(comment.comment for comment in game.comment_set.all())
            
            chunks_data = chunk_parser.cluster_chunks(comments_text, exclusion_words)  
            
            # Determine the next version number for the new NounChunk instance
            max_version = NounChunk.objects.filter(game=game).aggregate(Max('version'))['version__max']
            next_version = (max_version or 0) + 1
            
            NounChunk.objects.create(game=game, chunks_data=chunks_data, version=next_version)
            messages.success(request, 'Game analyzed and chunked')
            return redirect('data/chunker/') 
    else:
        form = NounChunkCreateForm(request.GET or None)
    return render(request, 'data/chunker.html', {'form': form})