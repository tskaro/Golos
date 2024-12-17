from django.contrib import admin

from tasker.models import Profile, Task, Habit, CompletedHabit

# Register your models here.
admin.site.register(Profile)
admin.site.register(Task)
admin.site.register(Habit)
admin.site.register(CompletedHabit)
