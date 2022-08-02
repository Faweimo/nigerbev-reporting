from django.contrib import admin
from .models import Report,TypeOfIncident
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin

class SummerAdmin(SummernoteModelAdmin):
    summernote_fields = ('descriptions',)

# Report admin
class ReportAdmin(admin.ModelAdmin):

    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="boader-radius:50%;">'.format(object.photo.url))
    thumbnail.short_description = 'Report photo'
    list_display = ('user','status','date_reported','date_of_incident')
  

# Report admin tabular line
# class ReportAdminInline(admin.TabularInline):
#     model = Report
#     readonly_fields  = ('user','status','date_reported','date_of_incident')
#     extra = 0


admin.site.register(Report,SummerAdmin)
admin.site.register(TypeOfIncident)