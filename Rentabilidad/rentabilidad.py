import pandas as pd

# Cargar el archivo subido
file_path = "./rentabilidad.xlsx"
df = pd.read_excel(file_path)

# Ver las primeras filas para entender la estructura
df.head()
# Calcular rentabilidad y margen
df["Rentabilidad"] = df["Total venta"] - df["Total costo"]
df["Margen (%)"] = round((df["Rentabilidad"] / df["Total venta"]) * 100, 2)

# Agrupar por producto
resumen_producto = df.groupby("Producto").agg(
    Total_ventas=("Total venta", "sum"),
    Total_costos=("Total costo", "sum"),
    Total_rentabilidad=("Rentabilidad", "sum"),
    Prom_margen_pct=("Margen (%)", "mean")
).reset_index()

# Agrupar por mes y categoría
df["Mes"] = df["Fecha"].dt.to_period("M")
resumen_mes_cat = df.groupby(["Mes", "Categoría"]).agg(
    Total_ventas=("Total venta", "sum"),
    Total_costos=("Total costo", "sum"),
    Rentabilidad=("Rentabilidad", "sum"),
    Prom_margen_pct=("Margen (%)", "mean")
).reset_index()

# Exportar a un nuevo Excel con resumen

with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Detalle", index=False)
    resumen_producto.to_excel(writer, sheet_name="Por producto", index=False)
    resumen_mes_cat.to_excel(writer, sheet_name="Por mes y categoría", index=False)

output_path = "./reporte_rentabilidad.xlsx"
