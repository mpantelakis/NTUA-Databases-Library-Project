from flask import Flask, render_template, request, flash, redirect, url_for, abort,session
from flask_mysqldb import MySQL
from library import db ## initially created by __init__.py, needs to be used here
from library.books import books
from library.books.forms import BookForm


@books.route("/books")
def getBooks():
    """
    Retrieve books from database
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
    try:
        cur = db.connection.cursor()
        query = "SELECT book.ISBN, title,GROUP_CONCAT(DISTINCT CONCAT(' ',author_first_name,' ', author_last_name)) AS authors, GROUP_CONCAT(DISTINCT category) as categories, GROUP_CONCAT( DISTINCT key_word) as key_words FROM book USE INDEX(book_titles) JOIN book_author ON book.ISBN = book_author.ISBN JOIN book_category ON book_category.ISBN=book.ISBN JOIN book_keywords ON book_keywords.ISBN=book.ISBN JOIN has_book ON has_book.ISBN = book.ISBN JOIN library_user ON library_user.school_name=has_book.school_name WHERE library_user.username = %s GROUP BY book.ISBN,title;"
        cur.execute(query, (username,))
        column_names = [i[0] for i in cur.description]
        books = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        print(books[0])
        cur.close()
        return render_template("books.html", pageTitle = "Books", home_name="Home", books = books,condition=condition,condition1=condition1)

    except Exception as e:
        flash(str(e), "danger")
        return redirect("/user/home_page")


@books.route("/books/search")
def getBookSearch():
    """
    Retrieve books from database
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
    try:
        cur = db.connection.cursor()
        if search.isdigit():
            search = int(request.args.get("search"))
            print(search)
            query = "SELECT book.ISBN, title,GROUP_CONCAT(DISTINCT CONCAT(' ',author_first_name,' ', author_last_name)) AS authors, GROUP_CONCAT(DISTINCT category) as categories, GROUP_CONCAT( DISTINCT key_word) as key_words FROM book USE INDEX(book_titles) JOIN book_author ON book.ISBN = book_author.ISBN JOIN book_category ON book_category.ISBN=book.ISBN JOIN book_keywords ON book_keywords.ISBN=book.ISBN JOIN has_book ON has_book.ISBN = book.ISBN JOIN library_user ON library_user.school_name=has_book.school_name JOIN copy ON copy.ISBN=book.ISBN AND copy.school_name=library_user.school_name WHERE library_user.username = %s  AND copy_id=%s GROUP BY title,book.ISBN;"
            cur.execute(query, (username,search))
        else:
            query = "SELECT book.ISBN, title,GROUP_CONCAT(DISTINCT CONCAT(' ',author_first_name,' ', author_last_name)) AS authors, GROUP_CONCAT(DISTINCT category) as categories, GROUP_CONCAT( DISTINCT key_word) as key_words FROM book USE INDEX(book_titles) JOIN book_author ON book.ISBN = book_author.ISBN JOIN book_category ON book_category.ISBN=book.ISBN JOIN book_keywords ON book_keywords.ISBN=book.ISBN JOIN has_book ON has_book.ISBN = book.ISBN JOIN library_user ON library_user.school_name=has_book.school_name WHERE library_user.username = %s AND book.title LIKE %s OR category LIKE %s OR author_first_name LIKE %s OR author_last_name LIKE %s OR CONCAT(author_first_name, ' ', author_last_name) LIKE %s OR key_word LIKE %s GROUP BY title,book.ISBN;"
            cur.execute(query, (username,f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%",f"%{search}%"))
        column_names = [i[0] for i in cur.description]
        books = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        print(books)
        cur.close()
        return render_template("books.html", pageTitle = "Books", home_name="Home", books = books,condition=condition,condition1=condition1)
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/books")

@books.route("/books/search/all")
def getBookSearchAll():
    """
    Retrieve books from database
    """
    search = request.args.get("search")

    try:
        cur = db.connection.cursor()
        query = "SELECT book.ISBN, title,GROUP_CONCAT(DISTINCT CONCAT(' ',author_first_name,' ', author_last_name)) AS authors, GROUP_CONCAT(DISTINCT category) as categories, GROUP_CONCAT( DISTINCT key_word) as key_words FROM book USE INDEX(book_titles) JOIN book_author ON book.ISBN = book_author.ISBN JOIN book_category ON book_category.ISBN=book.ISBN JOIN book_keywords ON book_keywords.ISBN=book.ISBN WHERE book.title LIKE %s OR category LIKE %s OR author_first_name LIKE %s OR author_last_name LIKE %s OR CONCAT(author_first_name, ' ', author_last_name) LIKE %s OR key_word LIKE %s GROUP BY title,book.ISBN;"
        cur.execute(query, (f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%", f"%{search}%",f"%{search}%"))
        #print(query)
        column_names = [i[0] for i in cur.description]
        books = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("books.html", pageTitle = "Books Depository", home_name="Home", books = books,condition="operator",condition1="all")
    except Exception as e:
        flash(str(e), "danger")




@books.route("/book/page")
def getBookPage():
    """
    Retrieve book info from database
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

    isbn = request.args.get("book_isbn")
    print(isbn)
    try:
        cur = db.connection.cursor()
        query = "SELECT title, book.ISBN,language, abstract, publisher, num_of_pages, image, GROUP_CONCAT(DISTINCT CONCAT(' ', author_first_name, ' ', author_last_name)) AS authors, GROUP_CONCAT(DISTINCT category) AS categories, GROUP_CONCAT(DISTINCT key_word) AS key_words FROM book USE INDEX(book_titles) JOIN book_author ON book.ISBN = book_author.ISBN JOIN book_category ON book_category.ISBN = book.ISBN JOIN book_keywords ON book_keywords.ISBN = book.ISBN WHERE book.ISBN = %s GROUP BY title, language, abstract, publisher,image, num_of_pages,book.ISBN;"
        cur.execute(query, (isbn,))
        column_names = [i[0] for i in cur.description]
        book = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        print(book[0])
        cur.close()
        return render_template("book_page.html", pageTitle = "Book Page", home_name="Home", book = book,condition=condition)
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/books")

@books.route("/books/add", methods = ["GET", "POST"]) 
def addBook():
    """
    Add a new book to the Library Network
    
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
    form = BookForm()

    if request.method == "POST" and  form.validate_on_submit() :

            try:
                newBook = form.__dict__
                query_book = "INSERT INTO book (ISBN,title,publisher, num_of_pages,abstract,image,language) VALUES (%s,%s,%s,%s,%s,%s,%s);"
                cur = db.connection.cursor()
                cur.execute(query_book,(newBook["isbn"].data,newBook["title"].data,newBook["publisher"].data,newBook["num_of_pages"].data,newBook["abstract"].data,newBook["image_link"].data,newBook["language"].data))   
                db.connection.commit()
                query_author = "INSERT INTO book_author (ISBN,author_first_name,author_last_name) VALUES (%s,%s,%s);"
                cur.execute(query_author,(newBook["isbn"].data,newBook["author_first_name"].data,newBook["author_last_name"].data))
                db.connection.commit()
                query_category = "INSERT INTO book_category (ISBN,category) VALUES (%s,%s);"
                cur.execute(query_category,(newBook["isbn"].data,newBook["category"].data))
                db.connection.commit()
                query_category = "INSERT INTO book_keywords (ISBN,key_word) VALUES (%s,%s);"
                cur.execute(query_category,(newBook["isbn"].data,newBook["keyword"].data))
                db.connection.commit()
                cur.close()
                flash("Book added successfully!", "success")
                return redirect("/books/all")
            except Exception as e: ## OperationalError
                flash(str(e), "danger")
                return redirect("/operator_page")
    # else, response for GET request
    else:
        try:      
            return render_template("book_form.html", pageTitle = "Add a book", form = form, home_name="Home", condition=condition)
        except Exception as e: ## OperationalError
            flash(str(e), "danger")
            return redirect("/operator_page")

@books.route("/books/all")
def getAllBooks():
    """
    Retrieve all books from database
    """

    condition="operator"
    condition1="all"
    try:
        cur = db.connection.cursor()
        query = "SELECT book.ISBN, title,GROUP_CONCAT(DISTINCT CONCAT(' ',author_first_name,' ', author_last_name)) AS authors, GROUP_CONCAT(DISTINCT category) as categories, GROUP_CONCAT( DISTINCT key_word) as key_words FROM book USE INDEX(book_titles) JOIN book_author ON book.ISBN = book_author.ISBN JOIN book_category ON book_category.ISBN=book.ISBN JOIN book_keywords ON book_keywords.ISBN=book.ISBN GROUP BY book.ISBN,title;"
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        books = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        print(books[0])
        cur.close()
        return render_template("books.html", pageTitle = "Books", home_name="Home", books = books,condition=condition,condition1=condition1)

    except Exception as e:
        flash(str(e), "danger")
        return redirect("/operator_page")

@books.route("/books/addi",  methods = ["GET", "POST"])
def addiBook():
    if "username" in session:
        username = session["username"]
    isbn = request.form.get("book_isbn")

    query="SELECT school_name FROM library_user WHERE username=%s"
    cur = db.connection.cursor()
    cur.execute(query, (username,))
    school_name=cur.fetchone()[0]
    cur.close()

    if(request.method == "POST"):
        try:
            query1="INSERT INTO has_book (ISBN,school_name) VALUES (%s,%s);"
            cur = db.connection.cursor()
            cur.execute(query1,(isbn,school_name,))
            db.connection.commit()
            cur.close()
            flash("Book added successfully to your school.", "success")
            return redirect("/books/all")
        except Exception as e:
            error_message = str(e.args[1])  # Access the MySQL error message from the exception object
            flash(error_message, "danger")
            return redirect("/books/all")
            
@books.route("/book/delete", methods = ["GET","POST"])
def deleteBook():
    """
    Delete book from school library 
    """
    if "username" in session:
        username = session["username"]
    isbn = request.form.get("book_isbn")
    cur = db.connection.cursor()
    query = "SELECT school_name FROM library_user WHERE username=%s;"
    cur.execute(query, (username,))
    school_name = cur.fetchone()[0] 
    cur.close()
    print(school_name)
    print(isbn)

    if(request.method == "POST"):
        try:
            cur = db.connection.cursor()
            query = "DELETE FROM has_book WHERE ISBN=%s AND school_name=%s;"
            cur.execute(query, (isbn,school_name,))
            db.connection.commit()
            cur.close()
            flash("Book deleted successfully", "success")
            return redirect("/books")
        except Exception as e:
            flash(str(e), "danger")
            return redirect("/books")
        
@books.route("/books/authors_5_less_than_max")
def getAuthors():

    try:
        cur = db.connection.cursor()
        query = "SELECT author_first_name, author_last_name, total_written_books FROM (SELECT author_first_name, author_last_name, COUNT(*) as total_written_books FROM book_author USE INDEX(book_author_full_name) GROUP BY author_first_name, author_last_name) AS subquery WHERE total_written_books <= (SELECT MAX(total_written_books) FROM (SELECT author_first_name, author_last_name, COUNT(*) as total_written_books FROM book_author USE INDEX(book_author_full_name) GROUP BY author_first_name, author_last_name) AS max_books) - 5 ORDER BY total_written_books DESC;"
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        authors = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("authors_5_less_than_max.html", pageTitle = "Authors with 5 Less Books Than the Author with Most Books", home_name="Home", authors=authors,condition="admin")

    except Exception as e:
        flash(str(e), "danger")
        return redirect("/admin_page")