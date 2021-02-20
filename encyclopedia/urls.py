from django.urls import path, include

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", include([ 
        path('', views.wikies,  name="title"), 
        path('edit/', views.edit, name="edit"),
    ])),
    path("search", views.searchentry, name="searchentry"),
    path("newentry", views.saveEntry, name="save_content"),    
    path("editform", views.editform, name="editform"),
    path('random', views.randomentry, name='random'),
]