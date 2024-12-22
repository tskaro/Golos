from itertools import groupby
from operator import attrgetter

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.generic.base import View
from tasker.models import Task, Category, Habit, CompletedHabit


def logout_user(request):
    logout(request)
    return redirect('login')


class TaskView(LoginRequiredMixin, View):
    def get(self, request):
        tasks = Task.objects.filter(user=request.user, archived=False).order_by('category__name')
        grouped_tasks = {k: list(v) for k, v in groupby(tasks, key=attrgetter('category.name'))}
        return render(request, 'tasker/tasks.html', {"grouped_tasks": grouped_tasks})


class ChangeStatusView(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)

        task.status = not task.status
        task.save()
        return redirect('task_list')


class ArchiveTaskView(LoginRequiredMixin, View):
    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)

        task.archived = True
        task.save()
        return redirect('task_list')


class AddTaskView(LoginRequiredMixin, View):
    def get(self, request):
        categories = Category.objects.filter(user=request.user)
        return render(request, 'tasker/add_task.html', {"categories": categories})

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        time = request.POST.get('time')
        due_date_time = request.POST.get('due_date_time')
        category_id = request.POST.get('category')
        recurring = bool(request.POST.get('recurring'))

        category = Category.objects.get(id=category_id) if category_id else None

        Task.objects.create(
            user=request.user,
            name=name,
            description=description,
            time=time,
            due_date_time=due_date_time,
            category=category,
            recurring=recurring,
        )
        return redirect('task_list')


class EditTaskView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        return render(request, 'tasker/edit_task.html', {"task": task})

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.name = request.POST.get('name')
        task.description = request.POST.get('description')
        task.time = int(request.POST.get('time'))
        task.due_date_time = request.POST.get('due_date_time')
        task.recurring = bool(request.POST.get('recurring'))
        task.save()
        return redirect('task_list')


class AddCategoryView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'tasker/add_category.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        if name:
            Category.objects.create(user=request.user, name=name, description=description)
        return redirect('task_list')


class HabitListView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        habits = Habit.objects.filter(user=request.user)
        for habit in habits:
            total_completions = CompletedHabit.objects.filter(habit=habit).count()
            habit.total_completions = total_completions

            start_of_day = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            has_completed_today = CompletedHabit.objects.filter(
                habit=habit,
                user=request.user,
                created_at_utc__gte=start_of_day
            ).exists()
            habit.has_completed_today = has_completed_today

        return render(request, 'tasker/habits.html', {'habits': habits})


class AddHabitView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        return render(request, 'tasker/add_habit.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        minimal_time = request.POST.get('minimal_time')
        score = request.POST.get('score', 0)

        if name and description:
            Habit.objects.create(
                user=request.user,
                name=name,
                description=description,
                minimal_time=minimal_time,
                score=score
            )
        return redirect('habit_list')  # We'll define habit_list in urls.py


class EditHabitView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, habit_id):
        habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        return render(request, 'tasker/edit_habit.html', {'habit': habit})

    def post(self, request, habit_id):
        habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        habit.name = request.POST.get('name')
        habit.description = request.POST.get('description')
        habit.minimal_time = request.POST.get('minimal_time')
        habit.score = request.POST.get('score', habit.score)
        habit.save()
        return redirect('habit_list')


class CompleteHabitView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, habit_id):
        habit = get_object_or_404(Habit, id=habit_id, user=request.user)
        CompletedHabit.objects.create(
            user=request.user,
            habit=habit,
            created_at_utc=timezone.now()
        )
        habit.score += 1
        habit.save()
        return redirect('habit_list')
