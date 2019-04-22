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
                       style nvarchar(60) not null,
                       year_of_birth int not null
                       )''')
    connection.commit()