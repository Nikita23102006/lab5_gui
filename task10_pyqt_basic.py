"""Задание средней сложности №10: простейший GUI на PyQt5.

Установка: pip install PyQt5
"""

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMessageBox, QPushButton, QSpinBox, QVBoxLayout, QWidget,
)


class MainWindow(QWidget):
    """Главное окно приложения PyQt5."""

    def __init__(self):
        super().__init__()
        self.click_count = 0
        self.setWindowTitle("Задание 10 — простейший GUI на PyQt5")
        self.setMinimumSize(460, 320)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        title = QLabel("Приветствие")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        layout.addWidget(self._build_input_group())
        layout.addWidget(self._build_counter_group())

        self.result = QLabel("Введите имя и нажмите «Поздороваться»")
        self.result.setAlignment(Qt.AlignCenter)
        self.result.setWordWrap(True)
        self.result.setStyleSheet(
            "padding: 12px; background: #eef3fa; border: 1px solid #b8c4d4;")
        layout.addWidget(self.result)

        layout.addStretch()

        close_button = QPushButton("Выход")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

    def _build_input_group(self):
        group = QGroupBox("Данные")
        box = QVBoxLayout()

        row = QHBoxLayout()
        row.addWidget(QLabel("Имя:"))
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Например, Никита")
        # Нажатие Enter в поле вызывает тот же слот, что и кнопка.
        self.name_edit.returnPressed.connect(self.greet)
        row.addWidget(self.name_edit)
        box.addLayout(row)

        row = QHBoxLayout()
        row.addWidget(QLabel("Возраст:"))
        self.age_spin = QSpinBox()
        self.age_spin.setRange(1, 120)
        self.age_spin.setValue(19)
        row.addWidget(self.age_spin)
        row.addStretch()
        box.addLayout(row)

        greet_button = QPushButton("Поздороваться")
        # Сигнал clicked соединяется со слотом greet — основа PyQt.
        greet_button.clicked.connect(self.greet)
        box.addWidget(greet_button)

        group.setLayout(box)
        return group

    def _build_counter_group(self):
        group = QGroupBox("Счётчик нажатий")
        row = QHBoxLayout()

        self.counter_label = QLabel("Нажатий: 0")
        row.addWidget(self.counter_label)
        row.addStretch()

        count_button = QPushButton("Нажми меня")
        count_button.clicked.connect(self.increment)
        row.addWidget(count_button)

        reset_button = QPushButton("Сброс")
        reset_button.clicked.connect(self.reset_counter)
        row.addWidget(reset_button)

        group.setLayout(row)
        return group

    # ---------- слоты ----------

    def greet(self):
        """Слот кнопки «Поздороваться»."""
        name = self.name_edit.text().strip()

        if not name:
            QMessageBox.warning(self, "Пустое поле",
                                "Введите имя — без него поздороваться не выйдет.")
            self.name_edit.setFocus()
            return

        age = self.age_spin.value()
        self.result.setText(f"Здравствуйте, {name}!\nВам {age} {self._years(age)}.")

    def increment(self):
        self.click_count += 1
        self.counter_label.setText(f"Нажатий: {self.click_count}")

    def reset_counter(self):
        self.click_count = 0
        self.counter_label.setText("Нажатий: 0")

    @staticmethod
    def _years(age):
        """Согласование слова «год» с числом."""
        if 11 <= age % 100 <= 14:
            return "лет"
        last = age % 10
        if last == 1:
            return "год"
        if last in (2, 3, 4):
            return "года"
        return "лет"


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
