from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from db import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
@login_required
def admin_dashboard():
    if current_user.role != 'Admin':
        abort(403)
    users = list(db.users.find())
    papers = list(db.papers.find())
    return render_template('admin.html', users=users, papers=papers)
