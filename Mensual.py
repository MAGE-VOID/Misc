import pandas as pd

# Datos iniciales
ingreso_mensual_total = 4500
gastos_diciembre = 890
gastos_enero_febrero = 0
gastos_marzo_en_adelante = 1390
gastos_mensuales = 1500
deuda = 8250

# Cálculos iniciales de sobrantes
sobrante_diciembre = ingreso_mensual_total - (gastos_mensuales + gastos_diciembre)
sobrante_enero_febrero = ingreso_mensual_total - gastos_mensuales
sobrante_marzo_en_adelante = ingreso_mensual_total - (gastos_mensuales + gastos_marzo_en_adelante)

# Crear detalle mensual inicial
deuda_restante = deuda
ahorro_acumulado = 0
meses_detalle = []

# Diciembre
deuda_inicial_mes = deuda_restante
pago_aplicado = min(sobrante_diciembre, deuda_restante)
deuda_restante -= pago_aplicado
ahorro_mensual = sobrante_diciembre - pago_aplicado
ahorro_acumulado += ahorro_mensual

meses_detalle.append({
    "Mes": "Diciembre",
    "Ingreso": ingreso_mensual_total,
    "Gastos Universidades": gastos_diciembre,
    "Otros Gastos": gastos_mensuales,
    "Deuda Inicial Mes": deuda_inicial_mes,
    "Pago Aplicado": pago_aplicado,
    "Deuda Restante": deuda_restante,
    "Ahorro Mensual": ahorro_mensual,
    "Ahorro Acumulado": ahorro_acumulado
})

# Generar datos para enero a diciembre
meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", 
         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

for mes_actual in meses:
    deuda_inicial_mes = deuda_restante
    if mes_actual in ["Enero", "Febrero"]:
        sobrante_actual = sobrante_enero_febrero
        gastos_actuales = gastos_enero_febrero
    else:
        sobrante_actual = sobrante_marzo_en_adelante
        gastos_actuales = gastos_marzo_en_adelante
    
    pago_aplicado = min(sobrante_actual, deuda_restante)
    deuda_restante -= pago_aplicado
    ahorro_mensual = sobrante_actual - pago_aplicado
    ahorro_acumulado += ahorro_mensual

    meses_detalle.append({
        "Mes": mes_actual,
        "Ingreso": ingreso_mensual_total,
        "Gastos Universidades": gastos_actuales,
        "Otros Gastos": gastos_mensuales,
        "Deuda Inicial Mes": deuda_inicial_mes,
        "Pago Aplicado": pago_aplicado,
        "Deuda Restante": deuda_restante,
        "Ahorro Mensual": ahorro_mensual,
        "Ahorro Acumulado": ahorro_acumulado
    })

# Convertir a DataFrame
detalle_pagos_df = pd.DataFrame(meses_detalle)

# Mostrar como DataFrame
print(detalle_pagos_df)
