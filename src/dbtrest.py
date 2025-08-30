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

results = connect_to("ktms","select id,password from users where id = 'aaa'")
print(results)

