from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^remove-employee/(?P<pk>\d+$)', views.remove_emp,name='remove_emp'),
    # url(r'^list-employees$', views.list_emp,name='list_emp'),
    # url(r'^createemp$',views.create_emp,name='create_emp'),
    # url(r'^editemp/(?P<pk>\d+)/$', views.update_emp, name='edit_emp'),
    # url(r'^list-employment-details/(?P<emp_id>\d+)/$',views.list_employment,name='list_employment'),
    # url(r'^edit-employment-details/(?P<emp_id>\d+)/$',views.update_employment,name='edit_employment'),
    url(r'^list-leave/(?P<emp_id>\d+)/$',views.display_leave,name='display_leave'),
    url(r'^apply-leave/(?P<emp_id>\d+)/$',views.apply_leave,name='apply_leave'),
    url(r'^add-dependent/(?P<emp_id>\d+)/$',views.add_dependent,name='add_dependent'),
    url(r'^edit-dependent/(?P<emp_id>\d+)/(?P<pk>\d+)/$',views.edit_dependent,name='edit_dependent'),
    url(r'^list-dependent/(?P<emp_id>\d+)/$',views.display_dependent,name='list_dependent'),
    url(r'^leave-details/(?P<pk>\d+)/$',views.display_leavetxn,name='leave_details'),
    url(r'^welcome/(?P<emp_id>\d+)/$',views.welcome,name='welcome'),
    url(r'^display_dependent_detail/(?P<pk>\d+)/$',views.display_dependenttxn,name='display_dependent_detail'),
    url(r'^login$',views.loginuser,name='login'),
]
