# This is the User class for use of the website by all users of it. 
# User is also the parent to the Registered and Guest classes.
# Registered - defines a User that is registed to the system
# Guest - degines a default user not registered in the system

class User:
    totalUsers = 0

    def __init__(self, name = '', password = '', email = '', mailAdd = '', billAdd = '', prefDinner = -1, prefPayMethod = '', points =
    -1, reservations = ''):
        self.name = name
        self.password = password
        self.email = email
        self.mailAdd = mailAdd # mailing address
        self.billAdd = billAdd # billing address
        self.prefDinner = prefPayMethod # preferred dinner
        self.prefPayMethod = prefPayMethod # preferred payment method
        self.points = points
        self.reservations = reservations
        User.totalUsers += 1

    def makeReservation(self):
        pass

class Registered(User):
    pass

class Guest(User):
    pass
    