import csv
import sys
import os


def parse_file(CPR_filename, Intermediate_filename):
    try:
        os.remove(Intermediate_filename)
    except OSError:
        pass

    TACT_ID_old = str(1234567)  # The TactId is always a number of 6 digits, 1234567 is not a possible number
    start = True

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
                    start_index = row[0]
                elif start:
                    start_index = row[0]
                    start = False

                TACT_ID_old = TACT_ID
                end_index = row[0]

        except csv.Error as e:
            sys.exit('file %s, line %d: %s' % (CPR_filename, reader.line_num, e))

    CPR_file.close()
    SO6_file.close()

    print 'File parsed'


# Main
in_filename = '1.201607271001tacop104ARCHIVED_OPLOG_ALL_CPR'
out_filename = 'file_1.csv'
parse_file(in_filename, out_filename)

in_filename = '1.201607281001tacop104ARCHIVED_OPLOG_ALL_CPR'
out_filename = 'file_2.csv'
parse_file(in_filename, out_filename)

in_filename = '1.201607291001tacop104ARCHIVED_OPLOG_ALL_CPR'
out_filename = 'file_3.csv'
parse_file(in_filename, out_filename)