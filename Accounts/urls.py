from django.urls import path, include
from .views import CreateUserView, UpdateUserView, DeleteUserView, LoginUserView, LogoutUserView, ProfileUserView, Check_git_hub

urlpatterns = [
    path('profile/<int:pk>', ProfileUserView.as_view(), name='Accounts-profile'),
    path('register/', CreateUserView.as_view(), name='Accounts-register'),
    path('login/', LoginUserView.as_view(), name='Accounts-login'),
    path('logout/', LogoutUserView.as_view(), name='Accounts-logout'),
    path('edit/', UpdateUserView.as_view(), name='Accounts-edit'),
    path('delete/', DeleteUserView.as_view(), name='Accounts-delete'),
    path("gitrepos/", Check_git_hub, name="github-repos"),

    path('', include('django.contrib.auth.urls')),
]   