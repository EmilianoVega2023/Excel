import pandas as pd
import random
from datetime import datetime, timedelta

# Generar fechas aleatorias
def generar_fechas(inicio, fin, n):
    inicio = datetime.strptime(inicio, "%Y-%m-%d")
    fin = datetime.strptime(fin, "%Y-%m-%d")
    fechas = [inicio + timedelta(days=random.randint(0, (fin - inicio).days)) for _ in range(n)]
    return sorted(fechas)

# Productos ficticios
productos = [
    {"Producto": "Hamburguesa", "Categoría": "Comida", "Costo": 1200, "Precio": 2500},
    {"Producto": "Pizza", "Categoría": "Comida", "Costo": 1500, "Precio": 3000},
    {"Producto": "Cerveza", "Categoría": "Bebida", "Costo": 500, "Precio": 1300},
    {"Producto": "Coca-Cola", "Categoría": "Bebida", "Costo": 350, "Precio": 900},
    {"Producto": "Papas", "Categoría": "Comida", "Costo": 800, "Precio": 1800},
]

# Generar dataset
fechas = generar_fechas("2025-01-01", "2025-04-30", 300)
data = []

for fecha in fechas:
    item = random.choice(productos)
    cantidad = random.randint(1, 5)
    data.append({
        "Fecha": fecha,
        "Producto": item["Producto"],
        "Categoría": item["Categoría"],
        "Cantidad": cantidad,
        "Precio unitario": item["Precio"],
        "Costo unitario": item["Costo"],
        "Total venta": cantidad * item["Precio"],
        "Total costo": cantidad * item["Costo"]
    })

df = pd.DataFrame(data)

# Guardar archivo Excel
file_path = "./rentabilidad.xlsx"
df.to_excel(file_path, index=False)

file_path
