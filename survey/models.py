from django.contrib.gis.db import models
from django.db.models import permalink

# lazy translation
from django.utils.translation import ugettext_lazy as _

# south introspection rules 
try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.PointField'])
    add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.MultiPolygonField'])
    add_introspection_rules([], ['^django\.contrib\.gis\.db\.models\.fields\.MultiLineStringField'])
except ImportError:
    pass


COMMUTER_MODES = (
        ('c', _('Car')),
        ('w', _('Walk')),
        ('b', _('Bike')),
        ('cp', _('Carpool')),
        ('t', _('Transit (bus, subway, etc.)')),
        ('o', _('Other (skate, canoe, etc.)')),
        ('tc', _('Telecommuting')),
    )

STUDENT_MODES = (
        ('w', _('Walk')),
        ('b', _('Bike')),
        ('sb', _('School Bus')),
        ('fv', _('Family Vehicle (only students of one family)')),
        ('cp', _('Carpool (with students from other families)')),
        ('t', _('Transit (city bus, subway, etc.)')),
        ('o', _('Other (skateboard, scooter, etc.)'))
    )


class Employer(models.Model):
    """ Greens Streets Initiative Employer list """

    name = models.CharField("Employer name", max_length=200)
    nr_employees = models.IntegerField("Number of employees", null=True, blank=True)
    active = models.BooleanField("Show in Commuter-Form", default=False)

    class Meta:
        verbose_name = _('Employer')
        verbose_name_plural = _('Employers')
        ordering = ['name']

    def __unicode__(self):
        return self.name

 
class Commutersurvey(models.Model):
    """
    Questions for adults about their commute work
    and Green Streets interest.
    """

    month = models.CharField('Walk/Ride Day Month', max_length=50)
    
    home_location = models.PointField(geography=True, blank=True, null=True, default='POINT(0 0)') # default SRS 4326
    home_address = models.CharField(max_length=200)
    work_location = models.PointField(geography=True, blank=True, null=True, default='POINT(0 0)')
    work_address = models.CharField(max_length=200)
    
    distance = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)
    duration = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)
    
    to_work_today = models.CharField(max_length=2, blank=True, null=True, choices=COMMUTER_MODES)
    from_work_today = models.CharField(max_length=2, blank=True, null=True, choices=COMMUTER_MODES)  
    to_work_normally = models.CharField(max_length=2, blank=True, null=True, choices=COMMUTER_MODES)
    from_work_normally = models.CharField(max_length=2, blank=True, null=True, choices=COMMUTER_MODES) 

    other_greentravel = models.BooleanField(default=False)
    
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    newsletter = models.BooleanField(default=False)
    employer = models.CharField('Employer', max_length=100, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    
    ip = models.IPAddressField('IP Address', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    objects = models.GeoManager()
    
    def __unicode__(self):
        return u'%s' % (self.id)   
    
    class Meta:
        verbose_name = 'Commuter Survey'
        verbose_name_plural = 'Commuter Surveys'     


class Schooldistrict(models.Model):
    """ School Districts """
    districtid = models.IntegerField(primary_key=True)
    distname = models.CharField(max_length=35)
    slug = models.SlugField(max_length=35, unique=True)
    startgrade = models.CharField(max_length=2)
    endgrade = models.CharField(max_length=2)
    distcode4 = models.CharField(max_length=4)
    distcode8 = models.CharField(max_length=8)
    
    geometry = models.MultiPolygonField(srid=26986)
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.distname
    
    class Meta:
        ordering = ['distname']
    

class School(models.Model):
    """ School """
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, null=True)
    
    schid = models.CharField('School ID', max_length=8, blank=True, null=True, unique=True)
    address = models.CharField(max_length=150, blank=True, null=True)
    town_mail = models.CharField(max_length=25, blank=True, null=True)
    town = models.CharField('School Town', max_length=25, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    zip = models.CharField(max_length=10, blank=True, null=True)
    principal = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    fax = models.CharField(max_length=15, blank=True, null=True)
    grades = models.CharField(max_length=70, blank=True, null=True)
    schl_type = models.CharField(max_length=3, blank=True, null=True)     
    districtid = models.ForeignKey('Schooldistrict', blank=True, null=True)
    
    survey_incentive = models.TextField(blank=True, null=True)
    survey_active = models.BooleanField('Is Survey School')
    
    # GeoDjango
    geometry = models.PointField(srid=26986)
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'School'
        verbose_name_plural = 'Schools' 
        

class Studentsurvey(models.Model):
    """ To checkin entire classrooms or groups of students """

    month = models.CharField('Walk/Ride Day Month', max_length=50)

    school = models.ForeignKey(School, verbose_name='School')

    teacher_name = models.CharField(max_length=50, blank=True, null=True)
    teacher_email = models.EmailField()
    newsletter = models.BooleanField(default=False)

    ip = models.IPAddressField('IP Address', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Studentsurvey')
        verbose_name_plural = _('Studentsurveys')

    def __unicode__(self):
        return "%s (%s)" % (self.teacher_email, self.month)
    

class Studentgroup(models.Model):
    """ Group of students to be checked in """

    teacher = models.ForeignKey(Studentsurvey)

    number = models.IntegerField('Number of students', default=1)
    distance = models.DecimalField('Travel distance', help_text='Average, in miles, e.g. 1.25', max_digits=10, decimal_places=3, blank=True, null=True)

    to_school_today = models.CharField(max_length=2, blank=True, null=True, choices=STUDENT_MODES)
    from_school_today = models.CharField(max_length=2, blank=True, null=True, choices=STUDENT_MODES) 

    to_school_normally = models.CharField(max_length=2, blank=True, null=True, choices=STUDENT_MODES)
    from_school_normally = models.CharField(max_length=2, blank=True, null=True, choices=STUDENT_MODES) 

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Studentgroup')
        verbose_name_plural = _('Studentgroups')

    def __unicode__(self):
        return "%s, %i students" % (self.teacher, self.number)
    
