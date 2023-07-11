from django.urls import path

from photos.views import gallery, addPhoto, viewPhoto, delete_photo, updatePhoto, loginPage, logoutPage, userRegistration, userProfile

urlpatterns = [
    
    path('login/', loginPage, name='login'),
    path('logout/', logoutPage, name='logout'),
    path('register/', userRegistration, name='register'),
    path('user-profile/<int:pk>/', userProfile, name='profile'),

    path('', gallery, name="gallery"),
    path('photo/<int:pk>/', viewPhoto, name="photo"),
    path('add/', addPhoto, name="add"),
    path('delete/<int:pk>/', delete_photo, name='delete'),
    path('edit/<int:pk>/', updatePhoto, name='edit'),
]
