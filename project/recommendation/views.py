from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View

from tables_app.models import Institute, Vacation, Student, User, Employer


class HomePageView(View):

    def get(self, request, *args, **kwargs):
        institutes = Institute.objects.all()
        vacations = Vacation.objects.all()
        if kwargs.get('institute_id'):
            vacations = vacations.filter(institute_id=kwargs['institute_id'])
        return render(request, 'index.html', context={
            "institutes": institutes,
            "vacations": vacations,
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
        return render(request, 'studprofile.html')


def logout_user(request):
    logout(request)
    return redirect('home')
