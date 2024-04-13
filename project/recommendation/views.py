from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.db.models import Q, Exists, OuterRef, Case, When, Value, BooleanField
from django.shortcuts import render, redirect
from django.views import View

from tables_app.models import Institute, Vacation, Student, User, Employer, Favourite, Reply, City


class HomePageView(View):

    def get(self, request, *args, **kwargs):
        institutes = Institute.objects.all()
        if request.user.is_authenticated and request.user.student:
            similar_user = User.objects.filter(
                Q(city=request.user.city) |
                Q(student__institute=request.user.student.institute) |
                Q(student__university=request.user.student.university)
            ).exclude(
                Q(id=request.user.id) |
                Q(employer__isnull=False)
            )
            recommend_vacations_pk = []
            for user in similar_user:
                favorite_vacations_pk = user.favourite_set.all().values_list("vacation__pk", flat=True)
                recommend_vacations_pk += favorite_vacations_pk
            recommend_vacations_pk = list(set(recommend_vacations_pk))
            vacations = Vacation.objects.annotate(
                is_favourite=Exists(
                    Favourite.objects.filter(
                        vacation_id=OuterRef('id'),
                        user=request.user if request.user.is_authenticated else None
                    )
                ),
                is_recommend=Case(
                    When(id__in=recommend_vacations_pk, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField()
                )
            ).all().order_by('-is_recommend', '-id')
        else:
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
        cities = City.objects.all()
        return render(request, 'hrlog.html', context={
            'cities': cities
        })

    def post(self, request):
        try:
            with transaction.atomic():
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
                    city_id=request.POST['city']
                )
        except Exception as error:
            return redirect('regstud')
        else:
            return redirect('login')


class StudentRegisterView(View):
    def get(self, request):
        institutes = Institute.objects.all()
        cities = City.objects.all()
        return render(request, 'regstud.html', context={
            'institutes': institutes,
            'cities': cities
        })

    def post(self, request):
        try:
            with transaction.atomic():
                student_info = Student.objects.create(
                    institute_id=request.POST['institute'],
                    study_group=request.POST['study_group'],
                    university=request.POST['university'],
                    faculty=request.POST['faculty']
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
                    city_id=request.POST['city']
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
        employers = Employer.objects.all()
        if request.GET.get('search'):
            employers = employers.filter(organization__icontains=request.GET['search'])
        return render(request, 'employerlist.html', context={
            'employers': employers
        })


class ReplyDeleteView(View):

    def get(self, request, id):
        Reply.objects.filter(id=id).delete()
        return redirect("employerprofile", request.user.id)


class StudentProfileView(View):
    def get(self, request, user_id):
        user = User.objects.filter(id=user_id)
        if not user.exists():
            redirect("home")
        favourite_vacations = Favourite.objects.filter(user=request.user).values_list('vacation__id', flat=True)
        vacations = Vacation.objects.filter(id__in=favourite_vacations)
        return render(request, 'studprofile.html', context={
            "vacations": vacations,
            "user": user.first()
        })


def logout_user(request):
    logout(request)
    return redirect('home')


class EmployerProfileView(View):
    def get(self, request, employer_id):
        user = User.objects.filter(id=employer_id)
        if not user.exists():
            return redirect("home")
        vacations = Vacation.objects.filter(employer=user.first())
        reply_list = Reply.objects.filter(vacation__employer=user.first())
        return render(request, 'employerprofile.html', context={
            "reply_list": reply_list,
            "vacations": vacations,
            "user": user.first()
        })


class AboutVacancyView(View):
    def get(self, request, vacation_id):
        vacation = Vacation.objects.annotate(
            is_favourite=Exists(
                Favourite.objects.filter(
                    vacation_id=OuterRef('id'),
                    user=request.user if request.user.is_authenticated else None
                )
            ),
            reply_exists=Exists(
                Reply.objects.filter(
                    vacation_id=OuterRef('id'),
                    student=request.user if request.user.is_authenticated else None
                )
            )
        ).get(id=vacation_id)
        return render(request, 'aboutvacancy.html', context={
            "vacation": vacation
        })


class VacationCreateView(View):

    def post(self, request):
        busyness = None
        if request.POST['busyness'] == "Полная занятось":
            busyness = "FULL"
        if request.POST['busyness'] == "Гибкий график":
            busyness = "FLEXIBLE"
        if request.POST['busyness'] == "Сменный график":
            busyness = "SHIFT_WORK"
        Vacation.objects.create(
            position=request.POST['position'],
            description=request.POST['description'].strip(),
            image=request.FILES['image'],
            city_id=request.POST['city'],
            institute_id=request.POST['institute'],
            employer=request.user,
            busyness=busyness,
            address=request.POST['address']
        )
        return redirect("employerprofile", request.user.id)


class VacationUpdateView(View):

    def get(self, request, vacation_id):
        vacation = Vacation.objects.get(id=vacation_id)
        cities = City.objects.all()
        institutes = Institute.objects.all()
        busyness = [Vacation.BUSYNESS_CHOICE[0][-1], Vacation.BUSYNESS_CHOICE[1][-1], Vacation.BUSYNESS_CHOICE[2][-1]]
        return render(request, 'createvacancy.html', context={
            "vacation": vacation,
            "cities": cities,
            "institutes": institutes,
            "busyness": busyness
        })

    def post(self, request, vacation_id):
        vacation = Vacation.objects.get(id=vacation_id)
        vacation.position = request.POST['position']
        vacation.description = request.POST['description'].strip()
        vacation.city_id = request.POST['city']
        if request.FILES.get('image'):
            vacation.image = request.FILES['image']
        vacation.institute_id = request.POST['institute']
        busyness = None
        if request.POST['busyness'] == "Полная занятось":
            busyness = "FULL"
        if request.POST['busyness'] == "Гибкий график":
            busyness = "FLEXIBLE"
        if request.POST['busyness'] == "Сменный график":
            busyness = "SHIFT_WORK"
        vacation.busyness = busyness
        vacation.address = request.POST['address']
        vacation.save()
        return redirect("employerprofile", request.user.id)


class VacationDeleteView(View):

    def get(self, request, vacation_id):
        Vacation.objects.filter(id=vacation_id).delete()
        return redirect("employerprofile", request.user.id)


class CreateVacancyView(View):
    def get(self, request):
        cities = City.objects.all()
        institutes = Institute.objects.all()
        busyness = [Vacation.BUSYNESS_CHOICE[0][-1], Vacation.BUSYNESS_CHOICE[1][-1], Vacation.BUSYNESS_CHOICE[2][-1]]
        return render(request, 'createvacancy.html', context={
            "cities": cities,
            "institutes": institutes,
            "busyness": busyness
        })


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


class VacationReplyView(View):

    def get(self, request, vacation_id):
        vacation = Vacation.objects.get(id=vacation_id)
        reply = Reply.objects.filter(
            student=request.user,
            vacation=vacation
        )
        if not reply.exists():
            Reply.objects.create(
                student=request.user,
                vacation=vacation
            )
        return redirect('aboutvacancy', vacation.id)


class ProfileUpdateView(View):

    def post(self, request, profile_id):
        user = User.objects.get(id=profile_id)
        if user == request.user:
            if request.FILES.get("image"):
                user.image = request.FILES["image"]
            if request.FILES.get("resume"):
                user.student.resume = request.FILES["resume"]
            if request.FILES.get("letter"):
                user.student.letter = request.FILES["letter"]
            if request.POST.get("telegram"):
                tg = request.POST["telegram"].split("@")[-1]
                if tg:
                    user.student.telegram = tg
            user.save()
        if user.student:
            user.student.save()
            return redirect("studprofile", user.id)
        else:
            return redirect("employerprofile", user.id)
