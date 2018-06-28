from django.conf.urls import url
from . import views

urlpatterns = [
#    url(r'^create-employee', views.create),
#    url(r'^save-employee', views.save),
#    url(r'^edit-employee/(?P<employee_id>\d+)', views.edit),
#    url(r'^update-employee', views.update),
    url(r'^remove-employee/(?P<pk>\d+$)', views.remove_emp,name='remove_emp'),
    url(r'^list-employees$', views.list_emp,name='list_emp'),
    url(r'^createemp$',views.create_emp,name='create_emp'),
    url(r'^editemp/(?P<pk>\d+)/$', views.update_emp, name='edit_emp'),
]
