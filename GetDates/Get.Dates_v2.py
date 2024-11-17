import os
from docx import Document
from datetime import datetime, timedelta
from module_dates_v2 import generate_module_dates
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

class ModuleSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Programa de Módulos")
        self.root.geometry("800x600")

        # Variables
        self.start_date_var = tk.StringVar()
        self.num_modules_var = tk.StringVar(value="1")

        # Interfaz gráfica
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style(self.root)
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 12))
        style.configure('TButton', background='#4CAF50', foreground='white', font=('Helvetica', 12))
        style.configure('TSpinbox', font=('Helvetica', 14))
        style.configure('TEntry', font=('Helvetica', 12))

        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame izquierdo para controles
        controls_frame = ttk.Frame(main_frame, padding="10")
        controls_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Fecha de inicio
        ttk.Label(controls_frame, text="Seleccione la fecha de inicio:").pack(pady=5)
        self.cal = DateEntry(
            controls_frame,
            width=15,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            locale="es_ES",
            date_pattern="dd/MM/yyyy",
            textvariable=self.start_date_var,
        )
        self.cal.pack(pady=5)

        # Número de módulos
        ttk.Label(controls_frame, text="Número de módulos:").pack(pady=5)
        self.num_modules_spinbox = ttk.Spinbox(
            controls_frame, from_=1, to=10, textvariable=self.num_modules_var, width=8
        )
        self.num_modules_spinbox.pack(pady=5)

        # Frame derecho para resultados
        results_frame = ttk.Frame(main_frame, padding="10")
        results_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.text_widget = tk.Text(results_frame, wrap=tk.WORD, font=('Helvetica', 12))
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(results_frame, command=self.text_widget.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_widget.config(yscrollcommand=scrollbar.set)
        self.text_widget.config(state=tk.DISABLED)

        # Actualizar resultados en tiempo real
        self.start_date_var.trace_add("write", lambda *args: self.update_results())
        self.num_modules_var.trace_add("write", lambda *args: self.update_results())

    def update_results(self):
        # Obtener los valores seleccionados
        start_date_str = self.start_date_var.get()
        num_modules_str = self.num_modules_var.get()

        # Validar los campos
        if not start_date_str or not num_modules_str.isdigit():
            return

        num_modules = int(num_modules_str)

        # Convertir la fecha de inicio
        try:
            start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
        except ValueError:
            return

        # Generar la información del módulo
        module_info_text = generate_module_dates(start_date, num_modules)

        # Mostrar los resultados
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete("1.0", tk.END)

        for key, value in module_info_text.items():
            self.text_widget.insert(tk.END, f"{key}:\n", 'header')
            if isinstance(value, list):
                for item in value:
                    for sub_key, sub_value in item.items():
                        self.text_widget.insert(tk.END, f"  {sub_key}: {sub_value}\n", 'content')
            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    self.text_widget.insert(tk.END, f"  {sub_key}: {sub_value}\n", 'content')
            else:
                self.text_widget.insert(tk.END, f"  {value}\n", 'content')
            self.text_widget.insert(tk.END, "\n")

        self.text_widget.config(state=tk.DISABLED)

        self.text_widget.tag_configure('header', font=('Helvetica', 12, 'bold'))
        self.text_widget.tag_configure('content', font=('Helvetica', 12))

if __name__ == "__main__":
    root = tk.Tk()
    app = ModuleSchedulerApp(root)
    root.mainloop()
