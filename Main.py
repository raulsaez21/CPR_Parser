########## This script is a CPR files parser; it reads a CPR file and outputs a .SO6 file #############

import csv
import sys
import os


# Functions definitions

# This function is used to read flight data from the flight before or after
def process_other_day(filename, TACT_ID, Day):
    SO6_filename = 'example_SO6.csv'

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
                                line_SO6 = [row_d]
                                writer.writerow(line_SO6)
                        elif found and row_d[1] != TACT_ID:
                            flight_end = True


            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (CPR_filename, reader.line_num, e))

    # D+1 case
    if Day == 1:
        flight_end = False
        with open(filename, 'rb') as file_D:
            reader_d = csv.reader(file_D, delimiter=';', lineterminator='\n')
            try:
                while not flight_end:
                    for row_d in reader_d:
                        if row_d[1] == TACT_ID:
                            if row_d[14] == 'End':
                                flight_end = True
                            with open(SO6_filename, 'a') as SO6_file:
                                writer = csv.writer(SO6_file)
                                line_SO6 = [row_d]
                                writer.writerow(line_SO6)

            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (CPR_filename, reader.line_num, e))

    file_D.close()
    SO6_file.close()


CPR_filename = '1.201607281001tacop104ARCHIVED_OPLOG_ALL_CPR'
# CPR_filename = 'example_CPR.txt'
SO6_filename = 'example_SO6.csv'

try:
    os.remove(SO6_filename)
except OSError:
    pass

TACT_ID_old = 1234567  # The TactId is always a number of 6 digits, like this we ensure this number is not possible
track_service_old = 'Start'
row_value = 0

with open(CPR_filename, 'rb') as CPR_file:
    reader = csv.reader(CPR_file, delimiter=';', lineterminator='\n')
    try:
        for row in reader:
            TACT_ID = row[1]
            track_service = row[14]

            if ((TACT_ID != TACT_ID_old) and (track_service == 'Continuing') and (track_service_old == 'End')) or (
                        track_service_old == 'Start'):
                filename = '1.201607271001tacop104ARCHIVED_OPLOG_ALL_CPR'
                Day = 0
                # read CPR D-1
                process_other_day(filename, TACT_ID, Day)

            elif (TACT_ID == TACT_ID_old) and (track_service == 'End'):
                print "Flight %s ends" % TACT_ID

            elif (TACT_ID != TACT_ID_old) and (track_service_old == 'Continuing'):
                filename = '1.201607291001tacop104ARCHIVED_OPLOG_ALL_CPR'
                Day = 1
                # Read CPR D+1
                process_other_day(filename, TACT_ID_old, Day)

            track_service_old = track_service
            TACT_ID_old = TACT_ID

            with open(SO6_filename, 'a') as SO6_file:
                writer = csv.writer(SO6_file)
                line_SO6 = [row]  # Up to row [22], and 20 fields for SO6
                writer.writerow(line_SO6)

    except csv.Error as e:
        sys.exit('file %s, line %d: %s' % (CPR_filename, reader.line_num, e))

CPR_file.close()
SO6_file.close()

# row[14] is Begin, Continuing or End
# from itertools import islice
# for row in islice(reader, skip_value, None):
