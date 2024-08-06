from django.urls import path
from .views import RegisterView, login_view, LogoutView, UserProfileView, AuthStatusView, CsrfTokenView,ProfileUpdateView, VolunteerCreateView, VolunteerDetailView,VolunteerListView, UserListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),  
    path('logout/', LogoutView.as_view(), name='logout'),  
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'), 
    path('auth/status/', AuthStatusView.as_view(), name='auth_status'),
    path('csrf/', CsrfTokenView.as_view(), name='csrf'),
    path('volunteer/', VolunteerListView.as_view(), name='volunteer-list'),  # Add the list view here
    path('volunteer/create/', VolunteerCreateView.as_view(), name='volunteer-create'), 
    path('volunteer/<int:pk>/', VolunteerDetailView.as_view(), name='volunteer-detail'),
]


