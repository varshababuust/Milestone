#Importing packages
from pymongo import MongoClient
import sqlite3

#Step1:Connect to MOngoDB cloud
connection_string=r"mongodb+srv://Varsha:Jyoti*123@cluster0.jglwy.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
try:
    client=MongoClient(connection_string)
    print("Connected to mongo atlas successful")

    #Connection to mongo cluster
    db=client['Assessment']

    #Access collection
    collection=db['movies']

    #Step 2:Fetch all details from mongo db
    movies=collection.find()

    #Connecting to Sqlite database(Local)
    connection=sqlite3.connect(r'local_movies.db')
    cursor=connection.cursor()
    print(cursor)

    #Creating movies table if does not exist
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT NOT NULL,
        Genre TEXT NOT NULL,
        Year INTEGER,
        Director TEXT,
        Rating REAL
        );
    '''
    # Execute the query to create the table
    cursor.execute(create_table_query)
    connection.commit()
    

    #Insert data from mongo DB to Sqlite
    for movie in movies:
        Title =movie.get('Title')
        Genre=movie.get('Genre')
        Year=movie.get('Year')
        Director=movie.get('Director')
        Rating=movie.get('Rating')
        
        #Insert into SQLITE
        cursor.execute(
            '''
            INSERT INTO movies(Title,Genre,Year,Director,Rating)
            VALUES(?,?,?,?,?)
            ''',(Title,Genre,Year,Director,Rating)
        )
    connection.commit()
    #Retrieve and display 3 rows of data from Sqlite 
    cursor.execute("SELECT * FROM movies LIMIT 3")
    rows=cursor.fetchall()
    #Print those rows
    for row in rows:
        print(row)
except Exception as e:
    print(e)
finally:
    connection.close()
    print("Data transaferred successfully")