import mysql.connector

def connect_to(dbName,sql):
    mydb = mysql.connector.connect(
    host="localhost",
    user="nahin",
    password="123456",
    database = dbName)

    cursor = mydb.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

results = connect_to("ktms","select max(id) from assets")
print(results[0][0])

