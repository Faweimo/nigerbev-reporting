from django.db import models
from accounts.models import User
from feedback.models import Feedback


class TypeOfIncident(models.Model):
    name = models.CharField(max_length=250)
    def __str__(self):
        return self.name

    class Meta:
        
        verbose_name = 'Type Of  Incident'
        verbose_name_plural = 'Type Of Incidents'

class Report(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    type_of_incident = models.ForeignKey(TypeOfIncident,on_delete=models.CASCADE)
    descriptions = models.TextField()
    status = models.IntegerField(default=0)
    photo = models.FileField(upload_to='photo/incident')
    feedback_reply = models.TextField(blank=True) 
    date_reported = models.DateTimeField(auto_now_add=True)
    date_of_incident = models.DateTimeField()
    
    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = 'report'
        verbose_name_plural = 'reports'