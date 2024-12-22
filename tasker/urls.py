from django.urls import path

from tasker import views
from tasker.views import ChangeStatusView, ArchiveTaskView, AddTaskView, EditTaskView, AddCategoryView, HabitListView, \
    AddHabitView, EditHabitView, CompleteHabitView

urlpatterns = [
    path("logout/", views.logout_user, name='logout'),
    path('', views.TaskView.as_view(), name="task_list"),
    path('change-status/<int:task_id>/', ChangeStatusView.as_view(), name='change_status'),
    path('archive/<int:task_id>/', ArchiveTaskView.as_view(), name='archive_task'),
    path('tasks/add/', AddTaskView.as_view(), name='add_task'),
    path('tasks/edit/<int:task_id>/', EditTaskView.as_view(), name='edit_task'),
    path('categories/add/', AddCategoryView.as_view(), name='add_category'),

    path('habits/', HabitListView.as_view(), name='habit_list'),
    path('habits/add/', AddHabitView.as_view(), name='add_habit'),
    path('habits/edit/<int:habit_id>/', EditHabitView.as_view(), name='edit_habit'),
    path('habits/complete/<int:habit_id>/', CompleteHabitView.as_view(), name='complete_habit'),

]
