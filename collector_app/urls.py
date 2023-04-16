from django.urls import path, include
from . import views
from register import views as v
from .views import RollPage, RollAPIView, store_items
from register.views import ProfileUpdateView
app_name = 'main'

urlpatterns = [
    path("register/", v.register, name = 'register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', include('django.contrib.auth.urls')),
    path('search/', views.user_search, name='user_search'),
    path('about/', views.about, name='about'),
    path("roll/", RollPage.as_view() , name='roll'),
    path('roll-api/', views.RollAPIView, name='roll-api'),
    path('store-items/', views.store_items, name='store-items'),
    path('profile/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('profile/<int:profile_id>/comment/<int:comment_id>/delete', views.delete_comment, name='delete_comment'),
    path('profile/<int:profile_id>/comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('profile/<int:pk>/edit/', ProfileUpdateView.as_view(), name='edit_profile'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('', views.index),
]
