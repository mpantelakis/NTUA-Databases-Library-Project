from flask import Flask, render_template, request, flash, redirect, url_for, abort, session
from flask_mysqldb import MySQL
from library import db
from library.login.forms import LoginForm
from library.login import login

@login.route("/login", methods=["GET", "POST"])
def user_login():
    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        user = form.__dict__

        print(user['username'].data)
        query_approved = "SELECT approved FROM library_user WHERE username='{}';".format(user['username'].data)
        query_student = "SELECT COUNT(*) FROM student, library_user WHERE library_user.username=student.username AND library_user.username='{}' AND password='{}';".format(user['username'].data, user['password'].data)
        query_professor = "SELECT COUNT(*) FROM professor, library_user WHERE library_user.username=professor.username AND library_user.username='{}' AND password='{}';".format(user['username'].data, user['password'].data)
        query_operator = "SELECT COUNT(*) FROM library_operator, library_user, professor WHERE library_user.username=professor.username AND library_operator.prof_id=professor.prof_id  AND library_user.username='{}' AND password='{}';".format(user['username'].data, user['password'].data)
        query_admin = "SELECT COUNT(*) FROM admin WHERE admin_username='{}' AND password='{}';".format(user['username'].data, user['password'].data)
        query_wrong_credentials = "SELECT COUNT(*) FROM library_user WHERE username='{}' AND password='{}';".format(user['username'].data, user['password'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query_admin)
            result_admin = cur.fetchone()[0]
            cur.close()
            if result_admin > 0:
                flash("Logged in successfully", "success")
                return redirect("/admin_page")
            cur = db.connection.cursor()
            cur.execute(query_wrong_credentials)
            result_wrong_credentials = cur.fetchone()[0]
            cur.close()
            print("Result Wrong Credentials:", result_wrong_credentials)
            if result_wrong_credentials == 0:
                flash("Wrong credentials.", "warning")
                return render_template("login.html", pageTitle="Log in", form=form, home_name="Home", home_page="/")
            cur = db.connection.cursor()
            cur.execute(query_approved)
            result_approved = cur.fetchone()[0]
            print("Result Approved:", result_approved)
            cur = db.connection.cursor()
            cur.execute(query_student)
            result_student = cur.fetchone()[0]
            print("Result Student:", result_student)
            cur.execute(query_professor)
            result_professor = cur.fetchone()[0]
            print("Result Professor:", result_professor)
            cur.execute(query_operator)
            result_operator = cur.fetchone()[0]
            print("Result Operator:", result_operator)
            cur.close()


            if result_approved == 0:
                flash("You haven't been approved yet.", "warning")
            elif result_student > 0:
                session["username"] = user["username"].data
                flash("Logged in successfully", "success")
                return redirect("/user/home_page")
            elif result_operator > 0:
                session["username"] = user["username"].data
                flash("Logged in successfully", "success")
                return redirect("/operator_page")
            elif result_professor > 0:
                session["username"] = user["username"].data
                flash("Logged in successfully", "success")
                return redirect("/user/home_page")
        except Exception as e:
            flash(str(e), "danger")
            redirect("/")

    return render_template("login.html", pageTitle="Log in", form=form, home_name="Home", home_page="/")
