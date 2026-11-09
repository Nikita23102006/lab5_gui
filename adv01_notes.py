"""Задание повышенной сложности №1: программа «Заметки» с сохранением в файл."""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from task08_file_dialog import TEXT_FILE_TYPES


class NotesApp:
    """Текстовый редактор: создать, открыть, сохранить, сохранить как."""

    def __init__(self, master):
        self.master = master
        self.current_path = None   # None означает «файл ещё не сохраняли»
        self.saved_text = ""       # содержимое на момент последнего сохранения

        master.geometry("720x520")
        master.minsize(480, 360)

        self._build_menu()
        self._build_toolbar()
        self._build_editor()
        self._build_status()

        self.update_title()

        # Перехватываем закрытие окна, чтобы предложить сохранить изменения.
        master.protocol("WM_DELETE_WINDOW", self.on_close)

        # Горячие клавиши.
        master.bind("<Control-n>", lambda event: self.new_file())
        master.bind("<Control-o>", lambda event: self.open_file())
        master.bind("<Control-s>", lambda event: self.save_file())

    def _build_menu(self):
        menubar = tk.Menu(self.master)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Создать", accelerator="Ctrl+N",
                              command=self.new_file)
        file_menu.add_command(label="Открыть...", accelerator="Ctrl+O",
                              command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Сохранить", accelerator="Ctrl+S",
                              command=self.save_file)
        file_menu.add_command(label="Сохранить как...",
                              command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.on_close)
        menubar.add_cascade(label="Файл", menu=file_menu)

        self.master.config(menu=menubar)

    def _build_toolbar(self):
        bar = ttk.Frame(self.master, padding=(8, 6, 8, 2))
        bar.pack(fill=tk.X)

        buttons = (
            ("Создать", self.new_file),
            ("Открыть", self.open_file),
            ("Сохранить", self.save_file),
            ("Сохранить как", self.save_file_as),
        )
        for text, command in buttons:
            ttk.Button(bar, text=text,
                       command=command).pack(side=tk.LEFT, padx=(0, 6))

    def _build_editor(self):
        frame = ttk.Frame(self.master, padding=(8, 4))
        frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text = tk.Text(frame, wrap=tk.WORD, undo=True,
                            font=("Helvetica", 12),
                            yscrollcommand=scrollbar.set)
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text.yview)

        # Любое изменение текста обновляет заголовок и строку состояния.
        self.text.bind("<<Modified>>", self.on_modified)
        self.text.bind("<KeyRelease>", lambda event: self.update_status())

    def _build_status(self):
        self.status = tk.StringVar()
        ttk.Label(self.master, textvariable=self.status, relief=tk.SUNKEN,
                  anchor=tk.W, padding=(6, 3)).pack(fill=tk.X, side=tk.BOTTOM)
        self.update_status()

    # ---------- состояние ----------

    def get_text(self):
        """Текст редактора без служебного перевода строки в конце."""
        return self.text.get("1.0", "end-1c")

    def is_modified(self):
        """Есть ли несохранённые изменения."""
        return self.get_text() != self.saved_text

    def update_title(self):
        name = os.path.basename(self.current_path) if self.current_path \
            else "Без имени"
        mark = " *" if self.is_modified() else ""
        self.master.title(f"{name}{mark} — Заметки")

    def update_status(self):
        content = self.get_text()
        lines = content.count("\n") + 1
        words = len(content.split())
        where = self.current_path or "файл не сохранён"
        self.status.set(f"Строк: {lines}   Слов: {words}   "
                        f"Символов: {len(content)}   |   {where}")

    def on_modified(self, event=None):
        """Обработчик виртуального события <<Modified>>.

        Флаг modified надо сбрасывать вручную, иначе событие
        больше не повторится.
        """
        self.text.edit_modified(False)
        self.update_title()
        self.update_status()

    def confirm_discard(self):
        """Спрашивает про несохранённые изменения.

        Возвращает True, если можно продолжать.
        """
        if not self.is_modified():
            return True

        answer = messagebox.askyesnocancel(
            "Несохранённые изменения",
            "Текст изменён. Сохранить перед продолжением?")

        if answer is None:        # Отмена
            return False
        if answer:                # Да
            return self.save_file()
        return True               # Нет — продолжаем без сохранения

    # ---------- действия ----------

    def new_file(self):
        if not self.confirm_discard():
            return

        self.text.delete("1.0", tk.END)
        self.current_path = None
        self.saved_text = ""
        self.update_title()
        self.update_status()

    def open_file(self):
        if not self.confirm_discard():
            return

        path = filedialog.askopenfilename(title="Открыть заметку",
                                          filetypes=TEXT_FILE_TYPES)
        if not path:
            return

        try:
            with open(path, encoding="utf-8") as file:
                content = file.read()
        except (OSError, UnicodeDecodeError) as error:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{error}")
            return

        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", content)
        self.current_path = path
        self.saved_text = content
        self.update_title()
        self.update_status()

    def save_file(self):
        """Сохраняет в текущий файл. Возвращает True при успехе."""
        if self.current_path is None:
            return self.save_file_as()
        return self.write_to(self.current_path)

    def save_file_as(self):
        """Спрашивает имя файла и сохраняет. Возвращает True при успехе."""
        path = filedialog.asksaveasfilename(
            title="Сохранить заметку как",
            defaultextension=".txt",
            filetypes=TEXT_FILE_TYPES,
            initialfile="заметка.txt",
        )
        if not path:
            return False
        return self.write_to(path)

    def write_to(self, path):
        """Записывает текст в файл."""
        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(self.get_text())
        except OSError as error:
            messagebox.showerror("Ошибка", f"Не удалось сохранить:\n{error}")
            return False

        self.current_path = path
        self.saved_text = self.get_text()
        self.update_title()
        self.update_status()
        return True

    def on_close(self):
        if self.confirm_discard():
            self.master.destroy()


def main():
    root = tk.Tk()
    NotesApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
