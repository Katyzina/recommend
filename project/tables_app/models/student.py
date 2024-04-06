from django.db import models


class Student(models.Model):
    university = models.CharField(max_length=50, verbose_name="Университет")
    faculty = models.CharField(max_length=50, verbose_name="Факультет")
    study_group = models.CharField(max_length=50, verbose_name="Учебная группа")
    resume = models.FileField(upload_to="users/students", verbose_name="Резюме")
    letter = models.FileField(upload_to="users/students", verbose_name="Сопроводительное письмо")
    # связь с институтом
    institute = models.ForeignKey("Institute", on_delete=models.SET_NULL, null=True, verbose_name="Институт")
    telegram = models.CharField(max_length=50, verbose_name="Телеграмм")

    def __str__(self):
        return f"{self.university} {self.faculty} {self.study_group}"

    class Meta:
        db_table = "students"
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
