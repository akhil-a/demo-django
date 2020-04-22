"""webSAS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from task_creator import views as task

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^login/$', auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name="/"), name='logout'),
    # url(r'^$', task.main),
    url(r'^$', task.dashboard),
    url(r'^dashboard/', task.dashboard, name='dashboard'),
    url(r'^create/', task.create_task, name='create_task'),
    url(r'^start-new-task/', task.start_new_task, name='start_new_task'),
    # url(r'^login/(?P<username>\w{0,50})/$', task.login, name='login'),
    url(r'^track/', task.track, name='track'),
    url(r'^track-test/(?P<test_id>\w{0,50})/$', task.track_test_id, name='track_test_id'),
    url(r'^log-viewer/', task.read_log_file, name='log_viewer'),
    url(r'^run-test/', task.run_test, name='run_test'),
    url(r'^get-devices/', task.get_devices, name='get_devices'),
    url(r'^final-run/', task.final_run, name='final_run'),
    path('create-test-suite/', task.create_test_suite, name='create_test_suite'),
    path('show/', task.show, name='show'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)