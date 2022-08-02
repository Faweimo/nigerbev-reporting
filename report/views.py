from django.http import HttpResponse
from django.shortcuts import redirect, render
from pytz import country_names
from accounts.models import User
from .models import Report, TypeOfIncident
from .forms import ReportForm, UpdateReportForm
from django.contrib.auth.decorators import login_required
from django.contrib import  messages
from django.views.decorators.csrf import csrf_exempt

#Plotly Graph chart
# from plotly.offline import plot
# import pandas as pd
# import plotly.express as px

# User to make report of any accident or incidents
@login_required
def report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST,request.FILES)
        if form.is_valid():
            descriptions = form.cleaned_data['descriptions']
            photo = form.cleaned_data['photo']
            date_of_incident = form.cleaned_data['date_of_incident']
            type_of_incident = form.cleaned_data['type_of_incident']
            user = User.objects.get(id=request.user.id)
            report = Report.objects.create(user=user,type_of_incident=type_of_incident,descriptions=descriptions,photo=photo,date_of_incident=date_of_incident)
            
            report.save()

            print('form save')
            messages.success(request,'Report sent successfully')
            return redirect('dashboard')
        print('form invalid')
        messages.error(request, 'Failed to send Report')    
    else:
        form = ReportForm()        
    context = {
        'form':form
    }        
    return render(request,'report/report.html',context)


# update individul report 
def update_report(request,pk):
    if not request.user:
        return HttpResponse('Log in to access the page')
    else:    
        report = Report.objects.get(id=pk)
        if request.method == 'POST':
            form = UpdateReportForm(request.POST,request.FILES,instance=report)

            if form.is_valid():
                form.save()
                print('Success')
                messages.success(request,'Report updated successfully')
                return redirect('dashboard')
            else:
                print('Failed')  
                messages.error(request,'Fail to update report')  
                return redirect('dashboard')
        else:
            form = UpdateReportForm(instance=report)
        context = {
            'form':form,
            'report':report,
        }        
        return render(request, 'report/update.html',context)


#Delete individual report
@login_required(login_url='login')    
def delete_report(request,pk):
    if not request.user:
        return HttpResponse('Log in to access this page')
    else:    
        report = Report.objects.get(id=pk)
        if request.method == 'POST':
            report.delete()
            print('Success')
            messages.success(request, 'Report deleted successfully')
            return redirect('dashboard')
        else:
            print('Failed')  
            # return redirect('delete_report')  
        context = {
            'report':report
        }
    return render(request,'report/delete.html',context)    


# Data Analysis 
def data_chart(request):
    if not request.user:
        return HttpResponse('Log in to access page')
    else:
        count = Report.objects.filter(user=request.user).count()
        counts = Report.objects.filter(user=request.user)
       
            
        done_report = Report.objects.filter(user=request.user,status=1).count()
        in_process_report = Report.objects.filter(user=request.user,status=0).count()
        ignore_report = Report.objects.filter(user=request.user,status=2).count()
        report_data = [
            {
                'Total Report':count,
                'Total Done Report':done_report,
                'Total Ignore Report':ignore_report
            }

        ]  
        # df = pd.DataFrame(report_data)

        # fig = px.histogram(df,x = ['Total Done Report','Total Ignore Report'],y='Total Report',title="Report Data Analysis", barmode='group', height=600)

        # gantt_plot = plot(fig, output_type='div')     
        context = {
            # 'graph':gantt_plot,
            'count':count,
            'done_report':done_report,
            'in_process_report':in_process_report,
            'ignore_report':ignore_report
        }
    return render(request, 'report/data_analysis.html',context)