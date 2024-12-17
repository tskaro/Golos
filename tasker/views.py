from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from tasker.models import Task


def logout_user(request):
    logout(request)
    return redirect('login')


class TaskView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        user_id = request.user.id
        tasks = Task.objects.filter(user_id=user_id, archived=False)

        return render(request, 'tasker/tasks.html', {
            "tasks": tasks,
        })


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
