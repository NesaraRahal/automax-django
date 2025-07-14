from .views import login_view, RegisterView, logout_view, ProfileView
from django.urls import path

urlpatterns = [
    path('login/', login_view, name = 'login'),
    path('register/', RegisterView.as_view(), name = 'register'),
    path('logout/', logout_view, name = 'logout'),
    path('profile/', ProfileView.as_view(), name = 'profile')
]
