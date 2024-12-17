from django.contrib import admin
from django.urls import path, include

from tasker import views
from tasker.views import ChangeStatusView, ArchiveTaskView

urlpatterns = [
    path("logout/", views.logout_user, name='logout'),
    path('', views.TaskView.as_view(), name="task_list"),
    path('change-status/<int:task_id>/', ChangeStatusView.as_view(), name='change_status'),
    path('archive/<int:task_id>/', ArchiveTaskView.as_view(), name='archive_task'),

]