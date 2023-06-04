#(3.1.1)
SELECT school_name, COUNT(*) as total_borrowings
FROM library_user
JOIN borrows ON borrows.username=library_user.username
AND EXTRACT(YEAR FROM borrowing_date)=2023 
AND EXTRACT(MONTH FROM borrowing_date)=04
GROUP BY school_name;

#(3.1.2) authors of a certain book category	
SELECT author_first_name, author_last_name, category
FROM book_author USE INDEX (book_author_full_name)
JOIN book_category ON book_author.ISBN = book_category.ISBN
AND category='Thriller';

#professors that borrowed books of a certain category the last year
SELECT DISTINCT first_name, last_name
FROM library_user USE INDEX (library_user_full_name)
JOIN professor ON library_user.username = professor.username
JOIN borrows USE INDEX(find_username_borrows,borrowing_copy_id) ON borrows.username = professor.username
JOIN copy ON borrows.copy_id = copy.copy_id
JOIN book_category USE INDEX (book_category_find_category) ON copy.ISBN = book_category.ISBN
WHERE EXTRACT(YEAR FROM borrowing_date) = EXTRACT(YEAR FROM CURDATE())
AND category = 'History';

#(3.1.3) professors under 40 years old that borrowed the max number of books
SELECT last_name, first_name,age, total_borrowings
FROM (
	#total_borrowings per username
    SELECT username, COUNT(username) as total_borrowings
    FROM borrows USE INDEX(find_username_borrows)
    GROUP BY username
) AS subquery
#last_name and first_name are in table library_user
JOIN library_user USE INDEX (library_user_full_name)  ON subquery.username = library_user.username
#we have to find which of these users are professors
JOIN professor USE INDEX (find_professor_username)ON professor.username=library_user.username
WHERE total_borrowings >= ALL (
    SELECT COUNT(*) 
    FROM borrows
    JOIN professor USE INDEX (find_professor_username) ON professor.username=borrows.username
	JOIN library_user ON library_user.username=professor.username
    WHERE age<40
    GROUP BY borrows.username
)
AND age<40;

# (3.1.4) authors' name that their books have never been borrowed
SELECT author_first_name, author_last_name
FROM book_author USE INDEX (book_author_full_name)
WHERE ISBN NOT IN (SELECT DISTINCT ISBN FROM copy WHERE copy_id IN (SELECT copy_id FROM borrows));

#(3.1.5) library operators that executed the same number of total borrowings with total borrowings>20
SELECT l1.last_name, l1.first_name, total_borrowings
FROM (
    SELECT lib_op_id, COUNT(lib_op_id) AS total_borrowings
    FROM borrows
    WHERE YEAR(borrowing_date) = 2023
    GROUP BY lib_op_id
    HAVING total_borrowings > 20
) AS subquery
JOIN library_operator ON subquery.lib_op_id = library_operator.lib_op_id
JOIN professor ON library_operator.prof_id = professor.prof_id
JOIN library_user l1 ON l1.username = professor.username
JOIN library_user l2 ON l1.username <> l2.username
GROUP BY last_name, first_name, total_borrowings
HAVING COUNT(*) > 1;

#(3.1.6)
SELECT
    (CASE WHEN bc1.category < bc2.category THEN bc1.category ELSE bc2.category END) AS category1,
    (CASE WHEN bc1.category < bc2.category THEN bc2.category ELSE bc1.category END) AS category2,
    COUNT(*) as appearances
	FROM book_category bc1 USE INDEX(book_category_find_category)
	JOIN book_category bc2 USE INDEX(book_category_find_category) ON bc1.ISBN = bc2.ISBN AND bc1.category <> bc2.category
	JOIN copy ON copy.ISBN = bc2.ISBN
	JOIN borrows USE INDEX(borrowing_copy_id) ON copy.copy_id = borrows.copy_id
	GROUP BY category1, category2
ORDER BY appearances DESC
LIMIT 3;

#(3.1.7)authors who have written at least 5 books less than the author who has written
#the maximum number of books 
SELECT author_first_name, author_last_name, total_written_books
FROM (
	#total written books for every author
    SELECT author_first_name, author_last_name, COUNT(*) as total_written_books
    FROM book_author USE INDEX(book_author_full_name)
    GROUP BY author_first_name, author_last_name
) AS subquery
WHERE total_written_books <= (
    SELECT MAX(total_written_books)
    FROM (
        SELECT author_first_name, author_last_name, COUNT(*) as total_written_books
        FROM book_author USE INDEX(book_author_full_name)
        GROUP BY author_first_name, author_last_name
    ) AS max_books
) - 5
ORDER BY total_written_books DESC;

#3.2

#(3.2.1)
#show all the books of the operator's school  
SELECT title,GROUP_CONCAT(DISTINCT CONCAT(' ',author_first_name,' ', author_last_name)) AS authors
FROM book USE INDEX(book_titles)
JOIN book_author ON book.ISBN = book_author.ISBN
JOIN has_book ON has_book.ISBN = book.ISBN
JOIN library_user ON library_user.school_name=has_book.school_name 
WHERE library_user.username ='claudiafzj881376'
GROUP BY title;

#search by title,category,author
SELECT book.ISBN, title,GROUP_CONCAT(DISTINCT CONCAT(' ',author_first_name,' ', author_last_name)) AS authors, 
	GROUP_CONCAT(DISTINCT category) as categories, GROUP_CONCAT( DISTINCT key_word) as key_words 
FROM book USE INDEX(book_titles) 
JOIN book_author ON book.ISBN = book_author.ISBN 
JOIN book_category ON book_category.ISBN=book.ISBN 
JOIN book_keywords ON book_keywords.ISBN=book.ISBN 
JOIN has_book ON has_book.ISBN = book.ISBN 
JOIN library_user ON library_user.school_name=has_book.school_name 
WHERE library_user.username = 'claudiafzj881376'
AND book.title LIKE '%r%'
OR category LIKE '%r%'
OR author_first_name LIKE '%r%'
OR author_last_name LIKE '%r%'
OR CONCAT(author_first_name, ' ', author_last_name) LIKE '%r%'
OR key_word LIKE '%r%'
GROUP BY title,book.ISBN;

#search by copy
SELECT book.ISBN, title,GROUP_CONCAT(DISTINCT CONCAT(' ',author_first_name,' ', author_last_name)) AS authors, 
	GROUP_CONCAT(DISTINCT category) as categories, GROUP_CONCAT( DISTINCT key_word) as key_words 
FROM book USE INDEX(book_titles) 
JOIN book_author ON book.ISBN = book_author.ISBN 
JOIN book_category ON book_category.ISBN=book.ISBN 
JOIN book_keywords ON book_keywords.ISBN=book.ISBN
JOIN has_book ON has_book.ISBN = book.ISBN 
JOIN library_user ON library_user.school_name=has_book.school_name 
JOIN copy ON copy.ISBN=book.ISBN AND copy.school_name=library_user.school_name
WHERE library_user.username ='claudiafzj881376'
AND copy_id=1
GROUP BY title,book.ISBN;

#(3.2.2)
#all users who own at least one book and have delayed its return	
SELECT DISTINCT first_name, last_name ,borrows.copy_id, DATEDIFF(CURDATE(),due_return_date) as total_delay_days
FROM library_user USE INDEX (library_user_full_name)
JOIN borrows USE INDEX(find_username_borrows) ON library_user.username = borrows.username 
AND library_user.school_name = 'High School of Kamalasai'
WHERE return_date IS NULL
AND DATEDIFF(CURDATE(),due_return_date) > 0 #ημέρες καθυστέρησης 
AND first_name ='Annadiane'
AND last_name = 'Cordelette';

#(3.2.3)
#average rating per user
SELECT DISTINCT first_name, last_name , avg(Likert) as average_rating
FROM library_user USE INDEX (library_user_full_name,library_user_school_name )
JOIN review ON review.username= library_user.username
WHERE library_user.school_name = "High School of Kamalasai"
AND library_user.username = 'afeatherstonhaughf'
GROUP BY first_name, last_name;

#average rating for books of a certain category	
SELECT category , avg(Likert) as average_rating
FROM book_category USE INDEX(book_category_find_category)
JOIN review ON review.ISBN= book_category.ISBN
JOIN has_book USE INDEX (has_book_find_school_name) ON review.ISBN= has_book.ISBN
JOIN library_user ON  has_book.school_name = library_user.school_name
WHERE library_user.school_name = "High School of Kamalasai"
AND category = 'History'
GROUP BY category;

#(3.3.1)					
#show all the books that the user's school have  
SELECT title,GROUP_CONCAT(DISTINCT CONCAT(' ',author_first_name,' ', author_last_name)) AS authors, 
	GROUP_CONCAT(DISTINCT category) as categories, GROUP_CONCAT( DISTINCT key_word) as key_words 
FROM book USE INDEX(book_titles) 
JOIN book_author USE INDEX(book_author_full_name) ON book.ISBN = book_author.ISBN 
JOIN book_category USE INDEX(book_category_find_category) ON book_category.ISBN=book.ISBN 
JOIN book_keywords ON book_keywords.ISBN=book.ISBN 
JOIN has_book USE INDEX(has_book_find_school_name) ON has_book.ISBN = book.ISBN 
JOIN library_user USE INDEX(library_user_school_name) ON library_user.school_name=has_book.school_name 
WHERE library_user.username = '%r%' 
AND book.title LIKE '%r%' 
OR category LIKE '%r%' 
OR author_first_name LIKE '%r%'
OR author_last_name LIKE '%r%'
OR CONCAT(author_first_name, ' ', author_last_name) LIKE '%r%'
OR key_word LIKE '%r%'
GROUP BY title;


#(3.3.2) books a user has borrowed and state of the borrowing for each one
SELECT title, borrowing_date, due_return_date,
    CASE
        WHEN borrows.return_date IS NULL THEN 'Pending return'
        ELSE 'Returned'
    END AS state
FROM book USE INDEX (book_titles)
JOIN copy ON book.ISBN = copy.ISBN
JOIN borrows USE INDEX (borrowing_copy_id,find_username_borrows) ON borrows.copy_id = copy.copy_id
JOIN library_user ON library_user.username = borrows.username
WHERE library_user.username = 'bbullang'
ORDER BY borrowing_date DESC;
