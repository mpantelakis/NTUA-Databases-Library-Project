from flask import Flask, render_template, request, flash, redirect, url_for, abort,session
from flask_mysqldb import MySQL
from library import db ## initially created by __init__.py, needs to be used here
from library.categories import categories

@categories.route("/categories/authors", methods = ["GET","POST"]) 
def getCateqoryAuthors():

    if request.method == "POST":
        category= request.form.get("category")
        try:
            cur = db.connection.cursor()
            query = "SELECT author_first_name, author_last_name, category FROM book_author USE INDEX (book_author_full_name) JOIN book_category ON book_author.ISBN = book_category.ISBN WHERE category=%s;"
            cur.execute(query,(category,))
            column_names = [i[0] for i in cur.description]
            authors = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            return render_template("specific_category_authors.html", pageTitle = "Authors and Categories", home_name="Home",authors=authors, condition="admin")
        except Exception as e:
            flash(str(e), "danger")
            return redirect("/admin_page")
    else:
        return render_template("specific_category_authors.html", pageTitle = "Authors and Categories", home_name="Home",authors={}, condition="admin")

@categories.route("/categories/professors", methods = ["GET","POST"]) 
def getCateqoryProfessors():

    if request.method == "POST":
        category= request.form.get("category")
        try:
            cur = db.connection.cursor()
            query = "SELECT DISTINCT first_name, last_name, category FROM library_user USE INDEX (library_user_full_name) JOIN professor ON library_user.username = professor.username JOIN borrows USE INDEX(find_username_borrows,borrowing_copy_id) ON borrows.username = professor.username JOIN copy ON borrows.copy_id = copy.copy_id JOIN book_category USE INDEX (book_category_find_category) ON copy.ISBN = book_category.ISBN WHERE EXTRACT(YEAR FROM borrowing_date) = EXTRACT(YEAR FROM CURDATE()) AND category = %s;"
            cur.execute(query,(category,))
            column_names = [i[0] for i in cur.description]
            professors = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            return render_template("specific_category_professors.html", pageTitle = "Authors and Categories", home_name="Home",professors=professors, condition="admin")
        except Exception as e:
            flash(str(e), "danger")
            return redirect("/admin_page")
    else:
        return render_template("specific_category_professors.html", pageTitle = "Professors and Categories", home_name="Home",professors={}, condition="admin")
    
@categories.route("/categories/top3")
def getTop3Categories():

        try:
            cur = db.connection.cursor()
            query = "SELECT (CASE WHEN bc1.category < bc2.category THEN bc1.category ELSE bc2.category END) AS category1, (CASE WHEN bc1.category < bc2.category THEN bc2.category ELSE bc1.category END) AS category2, COUNT(*) as appearances FROM book_category bc1 USE INDEX(book_category_find_category) JOIN book_category bc2 USE INDEX(book_category_find_category) ON bc1.ISBN = bc2.ISBN AND bc1.category <> bc2.category JOIN copy ON copy.ISBN = bc2.ISBN JOIN borrows USE INDEX(borrowing_copy_id) ON copy.copy_id = borrows.copy_id GROUP BY category1, category2 ORDER BY appearances DESC LIMIT 3;"
            cur.execute(query)
            column_names = [i[0] for i in cur.description]
            categories = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            cur.close()
            return render_template("top3_categories.html", pageTitle = "Top 3 Borrowed Categories", home_name="Home",categories=categories, condition="admin")
        except Exception as e:
            flash(str(e), "danger")
            return redirect("/admin_page")

