import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# -----------------------------
# 1. Leer productos desde Excel
# -----------------------------
df_productos = pd.read_excel("productos.xlsx")
# Ajustá el nombre de la columna si hace falta
col_nombre = df_productos.columns[1]  # normalmente la 2da columna
productos = df_productos[col_nombre].dropna().unique()

# Categorías ficticias
categorias = ["Mecanica", "Electrico", "Hidraulico", "Herramientas"]

# Proveedores
proveedores = ["Proveedor A", "Proveedor B", "Proveedor C"]

# -----------------------------
# 2. Generar dataset
# -----------------------------
n_registros = 500  # podés subirlo si querés

data = []

fecha_inicio = datetime(2025, 1, 1)

for i in range(n_registros):
    
    producto = random.choice(productos)
    categoria = random.choice(categorias)
    proveedor = random.choice(proveedores)
    
    fecha = fecha_inicio + timedelta(days=random.randint(0, 180))
    
    stock_inicial = np.random.randint(20, 200)
    
    # Simulación tipo distribución
    cantidad_egresada = max(0, int(np.random.normal(loc=20, scale=10)))
    cantidad_ingresada = max(0, int(np.random.normal(loc=15, scale=8)))
    
    stock_final = stock_inicial + cantidad_ingresada - cantidad_egresada
    
    stock_minimo = np.random.randint(10, 50)
    
    tiempo_reposicion = np.random.randint(1, 15)
    
    # Estado de stock
    if stock_final <= stock_minimo:
        estado = "critico"
    elif stock_final <= stock_minimo * 1.5:
        estado = "bajo"
    else:
        estado = "ok"
    
    data.append([
        i,
        producto,
        categoria,
        fecha,
        stock_inicial,
        cantidad_ingresada,
        cantidad_egresada,
        stock_final,
        stock_minimo,
        proveedor,
        tiempo_reposicion,
        estado
    ])

# -----------------------------
# 3. Crear DataFrame
# -----------------------------
df = pd.DataFrame(data, columns=[
    "id_producto",
    "nombre_producto",
    "categoria",
    "fecha",
    "stock_inicial",
    "cantidad_ingresada",
    "cantidad_egresada",
    "stock_final",
    "stock_minimo",
    "proveedor",
    "tiempo_reposicion_dias",
    "estado_stock"
])

# -----------------------------
# 4. Guardar CSV
# -----------------------------
df.to_csv("dataset_inventario.csv", index=False)

print("Dataset generado correctamente 🚀")

print("Script ejecutado correctamente")
print("Filas generadas:", len(df))