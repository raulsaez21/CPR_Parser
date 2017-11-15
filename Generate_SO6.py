import csv
import sys
import os
import re


def build_SO6_line(CPR_line, CPR_previous_line, index):

    time=re.sub("[^0-9]", "", CPR_line[2][-8:])
    previous_time = re.sub("[^0-9]", "", CPR_previous_line[2][-8:])

    date = re.sub("[^0-9]", "", CPR_line[2][:8])
    date= date[-2:] + date[2:4] + date[:2]
    previous_date = re.sub("[^0-9]", "", CPR_previous_line[2][:8])
    previous_date = previous_date[-2:] + previous_date[2:4] + previous_date[:2]

    Aircraft_Model=''

    if index == 0:
        SO6_line = ['%s_!00%d' % (CPR_line[9], index), CPR_line[9], CPR_line[10], Aircraft_Model, CPR_previous_line[13], CPR_line[13], previous_time, time]
    else:
        SO6_line = ['!00%d_!00%d' % (index-1, index), CPR_line[9], CPR_line[10], Aircraft_Model, CPR_previous_line[13], CPR_line[13], previous_time, time]
    return SO6_line


def read_flights(filename):
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

# Check how the flight_index works in order to print the segments names.
def write_SO6_flights(flights):

    TACT_ID_old = 1234567
    flight_index = 1

    for i in range(0, len(flights)):
        TACT_ID = flights[i][1]

        if TACT_ID != TACT_ID_old:
            flight_index = 0
            TACT_ID_old = TACT_ID
            continue

        with open(SO6_filename, 'a') as SO6_file:
            writer = csv.writer(SO6_file)
            line_SO6 = build_SO6_line(flights[i], flights[i-1], flight_index)
            writer.writerow(line_SO6)
            flight_index = flight_index + 1

        TACT_ID_old = TACT_ID

    SO6_file.close()
    print 'SO6 file created'
    return


# Main
CPR_filename = 'CPR_D.csv'
CPR_filename = 'test.txt'
CPR_flights = read_flights(CPR_filename)
SO6_filename = 'SO6_flights.csv'

try:
    os.remove(SO6_filename)
except OSError:
    pass

write_SO6_flights(CPR_flights)
