from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from db import db


review_bp = Blueprint('review', __name__)

@review_bp.route('/')
@login_required
def reviews():
    if current_user.role != "Reviewer":
        abort(403)
    assigned_papers = list(db.papers.find({"reviewer_id": current_user.id}))
    return render_template('review.html', papers=assigned_papers)
