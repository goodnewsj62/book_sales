from flask import Blueprint
from app import login_manager
from ..models import Admin

auth = Blueprint("auth",__name__)

@login_manager.user_loader
def load_user(user_id):
    return Admin.filter_by(id = user_id).first()