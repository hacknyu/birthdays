import csv
from dateutil.parser import parse
from datetime import date

def parse_csv(filename):
    output = [['Last Name', 'First Name', 'Email', 'Date of Birth', 'Normalized Date of Birth']]

    with open(filename, 'r') as csv_file:
        reader = csv.reader(csv_file)

        row_count = 1
        errors = []
        column_names = next(reader)

        # print(column_names)

        dob_index = column_names.index('Date of Birth')
        # lastname_index = column_names.index('Last Name')
        lastname_index = 0
        firstname_index = column_names.index('First Name')
        email_index = column_names.index('Email')

        for index, line in enumerate(reader):
            date_string = line[dob_index]
            lastname = line[lastname_index]
            firstname = line[firstname_index]
            email = line[email_index]
            output_row = [lastname, firstname, email, date_string]

            normalized_dob = ''

            try:
                normalized_dob = parse(date_string).date()
                print(str(index + 2) + ': ' + str(normalized_dob))

                if not(normalized_dob.year <= 2004 and normalized_dob.year >= 1970):
                    raise ValueError('Outside expected date range.')
            except ValueError as err:
                errors.append((index + 2, date_string))
                print(err)

                normalized_dob = 'ERROR: ' + str(err)

            output_row.append(normalized_dob)
            output.append(output_row)

            row_count += 1

        print(str(row_count) + ' rows')
        print(str(len(errors)) + ' errors')
        print(errors)

    return output


def get_under_18(all_rows, event):
    """
    Get all under 18 for the day of the event,
    and also anybody who had an irregular birthday input
    """
    under_18 = [['Last Name', 'First Name', 'Email', 'Date of Birth', 'Normalized Date of Birth']]

    n_dob_index = all_rows[0].index('Normalized Date of Birth')
    youngest_dob = date(year=event.year - 18, month=event.month, day=event.day)

    for row in all_rows[1:]:
        n_dob = row[n_dob_index]

        try:
            if (n_dob - youngest_dob).days > 0:
                under_18.append(row)

        except TypeError:
            under_18.append(row)

    return under_18


def write_csv(filename, output):
    with open(filename, 'w') as csv_file:
        writer = csv.writer(csv_file)

        for row in output:
            writer.writerow(row)

output = parse_csv('hacknyu-03-09-2018.csv')
write_csv('hacknyu-03-09-2018-birthdays.csv', output)
write_csv('hacknyu-03-09-2018-minors.csv', get_under_18(output, date(2018, 3, 23)))
