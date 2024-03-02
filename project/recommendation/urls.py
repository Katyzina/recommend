from django.urls import path

from recommendation.views import home_page

urlpatterns = [
    path('', home_page),
]
