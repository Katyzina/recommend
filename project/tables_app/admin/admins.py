from django.contrib import admin


from tables_app.models.user import User
from tables_app.models.city import City
from tables_app.models.employer import Employer
from tables_app.models.favourite import Favourite
from tables_app.models.institute import Institute
from tables_app.models.support import Support
from tables_app.models.student import Student
from tables_app.models.vacation import Vacation

admin.site.register(User)
admin.site.register(City)
admin.site.register(Employer)
admin.site.register(Favourite)
admin.site.register(Institute)
admin.site.register(Support)
admin.site.register(Student)
admin.site.register(Vacation)
