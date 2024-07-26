from django.urls import path
from .views import RegisterView, login_view, LogoutView, UserProfileView, AuthStatusView, CsrfTokenView,ProfileUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),  
    path('logout/', LogoutView.as_view(), name='logout'),  
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'), 
    path('auth/status/', AuthStatusView.as_view(), name='auth_status'),
    path('csrf/', CsrfTokenView.as_view(), name='csrf'),
]


