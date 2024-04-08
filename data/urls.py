from django.urls import path
from . import views


urlpatterns = [
    path('', views.data, name='data'),
    path('bgg/', views.bgg_view, name='bgg_view'),
    path('get_modifiers/<str:method_name>/', views.get_modifiers_for_method, name='get_modifiers'),
    path('search_history/', views.search_history, name='search_historys'),
    path('thread_collector/', views.thread_collector, name='thread_collector'),
    path('thread_analyzer/', views.thread_analyzer, name='thread_analyzer'),
    path('chunker/', views.noun_chunker, name='noun_chunker'),
]
