from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import simplejson
from django.contrib.gis.geos import fromstr

from django.forms.models import inlineformset_factory

from survey.models import School, Studentsurvey, Child, Schooldistrict, Street, Town, Commutersurvey, Employer, Walkrideday
from survey.forms import StudentForm, ChildForm, CommuterForm


def process_request(request):
    """ 
    Sets 'REMOTE_ADDR' based on 'HTTP_X_FORWARDED_FOR', if the latter is
    set.
    Based on http://djangosnippets.org/snippets/1706/
    """
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR'].split(",")[0].strip()
        request.META['REMOTE_ADDR'] = ip
    return request


def index(request):
    
    return render_to_response('survey/index.html', locals(), context_instance=RequestContext(request))
    
def district(request, district_slug):
    
    district = Schooldistrict.objects.get(slug__iexact=district_slug)
    
    return render_to_response('survey/district.html', {
            'district': district,
            'MEDIA_URL': settings.MEDIA_URL,
            },
            context_instance=RequestContext(request))

def get_employer_list(employers):
    """
    Translates a given employer query object to a list containing employer objects with selected properties.
    """
    employer_list =[]
    
    for employer in employers:
        employer_name = "%s, %s" % (employer.name, employer.address)
        employer_location = "%f %f" % (employer.geometry.y, employer.geometry.x)
        employer_detail = dict(name = employer_name, latlon = employer_location, infousa_id = employer.infousa_id, )
        employer_list.append(employer_detail)

    return employer_list

def get_employers(request):
    """
    Accepts lat, lon and radius parameters and returns a JSON object of found employers
    """

    location = fromstr('POINT(%s %s)' % (request.GET['lng'], request.GET['lat']), srid=4326)

    radius = float(request.GET['radius'])

    # search for employers within radius and order by distance, limit to 500
    employers = Employer.objects.transform(4326).filter(geometry__distance_lte=(location, radius)).distance(location).order_by('distance')[:500]

    employer_list = get_employer_list(employers)
    
    return HttpResponse(simplejson.dumps(employer_list), mimetype='application/json')

def get_town_employers(request, slug):
    """
    Returns all employers and their location for a given town
    """
    
    town = get_object_or_404(Town.objects, slug=slug)
    employers = Employer.objects.transform(4326).filter(town=town)[:500]
     
    employer_list = get_employer_list(employers)
    
    return HttpResponse(simplejson.dumps(employer_list), mimetype='application/json')

def get_schools(request, slug):
    """
    Returns all schools for given district as JSON
    """
    
    # check if district exists
    district = get_object_or_404(Schooldistrict.objects, slug=slug)
    
    schools = School.objects.transform(4326).filter(districtid=district)
    
    response = {}
    
    for school in schools:
        school_latlon = "%f %f" % (school.geometry.y, school.geometry.x)
        response[school.id] = dict(name=school.name, latlon = school_latlon)

    return HttpResponse(simplejson.dumps(response), mimetype='application/json')   
    
    
def get_streets(request, slug, regional_unit):
    """
    Returns all streets for given regional unit
    """
    
    # check for streets in regional unit
    if regional_unit == "town":
        town = get_object_or_404(Town.objects, slug=slug)
        streets = Street.objects.filter(town=town)
    elif regional_unit == "schooldistrict":
        schooldistrict = get_object_or_404(Schooldistrict.objects, slug=slug)
        streets = Street.objects.filter(schooldistrict=schooldistrict)
    
    street_list =[]
    
    for street in streets:
        street_list.append(street.name)
    
    return HttpResponse(simplejson.dumps(street_list), mimetype='application/json')

def student(request):
    """
    Renders Studentform or saves it and related Childforms in case of POST request. 
    """

    request = process_request(request)

    # check if district exists
    districts = Schooldistrict.objects.filter(school__survey_active=True).distinct()

    survey = Studentsurvey()
       
    SurveyFormset = inlineformset_factory(Studentsurvey, Child, form=ChildForm, extra=1, can_delete=False)
    
    if request.method == 'POST':
        surveyform = StudentForm(request.POST, instance=survey)
        surveyformset = SurveyFormset(request.POST, instance=survey)
        survey.walkrideday = Walkrideday.objects.filter(active=True).order_by('-date')[0]
        survey.ip = request.META['REMOTE_ADDR']

        if surveyformset.is_valid() and surveyform.is_valid():
            surveyform.save()
            surveyformset.save()
            
            return render_to_response('survey/thanks.html', locals(), context_instance=RequestContext(request))
            
        else:
            towns = Town.objects.filter(survey_active=True)
            return render_to_response('survey/studentform.html', locals(), context_instance=RequestContext(request))
    else:
        towns = Town.objects.filter(survey_active=True)
        
        surveyform = StudentForm(instance=survey)
        surveyformset = SurveyFormset(instance=survey)

        return render_to_response('survey/studentform.html', locals(), context_instance=RequestContext(request))

def commuter(request):
    """
    Renders Commuterform or saves it in case of POST request. 
    """

    request = process_request(request)

    commutersurvey = Commutersurvey()

    if request.method == 'POST':
        commuterform = CommuterForm(request.POST, instance=commutersurvey)
        commutersurvey.ip = request.META['REMOTE_ADDR']
        commutersurvey.walkrideday = Walkrideday.objects.filter(active=True).order_by('-date')[0]
        if commuterform.is_valid():
            commuterform.save()
            return render_to_response('survey/thanks.html', locals(), context_instance=RequestContext(request))
        else:
            towns = Town.objects.filter(survey_active=True)
            return render_to_response('survey/commuterform.html', locals(), context_instance=RequestContext(request))
    else:
        commuterform = CommuterForm(instance=commutersurvey)
        towns = Town.objects.filter(survey_active=True)
        return render_to_response('survey/commuterform.html', locals(), context_instance=RequestContext(request))