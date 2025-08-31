from flask import Flask,request,render_template,jsonify,session,redirect,url_for
import mysql.connector,datetime

mydb = mysql.connector.connect(
host="localhost",
user="root",
password="",
database = "ktms",
port=3307
)


app = Flask(__name__)
nav_items = [("Home","/"),("Assets","/assets"),("Collection","/collections"),("Upload","/upload"),("Saved","/saved"),("Recent","/recent")]

# Flask.secret_key
app.secret_key = b'_5wqdsyht#y2L"Fd4Q8z\n\xec]/'

@app.route("/")
def home():
    if "username" in session:
        return render_template("home.html" , navItems = nav_items, profile = session["username"])
    return render_template("home.html" , navItems = nav_items, profile = None)

@app.route("/login" , methods=['GET', 'POST'])
def login():
    bgImg = 'https://images.pexels.com/photos/443446/pexels-photo-443446.jpeg'
    if request.method == 'POST':
        id = request.form['id']
        pswd = request.form['pass']
        sql = f"SELECT id,password from users where id='{id}'"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        ret = mycursor.fetchall()
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
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        ret = mycursor.fetchall()
        if len(ret)!=0: return render_template("signup.html" , backimage = bgImg ,navItems = nav_items , msg = "username already taken!")
    
        sql = f"INSERT INTO users VALUES (%s, %s, %s, %s, %s)"
        val = (id,passd,fname,lname,email)
        mycursor.execute(sql,val)
        mydb.commit()

        session['username'] = id
        return redirect('/')
    return render_template("signup.html" , backimage = bgImg ,navItems = nav_items ,msg = None)

@app.route("/assets")
def assets():
    return render_template("assets.html",navItems = nav_items)

@app.route("/detail")
def detail():
    bgImg = "https://images.pexels.com/photos/15727975/pexels-photo-15727975.jpeg"
    id = request.args.get('id')
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT title,type,siteLink,description,createdAt,updatedAt,mainCategory,subCategory FROM assets where id ='{id}'")
    ret = mycursor.fetchall()
    if len(ret)==0: render_template("detail.html",backimage = bgImg,navItems = nav_items, getDetail = None)

    d = ret[0]
    return render_template("detail.html",backimage = bgImg,navItems = nav_items, getDetail = d, profile=session["username"])

@app.route("/saved")
def saved():
    if "username" in session:
        return render_template("saved.html",navItems = nav_items, profile=session["username"])
    return "page not found"

@app.route("/upload" , methods=['GET', 'POST'])
def uploads():
    bgImg = 'https://images.pexels.com/photos/443446/pexels-photo-443446.jpeg'

    if request.method == "POST":
        title = request.form["title"]
        des = request.form["description"]
        site = request.form["site"]
        main = request.form["mainCategory"]
        sub = request.form["subCategory"]
        d = datetime.datetime.now().strftime("%Y-%m-%d")
        typ = request.form["type"]

        sql = "select max(id) from assets"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        id,ret = 1,mycursor.fetchall()[0][0]
        if ret: id += int(ret)
        sql = f"INSERT INTO assets VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (id,title,des,site,d,d,main,sub,typ)
        mycursor.execute(sql,val)
        mydb.commit()

        sql = "insert into uploaded_by values(%s, %s)"
        mycursor.execute(sql,(session["username"],id))
        mydb.commit()
        return redirect("/upload")
    return render_template("uploads.html",backimage = bgImg, navItems = nav_items,profile=session["username"])

@app.route('/search')
def search():
    f = request.args.get('f')
    if f=="search":
        q = request.args.get('q')
        if q:
            mycursor = mydb.cursor()
            mycursor.execute("SELECT title FROM assets WHERE title LIKE %s",("%"+q+"%",))
            send = [dict(title=str(t[0])) for t in mycursor.fetchall()]
            return jsonify(send if send else [dict(title="not available!")])
        else:
            return jsonify([])
        
    if f=="asset":
        main = request.args.get('main')
        sub = request.args.get('sub')

        sql = "SELECT id,title,description,type,siteLink FROM assets"
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        send = [dict(id=str(i),title=str(tl),description=str(d),typp=str(tp),visite=str(l),detail=f"/detail?id={i}") for i,tl,d,tp,l in mycursor.fetchall()]
        return jsonify(send)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))