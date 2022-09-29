import User

class Reservation:
    totalReservations = 0

    def __init__(self, startTime = '', endTime = '', tables = [], partySize = -1):
        self.startTime = startTime
        self.endTime = endTime
        self.tables = tables
        self.partySize = partySize
        Reservation.totalReservations += 1