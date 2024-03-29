"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from app.forms import UserInput
from app.fuzzy_engine import start_fuzzy_engine
from app.fuzzy_engine import InputApartment

def check_data(cleaned_input_apartment):
    if cleaned_input_apartment.price > 10000 and cleaned_input_apartment.price < 10000000 and cleaned_input_apartment.size_min >= 0 and cleaned_input_apartment.size_max >= 0 and cleaned_input_apartment.size_max >= cleaned_input_apartment.size_min and cleaned_input_apartment.rooms_min >= 0 and cleaned_input_apartment.rooms_max >= 1 and cleaned_input_apartment.rooms_max >= cleaned_input_apartment.rooms_min:
        return True
    else:
        return False

def home(request):
    startTime = datetime.now()
    if request.method == 'POST':
        formUserInput = UserInput(request.POST)
        
        if formUserInput.is_valid():
            #try:
                cleaned_input_apartment = InputApartment(formUserInput.cleaned_data['city'], formUserInput.cleaned_data['price'], formUserInput.cleaned_data['rooms_min'], formUserInput.cleaned_data['rooms_max'], formUserInput.cleaned_data['size_min'], formUserInput.cleaned_data['size_max'], 1, formUserInput.cleaned_data['limiter'])
                if check_data(cleaned_input_apartment):
                    #launching fuzzy engine modeling
                    apartment_list = start_fuzzy_engine(cleaned_input_apartment)

                        #sorting by ideal score
                    apartment_list = sorted(apartment_list, key=lambda x: x.ideal_score, reverse=True)



                    return render(
                        request,
                            'app/results.html',
                            {
                                'speed':((datetime.now() - startTime)),
                                'apartment_list':apartment_list,
                                'formUserInput':UserInput,
                                'cleaned_input_apartment':cleaned_input_apartment,
                                'title':'Strona główna',
                                'year':datetime.now().year,
                            }   
                   )
                else:
                    return render(
                        request,
                            'app/error_form.html',
                            {
                                'title':'Error',
                                'year':datetime.now().year,
                            }
                    )
            #except:
            #        return render(
            #            request,
            #                'app/error.html',
            #                {
            #                    'title':'Error',
            #                    'year':datetime.now().year,
            #                }
            #        )



    else:
        formUserInput = UserInput()
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/index.html',
            {
                'formUserInput':UserInput,
                'title':'Strona główna',
                'year':datetime.now().year,
            }
        )

def contact(request):


    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Kontakt z autorem',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'O aplikacji',
            'year':datetime.now().year,
        }
    )
