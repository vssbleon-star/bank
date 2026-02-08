import tkinter as tk
from tkinter import ttk, messagebox
import json
import hashlib
import os
from datetime import datetime

class BankApp:
    def __init__(self):
        self.users_file = "users.json"
        self.current_user = None
        self.load_users()
        
        # Стиль для приложения
        self.bg_color = "#f0f0f0"
        self.primary_color = "#2c3e50"
        self.secondary_color = "#3498db"
        self.accent_color = "#27ae60"
        
        # Создаем главное окно
        self.root = tk.Tk()
        self.root.title("Банк Онлайн")
        self.root.geometry("400x500")
        self.root.configure(bg=self.bg_color)
        
        # Показываем окно регистрации
        self.show_registration_window()
        
    def load_users(self):
        """Загружаем пользователей из файла"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {}
    
    def save_users(self):
        """Сохраняем пользователей в файл"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=4)
    
    def hash_password(self, password):
        """Хешируем пароль"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def show_registration_window(self):
        """Окно регистрации"""
        self.reg_window = tk.Toplevel(self.root)
        self.reg_window.title("Регистрация")
        self.reg_window.geometry("350x450")
        self.reg_window.configure(bg=self.bg_color)
        self.reg_window.grab_set()  # Модальное окно
        
        # Заголовок
        title_label = tk.Label(
            self.reg_window,
            text="Регистрация в Банке",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.primary_color
        )
        title_label.pack(pady=20)
        
        # Фрейм для полей ввода
        input_frame = tk.Frame(self.reg_window, bg=self.bg_color)
        input_frame.pack(pady=20)
        
        # Поля для ввода
        labels = ["Имя:", "Фамилия:", "Email:", "Номер телефона:", "Пароль:", "Подтвердите пароль:"]
        self.reg_entries = {}
        
        for i, label_text in enumerate(labels):
            label = tk.Label(input_frame, text=label_text, bg=self.bg_color, anchor="w")
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
            
            entry = tk.Entry(input_frame, width=25)
            if "пароль" in label_text.lower():
                entry.config(show="*")
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.reg_entries[label_text.split(":")[0]] = entry
        
        # Кнопка регистрации
        reg_button = tk.Button(
            self.reg_window,
            text="Зарегистрироваться",
            command=self.register_user,
            bg=self.secondary_color,
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=10
        )
        reg_button.pack(pady=20)
        
        # Ссылка на вход
        login_label = tk.Label(
            self.reg_window,
            text="Уже есть аккаунт? Войти",
            bg=self.bg_color,
            fg=self.secondary_color,
            cursor="hand2"
        )
        login_label.pack()
        login_label.bind("<Button-1>", lambda e: self.switch_to_login())
    
    def switch_to_login(self):
        """Переход к окну входа"""
        self.reg_window.destroy()
        self.show_login_window()
    
    def register_user(self):
        """Регистрация нового пользователя"""
        # Получаем данные
        data = {}
        for field, entry in self.reg_entries.items():
            data[field] = entry.get().strip()
        
        # Проверяем заполненность полей
        for field, value in data.items():
            if not value:
                messagebox.showerror("Ошибка", f"Поле '{field}' обязательно для заполнения!")
                return
        
        # Проверяем пароли
        if data["Пароль"] != data["Подтвердите пароль"]:
            messagebox.showerror("Ошибка", "Пароли не совпадают!")
            return
        
        # Проверяем уникальность email
        if data["Email"] in self.users:
            messagebox.showerror("Ошибка", "Пользователь с таким email уже существует!")
            return
        
        # Создаем аккаунт пользователя
        self.users[data["Email"]] = {
            "имя": data["Имя"],
            "фамилия": data["Фамилия"],
            "телефон": data["Номер телефона"],
            "пароль": self.hash_password(data["Пароль"]),
            "баланс": 1000.00,  # Начальный баланс
            "транзакции": [],
            "активен": True
        }
        
        self.save_users()
        messagebox.showinfo("Успех", "Регистрация успешна! Теперь войдите в систему.")
        self.switch_to_login()
    
    def show_login_window(self):
        """Окно входа"""
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("Вход в систему")
        self.login_window.geometry("350x300")
        self.login_window.configure(bg=self.bg_color)
        self.login_window.grab_set()
        
        # Заголовок
        title_label = tk.Label(
            self.login_window,
            text="Вход в Банк",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.primary_color
        )
        title_label.pack(pady=30)
        
        # Поля для ввода
        input_frame = tk.Frame(self.login_window, bg=self.bg_color)
        input_frame.pack(pady=20)
        
        # Email
        email_label = tk.Label(input_frame, text="Email:", bg=self.bg_color)
        email_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.email_entry = tk.Entry(input_frame, width=25)
        self.email_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Пароль
        password_label = tk.Label(input_frame, text="Пароль:", bg=self.bg_color)
        password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.password_entry = tk.Entry(input_frame, width=25, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
        
        # Кнопка входа
        login_button = tk.Button(
            self.login_window,
            text="Войти",
            command=self.login_user,
            bg=self.accent_color,
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=10
        )
        login_button.pack(pady=20)
        
        # Ссылка на регистрацию
        reg_label = tk.Label(
            self.login_window,
            text="Нет аккаунта? Зарегистрироваться",
            bg=self.bg_color,
            fg=self.secondary_color,
            cursor="hand2"
        )
        reg_label.pack()
        reg_label.bind("<Button-1>", lambda e: self.switch_to_registration())
    
    def switch_to_registration(self):
        """Переход к окну регистрации"""
        self.login_window.destroy()
        self.show_registration_window()
    
    def login_user(self):
        """Авторизация пользователя"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return
        
        if email not in self.users:
            messagebox.showerror("Ошибка", "Пользователь не найден!")
            return
        
        user = self.users[email]
        
        if not user["активен"]:
            messagebox.showerror("Ошибка", "Аккаунт заблокирован!")
            return
        
        if user["пароль"] != self.hash_password(password):
            messagebox.showerror("Ошибка", "Неверный пароль!")
            return
        
        self.current_user = email
        self.login_window.destroy()
        self.show_bank_window()
    
    def show_bank_window(self):
        """Основное окно банка"""
        self.root.deiconify()  # Показываем главное окно
        self.root.title(f"Банк Онлайн - {self.users[self.current_user]['имя']} {self.users[self.current_user]['фамилия']}")
        
        # Верхняя панель
        header_frame = tk.Frame(self.root, bg=self.primary_color, height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        user_info = tk.Label(
            header_frame,
            text=f"Добро пожаловать, {self.users[self.current_user]['имя']}!",
            font=("Arial", 14, "bold"),
            bg=self.primary_color,
            fg="white"
        )
        user_info.pack(pady=20)
        
        # Основное содержание
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Баланс
        balance_frame = tk.Frame(main_frame, bg="white", relief="groove", bd=2)
        balance_frame.pack(fill="x", pady=10)
        
        balance_label = tk.Label(
            balance_frame,
            text="Ваш баланс:",
            font=("Arial", 12),
            bg="white"
        )
        balance_label.pack(pady=10)
        
        self.balance_value = tk.Label(
            balance_frame,
            text=f"{self.users[self.current_user]['баланс']:.2f} ₽",
            font=("Arial", 24, "bold"),
            bg="white",
            fg=self.accent_color
        )
        self.balance_value.pack(pady=10)
        
        # Кнопки операций
        buttons_frame = tk.Frame(main_frame, bg=self.bg_color)
        buttons_frame.pack(pady=20)
        
        operations = [
            ("Пополнить", self.deposit_money),
            ("Снять", self.withdraw_money),
            ("Перевести", self.transfer_money),
            ("История", self.show_history)
        ]
        
        for i, (text, command) in enumerate(operations):
            btn = tk.Button(
                buttons_frame,
                text=text,
                command=command,
                bg=self.secondary_color,
                fg="white",
                font=("Arial", 10, "bold"),
                width=15,
                height=2
            )
            btn.grid(row=i//2, column=i%2, padx=10, pady=10)
        
        # Кнопка выхода
        logout_btn = tk.Button(
            main_frame,
            text="Выйти",
            command=self.logout,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10),
            padx=20
        )
        logout_btn.pack(pady=20)
    
    def update_balance(self):
        """Обновляем отображение баланса"""
        self.balance_value.config(
            text=f"{self.users[self.current_user]['баланс']:.2f} ₽"
        )
    
    def add_transaction(self, transaction_type, amount, description=""):
        """Добавляем транзакцию в историю"""
        transaction = {
            "дата": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "тип": transaction_type,
            "сумма": amount,
            "описание": description
        }
        self.users[self.current_user]["транзакции"].append(transaction)
        self.save_users()
    
    def deposit_money(self):
        """Пополнение счета"""
        self.show_amount_window("Пополнение счета", "Введите сумму для пополнения:", "deposit")
    
    def withdraw_money(self):
        """Снятие денег"""
        self.show_amount_window("Снятие наличных", "Введите сумму для снятия:", "withdraw")
    
    def transfer_money(self):
        """Перевод денег"""
        transfer_window = tk.Toplevel(self.root)
        transfer_window.title("Перевод денег")
        transfer_window.geometry("350x250")
        transfer_window.configure(bg=self.bg_color)
        
        tk.Label(
            transfer_window,
            text="Перевод средств",
            font=("Arial", 14, "bold"),
            bg=self.bg_color
        ).pack(pady=20)
        
        # Получатель
        tk.Label(transfer_window, text="Email получателя:", bg=self.bg_color).pack()
        recipient_entry = tk.Entry(transfer_window, width=30)
        recipient_entry.pack(pady=5)
        
        # Сумма
        tk.Label(transfer_window, text="Сумма перевода:", bg=self.bg_color).pack()
        amount_entry = tk.Entry(transfer_window, width=30)
        amount_entry.pack(pady=5)
        
        def process_transfer():
            recipient = recipient_entry.get().strip()
            amount_str = amount_entry.get().strip()
            
            if not recipient or not amount_str:
                messagebox.showerror("Ошибка", "Заполните все поля!")
                return
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Ошибка", "Сумма должна быть положительной!")
                    return
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректную сумму!")
                return
            
            if recipient == self.current_user:
                messagebox.showerror("Ошибка", "Нельзя перевести деньги самому себе!")
                return
            
            if recipient not in self.users:
                messagebox.showerror("Ошибка", "Получатель не найден!")
                return
            
            if self.users[self.current_user]["баланс"] < amount:
                messagebox.showerror("Ошибка", "Недостаточно средств на счете!")
                return
            
            # Выполняем перевод
            self.users[self.current_user]["баланс"] -= amount
            self.users[recipient]["баланс"] += amount
            
            # Добавляем транзакции
            self.add_transaction("перевод", -amount, f"Перевод пользователю {recipient}")
            
            recipient_transaction = {
                "дата": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "тип": "перевод",
                "сумма": amount,
                "описание": f"Перевод от пользователя {self.current_user}"
            }
            self.users[recipient]["транзакции"].append(recipient_transaction)
            
            self.save_users()
            self.update_balance()
            messagebox.showinfo("Успех", "Перевод выполнен успешно!")
            transfer_window.destroy()
        
        tk.Button(
            transfer_window,
            text="Выполнить перевод",
            command=process_transfer,
            bg=self.accent_color,
            fg="white",
            padx=20,
            pady=10
        ).pack(pady=20)
    
    def show_amount_window(self, title, message, operation):
        """Окно для ввода суммы"""
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("300x200")
        window.configure(bg=self.bg_color)
        
        tk.Label(
            window,
            text=message,
            font=("Arial", 12),
            bg=self.bg_color
        ).pack(pady=30)
        
        amount_entry = tk.Entry(window, width=20, font=("Arial", 14))
        amount_entry.pack(pady=10)
        
        def process_operation():
            amount_str = amount_entry.get().strip()
            
            if not amount_str:
                messagebox.showerror("Ошибка", "Введите сумму!")
                return
            
            try:
                amount = float(amount_str)
                if amount <= 0:
                    messagebox.showerror("Ошибка", "Сумма должна быть положительной!")
                    return
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректную сумму!")
                return
            
            if operation == "deposit":
                self.users[self.current_user]["баланс"] += amount
                self.add_transaction("пополнение", amount)
                messagebox.showinfo("Успех", "Счет пополнен успешно!")
            elif operation == "withdraw":
                if self.users[self.current_user]["баланс"] < amount:
                    messagebox.showerror("Ошибка", "Недостаточно средств на счете!")
                    return
                self.users[self.current_user]["баланс"] -= amount
                self.add_transaction("снятие", -amount)
                messagebox.showinfo("Успех", "Деньги сняты успешно!")
            
            self.save_users()
            self.update_balance()
            window.destroy()
        
        tk.Button(
            window,
            text="Подтвердить",
            command=process_operation,
            bg=self.accent_color,
            fg="white",
            padx=20,
            pady=10
        ).pack(pady=20)
    
    def show_history(self):
        """Показываем историю транзакций"""
        history_window = tk.Toplevel(self.root)
        history_window.title("История операций")
        history_window.geometry("500x400")
        history_window.configure(bg=self.bg_color)
        
        tk.Label(
            history_window,
            text="История транзакций",
            font=("Arial", 14, "bold"),
            bg=self.bg_color
        ).pack(pady=10)
        
        # Создаем Treeview для отображения транзакций
        tree_frame = tk.Frame(history_window)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Создаем вертикальный скроллбар
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        tree = ttk.Treeview(
            tree_frame,
            columns=("Дата", "Тип", "Сумма", "Описание"),
            show="headings",
            yscrollcommand=scrollbar.set
        )
        
        scrollbar.config(command=tree.yview)
        
        # Настраиваем колонки
        tree.heading("Дата", text="Дата")
        tree.heading("Тип", text="Тип операции")
        tree.heading("Сумма", text="Сумма (₽)")
        tree.heading("Описание", text="Описание")
        
        tree.column("Дата", width=120)
        tree.column("Тип", width=100)
        tree.column("Сумма", width=100)
        tree.column("Описание", width=150)
        
        # Добавляем транзакции
        for transaction in reversed(self.users[self.current_user]["транзакции"]):
            amount = transaction["сумма"]
            amount_str = f"+{amount:.2f}" if amount > 0 else f"{amount:.2f}"
            
            tree.insert("", "end", values=(
                transaction["дата"],
                transaction["тип"],
                amount_str,
                transaction.get("описание", "")
            ))
        
        tree.pack(fill="both", expand=True)
    
    def logout(self):
        """Выход из системы"""
        self.current_user = None
        self.root.withdraw()  # Скрываем главное окно
        self.show_login_window()
    
    def run(self):
        """Запуск приложения"""
        self.root.withdraw()  # Скрываем главное окно до входа
        self.root.mainloop()

if __name__ == "__main__":
    app = BankApp()
    app.run()