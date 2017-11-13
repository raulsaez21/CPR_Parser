########## This script is a CPR files parser; it reads a CPR file and outputs a .SO6 file #############
import csv
import sys
import os
from itertools import islice


# Functions definitions

# Read flight data from the flight one day before or after
def process_other_day(filename, TACT_ID, Day, SO6_filename):
    # D-1 case
    if Day == 0:
        flight_end = False
        found = False
        with open(filename, 'rb') as file_D:
            reader_d = csv.reader(file_D, delimiter=';', lineterminator='\n')
            try:
                while not flight_end:
                    for row_d in reader_d:
                        if row_d[1] == TACT_ID:
                            found = True
                            with open(SO6_filename, 'a') as SO6_file:
                                writer = csv.writer(SO6_file)
                                line_SO6 = build_SO6(row_d)
                                writer.writerow(line_SO6)
                        elif found and row_d[1] != TACT_ID:
                            flight_end = True

                    flight_end = True

            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (CPR_filename, reader.line_num, e))

    # D+1 case
    if Day == 1:
        flight_end = False
        found = False
        with open(filename, 'rb') as file_D:
            reader_d = csv.reader(file_D, delimiter=';', lineterminator='\n')
            try:
                while not flight_end:
                    for row_d in reader_d:
                        if row_d[1] == TACT_ID:
                            found = True
                            with open(SO6_filename, 'a') as SO6_file:
                                writer = csv.writer(SO6_file)
                                line_SO6 = build_SO6(row_d)
                                writer.writerow(line_SO6)
                        elif found and row_d[1] != TACT_ID:
                            flight_end = True

                    flight_end = True

            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (CPR_filename, reader.line_num, e))

    file_D.close()

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
        reader = csv.reader(CPR_file, delimiter=';', lineterminator='\n')
        try:
            for row in reader:
                index_list.append(row[0])
                index_list.append(row[1])

        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (CPR_filename, reader.line_num, e))

    index_file.close()

    return index_list



# Main

# Reading the TACT_IDs and ending indexes for the several files
filename_1 = 'file_1.txt'
filename_2 = 'file_2.txt'
filename_3 = 'file_3.txt'

list1 = read_index_file(filename_1)
list2 = read_index_file(filename_2)
list3 = read_index_file(filename_3)

CPR_filename = '1.201607281001tacop104ARCHIVED_OPLOG_ALL_CPR'
SO6_filename = 'example_SO6.csv'

try:
    os.remove(SO6_filename)
except OSError:
    pass

TACT_ID_old = 1234567  # The TactId is always a number of 6 digits, 1234567 is not a possible number
row_value = 0
D_before = False
D_after = False

for i in range(1, (len(list2) / 2) + 1):
    with open(CPR_filename, 'rb') as CPR_file:
        reader = csv.reader(CPR_file, delimiter=';', lineterminator='\n')
        try:
            for row in islice(reader, list2[i * 2 - 1] - 1, None):
                TACT_ID = row[1]
                #search_same_TACT_ID(TACT_ID)

                # Write data of CPR D+1 (the day after;of the previous TACT_ID)
                if TACT_ID != TACT_ID_old and D_before:
                    filename = '1.201607291001tacop104ARCHIVED_OPLOG_ALL_CPR'
                    Day = 1
                    process_other_day(filename, TACT_ID_old, Day, SO6_filename, list3)
                    D_after = True
                # Write data of CPR D-1 (the day before;of the current TACT_ID) --> just executed once
                elif TACT_ID != TACT_ID_old and not D_before:
                    filename = '1.201607271001tacop104ARCHIVED_OPLOG_ALL_CPR'
                    Day = 0
                    process_other_day(filename, TACT_ID, Day, SO6_filename, list1)
                    D_before = True

                # Determining whether a flight has finished or not and then reading the CPR D-1 of new flight
                if D_before and D_after:
                    print "Flight %s finished" % TACT_ID_old
                    filename = '1.201607271001tacop104ARCHIVED_OPLOG_ALL_CPR'
                    Day = 0
                    # Write Data CPR D-1
                    process_other_day(filename, TACT_ID, Day, SO6_filename)
                    D_after = False

                # Write data of the CPR D (current day)
                with open(SO6_filename, 'a') as SO6_file:
                    writer = csv.writer(SO6_file)
                    line_SO6 = build_SO6(row)
                    writer.writerow(line_SO6)

                TACT_ID_old = TACT_ID

        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (CPR_filename, reader.line_num, e))

    CPR_file.close()
    SO6_file.close()
