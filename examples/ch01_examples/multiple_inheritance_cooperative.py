class Reservation:
    def __init__(self, name, *args, **kwargs):
        print(f"Reservation.__init__, name='{name}',",
              f"args={args}, kwargs={kwargs}")
        super().__init__(*args, **kwargs)  # args and kwargs will be empty
        self.name = name


class FlightReservation(Reservation):
    def __init__(self, airline, *args, **kwargs):
        print(f"FlightReservation.__init__, airline='{airline}',",
              f"args={args}, kwargs={kwargs}")
        super().__init__(*args, **kwargs)
        self.airline = airline


class HotelReservation(Reservation):
    def __init__(self, room_type, *args, **kwargs):
        print(f"HotelReservation.__init__, room_type='{room_type}',",
              f"args={args}, kwargs={kwargs}")
        super().__init__(*args, **kwargs)
        self.room_type = room_type


class FlightAndHotelRes(FlightReservation, HotelReservation):
   def __init__(self, name, airline, room_type):
        print('FlightAndHotelRes.__init__')
        super().__init__(name=name, airline=airline, room_type=room_type)
       

res = FlightAndHotelRes('Guido', 'United Airlines', 'King')
print('Name:', res.name)  # access Reservation attribute
print('Airline:', res.airline)  # access FlightReservation attribute
print('Room type:', res.room_type)  # access HotelReservation attribute
