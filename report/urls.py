from django.urls import path
from .import views
from report.managements.views import  *

urlpatterns = [
    # path('page/',views.report_page,name='report_page'),
    path('',views.report,name='report'),
    path('<int:pk>/update',views.update_report,name='update_report'),
    path('<int:pk>/delete',views.delete_report,name='delete_report'),
    path('data/chart/',views.data_chart,name='data_chart'),

    # Admin 
    path('admin/',admin,name='superadmin'),
    path('admin/data/',data_analysis,name='data_analysis'),
    path('report_feedback_message_replied/',report_feedback_message_replied,name='report_feedback_message_replied'),
    
]