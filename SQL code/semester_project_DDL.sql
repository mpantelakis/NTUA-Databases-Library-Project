CREATE DATABASE Library;
USE Library;

#update book set image="https://www.treasurehunt.gr/7/images/books/book_9.jpg";
CREATE TABLE school_unit (
    school_name VARCHAR(30) NOT NULL,
    street_name VARCHAR(20) NOT NULL,
    street_number INT NOT NULL,
    city VARCHAR(20) NOT NULL,
    zip_code INT UNSIGNED NOT NULL ,
    phone_number VARCHAR(10) NOT NULL,
    email VARCHAR(30) NOT NULL,
    director_first_name VARCHAR(20) NOT NULL,
    director_last_name VARCHAR(20) NOT NULL,
    lib_operator_first_name VARCHAR(20) NOT NULL,
    lib_operator_last_name VARCHAR(20) NOT NULL,
    primary key (school_name),
    unique(email,phone_number),
    CONSTRAINT chk_zip_code check(zip_code>9999 and zip_code<100000),
    CONSTRAINT chk_school_phone CHECK (phone_number REGEXP '^[0-9]{10}$')
);

CREATE TABLE library_user (
    username varchar(20) NOT NULL,
    password VARCHAR(16) NOT NULL,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    birth_date DATE,
    age TINYINT,
    email VARCHAR(40) NOT NULL,
    phone_number VARCHAR(10) NOT NULL,
    school_name VARCHAR(40) NOT NULL,
    approved BOOLEAN default false,
    unique(email,phone_number),
    primary key (username),
    CONSTRAINT fk_user_school_name foreign key (school_name) references school_unit(school_name) on delete cascade on update cascade,
    CONSTRAINT chk_user_phone CHECK (phone_number REGEXP '^[0-9]{10}$'),
    CONSTRAINT chk_password_length CHECK (length(password)>=4)
);

CREATE TABLE admin (
    admin_username varchar(20) NOT NULL,
    password VARCHAR(16) NOT NULL,
    first_name VARCHAR(20) NOT NULL,
    last_name VARCHAR(20) NOT NULL,
    email VARCHAR(30) NOT NULL,
    phone_number VARCHAR(10) NOT NULL,
    primary key (admin_username),
    CONSTRAINT chk_admin_phone CHECK (phone_number REGEXP '^[0-9]{10}$')
);

CREATE TABLE student (
    student_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL,
    primary key (student_id),
    CONSTRAINT fk_student_username foreign key (username) references library_user(username) on delete cascade on update cascade
);

CREATE TABLE professor (
    prof_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL,
    primary key (prof_id),
    CONSTRAINT fk_prof_username foreign key (username) references library_user(username) on delete cascade on update cascade
);

CREATE TABLE library_operator(
	lib_op_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    prof_id INT UNSIGNED NOT NULL,
    primary key (lib_op_id),
    CONSTRAINT fk_lib_op_prof_id foreign key (prof_id) references professor(prof_id) on delete cascade on update cascade
);

CREATE TABLE book (
    ISBN VARCHAR(10) NOT NULL,
    title VARCHAR(100) NOT NULL,
    publisher VARCHAR(50) NOT NULL,
    num_of_pages INT UNSIGNED NOT NULL,
    abstract TEXT NOT NULL,
    total_copies INT UNSIGNED NOT NULL DEFAULT 0,
    image VARCHAR(1000),
    language VARCHAR(20),
    primary key(ISBN),
    CONSTRAINT chk_ISBN CHECK (ISBN REGEXP '^[0-9]{10}$')
);

CREATE TABLE book_author (
    ISBN VARCHAR(10) NOT NULL ,
    author_first_name VARCHAR(20) NOT NULL,
    author_last_name VARCHAR(20) NOT NULL,
    primary key (ISBN,author_first_name,author_last_name),
    CONSTRAINT fk_author_ISBN foreign key (ISBN) references book(ISBN)  on delete cascade on update cascade
);

CREATE TABLE book_category (
    ISBN VARCHAR(10) NOT NULL,
    category VARCHAR(50) NOT NULL ,
    primary key (ISBN, category),
    CONSTRAINT chk_book_category check(category in ('Fiction', 'Non-fiction', 'Romance', 'Mystery', 'Thriller', 'Horror', 'Science Fiction', 'Fantasy', 'Historical Fiction', 'Biography', 'Autobiography','Dystopian','Satire',
     'Memoir', 'History', 'Art', 'Photography', 'Travel', 'Religion', 'Philosophy', 'Psychology', 'Sociology', 'Politics', 'Science', 'Technology', 'Business', 'Self-help', 'Cookbook', "Children book",'Magical Realism', 
     'Young Adult', 'Comics and Graphic Novel', 'Poetry', 'Drama', 'Educational', 'Reference', 'Dictionary', 'Encyclopedia', 'Almanac', 'Atlas', 'Thesaurus', 'Language Learning', 'Test preparation', 'Music', 'Coming of Age')),
    CONSTRAINT fk_categ_ISBN foreign key (ISBN) references book(ISBN) on delete cascade on update cascade
);

CREATE TABLE book_keywords (
    ISBN VARCHAR(10) NOT NULL ,
    key_word VARCHAR(20) NOT NULL,
    primary key (ISBN,key_word),
    CONSTRAINT fk_keyword_ISBN foreign key (ISBN) references book(ISBN) on delete cascade on update cascade
);

CREATE TABLE adds (
    ISBN VARCHAR(10) NOT NULL,
    lib_op_id INT UNSIGNED NOT NULL,
    primary key (ISBN,lib_op_id),
    CONSTRAINT fk_adds_ISBN foreign key (ISBN) references book(ISBN) on delete cascade on update cascade,
    CONSTRAINT fk_adds_lib_op_id foreign key (lib_op_id) references library_operator(lib_op_id)
);

CREATE TABLE has_book (
    ISBN VARCHAR(10) NOT NULL,
    school_name VARCHAR(30) NOT NULL,
    total_school_copies INT NOT NULL DEFAULT 0,
    available_copies INT NOT NULL DEFAULT 0,
    primary key (ISBN,school_name),
    CONSTRAINT fk_has_book_ISBN foreign key (ISBN) references book(ISBN) on delete cascade on update cascade,
    CONSTRAINT fk_has_book_school_name foreign key (school_name) references school_unit(school_name) on delete cascade on update cascade
);

CREATE TABLE copy (
    copy_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    ISBN VARCHAR(10) NOT NULL,
    school_name VARCHAR(30) NOT NULL,
    borrowed BOOLEAN NOT NULL DEFAULT false,
    reserved BOOLEAN NOT NULL DEFAULT false,
    primary key(copy_id),
    CONSTRAINT fk_copy_school_name foreign key (school_name) references school_unit(school_name) on delete cascade on update cascade,
    CONSTRAINT fk_copy_ISBN foreign key (ISBN) references book(ISBN) on delete cascade on update cascade
);

CREATE TABLE review (
    review_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    Likert TINYINT UNSIGNED NOT NULL,
    review_text TEXT NOT NULL,
    approved BOOLEAN NOT NULL DEFAULT false,
    ISBN VARCHAR(10) NOT NULL,
    username VARCHAR(20) NOT NULL,
    primary key (review_id),
    CONSTRAINT chk_likert check (Likert>=1 and Likert<=5),
    CONSTRAINT fk_review_ISBN foreign key (ISBN) references book(ISBN),
    CONSTRAINT fk_review_username foreign key (username) references library_user(username) on delete cascade on update cascade
);

CREATE TABLE borrows (
	borrowing_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL,
    copy_id INT UNSIGNED NOT NULL,
    borrowing_date DATE NOT NULL,
    return_date DATE,
    due_return_date DATE NOT NULL,
    lib_op_id INT UNSIGNED NOT NULL,
    primary key (borrowing_id), 
    CONSTRAINT fk_borrows_username foreign key (username) references library_user(username) on delete cascade on update cascade,
    CONSTRAINT fk_borrows_copy_id foreign key (copy_id) references copy(copy_id) on delete cascade on update cascade,
    CONSTRAINT fk_borrowed_by_lib_op foreign key (lib_op_id) references library_operator(lib_op_id)
);

CREATE TABLE reserves (
	reservation_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    username VARCHAR(20) NOT NULL,
    copy_id INT UNSIGNED NOT NULL,
    reservation_date DATE NOT NULL,
    cancellation_date DATE,
    approved BOOLEAN NOT NULL DEFAULT false,
    primary key (reservation_id), 
    CONSTRAINT fk_reserves_username foreign key (username) references library_user(username) on delete cascade on update cascade, 
    CONSTRAINT fk_reserves_copy_id foreign key (copy_id) references copy(copy_id) on delete cascade on update cascade
);

#indexes
CREATE INDEX book_titles ON book(title);
CREATE INDEX library_user_full_name ON library_user (first_name,last_name);
CREATE INDEX library_user_school_name ON library_user(school_name);
CREATE INDEX find_professor_username ON professor(username);
#για το copy
CREATE INDEX copy_find_ISBN ON copy(ISBN);
CREATE INDEX copy_find_school_name ON copy(school_name);
#για το borrows
CREATE INDEX find_username_borrows ON borrows(username);
CREATE INDEX borrowing_copy_id ON borrows(copy_id);
#όμοια για το reserves 
CREATE INDEX find_username_reserves ON reserves(username);
CREATE INDEX reserved_copy_id ON reserves(copy_id);


#χρησιμοποιείται στο view το library_operator.prof_id
CREATE INDEX lib_op_prof_id ON library_operator(prof_id);
#ΓΙΑ ΤΑ TABLES ΠΟΥ ΈΧΟΥΝ COMPOSITE PRIMARY KEYS
#για το table book_author by default δημιουργειται index για αναζήτηση (ISBN),(ISBN, author_first_name),(ISBN,author_first_nane,author_last_name) 
#επομένως φτιάχνουμε index για το full name του
CREATE INDEX book_author_full_name ON book_author(author_first_name, author_last_name);  #!!!
#στο table book_category έχουμε composite primary key(ISBN,category), επομένως η mySQL by default θα φτιάξει index
#για το ISBN και για το ζεύγος (ISBN,category). Συνεπώς φτιάχνουμε ένα index για το category 
CREATE INDEX book_category_find_category ON book_category(category);
#ομοίως για το table has_book που έχει composite primary key τα (ISBN,school_name)
CREATE INDEX has_book_find_school_name ON has_book(school_name);


#views

#βρίσκουμε τα ονόματα των σχολείων όλων των op και ποιος ειναι ο operator στο καθένα			!!!
CREATE VIEW operators_school_name
(school_name,lib_op_id)
AS
SELECT school_name, lib_op_id
    FROM library_operator USE INDEX(lib_op_prof_id)
    JOIN professor USE INDEX(find_professor_username) ON library_operator.prof_id = professor.prof_id 
    JOIN library_user ON professor.username = library_user.username;
