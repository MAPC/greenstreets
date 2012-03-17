from django.forms import ModelForm, HiddenInput

from survey.models import Commutersurvey, Studentsurvey, Studentgroup


class CommuterForm(ModelForm):
    class Meta:
        model = Commutersurvey
        exclude = ('walkrideday','ip')
        widgets = {
                   'home_location': HiddenInput(),
                   'work_location': HiddenInput(),
                   'distance': HiddenInput(),
                   'duration': HiddenInput(),
                   }


class StudentForm(ModelForm): 
    class Meta:
        model = Studentsurvey
        exclude = ('ip', 'created')
        widgets = {
          'school': HiddenInput(),   
        }


class StudentgroupForm(ModelForm):
    class Meta:
        model = Studentgroup
        exclude = ('created')
    
