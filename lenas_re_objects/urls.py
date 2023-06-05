"""lenas_re_objects URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from reg_auth import views as reg_auth_views
from re_objects import views as re_objects_views

urlpatterns = [
    #path('admin/', admin.site.urls),

    path('reg', reg_auth_views.reg_htm),
    path('reg_process', reg_auth_views.reg_process),
    path('ajax_1', reg_auth_views.reg_process_check_email_username, name="aj_user_reg_process"),
    path('ajax_2', reg_auth_views.send_email_activation_hash, name="aj_send_email_activation_code"),
    path('reg_email_confirm', reg_auth_views.reg_email_confirm_process),


    path('auth', reg_auth_views.auth_htm),
    path('auth_process', reg_auth_views.auth_process),

    path('change_pass', reg_auth_views.change_pass_send_email_htm),
    path('change_pass_send_email', reg_auth_views.change_pass_send_email),
    path('change_pass_process_htm', reg_auth_views.change_pass_process_htm),

    path('change_pass_process', reg_auth_views.change_pass_process),



    path('logout', reg_auth_views.logout_process),



    path('', re_objects_views.list_re_objects),
    path('re_objects_list', re_objects_views.list_re_objects),

]
