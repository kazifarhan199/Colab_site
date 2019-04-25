from django.urls import path
from .views import send_projects

urlpatterns = [
    path('<id>/', send_projects),
]