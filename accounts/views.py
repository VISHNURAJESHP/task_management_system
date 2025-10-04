from django.shortcuts import render, redirect
import datetime
import jwt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from .models import User
from .serializers import UserCreateSerializer
from accounts.utils import get_token_from_request
from tasks.models import Task

class UserViewSet(ViewSet):

    # Create user (Super Admin only)
    def create(self, request):
        current_user = get_token_from_request(request)
        if not current_user or current_user.role != "Super Admin":
            return render(request, "admin_panel/unauthorized.html")

        role = "Admin" if "admins" in request.path else "User"

        if request.method == "POST":
            data = request.POST.copy()
            data["role"] = role  # Automatically assign role
            serializer = UserCreateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                # Redirect to correct list page
                return redirect("admins_html" if role == "Admin" else "users_html")
            # Re-render form with errors
            return render(
                request,
                f"admin_panel/{'admins' if role == 'Admin' else 'users'}.html",
                {"errors": serializer.errors, "user": current_user}
            )

        # For GET: just show the correct form page
        return render(
            request,
            f"admin_panel/{'admins' if role == 'Admin' else 'users'}.html",
            {"user": current_user}
        )

    # Delete user (Super Admin only)
    def destroy(self, request, pk=None):
        current_user = get_token_from_request(request)
        if not current_user or current_user.role != "Super Admin":
            return render(request, "admin_panel/unauthorized.html")

        try:
            user = User.objects.get(id=pk)
            role = user.role
            user.delete()
            return redirect("admins_html" if role == "Admin" else "users_html")
        except User.DoesNotExist:
            return redirect("users_html")  # fallback GET redirect

    # List all users (Super Admin only)
    def list_users(self, request):
        current_user = get_token_from_request(request)
        if not current_user or current_user.role != "Super Admin":
            return render(request, "admin_panel/unauthorized.html")

        users = User.objects.filter(role="User")
        return render(request, "admin_panel/users.html", {"users": users, "user": current_user})

    # List all admins (Super Admin only)
    def list_admins(self, request):
        current_user = get_token_from_request(request)
        if not current_user or current_user.role != "Super Admin":
            return render(request, "admin_panel/unauthorized.html")

        admins = User.objects.filter(role="Admin")
        return render(request, "admin_panel/admins.html", {"admins": admins, "user": current_user})

    # Assign user to admin (Super Admin only)
    def assign_user_to_admin(self, request):
        current_user = get_token_from_request(request)
        if not current_user or current_user.role != "Super Admin":
            return render(request, "admin_panel/unauthorized.html")

        users = User.objects.filter(role="User")
        admins = User.objects.filter(role="Admin")

        if request.method == "POST":
            user_id = request.POST.get("user_id")
            admin_id = request.POST.get("admin_id")
            try:
                user = User.objects.get(id=user_id, role="User")
            except User.DoesNotExist:
                return render(request, "admin_panel/assign_user.html", {"error": "User not found", "users": users, "admins": admins, "user": current_user})

            try:
                admin = User.objects.get(id=admin_id, role="Admin")
            except User.DoesNotExist:
                return render(request, "admin_panel/assign_user.html", {"error": "Admin not found", "users": users, "admins": admins, "user": current_user})

            user.assigned_admin = admin
            user.save()
            return redirect("users_html")

        return render(request, "admin_panel/assign_user.html", {"users": users, "admins": admins, "user": current_user})


class LoginView(APIView):

    def get(self, request):
        user = get_token_from_request(request)
        if user.role == "User":
            redirect("admin_panel/user_dashboard_html")
        else:
            redirect("admin_panel/dashboard_html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username=username).first()
        if not user:
            return render(request, "admin_panel/login.html", {"error": "User not found!"})
        if not user.check_password(password):
            return render(request, "admin_panel/login.html", {"error": "Incorrect password!"})

        payload = {
            "id": user.id,
            "username": user.username,
            "role": user.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
            "iat": datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
        token = token if isinstance(token, str) else token.decode("utf-8")  # decode if bytes

        response = redirect("dashboard_html")
        response.set_cookie(key="jwt", value=token, httponly=True)  # add secure=True if HTTPS
        return response


def logout_view(request):
    response = redirect("login_html")
    response.delete_cookie("jwt")
    return response


def dashboard_view(request):
    user = get_token_from_request(request)

    if not user:
        return redirect("login_html")

    context = {"user": user}

    if user.role == "Super Admin":
        context.update({
            "users_count": User.objects.filter(role="User").count(),
            "admins_count": User.objects.filter(role="Admin").count(),
            "tasks_count": Task.objects.all().count()
        })
        return render(request, "admin_panel/dashboard.html", context)

    elif user.role == "Admin":
        context.update({
            "users_count": User.objects.filter(assigned_admin=user).count(),
            "tasks_count": Task.objects.filter(assigned_to__assigned_admin=user).count()
        })
        return render(request, "admin_panel/dashboard.html", context)

    else:  # Regular user
        tasks = Task.objects.filter(assigned_to=user)
        context.update({"tasks": tasks})
        return render(request, "admin_panel/user_dashboard.html", context)