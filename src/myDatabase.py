import mysql.connector

PORT = 3307

def sql_get(sql:str):
    global PORT
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=PORT)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    ret = mycursor.fetchall()
    mydb.close()
    return ret

def sql_run(sql:str):
    global PORT
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=PORT)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()

def getNextId(table:str):
    global PORT
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=PORT)
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
    global PORT
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=PORT)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    ret = mycursor.fetchone()
    mydb.close()
    if ret: return ret[0]
    return None

def insert_to(table:str,val:tuple):
    sql = f"INSERT INTO {table} VALUES({" ,".join(["%s"]*len(val))})"
    global PORT
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=PORT)
    mycursor = mydb.cursor()
    mycursor.execute(sql,val)
    mydb.commit()
    mydb.close()


def count_forname(table:str,name:str):
    sql = f"select count(*) from {table} where name='{name}'"
    global PORT
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=PORT)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    ret = mycursor.fetchone()
    mydb.close()
    return ret[0]

def get_all(table:str,val:str):
    global PORT
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=PORT)
    sql = f"select {val} from {table}"
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    ret = mycursor.fetchall()
    mydb.close()
    return ret

def insert_unique(table:str,name:str):
    name = name.strip()
    if name and count_forname(table,name)==0: insert_to(table,(getNextId(table),name.strip()))

def check_insert(table,lst:list):
    for item in lst: insert_unique(table,item)

def asset_filter(q:str,main:list,sub:list,genre:list,byUser=None,offset=0,user=None):
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
    sql += f" Limit 20 Offset {offset}"
    global PORT
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=PORT)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    send = [dict(id=str(i),title=str(tl),description=str(d),contentsrc=cl,typp=str(tp),visite=str(l),detail=f"/detail?id={i}",marked=if_bookmarked(i,user)) for i,tl,d,tp,l,cl in mycursor.fetchall()]
    mydb.close()
    return send

def asset_filter_bookmarked(q:str,main:list,sub:list,genre:list,byUser=None,offset=0):
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
    sql += f" Limit 20 Offset {offset}"
    global PORT
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=PORT)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    send = [dict(id=str(i),title=str(tl),description=str(d),contentsrc=cl,typp=str(tp),visite=str(l),detail=f"/detail?id={i}") for i,tl,d,tp,l,cl in mycursor.fetchall()]
    mydb.close()
    return send

def del_asset_relation(typp:str,asset_id:str,r_id:str):
    r_table,search = "",""
    if typp=="genre":r_table,search = "asset_genre","genre_id"
    elif typp=="main": r_table,search = "asset_mainctg","main_id"
    elif typp=="sub": r_table,search = "asset_subctg","sub_id"
    else: return
    sql = f"delete from {r_table} where asset_id={asset_id} and {search}={r_id}"
    global PORT
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=PORT)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()

def add_relation(typp:str,asset_id:str,name:str):
    table,r_table = "",""
    if typp=="genre": table,r_table = "genre","asset_genre"
    elif typp=="main": table,r_table = "maincategory","asset_mainctg"
    elif typp=="sub": table,r_table = "subcategory","asset_subctg"
    else: return
    insert_unique(table,name)
    insert_to(r_table,(asset_id,str(get_id(table,name))))

def del_asset(id:str):
    sql = f"delete from assets where id={id}"
    global PORT
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=PORT)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()

def if_bookmarked(asset_id:str,user_id:str):
    if asset_id==None or user_id==None: return False
    sql = f"select count(*) from bookmark where asset_id={asset_id} and user_id='{user_id}'"
    global PORT
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=PORT)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    ret = mycursor.fetchone()
    mydb.close()
    return ret[0]>0

def make_bookmark(asset_id:str,user_id:str):
    if if_bookmarked(asset_id,user_id): return
    sql = f"insert into bookmark values('{user_id}', {asset_id})"
    global PORT
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=PORT)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()

def del_bookmark(asset_id:str,user_id:str):
    if not if_bookmarked(asset_id,user_id): return
    sql = f"delete from bookmark where asset_id={asset_id} and user_id='{user_id}'"
    global PORT
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=PORT)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    mydb.close()