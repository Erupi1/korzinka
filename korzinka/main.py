import sys
from PyQt5.QtWidgets import QApplication
from db import init_db
from ui.login_window import LoginWindow
from ui.main_window import MainWindow

if __name__ == '__main__':
    init_db()
    app = QApplication(sys.argv)
    # Подключаем стили
    with open('ui/styles.qss', 'r', encoding='utf-8') as f:
        app.setStyleSheet(f.read())
    login = LoginWindow()
    if login.exec_() == LoginWindow.Accepted:
        user = login.user_info
        window = MainWindow(user)
        window.show()
        sys.exit(app.exec_())
    else:
        print('Вход не выполнен.') 