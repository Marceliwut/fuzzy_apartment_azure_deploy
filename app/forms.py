"""
Definition of forms.
"""

from django import forms
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _


class UserInput(forms.Form):
    city = forms.CharField(label='Miasto', initial="Kraków", required=True)
    price = forms.FloatField(label='Cena mieszkania', initial="500000", required=True)
    size_min = forms.IntegerField(label='Wielkość minimum', initial="40", required=True)
    size_max = forms.IntegerField(label='Wielkość maksimum', initial="60", required=True)
    rooms_min = forms.IntegerField(label='Liczba pokoi minimum', initial="2", required=True)
    rooms_max = forms.IntegerField(label='Liczba pokoi maksimum', initial="4", required=True)
    #pages = forms.IntegerField(label='Limit stron', initial="1")
    limiter = forms.IntegerField(label='Limit wyników', initial="4", required=True)

    def check_data(self):
        if self.price > 10000 and self.price < 10000000 and self.size_min >= 0 and self.size_max >= 0 and self.size_max >= self.size_min and self.rooms_min >= 0 and self.rooms_max >= 1 and self.rooms_max >= self.rooms_min:
            return True
        else:
            return False


   