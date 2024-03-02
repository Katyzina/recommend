from django.shortcuts import render
from django.views import View

from tables_app.models import Institute, Vacation


class HomePageView(View):

    def get(self, request):
        # get(id=1) -> obj
        # filter(name=ep) -> [obj]
        # all() -> [obj, obj]
        institutes = Institute.objects.all()
        vacations = Vacation.objects.all()
        return render(request, 'index.html', context={
            "institutes": institutes,
            "vacations": vacations,

        })
