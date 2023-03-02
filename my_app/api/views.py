from rest_framework import generics
from django.http import JsonResponse
from .services import get_all_tasks, get_task_by_id
from .serializers import TaskSerializer


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = get_all_tasks(user)

        return queryset


class CreateTaskView(generics.CreateAPIView):
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CertainTaskListView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        user = self.request.user
        queryset = get_task_by_id(user=user, id=pk)
        return queryset


class MarkCompletedView(generics.UpdateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        user = self.request.user
        queryset = get_task_by_id(user=user, id=pk)
        return queryset

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        mark_completed = {"is_completed": True}
        serializer = self.get_serializer(instance, data=mark_completed, partial=True)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "success", "details": serializer.errors})
        else:
            return JsonResponse({"message": "failed", "details": serializer.errors})


class DeleteTaskView(generics.DestroyAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        user = self.request.user
        queryset = get_task_by_id(user=user, id=pk)
        return queryset

    def delete(self, request, *args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return JsonResponse({"message": "success", "status_code": 204})
