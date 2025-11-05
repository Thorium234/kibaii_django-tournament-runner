from django.urls import path, include
from .views import SignUpView, home, profile

urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/profile/', profile, name='profile'),
]
