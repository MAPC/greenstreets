from django.forms import ModelForm, TextInput

from survey.models import School, Studentsurvey, Child, Schooldistrict, Employer, Street, Commutersurvey, Walkrideday, Sponsor
# from django.contrib import admin
from django.contrib.gis import admin

class DistrictAdmin(admin.OSMGeoAdmin):
    prepopulated_fields = {'slug': ('distname',)}

class SchoolAdmin(admin.OSMGeoAdmin):
    fieldsets = [
        (None, 
            {'fields': ['name', 'slug', 'survey_active', 'districtid', 'survey_incentive']}),
        ('School Database Attributes', 
            {'fields': ['schid', 'address', 'town', 'state', 'zip', 'principal', 'phone', 'fax', 'grades', 'schl_type']}),
        ('Map',
            {'fields': ['geometry', ]}),
    ]    
    list_filter = ['survey_active']
    list_display = ('name', 'survey_count', 'town', 'grades', 'principal','phone',)
    search_fields = ['name', 'districtid__distname']
    ordering = ['districtid__distname']
    prepopulated_fields = {'slug': ('name',)}
    
    def survey_count(self, obj):
        return obj.survey_set.count()


class CommutersurveyAdminForm(ModelForm):
  class Meta:
    model = Commutersurvey
    widgets = {
        'employer': TextInput(),
    }

class CommutersurveyAdmin(admin.OSMGeoAdmin):
    form = CommutersurveyAdminForm


class SponsorAdminForm(ModelForm):
    class Meta:
        model = Sponsor
        widgets = {
            'employer': TextInput(),
        }

class SponsorAdmin(admin.ModelAdmin):
    form = CommutersurveyAdminForm
    
class StudentsurveyAdmin(admin.OSMGeoAdmin):
    list_display = ('pk','school')
    search_fields = ['school__name']

class ChildAdmin(admin.ModelAdmin):
    list_display = ('pk','survey')

admin.site.register(Schooldistrict, DistrictAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Studentsurvey, StudentsurveyAdmin)
admin.site.register(Child, ChildAdmin)
admin.site.register(Employer, admin.OSMGeoAdmin)
admin.site.register(Street, admin.OSMGeoAdmin)
admin.site.register(Commutersurvey, CommutersurveyAdmin)
admin.site.register(Walkrideday, admin.ModelAdmin)
admin.site.register(Sponsor, SponsorAdmin)