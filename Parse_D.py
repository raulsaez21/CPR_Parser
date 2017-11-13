import csv
import sys
import os


def parse_file(CPR_filename, SO6_filename_f):

    try:
        os.remove(SO6_filename_f)
    except OSError:
        pass

    TACT_ID_search = str(351269)  # The TactId is always a number of 6 digits, 1234567 is nto a possible number
    TACT_ID_search = 'EXS16PV'

    with open(CPR_filename, 'rb') as CPR_file:
        reader = csv.reader(CPR_file, delimiter=';', lineterminator='\n')
        try:
            for row in reader:
                TACT_ID = row[1]
                TACT_ID = row[8]

                if TACT_ID == TACT_ID_search:
                    with open(SO6_filename_f, 'a') as SO6_file:
                        writer = csv.writer(SO6_file)
                        line_SO6 = [row]
                        writer.writerow(line_SO6)

        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (CPR_filename, reader.line_num, e))

    CPR_file.close()
    SO6_file.close()

    print 'File parsed'


# Main
filename = '1.201607271001tacop104ARCHIVED_OPLOG_ALL_CPR'
SO6_filename = 'example_SO6_2.csv'

parse_file(filename, SO6_filename)
