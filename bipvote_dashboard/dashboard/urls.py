from django.urls import path

from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
    path('index/', views.index, name='index'),
    path('vote/', views.vote, name='vote'),
    path('topic/', views.topic, name='topic'),
    path('create_topic/', views.create_topic, name='create_topic'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('collect_dtmf/', views.collect_dtmf, name='collect_dtmf'),
]