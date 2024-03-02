from django.db import models


class Favourite(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, verbose_name="Пользователь")
    vacation = models.ForeignKey("Vacation", on_delete=models.CASCADE, verbose_name="Вакансия")


    def __str__(self):
        return f"{self.user.fisrt_name} {self.vacation.position}"

    class Meta:
        db_table = "favourites"
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
