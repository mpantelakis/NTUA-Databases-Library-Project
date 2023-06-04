from flask import Flask, render_template, request, flash, redirect, url_for, abort,session
from flask_mysqldb import MySQL
from library import db ## initially created by __init__.py, needs to be used here
from library.reviews.forms import ReviewForm
from library.reviews import reviews

@reviews.route("/reviews")
def getReviews():
    """
    Retrieve reviews from database
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
        query = "SELECT book.ISBN as ISBN, title, review_id, Likert, review_text FROM review JOIN book ON book.ISBN=review.ISBN JOIN library_user ON library_user.username = review.username WHERE library_user.username = %s ORDER BY review_id DESC;"
        cur.execute(query, (username,))
        column_names = [i[0] for i in cur.description]
        reviews= [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("reviews.html", pageTitle = "Reviews Page", home_name="Home", reviews=reviews,condition=condition)
    except Exception as e:
        flash(str(e), "danger")


@reviews.route("/reviews/library")
def getLibraryReviews():
    """
    Retrieve library reviews from database
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
        cur.execute("SELECT school_name FROM library_user WHERE username=%s;",(username,))
        school_name=cur.fetchone()[0]
        query = "SELECT review.username as username, review.ISBN as ISBN, title, review_id, Likert, review_text FROM review JOIN book ON book.ISBN=review.ISBN JOIN library_user ON library_user.username = review.username WHERE library_user.school_name = %s AND review.approved=true ORDER BY review_id DESC;"
        cur.execute(query, (school_name,))
        column_names = [i[0] for i in cur.description]
        reviews= [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("reviews.html", pageTitle = "Reviews Page", home_name="Home", reviews=reviews,condition=condition,condition1=condition)
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/operator_page")

@reviews.route("/reviews/show")
def getBookReviews():
    """
    Retrieve reviews for a book from database
    """
    if "username" in session:
        username = session["username"]
    isbn = request.args.get("book_isbn") 
    print(username)
    print(isbn)
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
        query1 = "SELECT book.ISBN, review_id, library_user.username as username, title, Likert, review_text FROM review JOIN book ON book.ISBN=review.ISBN JOIN library_user ON library_user.username = review.username WHERE review.ISBN=%s AND review.approved=true ORDER BY username DESC;"
        cur.execute(query1,(isbn,))
        column_names = [i[0] for i in cur.description]
        reviews= [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("reviews.html", pageTitle = "Reviews Page", home_name="Home", reviews=reviews,condition=condition,condition1="book_reviews")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/books")

@reviews.route("/reviews/library/for_approval")
def getLibraryReviewsForApproval():
    """
    Retrieve library reviews for approval from database
    """
    if "username" in session:
        username = session["username"]
    try:
        cur = db.connection.cursor()
        cur.execute("SELECT school_name FROM library_user WHERE username=%s;",(username,))
        school_name=cur.fetchone()[0]
        query = "SELECT review.username, review.ISBN, title, review_id, Likert, review_text FROM review JOIN book ON book.ISBN=review.ISBN JOIN library_user ON library_user.username = review.username WHERE library_user.school_name = %s AND review.approved=false ORDER BY review_id DESC;"
        cur.execute(query, (school_name,))
        column_names = [i[0] for i in cur.description]
        reviews= [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("reviews_for_approval.html", pageTitle = "Reviews For Approval", home_name="Home", reviews=reviews,condition="operator")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/operator_page")

@reviews.route("/reviews/delete", methods = ["POST"])
def deleteReview():
    """
    Delete copy from the database
    """
    if "username" in session:
        username = session["username"]
        query_operator = "SELECT COUNT(*) FROM library_operator, library_user, professor WHERE library_user.username=professor.username AND library_operator.prof_id=professor.prof_id  AND library_user.username='{}';".format(username)        
        cur = db.connection.cursor()
        cur.execute(query_operator)
        result_operator = cur.fetchone()[0]
        cur.close()
    review_id = request.form.get("review-id") 
    try:
        cur = db.connection.cursor()
        query = "DELETE FROM review WHERE review_id=%s"
        cur.execute(query, (review_id,))
        db.connection.commit()
        cur.close()
        flash("Review deleted successfully", "success")
        if result_operator==0:
            return redirect("/reviews")
        else:
            return redirect("/reviews/library")
    except Exception as e:
            flash(str(e), "danger")
            return redirect("/reviews")

@reviews.route("/reviews/disapprove/<review_id>", methods = ["POST"])
def disapproveReview(review_id):
    """
    Disapprove review from the database
    """
    try:
        cur = db.connection.cursor()
        query = "DELETE FROM review WHERE review_id=%s"
        cur.execute(query, (review_id,))
        db.connection.commit()
        cur.close()
        flash("Review disapproved successfully", "success")
        return redirect("/reviews/library/for_approval")
    except Exception as e:
            flash(str(e), "danger")
            return redirect("/operator_page")
    
@reviews.route("/reviews/approve/<review_id>", methods = ["POST"])
def ApproveReview(review_id):
    """
    Approve review from the database
    """
    try:
        cur = db.connection.cursor()
        query = "UPDATE review SET approved=true WHERE review_id=%s"
        cur.execute(query, (review_id,))
        db.connection.commit()
        cur.close()
        flash("Review approved successfully", "success")
        return redirect("/reviews/library/for_approval")
    except Exception as e:
            flash(str(e), "danger")
            return redirect("/operator_page")

@reviews.route("/review/create", methods = ["GET", "POST"]) 
def createReview():
    """
    Create a review for a book
    
    """

    if "username" in session:
        username = session["username"]

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
    print(condition)
    form = ReviewForm()

    isbn = request.args.get("book_isbn") 
    print(isbn)


    if request.method == "POST" and  form.validate_on_submit() :

            try:
                newReview = form.__dict__
                # print(int(newReview["rating"]).data)
                query = "INSERT INTO review (Likert,review_text,ISBN,username) VALUES (%s,%s,%s,%s);"
                cur = db.connection.cursor()
                cur.execute(query,(newReview["rating"].data,newReview["review_text"].data,isbn,username,))   
                db.connection.commit()
                cur.close()
                flash("Review created successfully!", "success")
                return redirect("/reviews")
            except Exception as e: ## OperationalError
                flash(str(e), "danger")
                return redirect("/books")
    # else, response for GET request
    else:
        try:      
            return render_template("review_form.html", pageTitle = "Add a review", form = form, home_name="Home", condition=condition)
        except Exception as e: ## OperationalError
            flash(str(e), "danger")
            return redirect("/books")

@reviews.route("/reviews/average")
def getAverageRatings():
    """
    Retrieve ratings for a book from database
    """    
    try:
        return render_template("average_ratings.html", pageTitle = "Average Ratings per Library User or Book Category", home_name="Home", ratings={},condition="operator")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/operator_page")
    
@reviews.route("/reviews/average/search")
def showAverageRatings():
    """
    Retrieve ratings for a book from database
    """
    if "username" in session:
        username = session["username"]
    print(username)
    cur = db.connection.cursor()
    query_school_name="SELECT school_name FROM library_user WHERE username=%s"
    cur.execute(query_school_name,(username,))
    school_name = cur.fetchone()[0]
    cur.close()
    print(school_name)

    
    try:
        option = request.args.get("search_type")
        search = request.args.get("search")
        print(option)
        cur = db.connection.cursor()  
        if option=="user":
            query = "SELECT DISTINCT first_name, last_name , avg(Likert) as average_rating FROM library_user USE INDEX (library_user_full_name,library_user_school_name ) JOIN review ON review.username= library_user.username WHERE library_user.school_name = %s AND library_user.username LIKE %s GROUP BY first_name, last_name;"
            cur.execute(query,(school_name, f"%{search}%",))
            column_names = [i[0] for i in cur.description]
            ratings= [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            return render_template("average_ratings.html", pageTitle = "Average Ratings per Library User or Book Category", home_name="Home", ratings=ratings,condition="operator",condition1="user")
        elif option=="category":
            query = "SELECT category , avg(Likert) as average_rating FROM book_category USE INDEX(book_category_find_category) JOIN review ON review.ISBN= book_category.ISBN JOIN has_book USE INDEX (has_book_find_school_name) ON review.ISBN= has_book.ISBN JOIN library_user ON  has_book.school_name = library_user.school_name WHERE library_user.school_name = %s AND category = %s GROUP BY category;"
            cur.execute(query,(school_name,search,))
            column_names = [i[0] for i in cur.description]
            ratings= [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            return render_template("average_ratings.html", pageTitle = "Average Ratings per Library User or Book Category", home_name="Home", ratings=ratings,condition="operator",condition1="category")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/operator_page")