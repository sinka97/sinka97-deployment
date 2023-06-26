from django import forms

class DateForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class': 'flex-grow-1'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date', 'class': 'flex-grow-1'}))