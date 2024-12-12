import sqlite3

class CoffeeDatabase:
    def __init__(self, db_name='coffee.db'):
        self.connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.connection:
            self.connection.execute('''
                CREATE TABLE IF NOT EXISTS coffee (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    price REAL NOT NULL
                )
            ''')

    def add_coffee(self, name, type_, price):
        with self.connection:
            self.connection.execute('INSERT INTO coffee (name, type, price) VALUES (?, ?, ?)',
                                    (name, type_, price))

    def update_coffee(self, coffee_id, name, type_, price):
        with self.connection:
            self.connection.execute('UPDATE coffee SET name = ?, type = ?, price = ? WHERE id = ?',
                                    (name, type_, price, coffee_id))

    def get_coffee(self, coffee_id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT name, type, price FROM coffee WHERE id = ?', (coffee_id,))
        return cursor.fetchone()

    def close(self):
        self.connection.close()
from PyQt5 import QtWidgets, uic

class AddEditCoffeeForm(QtWidgets.QDialog):
    def __init__(self, coffee_db, coffee_id=None):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.coffee_db = coffee_db
        self.coffee_id = coffee_id

        if coffee_id:
            self.load_coffee_data(coffee_id)

        self.save_button.clicked.connect(self.save_coffee)

    def load_coffee_data(self, coffee_id):
        data = self.coffee_db.get_coffee(coffee_id)
        if data:
            self.name_input.setText(data[0])
            self.type_input.setText(data[1])
            self.price_input.setValue(data[2])

    def save_coffee(self):
        name = self.name_input.text()
        type_ = self.type_input.text()
        price = self.price_input.value()

        if self.coffee_id:
            self.coffee_db.update_coffee(self.coffee_id, name, type_, price)
        else:
            self.coffee_db.add_coffee(name, type_, price)

        self.accept()


import sys
from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.coffee_db = CoffeeDatabase()

        # Здесь вы можете добавить кнопки для открытия формы добавления/редактирования кофе
        # Например:
        self.add_button = QtWidgets.QPushButton("Добавить кофе", self)
        self.add_button.clicked.connect(self.open_add_edit_form)
        self.setCentralWidget(self.add_button)

    def open_add_edit_form(self, coffee_id=None):
        form = AddEditCoffeeForm(self.coffee_db, coffee_id)
        form.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
