from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from library import db ## initially created by __init__.py, need to be used here
from library.signup.forms import SignupForm
from library.signup import signup
import pymysql.err


@signup.route("/signup", methods = ["GET", "POST"]) ## "GET" by default
def createUser():
    """
    Create new user in the database
    
    """
    form = SignupForm() ## This is an object of a class that inherits FlaskForm
    ## which in turn inherits Form from wtforms
    ## https://flask-wtf.readthedocs.io/en/0.15.x/api/#flask_wtf.FlaskForm
    ## https://wtforms.readthedocs.io/en/2.3.x/forms/#wtforms.form.Form
    ## If no form data is specified via the formdata parameter of Form
    ## (it isn't here) it will implicitly use flask.request.form and flask.request.files.
    ## So when this method is called because of a GET request, the request
    ## object's form field will not contain user input, whereas if the HTTP
    ## request type is POST, it will implicitly retrieve the data.
    ## https://flask-wtf.readthedocs.io/en/0.15.x/form/
    ## Alternatively, in the case of a POST request, the data could have between
    ## retrieved directly from the request object: request.form.get("key name")
    ## when the form is submitted
    cur = db.connection.cursor()
    cur.execute('SELECT school_name, school_name FROM school_unit;')
    form.school_name.choices = list(cur.fetchall())
    cur.execute("SELECT max(prof_id) FROM professor")
    max_prof_id = int(cur.fetchone()[0])
    cur.close()

    if(request.method == "POST" and form.validate_on_submit()):

        newUser = form.__dict__
        query1 = "INSERT INTO library_user (username, password, first_name, last_name, birth_date, email, phone_number, school_name) VALUES ('{}', '{}', '{}','{}', '{}', '{}','{}', '{}');".format(
            newUser['username'].data,newUser['password'].data,newUser['first_name'].data, newUser['last_name'].data,
            newUser['birth_date'].data, newUser['email'].data,newUser['phone_number'].data,newUser['school_name'].data)
        query2="INSERT INTO student (username) VALUES ('{}');".format(newUser['username'].data)
        query3="INSERT INTO professor (username) VALUES ('{}');".format(newUser['username'].data)
        query4="INSERT INTO library_operator (prof_id) VALUES ('{}');".format(max_prof_id+1)
        try:
            if newUser['library_operator'].data=="Yes" and newUser['user_type'].data=="Student" :
                flash("You cannot aply for Library Operator", "warning")
                return render_template("signup.html", pageTitle = "Create an account", form = form, home_name="Home", condition="landing")
            cur = db.connection.cursor()
            cur.execute(query1)
            if (newUser['user_type'].data=="Student"): cur.execute(query2)
            elif (newUser['user_type'].data=="Professor"): 
                cur.execute(query3)
                if (newUser['library_operator'].data=="Yes"):
                     cur.execute(query4)
                     
            db.connection.commit()
            cur.close()
            flash("Account created successfully! Though you have to wait for approval by your library operator", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")
            print(str(e))
    # else, response for GET request
    else:
        try:      
            return render_template("signup.html", pageTitle = "Create an account", form = form, home_name="Home", condition="landing")
        except Exception as e: ## OperationalError
            flash(str(e), "danger")
