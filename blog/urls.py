from django.urls import path
from . import views


urlpatterns =[
    path('', views.start, name='start'),
    path('active/', views.ApplicationListView.as_view(), name='active-list'),
    path('application/<int:pk>/', views.ApplicationDetailView.as_view(), name='application-detail'),
    path('pending/', views.PermissionListView.as_view(), name='pending-list'),
    path('permission/<int:pk>/', views.PermissionDetailView.as_view(), name='permission-detail'),
    path('application/new/', views.ApplicationCreateView.as_view(), name='application-create'),
    path('reject/<int:pk>/', views.reject, name='reject'),
    path('accept/<int:pk>/', views.accept, name='accept'),
    path('application_history/', views.ApplicationHistoryListView.as_view(), name='application-history'),
    path('permission_history/', views.PermissionHistoryListView.as_view(), name='permission-history'),
]
