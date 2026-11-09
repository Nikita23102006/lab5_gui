"""Задание средней сложности №8: диалог выбора файла."""

import datetime
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Фильтры расширений. Пара ("описание", "маска"); маска "*.*" — все файлы.
TEXT_FILE_TYPES = [
    ("Текстовые файлы", "*.txt"),
    ("Python-файлы", "*.py"),
    ("Markdown", "*.md"),
    ("Все файлы", "*.*"),
]

PREVIEW_LIMIT = 4000  # сколько символов показывать в предпросмотре


def describe_file(path):
    """Возвращает список пар (свойство, значение) для файла."""
    stat = os.stat(path)
    modified = datetime.datetime.fromtimestamp(stat.st_mtime)

    return [
        ("Имя", os.path.basename(path)),
        ("Папка", os.path.dirname(path) or "."),
        ("Размер", f"{stat.st_size} байт ({stat.st_size / 1024:.1f} КБ)"),
        ("Изменён", modified.strftime("%d.%m.%Y %H:%M:%S")),
        ("Расширение", os.path.splitext(path)[1] or "нет"),
    ]


def read_preview(path, limit=PREVIEW_LIMIT):
    """Читает начало текстового файла. Возвращает (текст, успех)."""
    try:
        with open(path, encoding="utf-8") as file:
            content = file.read(limit)
    except UnicodeDecodeError:
        return "Файл не в кодировке UTF-8 — возможно, он двоичный.", False
    except OSError as error:
        return f"Не удалось прочитать файл: {error}", False

    if len(content) == limit:
        content += f"\n\n... показаны первые {limit} символов"
    return content, True


class FileDialogApp:
    """Окно, демонстрирующее четыре стандартных файловых диалога."""

    def __init__(self, master):
        self.master = master
        master.title("Задание 8 — диалог выбора файла")
        master.geometry("660x480")
        master.minsize(520, 400)

        self.current_path = None

        self._build_buttons()
        self._build_info()
        self._build_preview()
        self._build_status()

    def _build_buttons(self):
        frame = ttk.Frame(self.master, padding=(10, 10, 10, 4))
        frame.pack(fill=tk.X)

        buttons = (
            ("Открыть файл", self.open_file),
            ("Несколько файлов", self.open_many),
            ("Выбрать папку", self.choose_directory),
            ("Сохранить как", self.save_as),
        )
        for text, command in buttons:
            ttk.Button(frame, text=text,
                       command=command).pack(side=tk.LEFT, padx=(0, 6))

    def _build_info(self):
        frame = ttk.LabelFrame(self.master, text="Свойства файла", padding=6)
        frame.pack(fill=tk.X, padx=10, pady=4)

        self.info = tk.StringVar(value="Файл не выбран")
        ttk.Label(frame, textvariable=self.info,
                  justify=tk.LEFT, anchor=tk.W).pack(fill=tk.X)

    def _build_preview(self):
        frame = ttk.LabelFrame(self.master, text="Содержимое", padding=4)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.preview = tk.Text(frame, wrap=tk.WORD, height=10,
                               yscrollcommand=scrollbar.set)
        self.preview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.preview.yview)

    def _build_status(self):
        self.status = tk.StringVar(value="Готово")
        ttk.Label(self.master, textvariable=self.status, relief=tk.SUNKEN,
                  anchor=tk.W, padding=(6, 3)).pack(fill=tk.X, side=tk.BOTTOM)

    # ---------- действия ----------

    def open_file(self):
        """askopenfilename возвращает путь или пустую строку при отмене."""
        path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=TEXT_FILE_TYPES,
            initialdir=os.path.expanduser("~"),
        )
        if not path:
            self.status.set("Выбор отменён")
            return

        self.show_file(path)

    def open_many(self):
        """askopenfilenames возвращает кортеж путей."""
        paths = filedialog.askopenfilenames(
            title="Выберите несколько файлов",
            filetypes=TEXT_FILE_TYPES,
        )
        if not paths:
            self.status.set("Выбор отменён")
            return

        self.info.set(f"Выбрано файлов: {len(paths)}")
        self.preview.delete("1.0", tk.END)
        total = 0
        for path in paths:
            size = os.path.getsize(path)
            total += size
            self.preview.insert(tk.END, f"{size:>10} байт  {path}\n")
        self.preview.insert(tk.END, f"\nОбщий размер: {total} байт")
        self.status.set(f"Выбрано {len(paths)} файлов")

    def choose_directory(self):
        """askdirectory выбирает папку, а не файл."""
        path = filedialog.askdirectory(title="Выберите папку")
        if not path:
            self.status.set("Выбор отменён")
            return

        entries = sorted(os.listdir(path))
        self.info.set(f"Папка: {path}\nОбъектов внутри: {len(entries)}")

        self.preview.delete("1.0", tk.END)
        for name in entries:
            full = os.path.join(path, name)
            mark = "[папка]" if os.path.isdir(full) else "       "
            self.preview.insert(tk.END, f"{mark} {name}\n")
        self.status.set(f"Открыта папка {os.path.basename(path)}")

    def save_as(self):
        """asksaveasfilename спрашивает подтверждение при перезаписи."""
        if not self.preview.get("1.0", tk.END).strip():
            messagebox.showinfo("Нечего сохранять",
                                "Сначала откройте файл или папку.")
            return

        path = filedialog.asksaveasfilename(
            title="Сохранить содержимое как",
            defaultextension=".txt",
            filetypes=TEXT_FILE_TYPES,
            initialfile="копия.txt",
        )
        if not path:
            self.status.set("Сохранение отменено")
            return

        try:
            with open(path, "w", encoding="utf-8") as file:
                file.write(self.preview.get("1.0", tk.END))
        except OSError as error:
            messagebox.showerror("Ошибка", f"Не удалось сохранить:\n{error}")
            return

        self.status.set(f"Сохранено: {path}")

    def show_file(self, path):
        """Показывает свойства и содержимое выбранного файла."""
        self.current_path = path

        properties = describe_file(path)
        self.info.set("   ".join(f"{name}: {value}"
                                 for name, value in properties[:3]))

        content, ok = read_preview(path)
        self.preview.delete("1.0", tk.END)
        self.preview.insert("1.0", content)
        self.status.set("Файл открыт" if ok else "Файл открыт частично")


def main():
    root = tk.Tk()
    FileDialogApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
