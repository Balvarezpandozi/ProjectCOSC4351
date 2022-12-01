from .models import Reservation, Table, ReservationTables
from datetime import datetime
import itertools

def check_table_availability(start_time, end_time, party_size):
    # Get all reservations ids that are in the time range
    reservations = Reservation.query.all()

    # Filter reservations by time range
    reservations = [reser for reser in reservations if ((reser.start_time >= start_time and reser.start_time <= end_time) or (reser.end_time >= start_time and reser.end_time <= end_time ))]

    # Get all tables that are not taken by these reservations
    tables = Table.query.all()
    print("Tables before filtering: ", tables[0].capacity, tables[1].capacity)

    # Get associative table for tables and reservations
    reservation_tables = ReservationTables.query.all()

    # Filter tables by ones that are not taken by these reservations
    for reservation in reservations:
        for association in reservation_tables:
            if association.reservation_id == reservation.id:
                if tables == []:
                    return []
                for table in tables:
                    if association.table_id == table.id:
                        tables.remove(table)

    # If tables is empty no tables are available
    if(tables == []):
        return []
    
    # If is not empty find combination of tables to fit the party size
    table_combinations = []
    for i in range(1, len(tables) + 1):
        table_combinations += list(itertools.combinations(tables, i))
    
    # Find combination that fits the party size
    for combination in table_combinations:
        if sum([table.capacity for table in combination]) >= party_size:
            return combination

    return []