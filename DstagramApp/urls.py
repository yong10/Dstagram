from django.urls import path
from .import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('logUser', views.logUser),
    path('addUser', views.addUser),
    path('Dstagram', views.Dstagram),
    path('createPhoto', views.createPhoto),
    path('addPhoto', views.addPhoto),
    path('update/<int:id>', views.update),
    path('updatePhoto/<int:id>', views.updatePhoto),
    path('deletePhoto/<int:id>', views.deletePhoto),
    path('addComment/<int:id>', views.addComment),
    path('deleteComment/<int:id>', views.deleteComment),
    path('like/<int:id>', views.like),
    path('liked_post', views.liked_post),
    path('save/<int:id>', views.save),
    path('saved_post', views.saved_post),
    path('logout', views.logout),
]