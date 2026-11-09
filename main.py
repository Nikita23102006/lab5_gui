"""Лабораторная работа №5. Вариант 8. Меню запуска заданий.

Каждое задание запускается отдельным процессом. Так сделано потому, что
Tkinter и PyQt5 имеют собственные циклы обработки событий (mainloop и
app.exec_), и запустить их в одном процессе одновременно нельзя.
"""

import os
import subprocess
import sys
import tkinter as tk
from tkinter import messagebox, ttk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TASKS = [
    ("Средн. №8", "Диалог выбора файла", "task08_file_dialog.py", "Tkinter"),
    ("Средн. №10", "Простейший GUI на PyQt5", "task10_pyqt_basic.py", "PyQt5"),
    ("Средн. №4", "Список (Listbox) и выбор элемента", "task04_listbox.py", "Tkinter"),
    ("Повыш. №8", "Программа с несколькими окнами", "adv08_multiwindow.py", "Tkinter"),
    ("Повыш. №1", "Программа «Заметки»", "adv01_notes.py", "Tkinter"),
]


class Launcher:
    """Окно со списком заданий и кнопкой запуска."""

    def __init__(self, master):
        self.master = master
        master.title("Лабораторная работа №5 — вариант 8")
        master.geometry("620x380")
        master.minsize(520, 320)

        self.processes = []

        self._build_header()
        self._build_table()
        self._build_buttons()
        self._build_status()

    def _build_header(self):
        frame = ttk.Frame(self.master, padding=(12, 12, 12, 4))
        frame.pack(fill=tk.X)

        ttk.Label(frame, text="Визуальное программирование на Python",
                  font=("Helvetica", 14, "bold")).pack(anchor=tk.W)
        ttk.Label(frame, text="Кострикин Н. А., группа 220042-11, вариант 8",
                  foreground="#555").pack(anchor=tk.W)

    def _build_table(self):
        frame = ttk.Frame(self.master, padding=(12, 4))
        frame.pack(fill=tk.BOTH, expand=True)

        columns = ("level", "name", "toolkit")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings",
                                 height=len(TASKS), selectmode="browse")
        self.tree.heading("level", text="Задание")
        self.tree.heading("name", text="Название")
        self.tree.heading("toolkit", text="Библиотека")
        self.tree.column("level", width=90, anchor=tk.W)
        self.tree.column("name", width=330, anchor=tk.W)
        self.tree.column("toolkit", width=90, anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True)

        for level, name, script, toolkit in TASKS:
            self.tree.insert("", tk.END, iid=script,
                             values=(level, name, toolkit))

        self.tree.selection_set(TASKS[0][2])
        self.tree.bind("<Double-Button-1>", lambda event: self.run_selected())

    def _build_buttons(self):
        frame = ttk.Frame(self.master, padding=(12, 4, 12, 10))
        frame.pack(fill=tk.X)

        ttk.Button(frame, text="Запустить",
                   command=self.run_selected).pack(side=tk.LEFT)
        ttk.Button(frame, text="Запустить все",
                   command=self.run_all).pack(side=tk.LEFT, padx=6)
        ttk.Button(frame, text="Выход",
                   command=self.master.destroy).pack(side=tk.RIGHT)

    def _build_status(self):
        self.status = tk.StringVar(value="Выберите задание и нажмите «Запустить»")
        ttk.Label(self.master, textvariable=self.status, relief=tk.SUNKEN,
                  anchor=tk.W, padding=(6, 3)).pack(fill=tk.X, side=tk.BOTTOM)

    # ---------- запуск ----------

    def launch(self, script):
        """Запускает скрипт отдельным процессом тем же интерпретатором."""
        path = os.path.join(BASE_DIR, script)
        if not os.path.exists(path):
            messagebox.showerror("Файл не найден", f"Нет файла {script}")
            return False

        try:
            process = subprocess.Popen([sys.executable, path], cwd=BASE_DIR)
        except OSError as error:
            messagebox.showerror("Ошибка запуска", str(error))
            return False

        self.processes.append(process)
        return True

    def run_selected(self):
        selection = self.tree.selection()
        if not selection:
            self.status.set("Сначала выберите задание в списке")
            return

        script = selection[0]
        if self.launch(script):
            self.status.set(f"Запущено: {script}")

    def run_all(self):
        started = sum(1 for _, _, script, _ in TASKS if self.launch(script))
        self.status.set(f"Запущено процессов: {started}")


def main():
    root = tk.Tk()
    Launcher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
