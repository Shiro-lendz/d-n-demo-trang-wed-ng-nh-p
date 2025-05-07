from flask import Blueprint, render_template, request, flash, redirect, url_for ,session
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask import session

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])  
def login():
    print("Rendering login page")
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        password = request.form.get('password')
        
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                session['user_id'] = user.id
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html")

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        error = False

        # Kiểm tra điều kiện và flash message
        if user:
            flash('Email đã tồn tại!', category='error')
            error = True
        elif len(email) < 4:
            flash('Email phải dài hơn 3 ký tự.', category='error')
            error = True
        elif len(first_name) < 2:
            flash('Tên phải dài hơn 1 ký tự.', category='error')
            error = True
        elif password1 != password2:
            flash('Mật khẩu không khớp.', category='error')
            error = True
        elif len(password1) < 6:
            flash('Mật khẩu phải ít nhất 6 ký tự.', category='error')
            error = True

        if not error:
            new_user = User(
                email=email, 
                first_name=first_name, 
                password=generate_password_hash(password1)
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Tạo tài khoản thành công!', category='success')
            return redirect(url_for('auth.login'))  # Redirect đến login

    return render_template("sign_up.html")


@auth.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))
