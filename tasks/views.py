from rest_framework import viewsets
from django.shortcuts import render, redirect
from .models import Task
from .serializers import TaskCreateSerializer
from accounts.utils import get_token_from_request

class TaskViewSet(viewsets.ViewSet):

    def list(self, request):
        current_user = get_token_from_request(request)
        if not current_user:
            return render(request, "admin_panel/unauthorized.html")

        if current_user.role == "Super Admin":
            tasks = Task.objects.all()
        elif current_user.role == "Admin":
            tasks = Task.objects.filter(assigned_to__assigned_admin=current_user)
        else:  # User
            tasks = Task.objects.filter(assigned_to=current_user)

        return render(request, "admin_panel/tasks.html", {"tasks": tasks, "user": current_user})


    def create(self, request):
        current_user = get_token_from_request(request)
        if not current_user or current_user.role != "Admin":
            return render(request, "admin_panel/unauthorized.html")

        if request.method == "POST":
            serializer = TaskCreateSerializer(data=request.POST)
            if serializer.is_valid():
                user = serializer.validated_data["assigned_to"]
                if user.assigned_admin != current_user:
                    return render(
                        request,
                        "admin_panel/unauthorized.html",
                        {"error": "You can only assign tasks to your own users"},
                    )
                serializer.save()
                return redirect("tasks_html")
            return render(request, "admin_panel/task_form.html", {"errors": serializer.errors})

        return render(request, "admin_panel/task_form.html")


    def update(self, request, pk=None):
        current_user = get_token_from_request(request)
        if not current_user:
            return render(request, "admin_panel/unauthorized.html")

        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return render(request, "admin_panel/task_report.html", {"error": "Task not found"})

        # USER updating their own task
        if current_user.role == "User":
            if task.assigned_to != current_user:
                return render(request, "admin_panel/unauthorized.html")

            if request.method == "POST":
                status_val = request.POST.get("status")

                if status_val == "Completed":
                    completion_report = request.POST.get("completion_report")
                    worked_hours_str = request.POST.get("worked_hours")

                    # Validation
                    try:
                        worked_hours = float(worked_hours_str)
                    except (TypeError, ValueError):
                        return render(
                            request,
                            "admin_panel/task_form.html",
                            {"task": task, "error": "Worked hours must be a valid number"},
                        )

                    if not completion_report:
                        return render(
                            request,
                            "admin_panel/task_form.html",
                            {"task": task, "error": "Completion report is required"},
                        )
                    if worked_hours <= 0:
                        return render(
                            request,
                            "admin_panel/task_form.html",
                            {"task": task, "error": "Worked hours must be greater than 0"},
                        )

                    # Save updates
                    task.status = "Completed"
                    task.completion_report = completion_report
                    task.worked_hours = worked_hours
                    task.save()
                else:
                    task.status = status_val
                    task.save()

                # Redirect to user dashboard
                return redirect("user_dashboard_html")

            return render(request, "admin_panel/task_form.html", {"task": task})

        # ADMIN / SUPER ADMIN can update any task
        elif current_user.role in ["Admin", "Super Admin"]:
            if request.method == "POST":
                task.status = request.POST.get("status", task.status)
                task.save()
                return redirect("tasks_html")

            return render(request, "admin_panel/task_form.html", {"task": task})

        return render(request, "admin_panel/unauthorized.html")


    def report(self, request, pk=None):
        current_user = get_token_from_request(request)
        if not current_user:
            return render(request, "admin_panel/unauthorized.html")

        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return render(request, "admin_panel/task_report.html", {"error": "Task not found"})

        if task.status != "Completed":
            return render(request, "admin_panel/task_report.html", {"task": task, "error": "Task not completed yet"})

        # Super Admin can view all reports
        if current_user.role == "Super Admin":
            return render(request, "admin_panel/task_report.html", {"task": task})

        # Admin can view reports for their assigned users
        if current_user.role == "Admin" and task.assigned_to.assigned_admin == current_user:
            return render(request, "admin_panel/task_report.html", {"task": task})

        return render(request, "admin_panel/unauthorized.html")


def user_dashboard_view(request):
    current_user = get_token_from_request(request)
    if not current_user or current_user.role != "User":
        return render(request, "admin_panel/unauthorized.html")

    tasks = Task.objects.filter(assigned_to=current_user)
    return render(request, "admin_panel/user_dashboard.html", {"tasks": tasks, "user": current_user})
