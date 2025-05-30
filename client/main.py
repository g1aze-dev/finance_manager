import tkinter as tk
from tkinter import ttk
from api_client import add_transaction, get_transactions, delete_transaction
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from typing import Dict, List, Any, Optional


class TransationListWindow(tk.Toplevel):
    """Окно для отображения списка транзакций в виде таблицы.

    Attributes:
        parent: Родительское окно.
        transactions: Список транзакций, полученный из API.
        tree: Виджет Treeview для отображения данных.
        scrollbar: Полоса прокрутки для таблицы.
    """

    def __init__(self, parent: tk.Tk) -> None:
        """Инициализирует окно списка транзакций.

        Args:
            parent: Родительское окно приложения.
        """
        super().__init__(parent)
        self.title("Отсчет")
        self.transactions: List[Dict[str, Any]] = get_transactions()  # Предполагается, что это возвращает список словарей
        
        # Создаем Treeview
        self.tree: ttk.Treeview = ttk.Treeview(self, columns=("ID", "Amount", "Category", "Type", "Data"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Amount", text="Цена")
        self.tree.heading("Category", text="Категория")
        self.tree.heading("Type", text="Тип")
        self.tree.heading("Data", text="Дата")
        
        # Заполняем данными (используем ключи словаря)
        for transaction in self.transactions:
            self.tree.insert("", tk.END, values=(
                transaction['id'], 
                transaction['amount'], 
                transaction['category'], 
                transaction['type'],
                transaction['date']
            ))
        
        self.scrollbar: ttk.Scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)
        
        self.pack_widgets()
    
    def pack_widgets(self) -> None:
        """Упаковывает виджеты в окне."""
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


class Add_Notes(tk.Toplevel):
    """Окно для добавления новых транзакций.

    Attributes:
        parent: Родительское окно.
        title_label: Заголовок окна.
        amount_label, amount_entry: Поле для ввода суммы.
        category_label, category_entry: Поле для ввода категории.
        type_label, type_entry: Поле для ввода типа транзакции.
        date_label, date_entry: Поле для ввода даты.
        add_button: Кнопка добавления транзакции.
    """

    def __init__(self, parent: tk.Tk) -> None:
        """Инициализирует окно добавления транзакций.

        Args:
            parent: Родительское окно приложения.
        """
        super().__init__(parent)
        self.title("Добавление записей")
        
        self.title_label: tk.Label = tk.Label(self, text="Добавление записей", font=("Helvetica", 24))
        
        # Поля для ввода
        self.amount_label: tk.Label = tk.Label(self, text="Сумма:")
        self.amount_entry: tk.Entry = tk.Entry(self)
        
        self.category_label: tk.Label = tk.Label(self, text="Категория:")
        self.category_entry: tk.Entry = tk.Entry(self)
        
        self.type_label: tk.Label = tk.Label(self, text="Тип (расход или доход):")
        self.type_entry: tk.Entry = tk.Entry(self)
        
        self.date_label: tk.Label = tk.Label(self, text="Дата в формате гггг-мм-дд:")
        self.date_entry: tk.Entry = tk.Entry(self)

        # Кнопка добавления
        self.add_button: ttk.Button = ttk.Button(self, text="Добавить", command=self.add_transaction)
        
        self.pack_widgets()
        
    def pack_widgets(self) -> None:
        """Упаковывает виджеты в окне."""
        self.title_label.pack(pady=10)
        
        self.amount_label.pack()
        self.amount_entry.pack()
        
        self.category_label.pack()
        self.category_entry.pack()
        
        self.date_label.pack()
        self.date_entry.pack()
        
        self.type_label.pack()
        self.type_entry.pack()
        
        self.add_button.pack(pady=10)
    
    def add_transaction(self) -> None:
        """Добавляет новую транзакцию через API."""
        try:
            amount: float = float(self.amount_entry.get())
            category: str = self.category_entry.get()
            date: str = self.date_entry.get()
            transaction_type: str = self.type_entry.get()
            
            add_transaction(amount, category, date, transaction_type)
            print("Транзакция добавлена!")
        except ValueError:
            print("Ошибка ввода данных!")


class Del_Notes(tk.Toplevel):
    """Окно для удаления транзакций.

    Attributes:
        parent: Родительское окно.
        title_label: Заголовок окна.
        category_label, category_entry: Поле для ввода категории.
        type_label, type_entry: Поле для ввода типа транзакции.
        date_label, date_entry: Поле для ввода даты.
        delete_button: Кнопка удаления транзакции.
    """

    def __init__(self, parent: tk.Tk) -> None:
        """Инициализирует окно удаления транзакций.

        Args:
            parent: Родительское окно приложения.
        """
        super().__init__(parent)
        self.title("Удаление записей")
        
        self.title_label: tk.Label = tk.Label(self, text="Удаление записей", font=("Helvetica", 24))
        
        # Поля для ввода
        self.category_label: tk.Label = tk.Label(self, text="Категория:")
        self.category_entry: tk.Entry = tk.Entry(self)
        
        self.type_label: tk.Label = tk.Label(self, text="Тип (расход или доход):")
        self.type_entry: tk.Entry = tk.Entry(self)
        
        self.date_label: tk.Label = tk.Label(self, text="Дата в формате гггг-мм-дд:")
        self.date_entry: tk.Entry = tk.Entry(self)

        # Кнопка добавления
        self.delete_button: ttk.Button = ttk.Button(self, text="Удалить", command=self.delete_transaction)
        
        self.pack_widgets()
        
    def pack_widgets(self) -> None:
        """Упаковывает виджеты в окне."""
        self.title_label.pack(pady=10)
        self.category_label.pack()
        self.category_entry.pack()
        
        self.date_label.pack()
        self.date_entry.pack()
        
        self.type_label.pack()
        self.type_entry.pack()
        
        self.delete_button.pack(pady=10)
    
    def delete_transaction(self) -> None:
        """Удаляет транзакцию через API."""
        try:
            category: str = self.category_entry.get()
            date: str = self.date_entry.get()
            transaction_type: str = self.type_entry.get()
            
            delete_transaction(category, date, transaction_type)
            print("Транзакция удалена!")
        except ValueError:
            print("Ошибка ввода данных!")


class ShowStat(tk.Toplevel):
    """Окно для отображения статистики по транзакциям.

    Attributes:
        parent: Родительское окно.
        transactions: Список транзакций.
        pie_frame: Фрейм для круговых диаграмм.
        pie_canvas_1, pie_canvas_2: Холсты для круговых диаграмм.
        bar_frame: Фрейм для столбчатых диаграмм.
        bar_canvas_1, bar_canvas_2: Холсты для столбчатых диаграмм.
        title_label: Заголовок окна.
        show_pie_button, hide_pie_button: Кнопки управления круговыми диаграммами.
        show_bar_button, hide_bar_button: Кнопки управления столбчатыми диаграммами.
        categories_income: Словарь категорий доходов.
        categories_expenditure: Словарь категорий расходов.
    """

    def __init__(self, parent: tk.Tk) -> None:
        """Инициализирует окно статистики.

        Args:
            parent: Родительское окно приложения.
        """
        super().__init__(parent)
        self.title("Статистика")
        self.transactions: List[Dict[str, Any]] = get_transactions()
        
        # Для круговых диаграмм
        self.pie_frame: Optional[ttk.Frame] = None
        self.pie_canvas_1: Optional[FigureCanvasTkAgg] = None
        self.pie_canvas_2: Optional[FigureCanvasTkAgg] = None
        
        # Для столбчатых диаграмм
        self.bar_frame: Optional[ttk.Frame] = None
        self.bar_canvas_1: Optional[FigureCanvasTkAgg] = None
        self.bar_canvas_2: Optional[FigureCanvasTkAgg] = None
        
        self.title_label: ttk.Label = ttk.Label(self, text="Статистика", font=("Helvetica", 24))
        
        # Кнопки для круговых диаграмм
        self.show_pie_button: ttk.Button = ttk.Button(
            self, 
            text="Показать круговую диаграмму", 
            command=self.show_pie
        )
        self.hide_pie_button: ttk.Button = ttk.Button(
            self, 
            text="Скрыть круговую диаграмму", 
            command=self.hide_pie_chart,
            state=tk.DISABLED
        )
        
        # Кнопки для столбчатых диаграмм
        self.show_bar_button: ttk.Button = ttk.Button(
            self, 
            text="Показать столбчатую диаграмму", 
            command=self.show_bar
        )
        self.hide_bar_button: ttk.Button = ttk.Button(
            self, 
            text="Скрыть столбчатую диаграмму", 
            command=self.hide_bar_chart,
            state=tk.DISABLED
        )
        
        self.categories_income: Dict[str, float] = {}
        self.categories_expenditure: Dict[str, float] = {}
        self.pack_widgets()
        
    def collect_data(self) -> None:
        """Собирает данные по категориям из списка транзакций."""
        self.categories_income.clear()
        self.categories_expenditure.clear()
        
        for t in self.transactions:
            if t["type"] == 'доход':
                self.categories_income[t["category"]] = self.categories_income.get(t["category"], 0) + t["amount"]
            else:
                self.categories_expenditure[t["category"]] = self.categories_expenditure.get(t["category"], 0) + t["amount"]
    
    def show_pie(self) -> None:
        """Отображает круговые диаграммы доходов и расходов."""
        self.collect_data()
        
        # Очищаем предыдущие диаграммы
        if self.pie_frame:
            self.pie_frame.destroy()
            
        self.pie_frame = ttk.Frame(self)
        self.pie_frame.pack(pady=10)

        # Общие параметры для диаграмм
        fig_size = (5, 4)
        margin = 0.2

        # Диаграмма доходов
        fig_1 = plt.Figure(figsize=fig_size)
        ax_1 = fig_1.add_subplot(111)
        fig_1.subplots_adjust(left=margin, right=1-margin, top=1-margin, bottom=margin)
        ax_1.pie(self.categories_income.values(), 
               labels=self.categories_income.keys(), 
               autopct="%1.1f%%", 
               radius=1.0)
        ax_1.set_title('Доходы')

        # Диаграмма расходов
        fig_2 = plt.Figure(figsize=fig_size)
        ax_2 = fig_2.add_subplot(111)
        fig_2.subplots_adjust(left=margin, right=1-margin, top=1-margin, bottom=margin)
        ax_2.pie(self.categories_expenditure.values(), 
               labels=self.categories_expenditure.keys(), 
               autopct="%1.1f%%", 
               radius=1.0)
        ax_2.set_title('Расходы')

        # Размещаем диаграммы
        self.pie_canvas_1 = FigureCanvasTkAgg(fig_1, master=self.pie_frame)
        self.pie_canvas_1.draw()
        self.pie_canvas_1.get_tk_widget().pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        self.pie_canvas_2 = FigureCanvasTkAgg(fig_2, master=self.pie_frame)
        self.pie_canvas_2.draw()
        self.pie_canvas_2.get_tk_widget().pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)

        # Обновляем кнопки
        self.show_pie_button.config(state=tk.DISABLED)
        self.hide_pie_button.config(state=tk.NORMAL)
        self.show_bar_button.config(state=tk.DISABLED)
    
    def hide_pie_chart(self) -> None:
        """Скрывает круговые диаграммы."""
        if self.pie_frame:
            self.pie_frame.destroy()
            self.pie_frame = None
            plt.close('all')  # Закрываем все фигуры matplotlib
            self.pie_canvas_1 = None
            self.pie_canvas_2 = None
            
        self.show_pie_button.config(state=tk.NORMAL)
        self.hide_pie_button.config(state=tk.DISABLED)
        self.show_bar_button.config(state=tk.NORMAL)
    
    def show_bar(self) -> None:
        """Отображает столбчатые диаграммы доходов и расходов."""
        self.collect_data()
        
        # Очищаем предыдущие диаграммы
        if self.bar_frame:
            self.bar_frame.destroy()
            
        self.bar_frame = ttk.Frame(self)
        self.bar_frame.pack(pady=10)

        # Общие параметры для диаграмм
        fig_size = (5, 4)
        margin = 0.2

        # Диаграмма доходов
        fig_1 = plt.Figure(figsize=fig_size)
        ax_1 = fig_1.add_subplot(111)
        fig_1.subplots_adjust(left=margin, right=1-margin, top=1-margin, bottom=margin)
        
        # Создаем столбчатую диаграмму для доходов
        categories = list(self.categories_income.keys())
        values = list(self.categories_income.values())
        ax_1.bar(categories, values)
        ax_1.set_title('Доходы')
        ax_1.tick_params(axis='x', rotation=45)  # Поворачиваем подписи для читаемости

        # Диаграмма расходов
        fig_2 = plt.Figure(figsize=fig_size)
        ax_2 = fig_2.add_subplot(111)
        fig_2.subplots_adjust(left=margin, right=1-margin, top=1-margin, bottom=margin)
        
        # Создаем столбчатую диаграмму для расходов
        categories = list(self.categories_expenditure.keys())
        values = list(self.categories_expenditure.values())
        ax_2.bar(categories, values)
        ax_2.set_title('Расходы')
        ax_2.tick_params(axis='x', rotation=45)  # Поворачиваем подписи для читаемости

        # Размещаем диаграммы
        self.bar_canvas_1 = FigureCanvasTkAgg(fig_1, master=self.bar_frame)
        self.bar_canvas_1.draw()
        self.bar_canvas_1.get_tk_widget().pack(side=tk.LEFT, padx=10, fill=tk.BOTH, expand=True)

        self.bar_canvas_2 = FigureCanvasTkAgg(fig_2, master=self.bar_frame)
        self.bar_canvas_2.draw()
        self.bar_canvas_2.get_tk_widget().pack(side=tk.RIGHT, padx=10, fill=tk.BOTH, expand=True)

        # Обновляем кнопки
        self.show_bar_button.config(state=tk.DISABLED)
        self.hide_bar_button.config(state=tk.NORMAL)
        self.show_pie_button.config(state=tk.DISABLED)
    
    def hide_bar_chart(self) -> None:
        """Скрывает столбчатые диаграммы."""
        if self.bar_frame:
            self.bar_frame.destroy()
            self.bar_frame = None
            plt.close('all')  # Закрываем все фигуры matplotlib
            self.bar_canvas_1 = None
            self.bar_canvas_2 = None
            
        self.show_bar_button.config(state=tk.NORMAL)
        self.hide_bar_button.config(state=tk.DISABLED)
        self.show_pie_button.config(state=tk.NORMAL)
    
    def pack_widgets(self) -> None:
        """Упаковывает виджеты в окне."""
        self.title_label.pack(pady=10)
        
        # Кнопки для круговых диаграмм
        self.show_pie_button.pack(pady=5)
        self.hide_pie_button.pack(pady=5)
        
        # Кнопки для столбчатых диаграмм
        self.show_bar_button.pack(pady=5)
        self.hide_bar_button.pack(pady=5)


class Application(tk.Tk):
    """Главное окно приложения финансового менеджера.

    Attributes:
        title_label: Заголовок приложения.
        add_notes_button: Кнопка для открытия окна добавления записей.
        del_notes_button: Кнопка для открытия окна удаления записей.
        show_stat_button: Кнопка для открытия окна статистики.
        show_transaction_list_button: Кнопка для открытия списка транзакций.
    """

    def __init__(self) -> None:
        """Инициализирует главное окно приложения."""
        super().__init__()
        self.title("Финансовый менеджер")
        
        self.title_label: tk.Label = tk.Label(self, text="Финансовый менеджер", font=("Helvetica", 24))
        self.add_notes_button: ttk.Button = ttk.Button(self, text="Добавить запись", command=self.open_add_notes)
        self.del_notes_button: ttk.Button = ttk.Button(self, text="Удалить запись", command=self.open_del_notes)
        self.show_stat_button: ttk.Button = ttk.Button(self, text="Показать статистику", command=self.open_show_stat)
        self.show_transaction_list_button: ttk.Button = ttk.Button(
            self, 
            text="Получить отсчет", 
            command=self.transaction_list_show
        )
        self.pack_widgets()
    
    def transaction_list_show(self) -> None:
        """Открывает окно списка транзакций."""
        TransationListWindow(self)
    
    def open_show_stat(self) -> None:
        """Открывает окно статистики."""
        ShowStat(self)
    
    def open_del_notes(self) -> None:
        """Открывает окно удаления записей."""
        Del_Notes(self)
    
    def open_add_notes(self) -> None:
        """Открывает окно добавления записей."""
        Add_Notes(self)
    
    def pack_widgets(self) -> None:
        """Упаковывает виджеты в главном окне."""
        self.title_label.pack(pady=20)
        self.add_notes_button.pack(pady=10)
        self.del_notes_button.pack(pady=10)
        self.show_stat_button.pack(pady=10)
        self.show_transaction_list_button.pack(pady=10)


if __name__ == "__main__":
    app = Application()
    app.mainloop()