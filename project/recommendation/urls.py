from django.urls import path

from recommendation.views import (
    HomePageView, UserLoginView, EmployerRegisterView,
    StudentRegisterView, SupportCreateView, EmployerListView,
    StudentProfileView, EmployerProfileView, AboutVacancyView, logout_user,
    VacationFavouriteCreateView, VacationFavouriteDeleteView, CreateVacancyView
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('<int:institute_id>/', HomePageView.as_view(), name='filter_vacation'),

    path('vacations/search/', HomePageView.as_view(), name='search_vacation'),

    path('vacations/<int:vacation_id>/favourite/', VacationFavouriteCreateView.as_view(), name='favourite'),
    path('vacations/<int:vacation_id>/favourite_delete/', VacationFavouriteDeleteView.as_view(), name='favourite_delete'),

    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('hrlog/', EmployerRegisterView.as_view(), name='hrlog'),
    path('regstud/', StudentRegisterView.as_view(), name='regstud'),
    path('support/', SupportCreateView.as_view(), name='support'),
    path('employerlist/', EmployerListView.as_view(), name='employerlist'),
    path('studprofile/', StudentProfileView.as_view(), name='studprofile'),
    path('employerprofile/', EmployerProfileView.as_view(), name='employerprofile'),
    path('aboutvacancy/', AboutVacancyView.as_view(), name='aboutvacancy'),
    path('createvacancy/', CreateVacancyView.as_view(), name='createvacancy'),
]
