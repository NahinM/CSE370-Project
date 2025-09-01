import mysql.connector

def getNextId(table):
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=3307)
    sql = f"select max(id) from {table}"
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    ret = mycursor.fetchall()
    mydb.close()
    n = ret[0][0]
    if n: return n+1
    return 1

def get_id(table,val):
    sql = f"select id from {table} where name='{val}'"
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=3307)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    ret = mycursor.fetchall()
    mydb.close()
    return ret[0][0]

def insert_to(table:str,val:tuple):
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=3307)
    sql = f"INSERT INTO {table} VALUES({" ,".join(["%s"]*len(val))})"
    mycursor = mydb.cursor()
    mycursor.execute(sql,val)
    mydb.commit()
    mydb.close()

def get_all(table,val):
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=3307)
    sql = f"select {val} from {table}"
    mycursor = mydb.cursor()
    ret = mycursor.execute(sql)
    mydb.close()
    return ret

def check_insert(table,lst:list):
    vals = get_all(table,"name")
    for item in lst:
        if vals==None: insert_to(table,(getNextId(table),item.strip()))
        elif item not in vals: insert_to(table,(getNextId(table),item.strip()))

def filter(main:list,sub:list,genre:list):
    sql = f"SELECT a.id,a.title FROM"
    sql += " assets a,"
    filtering = ""
    if main: filtering = f" and m.name in ({','.join([f"'{x}'" for x in main])})"
    sql += f" (SELECT DISTINCT(r.asset_id) FROM asset_mainctg r, maincategory m where r.main_id=m.id{filtering}) m,"
    filtering = ""
    if sub: filtering = f" and s.name in ({','.join([f"'{x}'" for x in sub])})"
    sql += f" (SELECT DISTINCT(r.asset_id) FROM asset_subctg r, subcategory s where r.sub_id=s.id{filtering}) s,"
    filtering = ""
    if genre: filtering = f" and g.name in ({','.join([f"'{x}'" for x in genre])})"
    sql+= f" (SELECT DISTINCT(r.asset_id) FROM asset_genre r, genre g where r.genre_id=g.id{filtering}) g"
    sql += " WHERE a.id=m.asset_id AND a.id=s.asset_id AND a.id=g.asset_id"
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=3307)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    ret = mycursor.fetchall()
    mydb.close()
    return ret