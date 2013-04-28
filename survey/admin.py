
import csv
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

from django.db.models import Sum, Count

from django.forms import ModelForm

from survey.models import School, Schooldistrict, Commutersurvey, Employer, EmplSector, EmplSizeCategory, Studentsurvey, Studentgroup
# from django.contrib import admin
from django.contrib.gis import admin


# default GeoAdmin overloads
admin.GeoModelAdmin.default_lon = -7915039
admin.GeoModelAdmin.default_lat = 5216500
admin.GeoModelAdmin.default_zoom = 12


def export_as_csv(modeladmin, request, queryset):
    """
    Generic csv export admin action.
    """

    if not request.user.is_staff:
        raise PermissionDenied

    opts = modeladmin.model._meta
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')
    writer = csv.writer(response)
    
    field_names = [field.name for field in opts.fields]
    
    # Write a first row with header information
    writer.writerow(field_names)
    
    # Write data rows
    for obj in queryset:
        try:
            writer.writerow([getattr(obj, field) for field in field_names])
        except UnicodeEncodeError:
            print "Could not export data row."
    return response

export_as_csv.short_description = "Export selected rows as csv file"


class EmployerAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display_links = ['id']
    list_display = ['id', 'name', 'active', 'nr_employees', 'size_cat', 'sector', 'nr_surveys']
    list_editable = ['name', 'active', 'nr_employees', 'size_cat', 'sector', ]
    list_filter = ['size_cat', 'sector', 'active']
    actions = [export_as_csv]


class EmployerLookupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_editable = ['name']
    actions = [export_as_csv]


class CommutersurveyAdmin(admin.OSMGeoAdmin):
    fieldsets = [
        (None, 
            {'fields': ['month', 'name', 'email', 'employer', 'newsletter']}),
        ('Commute', 
            {'fields': ['home_address', 'work_address', 'to_work_today', 'from_work_today', 'to_work_normally', 'from_work_normally']}),
        ('Maps',
            {'fields': ['home_location', 'work_location']}),
        ('Meta',
            {'fields': ['ip']}),
    ]
    list_display = ('month', 'email', 'employer', 'home_address', 'work_address', 'to_work_today', 'from_work_today', 'to_work_normally', 'from_work_normally')
    list_display_links = ['email']
    list_editable = ['employer']
    list_filter = ['month', 'to_work_today', 'from_work_today', 'to_work_normally', 'from_work_normally']
    search_fields = ['name', 'employer']
    actions = [export_as_csv]


class DistrictAdmin(admin.OSMGeoAdmin):
    prepopulated_fields = {'slug': ('distname',)}


class SchoolAdmin(admin.OSMGeoAdmin):
    fieldsets = [
        (None, 
            {'fields': ['name', 'slug', 'survey_active', 'districtid']}),
        ('School Database Attributes', 
            {'fields': ['schid', 'address', 'town', 'state', 'zip', 'principal', 'phone', 'fax', 'grades', 'schl_type']}),
        ('Map',
            {'fields': ['geometry', ]}),
    ]    
    list_filter = ['survey_active']
    list_display = ['name', 'survey_active', 'town', 'grades',]
    list_editable = ['survey_active']
    search_fields = ['name', 'districtid__distname']
    ordering = ['districtid__distname']
    prepopulated_fields = {'slug': ('name',)}
    
    def survey_count(self, obj):
        return obj.survey_set.count()

class StudentsurveyAdmin(admin.ModelAdmin):
    list_display = ('month', 'school', 'teacher_email', 'num_students_sum', 'num_studentgroups_count', 'created')
    list_filter = ['month', 'school__town', 'school']
    list_display_links = ['school']
    search_fields = ['school__name', 'teacher_name']
    actions = [export_as_csv]

    def queryset(self, request):
        qs = super(StudentsurveyAdmin, self).queryset(request)
        return qs.annotate(num_students=Sum('studentgroup__number'), num_studentgroups=Count('studentgroup'))

    def num_students_sum(self, obj):
        return obj.num_students
    num_students_sum.short_description = 'Checked-in Students'
    num_students_sum.admin_order_field = 'num_students_sum'

    def num_studentgroups_count(self, obj):
        return obj.num_studentgroups
    num_studentgroups_count.short_description = 'Studentgroups'
    num_studentgroups_count.admin_order_field = 'num_studentgroups_count'

    
class StudentgroupAdmin(admin.ModelAdmin):
    list_display = ['month', 'teacher', 'number', 'distance', 'to_school_today', 'from_school_today']
    list_display_links = ['teacher']
    list_filter = ['teacher__month', 'teacher__school__town', 'teacher__school']
    actions = [export_as_csv]

    def month(self, obj):
        return obj.teacher.month


admin.site.register(Schooldistrict, DistrictAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Commutersurvey, CommutersurveyAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(EmplSizeCategory, EmployerLookupAdmin)
admin.site.register(EmplSector, EmployerLookupAdmin)
admin.site.register(Studentsurvey, StudentsurveyAdmin)
admin.site.register(Studentgroup, StudentgroupAdmin)