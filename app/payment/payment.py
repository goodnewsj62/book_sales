from flask import Blueprint, render_template,request,url_for,redirect
from app import db
from app.models import *
from .form import PaymentForm

payment = Blueprint("payment",__name__)

#your request handles here with @core.route()

@payment.route('/home', methods=['GET'])
@payment.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@payment.route('/place-order', methods=['GET','POST'])
def preorder():
    form = PaymentForm()
    if form.validate_on_submit():
        payment_details=  Payment.payment_exists(form.email.data,form.phone.data)
        if not payment_details:
            payment_details = Payment(amount= 1500,names= form.names.data,email=form.email.data,phone=form.phone.data)
            db.session.add(payment_details)
            db.session.commit()
        return redirect(url_for('payment.paypage',ref = payment_details.ref))
    return render_template('order.html',form=form)

@payment.route('/payment/<string:ref>',methods=["GET","POST"])
def paypage(ref):
    payment_details = Payment.query.filter(Payment.ref == ref).first()
    return render_template('proceed.html',payment_details =payment_details)


@payment.route('/verifypayment',methods=["GET"])
def verify():
    ref = request.values.get("ref")
    verified = Payment.query.filter_by(ref=ref).first().verify_payment()
    if verified:
        return redirect(url_for("payment.payment_result",status="success"))
    return redirect(url_for('payment.payment_result',status="failed"))


@payment.route('/payment-result/<string:status>',methods=["GET"])
def payment_result(status):
    return render_template("paymentresult.html",status=status)



