from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.conf import settings
from rest_framework import routers
from order.views import ProdutoViewSet
router = routers.DefaultRouter()
router.register('order', ProdutoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('home/', include('home.urls')),
    path('galeria/', include('galeria.urls')),
    path('historia/', include('historia.urls')),
    path('produtos/', include('order.urls')),
    path('reservar/', include('reservar.urls')),
]

urlpatterns += [
    path('accounts/', include ('django.contrib.auth.urls')),
]

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)