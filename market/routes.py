from market import app
from flask import render_template, redirect,url_for,flash,request
from market.models import Item, User
from market.form import PurchaseForm, RegisterForm, LoginForm, SellForm, AddItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market',methods = ['GET','POST'])
@login_required
def market():
    forms = PurchaseForm()
    sell_form = SellForm()
    if request.method == "POST":

        # Purchase 
        item_bought = (request.form.get('purchase_item'))
        if item_bought:
            item_obj = Item.query.filter_by(name=item_bought).first()
            #print(item_obj.name)
            if current_user.can_purchase(item_obj):
                item_obj.buy(current_user)
                flash(f"Congratulations! You purchased {item_obj.name} for {item_obj.price}$", category='success')
            else:
                flash(f"Please add money to buy {item_obj.name}", category='danger')


        # Sell
        item_sold = (request.form.get('sell_item'))
        if item_sold:
            sold_item_obj = Item.query.filter_by(name=item_sold).first()
            #print(sold_item_obj.name)
            if current_user.can_sell(sold_item_obj):
                sold_item_obj.sell(current_user)
                flash(f"Congratulations! You sold {sold_item_obj.name} for {sold_item_obj.price}$", category='success')
            else:
                flash(f"Transaction for {sold_item_obj.name} could not complete!", category='danger')



        return redirect(url_for('market'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        items_owned = Item.query.filter_by(owner=current_user.id)                  
        return render_template('market.html',item = items, forms=forms, sell_form=sell_form,items_owned = items_owned )

@app.route('/register', methods = ['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email_address=form.email.data,
                    password=form.password1.data)
        db.session.add(user)
        db.session.commit()
 
        login_user(user)
        flash(f"Success registering, Welcome {user.username}" , category = "success")
        return redirect(url_for("market"))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category = "danger")
    return render_template('register.html',form = form)


@app.route('/login', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        attempt_user = User.query.filter_by(username=form.username.data).first()
        if attempt_user and attempt_user.password_check(password_attempt=form.password.data):

            login_user(attempt_user)
            flash(f"Success logging in, Welcome {attempt_user.username}" , category = "success")
            return redirect(url_for("market"))
        else:
            flash(f'There was an error logging', category = "danger")
            
    
    return render_template('login.html',form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_page'))


@app.route('/additem', methods = ['GET','POST'])
@login_required
def add_item():
    form = AddItemForm()

    if form.validate_on_submit():
        item_to_add = Item(name=form.name.data,
                    price=form.price.data,
                    barcode=form.barcode.data,
                    desc=form.description.data)
        db.session.add(item_to_add)
        db.session.commit()
 
        flash(f"Success adding {item_to_add.name}" , category = "success")
        return redirect(url_for("market"))

    if form.errors != {}: #If there are errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error adding item {err_msg}', category = "danger")

    return render_template('additem.html',form=form)