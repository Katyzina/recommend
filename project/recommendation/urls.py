from django.urls import path

from recommendation.views import HomePageView

urlpatterns = [
    path('', HomePageView.as_view()),
]
