
from django.urls import path, re_path
from . import views
from django.urls import include


urlpatterns = [
    path('', views.index, name='index'),
    path('main/', views.index, name='index'),
    path('admin_page/', views.admin_page, name='admin_page')
]

urlpatterns += [
    path('mismatch/', views.mismatch_list, name='mismatch_list'),
    path('mismatch/<int:pk>/', views.mismatch_detail, name='mismatch_detail'),
    path('mismatch/<int:pk>/close', views.mismatch_close, name='close_mismatch'),
    path('mismatch/create/', views.mismatch_create, name='mismatch_create'),
    # path('mismatch/create/', views.MismatchCreate.as_view(), name='mismatch_create'),
    path('mismatch/<int:pk>/update/', views.MismatchUpdate.as_view(), name='mismatch_update'),
    path('mismatch/<int:pk>/delete/', views.MismatchDelete.as_view(), name='mismatch_delete'),

    path('mismatch_filter/', views.mismatch_filter, name='mismatch_filter'),
]

urlpatterns += [
    path('business_trip/', views.business_trip, name='business_trip'),
    path('business_trip/<int:pk>/', views.trip, name='business_trip_detail'),
    path('business_trip/<int:pk>/extension/', views.extension_business_trip, name='extension_business_trip'),
    path('business_trip/create/', views.business_trip_create, name='business_trip_create'),
    # path('business_trip/create/', views.BusinessTripCreate.as_view(), name='business_trip_create'),
    path('business_trip/<int:pk>/update/', views.BusinessTripUpdate.as_view(), name='business_trip_update'),
    path('business_trip/<int:pk>/delete/', views.BusinessTripDelete.as_view(), name='business_trip_delete'),

    path('condition/<int:pk>/', views.condition_show, name='condition'),
]

urlpatterns += [
    path('place/', views.place_list, name='place_list'),
    path('place/<int:pk>/', views.place_detail, name='place_detail'),
    path('place/create/', views.place_create, name='place_create'),
    path('place/<int:pk>/update/', views.PlaceUpdate.as_view(), name='place_update'),
    path('place/<int:pk>/delete/', views.PlaceDelete.as_view(), name='place_delete'),
]

urlpatterns += [
    path('group/', views.group_list, name='group_list'),
    path('group/<int:pk>/', views.group_detail, name='group_detail'),
    path('group/create/', views.group_create, name='group_create'),
    path('group/<int:pk>/update/', views.GroupUpdate.as_view(), name='group_update'),
    path('group/<int:pk>/delete/', views.GroupDelete.as_view(), name='group_delete'),
]

# urlpatterns += [
#     path('drawing/', views.drawing_list, name='drawing_list'),
#     path('drawing/<int:pk>/', views.drawing_detail, name='drawing_detail'),
#     path('drawing/create/', views.drawing_create, name='drawing_create'),
#     path('drawing/<int:pk>/update/', views.DrawingUpdate.as_view(), name='drawing_update'),
#     path('drawing/<int:pk>/delete/', views.DrawingDelete.as_view(), name='drawing_delete'),
# ]

# urlpatterns += [
#     path('detail/', views.detail_list, name='detail_list'),
#     path('detail/<int:pk>/', views.detail_detail, name='detail_detail'),
#     path('detail/create/', views.DetailCreate.as_view(), name='detail_create'),
#     path('detail/<int:pk>/update/', views.DetailUpdate.as_view(), name='detail_update'),
#     path('detail/<int:pk>/delete/', views.DetailDelete.as_view(), name='detail_delete'),
# ]

urlpatterns += [
    path('employee/', views.employee_list, name='employee_list'),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('employee/<int:pk>/update/', views.employee_update, name='employee_update'),
    # path('employee/<int:pk>/update/', views.EmployeeUpdate.as_view(), name='employee_update'),

]

urlpatterns += [
    path('letter/', views.letter_list, name='letter_list'),
    path('letter/<int:pk>/', views.letter_detail, name='letter_detail'),
    re_path(r'^letter/create/$', views.letter_create, name='letter_create'),
    path('letter/<int:pk>/update/', views.LetterUpdate.as_view(), name='letter_update'),
    # path('letter/<int:pk>/delete/', views.LetterDelete.as_view(), name='letter_delete'),
]

urlpatterns += [
    path('solution/', views.solution_list, name='solution_list'),
    path('solution/<int:pk>/', views.solution_detail, name='solution_detail'),
    path('solution/create/', views.solution_create, name='solution_create'),
    path('solution/<int:pk>/update/', views.SolutionUpdate.as_view(), name='solution_update'),
    # path('solution/<int:pk>/delete/', views.SolutionDelete.as_view(), name='solution_delete'),
]

urlpatterns += [
    path('place_status/', views.place_status_list, name='place_status_list'),
    path('status_place/<int:pk>/', views.place_status_show, name='status_place'),
    # path('place_status/<int:pk>/', views.place_status_detail, name='place_status_detail'),
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

urlpatterns += [
    path('position/', views.position_list, name='position_list'),
    # path('position/<int:pk>/', views.position_detail, name='position_detail'),
    path('position/create/', views.PositionCreate.as_view(), name='position_create'),
    path('position/<int:pk>/update/', views.PositionUpdate.as_view(), name='position_update'),
    path('position/<int:pk>/delete/', views.PositionDelete.as_view(), name='position_delete'),
]

urlpatterns += [
    path('condition_trip/', views.condition_trip_list, name='condition_trip_list'),
    # path('condition_trip/<int:pk>/', views.condition_trip_detail, name='condition_trip_detail'),
    path('condition_trip/create/', views.ConditionTripCreate.as_view(), name='condition_trip_create'),
    path('condition_trip/<int:pk>/update/', views.ConditionTripUpdate.as_view(), name='condition_trip_update'),
    path('condition_trip/<int:pk>/delete/', views.ConditionTripDelete.as_view(), name='condition_trip_delete'),
]

urlpatterns += [
    path('status_mismatch/', views.status_mismatch_list, name='status_mismatch_list'),
    # path('status_mismatch/<int:pk>/', views.status_mismatch_detail, name='status_mismatch_detail'),
    path('status_mismatch/create/', views.StatusMismatchCreate.as_view(), name='status_mismatch_create'),
    path('status_mismatch/<int:pk>/update/', views.StatusMismatchUpdate.as_view(), name='status_mismatch_update'),
    path('status_mismatch/<int:pk>/delete/', views.StatusMismatchDelete.as_view(), name='status_mismatch_delete'),
]
