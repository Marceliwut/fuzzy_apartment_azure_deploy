
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl
from app.Scrapper import launcher
from app.Scrapper import Apartment
from datetime import datetime
from app.forms import UserInput

class InputApartment:
    def __init__(self, price, room_min, room_max, size_min, size_max, pages, limiter):
        self.price = price
        self.rooms_min = room_min
        self.rooms_max = room_max
        self.size_min = size_min
        self.size_max = size_max
        self.pages = pages
        self.limiter = limiter


def draw_plots(price, price_in_range, price_bit_high, price_really_high, rooms, rooms_too_few, rooms_in_range, rooms_too_many, size, size_too_small, size_in_range, size_too_big, score_super_low, score_bit_low, score_low, score_mid_low, score_mid, score_mid_high, score_high_low, score_high_mid, score_high, score_ideal ):
    # Visualize these universes and membership functions
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))
    fig, (ax3)= plt.subplots(nrows=1, figsize=(7, 6))
   

    ax0.set_title('Price')
    ax0.set_yscale('log')

    #ax0.axis(0,1,100000,1000000)
    #x1,x2,y1,y2 = ax0.axis()
    #ax0.axis((x1,x2,100000,1000000))
   #pppp ax0.plot(price, price_in_range, 'b', linewidth=1.5, label='In range')
   # ax0.plot(price, price_bit_high, 'g', linewidth=1.5, label='Bit high')
    #plt.ylim(0, 1000000)
   # ax0.plot(price, price_really_high, 'r', linewidth=1.5, label='Really high')
    

    ax1.set_title('Number of rooms')
    ax1.plot(rooms, rooms_too_few, 'b', linewidth=1.5, label='Too few')
    ax1.plot(rooms, rooms_in_range, 'g', linewidth=1.5, label='In range')
    ax1.plot(rooms, rooms_too_many, 'r', linewidth=1.5, label='Too many')
    
    ax2.set_title('Size in square meters')
    ax2.plot(size, size_too_small, 'b', linewidth=1.5, label='Too low')
    ax2.plot(size, size_in_range, 'g', linewidth=1.5, label='In range')
    ax2.plot(size, size_too_big, 'r', linewidth=1.5, label='Too big')

    ax3.set_title('Ideal score')
    ax3.plot(ideal_score, score_super_low, 'b', linewidth=1.5, label='Super low')
    ax3.plot(ideal_score, score_bit_low, 'g', linewidth=1.5, label='Bit low')
    ax3.plot(ideal_score, score_low, 'c', linewidth=1.5, label='Low')
    ax3.plot(ideal_score, score_mid_low, 'm', linewidth=1.5, label='Mid Low')
    ax3.plot(ideal_score, score_mid, 'y', linewidth=1.5, label='Mid')
    ax3.plot(ideal_score, score_mid_high, 'b', linewidth=1.5, label='Mid high')
    ax3.plot(ideal_score, score_high_low, 'g', linewidth=1.5, label='High low')
    ax3.plot(ideal_score, score_high_mid, 'c', linewidth=1.5, label='High mid')
    ax3.plot(ideal_score, score_high, 'm', linewidth=1.5, label='High')
    ax3.plot(ideal_score, score_ideal, 'r', linewidth=1.5, label='ideal')

    ax0.legend()
    ax1.legend()
    ax2.legend()
    ax3.legend()
    plt.tight_layout()
    plt.show()
    plt.savefig('foo.pdf')

def draw_result_plot (ideal_score, score_super_low, score_bit_low, score_low, score_mid_low, score_mid, score_mid_high, score_high_low, score_high_mid, score_high, score_ideal, score0, aggregated, final_ideal_score, final_score_activation):
    #plotting results here
    fig, ax0 = plt.subplots(figsize=(8, 3))

    ax0.plot(ideal_score, score_super_low, 'b', linewidth=0.5, linestyle='--')
    ax0.plot(ideal_score, score_bit_low, 'g', linewidth=0.5, linestyle='--')
    ax0.plot(ideal_score, score_low, 'c', linewidth=0.5, linestyle='--')
    ax0.plot(ideal_score, score_mid_low, 'm', linewidth=0.5, linestyle='--')
    ax0.plot(ideal_score, score_mid, 'y', linewidth=0.5, linestyle='--')
    ax0.plot(ideal_score, score_mid_high, 'b', linewidth=0.5, linestyle='--')
    ax0.plot(ideal_score, score_high_low, 'g', linewidth=0.5, linestyle='--')
    ax0.plot(ideal_score, score_high_mid, 'c', linewidth=0.5, linestyle='--')
    ax0.plot(ideal_score, score_high, 'm', linewidth=0.5, linestyle='--')
    ax0.plot(ideal_score, score_ideal, 'r', linewidth=0.5, linestyle='--')

    ax0.fill_between(ideal_score, score0, aggregated, facecolor='Blue', alpha=0.7)
    ax0.plot([final_ideal_score, final_ideal_score], [0, final_score_activation], 'k', linewidth=1.5, alpha=0.9)
    ax0.set_title('Result plot:')

    plt.tight_layout()
    plt.show()
def start_fuzzy_engine(formUserInput):
    startTime = datetime.now()
    #dividing prices by 1000 was one of the ideas to speed up assignement process -unlucky idea to be honest
    speed_up_price_calc = 1


    #input variables -static for now
    input_price = float(formUserInput.price)# / speed_up_price_calc
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
    ideal_score = np.arange(0, 10, 1)

    #fuzzy membership functions
    price_in_range = fuzz.trapmf(price, [0, 0, (input_price * 0.9), (input_price *1.05)])
    price_bit_high = fuzz.trapmf(price, [(input_price), (input_price * 1.05), (input_price * 1.10), (input_price * 1.15)])
    price_really_high = fuzz.trapmf(price, [(input_price * 1.10), (input_price * 1.20), (10000000 / speed_up_price_calc), (10000000 / speed_up_price_calc)])


    if input_room_min != 1:
        rooms_too_few = fuzz.trimf(rooms, [0, 0, input_room_min ])
    else:
        rooms_too_few = fuzz.trimf(rooms, [0, 0, 0, 1])

    rooms_in_range = fuzz.trapmf(rooms, [input_room_min, input_room_min, input_room_max, input_room_max])
    #Exception handling if max rooms are over 20. It will be limited to 20 on user interface
    if input_room_max != 20:
        if input_room_max == 0:
            rooms_too_many = fuzz.trapmf(rooms, [20, 20, 20, 20])
        else:
            rooms_too_many = fuzz.trapmf(rooms, [input_room_max, (input_room_max + 2), 20, 20])
    else:
        rooms_too_many = fuzz.trapmf(rooms, [21, 21, 21, 21])

    size_too_small = fuzz.trimf(size, [0, 0, input_size_min])
    size_in_range = fuzz.trapmf(size, [input_size_min, input_size_min, input_size_max, input_size_max])
    size_too_big = fuzz.trapmf(size, [input_size_max, input_size_max * 1.3, 200, 200])

    #output -  ideal score
    score_super_low = fuzz.trimf(ideal_score, [0, 1, 2])
    score_bit_low = fuzz.trimf(ideal_score, [1, 2, 3])
    score_low = fuzz.trimf(ideal_score, [2, 3, 4])
    score_mid_low = fuzz.trimf(ideal_score, [3, 4, 5])
    score_mid = fuzz.trimf(ideal_score, [4, 5, 6])
    score_mid_high = fuzz.trimf(ideal_score, [5, 6, 7])
    score_high_low = fuzz.trimf(ideal_score, [6, 7, 8])
    score_high_mid = fuzz.trimf(ideal_score, [7, 8, 9])
    score_high = fuzz.trimf(ideal_score, [8, 9, 10])
    score_ideal = fuzz.trimf(ideal_score, [10, 10, 10])

    #draw_plots(price, price_in_range, price_bit_high, price_really_high, rooms, rooms_too_few, rooms_in_range, rooms_too_many, size, size_too_small, size_in_range, size_too_big, score_super_low, score_bit_low, score_low, score_mid_low, score_mid, score_mid_high, score_high_low, score_high_mid, score_high, score_ideal)


    #Starting scrapper for newest apartment_list from domiporta.pl
    apartment_list = launcher("Kraków", "", pages, limiter)

    #For debugging purposes
    #print("Script downloaded ", len(apartment_list), " apartments in: ", (datetime.now() - startTime))
    i = 1

    forStartTime = datetime.now()
    for apartment in apartment_list:
        activation_super_low_score = 0
        activation_bit_low_score = 0
        activation_low_score = 0 
        activation_mid_low_score = 0
        activation_mid_score = 0    
        activation_mid_high_score = 0
        activation_high_low_score = 0
        activation_high_mid_score = 0
        activation_high_score = 0
        activation_ideal_score = 0

        #activation range for inputs
        #activation for price
        activation_price_in_range = fuzz.interp_membership(price, price_in_range, (int(apartment.price) / speed_up_price_calc))
        activation_price_bit_high = fuzz.interp_membership(price, price_bit_high, (int(apartment.price) / speed_up_price_calc))
        activation_price_really_high = fuzz.interp_membership(price, price_really_high, (int(apartment.price) / speed_up_price_calc))

        #activation for size
        activation_size_too_small = fuzz.interp_membership(size, size_too_small, apartment.size)
        activation_size_in_range = fuzz.interp_membership(size, size_in_range, apartment.size)
        activation_size_too_big = fuzz.interp_membership(size, size_too_big, apartment.size)


        #rules and rules assignemenets
        #rules for price in range
        active_rule1 = np.fmax(activation_price_in_range, activation_size_in_range)
        activation_ideal_score = np.fmax(active_rule1, score_ideal)

        active_rule2 = np.fmax(activation_price_in_range, activation_size_too_small)
        activation_mid_high_score = np.fmax(active_rule2, score_mid_low)

        active_rule3 = np.fmax(activation_price_in_range, activation_size_too_big)
        activation_high_score = np.fmax(active_rule3, score_high)

        #rules for bit high price
        active_rule4 = np.fmax(activation_price_bit_high, activation_size_in_range)
        activation_mid_score = np.fmax(active_rule4, score_mid)

        active_rule5 = np.fmax(activation_price_bit_high, activation_size_too_small)
        activation_low_score = np.fmax(active_rule5, score_low)

        active_rule6 = np.fmax(activation_price_bit_high, activation_size_too_big)
        activation_high_score = np.fmax(active_rule6, score_low)

        #rules for really high price
        active_rule7 = np.fmax(activation_price_really_high, activation_size_in_range)
        activation_low_score = np.fmax(active_rule7, score_mid)

        active_rule8 = np.fmax(activation_price_really_high, activation_size_too_small)
        activation_super_low_score = np.fmax(active_rule8, score_super_low)

        active_rule9 = np.fmax(activation_price_really_high, activation_size_too_big)
        activation_bit_low_score = np.fmax(active_rule9, score_bit_low)

        score0 = np.zeros_like(ideal_score)
        #aggregating results and deffuzification
        aggregated = np.fmax(activation_super_low_score,
                         np.fmax(activation_bit_low_score,
                                 np.fmax(activation_low_score,
                                         np.fmax(activation_mid_low_score,
                                                 np.fmax(activation_mid_score,
                                                         np.fmax(activation_mid_high_score,
                                                                 np.fmax(activation_high_low_score,
                                                                         np.fmax(activation_high_mid_score,
                                                                                 np.fmax(activation_high_score, activation_ideal_score)))))))))

        final_ideal_score = fuzz.defuzz(ideal_score, aggregated, 'centroid')
        final_score_activation = fuzz.interp_membership(ideal_score, aggregated, final_ideal_score)
        apartment.ideal_score = final_ideal_score
    
        #Plot function for result
        #draw_result_plot (ideal_score, score_super_low, score_bit_low, score_low, score_mid_low, score_mid, score_mid_high, score_high_low, score_high_mid, score_high, score_ideal, score0, aggregated, final_ideal_score, final_score_activation)

        i = i + 1

    #for apartment in apartment_list:
    #    print(apartment)


    #Debugging purposes
    #print("For finished in: ", (datetime.now() - forStartTime))
    #print("Script finished in: ", (datetime.now() - startTime))
    return apartment_list