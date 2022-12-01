# return available tables according to their availablitity time and party size and date.
# if no tables are available, return an empty list
# use "Reservation.query.get(some field of Reservation class to find)" to find and return a specific instance of a Reservation 
# - look into this later (SQL Alchemy model documentation)
# note: if a table party size isn't available, check if different combos of table sizes are available 
# - check the minimum size combos first, then grow the size if no combos suffice until no combos are left
# - assumption: make a table combo limit of 4 tables, if a party size isnt met by a combo of 4 tables then return an empty list
from models import Reservation 
from models import Table
from datetime import datetime

# Build the tables that will be used
# lets make there be 10 2-party tables, 10 4-party tables, and 10 6-party tables
twoTablesCount = 10
fourTablesCount = 10
sixTablesCount = 10
tableLimit = twoTablesCount + fourTablesCount + sixTablesCount
tables = []
count = 0
available = []
while (count < twoTablesCount): # making tables with party of 2
    table = Table()
    table.capacity = 2
    table.id = count
    table.is_taken = False
    tables.append(table)
    count+=1

while (count < (twoTablesCount + fourTablesCount)): # making tables with party of 4
    table = Table()
    table.capacity = 4
    table.id = count
    table.is_taken = False
    tables.append(table)
    count+=1

while (count < tableLimit): # making tables with party of 6
    table = Table()
    table.capacity = 6
    table.id = count
    table.is_taken = False
    tables.append(table)
    count+=1

def ReservationHandler(date, startTime, endTime, partySize):
    #Session = sessionmaker(bind=engine)
    #session = Session()
    
    # 1st check: no reservations can be made if the number of tables is at max limit
    "tablesCount = get count of total entries in Tables in database"
    if (tablesCount >= tablelimit):
        return available # an empty list
    else:
        # reservations = list of reservations from Reservation table in database
        
        while (tablesCount < tablelimit):
            for table in tables:
                currIndex = tables.index(table)
                if not table.is_taken and partySize <= table.capacity:
                    table.is_taken = True
                elif (tables.len - currIndex == 1): # checking if at end of list (no single tables met party size)
                    comboFound = False # specifies if a combination can be made                                  
                    for x in tables:
                        t1 = tables.index(x)
                        t2 = t1 + 1
                        while t2 < tableLimit:
                            # check that both tables are free and if they meet the party size when combined starting with smaller sized tables:
                            if (not tables[t1].is_taken and not tables[t2].is_taken and tables[t1].capacity + tables[t2].capacity >= partySize):
                                tables[t1].is_taken = True
                                tables[t2].is_taken = True
                                comboFound = True
                                break
                            else:
                                t2 += 1
                        if (comboFound):
                            break

   # reservation = Reservation.query.filter(date).first()
    #if ((reservation.start_time = startTime & reservation.end_time = endTime) & reservation.party_size = partySize)