import json
class Film:
    def __init__(self, filmName, imageLink, id, seatInfo):
        # Film class constructor
        self.filmName = filmName
        self.imageLink = imageLink
        self.id = id
        self.seatInfo = seatInfo
        
class Seat:
    def __init__(self, seatNo, seatOccupied, buyerName, amount):
        # Seat class constructor
        self.seatNo = seatNo
        self.seatOccupied = seatOccupied
        self.buyerName = buyerName
        self.amount = amount

def bringTheData():
    # Read data from 'rawData.json' and convert it into Film objects   
    file = open('rawData.json')    
    data = json.load(file)
    filmList = []
    # Iterate through each film in the data
    for filmName in data.keys():
        film = data[filmName]
        # Create Seat objects for the film's seat information
        seatList = [Seat(seat["seatNumber"], seat['seatOccupied'], seat['buyerName'], seat['amount']) for seat in film['seatInfo']]
        # Create a Film object and append it to the filmList
        filmList.append(Film(filmName, film['image'], film['id'], seatList))
    return filmList

filmList = bringTheData()