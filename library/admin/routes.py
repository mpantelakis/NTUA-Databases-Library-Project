from flask import Flask, render_template, request, flash, redirect, url_for, abort,session
from flask_mysqldb import MySQL
from library import db ## initially created by __init__.py, needs to be used here
from library.admin import admin

@admin.route("/admin_page")
def admin_index():
        try:
            return render_template("admin_page.html", pageTitle = "Administration of Library Network",home_name="Home",condition="admin")
        except Exception as e: ## OperationalError
            flash(str(e), "danger")
            redirect("/")