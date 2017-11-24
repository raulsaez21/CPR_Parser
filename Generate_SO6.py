import csv
import sys
import os
import re
import math



def compute_distance(lat, pre_lat, lon, pre_lon):

    R = 6371000  # Earth's radius in metres
    pre_lat = math.radians(float(pre_lat) / 60)
    lat = math.radians(float(lat) / 60)
    delta_lat = lat - pre_lat
    delta_lon = math.radians(float(lon) / 60 - float(pre_lon) / 60)

    a = math.sin(delta_lat / 2) * math.sin(delta_lat / 2) + math.cos(pre_lat) * math.cos(lat) * math.sin(delta_lon / 2) * math.sin(delta_lon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = ((R * c) / 1000) / 1.852        # Distance in Nautical Miles

    return distance


def build_SO6_line(CPR_line, CPR_previous_line, index, end):
    # Time and date
    time = re.sub("[^0-9]", "", CPR_line[2][-8:])
    previous_time = re.sub("[^0-9]", "", CPR_previous_line[2][-8:])

    date = re.sub("[^0-9]", "", CPR_line[2][:8])
    date = date[-2:] + date[2:4] + date[:2]
    previous_date = re.sub("[^0-9]", "", CPR_previous_line[2][:8])
    previous_date = previous_date[-2:] + previous_date[2:4] + previous_date[:2]

    # Aircraft Model
    Aircraft_Model = ''

    # Status
    Status = ''
    if CPR_previous_line[19] == 'LEVEL_FLIGHT':
        Status = '2'
    elif CPR_previous_line[19] == 'CLIMB':
        Status = '0'
    elif CPR_previous_line[19] == 'DESCEND':
        Status = '1'

    # Latitude and Longitude (6 decimals)
    if CPR_line[12] == 'Not_Geo_Point':
        Lat = ''
        Lon = ''
        previous_lat = ''
        previous_lon = ''
    else:
        Lat = CPR_line[12][:7]
        if Lat[-1:] == 'N':
            Lat = '%.6f' % (float(float(Lat[:2]) * 60 + float(Lat[2:4]) + float(Lat[4:6]) / 60))
        else:
            Lat = '%.6f' % (float(float(Lat[:2]) * 60 + float(Lat[2:4]) + float(Lat[4:6]) / 60) * -1)

        previous_lat = CPR_previous_line[12][:7]
        if previous_lat[-1:] == 'N':
            previous_lat = '%.6f' % (float(float(previous_lat[:2]) * 60 + float(previous_lat[2:4]) +
                                           float(previous_lat[4:6]) / 60))
        else:
            previous_lat = '%.6f' % (float(float(previous_lat[:2]) * 60 + float(previous_lat[2:4]) +
                                           float(previous_lat[4:6]) / 60) * -1)

        Lon = CPR_line[12][-8:]
        if Lon[-1:] == 'E':
            Lon = '%.6f' % (float(float(Lon[:3]) * 60 + float(Lon[3:5]) + float(Lon[5:7]) / 60))
        else:
            Lon = '%.6f' % (float(float(Lon[:3]) * 60 + float(Lon[3:5]) + float(Lon[5:7]) / 60) * -1)

        previous_lon = CPR_previous_line[12][-8:]
        if previous_lon[-1:] == 'E':
            previous_lon = '%.6f' % (float(float(previous_lon[:3]) * 60 + float(previous_lon[3:5]) +
                                           float(previous_lon[5:7]) / 60))
        else:
            previous_lon = '%.6f' % (float(float(previous_lon[:3]) * 60 + float(previous_lon[3:5]) +
                                           float(previous_lon[5:7]) / 60) * -1)

    # Flight Identifier
    flight_id = ''

    # Segment length (6 decimals)
    segment_length = compute_distance(Lat, previous_lat, Lon, previous_lon)
    segment_length = '%.6f' % segment_length

    #Generating the SO6 line
    # We have to check the issue with the origin and destination airport if we are actually there or not
    # (actually we are never there, always 3000 ft above or something like that) ;;; how to identify last segment
    if index == 0:
        #x = [x for x in airports if 'Hello' in x][0]

        SO6_line = ['%s_!%03d' % (CPR_line[9], index), CPR_line[9], CPR_line[10], Aircraft_Model, previous_time, time,
                    CPR_previous_line[13], CPR_line[13], Status, CPR_line[8], previous_date, date, previous_lat,
                    previous_lon, Lat, Lon, flight_id, str(index + 1), segment_length, '0']
    elif end:
        SO6_line = ['!%03d_%s' % (index, CPR_line[10]), CPR_line[9], CPR_line[10], Aircraft_Model, previous_time, time,
                    CPR_previous_line[13], CPR_line[13], Status, CPR_line[8], previous_date, date, previous_lat,
                    previous_lon, Lat, Lon, flight_id, str(index + 1), segment_length, '0']
    else:
        SO6_line = ['!%03d_!%03d' % (index - 1, index), CPR_line[9], CPR_line[10], Aircraft_Model, previous_time, time,
                    CPR_previous_line[13], CPR_line[13], Status, CPR_line[8], previous_date, date, previous_lat,
                    previous_lon, Lat, Lon, flight_id, str(index + 1), segment_length, '0']
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


def write_SO6_flights(flights):
    end= False
    TACT_ID_old = 1234567
    flight_index = 1

    for i in range(0, len(flights)):
        TACT_ID = flights[i][1]

        if TACT_ID != TACT_ID_old:
            flight_index = 0
            end = False
            print 'Flight %s converted' % TACT_ID
            TACT_ID_old = TACT_ID
            continue

        if i < (len(flights)):
            if (i+1) == len(flights):
                end = True
            elif flights[i+1][1] != TACT_ID:
                end = True

        with open(SO6_filename, 'a') as SO6_file:
            writer = csv.writer(SO6_file)
            line_SO6 = build_SO6_line(flights[i], flights[i - 1], flight_index, end)
            writer.writerow(line_SO6)
            flight_index = flight_index + 1

        TACT_ID_old = TACT_ID

    SO6_file.close()
    print 'SO6 file created'
    return

def read_airports(filename):
    list_airports = []

    with open(filename, 'rb') as airports_file:
        reader = csv.reader(airports_file, delimiter=',', lineterminator='\n')
        try:
            for row in reader:
                list_airports.append(row)
        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

        airports_file.close()
    print 'Airports stored to list'
    return list_airports


# Main
CPR_filename = 'CPR_D.csv'
CPR_filename = 'test.txt'
CPR_flights = read_flights(CPR_filename)

airports_filename = 'airports.csv'
airports = read_airports(airports_filename)





SO6_filename = 'SO6_flights.csv'

try:
    os.remove(SO6_filename)
except OSError:
    pass

write_SO6_flights(CPR_flights)
