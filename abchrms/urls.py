from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^remove-employee/(?P<pk>\d+$)', views.remove_emp,name='remove_emp'),
    url(r'^list-employees$', views.list_emp,name='list_emp'),
    url(r'^createemp$',views.create_emp,name='create_emp'),
    url(r'^editemp/(?P<pk>\d+)/$', views.update_emp, name='edit_emp'),
    url(r'^list-employment-details$',views.list_employment,name='list_employment'),
    url(r'^edit-employment-details/(?P<emp_id>\d+)/$',views.update_employment,name='edit_employment'),
]
