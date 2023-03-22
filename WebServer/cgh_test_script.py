# import mysql.connector
import MySQLdb


db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                    #  user="cj",         # your username
                    #  passwd="your_password_here",  # your password
                     db="graphcrunch3"
                     )        # name of the data base

print(db)

from django.contrib.auth import get_user_model
User = get_user_model()
users = User.objects.all()

print(users)

if False:

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()

    # Use all the SQL you like
    cur.execute("SELECT * FROM user")
    # cur.execute("SELECT * FROM proc")

    # print all the first cell of all the rows
    for row in cur.fetchall():
        # print(row[0])
        print(row)

    db.close()