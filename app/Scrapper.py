

from lxml import html
import requests

########## # # # # # #
#
# Scrapper
# @mmirzyns ver.0.2 -added auto page limitation
#
# # # # # # # # # # # # # # # #

class Apartment:
    def __init__(self, name, link, price, room, size):
        self.name = name
        self.link = link
        self.price = price
        self.room = room
        self.size = size
        self.ideal_score = 0
    def __str__(self):
        return_string = ("Name: " + str(self.name) + "Link: " + str(self.link) + " Price: " + str(self.price) + " Rooms: " + str(self.room) + " Size: " + str(self.size) + " Score: " + str(self.ideal_score))
        return return_string
   

def clear_data(v, type):
    v = str(v)

    return v
def clear_data(lxml_list, type):
    temp_list = list()
    for v in lxml_list:
        v = v.replace("zł", "")
        v = v.replace(" ", "")
        v = v.replace("\r\n", "")
        v = v.replace("\n", "")
        v = v.replace("\xa0", "")
        v = v.replace("\'\r\n\'", "")
        v = v.replace("\r\n", "")
        v = v.replace(" ", "")
        if type == 'size':
            v = v.replace(",", ".")
            v = v.replace("m", "")
        if v != "":
            if ("Zapytajocenę" not in v):
                temp_list.append(v)
    return temp_list

def start_scrapper(url_address, limiter):
    
    page = requests.get(url_address)
    if page:
        tree = html.fromstring(page.content)

    #prices = tree.xpath('//span[@title="buyer-name"]/text()')
    prices = tree.xpath('//span[@class="sneakpeak__details_price"]/text()')
    names = tree.xpath('//span[@class="sneakpeak__title--bold"]/text()')
    sizes = tree.xpath('//span[@class="sneakpeak__details_item sneakpeak__details_item--area"]/text()')
    rooms = tree.xpath('//span[@class="sneakpeak__details_item sneakpeak__details_item--room"]/text()')
    link = tree.xpath('//a[@class="sneakpeak__title sneakpeak__title_normal sneakpeak__link"]/@href')

    #print(link)

    cleared_sizes = clear_data(sizes, 'size')
    cleared_rooms = clear_data(rooms, 'other')
    cleared_prices = clear_data(prices, 'other')
    cleared_links = clear_data(link, 'other')

    
    apartment_list = list()
    if limiter == 0 or (limiter <= len(cleared_prices)):
        for i in range(len(cleared_prices) -1):  
            apartment_list.append(Apartment(names[i],
                                            cleared_links[i],
                                            cleared_prices[i], cleared_rooms[i], cleared_sizes[i]))
            return apartment_list
    else:
        
            for i in range(limiter):  
                apartment_list.append(Apartment(names[i], 
                                                cleared_links[i],
                                               cleared_prices[i], cleared_rooms[i], cleared_sizes[i]))

    return apartment_list

def launcher(city, district, pages, limiter):
    if limiter > 36:
        #print(limiter / 36)
        pages = int((limiter / 36)) + (limiter % 36 > 0)
        #print("changing pages to fit limiter new pages: ", pages)
        pages_changed = True
    else:
        pages_changed = False


    apartment_list = list()


        

    for i in range(pages, 0, -1): 
        if district != "":
            URL_address = 'https://www.domiporta.pl/mieszkanie/sprzedam?Localization=' + city + '/' + district + '&PageNumber=' + str(i)
        else:
            URL_address = 'https://www.domiporta.pl/mieszkanie/sprzedam?Localization=' + city + '&PageNumber=' + str(i)
        #print("Will download apartments from ", URL_address)
        if(pages_changed and limiter > 36):
            limiter = limiter - 36
            apartment_list += start_scrapper(URL_address, 36)
        else:
            apartment_list += start_scrapper(URL_address, limiter)
    return apartment_list


