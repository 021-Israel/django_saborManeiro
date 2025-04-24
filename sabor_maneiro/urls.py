from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('home/', include('home.urls')),
    path('galeria/', include('galeria.urls')),
    path('historia/', include('historia.urls')),
    path('order/', include('order.urls')),
    path('reservar/', include('reservar.urls')),
]
urlpatterns += [
    path('accounts/', include ('django.contrib.auth.urls')),
]
