from django.urls import path
from .views import UserViewSet, LoginView

urlpatterns = [
    # Login
    path('login/', LoginView.as_view(), name='login'),

    # List Users (SuperAdmin)
    path('users/list/', UserViewSet.as_view({'get': 'list_users'}), name='list-users'),

    # Create User/Admin (SuperAdmin)
    path('users/create/', UserViewSet.as_view({'post': 'create'}), name='create-user'),

    # Delete User/Admin (SuperAdmin)
    path('users/<int:pk>/delete/', UserViewSet.as_view({'delete': 'destroy'}), name='delete-user'),

    # List Admins (SuperAdmin)
    path('admins/list/', UserViewSet.as_view({'get': 'list_admins'}), name='list-admins'),

    # Assign user to admin
    path('assign-user-admin/', UserViewSet.as_view({'post': 'assign_user_to_admin'}), name='assign-user-admin'),
]
