from flask import Flask, render_template, request, flash, redirect, url_for, abort,session
from flask_mysqldb import MySQL
from library import db ## initially created by __init__.py, needs to be used here
from library.copies import copies

@copies.route("/copies")
def getCopies():
    """
    Retrieve copies from database
    """
    if "username" in session:
        username = session["username"]
        isbn = request.args.get("book_isbn")  # Get the book title from the form data
    
    if (isbn==None):
        isbn = session["book_isbn"]
    else:
        session["book_isbn"]=isbn

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
        
        condition1="not_operator"
        if result_student > 0:
            condition="student"
        elif result_operator > 0:
            condition="operator"
            condition1="operator"
        elif result_professor > 0:
            condition="professor"
        elif result_admin > 0:
            condition="admin"
        print(isbn)
        print(username)
        cur = db.connection.cursor()
        query = "SELECT copy_id, CASE WHEN (borrowed IS TRUE AND reserved IS FALSE) OR (borrowed IS FALSE AND reserved IS FALSE) THEN 'Yes' WHEN (borrowed IS TRUE AND reserved IS TRUE) OR  (borrowed IS FALSE AND reserved IS TRUE) THEN 'No'  END AS reservation_availability, CASE WHEN (borrowed IS TRUE AND reserved IS FALSE) OR (borrowed IS TRUE AND reserved IS TRUE) OR (borrowed IS FALSE AND reserved IS TRUE) THEN 'No' WHEN (borrowed IS FALSE AND reserved IS FALSE)  THEN 'Yes' END AS borrowing_availability FROM book  JOIN copy ON copy.ISBN=book.ISBN JOIN library_user ON library_user.school_name=copy.school_name WHERE library_user.username = %s AND book.ISBN=%s;"
        cur.execute(query, (username,isbn,))
        column_names = [i[0] for i in cur.description]
        copies = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.execute("SELECT  title  FROM book WHERE ISBN=%s;",(isbn,))
        book_title = cur.fetchone()[0]
        cur.close()
        return render_template("copies.html", pageTitle = "Copies of {}".format(book_title), home_name="Home", copies = copies,condition=condition,condition1=condition1)
    except Exception as e:
        flash(str(e), "danger")

@copies.route("/copies/add",  methods = ["GET", "POST"])
def addCopy():
    """
    Add copy to database
    """
    if "username" in session:
        username = session["username"]
    print(username)
    isbn = request.form.get("book_isbn")  # Get the book title from the form data
    print(isbn)
    query_school_name="SELECT school_name FROM library_user WHERE username=%s;"

    cur = db.connection.cursor()
    cur.execute(query_school_name,(username,))
    school_name = cur.fetchone()[0]    
    cur.close()
    print(school_name)

    if(request.method == "POST"):
        try:
            cur = db.connection.cursor()
            query = "INSERT INTO copy (ISBN,school_name) VALUES (%s,%s);"
            cur.execute(query, (isbn,school_name,))
            db.connection.commit()
            cur.close()
            flash("Copy added successfully", "success")
            return redirect("/books")
        except Exception as e:
            flash(str(e), "danger")

@copies.route("/copies/delete", methods = ["GET","POST"])
def deleteCopy():
    """
    Delete copy from the database
    """

    copy_id = request.form.get("copy_id") 
    cur = db.connection.cursor()
    query = "SELECT book.ISBN FROM book JOIN copy ON copy.ISBN=book.ISBN WHERE copy_id=%s;"
    cur.execute(query, (copy_id,))
    isbn = cur.fetchone()[0] 
    cur.close()
    session["isbn"] = isbn
    print(copy_id)
    print(isbn)

    if(request.method == "POST"):
        try:
            cur = db.connection.cursor()
            query = "DELETE FROM copy WHERE copy_id=%s"
            cur.execute(query, (copy_id,))
            db.connection.commit()
            cur.close()
            flash("Copy deleted successfully", "success")
            return redirect("/copies")
        except Exception as e:
            error_message = str(e.args[1])  # Access the MySQL error message from the exception object
            flash(error_message, "danger")
            return redirect("/copies")