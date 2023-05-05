from django.forms import ModelForm
from django import forms
from .models import SoEmployee, SoOut, SoType, Shift




class SoOutForm(ModelForm):
    class Meta:
        model = SoOut
        fields = ['co_fk_type_id_key','co_fk_em_id_key','co_date','co_time_dif','co_time_arrived']
        labels = { 'co_fk_em_id_key': 'Employee' }
        widgets = {
            'co_fk_em_id_key': forms.Select(attrs={'class':'form-control', 'id':'single1'}),
            'co_fk_type_id_key': forms.Select(attrs={'class  mr-5':''}), 
            'co_time_arrived': forms.HiddenInput(),
            'co_date': forms.HiddenInput(),
            'co_time_dif': forms.HiddenInput()
        }



class UpdateoOutsForm(ModelForm):
    class Meta:
        model = SoOut
        fields = ['co_fk_type_id_key','co_fk_em_id_key','co_date','co_time_dif','co_time_arrived']
        labels = {
            "co_fk_type_id_key": 'Type',
            'co_fk_em_id_key': "Name", 
            'co_date': 'asdasdad',
            'co_time_arrived': 'Time Arrived',
        }
        widgets = { 
            'co_fk_em_id_key': forms.HiddenInput(),
            'co_fk_type_id_key': forms.Select(attrs={'class':'form-control','required': True}), 
            'co_time_arrived': forms.HiddenInput(),
            'co_date':  forms.HiddenInput(),
            'co_time_dif': forms.HiddenInput()
        } 

        
class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))