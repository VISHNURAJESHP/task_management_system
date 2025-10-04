"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
    """
from django.contrib import admin
from django.urls import path, include
from accounts.views import UserViewSet, LoginView, dashboard_view, logout_view
from tasks.views import TaskViewSet, user_dashboard_view

# ------------------- User Views -------------------
user_list = UserViewSet.as_view({"get": "list_users"})
admin_list = UserViewSet.as_view({"get": "list_admins"})

create_user = UserViewSet.as_view({"get": "create", "post": "create"})
delete_user = UserViewSet.as_view({"get": "destroy", "post": "destroy"})

create_admin = UserViewSet.as_view({"get": "create", "post": "create"})
delete_admin = UserViewSet.as_view({"get": "destroy", "post": "destroy"})

assign_user = UserViewSet.as_view({"get": "assign_user_to_admin", "post": "assign_user_to_admin"})

# ------------------- Task Views -------------------
task_list = TaskViewSet.as_view({"get": "list"})
task_create = TaskViewSet.as_view({"get": "create", "post": "create"})
task_update = TaskViewSet.as_view({"get": "update", "post": "update"})
task_report = TaskViewSet.as_view({"get": "report"})

# ------------------- URL Patterns -------------------
urlpatterns = [
    path("admin/", admin.site.urls),

    # ---------- Auth + Dashboards ----------
    path("", dashboard_view, name="dashboard_html"),                  # Admin / Super Admin dashboard
    path("user/dashboard/", user_dashboard_view, name="user_dashboard_html"),  # User dashboard
    path("login/", LoginView.as_view(), name="login_html"),
    path("logout/", logout_view, name="logout_html"),

    # ---------- User Management (SuperAdmin) ----------
    path("users/", user_list, name="users_html"),
    path("users/create/", create_user, name="create_user_html"),
    path("users/<int:pk>/delete/", delete_user, name="delete_user_html"),
    path("users/assign/", assign_user, name="assign_user_html"),

    # ---------- Admin Management (SuperAdmin) ----------
    path("admins/", admin_list, name="admins_html"),
    path("admins/create/", create_admin, name="create_admin_html"),
    path("admins/<int:pk>/delete/", delete_admin, name="delete_admin_html"),

    # ---------- Task Management ----------
    path("tasks/", task_list, name="tasks_html"),
    path("tasks/create/", task_create, name="create_task_html"),
    path("tasks/<int:pk>/update/", task_update, name="update_task_html"),
    path("tasks/<int:pk>/report/", task_report, name="task_report_html"),

    # ---------- API Endpoints ----------
    path("api/accounts/", include("accounts.urls")),
    path("api/tasks/", include("tasks.urls")),
]