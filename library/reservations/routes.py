from flask import Flask, render_template, request, flash, redirect, url_for, abort, session
from flask_mysqldb import MySQL
from library import db ## initially created by __init__.py, needs to be used here
from library.reservations import reservations

@reservations.route("/reservations")
def getReservations():
    """
    Retrieve reservations from the database
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

    
        print(username)
        cur = db.connection.cursor()
        query = "SELECT reservation_id, book.ISBN, title,reserves.copy_id as copy_id, cancellation_date, reservation_date, CASE WHEN reserves.cancellation_date IS NULL THEN 'Active' ELSE 'Cancelled' END AS state FROM book USE INDEX (book_titles) JOIN copy ON book.ISBN = copy.ISBN JOIN reserves ON reserves.copy_id = copy.copy_id JOIN library_user ON library_user.username = reserves.username WHERE library_user.username = %s ORDER BY reservation_date DESC;"
        cur.execute(query, (username,))
        column_names = [i[0] for i in cur.description]
        reservations = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("reservations.html", pageTitle="Reservations Page", home_name="Home", reservations=reservations,condition=condition,condition1="cancel")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/user/home_page")
    
@reservations.route("/reservations/library")
def getLibraryReservations():
    """
    Retrieve library reservations from the database
    """
    if "username" in session:
        username = session["username"]
    try:
        cur = db.connection.cursor()
        query_school_name="SELECT school_name FROM library_user WHERE username=%s"
        cur.execute(query_school_name,(username,))
        school_name = cur.fetchone()[0]
        query = "SELECT reservation_id,book.ISBN, title,reserves.copy_id as copy_id, cancellation_date, reservation_date, CASE WHEN reserves.cancellation_date IS NULL THEN 'Active' ELSE 'Cancelled' END AS state FROM book USE INDEX (book_titles) JOIN copy ON book.ISBN = copy.ISBN JOIN reserves ON reserves.copy_id = copy.copy_id AND copy.school_name= %s ORDER BY reservation_date DESC;"
        cur.execute(query, (school_name,))
        column_names = [i[0] for i in cur.description]
        reservations = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("reservations.html", pageTitle="Reservations Page", home_name="Home", reservations=reservations,condition="operator",condition1="nocancel")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/operator_page")
    
@reservations.route("/reservations/active")
def getActiveReservations():
    """
    Retrieve active library reservations from the database
    """
    if "username" in session:
        username = session["username"]
    try:
        cur = db.connection.cursor()
        query_school_name="SELECT school_name FROM library_user WHERE username=%s"
        cur.execute(query_school_name,(username,))
        school_name = cur.fetchone()[0]
        query = "SELECT reservation_id,book.ISBN, title,reserves.copy_id as copy_id, cancellation_date, reservation_date, CASE WHEN reserves.cancellation_date IS NULL THEN 'Active' ELSE 'Cancelled' END AS state FROM book USE INDEX (book_titles) JOIN copy ON book.ISBN = copy.ISBN JOIN reserves ON reserves.copy_id = copy.copy_id AND copy.school_name= %s AND cancellation_date IS NULL ORDER BY reservation_date DESC;"
        cur.execute(query, (school_name,))
        column_names = [i[0] for i in cur.description]
        reservations = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("reservations.html", pageTitle=" Active Reservations Page", home_name="Home", reservations=reservations,condition="operator",condition1="active")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/operator_page")
    
@reservations.route("/reservations/search")
def searchLibraryReservations():
    """
    Retrieve reservations from database
    """
    if "username" in session:
        username = session["username"]
    search = request.args.get("search")
    try:
        cur = db.connection.cursor()
        query_school_name="SELECT school_name FROM library_user WHERE username=%s"
        cur.execute(query_school_name,(username,))
        school_name = cur.fetchone()[0]
        query = "SELECT borrowing_id,borrows.copy_id, book.ISBN, title, borrowing_date, due_return_date,CASE WHEN borrows.return_date IS NULL THEN 'Pending return' ELSE 'Returned'END AS state FROM book USE INDEX (book_titles) JOIN copy ON book.ISBN = copy.ISBN JOIN borrows ON borrows.copy_id=copy.copy_id WHERE copy.school_name=%s and borrows.copy_id LIKE %s ORDER BY borrowing_date DESC;"
        cur.execute(query, (school_name,f"%{search}%",))
        column_names = [i[0] for i in cur.description]
        borrowings = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("borrowings.html", pageTitle = "Borrowings Page", home_name="Home", borrowings = borrowings,condition="operator")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/operator_page")

@reservations.route("/reserve_copy", methods = ["POST"])
def reserveCopy():
    """
    Reserve a book
    """
    if "username" in session:
        username = session["username"]
        print(username)
    copy_id = int(request.form.get("copy_id")) 
    print(copy_id)

    if(request.method == "POST"):
        try:
            cur = db.connection.cursor()
            query = "INSERT INTO reserves (username, copy_id) values ('{}',{});".format(username,copy_id)
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Copy reserved successfully", "success")
            return redirect("/reservations")
        except Exception as e:
            error_message = str(e.args[1])  # Access the MySQL error message from the exception object
            flash(error_message, "danger")
            return redirect("/copies")
        
@reservations.route("/reservations/cancel", methods = ["POST"])
def cancelReservation():
    """
    Cancel reservation
    """
    reservation_id= request.form.get("reservation_id")
    print(reservation_id)
    query = "UPDATE reserves SET cancellation_date=CURDATE() WHERE reservation_id=%s AND cancellation_date IS NULL;"
    try:
        cur = db.connection.cursor()
        cur.execute(query, (reservation_id,))
        db.connection.commit()
        cur.close()
        flash("Reservation cancelled successfully", "success")
        return redirect("/reservations")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/reservations")
    
@reservations.route("/reservations/approve", methods = ["POST"])
def approveReservation():
    """
    Approve reservation
    """
    reservation_id= request.form.get("reservation_id")
    query = "UPDATE reserves SET approved=true WHERE reservation_id=%s AND cancellation_date IS NULL;"
    try:
        cur = db.connection.cursor()
        cur.execute(query, (reservation_id,))
        db.connection.commit()
        cur.close()
        flash("Reservation approved successfully", "success")
        return redirect("/borrowings/library")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/operator_page")
