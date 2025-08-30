from flask import Flask,request,render_template,jsonify,session,redirect,url_for
import mysql.connector

mydb = mysql.connector.connect(
host="localhost",
user="nahin",
password="123456",
database = "ktms"
)


app = Flask(__name__)
nav_items = [("Home","/"),("Assets","/assets"),("Collection","/collections"),("Uploads","/uploads"),("Saved","/saved"),("Recent","/recent")]

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
        cursor = mydb.cursor()
        cursor.execute(sql)
        ret = cursor.fetchall()
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
        cursor = mydb.cursor()
        cursor.execute(sql)
        ret = cursor.fetchall()
        if len(ret)!=0: return render_template("signup.html" , backimage = bgImg ,navItems = nav_items , msg = "username already taken!")
    
        sql = f"INSERT INTO users VALUES (%s, %s, %s, %s, %s)"
        val = (id,passd,fname,lname,email)
        cursor = mydb.cursor()
        cursor.execute(sql,val)
        mydb.commit()

        session['username'] = id
        return redirect('/')
    return render_template("signup.html" , backimage = bgImg ,navItems = nav_items ,msg = None)

@app.route("/assets")
def assets():
    return render_template("assets.html",navItems = nav_items)

@app.route("/saved")
def saved():
    return render_template("saved.html",navItems = nav_items)

@app.route("/uploads")
def uploads():
    return render_template("uploads.html",navItems = nav_items)

@app.route('/search')
def search():
    q = request.args.get('q')
    if q:
        # mycursor.execute("SELECT * FROM accounts WHERE name LIKE %s",("%"+q+"%",))
        # send = [dict(user=u,name=n,email=e,age=a,pswd=p) for u,n,e,a,p in mycursor.fetchall()]
        send = [dict(name=f"Somting{i}",id=i) for i in range(10)]
        return jsonify(send)
    else:
        return jsonify([])

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('home'))