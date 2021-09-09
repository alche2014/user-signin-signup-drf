from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
import rest_framework.authtoken

from users import views

urlpatterns = [
    path('profile/',views.ProfileView.as_view()),
    path('api/auth/', views.CustomAuthToken.as_view()),
    path('api/login/', views.UserLoginAPIView.as_view()),
    path('api/signup/', views.UserSignupView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
