from django.contrib.auth import authenticate, login, logout
from django.db import models
from django.db.models import Value, F, Q, Subquery, Case, When, BooleanField, Exists, OuterRef
from django.shortcuts import render, redirect
from django.views import View

from tables_app.models import Institute, Vacation, Student, User, Employer, Favourite


class HomePageView(View):

    def get(self, request, *args, **kwargs):
        institutes = Institute.objects.all()
        vacations = Vacation.objects.annotate(
            is_favourite=Exists(
                Favourite.objects.filter(
                    vacation_id=OuterRef('id'),
                    user=request.user if request.user.is_authenticated else None
                )
            )
        ).all()
        institute = None
        if kwargs.get('institute_id'):
            institute = institutes.get(id=kwargs['institute_id'])
            vacations = vacations.filter(institute_id=kwargs['institute_id'])
        if request.GET.get('search'):
            vacations = vacations.filter(
                Q(position__icontains=request.GET['search']) |
                Q(description__icontains=request.GET['search'])
            )
        return render(request, 'index.html', context={
            "institutes": institutes,
            "vacations": vacations,
            "institute_id": kwargs['institute_id'] if kwargs.get('institute_id') else None,
            "institute": institute
        })


class UserLoginView(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        user = authenticate(
            request,
            username=request.POST['email'],
            password=request.POST['password'],
        )
        if user:
            login(request, user)
            return redirect('home')
        return redirect('login')


class EmployerRegisterView(View):
    def get(self, request):
        return render(request, 'hrlog.html')

    def post(self, request):
        try:
            employer_info = Employer.objects.create(
                organization=request.POST['organization'],
            )
            User.objects.create_user(
                username=request.POST['email'],
                password=request.POST['password'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                middle_name=request.POST['middle_name'],
                phone_number=request.POST['phone_number'],
                email=request.POST['email'],
                employer=employer_info,
            )
        except Exception as error:
            return redirect('regstud')
        else:
            return redirect('login')


class StudentRegisterView(View):
    def get(self, request):
        institutes = Institute.objects.all()
        return render(request, 'regstud.html', context={
            'institutes': institutes
        })

    def post(self, request):
        try:
            student_info = Student.objects.create(
                institute_id=request.POST['institute'],
                study_group=request.POST['study_group']
            )
            User.objects.create_user(
                username=request.POST['email'],
                password=request.POST['password'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                middle_name=request.POST['middle_name'],
                phone_number=request.POST['phone_number'],
                email=request.POST['email'],
                student=student_info,
            )
        except Exception as error:
            return redirect('regstud')
        else:
            return redirect('login')


class SupportCreateView(View):
    def get(self, request):
        return render(request, 'support.html')


class EmployerListView(View):

    def get(self, request):
        return render(request, 'employerlist.html')


class StudentProfileView(View):
    def get(self, request):
        favourite_vacations = Favourite.objects.filter(user=request.user).values_list('vacation__id', flat=True)
        vacations = Vacation.objects.filter(id__in=favourite_vacations)
        return render(request, 'studprofile.html', context={
            "vacations": vacations
        })


def logout_user(request):
    logout(request)
    return redirect('home')


class EmployerProfileView(View):
    def get(self, request):
        return render(request, 'employerprofile.html')


class AboutVacancyView(View):
    def get(self, request):
        return render(request, 'aboutvacancy.html')

class CreateVacancyView(View):
    def get(self, request):
        return render(request, 'createvacancy.html')


class VacationFavouriteCreateView(View):

    def get(self, request, vacation_id):
        vacation = Vacation.objects.get(id=vacation_id)
        Favourite.objects.create(
            vacation=vacation,
            user=request.user
        )
        return redirect('home')


class VacationFavouriteDeleteView(View):

    def get(self, request, vacation_id):
        vacation = Vacation.objects.get(id=vacation_id)
        Favourite.objects.filter(
            vacation=vacation,
            user=request.user
        ).delete()
        return redirect('home')
