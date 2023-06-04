from flask import Flask, render_template, request, flash, redirect, url_for, abort, session
from flask_mysqldb import MySQL
from library import db ## initially created by __init__.py, needs to be used here
from library.schools import schools
from library.schools.forms import SchoolForm

@schools.route("/schools")
def getSchools():
    """
    Retrieve schools from the database
    """
    try:

        cur = db.connection.cursor()
        query = "SELECT school_name, street_name,street_number,city,zip_code,phone_number,email,director_first_name,director_last_name, lib_operator_first_name, lib_operator_last_name FROM school_unit;"
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        schools= [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("schools.html", pageTitle="School Units", home_name="Home", schools=schools, condition="admin")
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/admin_page")

@schools.route("/schools/add", methods = ["GET", "POST"]) ## "GET" by default
def addSchool():
    """
    Create new school unit in the database
    
    """
    form = SchoolForm()

    if(request.method == "POST" and form.validate_on_submit()):

        newSchool = form.__dict__
        query = "INSERT INTO school_unit (school_name, street_name, street_number, city, zip_code, phone_number, email, director_first_name, director_last_name, lib_operator_first_name, lib_operator_last_name) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(
            newSchool['name'].data, newSchool['street_name'].data, newSchool['street_number'].data, newSchool['city'].data,
            newSchool['zip_code'].data, newSchool['phone_number'].data, newSchool['email'].data, newSchool['director_first_name'].data,
            newSchool['director_last_name'].data, newSchool['library_operator_first_name'].data, newSchool['library_operator_last_name'].data)

        try:
            cur = db.connection.cursor()
            cur.execute(query)                     
            db.connection.commit()
            cur.close()
            flash("New school unit created successfully!", "success")
            return redirect("/schools")
        except Exception as e: ## OperationalError
            flash(str(e), "danger")
            print(str(e))
            return redirect("/admin_page")
    # else, response for GET request
    else:
        try:      
            return render_template("school_form.html", pageTitle = "Add a new school unit", form = form, home_name="Home", condition="admin")
        except Exception as e: ## OperationalError
            flash(str(e), "danger")
            return redirect("/admin_page")

@schools.route("/schools/edit/<schoolName>", methods=["POST"])
def editSchool(schoolName):
    """
    Change school information by school name in the database
    """
    # Retrieve the updated information from the form
    new_street_name = request.form.get('new_street_name')
    new_street_number = request.form.get('new_street_number')
    new_city = request.form.get('new_city')
    new_zip_code = request.form.get('new_zip_code')
    new_phone_number = request.form.get('new_phone_number')
    new_email = request.form.get('new_email')
    new_director_first_name = request.form.get('new_director_first_name')
    new_director_last_name = request.form.get('new_director_last_name')
    new_lib_operator_first_name = request.form.get('new_library_operator_first_name')
    new_lib_operator_last_name = request.form.get('new_library_operator_last_name')

    # Print the new attribute values
    print("New Street Name:", new_street_name)
    print("New Street Number:", new_street_number)
    print("New City:", new_city)
    print("New ZIP Code:", new_zip_code)
    print("New Phone Number:", new_phone_number)
    print("New Email:", new_email)
    print("New Director's First Name:", new_director_first_name)
    print("New Director's Last Name:", new_director_last_name)
    print("New Library Operator's First Name:", new_lib_operator_first_name)
    print("New Library Operator's Last Name:", new_lib_operator_last_name)

    query = """
        UPDATE school_unit
        SET street_name=%s, street_number=%s, city=%s, zip_code=%s,
            phone_number=%s, email=%s, director_first_name=%s, director_last_name=%s,
            lib_operator_first_name=%s, lib_operator_last_name=%s
        WHERE school_name=%s;
    """

    try:
        cur = db.connection.cursor()
        cur.execute(query, (
            new_street_name, new_street_number, new_city, new_zip_code,
            new_phone_number, new_email, new_director_first_name, new_director_last_name,
            new_lib_operator_first_name, new_lib_operator_last_name, schoolName,
        ))
        db.connection.commit()
        cur.close()
        flash("School information updated successfully", "success")
        return redirect("/schools")  # Redirect to the schools listing page
    except Exception as e:
        flash(str(e), "danger")
        return redirect("/schools")


