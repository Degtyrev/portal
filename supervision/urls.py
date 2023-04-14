
from django.urls import path
from . import views
from django.urls import include


urlpatterns = [
    path('', views.index, name='index'),
    path('', include('django.contrib.auth.urls')),
    path('main/', views.index, name='index'),
]

urlpatterns += [
    path('mismatch/', views.mismatch, name='mismatch'),
    path('mismatch/<int:pk>', views.mismatch_detail, name='mismatch_detail'),
    path('mismatch/create/', views.MismatchCreate.as_view(), name='mismatch_create'),
    path('mismatch/<int:pk>/update/', views.MismatchUpdate.as_view(), name='mismatch_update'),
    path('mismatch/<int:pk>/delete/', views.MismatchDelete.as_view(), name='mismatch_delete'),
]

urlpatterns += [
    path('business_trip/', views.business_trip, name='business_trip'),
    path('business_trip/<int:pk>', views.trip, name='business_trip_detail'),
    path('business_trip/<int:pk>/extension/', views.extension_business_trip, name='extension_business_trip'),
    path('business_trip/create/', views.BusinessTripCreate.as_view(), name='business_trip_create'),
    path('business_trip/<int:pk>/update/', views.BusinessTripUpdate.as_view(), name='business_trip_update'),
    path('business_trip/<int:pk>/delete/', views.BusinessTripDelete.as_view(), name='business_trip_delete'),
]

urlpatterns += [
    path('place/', views.place_list, name='place_list'),
    path('place/<int:pk>', views.place_detail, name='place_detail'),
    path('place/create/', views.PlaсeCreate.as_view(), name='place_create'),
    path('place/<int:pk>/update/', views.PlaсeUpdate.as_view(), name='place_update'),
    path('place/<int:pk>/delete/', views.PlaсeDelete.as_view(), name='place_delete'),
]

urlpatterns += [
    path('unit/', views.unit_list, name='unit_list'),
    path('unit/<int:pk>', views.unit_detail, name='unit_detail'),
    path('unit/create/', views.UnitCreate.as_view(), name='unit_create'),
    path('unit/<int:pk>/update/', views.UnitUpdate.as_view(), name='unit_update'),
    path('unit/<int:pk>/delete/', views.UnitDelete.as_view(), name='unit_delete'),
]

urlpatterns += [
    path('element/', views.element_list, name='element_list'),
    path('element/<int:pk>', views.element_detail, name='element_detail'),
    path('element/create/', views.ElementCreate.as_view(), name='element_create'),
    path('element/<int:pk>/update/', views.ElementUpdate.as_view(), name='element_update'),
    path('element/<int:pk>/delete/', views.ElementDelete.as_view(), name='element_delete'),
]

urlpatterns += [
    path('employee/', views.employee_list, name='employee_list'),
    path('employee/<int:pk>', views.employee_detail, name='employee_detail'),
    path('employee/create/', views.EmployeeCreate.as_view(), name='employee_create'),
    path('employee/<int:pk>/update/', views.EmployeeUpdate.as_view(), name='employee_update'),
    path('employee/<int:pk>/delete/', views.EmployeeDelete.as_view(), name='employee_delete'),
]