
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl
from app.Scrapper import launcher
from app.Scrapper import Apartment
from app.forms import UserInput

########## # # # # # #
#
# FuzzyEngine on SciKitFuzzy
# @mmirzyns ver.0.2
#
# # # # # # # # # # # # # # # #

class InputApartment:
    def __init__(self, city, price, room_min, room_max, size_min, size_max, pages, limiter):
        self.city = city
        self.price = price
        self.rooms_min = int(room_min)
        self.rooms_max = int(room_max)
        self.size_min = size_min
        self.size_max = size_max
        self.pages = pages
        self.limiter = limiter


def start_fuzzy_engine(formUserInput):

    #dividing prices by 1000 was one of the ideas to speed up assignement process -unlucky idea to be honest
    #speed_up_price_calc = 1



    #input variables -static for now
    city = formUserInput.city
    input_price = float(formUserInput.price)
    input_room_min = int(formUserInput.rooms_min)
    input_room_max = int(formUserInput.rooms_max)
    input_size_min = int(formUserInput.size_min)
    input_size_max = int(formUserInput.size_max)
    pages = int(formUserInput.pages)
    limiter = int(formUserInput.limiter)

    #print ("Inputs")
    #print("Price: ", input_price, " rooms min: ", input_room_min, " rooms max: ", input_room_max, " size min: ", input_size_min, " size max: ", input_size_max)

    #example of ideal apartment
    #ideal_apartment = Apartment("ideal",(input_price / 2), round((((input_room_max - input_room_min) / 2) + input_room_min),0), (((input_size_max - input_size_min) / 2) + input_size_min))


    #universe variables
    #price of the aparatment up to 10 mln, will be limited to 8 000 000 on user interface to handle really high fuzzification
    price = np.arange(0, 10000000, 1)
    #number of rooms in the apartment limited to 20 on user interface, 21 given to handle exception
    rooms = np.arange(0, 21, 1)
    #size of the apartment
    size = np.arange(10, 200, 1)
    #score given to each apartment as result of fuzzification up to 10
    ideal_score = np.arange(0, 11, 1)

    #fuzzy membership functions
    price_in_range = fuzz.trapmf(price, [0, 0, input_price, (input_price *1.05)])
    price_bit_high = fuzz.trapmf(price, [(input_price), (input_price * 1.05), (input_price * 1.10), (input_price * 1.15)])
    price_really_high = fuzz.trapmf(price, [(input_price * 1.10), (input_price * 1.20), (input_price * 1.5), (input_price * 2)])
    price_way_too_high = fuzz.trapmf(price, [(input_price * 1.5), (input_price * 2), (20000000), (20000000)])
    


    if input_room_min != 1:
        rooms_too_few = fuzz.trimf(rooms, [0, 0, input_room_min ])
    else:
        rooms_too_few = fuzz.trimf(rooms, [0, 0, 1])

    rooms_in_range = fuzz.trapmf(rooms, [input_room_min, input_room_min, input_room_max, input_room_max])
    #Exception handling if max rooms are over 20. It will be limited to 20 on user interface
    if input_room_max != 20:
        if input_room_max == 0:
            rooms_too_many = fuzz.trapmf(rooms, [20, 20, 20, 20])
        else:
            rooms_too_many = fuzz.trapmf(rooms, [input_room_max, (input_room_max + 2), 20, 20])
    else:
        rooms_too_many = fuzz.trapmf(rooms, [21, 21, 21, 21])



    size_super_small = fuzz.trapmf(size, [0, 0, (input_size_min * 0.75), (input_size_min * 0.9)])
    size_too_small = fuzz.trimf(size, [(input_size_min * 0.7), (input_size_min * 0.9), input_size_min])
    size_in_range = fuzz.trapmf(size, [input_size_min, input_size_min, input_size_max, input_size_max])
    size_too_big = fuzz.trapmf(size, [input_size_max, input_size_max * 1.3, 200, 200])

    #output -  ideal score
    score_super_low = fuzz.trimf(ideal_score, [0, 0, 2])
    score_bit_low = fuzz.trimf(ideal_score, [1, 2, 3])
    score_low = fuzz.trimf(ideal_score, [2, 3, 4])
    score_mid_low = fuzz.trimf(ideal_score, [3, 4, 5])
    score_mid = fuzz.trimf(ideal_score, [4, 5, 6])
    score_mid_high = fuzz.trimf(ideal_score, [5, 6, 7])
    score_high_low = fuzz.trimf(ideal_score, [6, 7, 8])
    score_high_mid = fuzz.trimf(ideal_score, [7, 8, 9])
    score_high = fuzz.trimf(ideal_score, [8, 9, 9.9])
    score_ideal = fuzz.trimf(ideal_score, [10, 10, 10])

   # draw_plots(price, price_in_range, price_bit_high, price_really_high, rooms, rooms_too_few, rooms_in_range, rooms_too_many, size, size_too_small, size_in_range, size_too_big, score_super_low, score_bit_low, score_low, score_mid_low, score_mid, score_mid_high, score_high_low, score_high_mid, score_high, score_ideal, ideal_score, size_super_small)


    #Starting scrapper for newest apartment_list from domiporta.pl
    apartment_list = launcher(city, "", pages, limiter)

 #   apartment1 = Apartment("Ideal","/link", 200000, 2, 50)
#    apartment2 = Apartment("Rooms_too_many","/link", 200000, 10, 50)
#    apartment3 = Apartment("Rooms_too_Few","/link", 200000, 1, 50)
    #apartment2 = Apartment("too big","/link",500000,2,80)
    #apartment3 = Apartment("small","/link",500000,2,35)
    #apartment3 = Apartment("super_small","/link",500000,2,10)
    #apartment4 = Apartment("expensive super small","/link",7000000,2,15)
#    apartment_list = list()
 #   apartment_list.append(apartment1)
#    apartment_list.append(apartment2)
#    apartment_list.append(apartment3)
   # apartment_list.append(apartment4)

    #For debugging purposes
    #print("Script downloaded ", len(apartment_list), " apartments in: ", (datetime.now() - startTime))
    i = 1
    for apartment in apartment_list:



        #activation range for inputs
        #activation for price
        activation_price_in_range = fuzz.interp_membership(price, price_in_range, apartment.price)
        activation_price_bit_high = fuzz.interp_membership(price, price_bit_high, apartment.price)
        activation_price_really_high = fuzz.interp_membership(price, price_really_high, apartment.price)
        activation_price_way_too_high = fuzz.interp_membership(price, price_way_too_high, apartment.price)

        #activation for size
        activation_size_super_small = fuzz.interp_membership(size, size_super_small, apartment.size)
        activation_size_too_small = fuzz.interp_membership(size, size_too_small, apartment.size)
        activation_size_in_range = fuzz.interp_membership(size, size_in_range, apartment.size)
        activation_size_too_big = fuzz.interp_membership(size, size_too_big, apartment.size)

        #activation for room number
        activation_rooms_too_few = fuzz.interp_membership(rooms, rooms_too_few, apartment.room)
        activation_rooms_in_range = fuzz.interp_membership(rooms, rooms_in_range, apartment.room)
        activation_rooms_too_many = fuzz.interp_membership(rooms, rooms_too_many, apartment.room)


        #print("Activation price in range", activation_price_in_range)
        #print("Price high", activation_price_bit_high)
        #print("Price really high", activation_price_really_high)
        #print("Size super small", activation_size_super_small)
        #print("Size too small", activation_size_too_small)
        #print("Size in range", activation_size_in_range)
        #print("Size too big", activation_size_too_big)

        activation_low_score = 0

        #super_low      X
        #bit_low        X
        #low            XXX
        #mid_low        X
        #mid_high       X

        #mid            X
        #high_mid       X
        #high_low       X
        #high           X
        #ideal          X

        #rules and rules assignemenets
        #rules for price in range
        in_range_rule1 = np.fmin(activation_price_in_range, np.fmin(activation_rooms_in_range, activation_size_in_range))
        activation_ideal_score = np.fmin(in_range_rule1, score_ideal)

        in_range_rule2 = np.fmin(activation_price_in_range, np.fmax(activation_size_too_big, activation_rooms_too_many))
        activation_high_score = np.fmin(in_range_rule2, score_high)

        in_range_rule3 = np.fmin(activation_price_in_range, np.fmax(activation_size_too_small, activation_rooms_too_few))
        activation_mid_score = np.fmin(in_range_rule3, score_mid)

        in_range_rule4 = np.fmin(activation_price_in_range, activation_size_super_small)
        activation_low_score = np.fmin(in_range_rule4, score_low)

        in_range_rule5 = np.fmin(activation_price_in_range, np.fmin(activation_size_in_range, activation_rooms_too_many))
        activation_mid_high_score = np.fmin(in_range_rule5, score_mid_high)

        in_range_rule6 = np.fmin(activation_price_in_range, np.fmin(activation_size_in_range, activation_rooms_too_few))
        activation_mid_low_score= np.fmin(in_range_rule6, score_mid_low)


        #prices bit high
        bit_high_rule1 = np.fmin(activation_price_bit_high, np.fmax(activation_size_too_big, activation_rooms_too_many))
        activation_high_mid_score = np.fmin(bit_high_rule1, score_high_mid)

        bit_high_rule2 = np.fmin(activation_price_bit_high, np.fmax(activation_size_in_range, activation_rooms_in_range))
        activation_high_low_score = np.fmin(bit_high_rule2, score_high_low)

        bit_high_rule3 = np.fmin(activation_price_bit_high, activation_size_too_small)
        if(activation_low_score.any() == 0):
            activation_low_score = np.fmin(bit_high_rule3, score_low)

        #print("Activation low score: ", activation_low_score)

        bit_high_rule4 = np.fmin(activation_price_bit_high, activation_size_super_small)
        activation_bit_low_score = np.fmin(bit_high_rule4, score_bit_low)



        #prices really high
        really_high_rule1 = np.fmin(activation_price_really_high, activation_size_too_big)
        if(activation_mid_high_score.any() == 0):
            activation_mid_high_score = np.fmin(really_high_rule1, score_mid_high)

        really_high_rule2 = np.fmin(activation_price_really_high, activation_size_in_range)
        if(activation_low_score.any() == 0):
            activation_mid_low_score = np.fmin(really_high_rule2, score_mid_low)

        really_high_rule3 = np.fmin(activation_price_really_high, activation_size_too_small)
        if(activation_low_score.any() == 0):
            activation_low_score = np.fmin(really_high_rule3, score_low)

        really_high_rule4 = np.fmin(activation_price_really_high, np.fmax(activation_size_super_small, activation_rooms_too_few))
        activation_super_low_score = np.fmin(really_high_rule4, score_super_low)

        way_too_high_rule1 = activation_price_way_too_high
        activation_super_low_score = np.fmin(way_too_high_rule1, score_super_low)

        #print("Activation slow score: ", activation_super_low_score)
        #print("Activation blow score: ", activation_bit_low_score)
        #print("Activation low score: ", activation_low_score)
        #print("Activation mid_high score: ", activation_mid_high_score)
        #print("Activation mid score: ", activation_mid_score)
        #print("Activation high score: ", activation_high_score)
        #print("Activation ideal score: ", activation_ideal_score)
        #os.system("PAUSE")
        #activation_bit_low_score = np.fmin(active_rule9, score_bit_low)

        aggregated = None
        aggregated = np.fmax(activation_super_low_score,
                             np.fmax(activation_bit_low_score,
                                   np.fmax(activation_low_score,
                                           np.fmax(activation_mid_low_score,
                                                np.fmax(activation_mid_high_score,
                                                    np.fmax(activation_mid_score,
                                                    np.fmax(activation_high_low_score,
                                                    np.fmax(activation_high_mid_score,
                                                            np.fmax(activation_high_score, activation_ideal_score)
                                                            )
                                                    )
                                            )
                                   )
                             ))))

        # if there somehow there are no activation functions active it will ommit this appartment
        try:
            final_ideal_score = fuzz.defuzz(ideal_score, aggregated, 'centroid')
            final_score_activation = fuzz.interp_membership(ideal_score, aggregated, final_ideal_score)
            #if round(final_ideal_score, 2) == 9.67:
            #    apartment.ideal_score = 10
            #else:
            apartment.ideal_score = round(final_ideal_score, 2)
        except AssertionError:
            final_ideal_score = ""

        i = i + 1

    return apartment_list