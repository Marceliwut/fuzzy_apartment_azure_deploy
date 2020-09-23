"""
Definition of forms.
"""

from django import forms
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _


class UserInput(forms.Form):
    city = forms.CharField(label='Miasto', initial="Kraków", required=True)
    price = forms.IntegerField(label='Cena mieszkania', initial="500000", required=True)
    size_min = forms.IntegerField(label='Wielkość minimum', initial="40", required=True)
    size_max = forms.IntegerField(label='Wielkość maksimum', initial="60", required=True)
    rooms_min = forms.IntegerField(label='Liczba pokoi minimum', initial="2", required=True)
    rooms_max = forms.IntegerField(label='Liczba pokoi maksimum', initial="4", required=True)
    #pages = forms.IntegerField(label='Limit stron', initial="1")
    limiter = forms.IntegerField(label='Limit wyników', initial="4", required=True)


   