import tkinter as tk
from tkinter import ttk, messagebox
import json
import hashlib
import os
import re
from datetime import datetime, timedelta
import random
import string
from PIL import Image, ImageTk
import threading
import time

class ModernBankApp:
    def __init__(self):
        self.users_file = "bank_users_v2.json"
        self.transactions_file = "transactions_v2.json"
        self.current_user = None
        self.load_data()
        
        # Современная цветовая схема
        self.colors = {
            'primary': '#1a237e',
            'secondary': '#303f9f',
            'accent': '#3f51b5',
            'success': '#4caf50',
            'warning': '#ff9800',
            'danger': '#f44336',
            'light': '#f5f5f5',
            'dark': '#212121',
            'background': '#f8f9fa'
        }
        
        # Создаем главное окно
        self.root = tk.Tk()
        self.root.title("Modern Bank 2.0")
        self.root.geometry("500x700")
        self.root.configure(bg=self.colors['background'])
        
        # Центрируем окно
        self.center_window(self.root, 500, 700)
        
        # Иконки (символические, можно заменить на реальные картинки)
        self.icons = {}
        self.create_icons()
        
        # Запускаем приложение
        self.show_splash_screen()
        
    def center_window(self, window, width, height):
        """Центрирование окна на экране"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_icons(self):
        """Создаем простые иконки (можно заменить на загрузку реальных изображений)"""
        # В реальном приложении здесь была бы загрузка PNG иконок
        pass
    
    def load_data(self):
        """Загружаем данные пользователей и транзакций"""
        # Пользователи
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
        else:
            self.users = {}
        
        # Транзакции
        if os.path.exists(self.transactions_file):
            with open(self.transactions_file, 'r', encoding='utf-8') as f:
                self.all_transactions = json.load(f)
        else:
            self.all_transactions = {}
    
    def save_data(self):
        """Сохраняем все данные"""
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, indent=4, ensure_ascii=False)
        with open(self.transactions_file, 'w', encoding='utf-8') as f:
            json.dump(self.all_transactions, f, indent=4, ensure_ascii=False)
    
    def validate_email(self, email):
        """Валидация email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone):
        """Валидация телефона"""
        pattern = r'^\+?[1-9]\d{10,14}$'
        phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
        return re.match(pattern, phone) is not None
    
    def validate_password(self, password):
        """Валидация пароля"""
        if len(password) < 8:
            return False, "Пароль должен содержать минимум 8 символов"
        if not re.search(r'[A-Z]', password):
            return False, "Пароль должен содержать хотя бы одну заглавную букву"
        if not re.search(r'[a-z]', password):
            return False, "Пароль должен содержать хотя бы одну строчную букву"
        if not re.search(r'\d', password):
            return False, "Пароль должен содержать хотя бы одну цифру"
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Пароль должен содержать хотя бы один специальный символ"
        return True, "Пароль надежный"
    
    def generate_card_number(self):
        """Генерация номера карты"""
        return ''.join([str(random.randint(0, 9)) for _ in range(16)])
    
    def generate_cvv(self):
        """Генерация CVV кода"""
        return ''.join([str(random.randint(0, 9)) for _ in range(3)])
    
    def hash_password(self, password):
        """Хеширование пароля с солью"""
        salt = "bank_salt_v2_"
        return hashlib.sha256((salt + password).encode()).hexdigest()
    
    def show_splash_screen(self):
        """Экран загрузки"""
        splash = tk.Toplevel(self.root)
        splash.title("Modern Bank 2.0")
        splash.geometry("400x300")
        splash.configure(bg=self.colors['primary'])
        self.center_window(splash, 400, 300)
        
        # Запрещаем закрытие
        splash.overrideredirect(True)
        
        # Заголовок
        title_label = tk.Label(
            splash,
            text="Modern Bank 2.0",
            font=("Arial", 24, "bold"),
            bg=self.colors['primary'],
            fg="white"
        )
        title_label.pack(pady=40)
        
        # Подзаголовок
        subtitle_label = tk.Label(
            splash,
            text="Ваш надежный финансовый партнер",
            font=("Arial", 12),
            bg=self.colors['primary'],
            fg=self.colors['light']
        )
        subtitle_label.pack()
        
        # Прогресс бар
        progress_frame = tk.Frame(splash, bg=self.colors['primary'])
        progress_frame.pack(pady=30)
        
        progress_bar = ttk.Progressbar(
            progress_frame,
            length=200,
            mode='indeterminate'
        )
        progress_bar.pack()
        progress_bar.start(10)
        
        # Версия
        version_label = tk.Label(
            splash,
            text="Версия 2.0",
            font=("Arial", 8),
            bg=self.colors['primary'],
            fg=self.colors['light']
        )
        version_label.pack(side="bottom", pady=10)
        
        # Закрываем сплеш и показываем основной экран
        splash.after(2000, lambda: self.close_splash(splash))
    
    def close_splash(self, splash):
        """Закрываем сплеш и показываем основной экран"""
        splash.destroy()
        self.show_main_menu()
    
    def show_main_menu(self):
        """Главное меню"""
        self.clear_window()
        
        # Заголовок
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=100)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Modern Bank 2.0",
            font=("Arial", 24, "bold"),
            bg=self.colors['primary'],
            fg="white"
        )
        title_label.pack(expand=True)
        
        # Основной контент
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Приветствие
        welcome_label = tk.Label(
            main_frame,
            text="Добро пожаловать!",
            font=("Arial", 18, "bold"),
            bg=self.colors['background'],
            fg=self.colors['dark']
        )
        welcome_label.pack(pady=20)
        
        description_label = tk.Label(
            main_frame,
            text="Выберите действие:",
            font=("Arial", 12),
            bg=self.colors['background'],
            fg=self.colors['dark']
        )
        description_label.pack(pady=10)
        
        # Кнопки
        buttons_frame = tk.Frame(main_frame, bg=self.colors['background'])
        buttons_frame.pack(pady=30)
        
        buttons = [
            ("Регистрация", self.show_registration, self.colors['success']),
            ("Вход", self.show_login, self.colors['accent']),
            ("Гость", self.show_guest_mode, self.colors['warning']),
            ("Выход", self.root.quit, self.colors['danger'])
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(
                buttons_frame,
                text=text,
                command=command,
                bg=color,
                fg="white",
                font=("Arial", 12, "bold"),
                width=20,
                height=2,
                relief="flat",
                cursor="hand2"
            )
            btn.pack(pady=10)
        
        # Статистика
        stats_frame = tk.Frame(main_frame, bg="white", relief="groove", bd=1)
        stats_frame.pack(fill="x", pady=20)
        
        stats_label = tk.Label(
            stats_frame,
            text=f"Всего пользователей: {len(self.users)}",
            font=("Arial", 10),
            bg="white",
            fg=self.colors['dark']
        )
        stats_label.pack(pady=10)
    
    def clear_window(self):
        """Очистка окна"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_registration(self):
        """Окно регистрации"""
        self.clear_window()
        
        # Заголовок
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Регистрация",
            font=("Arial", 20, "bold"),
            bg=self.colors['primary'],
            fg="white"
        )
        title_label.pack(expand=True)
        
        # Основной контент с прокруткой
        canvas = tk.Canvas(self.root, bg=self.colors['background'])
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Поля для ввода
        input_frame = tk.Frame(scrollable_frame, bg=self.colors['background'], padx=20, pady=20)
        input_frame.pack()
        
        # Словарь для хранения полей и сообщений об ошибках
        self.reg_fields = {}
        self.error_labels = {}
        
        fields = [
            ("Имя", "text", True),
            ("Фамилия", "text", True),
            ("Email", "email", True),
            ("Телефон", "tel", True),
            ("Дата рождения", "date", True),
            ("Адрес", "text", False),
            ("Пароль", "password", True),
            ("Подтверждение пароля", "password", True)
        ]
        
        for i, (label_text, field_type, required) in enumerate(fields):
            # Фрейм для поля
            field_frame = tk.Frame(input_frame, bg=self.colors['background'])
            field_frame.pack(fill="x", pady=5)
            
            # Метка
            label = tk.Label(
                field_frame,
                text=f"{label_text}{'*' if required else ''}:",
                font=("Arial", 10),
                bg=self.colors['background'],
                fg=self.colors['dark'],
                width=25,
                anchor="w"
            )
            label.pack(side="left")
            
            # Поле ввода
            if field_type == "password":
                entry = tk.Entry(field_frame, width=30, show="•", font=("Arial", 10))
            else:
                entry = tk.Entry(field_frame, width=30, font=("Arial", 10))
            
            entry.pack(side="left", padx=5)
            
            # Сохраняем поле
            self.reg_fields[label_text] = {
                'entry': entry,
                'type': field_type,
                'required': required
            }
            
            # Метка для ошибок
            error_label = tk.Label(
                field_frame,
                text="",
                font=("Arial", 8),
                bg=self.colors['background'],
                fg=self.colors['danger']
            )
            error_label.pack(side="left", padx=5)
            self.error_labels[label_text] = error_label
            
            # Валидация в реальном времени для некоторых полей
            if field_type == "email":
                entry.bind("<FocusOut>", lambda e, f=label_text: self.validate_field(f))
            elif field_type == "password" and label_text == "Пароль":
                entry.bind("<KeyRelease>", lambda e, f=label_text: self.validate_field(f))
        
        # Кнопки
        button_frame = tk.Frame(scrollable_frame, bg=self.colors['background'], pady=20)
        button_frame.pack()
        
        register_btn = tk.Button(
            button_frame,
            text="Зарегистрироваться",
            command=self.register_user,
            bg=self.colors['success'],
            fg="white",
            font=("Arial", 12, "bold"),
            width=20,
            height=2,
            cursor="hand2"
        )
        register_btn.pack(side="left", padx=10)
        
        back_btn = tk.Button(
            button_frame,
            text="Назад",
            command=self.show_main_menu,
            bg=self.colors['warning'],
            fg="white",
            font=("Arial", 12),
            width=15,
            cursor="hand2"
        )
        back_btn.pack(side="left", padx=10)
        
        # Информация о требованиях к паролю
        info_frame = tk.Frame(scrollable_frame, bg=self.colors['background'])
        info_frame.pack(pady=10)
        
        info_text = """Требования к паролю:
        • Минимум 8 символов
        • Заглавные и строчные буквы
        • Хотя бы одна цифра
        • Хотя бы один специальный символ"""
        
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 9),
            bg=self.colors['background'],
            fg=self.colors['dark'],
            justify="left"
        )
        info_label.pack()
    
    def validate_field(self, field_name):
        """Валидация поля в реальном времени"""
        field_data = self.reg_fields[field_name]
        entry = field_data['entry']
        value = entry.get().strip()
        error_label = self.error_labels[field_name]
        
        if field_name == "Email":
            if not value:
                error_label.config(text="")
            elif not self.validate_email(value):
                error_label.config(text="Неверный формат email")
            elif value in self.users:
                error_label.config(text="Email уже зарегистрирован")
            else:
                error_label.config(text="✓", fg=self.colors['success'])
        
        elif field_name == "Пароль":
            if not value:
                error_label.config(text="")
            else:
                is_valid, message = self.validate_password(value)
                if is_valid:
                    error_label.config(text="✓", fg=self.colors['success'])
                else:
                    error_label.config(text=message)
    
    def register_user(self):
        """Регистрация пользователя"""
        # Собираем данные
        user_data = {}
        errors = []
        
        for field_name, field_data in self.reg_fields.items():
            value = field_data['entry'].get().strip()
            
            # Проверка обязательных полей
            if field_data['required'] and not value:
                errors.append(f"Поле '{field_name}' обязательно для заполнения")
                continue
            
            # Валидация по типу
            if field_name == "Email":
                if not self.validate_email(value):
                    errors.append("Неверный формат email")
                elif value in self.users:
                    errors.append("Пользователь с таким email уже существует")
            
            elif field_name == "Телефон":
                if not self.validate_phone(value):
                    errors.append("Неверный формат телефона")
            
            elif field_name == "Пароль":
                is_valid, message = self.validate_password(value)
                if not is_valid:
                    errors.append(message)
            
            elif field_name == "Подтверждение пароля":
                password = self.reg_fields["Пароль"]['entry'].get().strip()
                if value != password:
                    errors.append("Пароли не совпадают")
            
            user_data[field_name] = value
        
        # Проверяем возраст
        if "Дата рождения" in user_data:
            try:
                birth_date = datetime.strptime(user_data["Дата рождения"], "%Y-%m-%d")
                age = (datetime.now() - birth_date).days // 365
                if age < 18:
                    errors.append("Минимальный возраст для регистрации - 18 лет")
            except ValueError:
                errors.append("Неверный формат даты рождения (используйте ГГГГ-ММ-ДД)")
        
        # Если есть ошибки - показываем их
        if errors:
            messagebox.showerror("Ошибки регистрации", "\n".join(errors))
            return
        
        # Создаем пользователя
        email = user_data["Email"]
        
        self.users[email] = {
            "personal_info": {
                "имя": user_data["Имя"],
                "фамилия": user_data["Фамилия"],
                "телефон": user_data["Телефон"],
                "дата_рождения": user_data.get("Дата рождения", ""),
                "адрес": user_data.get("Адрес", "")
            },
            "security": {
                "пароль": self.hash_password(user_data["Пароль"]),
                "последний_вход": None,
                "попытки_входа": 0,
                "активен": True,
                "регистрация": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            "accounts": {
                "основной": {
                    "баланс": 1000.00,
                    "валюта": "RUB",
                    "карта": self.generate_card_number(),
                    "cvv": self.generate_cvv(),
                    "срок": f"{datetime.now().year + 5}-12-31"
                }
            },
            "настройки": {
                "уведомления": True,
                "двухфакторная_аутентификация": False,
                "автовход": False
            }
        }
        
        # Сохраняем данные
        self.save_data()
        
        # Показываем успешную регистрацию
        success_window = tk.Toplevel(self.root)
        success_window.title("Регистрация успешна")
        success_window.geometry("400x300")
        success_window.configure(bg=self.colors['background'])
        self.center_window(success_window, 400, 300)
        
        tk.Label(
            success_window,
            text="✓",
            font=("Arial", 48, "bold"),
            bg=self.colors['background'],
            fg=self.colors['success']
        ).pack(pady=20)
        
        tk.Label(
            success_window,
            text="Регистрация успешна!",
            font=("Arial", 16, "bold"),
            bg=self.colors['background'],
            fg=self.colors['dark']
        ).pack()
        
        tk.Label(
            success_window,
            text=f"Ваша карта: **** **** **** {self.users[email]['accounts']['основной']['карта'][-4:]}",
            font=("Arial", 10),
            bg=self.colors['background'],
            fg=self.colors['dark']
        ).pack(pady=10)
        
        tk.Label(
            success_window,
            text="Начальный баланс: 1,000.00 ₽",
            font=("Arial", 12),
            bg=self.colors['background'],
            fg=self.colors['success']
        ).pack(pady=10)
        
        tk.Button(
            success_window,
            text="Войти",
            command=lambda: [success_window.destroy(), self.show_login()],
            bg=self.colors['accent'],
            fg="white",
            font=("Arial", 12),
            width=15,
            cursor="hand2"
        ).pack(pady=20)
    
    def show_login(self):
        """Окно входа"""
        self.clear_window()
        
        # Заголовок
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="Вход в систему",
            font=("Arial", 20, "bold"),
            bg=self.colors['primary'],
            fg="white"
        )
        title_label.pack(expand=True)
        
        # Основной контент
        main_frame = tk.Frame(self.root, bg=self.colors['background'], padx=30, pady=30)
        main_frame.pack(fill="both", expand=True)
        
        # Поля ввода
        input_frame = tk.Frame(main_frame, bg=self.colors['background'])
        input_frame.pack(pady=20)
        
        # Email
        tk.Label(
            input_frame,
            text="Email:",
            font=("Arial", 11),
            bg=self.colors['background'],
            fg=self.colors['dark']
        ).grid(row=0, column=0, sticky="w", pady=5)
        
        self.login_email = tk.Entry(input_frame, width=30, font=("Arial", 11))
        self.login_email.grid(row=0, column=1, pady=5, padx=10)
        
        # Пароль
        tk.Label(
            input_frame,
            text="Пароль:",
            font=("Arial", 11),
            bg=self.colors['background'],
            fg=self.colors['dark']
        ).grid(row=1, column=0, sticky="w", pady=5)
        
        self.login_password = tk.Entry(input_frame, width=30, font=("Arial", 11), show="•")
        self.login_password.grid(row=1, column=1, pady=5, padx=10)
        
        # Запомнить меня
        self.remember_var = tk.BooleanVar()
        remember_check = tk.Checkbutton(
            input_frame,
            text="Запомнить меня",
            variable=self.remember_var,
            bg=self.colors['background'],
            font=("Arial", 10)
        )
        remember_check.grid(row=2, column=1, sticky="w", pady=10)
        
        # Кнопки
        button_frame = tk.Frame(main_frame, bg=self.colors['background'])
        button_frame.pack(pady=20)
        
        login_btn = tk.Button(
            button_frame,
            text="Войти",
            command=self.login_user,
            bg=self.colors['success'],
            fg="white",
            font=("Arial", 12, "bold"),
            width=15,
            height=2,
            cursor="hand2"
        )
        login_btn.pack(side="left", padx=10)
        
        back_btn = tk.Button(
            button_frame,
            text="Назад",
            command=self.show_main_menu,
            bg=self.colors['warning'],
            fg="white",
            font=("Arial", 12),
            width=15,
            cursor="hand2"
        )
        back_btn.pack(side="left", padx=10)
        
        # Дополнительные ссылки
        links_frame = tk.Frame(main_frame, bg=self.colors['background'])
        links_frame.pack(pady=10)
        
        forgot_link = tk.Label(
            links_frame,
            text="Забыли пароль?",
            font=("Arial", 10),
            bg=self.colors['background'],
            fg=self.colors['accent'],
            cursor="hand2"
        )
        forgot_link.pack()
        forgot_link.bind("<Button-1>", lambda e: self.show_password_recovery())
    
    def login_user(self):
        """Авторизация пользователя"""
        email = self.login_email.get().strip()
        password = self.login_password.get()
        
        if not email or not password:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return
        
        if email not in self.users:
            messagebox.showerror("Ошибка", "Пользователь не найден")
            return
        
        user = self.users[email]
        
        # Проверяем блокировку
        if not user['security']['активен']:
            messagebox.showerror("Ошибка", "Аккаунт заблокирован. Обратитесь в поддержку.")
            return
        
        # Проверяем пароль
        if user['security']['пароль'] != self.hash_password(password):
            user['security']['попытки_входа'] += 1
            
            # Блокировка после 5 неудачных попыток
            if user['security']['попытки_входа'] >= 5:
                user['security']['активен'] = False
                self.save_data()
                messagebox.showerror("Ошибка", "Аккаунт заблокирован из-за 5 неудачных попыток входа")
                return
            
            self.save_data()
            attempts_left = 5 - user['security']['попытки_входа']
            messagebox.showerror("Ошибка", f"Неверный пароль. Осталось попыток: {attempts_left}")
            return
        
        # Сброс счетчика попыток
        user['security']['попытки_входа'] = 0
        user['security']['последний_вход'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Обновляем настройки
        if self.remember_var.get():
            user['настройки']['автовход'] = True
        
        self.save_data()
        self.current_user = email
        self.show_dashboard()
    
    def show_dashboard(self):
        """Основная панель управления"""
        self.clear_window()
        
        user = self.users[self.current_user]
        
        # Верхняя панель
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=100)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Приветствие
        welcome_label = tk.Label(
            header_frame,
            text=f"Добро пожаловать, {user['personal_info']['имя']}!",
            font=("Arial", 18, "bold"),
            bg=self.colors['primary'],
            fg="white"
        )
        welcome_label.pack(side="left", padx=20, pady=20)
        
        # Кнопка выхода
        logout_btn = tk.Button(
            header_frame,
            text="Выйти",
            command=self.logout,
            bg=self.colors['danger'],
            fg="white",
            font=("Arial", 10),
            width=10,
            cursor="hand2"
        )
        logout_btn.pack(side="right", padx=20, pady=20)
        
        # Основной контент
        main_frame = tk.Frame(self.root, bg=self.colors['background'])
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Карточки с информацией
        cards_frame = tk.Frame(main_frame, bg=self.colors['background'])
        cards_frame.pack(fill="x", pady=10)
        
        # Карточка баланса
        balance_card = tk.Frame(cards_frame, bg="white", relief="groove", bd=2)
        balance_card.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(
            balance_card,
            text="БАЛАНС",
            font=("Arial", 10, "bold"),
            bg="white",
            fg=self.colors['dark']
        ).pack(pady=10)
        
        self.balance_label = tk.Label(
            balance_card,
            text=f"{user['accounts']['основной']['баланс']:,.2f} ₽",
            font=("Arial", 24, "bold"),
            bg="white",
            fg=self.colors['success']
        )
        self.balance_label.pack(pady=10)
        
        # Карточка карты
        card_card = tk.Frame(cards_frame, bg="white", relief="groove", bd=2)
        card_card.pack(side="left", fill="both", expand=True, padx=5)
        
        tk.Label(
            card_card,
            text="КАРТА",
            font=("Arial", 10, "bold"),
            bg="white",
            fg=self.colors['dark']
        ).pack(pady=10)
        
        card_number = user['accounts']['основной']['карта']
        tk.Label(
            card_card,
            text=f"**** **** **** {card_number[-4:]}",
            font=("Arial", 14, "bold"),
            bg="white",
            fg=self.colors['dark']
        ).pack(pady=10)
        
        # Быстрые операции
        operations_frame = tk.Frame(main_frame, bg=self.colors['background'])
        operations_frame.pack(fill="x", pady=20)
        
        tk.Label(
            operations_frame,
            text="Быстрые операции:",
            font=("Arial", 14, "bold"),
            bg=self.colors['background'],
            fg=self.colors['dark']
        ).pack(anchor="w")
        
        # Кнопки операций
        buttons_grid = tk.Frame(operations_frame, bg=self.colors['background'])
        buttons_grid.pack(pady=10)
        
        operations = [
            ("Пополнить", self.deposit_money, self.colors['success']),
            ("Снять", self.withdraw_money, self.colors['warning']),
            ("Перевести", self.transfer_money, self.colors['accent']),
            ("История", self.show_transaction_history, self.colors['secondary']),
            ("Накопления", self.show_savings_module, self.colors['primary']),
            ("Кредит", self.show_credit_module, self.colors['danger'])
        ]
        
        for i, (text, command, color) in enumerate(operations):
            row = i // 3
            col = i % 3
            
            btn = tk.Button(
                buttons_grid,
                text=text,
                command=command,
                bg=color,
                fg="white",
                font=("Arial", 11, "bold"),
                width=15,
                height=2,
                cursor="hand2"
            )
            btn.grid(row=row, column=col, padx=5, pady=5)
        
        # Последние транзакции
        transactions_frame = tk.Frame(main_frame, bg="white", relief="groove", bd=1)
        transactions_frame.pack(fill="both", expand=True, pady=10)
        
        tk.Label(
            transactions_frame,
            text="Последние операции:",
            font=("Arial", 12, "bold"),
            bg="white",
            fg=self.colors['dark']
        ).pack(anchor="w", padx=10, pady=10)
        
        # Здесь будет список транзакций
        self.transactions_text = tk.Text(
            transactions_frame,
            height=8,
            bg="white",
            font=("Arial", 10)
        )
        self.transactions_text.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Загружаем последние транзакции
        self.load_recent_transactions()
    
    def load_recent_transactions(self):
        """Загружаем последние транзакции"""
        if self.current_user not in self.all_transactions:
            self.transactions_text.insert("end", "Транзакций пока нет\n")
            return
        
        transactions = self.all_transactions[self.current_user][-5:]  # Последние 5
        for trans in reversed(transactions):
            amount = trans['сумма']
            amount_str = f"+{amount:,.2f} ₽" if amount > 0 else f"{amount:,.2f} ₽"
            color = "green" if amount > 0 else "red"
            
            self.transactions_text.insert("end", f"{trans['дата']}: {trans['тип']}\n")
            self.transactions_text.insert("end", f"  {amount_str}\n", color)
            self.transactions_text.insert("end", f"  {trans['описание']}\n\n")
        
        self.transactions_text.tag_config("green", foreground="green")
        self.transactions_text.tag_config("red", foreground="red")
        self.transactions_text.config(state="disabled")
    
    def deposit_money(self):
        """Пополнение счета"""
        self.show_amount_dialog("Пополнение счета", "Введите сумму для пополнения:", "deposit")
    
    def withdraw_money(self):
        """Снятие наличных"""
        self.show_amount_dialog("Снятие наличных", "Введите сумму для снятия:", "withdraw")
    
    def transfer_money(self):
        """Перевод средств"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Перевод средств")
        dialog.geometry("400x300")
        dialog.configure(bg=self.colors['background'])
        self.center_window(dialog, 400, 300)
        
        tk.Label(
            dialog,
            text="Перевод средств",
            font=("Arial", 16, "bold"),
            bg=self.colors['background'],
            fg=self.colors['dark']
        ).pack(pady=20)
        
        # Получатель
        tk.Label(dialog, text="Email получателя:", bg=self.colors['background']).pack()
        recipient_entry = tk.Entry(dialog, width=30, font=("Arial", 11))
        recipient_entry.pack(pady=5)
        
        # Сумма
        tk.Label(dialog, text="Сумма перевода:", bg=self.colors['background']).pack()
        amount_entry = tk.Entry(dialog, width=30, font=("Arial", 11))
        amount_entry.pack(pady=5)
        
        # Комментарий
        tk.Label(dialog, text="Комментарий:", bg=self.colors['background']).pack()
        comment_entry = tk.Entry(dialog, width=30, font=("Arial", 11))
        comment_entry.pack(pady=5)
        
        def process_transfer():
            # Валидация
            recipient = recipient_entry.get().strip()
            amount_str = amount_entry.get().strip()
            comment = comment_entry.get().strip()
            
            # Проверки
            if not recipient or not amount_str:
                messagebox.showerror("Ошибка", "Заполните обязательные поля")
                return
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Ошибка", "Сумма должна быть больше 0")
                    return
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректную сумму")
                return
            
            # Проверка получателя
            if recipient == self.current_user:
                messagebox.showerror("Ошибка", "Нельзя перевести самому себе")
                return
            
            if recipient not in self.users:
                messagebox.showerror("Ошибка", "Получатель не найден")
                return
            
            # Проверка баланса
            if self.users[self.current_user]['accounts']['основной']['баланс'] < amount:
                messagebox.showerror("Ошибка", "Недостаточно средств")
                return
            
            # Проверка лимита
            if amount > 50000:
                messagebox.showerror("Ошибка", "Превышен лимит перевода (50,000 ₽)")
                return
            
            # Подтверждение
            if not messagebox.askyesno("Подтверждение", f"Перевести {amount:,.2f} ₽ пользователю {recipient}?"):
                return
            
            # Выполнение перевода
            self.users[self.current_user]['accounts']['основной']['баланс'] -= amount
            self.users[recipient]['accounts']['основной']['баланс'] += amount
            
            # Запись транзакций
            transaction = {
                'дата': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'тип': 'перевод',
                'сумма': -amount,
                'описание': f"Перевод {recipient}" + (f": {comment}" if comment else "")
            }
            
            if self.current_user not in self.all_transactions:
                self.all_transactions[self.current_user] = []
            self.all_transactions[self.current_user].append(transaction)
            
            recipient_transaction = {
                'дата': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'тип': 'перевод',
                'сумма': amount,
                'описание': f"Перевод от {self.current_user}" + (f": {comment}" if comment else "")
            }
            
            if recipient not in self.all_transactions:
                self.all_transactions[recipient] = []
            self.all_transactions[recipient].append(recipient_transaction)
            
            self.save_data()
            self.update_dashboard()
            messagebox.showinfo("Успех", "Перевод выполнен")
            dialog.destroy()
        
        tk.Button(
            dialog,
            text="Выполнить перевод",
            command=process_transfer,
            bg=self.colors['success'],
            fg="white",
            font=("Arial", 12),
            width=20,
            cursor="hand2"
        ).pack(pady=20)
    
    def show_amount_dialog(self, title, message, operation):
        """Диалог для ввода суммы"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("350x200")
        dialog.configure(bg=self.colors['background'])
        self.center_window(dialog, 350, 200)
        
        tk.Label(
            dialog,
            text=message,
            font=("Arial", 12),
            bg=self.colors['background']
        ).pack(pady=20)
        
        amount_entry = tk.Entry(dialog, font=("Arial", 14), width=20)
        amount_entry.pack(pady=10)
        
        # Кнопки быстрого ввода
        quick_frame = tk.Frame(dialog, bg=self.colors['background'])
        quick_frame.pack(pady=10)
        
        quick_amounts = [500, 1000, 5000, 10000]
        for amount in quick_amounts:
            btn = tk.Button(
                quick_frame,
                text=f"{amount:,} ₽",
                command=lambda a=amount: amount_entry.insert(0, str(a)),
                bg=self.colors['light'],
                font=("Arial", 9),
                width=8
            )
            btn.pack(side="left", padx=2)
        
        def process():
            amount_str = amount_entry.get().strip()
            
            if not amount_str:
                messagebox.showerror("Ошибка", "Введите сумму")
                return
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Ошибка", "Сумма должна быть больше 0")
                    return
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректную сумму")
                return
            
            if operation == "withdraw":
                if self.users[self.current_user]['accounts']['основной']['баланс'] < amount:
                    messagebox.showerror("Ошибка", "Недостаточно средств")
                    return
            
            # Создаем транзакцию
            transaction_type = "пополнение" if operation == "deposit" else "снятие"
            transaction_amount = amount if operation == "deposit" else -amount
            
            self.users[self.current_user]['accounts']['основной']['баланс'] += transaction_amount
            
            transaction = {
                'дата': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'тип': transaction_type,
                'сумма': transaction_amount,
                'описание': transaction_type.capitalize()
            }
            
            if self.current_user not in self.all_transactions:
                self.all_transactions[self.current_user] = []
            self.all_transactions[self.current_user].append(transaction)
            
            self.save_data()
            self.update_dashboard()
            messagebox.showinfo("Успех", f"Операция выполнена: {transaction_amount:,.2f} ₽")
            dialog.destroy()
        
        tk.Button(
            dialog,
            text="Подтвердить",
            command=process,
            bg=self.colors['success'],
            fg="white",
            font=("Arial", 12),
            width=15,
            cursor="hand2"
        ).pack(pady=20)
    
    # НОВЫЕ МОДУЛИ:
    
    def show_savings_module(self):
        """Модуль накоплений (Накопительный счет)"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Накопительный счет")
        dialog.geometry("500x400")
        dialog.configure(bg=self.colors['background'])
        self.center_window(dialog, 500, 400)
        
        # Проверяем наличие накопительного счета
        if 'накопительный' not in self.users[self.current_user]['accounts']:
            # Создаем накопительный счет
            self.users[self.current_user]['accounts']['накопительный'] = {
                'баланс': 0.00,
                'валюта': 'RUB',
                'процент': 5.5,  # Годовая ставка
                'открыт': datetime.now().strftime("%Y-%m-%d"),
                'цель': None
            }
            self.save_data()
        
        savings = self.users[self.current_user]['accounts']['накопительный']
        
        # Заголовок
        tk.Label(
            dialog,
            text="💰 Накопительный счет",
            font=("Arial", 18, "bold"),
            bg=self.colors['background'],
            fg=self.colors['primary']
        ).pack(pady=20)
        
        # Информация
        info_frame = tk.Frame(dialog, bg="white", relief="groove", bd=2)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(
            info_frame,
            text=f"Текущий баланс: {savings['баланс']:,.2f} ₽",
            font=("Arial", 16, "bold"),
            bg="white",
            fg=self.colors['success']
        ).pack(pady=10)
        
        tk.Label(
            info_frame,
            text=f"Процентная ставка: {savings['процент']}% годовых",
            font=("Arial", 12),
            bg="white"
        ).pack(pady=5)
        
        # Операции
        tk.Label(
            dialog,
            text="Операции:",
            font=("Arial", 14, "bold"),
            bg=self.colors['background']
        ).pack(pady=10)
        
        buttons_frame = tk.Frame(dialog, bg=self.colors['background'])
        buttons_frame.pack(pady=10)
        
        def transfer_to_savings():
            amount_dialog = tk.Toplevel(dialog)
            amount_dialog.title("Пополнение накоплений")
            amount_dialog.geometry("300x200")
            amount_dialog.configure(bg=self.colors['background'])
            
            tk.Label(amount_dialog, text="Сумма для накопления:", bg=self.colors['background']).pack(pady=20)
            amount_entry = tk.Entry(amount_dialog, font=("Arial", 14))
            amount_entry.pack(pady=10)
            
            def process_transfer():
                try:
                    amount = float(amount_entry.get())
                    if amount <= 0:
                        messagebox.showerror("Ошибка", "Сумма должна быть больше 0")
                        return
                    
                    # Проверяем основной баланс
                    if self.users[self.current_user]['accounts']['основной']['баланс'] < amount:
                        messagebox.showerror("Ошибка", "Недостаточно средств на основном счете")
                        return
                    
                    # Переводим
                    self.users[self.current_user]['accounts']['основной']['баланс'] -= amount
                    savings['баланс'] += amount
                    
                    # Записываем транзакцию
                    transaction = {
                        'дата': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'тип': 'накопление',
                        'сумма': -amount,
                        'описание': "Перевод на накопительный счет"
                    }
                    if self.current_user not in self.all_transactions:
                        self.all_transactions[self.current_user] = []
                    self.all_transactions[self.current_user].append(transaction)
                    
                    self.save_data()
                    messagebox.showinfo("Успех", f"Переведено {amount:,.2f} ₽ на накопительный счет")
                    amount_dialog.destroy()
                    dialog.destroy()
                    self.show_savings_module()
                    
                except ValueError:
                    messagebox.showerror("Ошибка", "Введите корректную сумму")
            
            tk.Button(
                amount_dialog,
                text="Перевести",
                command=process_transfer,
                bg=self.colors['success'],
                fg="white"
            ).pack(pady=20)
        
        def withdraw_from_savings():
            amount_dialog = tk.Toplevel(dialog)
            amount_dialog.title("Снятие с накоплений")
            amount_dialog.geometry("300x200")
            amount_dialog.configure(bg=self.colors['background'])
            
            tk.Label(amount_dialog, text="Сумма для снятия:", bg=self.colors['background']).pack(pady=20)
            amount_entry = tk.Entry(amount_dialog, font=("Arial", 14))
            amount_entry.pack(pady=10)
            
            def process_withdrawal():
                try:
                    amount = float(amount_entry.get())
                    if amount <= 0:
                        messagebox.showerror("Ошибка", "Сумма должна быть больше 0")
                        return
                    
                    if savings['баланс'] < amount:
                        messagebox.showerror("Ошибка", "Недостаточно средств на накопительном счете")
                        return
                    
                    # Переводим обратно
                    savings['баланс'] -= amount
                    self.users[self.current_user]['accounts']['основной']['баланс'] += amount
                    
                    transaction = {
                        'дата': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'тип': 'снятие_накоплений',
                        'сумма': amount,
                        'описание': "Снятие с накопительного счета"
                    }
                    if self.current_user not in self.all_transactions:
                        self.all_transactions[self.current_user] = []
                    self.all_transactions[self.current_user].append(transaction)
                    
                    self.save_data()
                    messagebox.showinfo("Успех", f"Снято {amount:,.2f} ₽ с накопительного счета")
                    amount_dialog.destroy()
                    dialog.destroy()
                    self.show_savings_module()
                    
                except ValueError:
                    messagebox.showerror("Ошибка", "Введите корректную сумму")
            
            tk.Button(
                amount_dialog,
                text="Снять",
                command=process_withdrawal,
                bg=self.colors['warning'],
                fg="white"
            ).pack(pady=20)
        
        tk.Button(
            buttons_frame,
            text="Пополнить накопления",
            command=transfer_to_savings,
            bg=self.colors['success'],
            fg="white",
            width=20
        ).pack(pady=5)
        
        tk.Button(
            buttons_frame,
            text="Снять с накоплений",
            command=withdraw_from_savings,
            bg=self.colors['warning'],
            fg="white",
            width=20
        ).pack(pady=5)
        
        # Рассчет дохода
        def calculate_profit():
            amount = savings['баланс']
            rate = savings['процент']
            monthly = (amount * rate / 100) / 12
            yearly = amount * rate / 100
            
            profit_window = tk.Toplevel(dialog)
            profit_window.title("Рассчет дохода")
            profit_window.geometry("300x250")
            profit_window.configure(bg=self.colors['background'])
            
            tk.Label(
                profit_window,
                text="Прогноз дохода:",
                font=("Arial", 14, "bold"),
                bg=self.colors['background']
            ).pack(pady=10)
            
            tk.Label(
                profit_window,
                text=f"Месячный доход: {monthly:,.2f} ₽",
                font=("Arial", 12),
                bg=self.colors['background']
            ).pack(pady=5)
            
            tk.Label(
                profit_window,
                text=f"Годовой доход: {yearly:,.2f} ₽",
                font=("Arial", 12, "bold"),
                bg=self.colors['background'],
                fg=self.colors['success']
            ).pack(pady=5)
            
            tk.Label(
                profit_window,
                text=f"Через год: {(amount + yearly):,.2f} ₽",
                font=("Arial", 12),
                bg=self.colors['background']
            ).pack(pady=10)
        
        tk.Button(
            dialog,
            text="Рассчитать доход",
            command=calculate_profit,
            bg=self.colors['accent'],
            fg="white"
        ).pack(pady=20)
    
    def show_credit_module(self):
        """Модуль кредитования"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Кредитный калькулятор")
        dialog.geometry("500x450")
        dialog.configure(bg=self.colors['background'])
        self.center_window(dialog, 500, 450)
        
        # Заголовок
        tk.Label(
            dialog,
            text="💳 Кредитный калькулятор",
            font=("Arial", 18, "bold"),
            bg=self.colors['background'],
            fg=self.colors['primary']
        ).pack(pady=20)
        
        # Форма ввода
        input_frame = tk.Frame(dialog, bg=self.colors['background'])
        input_frame.pack(pady=10)
        
        # Сумма кредита
        tk.Label(
            input_frame,
            text="Сумма кредита (₽):",
            bg=self.colors['background']
        ).grid(row=0, column=0, sticky="w", pady=5)
        loan_amount = tk.Entry(input_frame, width=20)
        loan_amount.grid(row=0, column=1, pady=5, padx=10)
        loan_amount.insert(0, "100000")
        
        # Срок кредита
        tk.Label(
            input_frame,
            text="Срок (месяцев):",
            bg=self.colors['background']
        ).grid(row=1, column=0, sticky="w", pady=5)
        loan_term = tk.Entry(input_frame, width=20)
        loan_term.grid(row=1, column=1, pady=5, padx=10)
        loan_term.insert(0, "12")
        
        # Процентная ставка
        tk.Label(
            input_frame,
            text="Ставка (% годовых):",
            bg=self.colors['background']
        ).grid(row=2, column=0, sticky="w", pady=5)
        interest_rate = tk.Entry(input_frame, width=20)
        interest_rate.grid(row=2, column=1, pady=5, padx=10)
        interest_rate.insert(0, "12")
        
        # Тип платежа
        tk.Label(
            input_frame,
            text="Тип платежа:",
            bg=self.colors['background']
        ).grid(row=3, column=0, sticky="w", pady=5)
        payment_type = ttk.Combobox(input_frame, values=["Аннуитетный", "Дифференцированный"], width=18)
        payment_type.grid(row=3, column=1, pady=5, padx=10)
        payment_type.set("Аннуитетный")
        
        # Результаты
        result_frame = tk.Frame(dialog, bg="white", relief="groove", bd=2)
        result_frame.pack(fill="x", padx=20, pady=20)
        
        results_text = tk.Text(result_frame, height=8, width=40, bg="white", font=("Arial", 10))
        results_text.pack(padx=10, pady=10)
        
        def calculate_credit():
            try:
                amount = float(loan_amount.get())
                term = int(loan_term.get())
                rate = float(interest_rate.get())
                ptype = payment_type.get()
                
                if amount <= 0 or term <= 0 or rate <= 0:
                    messagebox.showerror("Ошибка", "Все значения должны быть положительными")
                    return
                
                # Месячная процентная ставка
                monthly_rate = rate / 12 / 100
                
                if ptype == "Аннуитетный":
                    # Формула аннуитетного платежа
                    monthly_payment = amount * (monthly_rate * (1 + monthly_rate) ** term) / ((1 + monthly_rate) ** term - 1)
                    total_payment = monthly_payment * term
                    overpayment = total_payment - amount
                    
                    results_text.delete(1.0, tk.END)
                    results_text.insert(tk.END, "=== АННУИТЕТНЫЙ ПЛАТЕЖ ===\n\n")
                    results_text.insert(tk.END, f"Ежемесячный платеж: {monthly_payment:,.2f} ₽\n")
                    results_text.insert(tk.END, f"Общая сумма выплат: {total_payment:,.2f} ₽\n")
                    results_text.insert(tk.END, f"Переплата: {overpayment:,.2f} ₽\n\n")
                    
                    # График платежей
                    results_text.insert(tk.END, "Первые 3 месяца:\n")
                    remaining = amount
                    for month in range(1, min(4, term + 1)):
                        interest = remaining * monthly_rate
                        principal = monthly_payment - interest
                        remaining -= principal
                        
                        results_text.insert(tk.END, f"Месяц {month}: {monthly_payment:,.2f} ₽ ")
                        results_text.insert(tk.END, f"(осн. долг: {principal:,.2f} ₽, проценты: {interest:,.2f} ₽)\n")
                
                else:
                    # Дифференцированный платеж
                    principal_payment = amount / term
                    total_payment = 0
                    payments = []
                    
                    remaining = amount
                    for month in range(1, term + 1):
                        interest = remaining * monthly_rate
                        monthly_payment = principal_payment + interest
                        remaining -= principal_payment
                        total_payment += monthly_payment
                        payments.append(monthly_payment)
                    
                    overpayment = total_payment - amount
                    
                    results_text.delete(1.0, tk.END)
                    results_text.insert(tk.END, "=== ДИФФЕРЕНЦИРОВАННЫЙ ПЛАТЕЖ ===\n\n")
                    results_text.insert(tk.END, f"Первый платеж: {payments[0]:,.2f} ₽\n")
                    results_text.insert(tk.END, f"Последний платеж: {payments[-1]:,.2f} ₽\n")
                    results_text.insert(tk.END, f"Общая сумма выплат: {total_payment:,.2f} ₽\n")
                    results_text.insert(tk.END, f"Переплата: {overpayment:,.2f} ₽\n")
                    
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректные числовые значения")
        
        def apply_for_credit():
            try:
                amount = float(loan_amount.get())
                
                # Проверяем кредитную историю (упрощенно)
                if 'кредиты' not in self.users[self.current_user]:
                    self.users[self.current_user]['кредиты'] = []
                
                # Проверяем максимальный кредит (10x от баланса)
                max_credit = self.users[self.current_user]['accounts']['основной']['баланс'] * 10
                if amount > max_credit:
                    messagebox.showerror("Ошибка", f"Максимальная сумма кредита: {max_credit:,.2f} ₽")
                    return
                
                # Проверяем активные кредиты
                active_credits = sum(loan['остаток'] for loan in self.users[self.current_user]['кредиты'] 
                                   if loan['статус'] == 'активен')
                
                if active_credits > max_credit * 0.5:
                    messagebox.showerror("Ошибка", "У вас уже есть активные кредиты")
                    return
                
                if messagebox.askyesno("Заявка на кредит", f"Подать заявку на кредит {amount:,.2f} ₽?"):
                    # Создаем заявку
                    credit = {
                        'сумма': amount,
                        'дата': datetime.now().strftime("%Y-%m-%d"),
                        'статус': 'на рассмотрении',
                        'номер': ''.join(random.choices(string.digits, k=10))
                    }
                    
                    self.users[self.current_user]['кредиты'].append(credit)
                    self.save_data()
                    
                    messagebox.showinfo("Заявка подана", 
                                      f"Заявка №{credit['номер']} принята в обработку\n"
                                      f"Решение будет в течение 2 рабочих дней")
                    
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректную сумму кредита")
        
        # Кнопки
        button_frame = tk.Frame(dialog, bg=self.colors['background'])
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="Рассчитать",
            command=calculate_credit,
            bg=self.colors['accent'],
            fg="white",
            width=15
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame,
            text="Подать заявку",
            command=apply_for_credit,
            bg=self.colors['success'],
            fg="white",
            width=15
        ).pack(side="left", padx=5)
        
        # Сразу рассчитываем
        calculate_credit()
    
    def show_transaction_history(self):
        """История транзакций"""
        if self.current_user not in self.all_transactions or not self.all_transactions[self.current_user]:
            messagebox.showinfo("История", "Транзакций пока нет")
            return
        
        history_window = tk.Toplevel(self.root)
        history_window.title("История транзакций")
        history_window.geometry("600x500")
        history_window.configure(bg=self.colors['background'])
        self.center_window(history_window, 600, 500)
        
        # Заголовок
        tk.Label(
            history_window,
            text="История транзакций",
            font=("Arial", 16, "bold"),
            bg=self.colors['background'],
            fg=self.colors['dark']
        ).pack(pady=20)
        
        # Фильтры
        filter_frame = tk.Frame(history_window, bg=self.colors['background'])
        filter_frame.pack(pady=10)
        
        tk.Label(filter_frame, text="Фильтр по типу:", bg=self.colors['background']).pack(side="left", padx=5)
        type_filter = ttk.Combobox(filter_frame, values=["Все", "пополнение", "снятие", "перевод", "накопление"])
        type_filter.pack(side="left", padx=5)
        type_filter.set("Все")
        
        tk.Label(filter_frame, text="Сортировка:", bg=self.colors['background']).pack(side="left", padx=5)
        sort_filter = ttk.Combobox(filter_frame, values=["По дате (новые)", "По дате (старые)", "По сумме (↑)", "По сумме (↓)"])
        sort_filter.pack(side="left", padx=5)
        sort_filter.set("По дате (новые)")
        
        # Таблица транзакций
        tree_frame = tk.Frame(history_window)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Создаем Treeview
        columns = ("Дата", "Тип", "Сумма", "Описание")
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        
        # Настраиваем колонки
        tree.heading("Дата", text="Дата")
        tree.heading("Тип", text="Тип операции")
        tree.heading("Сумма", text="Сумма (₽)")
        tree.heading("Описание", text="Описание")
        
        tree.column("Дата", width=120)
        tree.column("Тип", width=100)
        tree.column("Сумма", width=100)
        tree.column("Описание", width=200)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Загружаем транзакции
        def load_transactions():
            transactions = self.all_transactions[self.current_user].copy()
            
            # Применяем фильтр
            selected_type = type_filter.get()
            if selected_type != "Все":
                transactions = [t for t in transactions if t['тип'] == selected_type]
            
            # Применяем сортировку
            sort_by = sort_filter.get()
            if sort_by == "По дате (новые)":
                transactions.sort(key=lambda x: x['дата'], reverse=True)
            elif sort_by == "По дате (старые)":
                transactions.sort(key=lambda x: x['дата'])
            elif sort_by == "По сумме (↑)":
                transactions.sort(key=lambda x: x['сумма'])
            elif sort_by == "По сумме (↓)":
                transactions.sort(key=lambda x: x['сумма'], reverse=True)
            
            # Очищаем дерево
            for item in tree.get_children():
                tree.delete(item)
            
            # Добавляем транзакции
            for trans in transactions:
                amount = trans['сумма']
                amount_str = f"+{amount:,.2f}" if amount > 0 else f"{amount:,.2f}"
                tags = ('positive',) if amount > 0 else ('negative',)
                
                tree.insert("", "end", values=(
                    trans['дата'],
                    trans['тип'],
                    amount_str,
                    trans['описание']
                ), tags=tags)
            
            # Настраиваем цвета
            tree.tag_configure('positive', foreground='green')
            tree.tag_configure('negative', foreground='red')
        
        # Кнопка обновления
        tk.Button(
            history_window,
            text="Обновить",
            command=load_transactions,
            bg=self.colors['accent'],
            fg="white",
            width=15
        ).pack(pady=10)
        
        # Кнопка экспорта
        def export_transactions():
            try:
                filename = f"transactions_{self.current_user}_{datetime.now().strftime('%Y%m%d')}.txt"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("История транзакций\n")
                    f.write(f"Пользователь: {self.current_user}\n")
                    f.write(f"Дата экспорта: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("="*50 + "\n\n")
                    
                    for trans in self.all_transactions[self.current_user]:
                        amount = trans['сумма']
                        amount_str = f"+{amount:,.2f} ₽" if amount > 0 else f"{amount:,.2f} ₽"
                        f.write(f"{trans['дата']} | {trans['тип']} | {amount_str} | {trans['описание']}\n")
                
                messagebox.showinfo("Экспорт", f"Транзакции экспортированы в файл: {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось экспортировать: {str(e)}")
        
        tk.Button(
            history_window,
            text="Экспорт в файл",
            command=export_transactions,
            bg=self.colors['success'],
            fg="white",
            width=15
        ).pack(pady=5)
        
        # Привязываем фильтры
        type_filter.bind("<<ComboboxSelected>>", lambda e: load_transactions())
        sort_filter.bind("<<ComboboxSelected>>", lambda e: load_transactions())
        
        # Загружаем начальные данные
        load_transactions()
    
    def show_password_recovery(self):
        """Восстановление пароля"""
        recovery_window = tk.Toplevel(self.root)
        recovery_window.title("Восстановление пароля")
        recovery_window.geometry("400x300")
        recovery_window.configure(bg=self.colors['background'])
        self.center_window(recovery_window, 400, 300)
        
        tk.Label(
            recovery_window,
            text="Восстановление пароля",
            font=("Arial", 16, "bold"),
            bg=self.colors['background']
        ).pack(pady=20)
        
        tk.Label(recovery_window, text="Введите ваш email:", bg=self.colors['background']).pack()
        email_entry = tk.Entry(recovery_window, width=30)
        email_entry.pack(pady=10)
        
        def recover():
            email = email_entry.get().strip()
            if email not in self.users:
                messagebox.showerror("Ошибка", "Пользователь не найден")
                return
            
            # Генерируем временный пароль
            temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            self.users[email]['security']['пароль'] = self.hash_password(temp_password)
            self.save_data()
            
            messagebox.showinfo("Пароль восстановлен", 
                              f"Временный пароль: {temp_password}\n"
                              f"Рекомендуем сменить его после входа в систему.")
            recovery_window.destroy()
        
        tk.Button(
            recovery_window,
            text="Восстановить",
            command=recover,
            bg=self.colors['warning'],
            fg="white",
            width=15
        ).pack(pady=20)
    
    def show_guest_mode(self):
        """Режим гостя"""
        self.clear_window()
        
        tk.Label(
            self.root,
            text="Гостевой режим",
            font=("Arial", 18, "bold"),
            bg=self.colors['background']
        ).pack(pady=50)
        
        tk.Label(
            self.root,
            text="Демонстрация возможностей банка",
            font=("Arial", 12),
            bg=self.colors['background']
        ).pack(pady=10)
        
        features = [
            "• Безопасная регистрация и авторизация",
            "• Управление счетами и картами",
            "• Переводы между пользователями",
            "• Накопительный счет с процентами",
            "• Кредитный калькулятор",
            "• История всех операций",
            "• Современный интерфейс"
        ]
        
        for feature in features:
            tk.Label(
                self.root,
                text=feature,
                font=("Arial", 10),
                bg=self.colors['background']
            ).pack(pady=2)
        
        tk.Button(
            self.root,
            text="Вернуться в меню",
            command=self.show_main_menu,
            bg=self.colors['accent'],
            fg="white",
            font=("Arial", 12),
            width=20,
            pady=10
        ).pack(pady=30)
    
    def update_dashboard(self):
        """Обновление информации на панели управления"""
        user = self.users[self.current_user]
        self.balance_label.config(text=f"{user['accounts']['основной']['баланс']:,.2f} ₽")
        
        # Обновляем список транзакций
        self.transactions_text.config(state="normal")
        self.transactions_text.delete(1.0, tk.END)
        self.load_recent_transactions()
    
    def logout(self):
        """Выход из системы"""
        self.current_user = None
        self.show_main_menu()
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

# Запуск приложения
if __name__ == "__main__":
    app = ModernBankApp()
    app.run()