import mysql.connector

def connect_to(dbName,sql):
    mydb = mysql.connector.connect(
    host="localhost",
    user="nahin",
    password="123456",
    database = dbName,
    port = 3307
    )

    cursor = mydb.cursor()
    cursor.execute(sql)
    return cursor.fetchall()

results = connect_to("ktms","SELECT title,type,siteLink,description,createdAt,updatedAt,mainCategory,subCategory FROM assets where id ='2'")

send = results[0]
print(send)

