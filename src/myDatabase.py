import mysql.connector

def getNextId(table:str):
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=3307)
    sql = f"select max(id) from {table}"
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    ret = mycursor.fetchall()
    mydb.close()
    n = ret[0][0]
    if n: return n+1
    return 1

def get_id(table:str,val:str):
    sql = f"select id from {table} where name='{val}'"
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=3307)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    ret = mycursor.fetchall()
    mydb.close()
    return ret[0][0]

def insert_to(table:str,val:tuple):
    sql = f"INSERT INTO {table} VALUES({" ,".join(["%s"]*len(val))})"
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=3307)
    mycursor = mydb.cursor()
    mycursor.execute(sql,val)
    mydb.commit()
    mydb.close()


def count_forname(table,name):
    sql = f"select count(*) from {table} where name='{name}'"
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=3307)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    ret = mycursor.fetchone()
    mydb.close()
    return ret[0]

def get_all(table,val):
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=3307)
    sql = f"select {val} from {table}"
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    ret = mycursor.fetchall()
    mydb.close()
    return ret

def check_insert(table,lst:list):
    for item in lst:
        if item=="": continue
        if count_forname(table,item)==0: insert_to(table,(getNextId(table),item.strip()))

def asset_filter(q:str,main:list,sub:list,genre:list,byUser=None):
    sql = f"SELECT DISTINCT a.id,a.title,a.description,a.type,a.siteLink,a.contentlink FROM"
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
    if byUser: sql += f", (SELECT DISTINCT(asset_id) FROM uploaded_by where user_id='{byUser}') u"
    sql += " WHERE a.id=m.asset_id AND a.id=s.asset_id AND a.id=g.asset_id"
    if byUser: sql+= " AND u.asset_id=a.id"
    if q: sql += f" and a.title like '%{q.upper()}%'"
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=3307)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    send = [dict(id=str(i),title=str(tl),description=str(d),contentsrc=cl,typp=str(tp),visite=str(l),detail=f"/detail?id={i}") for i,tl,d,tp,l,cl in mycursor.fetchall()]
    mydb.close()
    return send

def asset_filter_bookmarked(q:str,main:list,sub:list,genre:list,byUser=None):
    sql = f"SELECT DISTINCT a.id,a.title,a.description,a.type,a.siteLink,a.contentlink FROM"
    sql += " assets a,"
    filtering = ""
    if main: filtering = f" and m.name in ({','.join([f"'{x}'" for x in main])})"
    sql += f" (SELECT DISTINCT(r.asset_id) FROM asset_mainctg r, maincategory m where r.main_id=m.id{filtering}) m,"
    filtering = ""
    if sub: filtering = f" and s.name in ({','.join([f"'{x}'" for x in sub])})"
    sql += f" (SELECT DISTINCT(r.asset_id) FROM asset_subctg r, subcategory s where r.sub_id=s.id{filtering}) s,"
    filtering = ""
    if genre: filtering = f" and g.name in ({','.join([f"'{x}'" for x in genre])})"
    sql+= f" (SELECT DISTINCT(r.asset_id) FROM asset_genre r, genre g where r.genre_id=g.id{filtering}) g,"
    sql += f" (SELECT DISTINCT(asset_id) FROM bookmark where user_id='{byUser}') b"
    sql += " WHERE a.id=m.asset_id AND a.id=s.asset_id AND a.id=g.asset_id AND a.id=b.asset_id"
    if q: sql += f" and a.title like '%{q.upper()}%'"
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=3307)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    send = [dict(id=str(i),title=str(tl),description=str(d),contentsrc=cl,typp=str(tp),visite=str(l),detail=f"/detail?id={i}") for i,tl,d,tp,l,cl in mycursor.fetchall()]
    mydb.close()
    return send

def del_asset_relation(table,name):
    pass

def update_asset():
    pass

def del_asset(id):
    sql = f"delete from assets where id={id}"
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=3307)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()

def if_bookmarked(asset_id,user_id):
    sql = f"select count(*) from bookmark where asset_id={asset_id} and user_id='{user_id}'"
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=3307)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    ret = mycursor.fetchone()
    mydb.close()
    return ret[0]>0

def make_bookmark(asset_id,user_id):
    if if_bookmarked(asset_id,user_id): return
    sql = f"insert into bookmark values('{user_id}', {asset_id})"
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=3307)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()

def del_bookmark(asset_id,user_id):
    if not if_bookmarked(asset_id,user_id): return
    sql = f"delete from bookmark where asset_id={asset_id} and user_id='{user_id}'"
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=3307)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()