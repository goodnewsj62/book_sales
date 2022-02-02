from flask import Blueprint, jsonify, redirect, render_template,request, url_for
from flask_login import login_required,login_user,current_user
from flask_sqlalchemy import Pagination

from app import login_manager,pwd_context
from app.auth.form import LoginForm
from ..models import Admin,Payment
from ..payment.verify_payment import Verify

auth = Blueprint("auth",__name__,url_prefix='/auth')

login_manager.login_view = 'auth.login'
login_manager.login_message = "please login to access this page"

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.filter_by(id = user_id).first()


@auth.route('/',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Admin.query.filter_by(username = form.username.data).first()
        if user and pwd_context.verify(form.password.data,user.password):
            login_user(user=user,remember=True)
            return redirect(url_for('auth.db_admin'))
    return render_template('login.html', form=form)

@auth.route('/admin', methods=["GET"])
@login_required
def admin():
    page = request.values.get("page",1,int)
    class_object = Verify()
    data = class_object.list_transactions(page)
    data= data["data"] if data["status"] else False
    next_ = url_for('auth.admin') + f"?page={page + 1}" if  class_object.list_transactions(page + 1)["data"] else False
    prev_ = url_for('auth.admin') + f"?page={page -1}"  if page > 1 and  class_object.list_transactions(page - 1) else False
    return render_template('admin.html',db_admin=False,data=data,next_page=next_,prev_page=prev_)


@auth.route('/admin/local', methods=["GET"])
@login_required
def db_admin():
    page = request.values.get("page",1,int)
    records= Payment.query.filter_by(verified = True).paginate(page=page,per_page=50)
    next_ = url_for('auth.db_admin') + f"?page={records.next_num}" if records.has_next else False
    prev_ = url_for('auth.db_admin') + f"?page={records.prev_num}" if records.has_prev else False
    return render_template('admin.html',db_admin = True,data=records.items,next_page=next_,prev_page=prev_)