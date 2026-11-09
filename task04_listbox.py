"""Задание средней сложности №4: список (Listbox) и выбор элемента."""

import tkinter as tk
from tkinter import ttk

LANGUAGES = [
    "Python", "JavaScript", "Java", "C++", "C#", "Go",
    "Rust", "Kotlin", "Swift", "TypeScript", "PHP", "Ruby",
]


class ListboxApp:
    """Окно со списком: выбор, добавление и удаление элементов."""

    def __init__(self, master):
        self.master = master
        master.title("Задание 4 — список и выбор элемента")
        master.geometry("520x420")
        master.minsize(420, 360)

        self._build_list()
        self._build_controls()
        self._build_status()

        # Заполняем список стартовыми данными.
        for language in LANGUAGES:
            self.listbox.insert(tk.END, language)

    def _build_list(self):
        """Список со полосой прокрутки."""
        frame = ttk.LabelFrame(self.master, text="Языки программирования")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 6))

        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.listbox = tk.Listbox(
            frame,
            selectmode=tk.EXTENDED,     # можно выбрать несколько: Ctrl и Shift
            yscrollcommand=scrollbar.set,
            activestyle="dotbox",
            height=10,
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4, pady=4)
        scrollbar.config(command=self.listbox.yview)

        # Событие выбора: срабатывает каждый раз, когда выделение меняется.
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        # Двойной щелчок — отдельное событие.
        self.listbox.bind("<Double-Button-1>", self.on_double_click)

    def _build_controls(self):
        """Поле ввода и кнопки."""
        entry_frame = ttk.Frame(self.master)
        entry_frame.pack(fill=tk.X, padx=10)

        self.entry = ttk.Entry(entry_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", lambda event: self.add_item())

        ttk.Button(entry_frame, text="Добавить",
                   command=self.add_item).pack(side=tk.LEFT, padx=(6, 0))

        button_frame = ttk.Frame(self.master)
        button_frame.pack(fill=tk.X, padx=10, pady=6)

        buttons = (
            ("Удалить выбранное", self.delete_selected),
            ("Очистить", self.clear_all),
            ("Сортировать", self.sort_items),
        )
        for text, command in buttons:
            ttk.Button(button_frame, text=text,
                       command=command).pack(side=tk.LEFT, padx=(0, 6))

    def _build_status(self):
        """Строка состояния внизу окна."""
        self.status = tk.StringVar(value="Выберите элемент списка")
        ttk.Label(self.master, textvariable=self.status,
                  relief=tk.SUNKEN, anchor=tk.W,
                  padding=(6, 3)).pack(fill=tk.X, side=tk.BOTTOM)

    # ---------- обработчики событий ----------

    def on_select(self, event=None):
        """Вызывается при изменении выделения в списке."""
        indices = self.listbox.curselection()

        if not indices:
            self.status.set("Ничего не выбрано")
            return

        if len(indices) == 1:
            index = indices[0]
            value = self.listbox.get(index)
            self.status.set(f"Выбрано: {value}  (индекс {index})")
        else:
            values = ", ".join(self.listbox.get(i) for i in indices)
            self.status.set(f"Выбрано элементов: {len(indices)} — {values}")

    def on_double_click(self, event=None):
        """Двойной щелчок переносит значение в поле ввода."""
        indices = self.listbox.curselection()
        if indices:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.listbox.get(indices[0]))

    # ---------- действия ----------

    def add_item(self):
        """Добавляет значение из поля ввода в конец списка."""
        value = self.entry.get().strip()
        if not value:
            self.status.set("Поле ввода пустое")
            return

        self.listbox.insert(tk.END, value)
        self.entry.delete(0, tk.END)
        self.listbox.see(tk.END)
        self.status.set(f"Добавлено: {value}")

    def delete_selected(self):
        """Удаляет выделенные элементы.

        Идём в обратном порядке: при удалении индексы сдвигаются,
        и прямой проход удалил бы не то, что нужно.
        """
        indices = self.listbox.curselection()
        if not indices:
            self.status.set("Сначала выберите, что удалять")
            return

        for index in reversed(indices):
            self.listbox.delete(index)
        self.status.set(f"Удалено элементов: {len(indices)}")

    def clear_all(self):
        """Очищает список целиком."""
        count = self.listbox.size()
        self.listbox.delete(0, tk.END)
        self.status.set(f"Список очищен (было {count})")

    def sort_items(self):
        """Сортирует список по алфавиту."""
        items = sorted(self.listbox.get(0, tk.END), key=str.lower)
        self.listbox.delete(0, tk.END)
        for item in items:
            self.listbox.insert(tk.END, item)
        self.status.set("Список отсортирован")


def main():
    root = tk.Tk()
    ListboxApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
