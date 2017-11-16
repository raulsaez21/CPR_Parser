import csv
import sys
import os
from operator import itemgetter


def read_flights(filename):
    list_flights = []

    with open(filename, 'rb') as flights_file:
        reader = csv.reader(flights_file, delimiter=';', lineterminator='\n')
        try:
            for row in reader:
                list_flights.append(row)
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

    flights_file.close()
    print 'Flight stored to list'
    return list_flights


def read_flights_comma(filename):
    list_flights = []

    with open(filename, 'rb') as flights_file:
        reader = csv.reader(flights_file, delimiter=',', lineterminator='\n')
        try:
            for row in reader:
                list_flights.append(row)
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

    flights_file.close()
    print 'Flight stored to list'
    return list_flights


def write_sorted_flight(output_filename, flights):

    for t in range(0, len(flights)):
        with open(output_filename, 'a') as SO6_file:
            writer = csv.writer(SO6_file)
            line_SO6 = flights[t]
            writer.writerow(line_SO6)

    print 'Sorted flights files created'
    return


# Main
CPR_filename = 'previous_D_flights.csv'
D_before_flights = read_flights_comma(CPR_filename)

#CPR_filename = '1.201607281001tacop104ARCHIVED_OPLOG_ALL_CPR'
CPR_filename = '1.201702201001tacop304ARCHIVED_OPLOG_ALL_CPR'
D_flights = read_flights(CPR_filename)

CPR_filename = 'next_D_flights.csv'
D_after_flights = read_flights_comma(CPR_filename)

D_before_flights.sort(key=itemgetter(1))
D_flights.sort(key=itemgetter(1))
D_after_flights.sort(key=itemgetter(1))

out_filename = 'Sorted_flight_previous_D.csv'
try:
    os.remove(out_filename)
except OSError:
    pass
write_sorted_flight(out_filename, D_before_flights)

out_filename = 'Sorted_flight_D.csv'
try:
    os.remove(out_filename)
except OSError:
    pass
write_sorted_flight(out_filename, D_flights)

out_filename = 'Sorted_flight_next_D.csv'
try:
    os.remove(out_filename)
except OSError:
    pass
write_sorted_flight(out_filename, D_after_flights)
