from django.forms import ModelForm
from django import forms
from .models import SoEmployee, SoOut, SoType, Shift
from django.forms.widgets import DateInput



class SoOutForm(ModelForm):
    class Meta:
        model = SoOut
        fields = ['co_date','co_time_dif','co_time_arrived','co_fk_type_id_key','co_fk_em_id_key']
        labels = { 'co_fk_type_id_key':'Type','co_fk_em_id_key': 'Employee'}
        widgets = {
            'co_fk_em_id_key': forms.Select(attrs={'class':'form-control', 'id':'single1', 'required':'True'}),
            'co_fk_type_id_key': forms.Select(attrs={'class':'form-control', 'id':'single3', 'required':'True'}), 
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
            'co_date': 'Date',
            'co_time_arrived': 'Time Arrived',
        }

        widgets = { 
            'co_fk_em_id_key': forms.HiddenInput(),
            'co_fk_type_id_key': forms.Select(attrs={'class':'form-control'}), 
            'co_time_arrived': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'},format='%H:%M'),
            'co_date': DateInput(attrs={'class':'form-control','type': 'date'}),
            'co_time_dif': forms.HiddenInput()
        } 

        
class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))