from .models import Reservation, Table

HOLIDAYS = [
    {'month': 1, 'day': 1}, # New Year's Day
    {'month': 1, 'day':18}, # Martin Luther King Jr. Day
    {'month': 2, 'day':21}, # President's Day
    {'month': 5, 'day': 8}, # Mother's Day
    {'month': 5, 'day':31}, # Memorial Day
    {'month': 7, 'day': 4}, # Independence Day
    {'month': 9, 'day': 7}, # Labor Day
    {'month': 10, 'day': 12}, # Columbus Day
    {'month': 11, 'day': 11}, # Veterans Day
    {'month': 11, 'day': 25}, # Thanksgiving Day
    {'month': 12, 'day': 25}, # Christmas Day
    {'month': 12, 'day': 31}, # New Year's Eve
]

def check_for_high_traffic(start_time):
    reservationDate = start_time
    
    # Check if date is a holiday
    for holiday in HOLIDAYS:
        if holiday == reservationDate:
            return True
    
    # Check if restaurant booking is above 50% capacity
    # Get maiximun capacity
    Tables = Table.query.all()
    maxCapacity = 0
    for table in Tables:
        if table.capacity > maxCapacity:
            maxCapacity += table.capacity
    # Multiply capacity for amount of hourse open
    maxCapacity *= 12

    # Get amount of people booked
    reservations = Reservation.query.all()
    amountOfPeopleBooked = 0
    for reservation in reservations:
        amountOfPeopleBooked += reservation.party_size

    # Check if amount of people booked is above 50% of capacity
    if amountOfPeopleBooked > maxCapacity * 0.5:
        return True
    
    return False