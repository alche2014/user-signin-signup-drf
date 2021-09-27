from django.urls import path

from .views import GoogleSocialAuthView, FacebookSocialAuthView, AppleSocialAuthView

app_name = 'social_login'
urlpatterns = [
    path('google/', GoogleSocialAuthView.as_view()),
    path('facebook/', FacebookSocialAuthView.as_view()),
    path('apple/', AppleSocialAuthView.as_view()),


]
