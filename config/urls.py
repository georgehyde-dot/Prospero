from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crm/', include(('website.urls', 'website'), namespace='website')),  
    path('data/', include(('data.urls', 'data'), namespace='data')),  
    path('visualize/', include(('visualize.urls', 'visualize'), namespace='visualize')), 

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
