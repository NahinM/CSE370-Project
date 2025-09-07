from flask import Flask,request,render_template,jsonify,session,redirect,url_for
import mysql.connector,datetime
from myDatabase import *

# to run app
# flask --app myapp --debug run

app = Flask(__name__)
nav_items = [("Home","/"),("Assets","/assets"),("Upload","/upload"),("Bookmarked","/mybookmarks")]

# Flask.secret_key
app.secret_key = b'_5wqdsyht#y2L"Fd4Q8z\n\xec]/'

@app.route("/")
def home():
    if "username" in session:
        return render_template("home.html" , navItems = nav_items, profile = session["username"],Footer=True)
    return render_template("home.html" , navItems = nav_items, profile = None,Footer=True)

@app.route("/login" , methods=['GET', 'POST'])
def login():
    
    bgImg = 'https://images.pexels.com/photos/443446/pexels-photo-443446.jpeg'
    if request.method == 'POST':
        id = request.form['id']
        pswd = request.form['pass']
        sql = f"SELECT id,password from users where id='{id}'"
        ret = sql_get(sql)
        if len(ret)==0: return render_template("login.html", backimage = bgImg,navItems = nav_items, message = ("username not found",None))
        db_id,db_pswd = ret[0]
        if db_pswd!=pswd: return render_template("login.html", backimage = bgImg,navItems = nav_items, message = (None,"password incorrect"))

        session['username'] = id
        return redirect('/')
    return render_template("login.html", backimage = bgImg,navItems = nav_items, message = (None,None))

@app.route("/signup" , methods=['GET', 'POST'])
def signup():
    bgImg = 'https://images.pexels.com/photos/443446/pexels-photo-443446.jpeg'

    if request.method == 'POST':
        id = request.form["id"]
        passd = request.form["pass"]
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]

        sql = f"SELECT id,password from users where id='{id}'"
        ret = sql_get(sql)
        if len(ret)!=0: return render_template("signup.html" , backimage = bgImg ,navItems = nav_items , msg = "username already taken!")
    
        insert_to("users",(id,passd,fname,lname,email))

        session['username'] = id
        return redirect('/')
    return render_template("signup.html" , backimage = bgImg ,navItems = nav_items ,msg = None)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route("/myprofile")
def myprofile():
    id = session["username"]
    global PORT
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=PORT)
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT id,fname,lname,email from users where id='{id}'")
    ret = mycursor.fetchall()
    mydb.close()
    return render_template("profile.html", profile=session["username"], getDetail = ret[0],Footer=True)


@app.route("/upload" , methods=['GET', 'POST'])
def uploads():

    if request.method == "POST":
        title = request.form["title"]
        site = request.form["site"]
        clink = request.form["clink"]
        des = request.form["description"]
        typ = request.form["type"]
        main = str(request.form["main"]).split(",")
        sub = str(request.form["sub"]).split(",")
        g = str(request.form["genre"]).split(",")
        d = datetime.datetime.now().strftime("%Y-%m-%d")

        # all ids
        user_id = session["username"]
        asset_id = getNextId("assets")
        # return jsonify([title,site,des,typ,main,sub,g,d])

        # insert to
        # asset (id,title,description,siteLink,createdAt,updatedAt,type)
        insert_to("assets",(asset_id,title,des,site,clink,d,d,typ))
        # uploaded_by (user_id,asset_id)
        insert_to("uploaded_by",(user_id,asset_id))
        # mainCategory(id,name)
        check_insert("mainCategory",main)
        # subCategory(id,name)
        check_insert("subCategory",sub)
        # genre(id,name)
        check_insert("genre",g)
        # maintosub(main_id,sub_id)

        # asset_genre(asset_id,genre_id)
        for item in g: insert_to("asset_genre",(asset_id,get_id("genre",item)))
        # asset_mainctg(asset_id,main_id)
        for item in main: insert_to("asset_mainctg",(asset_id,get_id("maincategory",item)))
        # asset_subctg(asset_id,sub_id)
        for item in sub: insert_to("asset_subctg",(asset_id,get_id("subcategory",item)))
    
    if "username" not in session: return redirect("/login")
    return render_template("upload.html", navItems = nav_items,profile=session["username"])



@app.route("/assets")
def assets():
    prf = None
    if "username" in session: prf = session["username"]
    return render_template("assets.html",navItems = nav_items, profile=prf,Footer=True)

@app.route("/bookmark")
def bookmark():
    if "username" in session:
        asset_id = request.args.get("id")
        q = request.args.get('q')
        if q == "add":
            make_bookmark(asset_id,session["username"])
            return "remove"
        elif q=="remove":
            del_bookmark(asset_id,session["username"])
            return "add"
    else: return redirect('/login')

@app.route('/mybookmarks')
def mybookmarks():
    if "username" not in session: return redirect('/login')
    return render_template("bookmark.html", navItems = nav_items, profile=session["username"],Footer=True)



@app.route("/myupload")
def myupload():
    prf = None
    if "username" in session:
        prf = session["username"]
        return render_template("myuploads.html",navItems = nav_items, profile=prf,Footer=True)
    return redirect('/login')

@app.route("/detail")
def detail():
    if "username" not in session: return redirect('/login')
    bgImg = "https://images.pexels.com/photos/15727975/pexels-photo-15727975.jpeg"
    id = request.args.get('id')
    global PORT
    mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=PORT)
    mycursor = mydb.cursor()
    sql = f"select title,type,siteLink,description,createdAt,updatedAt,id,contentlink from assets where id={id}"
    mycursor.execute(sql)
    getAsset = mycursor.fetchone()
    sql = f"select g.name from genre g, asset_genre r where r.asset_id={id} and g.id=r.genre_id"
    mycursor.execute(sql)
    getGenre = mycursor.fetchall()
    sql = f"select m.name from maincategory m, asset_mainctg r where r.asset_id={id} and r.main_id=m.id"
    mycursor.execute(sql)
    getMain = mycursor.fetchall()
    sql = f"select s.name from subcategory s, asset_subctg r where r.asset_id={id} and r.sub_id=s.id"
    mycursor.execute(sql)
    getSub = mycursor.fetchall()
    sql = f"select user_id from uploaded_by where asset_id={id}"
    mycursor.execute(sql)
    getUser = mycursor.fetchone()
    mydb.close()
    if len(getAsset)==0: render_template("detail.html",backimage = bgImg,navItems = nav_items, getDetail = None, profile = session["username"])

    return render_template("detail.html",backimage = bgImg,navItems = nav_items, getDetail = dict(asset=getAsset,genre=getGenre,main=getMain,sub=getSub,owner=getUser,bookmark=if_bookmarked(id,session["username"])), profile=session["username"])

@app.route('/editasset')
def eidt_asset():
    if "username" not in session: return redirect('/login')
    id = request.args.get('id')
    return render_template("editasset.html",navItems = nav_items, profile = session["username"], a_id=id)

@app.route('/search')
def search():
    f = request.args.get('f')
    if f=="search":
        q = request.args.get('q')
        if q:
            global PORT
            mydb = mysql.connector.connect(host="localhost",user="root",password="",database = "ktms",port=PORT)
            mycursor = mydb.cursor()
            mycursor.execute("SELECT id,title FROM assets WHERE title LIKE %s",("%"+q+"%",))
            send = [dict(detail=f"/detail?id={i}",title=str(t)) for i,t in mycursor.fetchall()]
            mydb.close()
            return jsonify(send if send else [dict(title="not available!")])
        else:
            return jsonify([])
        
    if f=="asset":
        main = request.args.get('main')
        sub = request.args.get('sub')
        g = request.args.get('genre')
        q = request.args.get('q')
        u = request.args.get('user')
        page = request.args.get('page')
        if u=="": u=None
        if q=="": q = None
        if main: main = [x for x in main.split(",") if x!=""]
        else : main = None
        if sub: sub = [x for x in sub.split(",") if x!=""]
        else : sub = None
        if g: g = [x for x in g.split(",") if x!=""]
        else : g = None
        user = None
        if "username" in session: user=session["username"]
        offset = 0
        if page: offset= 20*(int(page)-1)
        return jsonify(asset_filter(q,main,sub,g,u,offset,user))
    
    if f=="bookmark":
        main = request.args.get('main')
        sub = request.args.get('sub')
        g = request.args.get('genre')
        q = request.args.get('q')
        u = request.args.get('user')
        page = request.args.get('page')
        if u=="": u=None
        if q=="": q = None
        if main: main = [x for x in main.split(",") if x!=""]
        else : main = None
        if sub: sub = [x for x in sub.split(",") if x!=""]
        else : sub = None
        if g: g = [x for x in g.split(",") if x!=""]
        else : g = None
        offset = 0
        if page: offset = (int(page)-1)*20
        return jsonify(asset_filter_bookmarked(q,main,sub,g,u,offset))
    
    if f=="offcanvas":
        main = request.args.get('main')
        if main: main = [x for x in main.split(",") if x!=""]
        else : main = None
        g = [dict(id=i,name=n,selected=False) for i,n in get_all("genre","id,name")]
        m = [dict(id=i,name=n,selected=False) for i,n in get_all("maincategory","id,name")]
        s = [dict(id=i,name=n,selected=False) for i,n in get_all("subcategory","id,name")]
        return dict(genre=g,main=m,sub=s)
    
    if f=="singleasset":
        id = request.args.get('id')
        a_ret = sql_get(f"select id,title,description,sitelink,contentlink from assets where id={id}")
        g_sql = f"select g.id,g.name from genre g, (select distinct genre_id from asset_genre where asset_id={id}) r where g.id=r.genre_id"
        m_sql = f"select m.id,m.name from maincategory m, (select distinct main_id from asset_mainctg where asset_id={id}) r where m.id=r.main_id"
        s_sql = f"select s.id,s.name from subcategory s, (select distinct sub_id from asset_subctg where asset_id={id}) r where s.id=r.sub_id"
        return jsonify({
                "asset": [dict(id=i,title=tl,description=des,site=sln,content=cln) for i,tl,des,sln,cln in a_ret][0],
                "genre": [dict(id=i,name=n) for i,n in sql_get(g_sql)],
                "main" : [dict(id=i,name=n) for i,n in sql_get(m_sql)],
                "sub": [dict(id=i,name=n) for i,n in sql_get(s_sql)]
        })
    
@app.route('/delete' , methods=['GET', 'POST'])
def delete_from():
    if "username" not in session: return redirect('/')
    t = request.args.get('type')
    a_id = request.args.get('assetid')
    if t=="asset":
        del_asset(a_id)
        return redirect('/assets')
    elif t in ["genre","main","sub"]:
        r_id = request.args.get('relid')
        del_asset_relation(t,a_id,r_id)
        return f"deleted from {t}"
    else: return "Page not found"


@app.route('/update' ,  methods=['GET', 'POST'])
def update():
    if request.method == "POST":
        id = request.form['id']
        title = request.form['title']
        des = request.form['description']
        site = request.form['site']
        content = request.form['content']
        d = datetime.datetime.now().strftime("%Y-%m-%d")
        sql_run(f"update assets set title='{title}', description='{des}', siteLink='{site}', contentlink='{content}', updatedAt='{d}' where id={id}")
        return "asset info updated"
    t = request.args.get('type')
    a_id = request.args.get('assetid')
    if t in ["genre","main","sub"]:
        name = request.args.get("name")
        add_relation(t,a_id,name)
        return f"name: {name} added for {t}"
    else: return "Page not found"