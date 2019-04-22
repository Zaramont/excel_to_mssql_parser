import pyodbc
import to_csv_converter
import re
import create_for_mssql


def insert_club(connection, cursor, city, name):
    club_id = cursor.execute(
        "select club_id from Clubs where club_city='{}' and club_name='{}'".format(city, name)).fetchone()
    if club_id:
        pass
    else:
        cursor.execute("insert into Clubs(club_city,club_name) values('{}','{}')".format(city, name))
        club_id = cursor.execute("select @@IDENTITY").fetchone()
    return club_id[0]


def insert_swimmer(connection, cursor, last_name, first_name, year_of_birth, club_id):
    swimmer_id = cursor.execute(
        "select swimmer_id from Swimmers \
        where last_name='{}' and first_name='{}' and year_of_birth='{}' and club_id={}".format(
            last_name, first_name, year_of_birth, club_id)).fetchone()
    if swimmer_id:
        pass
    else:
        cursor.execute(
            "insert into Swimmers(last_name,first_name,year_of_birth,club_id) values('{}','{}','{}',{})".format(
                last_name, first_name, year_of_birth, club_id))
        swimmer_id = cursor.execute("select @@IDENTITY").fetchone()[0]
    return swimmer_id[0]


path_to_xls = './resources/Competition1.xls'
path_to_csv = './resources/Competition1.csv'
to_csv_converter.xls2csv(path_to_xls, path_to_csv)
connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;UID=SA;\
PWD=E3fxsfDY;DATABASE=EXAMPLE2')
cur = connection.cursor()
# create_for_mssql.create_tables(connection,cur)
# connection.close()
club_id = insert_club(connection, cur, 'Onix', 'Utki')
swimmer_id = insert_swimmer(connection,cur,'Alex','Puchek','1990',club_id)
file = open(path_to_csv, encoding='utf-8')
parts = re.split(',' * 8, file.read())
# parts.pop(0)
for part in parts:
    results = part.split('\n')
    if len(results) < 9:
        continue
    else:
        distance = ''
        style = ''
        sex = ''
        comp_year = ''
        match = re.findall(r',\w.+,,,,,,,', part)
        if match:
            results = re.split(r',\w.+,,,,,,,', part)[1].split('\n')
            temp = match[0].split(',')[1].split(' ')
            distance = temp[0]
            style = temp[1]
            sex = temp[2]
            comp_year = temp[3]
            # print(match[0])
        for result in results:
            if result == '' or result.split(',')[0] == '' or result == '\n':
                continue
            record = result.split(',')
            if len(record) == 10:
                record.insert(5, '')
            place = record[0].split('.')[0]
            last_name = record[1].split(' ')[0]
            first_name = record[1].split(' ')[1]
            year_of_birth = record[2].split('.')[0]
            club_city = record[4].replace('"', '')
            club_name = record[5].replace('"', '')
            time = record[6] + ',' + record[7]
            time = time.replace('"', '')

            print('{} {} {} {} {} {} {} {} {} {} {}'.format(place,
                                                            last_name,
                                                            first_name,
                                                            year_of_birth,
                                                            club_city,
                                                            club_name,
                                                            time, distance, style, sex, comp_year))

connection.close()
file.close()
