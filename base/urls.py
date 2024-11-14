from django.urls import path
from . import views

app_name = 'base'

urlpatterns = [
    # Dashboard
    path('', views.Dashboard, name='dashboard'),
    # watch regular fields data
    path('fields/', views.Fields_Track, name='fields_track'),
    path('<str:field_id>/lines', views.Lines_Track, name='lines_track'),
    # define new qr codes for fields
    path('qr_define/', views.QR_Define_Field, name='qr_define_field'),
    path('qr_define/<str:field_id>', views.QR_Define_Lines, name='qr_define_lines'),
    # choose field for activity
    path('choose_activity_field/', views.Choose_Activity_Field, name='choose_activity_field'),
    # start activity for chosen field
    path('activity/<str:field_id>', views.Activity, name='activity'),
]
