from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.utils import simplejson
from django.forms.models import inlineformset_factory

from survey.models import School, Schooldistrict, Commutersurvey, Employer, Studentsurvey, Studentgroup
from survey.forms import CommuterForm, StudentForm, StudentgroupForm


def process_request(request):
    """ 
    Sets 'REMOTE_ADDR' to 'HTTP_X_REAL_IP', if the latter is set.
    'HTTP_X_REAL_IP' is specified in Nginx config.
    """
    if 'HTTP_X_REAL_IP' in request.META:
        request.META['REMOTE_ADDR'] = request.META['HTTP_X_REAL_IP']
    return request
    

def get_schools(request, slug):
    """
    Returns all schools for given district as JSON
    """
    
    # check if exists
    district = get_object_or_404(Schooldistrict.objects, slug=slug)
    
    schools = School.objects.filter(districtid=district).order_by('name')
    
    # build slim response data
    response = []
    for school in schools:
        response.append(dict(name=school.name, id=school.id))

    return HttpResponse(simplejson.dumps(response), mimetype='application/json')   
  

def commuter(request):
    """
    Renders Commuterform or saves it in case of POST request. 
    """

    request = process_request(request)

    survey = Commutersurvey()

    employers = Employer.objects.filter(active=True)

    if request.method == 'POST':
        surveyform = CommuterForm(request.POST, instance=survey)
        survey.ip = request.META['REMOTE_ADDR']
        
        # check if user already checked in this month
        month = request.POST['month']
        email = request.POST['email']
        if Commutersurvey.objects.filter(month__iexact=month, email__iexact=email).exists():
            existing_survey = Commutersurvey.objects.filter(month__iexact=month, email__iexact=email).order_by('-created')[0]
            # addding existing id forces update
            survey.id = existing_survey.id
            survey.created = existing_survey.created

        # add new employer to GSI Employer list
        employer = request.POST['employer']
        if employer != "" and not Employer.objects.filter(name__exact=employer):
            new_employer = Employer(name=employer)
            new_employer.save()

        if surveyform.is_valid():
            surveyform.save() 
            return render_to_response('survey/thanks.html', locals(), context_instance=RequestContext(request))
        else:
            return render_to_response('survey/commuterform.html', locals(), context_instance=RequestContext(request))
    else:
        surveyform = CommuterForm(instance=survey)
        return render_to_response('survey/commuterform.html', locals(), context_instance=RequestContext(request))


def student(request):
    """ 
    Renders Teacherform or saves it if POST
    """

    request = process_request(request)

    # get all school districts with participating schools
    districts = Schooldistrict.objects.filter(school__survey_active=True).distinct()

    survey = Studentsurvey()

    SurveyFormset = inlineformset_factory(Studentsurvey, Studentgroup, form=StudentgroupForm, extra=1, can_delete=False)

    if request.method == 'POST':
        surveyform = StudentForm(request.POST, instance=survey)
        surveyformset = SurveyFormset(request.POST, instance=survey)
        survey.ip = request.META['REMOTE_ADDR']

        # check if user already checked in this month
        month = request.POST['month']
        teacher_email = request.POST['teacher_email']
        if Studentsurvey.objects.filter(month__iexact=month, teacher_email__iexact=teacher_email).exists():
            existing_survey = Studentsurvey.objects.filter(month__iexact=month, teacher_email__iexact=teacher_email).order_by('-created')[0]
            # remove all related objects
            existing_studentgroups = existing_survey.studentgroup_set.all()
            for existing_studentgroup in existing_studentgroups:
                existing_studentgroup.delete()
            # adding existing id forces update
            survey.id = existing_survey.id
            survey.created = existing_survey.created
            
        if surveyformset.is_valid() and surveyform.is_valid():
            surveyform.save()
            surveyformset.save()  
            month = request.POST['month']
            return render_to_response('survey/thanks.html', locals(), context_instance=RequestContext(request)) 
        else:
            return render_to_response('survey/studentform.html', locals(), context_instance=RequestContext(request))
    else:
        surveyform = StudentForm(instance=survey)
        surveyformset = SurveyFormset(instance=survey)
    return render_to_response('survey/studentform.html', locals(), context_instance=RequestContext(request))


