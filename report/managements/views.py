from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.models import *
from ..models import  *
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt

def admin(request):
    if request.user.is_superadmin != True:
        return HttpResponse('This page is for Super Admin')
    else:
        total_report = Report.objects.count()
        total_done_report = Report.objects.filter(status=1).count()
        total_ignore_report = Report.objects.filter(status=2).count()
        reports = Report.objects.all().order_by('-date_reported')

        # page pagination
        paginator = Paginator(reports, 25)
        page = request.GET.get('page')
        paged_reports = paginator.get_page(page)
        context = {
            'reports':paged_reports,
            'total_report':total_report,
            'total_ignore_report':total_ignore_report,
            'total_done_report':total_done_report,
        }
    return render(request,'report/managements/admin.html',context)


# Superadmin Dashboard 
def data_analysis(request):
    if request.user.is_superadmin != True:
        return HttpResponse('This page is for Super Admin')
    else:
        total_report = Report.objects.count()
        total_done_report = Report.objects.filter(status=1).count()
        total_ignore_report = Report.objects.filter(status=2).count()
        reports = Report.objects.all().order_by('-date_reported')

        # page pagination
        paginator = Paginator(reports, 25)
        page = request.GET.get('page')
        paged_feedbacks = paginator.get_page(page)
        context = {
            'reports':paged_feedbacks,
            'total_report':total_report,
            'total_ignore_report':total_ignore_report,
            'total_done_report':total_done_report,
        }
    return render(request,'report/managements/data.html',context)



@csrf_exempt
def report_feedback_message_replied(request):
    if not request.user.is_superadmin == True:
        return HttpResponse('You are not allow to view this page')
    else:

        id = request.POST.get('id')
        feedback_reply = request.POST.get('message')

        try:
            report_feedback = Report.objects.get(id=id)

            report_feedback.feedback_reply = feedback_reply
            report_feedback.save()
            return HttpResponse('True')
        except:
            return HttpResponse('False')    