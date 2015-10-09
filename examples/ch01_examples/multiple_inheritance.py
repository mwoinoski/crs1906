class FlightReservation:
    def __init__(self, airline):
        print('FlightReservation.__init__')
        self.airline = airline


class HotelReservation:
    def __init__(self, room_type):
        print('HotelReservation.__init__')
        self.room_type = room_type


class FlightAndHotelRes(FlightReservation, HotelReservation):
   def __init__(self, airline, room_type):
        print('FlightAndHotelRes.__init__')
        FlightReservation.__init__(self, airline)
        HotelReservation.__init__(self, room_type)

res = FlightAndHotelRes('United Airlines', 'King')
print('Airline:', res.airline)      # FlightReservation attribute
print('Room type:', res.room_type)  # HotelReservation attribute
