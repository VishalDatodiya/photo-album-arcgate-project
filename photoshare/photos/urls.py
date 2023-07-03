from django.urls import path

from photos.views import gallery, addPhoto, viewPhoto, delete_photo, updatePhoto

urlpatterns = [
    path('', gallery, name="gallery"),
    path('photo/<int:pk>/', viewPhoto, name="photo"),
    path('add/', addPhoto, name="add"),
    path('delete/<int:pk>/', delete_photo, name='delete'),
    path('edit/<int:pk>/', updatePhoto, name='edit'),
]
