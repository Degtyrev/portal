"""portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from supervision.views import pageNotFound

urlpatterns = [
    path('admin/', admin.site.urls),
]
from django.urls import include

from django.views.generic import RedirectView
urlpatterns += [
    # редирект при пустом адресе
    path('', RedirectView.as_view(url='/supervision/', permanent=True)),
]

urlpatterns += [
#станица приветствия
    path('supervision/', include('users.urls')),
#станица аутентификации
    path('accounts/', include('django.contrib.auth.urls')),
#станица домашняя
    path('home/', include('supervision.urls')),

]
# обработка несуществующей страницы и ошибок 404, 301, 302, 500

handler404 = pageNotFound


from django.conf.urls.static import static
from django.conf import settings

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

