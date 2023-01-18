from django.urls import path
from rest_framework_simplejwt.views import (
    TokenVerifyView
)
from .models import MyTokenObtainPairView, MyTokenObtainRefreshView

urlpatterns = [
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', MyTokenObtainRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
