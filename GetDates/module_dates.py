from datetime import datetime, timedelta


def find_closest_saturday_improved(start_date):
    day_of_week = start_date.weekday()
    if day_of_week == 5:
        return start_date
    distance_to_last_saturday = (start_date.weekday() - 5) % 7
    distance_to_next_saturday = (5 - start_date.weekday()) % 7
    if distance_to_last_saturday <= distance_to_next_saturday:
        return start_date - timedelta(days=distance_to_last_saturday)
    return start_date + timedelta(days=distance_to_next_saturday)


def find_closest_sunday(date):
    day_of_week = date.weekday()
    distance_to_next_sunday = (6 - day_of_week) % 7
    return date + timedelta(days=distance_to_next_sunday)


def add_one_month_plus_one_day(date):
    month = (date.month % 12) + 1
    year = date.year + (date.month // 12)
    try:
        return datetime(year, month, date.day + 1)
    except ValueError:
        return datetime(year, month, 28) + timedelta(days=1)


def find_closest_monday(date):
    day_of_week = date.weekday()
    distance_to_next_monday = (7 - day_of_week) % 7
    return date + timedelta(days=distance_to_next_monday)


def calculate_module_dates_custom_start_corrected(start_date, num_modules):
    module_dates = []
    evaluation_dates = []
    rectification_dates = []
    platform_close_dates = []

    if num_modules == 1:
        for i in range(4):
            module_date = find_closest_saturday_improved(
                start_date + timedelta(days=7 * i)
            )
            module_dates.append(module_date)
            evaluation_start = module_dates[-1] + timedelta(days=7)
            evaluation_end = evaluation_start + timedelta(days=4)
            evaluation_dates.append((evaluation_start, evaluation_end))
            rectification_start = evaluation_end + timedelta(days=1)
            rectification_end = rectification_start + timedelta(days=3)
            rectification_dates.append((rectification_start, rectification_end))
            platform_close_date = find_closest_monday(rectification_end)
            platform_close_dates.append(platform_close_date)
    else:
        for i in range(num_modules):
            if i == 0:
                module_date = find_closest_saturday_improved(start_date)
            else:
                next_month_date = add_one_month_plus_one_day(module_dates[-1])
                module_date = find_closest_saturday_improved(next_month_date)

            module_dates.append(module_date)
            evaluation_start = add_one_month_plus_one_day(module_date)
            evaluation_end = evaluation_start + timedelta(days=14)
            evaluation_dates.append((evaluation_start, evaluation_end))

            rectification_start = evaluation_end + timedelta(days=1)
            rectification_end = rectification_start + timedelta(days=14)
            rectification_dates.append((rectification_start, rectification_end))

            platform_close_date = find_closest_sunday(rectification_end)
            platform_close_dates.append(platform_close_date)

    return module_dates, evaluation_dates, rectification_dates, platform_close_dates


"""
def calculate_module_dates_custom_start_corrected(start_date, num_modules):
    module_dates = []
    evaluation_dates = []
    rectification_dates = []
    platform_close_dates = []

    if num_modules == 1:
        for i in range(4):
            module_date = find_closest_saturday_improved(
                start_date + timedelta(days=7 * i)
            )
            module_dates.append(module_date)
            evaluation_start = module_dates[-1] + timedelta(days=7)
            evaluation_end = evaluation_start + timedelta(days=4)
            evaluation_dates.append((evaluation_start, evaluation_end))
            rectification_start = evaluation_end + timedelta(days=1)
            rectification_end = rectification_start + timedelta(days=3)
            rectification_dates.append((rectification_start, rectification_end))
            platform_close_date = find_closest_monday(rectification_end)
            platform_close_dates.append(platform_close_date)
    else:
        for i in range(num_modules):
            if i == 0:
                module_date = find_closest_saturday_improved(start_date)
            else:
                month = (module_date.month % 12) + 1
                year = module_date.year + (module_date.month // 12)

                try:
                    next_month_date = datetime(year, month, start_date.day)
                except ValueError:
                    next_month_date = datetime(year, month, 28)

                module_date = find_closest_saturday_improved(next_month_date)

            module_dates.append(module_date)
            evaluation_start = add_one_month_plus_one_day(module_date)
            evaluation_end = evaluation_start + timedelta(days=14)
            evaluation_dates.append((evaluation_start, evaluation_end))

            rectification_start = evaluation_end + timedelta(days=1)
            rectification_end = rectification_start + timedelta(days=14)
            rectification_dates.append((rectification_start, rectification_end))

            platform_close_date = find_closest_sunday(rectification_end)
            platform_close_dates.append(platform_close_date)

    return module_dates, evaluation_dates, rectification_dates, platform_close_dates
"""


def determine_week_of_month(date):
    first_day_of_month = date.replace(day=1)
    day_of_month = date.day
    adjusted_dom = day_of_month + first_day_of_month.weekday()
    return int(adjusted_dom / 7) + (1 if adjusted_dom % 7 > 0 else 0)


days_es = {
    "Monday": "Lunes",
    "Tuesday": "Martes",
    "Wednesday": "Miércoles",
    "Thursday": "Jueves",
    "Friday": "Viernes",
    "Saturday": "Sábado",
    "Sunday": "Domingo",
}
months_es = {
    "January": "Enero",
    "February": "Febrero",
    "March": "Marzo",
    "April": "Abril",
    "May": "Mayo",
    "June": "Junio",
    "July": "Julio",
    "August": "Agosto",
    "September": "Septiembre",
    "October": "Octubre",
    "November": "Noviembre",
    "December": "Diciembre",
}


def format_date_spanish(date):
    """Formatea la fecha dada al formato español."""
    day_spanish = days_es[date.strftime("%A")]
    month_spanish = months_es[date.strftime("%B")]
    return f"{day_spanish}, {date.strftime('%d')} de {month_spanish} del {date.strftime('%Y')}"


def generate_module_dates(start_date, num_modules):
    module_dates, evaluation_dates, rectification_dates, platform_close_dates = (
        calculate_module_dates_custom_start_corrected(start_date, num_modules)
    )
    resultados = {
        "fecha_inicio_programa": format_date_spanish(start_date),
        "fecha_fin_programa": {},
        "semana_de_inicio_del_modulo": {},
        "mes_del_modulo": {},
        "modulos": [],
        "evaluacion_final-actividades_pendientes": {},
        "periodo_subsanacion": {},
        "cierre_plataforma": {},
    }
    etiqueta_semana = ["1era", "2da", "3ra", "4ta", "5ta"]
    semana_del_mes = determine_week_of_month(module_dates[0])

    resultados["semana_de_inicio_del_modulo"] = (
        f"El módulo comienza en la {etiqueta_semana[semana_del_mes-1]} semana del mes."
    )
    resultados["mes_del_modulo"] = (
        f"{months_es[module_dates[0].strftime('%B')]} del {module_dates[0].strftime('%Y')}"
    )
    resultados["fecha_fin_programa"] = format_date_spanish(
        evaluation_dates[-1][0] - timedelta(days=1)
    )

    for i, fecha_modulo in enumerate(module_dates, start=1):
        resultados["modulos"].append({f"modulo_{i}": format_date_spanish(fecha_modulo)})

    inicio_evaluacion, fin_evaluacion = evaluation_dates[-1]
    resultados["evaluacion_final-actividades_pendientes"] = {
        "inicio": format_date_spanish(inicio_evaluacion),
        "fin": format_date_spanish(fin_evaluacion),
    }

    inicio_rectificacion, fin_rectificacion = rectification_dates[-1]
    resultados["periodo_subsanacion"] = {
        "inicio": format_date_spanish(inicio_rectificacion),
        "fin": format_date_spanish(fin_rectificacion),
    }

    resultados["cierre_plataforma"] = {
        "fecha": format_date_spanish(platform_close_dates[-1])
    }

    return resultados
