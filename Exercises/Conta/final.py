#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Genera un archivo Excel profesional con los estados financieros de ANTARES S.A.C. 2014:
  - Hoja "Situación Financiera" (Balance)
  - Hoja "Resultados Integrales" (Estado de Resultados)
Incluye:
  • Verificación automática de subtotales y totales
  • Formato de contabilidad y bordes
  • Alturas de fila para mejor espaciado
  • Orientación horizontal y ajuste a una página
  • Pie con “Elaboración: Propia” y “Fuente”
Requisitos:
    pip install pandas XlsxWriter
"""

import pandas as pd
import os
import sys

def verify_totals(df, section_col, concept_col, value_col):
    errors = []
    expected = {
        "Activo Corriente":    "Total Activo Corriente",
        "Activo No Corriente": "Total Activo No Corriente",
        "Pasivo Corriente":    "Total Pasivo Corriente",
        "Pasivo No Corriente": "Total Pasivo No Corriente",
        "Patrimonio":          "Total Patrimonio"
    }
    for sec, total_name in expected.items():
        subset = df[df[section_col] == sec]
        items_sum = subset[~subset[concept_col].str.lower().str.startswith("total")][value_col].sum()
        manual = subset[subset[concept_col] == total_name][value_col]
        if manual.empty:
            errors.append(f"No se encontró fila '{total_name}'")
        else:
            diff = items_sum - manual.iloc[0]
            if abs(diff) > 0.01:
                errors.append(f"'{total_name}' difiere: manual {manual.iloc[0]:,.2f} vs suma {items_sum:,.2f}")
    return errors

def write_sheet_balance(wb, ws, df, title_lines, footnote):
    fmt_title    = wb.add_format({'bold': True, 'align': 'center', 'font_size': 14})
    fmt_subtitle = wb.add_format({'bold': True, 'align': 'center', 'font_size': 12})
    fmt_header   = wb.add_format({'bold': True, 'align': 'center', 'bg_color': '#D9E1F2', 'border': 1})
    fmt_section  = wb.add_format({'bold': True, 'align': 'left', 'bg_color': '#4F81BD',
                                  'font_color': 'white', 'border': 1})
    fmt_label    = wb.add_format({'align': 'left', 'border': 1})
    fmt_number   = wb.add_format({'num_format': '#,##0.00;(#,##0.00)', 'align': 'right', 'border': 1})
    fmt_footnote = wb.add_format({'italic': True, 'align': 'left'})

    # Títulos
    ncols = 2  # usaremos columnas B y C para datos
    for i, line in enumerate(title_lines):
        ws.merge_range(i, 0, i, ncols, line, fmt_title if i == 0 else fmt_subtitle)
        ws.set_row(i, 20)
    start = len(title_lines) + 1

    # Encabezados
    headers = ["", "Descripción", "Valor (S/.)"]
    for col, h in enumerate(headers):
        ws.write(start, col, h, fmt_header)
    ws.set_row(start, 18)

    ws.freeze_panes(start+1, 0)
    ws.set_landscape()
    ws.set_paper(9)
    ws.fit_to_pages(1, 0)

    # Filas
    row = start + 1
    current = None
    for _, r in df.iterrows():
        sec, sub, concept, val = r
        if sec != current:
            row += 1
            ws.merge_range(row, 0, row, ncols, sec, fmt_section)
            ws.set_row(row, 16)
            row += 1
            current = sec
        display = f"    {concept}" if sub else concept
        ws.write(row, 1, display, fmt_label)
        ws.write_number(row, 2, val, fmt_number)
        row += 1

    ws.write(row+1, 0, footnote, fmt_footnote)
    ws.set_column('A:A', 2)
    ws.set_column('B:B', 45)
    ws.set_column('C:C', 18)

def write_sheet_results(wb, ws, df, title_lines, footnote):
    fmt_title    = wb.add_format({'bold': True, 'align': 'center', 'font_size': 14})
    fmt_subtitle = wb.add_format({'bold': True, 'align': 'center', 'font_size': 12})
    fmt_header   = wb.add_format({'bold': True, 'align': 'center', 'bg_color': '#E2EFDA', 'border': 1})
    fmt_label    = wb.add_format({'align': 'left', 'border': 1})
    fmt_number   = wb.add_format({'num_format': '#,##0.00;(#,##0.00)', 'align': 'right', 'border': 1})
    fmt_footnote = wb.add_format({'italic': True})

    # Títulos
    ncols = 2
    for i, line in enumerate(title_lines):
        ws.merge_range(i, 0, i, ncols, line, fmt_title if i == 0 else fmt_subtitle)
        ws.set_row(i, 20)
    start = len(title_lines) + 1

    # Encabezados
    headers = ["", "Descripción", "Valor (S/.)"]
    for col, h in enumerate(headers):
        ws.write(start, col, h, fmt_header)
    ws.set_row(start, 18)

    ws.freeze_panes(start+1, 0)
    ws.set_landscape()
    ws.set_paper(9)
    ws.fit_to_pages(1, 0)

    # Filas
    row = start + 1
    for _, r in df.iterrows():
        sub, concept, val = r
        display = f"    {concept}" if sub else concept
        ws.write(row, 1, display, fmt_label)
        ws.write_number(row, 2, val, fmt_number)
        row += 1

    ws.write(row+1, 0, footnote, fmt_footnote)
    ws.set_column('A:A', 2)
    ws.set_column('B:B', 45)
    ws.set_column('C:C', 18)

def main():
    # Datos base (sin totales manuales)
    items = [
        ("Activo Corriente", "", "Efectivo y equivalentes de efectivo", 65347.00),
        ("Activo Corriente", "", "Cuentas por cobrar comerciales - terceros", 6120.00),
        ("Activo Corriente", "", "Servicios y otros contratos por anticipado", 2843.95),
        ("Activo Corriente", "", "Materiales auxiliares y suministros", 2595.00),
        ("Activo No Corriente", "", "Inmuebles, maquinaria y equipo", 1544238.56),
        ("Activo No Corriente", "", "Depreciación acumulada", -565981.27),
        ("Pasivo Corriente", "", "Tributos por pagar", 23680.00),
        ("Pasivo Corriente", "", "Remuneraciones y participaciones por pagar", 13850.39),
        ("Pasivo Corriente", "", "Cuentas por pagar comerciales - terceros", 2940.20),
        ("Pasivo Corriente", "", "Obligaciones financieras", 41454.93),
        ("Pasivo No Corriente", "", "Obligaciones financieras", 102497.31),
        ("Patrimonio", "", "Capital", 777307.00),
        ("Patrimonio", "", "Reserva legal acumulada", 44222.10),
        ("Patrimonio", "", "Resultados acumulados", 49211.31),
    ]
    df_items = pd.DataFrame(items, columns=["Sección","Subsección","Concepto","Valor"])

    # Generar subtotales y totales automáticos
    totals = []
    for sec in df_items["Sección"].unique():
        subtotal = df_items[df_items["Sección"] == sec]["Valor"].sum()
        totals.append((sec, "", f"Total {sec}", subtotal))
    active_sum = df_items[df_items["Sección"].isin(["Activo Corriente","Activo No Corriente"])]["Valor"].sum()
    liab_sum   = df_items[df_items["Sección"].isin(["Pasivo Corriente","Pasivo No Corriente","Patrimonio"])]["Valor"].sum()
    totals.append(("Totales","", "Total Activo", active_sum))
    totals.append(("Totales","", "Total Pasivo y Patrimonio", liab_sum))

    balance_df = pd.concat([df_items, pd.DataFrame(totals, columns=df_items.columns)], ignore_index=True)

    # Verificar subtotales
    errs = verify_totals(balance_df, "Sección", "Concepto", "Valor")
    if errs:
        print("Errores en subtotales:\n" + "\n".join(errs))
        sys.exit(1)

    # Resultados Integrales
    base = [
        ("Ingresos", "Ventas Netas", 730847.48),
        ("Costo",    "Costo de Servicios", -412532.41),
    ]
    # Cálculos
    gross = sum(x[2] for x in base)
    op    = gross - 212772.09 - 278.40
    prefi = op - 23040.18
    part  = prefi * 0.05
    antes  = prefi - part
    imp   = antes * 0.30
    neto  = antes - imp

    result_rows = base + [
        ("", "Utilidad Bruta", gross),
        ("Gastos", "Gastos de Administración", -212772.09),
        ("Gastos", "Gastos de Ventas", -278.40),
        ("", "Utilidad Operativa", op),
        ("", "Gastos Financieros", -23040.18),
        ("", "Resultado Antes de Participaciones e Impuestos", prefi),
        ("", "Participación Trabajadores (5%)", -part),
        ("", "Utilidad Antes de Impuestos", antes),
        ("", "Impuesto a la Renta (30%)", -imp),
        ("", "Utilidad Neta del Ejercicio", neto),
    ]
    results_df = pd.DataFrame(result_rows, columns=["Subsección","Concepto","Valor"])

    # Ruta de salida
    out = r"D:\FOREX\MT5_1\MQL5\Experts\Projects\Sharing-Projects\Misc\Exercises\Conta\ANTARES_2014_profesional.xlsx"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    try:
        writer = pd.ExcelWriter(out, engine="xlsxwriter")
    except ImportError:
        print("Instala XlsxWriter: pip install XlsxWriter")
        sys.exit(1)
    wb = writer.book

    # Hoja Balance
    ws1 = wb.add_worksheet("Situación Financiera")
    writer.sheets["Situación Financiera"] = ws1
    write_sheet_balance(
        wb, ws1, balance_df[["Sección","Subsección","Concepto","Valor"]],
        [
            "ANTARES S.A.C.",
            "ESTADO DE SITUACIÓN FINANCIERA",
            "(Expresado en Nuevos Soles)",
            "Al 31 de diciembre de 2014"
        ],
        "Fuente: ANTARES S.A.C.   •   Elaboración: Propia"
    )

    # Hoja Resultados
    ws2 = wb.add_worksheet("Resultados Integrales")
    writer.sheets["Resultados Integrales"] = ws2
    write_sheet_results(
        wb, ws2, results_df,
        [
            "ANTARES S.A.C.",
            "ESTADO DE RESULTADOS INTEGRALES",
            "(Expresado en Nuevos Soles)",
            "Al 31 de diciembre de 2014"
        ],
        "Fuente: ANTARES S.A.C.   •   Elaboración: Propia"
    )

    writer.close()
    print(f"Excel profesional generado en: {out}")

if __name__ == "__main__":
    main()
