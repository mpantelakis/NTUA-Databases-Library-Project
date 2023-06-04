#triggers

#trigger to calculate the age of a user
DELIMITER $$
CREATE TRIGGER ins_age
BEFORE INSERT ON library_user
FOR EACH ROW
BEGIN
    SET new.age=TIMESTAMPDIFF(YEAR,new.birth_date,CURDATE());
END$$

#trigger to increase the total copies of a book on every insert in the table copy
DELIMITER $$
CREATE TRIGGER incr_total_copies
BEFORE INSERT ON copy
FOR EACH ROW
BEGIN
	UPDATE book
    SET total_copies=total_copies+1
    WHERE ISBN=new.ISBN;
END$$

#trigger to increase the total and available copies of a book in a school on every insert in the table copy
DELIMITER $$
CREATE TRIGGER incr_school_copies
BEFORE INSERT ON copy
FOR EACH ROW
BEGIN
	UPDATE has_book
    SET available_copies=available_copies+1, total_school_copies=total_school_copies+1
    WHERE ISBN=new.ISBN and school_name=new.school_name;
END$$

#If a book is deleted from a schoool, all copies of that book to the school should be deleted as well  
DELIMITER $$
CREATE TRIGGER delete_copies
AFTER DELETE ON has_book
FOR EACH ROW 
BEGIN
	DELETE FROM copy
    WHERE ISBN=old.ISBN 
    AND school_name=old.school_name;
END$$

#checking if the user has reached the limit of maximum borrowed books in the current week
DELIMITER $$
CREATE TRIGGER borrows_max_borrowed_books_per_week
BEFORE INSERT ON borrows
FOR EACH ROW
BEGIN
    #if the user is a professor, check if there is already one active borrowing in the same week
	IF EXISTS (SELECT username FROM professor WHERE username = new.username) 
	THEN 
		IF (
			(SELECT COUNT(*)
			FROM borrows USE INDEX(find_username_borrows)
			WHERE username = NEW.username
			AND borrowing_date BETWEEN DATE_SUB(CURDATE(),INTERVAL WEEKDAY(CURDATE()) DAY) AND CURDATE()
			) > 0
		)          
		THEN
			SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'The user has already borrowed the maximum number of books allowed for this week.';
		END IF;
	#if the user is a student, check if there are already two active borrowings in the same week
	ELSEIF EXISTS (SELECT username FROM student WHERE username = new.username)
    THEN
		IF(
			(SELECT COUNT(*)
			FROM borrows USE INDEX(find_username_borrows)
			WHERE username = NEW.username
			AND borrowing_date BETWEEN DATE_SUB(CURDATE(),INTERVAL WEEKDAY(CURDATE()) DAY) AND CURDATE()
			) > 1
		)
		THEN
			SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'The user has already borrowed the maximum number of books allowed for this week.';
		END IF;
	END IF;
END$$




#checking if there available copies of a book to borrow
DELIMITER $$
CREATE TRIGGER borrows_check_availability
BEFORE INSERT ON borrows
FOR EACH ROW 
BEGIN
	IF(
		SELECT available_copies
        FROM has_book USE INDEX(has_book_find_school_name)
        WHERE school_name=(SELECT school_name FROM library_user WHERE username = new.username)
        AND ISBN = (SELECT ISBN FROM copy WHERE copy_id = new.copy_id)
	)<1
    THEN 
		SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = "There aren't currently any available copies of this book.";
	END IF;
END$$

#check if someone try to borrow a copy that is already borrowed
DELIMITER $$
CREATE TRIGGER copy_already_borrowed
BEFORE INSERT ON borrows
FOR EACH ROW
BEGIN
	IF EXISTS( 
		SELECT copy_id
		FROM copy
		WHERE copy_id=NEW.copy_id
        AND borrowed IS TRUE
	)
	THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'This copy of the book is already borrowed.';
	END IF;
END$$

#trigger to set the library operator that carried out a borrowing
DELIMITER $$
CREATE TRIGGER borrow_approved_by
BEFORE INSERT ON borrows
FOR EACH ROW 
BEGIN
    SET new.lib_op_id=	(SELECT lib_op_id
						FROM library_operator USE INDEX(lib_op_prof_id)
						JOIN professor USE INDEX(find_professor_username) ON library_operator.prof_id = professor.prof_id
						JOIN library_user ON professor.username = library_user.username
						WHERE library_user.school_name = (SELECT school_name FROM library_user WHERE username = new.username));
END$$



#if a copy of a book is borrowed then set it as borrowed
DELIMITER $$
CREATE TRIGGER borrowed
BEFORE INSERT ON borrows
FOR EACH ROW 
BEGIN
	UPDATE copy
    SET borrowed=true
    where copy_id=new.copy_id;
END$$

#if a copy of a book is returned then set it as returned
DELIMITER $$
CREATE TRIGGER returned
BEFORE UPDATE ON borrows
FOR EACH ROW 
BEGIN
	UPDATE copy
    SET borrowed=false
    where copy_id=new.copy_id;
END$$


#every time a copy of a book is borrowed from a school, the available_copies of that book in that school should decrease
DELIMITER $$
CREATE TRIGGER decr_available_copies
AFTER INSERT ON borrows
FOR EACH ROW
BEGIN
	UPDATE has_book USE INDEX(has_book_find_school_name)
    SET available_copies=available_copies-1
    WHERE school_name=(SELECT school_name FROM library_user WHERE library_user.username=new.username) 
    AND available_copies>0 
    AND ISBN=(SELECT ISBN FROM copy WHERE copy_id = NEW.copy_id);
END$$

#every time a copy of a book is returned in a school, the available_copies of that book in that school should increase
DELIMITER $$
CREATE TRIGGER incr_available_copies
BEFORE UPDATE ON borrows
FOR EACH ROW
BEGIN
	UPDATE has_book USE INDEX(has_book_find_school_name)
    SET available_copies=available_copies+1
    WHERE school_name=(SELECT school_name FROM library_user WHERE library_user.username=new.username) 
    AND ISBN=(SELECT ISBN FROM copy WHERE copy_id = NEW.copy_id)
    AND NEW.return_date!=NULL;
END$$

#when a copy is deleted from a school, check if it can be deleted and decrease total school copies and total book copies
DELIMITER $$
CREATE TRIGGER decrease_total_copies
BEFORE DELETE ON copy
FOR EACH ROW 
BEGIN
	IF EXISTS (
		SELECT borrowing_id
        FROM borrows
        WHERE copy_id = OLD.copy_id AND return_date IS NULL
    )
    THEN 
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'This copy of the book is currently borrowed. It cannot be deleted.';
    ELSE
		UPDATE book
		SET total_copies = total_copies - 1
		WHERE ISBN = (SELECT ISBN FROM copy WHERE copy_id = OLD.copy_id);
		
		UPDATE has_book
		SET total_school_copies = total_school_copies - 1, available_copies = available_copies - 1
		WHERE ISBN = OLD.ISBN AND school_name = OLD.school_name;
	END IF;
END$$



#checking if the user has reached the limit of maximum borrowed books in the current week
DELIMITER $$
CREATE TRIGGER reserves_max_borrowed_books_per_week
BEFORE INSERT ON reserves
FOR EACH ROW
BEGIN
    #if the user is a professor, check if there is already one active borrowing in the same week
	IF EXISTS (SELECT username FROM professor WHERE username = new.username) 
	THEN 
		IF (
			(SELECT COUNT(*)
			FROM borrows USE INDEX(find_username_borrows)
			WHERE username = NEW.username
			AND borrowing_date BETWEEN DATE_SUB(CURDATE(),INTERVAL WEEKDAY(CURDATE()) DAY) AND CURDATE()
			) > 0
		)          
		THEN
			SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'You have already borrowed the maximum number of books allowed for this week.';
		END IF;
	#if the user is a student, check if there are already two active borrowings in the same week
	ELSEIF EXISTS (SELECT username FROM student WHERE username = new.username)
    THEN
		IF(
			(SELECT COUNT(*)
			FROM borrows USE INDEX(find_username_borrows)
			WHERE username = NEW.username
			AND borrowing_date BETWEEN DATE_SUB(CURDATE(),INTERVAL WEEKDAY(CURDATE()) DAY) AND CURDATE()
			) > 1
		)
		THEN
			SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'You have already borrowed the maximum number of books allowed for this week.';
		END IF;
	END IF;
END$$

#checking if the user has reached the limit of maximum reservations books in the current week
CREATE TRIGGER max_reserved_books_per_week
BEFORE INSERT ON reserves
FOR EACH ROW
BEGIN
	#if the user is a professor, check if there is already one active reservation in the same week
	IF EXISTS (SELECT username FROM professor WHERE username = new.username) 
	THEN 
		IF (
            SELECT COUNT(*)
			FROM reserves USE INDEX(find_username_reserves)
			WHERE username = NEW.username
			AND reservation_date BETWEEN DATE_SUB(CURDATE(),INTERVAL WEEKDAY(CURDATE()) DAY) AND CURDATE()
            AND cancellation_date IS NULL
            ) > 0
		THEN
			SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'You have already reserved the maximum number of books allowed for this week.';
		END IF;
		#if the user is a student, check if there are already two active reservations in the same week
	ELSEIF EXISTS (SELECT username FROM student WHERE username = new.username) 
	THEN 
		IF (
            SELECT COUNT(*)
			FROM reserves USE INDEX(find_username_reserves)
			WHERE username = NEW.username
			AND reservation_date BETWEEN DATE_SUB(CURDATE(),INTERVAL WEEKDAY(CURDATE()) DAY) AND CURDATE()
            AND cancellation_date IS NULL
            ) > 1
		THEN
			SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'You have already reserved the maximum number of books allowed for this week.';
		END IF;
	END IF;
END$$

#checking if a user is trying to reserve a book that it is already being borrowed by them 
DELIMITER $$
CREATE TRIGGER book_already_borrowed
BEFORE INSERT ON reserves
FOR EACH ROW
BEGIN
	IF( 
		SELECT COUNT(*)
		FROM borrows USE INDEX(borrowing_copy_id),copy USE INDEX(copy_find_ISBN)
		WHERE username = NEW.username
        AND borrows.copy_id=copy.copy_id
		AND copy.ISBN = (SELECT ISBN FROM copy WHERE copy_id = NEW.copy_id)
		AND borrows.return_date IS NULL
		) > 0
	THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'There is already an active borrowing of the same book.';
	END IF;
END$$

#checking if a user is trying to reserve a book that it is already reserved by them 
DELIMITER $$
CREATE TRIGGER book_already_reserved
BEFORE INSERT ON reserves
FOR EACH ROW
BEGIN
	IF( 
		SELECT COUNT(*)
		FROM reserves USE INDEX(reserved_copy_id),copy USE INDEX(copy_find_ISBN)
		WHERE username = NEW.username
        AND reserves.copy_id=copy.copy_id
		AND copy.ISBN = (SELECT ISBN FROM copy WHERE copy_id = NEW.copy_id)
		AND reserves.cancellation_date IS NULL
		) > 0
	THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'There is already an active reservation of the same book.';
	END IF;
END$$

#check if someone try to reserve a copy that is already reserved
DELIMITER $$
CREATE TRIGGER copy_already_reserved
BEFORE INSERT ON reserves
FOR EACH ROW
BEGIN
	IF EXISTS( 
		SELECT copy_id
		FROM copy
		WHERE copy_id=NEW.copy_id
        AND reserved IS TRUE
	)
	THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'This copy of the book is already reserved.';
	END IF;
END$$

#if the reservation is active then set the copy as reserved
DELIMITER $$
CREATE TRIGGER set_reserved_copy
AFTER INSERT ON reserves
FOR EACH ROW
BEGIN
	IF new.cancellation_date IS NULL
    THEN 
		UPDATE copy
		SET reserved=true
		WHERE copy_id=new.copy_id;
	END IF;
END$$

#If reservation is cancelled, deactivate it and the set the copy available again  
DELIMITER $$
CREATE TRIGGER deactivate_reservation
BEFORE UPDATE ON reserves
FOR EACH ROW
BEGIN
	IF new.cancellation_date=CURDATE()	
    THEN
		UPDATE copy
		SET reserved=false
		WHERE copy_id=new.copy_id;
		END IF;
END$$

#if the reservation is approved then add it to the borrowings, deactivate the reservation, set the book borrowed and the cancellation date as the current date
DELIMITER $$
CREATE TRIGGER reservation_to_borrowing 
BEFORE UPDATE ON reserves
FOR EACH ROW 
BEGIN
	IF new.approved=true
    THEN insert into borrows (username, copy_id, borrowing_date,lib_op_id) values (new.username, new.copy_id, CURDATE(),
		(SELECT lib_op_id
		FROM library_operator USE INDEX(lib_op_prof_id)
		JOIN professor USE INDEX(find_professor_username) ON library_operator.prof_id = professor.prof_id
		JOIN library_user USE INDEX(library_user_school_name) ON professor.username = library_user.username
		WHERE library_user.school_name = (SELECT school_name FROM library_user WHERE username = new.username)));
		
        SET new.cancellation_date=CURDATE();
        
        UPDATE copy
		SET reserved=false
		WHERE copy_id=new.copy_id;
        
        UPDATE copy
		SET borrowed=true
		WHERE copy_id=new.copy_id;
	END IF;
END$$









#events

#check every day for reservations that need to be cancelled
CREATE EVENT check_reservation_status
ON SCHEDULE
    EVERY 1 day
    STARTS CURRENT_TIMESTAMP
DO
    UPDATE reserves
    SET cancellation_date=CURDATE()
    WHERE DATEDIFF(CURDATE(),reservation_date) > 7 AND cancellation_date IS NULL;

#increase user's age when they have their birthdays       !!!!!!
CREATE EVENT increase_user_age
ON SCHEDULE 
	EVERY 1 DAY
	STARTS CURRENT_TIMESTAMP
DO
    UPDATE library_user
    SET age = age + 1
    WHERE DATE_FORMAT(birth_date, '%m-%d') = DATE_FORMAT(CURRENT_DATE, '%m-%d');
      