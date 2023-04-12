from django.urls import path
from . import views
from django.urls import include


urlpatterns = [
    # path('', views.login, name='login'),
    path('', include('django.contrib.auth.urls')),
    path('main/', views.index, name='index'),
    path('business_trip/', views.business_trip, name='business_trip'),
    path('mismatch/', views.mismatch, name='mismatch'),
    path('mismatch/<int:pk>', views.mismatch_detail, name='mismatch_detail'),
]