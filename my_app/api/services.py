from .models import Task
from typing import List


def get_all_tasks(user) -> List[Task]:
    result = Task.objects.filter(user=user)
    return result


def get_task_by_id(user, id: int) -> Task:
    result = Task.objects.filter(user=user, id=id)
    return result
