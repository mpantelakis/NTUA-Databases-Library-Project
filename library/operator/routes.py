from flask import Flask, render_template, request, flash, redirect, url_for, abort,session
from flask_mysqldb import MySQL
from library import db ## initially created by __init__.py, needs to be used here
from library.operator import operator

@operator.route("/operator_page")
def operator_index():
    if "username" in session:
        username = session["username"]
        query="SELECT school_name FROM library_user WHERE username='{}';".format(username)
        try:
                cur = db.connection.cursor()
                cur.execute(query)
                school_name = cur.fetchone()
                cur.close()
                return render_template("operator_page.html", pageTitle = "Welcome to the Library of {}".format(school_name[0]),home_name="Home",condition="operator")
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

@operator.route("/operators")
def getOperators():
    """
    Retrieve operators from the database
    """
        
    try:

        cur = db.connection.cursor()
        query = "SELECT lib_op_id,library_user.username, library_user.first_name,last_name,birth_date,age,email,phone_number,school_name  FROM library_operator JOIN professor ON library_operator.prof_id=professor.prof_id JOIN library_user ON library_user.username=professor.username WHERE approved=true;"
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        operators = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("operators.html", pageTitle="Operators", home_name="Home", operators=operators, condition="admin")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/admin_page")
    
@operator.route("/operators/for_approval")
def getOperatorsforApproval():
    """
    Retrieve operators for approval from the database
    """
        
    try:

        cur = db.connection.cursor()
        query = "SELECT lib_op_id,library_user.username, library_user.first_name,last_name,birth_date,age,email,phone_number,school_name  FROM library_operator JOIN professor ON library_operator.prof_id=professor.prof_id JOIN library_user ON library_user.username=professor.username WHERE approved=false;"
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        operators = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("operators_for_approval.html", pageTitle="Operators for Approval", home_name="Home", operators=operators, condition="admin")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/admin_page")
    
@operator.route("/operators/search")
def searchOperator():
    """
    Search operator in database
    """
    search = request.args.get("search")
    try:
        cur = db.connection.cursor()
        query = "SELECT lib_op_id, library_user.username, first_name, last_name,birth_date,age,email,phone_number,school_name FROM library_operator JOIN professor ON library_operator.prof_id=professor.prof_id JOIN library_user ON library_user.username=professor.username WHERE first_name LIKE %s OR last_name LIKE %s OR CONCAT(first_name, ' ', last_name) LIKE %s AND approved=true;"
        cur.execute(query, (f"%{search}%", f"%{search}%", f"%{search}%",))
        column_names = [i[0] for i in cur.description]
        operators = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("operators.html", pageTitle="Library Users", home_name="Home", operators=operators, condition="admin")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/admin_page")


@operator.route("/operators/disable/<username>", methods = ["POST"])
def disableUser(username):
    """
    Disable operator by username from database
    """
    print(username)
    query = "UPDATE library_user SET approved=false WHERE username=%s;"
    try:
        cur = db.connection.cursor()
        cur.execute(query, (username,))
        db.connection.commit()
        cur.close()
        flash("Operator disabled successfully", "primary")
        return redirect("/operators")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/admin_page")

@operator.route("/operators/approve/<username>", methods = ["POST"])
def approveOperator(username):
    """
    Approve operator by username from database
    """
    query = "UPDATE library_user SET approved=true WHERE username=%s;"
    try:
        cur = db.connection.cursor()
        cur.execute(query, (username,))
        db.connection.commit()
        cur.close()
        flash("Operator approved successfully", "primary")
        return redirect("/operators/for_approval")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/admin_page")
    
@operator.route("/operators/disapprove/<username>", methods = ["POST"])
def dissaproveOperator(username):
    """
    Disapprove operator by username from database
    """
    query = "DELETE FROM library_user WHERE username = %s;"
    try:
        cur = db.connection.cursor()
        cur.execute(query, (username,))
        db.connection.commit()
        cur.close()
        flash("Operator disapproved successfully", "primary")
        return redirect("/operators/for_approval")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/admin_page")