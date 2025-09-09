import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from app.config import Config
from sqlalchemy import inspect

# Инициализация расширений
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Инициализация расширений с приложением
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)  # Инициализация CSRF защиты
    
    # Импорт моделей после инициализации db
    from app import models
    
    # Настройка login_manager
    from app.models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'
    login_manager.login_message_category = 'info'
    
    # Регистрация blueprint'ов
    from app.routes.main import bp as main_bp
    from app.routes.auth import bp as auth_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # Автоматическое создание таблиц при запуске приложения
    with app.app_context():
        inspector = inspect(db.engine)
        tables_exist = inspector.has_table('user')
        
        if not tables_exist:
            db.create_all()
            print("✅ База данных создана!")
        else:
            print("✅ База данных уже существует")
    
    # === Проверка папок для пользователей ===
    usersdata_path = os.path.join(app.static_folder, "usersdata")
    avatars_path = os.path.join(usersdata_path, "avatars")

    os.makedirs(avatars_path, exist_ok=True)  # создаст обе папки, если их нет

    print(f"📂 Папка для аватарок готова: {avatars_path}")
    
    return app
