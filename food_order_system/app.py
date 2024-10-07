from flask import Flask, render_template, request, redirect, flash, url_for, session as flask_session  # Renamed import
from DBmain import *
from sqlalchemy.orm import sessionmaker, joinedload

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Create a database session
DatabaseSession = sessionmaker(bind=engine)  # Avoid using 'session'
database_session = DatabaseSession()  # Use 'database_session'

def get_total_items():
    username = flask_session.get('username')
    if not username:
        flash('Trebuie să te loghezi pentru a adauga in coș!', 'danger')
        return redirect(url_for('login'))

    user = database_session.query(User).filter_by(username=username).first()
    if not user or not user.cart:
        flash('Coșul tău este gol!', 'info')
        return render_template('cart.html', cart=[], total=0, total_items=0)

    cart_items = database_session.query(CartItem).options(joinedload(CartItem.menu_item)).filter_by(
        cart_id=user.cart.id).all()

    total_items = sum(ci.quantity for ci in cart_items)

    return total_items


@app.route("/")
def home():
    total_items = get_total_items()
    if 'username' in flask_session:
        username = flask_session['username']
        return render_template('homepage.html', logged_in=True, username=username, total_items=total_items)
    return render_template('homepage.html', logged_in=False, total_items=total_items)


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the user from the database
        user = database_session.query(User).filter_by(username=username).first()
        if user and user.password == password:  # Ensure you're checking the user object
            flask_session['username'] = username  # Store username in Flask session
            flash("Successfully logged in!", "success")
            return redirect(url_for('home'))
        flash("Invalid username or password!", "danger")
    return render_template('login.html')

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        email = request.form.get('email')

        if database_session.query(User).filter_by(username=username).first():
            flash("Username already exists. Please choose another one.", "danger")
        elif password != confirm_password:
            flash("Passwords do not match!", 'danger')
        else:
            new_user = User(username=username, password=password, email=email)
            database_session.add(new_user)
            database_session.commit()
            flash('Account created successfully! Please log in!', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route("/reset_password", methods=['POST', 'GET'])
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        user = database_session.query(User).filter_by(email=email).first()
        if user:
            flash('A reset link has been sent to your email (simulated)!', 'success')
            return redirect(url_for("login"))
        flash('Email not found', 'danger')
    return render_template('reset_password.html')

@app.route('/profile')
def profile():
    if 'username' not in flask_session:
        flash('You need to login first!', 'danger')
        return redirect(url_for('login'))

    username = flask_session['username']  # Use the renamed session variable
    return render_template('profile.html', username=username)

@app.route("/logout")
def logout():
    flask_session.pop('username', None)
    flash('You have been logged out!', 'success')
    return redirect(url_for('home'))

@app.route("/aperitive_garnituri")
def aperitive_garnituri():
    appetizers = database_session.query(MenuItem).filter_by(category_id=1).all()
    total_items = get_total_items()
    return render_template('aperitive_garnituri.html', meniu=appetizers, total_items=total_items)

@app.route("/bunatati_din_carne")
def bunatati_din_carne():
    meat_dishes = database_session.query(MenuItem).filter_by(category_id=2).all()
    total_items = get_total_items()
    return render_template('bunatati_din_carne.html', meniu=meat_dishes, total_items=total_items)

@app.route("/bunatati_vegetariene")
def bunatati_vegetariene():
    vegetarian_dishes = database_session.query(MenuItem).filter_by(category_id=3).all()
    total_items = get_total_items()
    return render_template('bunatati_vegetariene.html', meniu=vegetarian_dishes, total_items=total_items)

@app.route("/deserturi")
def deserturi():
    desserts = database_session.query(MenuItem).filter_by(category_id=4).all()
    total_items = get_total_items()
    return render_template('deserturi.html', meniu=desserts, total_items=total_items)


@app.route("/salate")
def salate():
    salads = database_session.query(MenuItem).filter_by(category_id=5).all()
    total_items = get_total_items()
    return render_template('salate.html', meniu=salads, total_items=total_items)

@app.route("/supe_ciorbe")
def supe_ciorbe():
    soups = database_session.query(MenuItem).filter_by(category_id=6).all()
    total_items = get_total_items()
    return render_template('supe_ciorbe.html', meniu=soups, total_items=total_items)

@app.route("/meniu")
def show_meniu():
    all_items = database_session.query(MenuItem).all()
    total_items = get_total_items()
    return render_template('meniu.html', meniu=all_items, total_items=total_items)

@app.route("/add_to_cart", methods=['POST'])
def add_to_cart():
    username = flask_session.get('username')
    if not username:
        flash('Trebuie să te loghezi pentru a adăuga articole în coș!', 'danger')
        return redirect(url_for('login'))

    user = database_session.query(User).filter_by(username=username).first()
    if not user:
        flash('Utilizatorul nu a fost găsit!', 'danger')
        return redirect(url_for('login'))

    # Asigură-te că utilizatorul are un coș
    if not user.cart:
        user.cart = Cart(user_id=user.id)
        database_session.add(user.cart)
        database_session.commit()

    cart = user.cart

    item_id = request.form.get('item_id', type=int)
    quantity = request.form.get('quantity', default=1, type=int)

    if not item_id:
        flash('Articolul nu a fost specificat corect!', 'danger')
        return redirect(url_for('show_meniu'))

    menu_item = database_session.query(MenuItem).filter_by(id=item_id).first()
    if not menu_item:
        flash('Articolul nu a fost găsit!', 'danger')
        return redirect(url_for('show_meniu'))

    # Verifică dacă CartItem există deja
    cart_item = database_session.query(CartItem).filter_by(cart_id=cart.id, menu_item_id=menu_item.id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.id, menu_item_id=menu_item.id, quantity=quantity)
        database_session.add(cart_item)

    database_session.commit()
    flash(f'{menu_item.name} a fost adăugat în coș!', 'success')
    return redirect(url_for('show_meniu'))


@app.route("/cart")
def show_cart():
    username = flask_session.get('username')
    if not username:
        flash('Trebuie să te loghezi pentru a vedea coșul!', 'danger')
        return redirect(url_for('login'))

    user = database_session.query(User).filter_by(username=username).first()
    if not user or not user.cart:
        flash('Coșul tău este gol!', 'info')
        return render_template('cart.html', cart=[], total=0, total_items=0)

    # Încarcă articolele din coș împreună cu detaliile MenuItem
    cart_items = database_session.query(CartItem).options(joinedload(CartItem.menu_item)).filter_by(cart_id=user.cart.id).all()

    # Calculează totalul
    total = sum(ci.menu_item.price * ci.quantity for ci in cart_items)

    # Calculează numărul total de articole
    total_items = sum(ci.quantity for ci in cart_items)

    return render_template('cart.html', cart=cart_items, total=total, total_items=total_items)


@app.route("/remove_from_cart", methods=['POST'])
def remove_from_cart():
    username = flask_session.get('username')
    if not username:
        flash('Trebuie să te loghezi pentru a elimina articole din coș!', 'danger')
        return redirect(url_for('login'))

    user = database_session.query(User).filter_by(username=username).first()
    if not user or not user.cart:
        flash('Coșul este gol!', 'danger')
        return redirect(url_for('show_cart'))

    item_id = request.form.get('item_id', type=int)
    if not item_id:
        flash('Articolul nu a fost specificat corect!', 'danger')
        return redirect(url_for('show_cart'))

    cart_item = database_session.query(CartItem).filter_by(cart_id=user.cart.id, menu_item_id=item_id).first()
    if cart_item:
        database_session.delete(cart_item)
        database_session.commit()
        flash('Articolul a fost eliminat din coș!', 'success')
    else:
        flash('Articolul nu este în coș!', 'danger')

    return redirect(url_for('show_cart'))


@app.route("/finish_order", methods=['POST'])
def finish_order():
    username = flask_session.get('username')
    if not username:
        flash('Trebuie să te loghezi pentru a finaliza comanda!', 'danger')
        return redirect(url_for('login'))

    user = database_session.query(User).filter_by(username=username).first()
    if not user or not user.cart:
        flash('Coșul tău este gol! Nu poți finaliza comanda.', 'danger')
        return redirect(url_for('show_cart'))

    # Create an Order
    order = Order(user_id=user.id)  # Assuming you have an Order model
    database_session.add(order)

    # Transfer items from cart to order
    cart_items = database_session.query(CartItem).filter_by(cart_id=user.cart.id).all()
    for cart_item in cart_items:
        order_item = OrderItem(order_id=order.id, menu_item_id=cart_item.menu_item_id, quantity=cart_item.quantity)
        database_session.add(order_item)

    # Clear the user's cart
    database_session.query(CartItem).filter_by(cart_id=user.cart.id).delete()

    # Optionally: Clear the cart object itself if you want
    # database_session.delete(user.cart)

    database_session.commit()

    flash('Comanda a fost finalizată cu succes! Mulțumim!', 'success')
    return redirect(url_for('show_meniu'))

@app.route("/order_history")
def order_history():
    username = flask_session.get('username')
    if not username:
        flash('Trebuie să te loghezi pentru a vedea istoricul comenzilor!', 'danger')
        return redirect(url_for('login'))

    user = database_session.query(User).filter_by(username=username).first()
    orders = database_session.query(Order).filter_by(user_id=user.id).all()  # Assuming Order is your order model

    return render_template('order_history.html', orders=orders, username=username)


if __name__ == "__main__":
    app.run(debug=True)
