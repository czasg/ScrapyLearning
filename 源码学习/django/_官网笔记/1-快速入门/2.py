__file__ = '2'

"""
python manage.py migrate
python manage.py makemigrations polls

from django.utils import timezone
q = Question(question_text="What's new?", pub_date=timezone.now())  # 使用timezone.now()而不是datetime模块
q.save()

python manage.py createsuperuser
---admin.py文件中
from django.contrib import admin
from .models import Question
admin.site.register(Question)
"""


from django.db import models
class Cza(models.Model):
    name = models.CharField(max_length=200)
    o = models.Manager()


class BookManager(models.Manager):  # 这玩意还得继承自Manager
    def create_book(self, title):
        book = self.create(title=title)
        return book
class Book(models.Model):
    title = models.CharField(max_length=100)
    objects = BookManager()
book = Book.objects.create_book("Pride and Prejudice")