from django.urls import path

from photos.views import gallery, addPhoto, viewPhoto

urlpatterns = [
    path('', gallery, name="gallery"),
    path('photo/<int:pk>/', viewPhoto, name="photo"),
    path('add/', addPhoto, name="add"),
]
