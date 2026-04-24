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
col_nombre = df_productos.columns[0]  # normalmente la 1da columna
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
# 4. Agregar margen de error
# -----------------------------
margen_error = 0.05
n_errores = int(len(df) * margen_error)

filas_con_error = np.random.choice(df.index, size=n_errores, replace=False)
tipos_error = (
    ["nulo"] * (n_errores // 3) +
    ["outlier"] * (n_errores // 3) +
    ["inconsistencia"] * (n_errores - 2 * (n_errores // 3))
)
random.shuffle(tipos_error)

for fila, tipo_error in zip(filas_con_error, tipos_error):
    if tipo_error == "nulo":
        columna = random.choice([
            "nombre_producto",
            "categoria",
            "stock_inicial",
            "cantidad_ingresada",
            "cantidad_egresada",
            "stock_final",
            "stock_minimo",
            "proveedor",
            "tiempo_reposicion_dias",
            "estado_stock"
        ])
        df.loc[fila, columna] = np.nan

    elif tipo_error == "outlier":
        columna = random.choice([
            "stock_inicial",
            "cantidad_ingresada",
            "cantidad_egresada",
            "stock_final",
            "stock_minimo",
            "tiempo_reposicion_dias"
        ])
        df.loc[fila, columna] = random.choice([
            np.random.randint(1000, 5000),
            np.random.randint(-500, -1)
        ])

    else:
        error = random.choice(["fecha_futura", "categoria_invalida", "estado_invalido"])

        if error == "fecha_futura":
            df.loc[fila, "fecha"] = datetime(2035, 1, 1)
        elif error == "categoria_invalida":
            df.loc[fila, "categoria"] = "Categoria desconocida"
        else:
            df.loc[fila, "estado_stock"] = "error"

# -----------------------------
# 5. Guardar CSV
# -----------------------------
df.to_csv("dataset_inventario_errores_1.csv", index=False)

print("Dataset generado correctamente")

print("Script ejecutado correctamente")
print("Filas generadas:", len(df))
print("Filas con errores simulados:", n_errores)
