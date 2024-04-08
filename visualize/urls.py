from django.urls import path
from . import views


urlpatterns = [
    path('', views.graphic, name='graphic'),
    path('options/', views.visualize, name='visualize'),
    path('comment_search/', views.comment_search, name='comment_search'),
    # path('display_chunks/')
    
]
