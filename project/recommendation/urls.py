from django.urls import path

from recommendation.views import HomePageView, login_view, hrlog_view, regstud_view, support_view, employerlist_view, studprofile_view

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login/', login_view, name='login'),
    path('hrlog/', hrlog_view, name='hrlog'),
    path('regstud/', regstud_view, name='regstud'),
    path('support/', support_view, name='support'),
    path('employerlist/', employerlist_view, name='employerlist'),
    path('studprofile/', studprofile_view, name='studprofile'),
]
