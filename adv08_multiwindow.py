"""Задание повышенной сложности №8: программа с несколькими окнами."""

import tkinter as tk
from tkinter import ttk

from adv01_notes import NotesApp


class SettingsWindow(tk.Toplevel):
    """Модальное окно настроек.

    Модальное — значит, что пока оно открыто, с главным окном
    работать нельзя. Результат возвращается через self.result.
    """

    def __init__(self, master, settings):
        super().__init__(master)
        self.title("Настройки")
        self.resizable(False, False)
        self.result = None

        self.name_var = tk.StringVar(value=settings["name"])
        self.size_var = tk.IntVar(value=settings["font_size"])
        self.dark_var = tk.BooleanVar(value=settings["dark"])

        self._build_ui()

        # Три строки, которые делают окно модальным.
        self.transient(master)   # всегда поверх родителя, без своей иконки
        self.grab_set()          # перехват событий мыши и клавиатуры
        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self._center_over(master)

    def _build_ui(self):
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Имя пользователя:").grid(
            row=0, column=0, sticky=tk.W, pady=4)
        ttk.Entry(frame, textvariable=self.name_var, width=24).grid(
            row=0, column=1, pady=4)

        ttk.Label(frame, text="Размер шрифта:").grid(
            row=1, column=0, sticky=tk.W, pady=4)
        ttk.Spinbox(frame, from_=8, to=32, textvariable=self.size_var,
                    width=22).grid(row=1, column=1, pady=4)

        ttk.Checkbutton(frame, text="Тёмная тема",
                        variable=self.dark_var).grid(
            row=2, column=0, columnspan=2, sticky=tk.W, pady=(8, 4))

        buttons = ttk.Frame(frame)
        buttons.grid(row=3, column=0, columnspan=2, pady=(12, 0))
        ttk.Button(buttons, text="OK", command=self.ok).pack(side=tk.LEFT, padx=4)
        ttk.Button(buttons, text="Отмена",
                   command=self.cancel).pack(side=tk.LEFT, padx=4)

    def _center_over(self, master):
        """Ставит окно по центру родительского."""
        self.update_idletasks()
        x = master.winfo_rootx() + (master.winfo_width() - self.winfo_width()) // 2
        y = master.winfo_rooty() + (master.winfo_height() - self.winfo_height()) // 3
        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")

    def ok(self):
        self.result = {
            "name": self.name_var.get().strip() or "Гость",
            "font_size": self.size_var.get(),
            "dark": self.dark_var.get(),
        }
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()


class AboutWindow(tk.Toplevel):
    """Немодальное окно «О программе».

    Открывается в одном экземпляре: повторное нажатие кнопки
    не плодит окна, а поднимает уже открытое.
    """

    def __init__(self, master):
        super().__init__(master)
        self.title("О программе")
        self.resizable(False, False)

        frame = ttk.Frame(self, padding=16)
        frame.pack()

        ttk.Label(frame, text="Лабораторная работа №5",
                  font=("Helvetica", 14, "bold")).pack(pady=(0, 6))
        ttk.Label(frame, text="Задание повышенной сложности №8:\n"
                              "программа с несколькими окнами",
                  justify=tk.CENTER).pack(pady=(0, 10))
        ttk.Label(frame, text="Кострикин Н. А., группа 220042-11").pack()

        ttk.Button(frame, text="Закрыть",
                   command=self.destroy).pack(pady=(12, 0))


class MainWindow:
    """Главное окно, управляющее дочерними."""

    def __init__(self, master):
        self.master = master
        master.title("Задание 8 — несколько окон")
        master.geometry("520x380")
        master.minsize(440, 320)

        self.settings = {"name": "Гость", "font_size": 12, "dark": False}
        self.about_window = None
        self.notes_window = None

        self._build_ui()
        self.refresh()

    def _build_ui(self):
        frame = ttk.Frame(self.master, padding=14)
        frame.pack(fill=tk.BOTH, expand=True)

        self.greeting = ttk.Label(frame, font=("Helvetica", 14, "bold"))
        self.greeting.pack(pady=(0, 4))

        self.summary = ttk.Label(frame, justify=tk.CENTER)
        self.summary.pack(pady=(0, 14))

        buttons = (
            ("Настройки (модальное окно)", self.open_settings),
            ("О программе (немодальное)", self.open_about),
            ("Открыть редактор заметок", self.open_notes),
            ("Закрыть все дочерние окна", self.close_children),
        )
        for text, command in buttons:
            ttk.Button(frame, text=text, command=command,
                       width=34).pack(pady=3)

        ttk.Separator(frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=12)
        ttk.Button(frame, text="Выход",
                   command=self.master.destroy).pack()

        self.status = tk.StringVar(value="Готово")
        ttk.Label(self.master, textvariable=self.status, relief=tk.SUNKEN,
                  anchor=tk.W, padding=(6, 3)).pack(fill=tk.X, side=tk.BOTTOM)

    def refresh(self):
        """Обновляет надписи по текущим настройкам."""
        theme = "тёмная" if self.settings["dark"] else "светлая"
        self.greeting.config(
            text=f"Здравствуйте, {self.settings['name']}!",
            font=("Helvetica", self.settings["font_size"] + 2, "bold"))
        self.summary.config(
            text=f"Размер шрифта: {self.settings['font_size']}   "
                 f"Тема: {theme}")

    # ---------- работа с дочерними окнами ----------

    def open_settings(self):
        """Модальное окно: ждём его закрытия и забираем результат."""
        dialog = SettingsWindow(self.master, self.settings)
        self.master.wait_window(dialog)   # выполнение останавливается здесь

        if dialog.result is None:
            self.status.set("Настройки не изменены")
            return

        self.settings = dialog.result
        self.refresh()
        self.status.set("Настройки сохранены")

    def open_about(self):
        """Немодальное окно в единственном экземпляре."""
        if self.about_window is not None and self.about_window.winfo_exists():
            self.about_window.lift()
            self.about_window.focus_set()
            self.status.set("Окно «О программе» уже открыто")
            return

        self.about_window = AboutWindow(self.master)
        self.status.set("Открыто окно «О программе»")

    def open_notes(self):
        """Переиспользуем редактор из задания повышенной сложности №1."""
        if self.notes_window is not None and self.notes_window.winfo_exists():
            self.notes_window.lift()
            self.status.set("Редактор уже открыт")
            return

        self.notes_window = tk.Toplevel(self.master)
        NotesApp(self.notes_window)
        self.status.set("Открыт редактор заметок")

    def close_children(self):
        """winfo_children() возвращает все дочерние виджеты и окна."""
        closed = 0
        for child in self.master.winfo_children():
            if isinstance(child, tk.Toplevel):
                child.destroy()
                closed += 1
        self.about_window = None
        self.notes_window = None
        self.status.set(f"Закрыто окон: {closed}")


def main():
    root = tk.Tk()
    MainWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()
