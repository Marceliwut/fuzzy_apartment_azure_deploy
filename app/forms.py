"""
Definition of forms.
"""

from django import forms
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _


class UserInput(forms.Form):
    city = forms.CharField(label='Miasto', initial="Kraków")
    price = forms.CharField(label='Cena mieszkania', initial="500000")
    size_min = forms.IntegerField(label='Wielkość minimum', initial="40")
    size_max = forms.IntegerField(label='Wielkość maksimum', initial="60")
    rooms_min = forms.IntegerField(label='Ilość pokoi minimum', initial="2")
    rooms_max = forms.IntegerField(label='Ilość pokoi maksimum', initial="4")
    #pages = forms.IntegerField(label='Limit stron', initial="1")
    limiter = forms.IntegerField(label='Limit wyników', initial="4")

    def check_data(self):
        if self.price > 10000 and size_min >= 0 and size_max >= 0 and size_max >= size_min and rooms_min >= 0 and rooms_max >= 1 and rooms_max >= rooms_min:
            return True
        else:
            return False


   