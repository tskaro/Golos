from itertools import groupby
from operator import attrgetter

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from tasker.models import Task, Category


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
