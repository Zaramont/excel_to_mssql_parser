import pyodbc


def insert_to_club(cursor, city, name):
    sql = "select club_id from Clubs where club_city='{}' and club_name='{}'".format(
        city, name)
    club_id = cursor.execute(sql).fetchone()
    if club_id:
        pass
    else:
        cursor.execute(
            "insert into Clubs(club_city,club_name) values('{}','{}')".format(
                city, name), )
        club_id = cursor.execute("select @@IDENTITY").fetchone()
    return club_id[0]


def insert_to_swimmer(cursor, last_name, first_name, year_of_birth,
                      club_id):
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


def insert_to_results(cursor, swimmer_id, discipline_id, place,
                      result_time):
    cursor.execute(
        "insert into Results(swimmer_id, discipline_id, place, result_time) values({},{},{},'{}')".format(
            swimmer_id, discipline_id, place, result_time))


def insert_to_disciplines(cursor, distance, style, gender,
                          comp_year):
    sql = "select discipline_id from Disciplines \
        where distance={} and style='{}' and gender='{}' and comp_year={}".format(
        distance, style, gender, comp_year)
    discipline_id = cursor.execute(sql).fetchone()
    if discipline_id:
        pass
    else:
        sql = "insert into Disciplines(distance, style, gender, comp_year) values({},'{}','{}',{})".format(
            distance, style, gender, comp_year)
        cursor.execute(sql
                       )
        discipline_id = cursor.execute("select @@IDENTITY").fetchone()
    return discipline_id[0]


def main():
    path_to_xls = './resources/Competition1.xls'

    excel_connection = pyodbc.connect(
        '''Driver=Microsoft Excel Driver (*.xls);Dbq={};'''.format(path_to_xls),
        autocommit=True)
    excel_cur = excel_connection.cursor()
    rows = excel_cur.execute("select * from [Лист1$]").fetchall()
    excel_connection.close()

    connection = pyodbc.connect(
        '''DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;CHARSET=UTF8;UID=SA;PWD=E3fxsfDY;DATABASE=EXAMPLE''')
    cur = connection.cursor()
    discipline_id = 0
    for row in rows:
        arrayWithData = row

        if arrayWithData[0] != None:

            place = int(arrayWithData[0])
            last_name = arrayWithData[1].split(' ')[0]
            first_name = arrayWithData[1].split(' ')[1]
            year_of_birth = int(arrayWithData[2])

            if (len(arrayWithData[4].split(',')) == 2):

                club_city = arrayWithData[4].split(',')[0]
                club_name = arrayWithData[4].split(',')[1]
            else:
                club_city = arrayWithData[4].split(',')[0]
                club_name = ""
            result_time = arrayWithData[5]
            points = arrayWithData[8]

            club_id = insert_to_club(cur, club_city, club_name)
            swimmer_id = insert_to_swimmer(cur, last_name,
                                           first_name, year_of_birth, club_id)
            insert_to_results(cur, swimmer_id, discipline_id, place,
                              result_time)
            connection.commit()
        elif arrayWithData[1] != None:
            arr = arrayWithData[1].split(' ')
            arr = list(filter(None, arr))
            if (len(arr) < 4):
                continue
            distance = arr[0]
            style = arr[1]
            gender = arr[2]
            comp_year = arr[3]
            discipline_id = insert_to_disciplines(cur, distance,
                                                  style, gender, comp_year)

    connection.close()


main()
