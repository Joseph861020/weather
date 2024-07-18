from django.contrib.auth.models import User
from django.db import models


class CitySearchHistory(models.Model):
    """
    Модель для хранения истории поиска городов пользователем.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    count = models.IntegerField(default=0)
    last_searched = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'city')

    def __str__(self):
        """
        Возвращает строковое представление объекта истории поиска города.
        """
        return f"{self.user.username} searched for {self.city} {self.count} times"
