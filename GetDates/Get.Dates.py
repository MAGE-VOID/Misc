import os
from docx import Document
from datetime import datetime, timedelta
from module_dates_v2 import generate_module_dates
import tkinter as tk
from tkinter import simpledialog
from tkcalendar import DateEntry

# Input
start_date = datetime(2024, 3, 9)
num_modules = 5
module_info_text = generate_module_dates(start_date, num_modules)

print(module_info_text)


def show_results(info_dict):
    results_window = tk.Tk()
    results_window.title("Resultados del Programa")

    # Crear un widget de texto para mostrar los resultados
    text_widget = tk.Text(results_window, height=50, width=70)
    text_widget.pack(padx=10, pady=10)

    # Insertar los resultados en el widget de texto
    for key, value in info_dict.items():
        text_widget.insert(tk.END, f"{key}:\n")
        if isinstance(value, list):
            for item in value:
                for sub_key, sub_value in item.items():
                    text_widget.insert(tk.END, f"  {sub_key}: {sub_value}\n")
        elif isinstance(value, dict):
            for sub_key, sub_value in value.items():
                text_widget.insert(tk.END, f"  {sub_key}: {sub_value}\n")
        else:
            text_widget.insert(tk.END, f"  {value}\n")
        text_widget.insert(tk.END, "\n")

    # Deshabilitar el widget de texto para evitar la edición del contenido
    text_widget.config(state=tk.DISABLED)

    # Calcular la posición central y posicionar la ventana
    results_window.update_idletasks()
    width = results_window.winfo_width()
    height = results_window.winfo_height()
    x = (results_window.winfo_screenwidth() // 2) - (width // 2)
    y = (results_window.winfo_screenheight() // 2) - (height // 2)
    results_window.geometry(f"+{x}+{y}")

    results_window.mainloop()


def request_inputs():
    def on_date_select():
        num_modules = simpledialog.askinteger(
            "Número de módulos", "Introduce el número de módulos:"
        )
        start_date = cal.get_date()
        root.destroy()

        # Suponiendo que la función generate_module_dates está definida y retorna el diccionario deseado
        module_info_text = generate_module_dates(start_date, num_modules)

        show_results(module_info_text)

    root = tk.Tk()
    root.title("Seleccione la fecha de inicio")
    tk.Label(root, text="Seleccione la fecha de inicio:").pack(padx=10, pady=10)

    cal = DateEntry(
        root,
        width=12,
        background="darkblue",
        foreground="white",
        borderwidth=2,
        locale="es_ES",
        date_pattern="dd/MM/yyyy",
    )
    cal.pack(padx=10, pady=10)

    tk.Button(root, text="Aceptar", command=on_date_select).pack(pady=20)

    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"+{x}+{y}")

    root.mainloop()


request_inputs()
