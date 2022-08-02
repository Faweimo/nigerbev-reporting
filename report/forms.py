from .models import Report
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django import  forms


class ReportForm(forms.ModelForm):
    # date_of_incident = forms.DateField(widget = forms.SelectDateWidget)
    class Meta:
        model = Report
        fields = '__all__'
        exclude = ('user','feedback','status',)
        widgets = {
            'user':forms.TextInput(attrs={
                'type':'hidden',
            }),
            'descriptions':forms.TextInput(attrs={
                'type':'text',
                'class':'form-control',
                'placeholder':'descriptions'
            }),
            'type_of_incident':forms.Select(attrs={
                'type':'select',
                'class':'form-control',
                'placeholder':'type of incident'
            }),
            'photo':forms.FileInput(attrs={
                'type':'file',
                'class':'form-control',
                'placeholder':'photo'
            }),
            'date_of_incident':forms.DateTimeInput(attrs={
                'type':'date',
                'class':'form-control',
                'placeholder':'date of incident'
            }),
            
        }    


class UpdateReportForm(forms.ModelForm):
    class Meta:
        model = Report  
        fields = '__all__'
        exclude = ('feedback','status')
        widgets = {
            'user':forms.TextInput(attrs={
                'type':'hidden',
            }),
        }    

    def __init__(self, *args, **kwargs):
        super(UpdateReportForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'       