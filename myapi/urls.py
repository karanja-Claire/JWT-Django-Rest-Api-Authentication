from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from myapi.views import auth_views 

urlpatterns = [
    
    path('api/token/', auth_views.LoginView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', auth_views.RegisterView.as_view(), name='register'),
    
]