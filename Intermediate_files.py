import csv
import sys
import os


def parse_file(CPR_filename, Intermediate_filename, list_flights, selector):
    try:
        os.remove(Intermediate_filename)
    except OSError:
        pass

    TACT_ID_old = str(1234567)  # The TactId is always a number of 6 digits, 1234567 is not a possible number
    start = True

    if selector:
        with open(CPR_filename, 'rb') as CPR_file:
            reader = csv.reader(CPR_file, delimiter=';', lineterminator='\n')
            try:
                for row in reader:
                    TACT_ID = row[1]

                    if TACT_ID != TACT_ID_old and not start:
                        with open(Intermediate_filename, 'a') as SO6_file:
                            writer = csv.writer(SO6_file)
                            line_SO6 = [TACT_ID_old, start_index, end_index]
                            writer.writerow(line_SO6)
                            #list_flights.append(TACT_ID_old)
                            list_flights.append(line_SO6)
                        start_index = row[0]
                    elif start:
                        start_index = row[0]
                        start = False

                    TACT_ID_old = TACT_ID
                    end_index = row[0]

            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (CPR_filename, reader.line_num, e))

            # Last field
            with open(Intermediate_filename, 'a') as SO6_file:
                writer = csv.writer(SO6_file)
                line_SO6 = [TACT_ID_old, start_index, end_index]
                writer.writerow(line_SO6)
                #list_flights.append(TACT_ID_old)
                list_flights.append(line_SO6)

    CPR_file.close()
    SO6_file.close()

    print 'File parsed'
    return list_flights


def filter_flights(list_flights_other_D, filename, D_TACT_ID):
    filtered_flight_indexes = []
    for i in range(0, len(list_flights_other_D)):
        if list_flights_other_D[i][0] in D_TACT_ID and list_flights_other_D[i][0] != '':
            with open(filename, 'a') as SO6_file:
                writer = csv.writer(SO6_file)
                line_SO6 = list_flights_other_D[i]
                writer.writerow(line_SO6)
                filtered_flight_indexes.append(line_SO6)
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
select_flights_D = True
list_flights_D = []
D_TACT_ID = []
in_filename = '1.201607281001tacop104ARCHIVED_OPLOG_ALL_CPR'
out_filename = 'file_2.csv'
try:
    os.remove(out_filename)
except OSError:
    pass
list_flights_D = parse_file(in_filename, out_filename, list_flights_D, select_flights_D)
for s in range(0, len(list_flights_D)):     # Extract TACT_ID of each flight to do the filter
    D_TACT_ID.append(list_flights_D[s][0])  # to the starting or ending indexes (in order to avoid problems with starting and ending indexes equal

list_flights_D_before = []
select_flights_D = True
in_filename = '1.201607271001tacop104ARCHIVED_OPLOG_ALL_CPR'
out_filename = 'file_1.csv'
try:
    os.remove(out_filename)
except OSError:
    pass
list_flights_D_before = parse_file(in_filename, out_filename, list_flights_D_before, select_flights_D)

list_flights_D_after = []
in_filename = '1.201607291001tacop104ARCHIVED_OPLOG_ALL_CPR'
out_filename = 'file_3.csv'
try:
    os.remove(out_filename)
except OSError:
    pass
list_flights_D_after = parse_file(in_filename, out_filename, list_flights_D_after, select_flights_D)


#Filtering D-1 and D+1 flights and creating the corresponding flights; first the indexes and then the flights
filename = 'previous_D_indexes.csv'
filtered_indexes_previous_D = []
try:
    os.remove(filename)
except OSError:
    pass
filtered_indexes_previous_D = filter_flights(list_flights_D_before, filename, D_TACT_ID)

filename = 'next_D_indexes.csv'
filtered_indexes_next_D = []
try:
    os.remove(filename)
except OSError:
    pass
filtered_indexes_next_D =filter_flights(list_flights_D_after, filename, D_TACT_ID)


list_flights_D_before = []
list_flights_D_after = []



#Reading the file and filter the list obtained with the flights
input_filename = '1.201607271001tacop104ARCHIVED_OPLOG_ALL_CPR'
raw_flights = read_flights(input_filename)
output_filename = 'previous_D_flights.csv'
try:
    os.remove(output_filename)
except OSError:
    pass
filter_flights_files(filtered_indexes_previous_D, output_filename, raw_flights)

raw_flights = []
input_filename = '1.201607291001tacop104ARCHIVED_OPLOG_ALL_CPR'
raw_flights = read_flights(input_filename)
output_filename = 'next_D_flights.csv'
try:
    os.remove(output_filename)
except OSError:
    pass
filter_flights_files(filtered_indexes_next_D, output_filename, raw_flights)



#Creating new intermediate files with the new indexes (after the flights have been filtered) --> check if it is necessary



