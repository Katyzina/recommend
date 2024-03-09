from django.urls import path

from recommendation.views import (
    HomePageView, UserLoginView, EmployerRegisterView,
    StudentRegisterView, SupportCreateView, EmployerListView,
    StudentProfileView, logout_user
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('<int:institute_id>/', HomePageView.as_view(), name='filter_vacation'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('hrlog/', EmployerRegisterView.as_view(), name='hrlog'),
    path('regstud/', StudentRegisterView.as_view(), name='regstud'),
    path('support/', SupportCreateView.as_view(), name='support'),
    path('employerlist/', EmployerListView.as_view(), name='employerlist'),
    path('studprofile/', StudentProfileView.as_view(), name='studprofile'),
]
