from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import User
from flask_login import login_required, current_user, logout_user
import os
from werkzeug.utils import secure_filename

bp = Blueprint('main', __name__)

# Разрешенные расширения для аватарок
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        # Валидация данных
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        bio = request.form.get('bio', '').strip()
        
        # Проверка обязательных полей
        if not username or not email:
            flash('Имя пользователя и email обязательны для заполнения', 'error')
            return render_template('profile.html')
        
        # Проверка длины
        if len(username) < 3 or len(username) > 64:
            flash('Имя пользователя должно быть от 3 до 64 символов', 'error')
            return render_template('profile.html')
        
        if len(bio) > 500:
            flash('Описание не должно превышать 500 символов', 'error')
            return render_template('profile.html')
        
        # Проверка уникальности username (если изменилось)
        if username != current_user.username:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user and existing_user.id != current_user.id:
                flash('Это имя пользователя уже занято', 'error')
                return render_template('profile.html')
        
        # Проверка уникальности email (если изменилось)
        if email != current_user.email:
            existing_email = User.query.filter_by(email=email).first()
            if existing_email and existing_email.id != current_user.id:
                flash('Этот email уже используется', 'error')
                return render_template('profile.html')
        
        # Обработка загрузки аватарки
        if 'avatar' in request.files:
            file = request.files['avatar']
            if file and file.filename != '' and allowed_file(file.filename):
                current_user.save_avatar(file)
        
        # Обновление данных пользователя
        current_user.username = username
        current_user.email = email
        current_user.bio = bio
        
        db.session.commit()
        flash('Профиль успешно обновлен!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('profile.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы', 'success')
    return redirect(url_for('main.index'))

@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404