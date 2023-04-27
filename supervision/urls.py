
from django.urls import path
from . import views
from django.urls import include


urlpatterns = [
    path('', views.index, name='index'),
    path('main/', views.index, name='index'),
]

urlpatterns += [
    path('mismatch/', views.mismatch_list, name='mismatch_list'),
    path('mismatch/<int:pk>/', views.mismatch_detail, name='mismatch_detail'),
    path('mismatch/create/', views.mismatch_create, name='mismatch_create'),
    # path('mismatch/create/', views.MismatchCreate.as_view(), name='mismatch_create'),
    path('mismatch/<int:pk>/update/', views.MismatchUpdate.as_view(), name='mismatch_update'),
    path('mismatch/<int:pk>/delete/', views.MismatchDelete.as_view(), name='mismatch_delete'),
]

urlpatterns += [
    path('business_trip/', views.business_trip, name='business_trip'),
    path('business_trip/<int:pk>/', views.trip, name='business_trip_detail'),
    path('business_trip/<int:pk>/extension/', views.extension_business_trip, name='extension_business_trip'),
    path('business_trip/create/', views.BusinessTripCreate.as_view(), name='business_trip_create'),
    path('business_trip/<int:pk>/update/', views.BusinessTripUpdate.as_view(), name='business_trip_update'),
    path('business_trip/<int:pk>/delete/', views.BusinessTripDelete.as_view(), name='business_trip_delete'),
]

urlpatterns += [
    path('place/', views.place_list, name='place_list'),
    path('place/<int:pk>/', views.place_detail, name='place_detail'),
    path('place/create/', views.place_create, name='place_create'),
    path('place/<int:pk>/update/', views.PlaceUpdate.as_view(), name='place_update'),
    path('place/<int:pk>/delete/', views.PlaceDelete.as_view(), name='place_delete'),
]

urlpatterns += [
    path('group/plase/<int:pk>/', views.group_list, name='group_list'),
    path('group/<int:pk>/', views.group_detail, name='group_detail'),
    path('group/create/<int:pk>', views.GroupCreate.as_view(), name='group_create'),
    path('group/<int:pk>/update/', views.GroupUpdate.as_view(), name='group_update'),
    path('group/<int:pk>/delete/', views.GroupDelete.as_view(), name='group_delete'),
]

urlpatterns += [
    path('drawing/', views.drawing_list, name='drawing_list'),
    path('drawing/<int:pk>/', views.drawing_detail, name='drawing_detail'),
    path('drawing/create/', views.DrawingCreate.as_view(), name='drawing_create'),
    path('drawing/<int:pk>/update/', views.DrawingUpdate.as_view(), name='drawing_update'),
    path('drawing/<int:pk>/delete/', views.DrawingDelete.as_view(), name='drawing_delete'),
]

urlpatterns += [
    path('detail/', views.detail_list, name='detail_list'),
    path('detail/<int:pk>/', views.detail_detail, name='detail_detail'),
    path('detail/create/', views.DetailCreate.as_view(), name='detail_create'),
    path('detail/<int:pk>/update/', views.DetailUpdate.as_view(), name='detail_update'),
    path('detail/<int:pk>/delete/', views.DetailDelete.as_view(), name='detail_delete'),
]

urlpatterns += [
    path('employee/', views.employee_list, name='employee_list'),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employee/create/', views.EmployeeCreate.as_view(), name='employee_create'),
    path('employee/<int:pk>/update/', views.EmployeeUpdate.as_view(), name='employee_update'),
    path('employee/<int:pk>/delete/', views.EmployeeDelete.as_view(), name='employee_delete'),
]

urlpatterns += [
    path('letter/', views.letter_list, name='letter_list'),
    path('letter/<int:pk>/', views.letter_detail, name='letter_detail'),
    path('letter/create/', views.LetterCreate.as_view(), name='letter_create'),
    path('letter/<int:pk>/update/', views.LetterUpdate.as_view(), name='letter_update'),
    path('letter/<int:pk>/delete/', views.LetterDelete.as_view(), name='letter_delete'),
]

urlpatterns += [
    path('solution/', views.solution_list, name='solution_list'),
    path('solution/<int:pk>/', views.solution_detail, name='solution_detail'),
    path('solution/create/', views.SolutionCreate.as_view(), name='solution_create'),
    path('solution/<int:pk>/update/', views.SolutionUpdate.as_view(), name='solution_update'),
    path('solution/<int:pk>/delete/', views.SolutionDelete.as_view(), name='solution_delete'),
]

urlpatterns += [
    path('place_status/', views.place_status_list, name='place_status_list'),
    path('status_place/<int:status_id>/', views.place_status_show, name='status_place'),
    path('place_status/<int:pk>/', views.place_status_detail, name='place_status_detail'),
    path('place_status/create/', views.PlaceStatusCreate.as_view(), name='place_status_create'),
    path('place_status/<int:pk>/update/', views.PlaceStatusUpdate.as_view(), name='place_status_update'),
    path('place_status/<int:pk>/delete/', views.PlaceStatusDelete.as_view(), name='place_status_delete'),
]

urlpatterns += [
    path('type_mismatch/', views.type_mismatch_list, name='type_mismatch_list'),
    # path('status_place/<int:status_id>/', views.type_mismatch_show, name='status_place'),
    path('type_mismatch/<int:pk>/', views.type_mismatch_detail, name='type_mismatch_detail'),
    path('type_mismatch/create/', views.TypeMismatchCreate.as_view(), name='type_mismatch_create'),
    path('type_mismatch/<int:pk>/update/', views.TypeMismatchUpdate.as_view(), name='type_mismatch_update'),
    path('type_mismatch/<int:pk>/delete/', views.TypeMismatchDelete.as_view(), name='type_mismatch_delete'),
]