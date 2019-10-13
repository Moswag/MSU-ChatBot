"""comedy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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



from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login),
    path('signin', views.signin),
    path('logout', views.logout_view),
    path('chat', views.home),
    path('dashboard', views.dashboard),
    path('add_student', views.addStudent),
    path('save_student', views.saveStudent, name='saveStudent'),
    path('view_students', views.viewStudents),

    path('add_program', views.addProgram),
    path('view_programs', views.viewPrograms),
    path('save_program', views.saveProgram),
    path('edit_program/<int:program_id>/', views.editProgram, name='edit_program'),
    path('delete_program/<int:program_id>/', views.editProgram, name='delete_program'),

    path('add_module', views.addModule),
    path('save_module', views.saveModule, name='saveModule'),
    path('view_modules', views.viewModules, name='viewModules'),

    path('add_lecturer', views.addLecturer),
    path('save_lecturer', views.saveLecturer, name='saveLecturer'),
    path('view_lecturers', views.viewLecturers, name='viewLecturers'),


    path('add_admin', views.addAdmin),
    path('save_admin', views.saveAdmin, name='saveAdmin'),
    path('view_admins', views.viewAdmins, name='viewAdmins'),

    path('get-response/', views.get_response),

]

if settings.DEBUG == True:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)