import re

import pyodbc

import create_tables_for_mssql


def insert_to_club(connection, cursor, city, name):
    sql = "select club_id from Clubs where club_city='{}' and club_name='{}'".format(city, name)
    club_id = cursor.execute(sql
        ).fetchone()
    if club_id:
        pass
    else:
        cursor.execute("insert into Clubs(club_city,club_name) values('{}','{}')".format(city, name),)
        club_id = cursor.execute("select @@IDENTITY").fetchone()
    return club_id[0]


def insert_to_swimmer(connection, cursor, last_name, first_name, year_of_birth, club_id):
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
        swimmer_id = cursor.execute("select @@IDENTITY").fetchone()
    return swimmer_id[0]


def insert_to_results(connection, cursor, swimmer_id, discipline_id, place, result_time):
    cursor.execute(
        "insert into Results(swimmer_id, discipline_id, place, result_time) values({},{},{},'{}')".format(
            swimmer_id, discipline_id, place, result_time))


def insert_to_disciplines(connection, cursor, distance, style, sex, comp_year):
    sql = "select discipline_id from Disciplines \
        where distance={} and style='{}' and sex='{}' and comp_year={}".format(
            distance, style, sex, comp_year)
    discipline_id = cursor.execute(sql).fetchone()
    if discipline_id:
        pass
    else:
        sql = "insert into Disciplines(distance, style, sex, comp_year) values({},'{}','{}',{})".format(
                distance, style, sex, comp_year)
        cursor.execute(sql
            )
        discipline_id = cursor.execute("select @@IDENTITY").fetchone()
    return discipline_id[0]


def main():
    path_to_xls = './resources/Competition1.xls'

    connection = pyodbc.connect('''Driver=Microsoft Excel Driver (*.xls);Dbq={};'''.format(path_to_xls))
    cur = connection.cursor()
    # connection = pyodbc.connect(
    #     '''DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;CHARSET=UTF8;UID=SA;PWD=E3fxsfDY;DATABASE=EXAMPLE2''')
    # cur = connection.cursor()
    # create_tables_for_mssql.create_tables(connection, cur)
    # club_id = insert_to_club(connection, cur, 'Саша3', 'Пучек3')
    # file = open(path_to_csv, encoding='utf-8')
    # parts = re.split(',' * 8, file.read())
    #
    # for part in parts:
    #     results = part.split('\n')
    #     if len(results) < 9:
    #         continue
    #     else:
    #         distance = ''
    #         style = ''
    #         sex = ''
    #         comp_year = ''
    #         match = re.findall(r',\w.+,,,,,,,', part)
    #
    #         if match:
    #             results = re.split(r',\w.+,,,,,,,', part)[1].split('\n')
    #             discipline = match[0].split(',')[1].split(' ')
    #
    #             distance = discipline[0]
    #             style = discipline[1]
    #             sex = discipline[2]
    #             comp_year = discipline[3]
    #             discipline_id = insert_to_disciplines(connection, cur, distance, style, sex, comp_year)
    #
    #         for result in results:
    #             if result == '' or result.split(',')[0] == '' or result == '\n':
    #                 continue
    #             record = result.split(',')
    #
    #             if len(record) == 10:
    #                 record.insert(5, '')
    #
    #             place = record[0].split('.')[0]
    #             last_name = record[1].split(' ')[0]
    #             first_name = record[1].split(' ')[1]
    #             year_of_birth = record[2].split('.')[0]
    #             club_city = record[4].replace('"', '')
    #             club_name = record[5].replace('"', '')
    #             time = record[6] + ',' + record[7]
    #             time = time.replace('"', '')
    #
    #             club_id = insert_to_club(connection, cur, club_city, club_name)
    #             swimmer_id = insert_to_swimmer(connection, cur, last_name, first_name, year_of_birth, club_id)
    #             insert_to_results(connection, cur, swimmer_id, discipline_id, place, time)
    #
    #             print('{} {} {} {} {} {} {} {} {} {} {}'.format(place, last_name,
    #                                                             first_name, year_of_birth,
    #                                                             club_city, club_name,
    #                                                             time, distance, style,
    #                                                             sex, comp_year))
    #         connection.commit()

    connection.close()
    # file.close()


main()
print('End...')
