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

# def count_rec(table:str,val)

def get_all(table,val):
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=3307)
    sql = f"select {val} from {table}"
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    ret = mycursor.fetchall()
    mydb.close()
    return ret

def check_insert(table,lst:list):
    vals = get_all(table,"name")
    for item in lst:
        if item=="": continue
        if len(vals)==0: insert_to(table,(getNextId(table),item.strip()))
        if item not in vals: insert_to(table,(getNextId(table),item.strip()))

def asset_filter(q:str,main:list,sub:list,genre:list,byUser=None):
    sql = f"SELECT a.id,a.title,a.description,a.type,a.siteLink FROM"
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
    if byUser: sql += f", (SELECT asset_id FROM uploaded_by where user_id='{byUser}') u"
    sql += " WHERE a.id=m.asset_id AND a.id=s.asset_id AND a.id=g.asset_id"
    if byUser: sql+= " AND u.asset_id=a.id"
    if q: sql += f" and a.title like '%{q}%'"
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=3307)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    send = [dict(id=str(i),title=str(tl),description=str(d),typp=str(tp),visite=str(l),detail=f"/detail?id={i}") for i,tl,d,tp,l in mycursor.fetchall()]
    mydb.close()
    return send