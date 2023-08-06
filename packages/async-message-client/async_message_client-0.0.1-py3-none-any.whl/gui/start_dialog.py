from PyQt6.QtWidgets import QDialog, QPushButton, QLineEdit, QApplication, QLabel
from PyQt6.QtCore import QEvent


# Стартовый диалог с выбором имени пользователя
class UserNameDialog(QDialog):
    """Стартовый диалог с выбором имени пользователя, если не были указаны при запуске из консоли"""
    def __init__(self):
        super().__init__()

        self.ok_pressed = False

        self.setWindowTitle('Привет!')
        self.setFixedSize(175, 133)

        self.label = QLabel('Введите имя пользователя:', self)
        self.label.move(10, 10)
        self.label.setFixedSize(150, 10)

        self.client_name = QLineEdit(self)
        self.client_name.setFixedSize(154, 20)
        self.client_name.move(10, 30)

        self.label_client_passwd = QLabel('Введите пароль:', self)
        self.label_client_passwd.move(10, 55)
        self.label_client_passwd.setFixedSize(150, 20)

        self.client_passwd = QLineEdit(self)
        self.client_passwd.setFixedSize(154, 20)
        self.client_passwd.move(10, 80)

        self.btn_ok = QPushButton('Начать', self)
        self.btn_ok.move(10, 100)
        self.btn_ok.clicked.connect(self.click)

        self.btn_cancel = QPushButton('Выход', self)
        self.btn_cancel.move(90, 100)
        self.btn_cancel.clicked.connect(QApplication.exit)

        self.show()

    # Обработчик кнопки ОК, если поле вводе не пустое, ставим флаг и завершаем приложение.
    def click(self):
        if self.client_name.text():
            self.ok_pressed = True
            QApplication.exit()


if __name__ == '__main__':
    app = QApplication([])
    dial = UserNameDialog()
    app.exec_()
