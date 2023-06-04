from flask import Flask, render_template, request, flash, redirect, url_for, abort, session
from flask_mysqldb import MySQL
from library import db ## initially created by __init__.py, needs to be used here
from library.users import users

@users.route("/user/home_page")
def user_index():
    if "username" in session:
        username = session["username"]
        query="SELECT school_name FROM library_user WHERE username='{}';".format(username)
        try:
                cur = db.connection.cursor()
                cur.execute(query)
                school_name = cur.fetchone()
                cur.close()
                return render_template("user_page.html", pageTitle = "Welcome to the Library of {}".format(school_name[0]),home_name="Home",condition="student")
        except Exception as e: ## OperationalError
            flash(str(e), "danger")


@users.route("/user")
def getUserInfo():
    """
    Retrieve user from the database
    """
    if "username" in session:
        username = session["username"]
    print(username)
    query_student = "SELECT COUNT(*) FROM student, library_user WHERE library_user.username=student.username AND library_user.username='{}';".format(username)
    query_professor = "SELECT COUNT(*) FROM professor, library_user WHERE library_user.username=professor.username AND library_user.username='{}';".format(username)
    query_operator = "SELECT COUNT(*) FROM library_operator, library_user, professor WHERE library_user.username=professor.username AND lib_op_id=professor.prof_id AND library_user.username='{}';".format(username)
    query_admin = "SELECT COUNT(*) FROM admin WHERE admin_username='{}';".format(username)
        
    try:
        cur = db.connection.cursor()
        cur.execute(query_student)
        result_student = cur.fetchone()[0]
        cur.execute(query_professor)
        result_professor = cur.fetchone()[0]
        cur.execute(query_operator)
        result_operator = cur.fetchone()[0]
        cur.execute(query_admin)
        result_admin = cur.fetchone()[0]
        cur.close()

        if result_student > 0:
            condition="student"
            condition1="student"
        elif result_professor > 0:
            condition="professor"
        elif result_operator > 0:
            condition="operator"
        elif result_admin > 0:
            condition="admin"
        print(condition)
        cur = db.connection.cursor()
        query = "SELECT username,password,first_name,last_name,birth_date,age,email,phone_number,school_name FROM library_user WHERE username=%s;"
        cur.execute(query, (username,))
        column_names = [i[0] for i in cur.description]
        information = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        print(information[0])
        return render_template("account.html", pageTitle="Account Information", home_name="Home", information=information, condition=condition)
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/user")

@users.route("/users")
def getUsers():
    """
    Retrieve users from the database
    """
    if "username" in session:
        username = session["username"]

        query_student = "SELECT COUNT(*) FROM student, library_user WHERE library_user.username=student.username AND library_user.username='{}';".format(username)
        query_professor = "SELECT COUNT(*) FROM professor, library_user WHERE library_user.username=professor.username AND library_user.username='{}';".format(username)
        query_operator = "SELECT COUNT(*) FROM library_operator, library_user, professor WHERE library_user.username=professor.username AND library_operator.prof_id=professor.prof_id  AND library_user.username='{}';".format(username)
        query_admin = "SELECT COUNT(*) FROM admin WHERE admin_username='{}';".format(username)
        
    try:
        cur = db.connection.cursor()
        cur.execute(query_student)
        result_student = cur.fetchone()[0]
        cur.execute(query_professor)
        result_professor = cur.fetchone()[0]
        cur.execute(query_operator)
        result_operator = cur.fetchone()[0]
        cur.execute(query_admin)
        result_admin = cur.fetchone()[0]
        cur.close()

        if result_student > 0:
            condition="student"
        elif result_operator > 0:
            condition="operator"
        elif result_professor > 0:
            condition="professor"
        elif result_admin > 0:
            condition="admin"

        cur = db.connection.cursor()
        query = "SELECT username,first_name,last_name,birth_date,age,email,phone_number, CASE WHEN username IN (SELECT username FROM student) THEN 'Student' ELSE 'Professor' END AS role FROM library_user  WHERE school_name=(SELECT school_name FROM library_user WHERE username=%s) AND approved=true;"
        cur.execute(query, (username,))
        column_names = [i[0] for i in cur.description]
        users = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("library_users.html", pageTitle="Library Users", home_name="Home", users=users, condition=condition)
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/operator_page")

@users.route("/users/for_approval")
def for_approval_Users():
    """
    Retrieve users from the database
    """
    if "username" in session:
        username = session["username"]

        query_student = "SELECT COUNT(*) FROM student, library_user WHERE library_user.username=student.username AND library_user.username='{}';".format(username)
        query_professor = "SELECT COUNT(*) FROM professor, library_user WHERE library_user.username=professor.username AND library_user.username='{}';".format(username)
        query_operator = "SELECT COUNT(*) FROM library_operator, library_user, professor WHERE library_user.username=professor.username AND library_operator.prof_id=professor.prof_id  AND library_user.username='{}';".format(username)
        query_admin = "SELECT COUNT(*) FROM admin WHERE admin_username='{}';".format(username)
        
    try:
        cur = db.connection.cursor()
        cur.execute(query_student)
        result_student = cur.fetchone()[0]
        cur.execute(query_professor)
        result_professor = cur.fetchone()[0]
        cur.execute(query_operator)
        result_operator = cur.fetchone()[0]
        cur.execute(query_admin)
        result_admin = cur.fetchone()[0]
        cur.close()

        if result_student > 0:
            condition="student"
        elif result_operator > 0:
            condition="operator"
        elif result_professor > 0:
            condition="professor"
        elif result_admin > 0:
            condition="admin"

    
        cur = db.connection.cursor()
        query = "SELECT username,first_name,last_name,birth_date,age,email,phone_number, CASE WHEN username IN (SELECT username FROM student) THEN 'Student' ELSE 'Professor' END AS role FROM library_user  WHERE school_name=(SELECT school_name FROM library_user WHERE username=%s) AND approved=false;"
        cur.execute(query, (username,))
        column_names = [i[0] for i in cur.description]
        users = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("users_for_approval.html", pageTitle="Library Users for Approval", home_name="Home", users=users, condition=condition)
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/operator_page")


@users.route("/users/search")
def searchUser():
    """
    Search user in database
    """
    if "username" in session:
        username = session["username"]
    search = request.args.get("search")
    query_student = "SELECT COUNT(*) FROM student, library_user WHERE library_user.username=student.username AND library_user.username='{}';".format(username)
    query_professor = "SELECT COUNT(*) FROM professor, library_user WHERE library_user.username=professor.username AND library_user.username='{}';".format(username)
    query_operator = "SELECT COUNT(*) FROM library_operator, library_user, professor WHERE library_user.username=professor.username AND library_operator.prof_id=professor.prof_id  AND library_user.username='{}';".format(username)
    query_admin = "SELECT COUNT(*) FROM admin WHERE admin_username='{}';".format(username)
        
    cur = db.connection.cursor()
    cur.execute(query_student)
    result_student = cur.fetchone()[0]
    cur.execute(query_professor)
    result_professor = cur.fetchone()[0]
    cur.execute(query_operator)
    result_operator = cur.fetchone()[0]
    cur.execute(query_admin)
    result_admin = cur.fetchone()[0]
    cur.close()

    if result_student > 0:
        condition="student"
    elif result_operator > 0:
        condition="operator"
    elif result_professor > 0:
        condition="professor"
    elif result_admin > 0:
        condition="admin"
    try:
        cur = db.connection.cursor()
        query = "SELECT username, first_name, last_name,birth_date,age,email,phone_number, CASE WHEN username IN (SELECT username FROM student) THEN 'Student' ELSE 'Professor' END AS role FROM library_user WHERE first_name LIKE %s OR last_name LIKE %s OR CONCAT(first_name, ' ', last_name) LIKE %s AND approved=true;"
        cur.execute(query, (f"%{search}%", f"%{search}%", f"%{search}%",))
        column_names = [i[0] for i in cur.description]
        users = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("library_users.html", pageTitle="Library Users", home_name="Home", users=users, condition=condition)
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/users")



@users.route("/users/delete/<username>", methods = ["POST"])
def deleteUser(username):
    """
    Delete user by username from database
    """
    print(username)
    query = "DELETE FROM library_user WHERE username = %s;"
    try:
        cur = db.connection.cursor()
        cur.execute(query, (username,))
        db.connection.commit()
        cur.close()
        flash("User deleted successfully", "primary")
        return redirect("/users")
    except Exception as e:
        flash(str(e), "danger")

@users.route("/users/disapprove/<username>", methods = ["POST"])
def dissaproveUser(username):
    """
    Disapprove user by username from database
    """
    print(username)
    query = "DELETE FROM library_user WHERE username = %s;"
    try:
        cur = db.connection.cursor()
        cur.execute(query, (username,))
        db.connection.commit()
        cur.close()
        flash("User disapproved successfully", "primary")
        return redirect("/users/for_approval")
    except Exception as e:
        flash(str(e), "danger")

@users.route("/users/approve/<username>", methods = ["POST"])
def approveUser(username):
    """
    Approve user by username from database
    """
    print(username)
    query = "UPDATE library_user SET approved=true WHERE username=%s;"
    try:
        cur = db.connection.cursor()
        cur.execute(query, (username,))
        db.connection.commit()
        cur.close()
        flash("User approved successfully", "primary")
        return redirect("/users/for_approval")
    except Exception as e:
        flash(str(e), "danger")

@users.route("/users/disable/<username>", methods = ["POST"])
def disableUser(username):
    """
    Disable user by username from database
    """
    print(username)
    query = "UPDATE library_user SET approved=false WHERE username=%s;"
    try:
        cur = db.connection.cursor()
        cur.execute(query, (username,))
        db.connection.commit()
        cur.close()
        flash("User disabled successfully", "primary")
        return redirect("/users")
    except Exception as e:
        flash(str(e), "danger")

@users.route("/users/print/<username>")
def printUser(username):
    """
    Print user's library card
    """
    print(username)
    flash("User's library card printed successfully", "success")
    return redirect("/users")

@users.route("/users/change_password/<username>", methods = ["POST"])
def changePassword(username):
    """
    Change password by username from database
    """
    print(username)
    new_password = request.form.get('new_password')
    print(new_password)
    query = "UPDATE library_user SET password=%s WHERE username=%s;"
    try:
        cur = db.connection.cursor()
        cur.execute(query, (new_password,username,))
        db.connection.commit()
        cur.close()
        flash("Password changed successfully", "success")
        return redirect("/login")
    except Exception as e:
        flash(str(e), "danger")

@users.route("/users/edit/<username>/<password>", methods=["POST"])
def editAccount(username,password):
    """
    Change account information by username from the database
    """
    print(username)
    print(password)
    new_password = request.form.get('new_password')
    new_first_name = request.form.get('new_first_name')
    new_last_name = request.form.get('new_last_name')
    new_birth_date = request.form.get('new_birth_date')
    new_email = request.form.get('new_email')
    new_phone_number = request.form.get('new_phone_number')
    print(new_password)
    print(new_first_name)
    print(new_last_name)
    print(new_birth_date)
    print(new_email)
    print(new_phone_number)
    query = "UPDATE library_user SET password=%s, first_name=%s, last_name=%s, birth_date=%s, email=%s, phone_number=%s WHERE username=%s;"
    
    try:
        cur = db.connection.cursor()
        cur.execute(query, (new_password, new_first_name, new_last_name, new_birth_date, new_email, new_phone_number, username,))
        db.connection.commit()
        cur.close()
        if(new_password!=password):
            flash("Account information updated successfully", "success")
            return redirect ("/login")
        else:
            flash("Account information updated successfully", "success")
            return redirect("/user")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/user")
