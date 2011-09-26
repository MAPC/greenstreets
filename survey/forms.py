from django.forms import ModelForm, HiddenInput, TextInput, IntegerField, CharField, ChoiceField, ModelChoiceField, DecimalField, ModelMultipleChoiceField 

# lazy translation
from django.utils.translation import ugettext_lazy as _

from survey.models import Schoolsurvey, Child, CHILD_MODES, CHILD_GRADES, CHILD_DROPOFF, Sponsor, School, Adultsurvey


class AdultForm(ModelForm):
    
    class Meta:
        model = Adultsurvey
        exclude = ('walkrideday','ip')
        widgets = {
                   'home_location': HiddenInput(),
                   'work_location': HiddenInput(),
                   'distance': HiddenInput(),
                   'duration': HiddenInput(),
                   }


class SurveyForm(ModelForm):
    """
    Parent Survey Form.
    """
    
    school = ModelChoiceField(queryset=School.objects.filter(survey_active=True))
    
    home_street = CharField(label=_('Name of your street'),
                    widget = TextInput(attrs={'size': '30'}),
                    required=False,)
    home_cross_st = CharField(label=_('Name of nearest cross-street'),
                    widget = TextInput(attrs={'size': '30'}),
                    required=False,)
    
    sponsor = ModelMultipleChoiceField(queryset=Sponsor.objects.filter(active=True))
    
    class Meta:
        model = Schoolsurvey
        exclude = ('walkrideday', 'ip')
        
        widgets = {
            'location': HiddenInput(),
            'distance': HiddenInput(),
            'duration': HiddenInput(),      
        }

class ChildForm(ModelForm):
    """
    Sub-form for collecting information for each child in given school.
    """
    
    grade = ChoiceField(label=_('What grade is your child in? (<span class="required_field">required</span>)'),
                      choices=CHILD_GRADES,
                      required=True,
                      initial='',)
    
    weight = DecimalField(label=_('What is your child\'s weight (used for estimating burned calories)?'),
               widget = TextInput(attrs={'size': '30'}),
               required=False,)
    
    to_school_today = ChoiceField(label=_('How does your child get TO school today? (<span class="required_field">required</span>)'),
                      choices=CHILD_MODES,
                      required=True,)
    dropoff_today = ChoiceField(label=_('Do you drop off your child on your way to work or another destination?'),
                      choices=CHILD_DROPOFF,
                      required=False,
                      initial='',)
    from_school_today = ChoiceField(label=_('How does your child get home FROM school today? (<span class="required_field">required</span>)'),
                      choices=CHILD_MODES,
                      required=True,)
    pickup_today = ChoiceField(label=_('Do you pick up your child on your way from work or another origin?'),
                      choices=CHILD_DROPOFF,
                      required=False,
                      initial='',)
    
    to_school_yesterday = ChoiceField(label=_('How did your child get TO school yesterday?'),
                      choices=CHILD_MODES,
                      required=False,)
    dropoff_yesterday = ChoiceField(label=_('Did you drop off your child on your way to work or another destination?'),
                      choices=CHILD_DROPOFF,
                      required=False,
                      initial='',)
    from_school_yesterday = ChoiceField(label=_('How did your child get home FROM school yesterday?'),
                      choices=CHILD_MODES,
                      required=False,)
    pickup_yesterday = ChoiceField(label=_('Did pick up your child on your way from work or another origin?'),
                      choices=CHILD_DROPOFF,
                      required=False,
                      initial='',)
    
    class Meta:
        model = Child