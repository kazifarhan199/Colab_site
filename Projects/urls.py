from django.urls import path, include
from .views import Projects_List, Projects_create_view, Projects_Dashboard_List, Projects_detail_view, Projects_Dashboard_Edit

urlpatterns = [
    path('', Projects_List.as_view(), name='Projects-list'),
    path('create/', Projects_create_view.as_view(), name='Projects-create'),
    path('detail/<pk>', Projects_detail_view.as_view(), name='Projects-detail'),
    path('dashboard/', Projects_Dashboard_List.as_view(), name='Projects-dashboard'),
    path('dashboard/edit/<pk>', Projects_Dashboard_Edit.as_view(), name='Projects-edit'),

]   