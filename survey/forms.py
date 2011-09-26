from django.forms import ModelForm, HiddenInput, TextInput, IntegerField, CharField, ChoiceField, ModelChoiceField, DecimalField, ModelMultipleChoiceField 

# lazy translation
from django.utils.translation import ugettext_lazy as _

from survey.models import Studentsurvey, Child, CHILD_MODES, CHILD_GRADES, CHILD_DROPOFF, Sponsor, School, Adultsurvey


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


class StudentForm(ModelForm):
    """
    Parent Survey Form
    """
    
    class Meta:
        model = Studentsurvey
        exclude = ('walkrideday', 'ip')
        
        widgets = {
            'home_location': HiddenInput(),
            'distance': HiddenInput(),
            'duration': HiddenInput(),
            'school': HiddenInput(),   
        }

class ChildForm(ModelForm):
    """
    Sub-form for collecting information for each child in given school.
    """
    
    grade = ChoiceField(label=_('What grade is your child in?'),
                      choices=CHILD_GRADES,
                      required=True,
                      initial='',)
    
    to_school_today = ChoiceField(label=_('How did your child get TO school today?'),
                      choices=CHILD_MODES,
                      required=True,)
    from_school_today = ChoiceField(label=_('How did your child get home FROM school today?'),
                      choices=CHILD_MODES,
                      required=True,)
    
    to_school_yesterday = ChoiceField(label=_('How did your child get TO school yesterday?'),
                      choices=CHILD_MODES,
                      required=False,)
    from_school_yesterday = ChoiceField(label=_('How did your child get home FROM school yesterday?'),
                      choices=CHILD_MODES,
                      required=False,)

    
    class Meta:
        model = Child
        exclude = ('dropoff_today', 'pickup_today', 'dropoff_yesterday', 'pickup_yesterday', 'weight',)