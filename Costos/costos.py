import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import numpy as np

# Cargar los datos desde el archivo Excel
df = pd.read_excel("../rentabilidad.xlsx")

# Convertir la columna Fecha a tipo datetime si no lo está ya
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Añadir columnas para análisis
df['Mes'] = df['Fecha'].dt.month_name()
df['Semana'] = df['Fecha'].dt.isocalendar().week
df['Ganancia'] = df['Total venta'] - df['Total costo']
df['Margen'] = (df['Ganancia'] / df['Total venta']) * 100

# 1. Análisis por proveedor
print("="*50)
print("ANÁLISIS POR PROVEEDOR")
print("="*50)

analisis_proveedor = df.groupby('Proveedor').agg({
    'Total venta': 'sum',
    'Total costo': 'sum',
    'Cantidad': 'sum'
}).reset_index()

analisis_proveedor['Ganancia'] = analisis_proveedor['Total venta'] - analisis_proveedor['Total costo']
analisis_proveedor['Margen (%)'] = (analisis_proveedor['Ganancia'] / analisis_proveedor['Total venta']) * 100

print(analisis_proveedor)

# 2. Análisis por categoría
print("\n" + "="*50)
print("ANÁLISIS POR CATEGORÍA")
print("="*50)

analisis_categoria = df.groupby('Categoría').agg({
    'Total venta': 'sum',
    'Total costo': 'sum',
    'Cantidad': 'sum'
}).reset_index()

analisis_categoria['Ganancia'] = analisis_categoria['Total venta'] - analisis_categoria['Total costo']
analisis_categoria['Margen (%)'] = (analisis_categoria['Ganancia'] / analisis_categoria['Total venta']) * 100

print(analisis_categoria)

# 3. Análisis de variación de costos por producto
print("\n" + "="*50)
print("VARIACIÓN DE COSTOS POR PRODUCTO")
print("="*50)

# Agrupar por producto y fecha (por semana para ver tendencia)
costo_semanal = df.groupby(['Producto', 'Semana'])['Costo unitario'].mean().reset_index()

# Para cada producto, calcular la variación
for producto in df['Producto'].unique():
    costos_producto = costo_semanal[costo_semanal['Producto'] == producto]
    if len(costos_producto) > 1:
        costo_inicial = costos_producto['Costo unitario'].iloc[0]
        costo_final = costos_producto['Costo unitario'].iloc[-1]
        variacion = ((costo_final - costo_inicial) / costo_inicial) * 100
        print(f"{producto}: Variación del costo: {variacion:.2f}%")
        
        # Calcular variaciones semanales
        costos_producto['Variación'] = costos_producto['Costo unitario'].pct_change() * 100
        promedio_variacion = costos_producto['Variación'].mean()
        print(f"   Variación promedio semanal: {promedio_variacion:.2f}%")

# 4. Visualizar tendencias
plt.figure(figsize=(12, 8))

# Gráfico de tendencia de costos por producto
plt.subplot(2, 1, 1)
for producto in df['Producto'].unique():
    datos = costo_semanal[costo_semanal['Producto'] == producto]
    plt.plot(datos['Semana'], datos['Costo unitario'], marker='o', label=producto)

plt.title('Tendencia de Costos Unitarios por Semana')
plt.xlabel('Semana del año')
plt.ylabel('Costo Unitario Promedio')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()

# Gráfico de rentabilidad por proveedor
plt.subplot(2, 1, 2)
sns.barplot(x='Proveedor', y='Margen (%)', data=analisis_proveedor)
plt.title('Margen de Rentabilidad por Proveedor')
plt.xlabel('Proveedor')
plt.ylabel('Margen (%)')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('analisis_rentabilidad.png')
plt.close()

# 5. Generar informe detallado por proveedor en un archivo CSV
resultados = []

for proveedor in df['Proveedor'].unique():
    datos_proveedor = df[df['Proveedor'] == proveedor]
    
    # Análisis por producto para este proveedor
    for producto in datos_proveedor['Producto'].unique():
        datos_producto = datos_proveedor[datos_proveedor['Producto'] == producto]
        
        # Calcular estadísticas
        cantidad_total = datos_producto['Cantidad'].sum()
        venta_total = datos_producto['Total venta'].sum()
        costo_total = datos_producto['Total costo'].sum()
        ganancia = venta_total - costo_total
        margen = (ganancia / venta_total) * 100 if venta_total > 0 else 0
        
        # Calcular tendencia de costos (primer y último registro)
        if len(datos_producto) > 1:
            primer_costo = datos_producto.sort_values('Fecha')['Costo unitario'].iloc[0]
            ultimo_costo = datos_producto.sort_values('Fecha')['Costo unitario'].iloc[-1]
            variacion_costo = ((ultimo_costo - primer_costo) / primer_costo) * 100
        else:
            variacion_costo = 0
        
        resultados.append({
            'Proveedor': proveedor,
            'Producto': producto,
            'Cantidad Total': cantidad_total,
            'Venta Total': venta_total,
            'Costo Total': costo_total,
            'Ganancia': ganancia,
            'Margen (%)': margen,
            'Variación Costo (%)': variacion_costo
        })

# Crear y guardar el informe detallado
informe_df = pd.DataFrame(resultados)
informe_df.to_csv('analisis_por_proveedor.csv', index=False)

print("\n" + "="*50)
print("Análisis completado. Se han generado los siguientes archivos:")
print("1. analisis_rentabilidad.png - Gráficos de tendencias")
print("2. analisis_por_proveedor.csv - Informe detallado por proveedor")
print("="*50)