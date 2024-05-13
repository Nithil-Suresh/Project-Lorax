"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from project_lorax import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/profile/', views.profile, name="profile"),
    path('accounts/', include('allauth.urls')),
    path("", views.landing_view, name="landing_page"),
    path('upload/', views.upload_file, name='upload_file'),
    path('accounts/profile/admin-view', views.admin_profile, name='admin-view'),
    path('accounts/profile/admin-view/update-status/',
         views.update_status, name='update_status'),
    path('accounts/profile/search/',
         views.search, name='search'),
    path('view-file/<path:file_key>/', views.view_file, name='view-file'),
    path("accounts/profile/admin-view/<int:reported_issue_id>/", views.view_reported_issue,
         name='view-reported-issue'),
    path('logout/', views.logout, name='logout'),
    path('accounts/profile/admin-view/delete-report', views.delete_report, name='delete_report')
]
