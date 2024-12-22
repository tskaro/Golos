from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    short_info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.user.username}"


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Categories are user-specific
    name = models.CharField(max_length=100, unique=True)  # Unique name per category
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    time = models.IntegerField()
    creation_date = models.DateTimeField(auto_now_add=True)
    recurring = models.BooleanField(default=False)
    due_date_time = models.DateTimeField()
    status = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.category.name if self.category else 'No Category'})"


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    minimal_time = models.IntegerField()
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class CompletedHabit(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    habit = models.ForeignKey(Habit, on_delete=models.DO_NOTHING)
    created_at_utc = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} {self.habit} {self.created_at_utc}"
