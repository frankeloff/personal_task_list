from django.urls import path, include, re_path
from .views import (
    TaskListView,
    CreateTaskView,
    CertainTaskListView,
    MarkCompletedView,
    DeleteTaskView,
)

urlpatterns = [
    path("tasks/", TaskListView.as_view(), name="tasks"),
    path("tasks/<int:pk>/", CertainTaskListView.as_view(), name="certain-tasks"),
    path("tasks/delete/<int:pk>/", DeleteTaskView.as_view(), name="delete-task"),
    path("tasks/create/", CreateTaskView.as_view(), name="create-tasks"),
    path(
        "tasks/<int:pk>/mark-completed/",
        MarkCompletedView.as_view(),
        name="mark-completed",
    ),
    path("api/v1/auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
]
