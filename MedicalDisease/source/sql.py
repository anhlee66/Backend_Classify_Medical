import mysql.connector as con
mydb = con.connect(
    host='localhost',
    user='root',
    password='0606'
)
mycusor = mydb.cursor()
# mycusor.execute('create database example')
mycusor.execute('show databases')
for x in mycusor:
    print(x)