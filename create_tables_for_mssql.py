def create_tables(connection,cursor):
    cursor.execute('''create table Clubs 
                       (club_id int identity primary key,
                       club_name nvarchar(60),
                       club_city  nvarchar(60) not null
                       )''')
    cursor.execute('''create table Swimmers 
                   (swimmer_id int identity primary key,
                   last_name nvarchar(60) not null,
                   first_name  nvarchar(60) not null,
                   year_of_birth int not null,
                   club_id int
                   FOREIGN KEY (club_id) REFERENCES Clubs(club_id)
                   )''')
    cursor.execute('''create table Disciplines 
                       (discipline_id int identity primary key,
                       distance int not null,
                       gender nvarchar(60),
                       style nvarchar(60) not null,
                       comp_year int not null
                       )''')
    cursor.execute('''create table Results 
                       (result_id int identity primary key,
                       place int not null,
                       result_time nvarchar(60) not null,
                       swimmer_id int,
                       discipline_id int
                       FOREIGN KEY (swimmer_id) REFERENCES Swimmers(swimmer_id),
                       FOREIGN KEY (discipline_id) REFERENCES Disciplines(discipline_id)
                       )''')
    connection.commit()