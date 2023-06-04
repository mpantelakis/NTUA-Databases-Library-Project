from flask import Flask, render_template, request, flash, redirect, abort,session
from flask_mysqldb import MySQL
from library import db ## initially created by __init__.py, needs to be used here
from library.borrowings import borrowings
from library.borrowings.forms import LendForm

@borrowings.route("/borrowings")
def getBorrowings():
    """
    Retrieve borrowings from database
    """
    if "username" in session:
        username = session["username"]
    try:
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
        cur = db.connection.cursor()
        query = "SELECT borrowing_id,book.ISBN,borrows.copy_id, title, borrowing_date, due_return_date,CASE WHEN borrows.return_date IS NULL THEN 'Pending return' ELSE 'Returned'END AS state FROM book USE INDEX (book_titles) JOIN copy ON book.ISBN = copy.ISBN JOIN borrows ON borrows.copy_id=copy.copy_id JOIN library_user ON library_user.username = borrows.username WHERE library_user.username = %s ORDER BY borrowing_date DESC;"
        cur.execute(query, (username,))
        column_names = [i[0] for i in cur.description]
        borrowings = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("borrowings.html", pageTitle = "Borrowings Page", home_name="Home", borrowings = borrowings,condition=condition)
    except Exception as e:
        flash(str(e), "danger")

@borrowings.route("/borrowings/library")
def getLibraryBorrowings():
    """
    Retrieve borrowings from database
    """
    if "username" in session:
        username = session["username"]
    try:
        cur = db.connection.cursor()
        query_school_name="SELECT school_name FROM library_user WHERE username=%s"
        cur.execute(query_school_name,(username,))
        school_name = cur.fetchone()[0]
        query = "SELECT borrows.username,borrowing_id,borrows.copy_id, book.ISBN, title, borrowing_date, due_return_date,CASE WHEN borrows.return_date IS NULL THEN 'Pending return' ELSE 'Returned'END AS state FROM book USE INDEX (book_titles) JOIN copy ON book.ISBN = copy.ISBN JOIN borrows ON borrows.copy_id=copy.copy_id WHERE copy.school_name=%s ORDER BY borrowing_date DESC;"
        cur.execute(query, (school_name,))
        column_names = [i[0] for i in cur.description]
        borrowings = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("borrowings.html", pageTitle = "Borrowings Page", home_name="Home", borrowings = borrowings,condition="operator",condition1="all")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/operator_page")

@borrowings.route("/borrowings/search")
def searchLibraryAllBorrowings():
    """
    Retrieve borrowings from database
    """
    if "username" in session:
        username = session["username"]
    search = request.args.get("search")
    try:
        cur = db.connection.cursor()
        query_school_name="SELECT school_name FROM library_user WHERE username=%s"
        cur.execute(query_school_name,(username,))
        school_name = cur.fetchone()[0]
        query = "SELECT borrows.username, borrowing_id,borrows.copy_id, book.ISBN, title, borrowing_date, due_return_date,CASE WHEN borrows.return_date IS NULL THEN 'Pending return' ELSE 'Returned'END AS state FROM book USE INDEX (book_titles) JOIN copy ON book.ISBN = copy.ISBN JOIN borrows ON borrows.copy_id=copy.copy_id WHERE copy.school_name=%s and borrows.copy_id LIKE %s ORDER BY borrowing_date DESC;"
        cur.execute(query, (school_name,f"%{search}%",))
        column_names = [i[0] for i in cur.description]
        borrowings = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("borrowings.html", pageTitle = "Borrowings Page", home_name="Home", borrowings = borrowings,condition="operator",condition1="all")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/operator_page")

@borrowings.route("/borrowings/delayed")
def getDelayedBorrowings():
    """
    Retrieve delayed borrowings from database
    """
    if "username" in session:
        username = session["username"]
    try:
        cur = db.connection.cursor()
        query_school_name="SELECT school_name FROM library_user WHERE username=%s"
        cur.execute(query_school_name,(username,))
        school_name = cur.fetchone()[0]
        query = "SELECT borrows.username, borrowing_id,borrows.copy_id, book.ISBN, title, borrowing_date, due_return_date,CASE WHEN borrows.return_date IS NULL THEN 'Pending return' ELSE 'Returned'END AS state FROM book USE INDEX (book_titles) JOIN copy ON book.ISBN = copy.ISBN JOIN borrows ON borrows.copy_id=copy.copy_id WHERE copy.school_name=%s AND DATEDIFF(due_return_date, CURDATE())<0  AND borrowed=true ORDER BY borrowing_date ASC;"
        cur.execute(query, (school_name,))
        column_names = [i[0] for i in cur.description]
        borrowings = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("borrowings.html", pageTitle = "Delayed Borrowings Page", home_name="Home", borrowings = borrowings,condition="operator",condition1="delayed")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/operator_page")
    
@borrowings.route("/borrowings/search/delayed")
def searchDelayedBorrowings():
    """
    Retrieve delayed borrowings from database
    """
    if "username" in session:
        username = session["username"]
    search = request.args.get("search")
    try:
        cur = db.connection.cursor()
        query_school_name="SELECT school_name FROM library_user WHERE username=%s"
        cur.execute(query_school_name,(username,))
        school_name = cur.fetchone()[0]
        query = "SELECT borrows.username, borrowing_id,borrows.copy_id, book.ISBN, title, borrowing_date, due_return_date,CASE WHEN borrows.return_date IS NULL THEN 'Pending return' ELSE 'Returned'END AS state FROM book USE INDEX (book_titles) JOIN copy ON book.ISBN = copy.ISBN JOIN borrows ON borrows.copy_id=copy.copy_id WHERE copy.school_name=%s AND DATEDIFF(due_return_date, CURDATE())<0  and borrows.copy_id LIKE %s AND borrowed=true ORDER BY borrowing_date ASC;"
        cur.execute(query, (school_name,f"%{search}%",))
        column_names = [i[0] for i in cur.description]
        borrowings = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("borrowings.html", pageTitle = "Delayed Borrowings Page", home_name="Home", borrowings = borrowings,condition="operator",condition1="delayed")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/operator_page")

@borrowings.route("/borrowing/return", methods = ["GET","POST"])
def returnBorrowing():
    """
    Return borrowing in the database
    """

    borrowing_id = request.form.get("borrowing_id") 

    if(request.method == "POST"):
        try:
            cur = db.connection.cursor()
            query = "UPDATE borrows SET return_date=CURDATE() WHERE borrowing_id=%s"
            cur.execute(query, (borrowing_id,))
            db.connection.commit()
            cur.close()
            flash("Copy returned successfully", "success")
            return redirect("/borrowings/library")
        except Exception as e:
            flash(str(e), "danger")
            return redirect("/operator_page")
        
@borrowings.route("/borrowings/lend", methods = ["GET","POST"]) 
def addBorrowing():
    """
    Add a new borrowing to the Database

    """

    form = LendForm()

    if request.method == "POST" and  form.validate_on_submit() :

        try:
            newBorrowing = form.__dict__
            query_borrowing = "INSERT INTO borrows (username,copy_id) VALUES (%s,%s);"
            cur = db.connection.cursor()
            cur.execute(query_borrowing,(newBorrowing["username"].data,newBorrowing["copy_id"].data,))   
            db.connection.commit()
            cur.close()
            flash("Copy borrowed successfully!", "success")
            return redirect("/borrowings/library")
        except Exception as e: ## OperationalError
            flash(str(e), "danger")
            return redirect("/operator_page")
    else:
        try:      
            return render_template("lend_form.html", pageTitle = "Lend a copy", form = form, home_name="Home", condition="operator")
        except Exception as e: ## OperationalError
            flash(str(e), "danger")
            return redirect("/operator_page")
        

@borrowings.route("/borrowings/schools", methods = ["GET","POST"]) 
def getSchoolsBorrowings():
    """
    Retrieve borrowings from database
    """
    year = request.form.get("year")
    month = request.form.get("month") 
    try:
        cur = db.connection.cursor()
        query = "SELECT school_name, COUNT(*) as total_borrowings FROM library_user JOIN borrows ON borrows.username=library_user.username AND EXTRACT(YEAR FROM borrowing_date)=%s  AND EXTRACT(MONTH FROM borrowing_date)=%s GROUP BY school_name;"
        cur.execute(query,(year,month,))
        column_names = [i[0] for i in cur.description]
        total_borrowings = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("total_borrowings.html", pageTitle = "Total Borrowings Per School For Specific Year and Month", home_name="Home", total_borrowings = total_borrowings,condition="admin",year=year,month=month)
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/admin_page")
    

@borrowings.route("/borrowings/users/delayed") 
def getUsersandDelayedBorrowings():
    """
    Retrieve borrowings from database
    """
    if "username" in session:
        username = session["username"]
    try:
            cur = db.connection.cursor()
            query_school_name="SELECT school_name FROM library_user WHERE username=%s"
            cur.execute(query_school_name,(username,))
            school_name = cur.fetchone()[0]
            query = "SELECT DISTINCT first_name, last_name ,borrows.copy_id, DATEDIFF(CURDATE(),due_return_date) as total_delay_days FROM library_user USE INDEX (library_user_full_name) JOIN borrows USE INDEX(find_username_borrows) ON library_user.username = borrows.username  WHERE return_date IS NULL AND library_user.school_name = %s;"
            cur.execute(query, (school_name,))
            column_names = [i[0] for i in cur.description]
            delays = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            return render_template("delayed_users.html", pageTitle = "Library Users and Delayed Books", home_name="Home", delays=delays,condition="operator")
    except Exception as e:
            flash(str(e), "danger")
            return redirect("/operator_page")
        
@borrowings.route("/borrowings/users/delayed/search") 
def searchUsersandDelayedBorrowings():
    """
    Retrieve borrowings from database
    """
    if "username" in session:
        username = session["username"]
    cur = db.connection.cursor()
    query_school_name="SELECT school_name FROM library_user WHERE username=%s"
    cur.execute(query_school_name,(username,))
    school_name = cur.fetchone()[0]
    cur.close()
    search = request.args.get("search")
    try:
            cur = db.connection.cursor()
            if search.isdigit():
                search = int(request.args.get("search"))
                print(search)
                query = "SELECT DISTINCT first_name, last_name, borrows.copy_id, DATEDIFF(CURDATE(), due_return_date) AS total_delay_days FROM library_user USE INDEX (library_user_full_name) JOIN borrows USE INDEX (find_username_borrows) ON library_user.username = borrows.username WHERE return_date IS NULL AND library_user.school_name = %s AND DATEDIFF(CURDATE(), due_return_date) > %s;"
                cur.execute(query, (school_name, search,))
            else:
                query = "SELECT DISTINCT first_name, last_name, borrows.copy_id, DATEDIFF(CURDATE(), due_return_date) AS total_delay_days FROM library_user USE INDEX (library_user_full_name) JOIN borrows USE INDEX (find_username_borrows) ON library_user.username = borrows.username WHERE return_date IS NULL AND library_user.school_name = %s AND DATEDIFF(CURDATE(), due_return_date) > 0 AND (first_name LIKE %s OR last_name LIKE %s OR CONCAT(first_name, ' ', last_name) LIKE %s);"
                cur.execute(query, (school_name, f"%{search}%", f"%{search}%", f"%{search}%",))

            column_names = [i[0] for i in cur.description]
            delays = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            return render_template("delayed_users.html", pageTitle = "Library Users and Delayed Books", home_name="Home", delays=delays,condition="operator")
    except Exception as e:
            flash(str(e), "danger")
            return redirect("/operator_page")
    
@borrowings.route("/borrowings/young_professors") 
def getYoungProfessorsBorrowings():
    """
    Retrieve borrowings from database
    """

    try:
            cur = db.connection.cursor()
            query = "SELECT last_name, first_name,age, total_borrowings FROM (SELECT username, COUNT(username) as total_borrowings FROM borrows USE INDEX(find_username_borrows) GROUP BY username ) AS subquery JOIN library_user USE INDEX (library_user_full_name)  ON subquery.username = library_user.username JOIN professor USE INDEX (find_professor_username)ON professor.username=library_user.username WHERE total_borrowings >= ALL (SELECT COUNT(*) FROM borrows JOIN professor USE INDEX (find_professor_username) ON professor.username=borrows.username JOIN library_user ON library_user.username=professor.username WHERE age<40 GROUP BY borrows.username) AND age<40;"
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            professors = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            return render_template("young_professors.html", pageTitle = "Young Professors' Borrowings", home_name="Home", professors=professors,condition="admin")
    except Exception as e:
            flash(str(e), "danger")
            return redirect("/admin_page")
    
@borrowings.route("/borrowings/authors/not_borrowed") 
def getAuthorsNotBorrowed():

    try:
            cur = db.connection.cursor()
            query = "SELECT author_first_name, author_last_name FROM book_author USE INDEX (book_author_full_name) WHERE ISBN NOT IN (SELECT DISTINCT ISBN FROM copy WHERE copy_id IN (SELECT copy_id FROM borrows));"
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            authors = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            return render_template("authors_not_borrowed.html", pageTitle = "Book Authors Not Borrowed", home_name="Home", authors=authors,condition="admin")
    except Exception as e:
            flash(str(e), "danger")
            return redirect("/admin_page")
    
@borrowings.route("/borrowings/operators")
def getOperatorBorrowings():
    if "username" in session:
        username = session["username"]
    try:
        cur = db.connection.cursor()
        query = "SELECT l1.last_name, l1.first_name, total_borrowings FROM ( SELECT lib_op_id, COUNT(lib_op_id) AS total_borrowings FROM borrows WHERE YEAR(borrowing_date) = 2023 GROUP BY lib_op_id HAVING total_borrowings > 20) AS subquery JOIN library_operator ON subquery.lib_op_id = library_operator.lib_op_id JOIN professor ON library_operator.prof_id = professor.prof_id JOIN library_user l1 ON l1.username = professor.username JOIN library_user l2 ON l1.username <> l2.username GROUP BY last_name, first_name, total_borrowings HAVING COUNT(*) > 1;"
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        operators = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("operators_borrowings.html", pageTitle = "Borrowings Page", home_name="Home",operators=operators,condition="admin")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/admin_page")
