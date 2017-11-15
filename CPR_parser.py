########## This script is a CPR files parser; it reads a CPR file and outputs a .SO6 file #############
import csv
import sys
import os
from itertools import islice
import gc


# Functions definitions

# Read flight data from the flight one day before or after
def process_other_day(TACT_ID, SO6_filename, flights):

    found = False
    for h in range(0, len(flights)):
        if flights[h][1] == TACT_ID:
            found = True
            with open(SO6_filename, 'a') as SO6_file:
                writer = csv.writer(SO6_file)
                line_SO6 = build_SO6(flights[h])
                writer.writerow(line_SO6)

        if found and flights[h][1] != TACT_ID:
            break

    #index_flight = list.index(TACT_ID) if TACT_ID in list else -1
    #if index_flight != -1:

    return


# Building the line to be written in the SO6 output file
def build_SO6(CPR_row):
    # Segment Identifier, Origin of flight, Destination of flight, aircraft type, Time begin segment,
    # Time end segment, FL begin segment, FL end segment, Status, Call sign, Date begin segment, Date end segment,
    # Latitude begin segment, Longitude begin segment, Latitude end segment, Longitude end segment,
    # Flight identifier, Sequence, Segment length, Segment parity/color
    line_SO6_f = [CPR_row]

    return line_SO6_f


def read_index_file(filename):
    index_list = []

    with open(filename, 'rb') as index_file:
        reader = csv.reader(index_file, delimiter=',', lineterminator='\n')
        try:
            for row in reader:
                index_list.append(row[0])
                index_list.append(row[1])
                index_list.append(row[2])

        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (CPR_filename, reader.line_num, e))

    index_file.close()
    return index_list


def read_flights(filename):
    list_flights = []

    with open(filename, 'rb') as flights_file:
        reader = csv.reader(flights_file, delimiter=';', lineterminator='\n')
        try:
            for row in reader:
                # for row in islice(reader, 0, 100000):
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
                # for row in islice(reader, 0, 100000):
                list_flights.append(row)
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

    flights_file.close()
    print 'Flight stored to list'
    return list_flights


# Main
# Reading the TACT_IDs and ending indexes for the several files (check if it is necessary to create a new file
# with the new start and ending indexes)!!!!!!!

CPR_filename = 'Sorted_flight_previous_D.csv'
D_before_flights = read_flights_comma(CPR_filename)
CPR_filename = 'Sorted_flight_D.csv'
D_flights = read_flights_comma(CPR_filename)
CPR_filename = 'Sorted_flight_next_D.csv'
D_after_flights = read_flights_comma(CPR_filename)

# Main code
CPR_filename = '1.201607281001tacop104ARCHIVED_OPLOG_ALL_CPR'
SO6_filename = 'CPR_D.csv'

try:
    os.remove(SO6_filename)
except OSError:
    pass

n_flights = len(D_flights)
TACT_ID_old = 1234567
D_before = False
D_after = False

for i in range(0, n_flights):

    TACT_ID = D_flights[i][1]

    # Process D + 1 and print flight finished
    if TACT_ID != TACT_ID_old and D_before:
        for sublist in D_after_flights:
            if sublist[1] == TACT_ID:
                process_other_day(TACT_ID_old, SO6_filename, D_after_flights)
        D_after = True
    if TACT_ID != TACT_ID_old and not D_before:
        for sublist in D_before_flights: #Maybe remove this sublist thing and go to the file directly (or compute the index?)
            if sublist[1] == TACT_ID:
                process_other_day(TACT_ID, SO6_filename, D_before_flights)
        D_before = True
    # # Processing the day before if the TACT_ID is there
    # if TACT_ID in D_before_flights: # Create a list with only the TACT_ID located in D-1
    #     filename = '1.201607271001tacop104ARCHIVED_OPLOG_ALL_CPR'
    #     process_other_day(filename, TACT_ID, SO6_filename, list1, D_before_flights)

    if D_before and D_after:
        print "Flight %s finished" % TACT_ID_old
        # Write Data CPR D-1
        process_other_day(TACT_ID, SO6_filename, D_before_flights)
        D_after = False

    # Write data of the CPR D (current day)
    with open(SO6_filename, 'a') as SO6_file:
        writer = csv.writer(SO6_file)
        line_SO6 = build_SO6(D_flights[i])
        writer.writerow(line_SO6)

    TACT_ID_old = TACT_ID

    SO6_file.close()










# for i in range(1, n_flights):
#     with open(CPR_filename, 'rb') as CPR_file:
#         reader = csv.reader(CPR_file, delimiter=';', lineterminator='\n')
#         try:
#             start = int(list2[i * 3 - 2]) - 1
#             stop = int(list2[i * 3 - 1])
#             TACT_ID = 0
#
#             for row in islice(reader, start, stop):
#                 TACT_ID = row[1]
#
#                 # Write data of CPR D-1 (the day before)
#                 if not D_before:
#                     filename = '1.201607271001tacop104ARCHIVED_OPLOG_ALL_CPR'
#                     process_other_day(filename, TACT_ID, SO6_filename, list1)
#                     D_before = True
#
#                 # Write data of the CPR D (current day)
#                 with open(SO6_filename, 'a') as SO6_file:
#                     writer = csv.writer(SO6_file)
#                     line_SO6 = build_SO6(row)
#                     writer.writerow(line_SO6)
#
#                     # search_same_TACT_ID(TACT_ID)  #check if in the file D there is information with the same TACT_ID
#
#             # Process D + 1 and print flight finished
#             filename = '1.201607291001tacop104ARCHIVED_OPLOG_ALL_CPR'
#             process_other_day(filename, TACT_ID, SO6_filename, list3)
#             D_before = False
#             #print "Flight %s finished" % TACT_ID
#
#         except csv.Error as e:
#             sys.exit('file %s, line %d: %s' % (CPR_filename, reader.line_num, e))
#
#     CPR_file.close()
#     SO6_file.close()
