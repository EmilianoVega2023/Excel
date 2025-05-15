import pandas as pd
from datetime import datetime

# Cargar archivo
df = pd.read_excel("./prueba.xlsx")

# Convertir a datetime
df["Hora Entrada"] = pd.to_datetime(df["Hora Entrada"].astype(str))
df["Hora Salida"] = pd.to_datetime(df["Hora Salida"].astype(str))

# Calcular horas trabajadas
df["Horas trabajadas"] = (df["Hora Salida"] - df["Hora Entrada"]).dt.total_seconds() / 3600

# Calcular pago
df["Pago del día"] = df["Horas trabajadas"] * df["Tarifa por hora"]

# Agrupar por empleado
resumen = df.groupby("Empleado").agg({
    "Horas trabajadas": "sum",
    "Pago del día": "sum"
}).round(2)

# Mostrar resultados
print("🧾 Resumen por empleado:\n")
print(resumen)

# Guardar resumen
resumen.to_excel("resumen_semanal.xlsx")
