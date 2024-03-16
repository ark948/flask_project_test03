from app import admin, login_manager
from flask_admin.contrib.sqla import ModelView
from flask import session, redirect, url_for, request, flash
from flask_login import current_user
from icecream import ic

class AdminView(ModelView):
    
    def is_accessible(self):
        return current_user.is_authenticated and current_user.username == "admin"

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('auth.login'))