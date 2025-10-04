from django.urls import path
from .views import TaskViewSet

urlpatterns = [
    # List tasks (all roles, role-based inside view)
    path('tasks/list/', TaskViewSet.as_view({'get': 'list'}), name='task-list'),

    # Create task (Admin only)
    path('tasks/create/', TaskViewSet.as_view({'post': 'create'}), name='task-create'),

    # Update task (User/Admin)
    path('tasks/<int:pk>/update/', TaskViewSet.as_view({'put': 'update'}), name='task-update'),

    # Task completion report (Admin/SuperAdmin)
    path('tasks/<int:pk>/report/', TaskViewSet.as_view({'get': 'report'}), name='task-report'),
]
