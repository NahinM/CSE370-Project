import mysql.connector

def get_id(table,val):
    sql = f"select id from {table} where name='{val}'"
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=3307)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    ret = mycursor.fetchall()
    mydb.close()
    print(ret)
    return ret[0][0]

# results = qq("SELECT id from mainCategory where name='aaa'")
def getNextId(table):
    mydb = mysql.connector.connect(host="localhost",user="nahin",password="123456",database = "ktms",port = 3307)
    sql = f"select max(id) from {table}"
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    ret = mycursor.fetchall()
    mydb.close()
    print(ret)
    n = ret[0][0]
    if n: return n+1
    return 1

# send = results[0]
print(get_id("subcategory","xq"))

