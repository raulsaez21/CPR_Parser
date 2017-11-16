import csv
import sys
import os


def find_indexes(CPR_filename, indexes):
    TACT_ID_old = str(1234567)  # The TactId is always a number of 6 digits, 1234567 is not a possible number
    start = True

    with open(CPR_filename, 'rb') as CPR_file:
        reader = csv.reader(CPR_file, delimiter=';', lineterminator='\n')

        for row in reader:
            TACT_ID = row[1]

            if TACT_ID != TACT_ID_old and not start:
                index_element = [TACT_ID_old, start_index, end_index]
                indexes.append(index_element)
                start_index = row[0]
            elif start:
                start_index = row[0]
                start = False

            TACT_ID_old = TACT_ID
            end_index = row[0]

        # Last field
        flight = [TACT_ID_old, start_index, end_index]
        indexes.append(flight)

    CPR_file.close()

    print 'File parsed'
    return indexes


def filter_flights(list_flights_other_D, D_TACT_ID):
    filtered_flight_indexes = []
    for i in range(0, len(list_flights_other_D)):
        if list_flights_other_D[i][0] in D_TACT_ID and list_flights_other_D[i][0] != '':
            flight = list_flights_other_D[i]
            filtered_flight_indexes.append(flight)
    print 'File with indexes created'
    return filtered_flight_indexes


def filter_flights_files(indexes, output_filename, flights):
    stop = len(indexes)
    for j in range(0, stop):
        init = int(indexes[j][1]) - 1
        end = int(indexes[j][2])
        for t in range(init, end):
            with open(output_filename, 'a') as SO6_file:
                writer = csv.writer(SO6_file)
                line_SO6 = flights[t]
                writer.writerow(line_SO6)

    print 'Filtered flight created'
    return


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
    print 'Flight to filter stored to list'
    return list_flights


# Main
# Read flight files and find the several blocks with the starting and ending indexes
selector = 1

if selector == 0:
    previous_D_filename = '1.201607271001tacop104ARCHIVED_OPLOG_ALL_CPR'
    D_filename = '1.201607281001tacop104ARCHIVED_OPLOG_ALL_CPR'
    next_D_filename = '1.201607291001tacop104ARCHIVED_OPLOG_ALL_CPR'
else:
    previous_D_filename ='1.201702191001tacop304ARCHIVED_OPLOG_ALL_CPR'
    D_filename = '1.201702201001tacop304ARCHIVED_OPLOG_ALL_CPR'
    next_D_filename = '1.201702211001tacop304ARCHIVED_OPLOG_ALL_CPR'

indexes_D = []
D_TACT_ID = []
indexes_D = find_indexes(D_filename, indexes_D)
for s in range(0, len(indexes_D)):  # Extract TACT_ID of each flight to do the filter
    D_TACT_ID.append(indexes_D[s][
                         0])  # to the starting or ending indexes (in order to avoid problems with starting and ending indexes equal

indexes_previous_D = []
indexes_previous_D = find_indexes(previous_D_filename, indexes_previous_D)

indexes_next_D = []
indexes_next_D = find_indexes(next_D_filename, indexes_next_D)

# Filtering D-1 and D+1 flights and creating the corresponding flights; first the indexes and then the flights
# The indexes are found by comparing the TACT_ID with the flights of day D
filtered_indexes_previous_D = []
filtered_indexes_previous_D = filter_flights(indexes_previous_D, D_TACT_ID)

filtered_indexes_next_D = []
filtered_indexes_next_D = filter_flights(indexes_next_D, D_TACT_ID)

list_flights_D_before = []
list_flights_D_after = []

# Reading the file and filter the list obtained with the flights
raw_flights = read_flights(previous_D_filename)
output_filename = 'previous_D_flights.csv'
try:
    os.remove(output_filename)
except OSError:
    pass
filter_flights_files(filtered_indexes_previous_D, output_filename, raw_flights)

raw_flights = []
raw_flights = read_flights(next_D_filename)
output_filename = 'next_D_flights.csv'
try:
    os.remove(output_filename)
except OSError:
    pass
filter_flights_files(filtered_indexes_next_D, output_filename, raw_flights)

# Creating new intermediate files with the new indexes (after the flights have been filtered) --> check if it is necessary
