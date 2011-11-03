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


class Walkrideday(models.Model):
    """ Selected dates when Walk/Ride days happened"""
    date = models.DateField(auto_now=False, auto_now_add=False)
    active = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return str(self.date)


class Town(models.Model):
    """ Towns participating in Walk/Ride Days"""
    town_id = models.IntegerField(primary_key=True)
    slug = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    
    survey_active = models.BooleanField()
    
    geometry = models.MultiPolygonField(srid=26986)
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

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
    town = models.CharField(max_length=25, blank=True, null=True)
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
        
    @permalink
    def get_absolute_url(self):
        return ('survey_school_form', None, { 'school_slug': self.slug, 'district_slug': self.districtid.slug})
  
    
class Employer(models.Model):
    """ Employer list to choose from """
    name = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=30, blank=True, null=True)
    infousa_id = models.CharField(unique=True, max_length=9, blank=True, null=True)
    town = models.ForeignKey('Town', blank=True, null=True)
    
    geometry = models.PointField(srid=26986) # default SRS 4326
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class Sponsor(models.Model):
    """ Walk/Ride day sponsors, likely also an Employer """
    name_alt = models.CharField('Alternative Name', max_length=30, blank=True, null=True)
    employer = models.ForeignKey('Employer')
    
    active = models.BooleanField(default=True)
    walkrideday = models.ManyToManyField('Walkrideday')

    def __unicode__(self):
        return self.employer.name
    
class Street(models.Model):
    """
    Streets to be returned as type-ahead in street-fields
    to limit the variety of street names and make geocoding
    more accurate.
    """
    name = models.CharField(max_length=240)
    
    town = models.ForeignKey('Town', blank=True, null=True)
    schooldistrict = models.ForeignKey('Schooldistrict', blank=True, null=True)
    
    geometry = models.MultiLineStringField(srid=26986)
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.name


COMMUTER_MODES = (
            ('c', _('Car')),
            ('w', _('Walk')),
            ('b', _('Bike')),
            ('cp', _('Carpool')),
            ('t', _('Transit (bus, subway, train, etc.)')),
            ('o', _('Other (skateboard, scooter, inline skates, etc.)'))
            )

 
class Commutersurvey(models.Model):
    """
    Questions for adults about their commute work
    and Green Streets interest.
    """
    
    walkrideday = models.ForeignKey('Walkrideday', blank=True, null=True)
    
    home_location = models.PointField(geography=True, blank=True, null=True, default='POINT(0 0)') # default SRS 4326
    
    employer = models.ForeignKey('Employer', to_field='infousa_id', blank=True, null=True)
    other_employer = models.CharField(max_length=50, blank=True, null=True)
    work_location = models.PointField(geography=True, blank=True, null=True, default='POINT(0 0)')
    
    distance = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)
    duration = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)
    
    to_work_today = models.CharField(max_length=2, blank=True, null=True, choices=COMMUTER_MODES)
    from_work_today = models.CharField(max_length=2, blank=True, null=True, choices=COMMUTER_MODES)  
    to_work_yesterday = models.CharField(max_length=2, blank=True, null=True, choices=COMMUTER_MODES)
    from_work_yesterday = models.CharField(max_length=2, blank=True, null=True, choices=COMMUTER_MODES) 
    
    weight = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    
    sponsor = models.ManyToManyField('Sponsor', limit_choices_to = {'active': True}, blank=True, null=True)
    
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    newsletter = models.BooleanField(default=False)
    coordinator = models.BooleanField(default=False)
    potential_sponsor = models.BooleanField(default=False)
    volunteer = models.BooleanField(default=False)
    feedback = models.TextField(blank=True, null=True)
    
    ip = models.IPAddressField('IP Address', blank=True, null=True)
    
    objects = models.GeoManager()
    
    def __unicode__(self):
        return u'%s' % (self.id)   
    
    class Meta:
        verbose_name = 'Commuter Survey'
        verbose_name_plural = 'Commuter Surveys' 


class Studentsurvey(models.Model):
    """ School Survey """
    
    walkrideday = models.ForeignKey('Walkrideday', blank=True, null=True)
    
    school = models.ForeignKey('School', blank=True, null=True)
    
    home_location = models.PointField(geography=True, blank=True, null=True, default='POINT(0 0)') # default SRS 4326
    home_street = models.CharField(max_length=50, blank=True, null=True)
    home_cross_st = models.CharField('Cross street', max_length=50, blank=True, null=True)
    
    distance = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)
    duration = models.DecimalField(max_digits=10, decimal_places=1, blank=True, null=True)
    
    sponsor = models.ManyToManyField('Sponsor', limit_choices_to = {'active': True}, blank=True, null=True)
    
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    newsletter = models.BooleanField(default=False)
    coordinator = models.BooleanField(default=False)
    volunteer = models.BooleanField(default=False)
    additional_info = models.TextField(blank=True, null=True)
    
    suggestions = models.TextField(blank=True, null=True)
    
    ip = models.IPAddressField('IP Address', blank=True, null=True)
    
    objects = models.GeoManager()
    
    def __unicode__(self):
        return u'%s' % (self.id)
    
    class Meta:
        verbose_name = 'School Survey'
        verbose_name_plural = 'School Surveys'


CHILD_GRADES = (
            ('', '--'),
            ('p', 'Pre-K'),
            ('k', 'K'),
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6', '6'),
            ('7', '7'),
            ('8', '8'),
            ('9', '9'),
            ('10', '10'),
            ('11', '11'),
            ('12', '12'),
            )

CHILD_MODES = (
            ('', '--'),
            ('w', _('Walk')),
            ('b', _('Bike')),
            ('sb', _('School Bus')),
            ('fv', _('Family Vehicle (only children in your family)')),
            ('cp', _('Carpool (with children from other families)')),
            ('t', _('Transit (city bus, subway, etc.)')),
            ('o', _('Other (skateboard, scooter, inline skates, etc.)'))
            )

CHILD_DROPOFF = (
            ('', '--'),
            ('yes', _('Yes')),
            ('no', _('No')),
            )
    
class Child(models.Model):
    """ A child that's checked in at a School """
    
    survey = models.ForeignKey('Studentsurvey')
    
    grade = models.CharField(max_length=2, blank=True, null=True, choices=CHILD_GRADES)
    
    to_school_today = models.CharField(max_length=2, blank=True, null=True, choices=CHILD_MODES)
    dropoff_today = models.CharField(max_length=3, blank=True, null=True, choices=CHILD_DROPOFF)   
    from_school_today = models.CharField(max_length=2, blank=True, null=True, choices=CHILD_MODES)    
    pickup_today = models.CharField(max_length=3, blank=True, null=True, choices=CHILD_DROPOFF)
    
    to_school_yesterday = models.CharField(max_length=2, blank=True, null=True, choices=CHILD_MODES)
    dropoff_yesterday = models.CharField(max_length=3, blank=True, null=True, choices=CHILD_DROPOFF)   
    from_school_yesterday = models.CharField(max_length=2, blank=True, null=True, choices=CHILD_MODES)    
    pickup_yesterday = models.CharField(max_length=3, blank=True, null=True, choices=CHILD_DROPOFF)
    
    weight = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Children'
        
    def __unicode__(self):
        return u'%s' % (self.id)
    


