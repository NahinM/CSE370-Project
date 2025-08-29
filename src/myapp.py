from flask import Flask,request,render_template,jsonify,session,redirect,url_for

# Flask.secret_key

app = Flask(__name__)
nav_items = [("Home","/"),("Assets","/assets"),("Collection","/collections"),("Uploads","/uploads"),("Saved","/saved"),("Recent","/recent")]

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def home():
    if "username" in session:
        return render_template("home.html" , navItems = nav_items, profile = "Nahin")
    return render_template("home.html" , navItems = nav_items, profile = None)

@app.route("/login" , methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect('/')
    return render_template("login.html", backimage = 'https://images.pexels.com/photos/443446/pexels-photo-443446.jpeg',navItems = nav_items)

@app.route("/signup")
def signup():
    return render_template("signup.html" , backimage = 'https://images.pexels.com/photos/443446/pexels-photo-443446.jpeg' ,navItems = nav_items)

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