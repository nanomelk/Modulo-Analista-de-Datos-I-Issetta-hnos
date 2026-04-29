import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd


ARCHIVO_ENTRADA = "planilla_carga_mat_corr.xlsx"
ARCHIVO_SALIDA = "dataset_inventario_errores_1.csv"
N_REGISTROS = 500
MARGEN_ERROR = 0.05


def normalizar_texto(texto):
    texto = str(texto).strip().lower()
    normalizaciones_directas = {
        "precio_actual (u$s)": "precio_actual_usd",
        "sub-categoria": "sub_categoria",
        "unidad-medida": "unidad_medida",
        "grup_": "grup",
    }
    if texto in normalizaciones_directas:
        return normalizaciones_directas[texto]

    reemplazos = {
        " ": "_",
        "-": "_",
        "/": "_",
        "(": "",
        ")": "",
        "$": "usd",
        ".": "",
    }
    for origen, destino in reemplazos.items():
        texto = texto.replace(origen, destino)
    while "__" in texto:
        texto = texto.replace("__", "_")
    return texto.strip("_")


def limpiar_valor_texto(valor):
    if pd.isna(valor):
        return np.nan
    texto = str(valor).strip()
    return texto if texto else np.nan


def limpiar_numero(valor):
    if pd.isna(valor):
        return np.nan
    texto = str(valor).strip()
    if not texto:
        return np.nan

    texto = texto.replace("USD", "").replace("usd", "").strip()
    texto = texto.replace("$", "").replace("u$s", "").strip()
    texto = texto.replace(" ", "")

    if "," in texto and "." in texto:
        texto = texto.replace(".", "").replace(",", ".")
    elif "," in texto:
        texto = texto.replace(",", ".")

    try:
        return float(texto)
    except ValueError:
        return np.nan


def cargar_base_productos():
    df_raw = pd.read_excel(ARCHIVO_ENTRADA, header=1)
    df_raw.columns = [normalizar_texto(col) for col in df_raw.columns]

    df = df_raw.copy()
    for columna in df.columns:
        df[columna] = df[columna].apply(limpiar_valor_texto)

    columnas_numericas = ["precio_actual_usd", "almacen", "cantidad"]
    for columna in columnas_numericas:
        if columna in df.columns:
            df[columna] = df[columna].apply(limpiar_numero)

    # La columna [0] / "id" se usa como nombre principal del producto.
    if "id" in df.columns:
        df["nombre_producto"] = df["id"]
    else:
        df["nombre_producto"] = df.iloc[:, 0]

    df = df[df["nombre_producto"].notna()].copy()
    df = df[df["nombre_producto"].astype(str).str.strip() != ""].copy()

    # Evita usar filas de agrupación como productos reales.
    if "codigo" in df.columns:
        df = df[df["codigo"].notna()].copy()

    df.reset_index(drop=True, inplace=True)
    return df


def completar_categorias(base_productos):
    categorias_base = [
        "mecanica",
        "electrico",
        "hidraulico",
        "herramientas",
        "seguridad",
        "ferreteria",
    ]

    categorias_validas = set(
        base_productos["categoria"].dropna().astype(str).str.strip().str.lower()
    )
    categorias_validas.update(categorias_base)
    return sorted(categorias_validas)


def calcular_precio_unitario(precio_base):
    if pd.notna(precio_base) and precio_base > 0:
        variacion = np.random.uniform(0.9, 1.15)
        return round(precio_base * variacion, 2)

    precio_generado = np.random.lognormal(mean=2.8, sigma=0.7)
    return round(precio_generado, 2)


def generar_dataset(base_productos):
    categorias_validas = completar_categorias(base_productos)
    proveedores = ["Proveedor A", "Proveedor B", "Proveedor C", "Proveedor D"]
    fecha_inicio = datetime(2025, 1, 1)
    data = []

    for i in range(N_REGISTROS):
        base = base_productos.sample(n=1).iloc[0]
        registro = base.to_dict()

        fecha = fecha_inicio + timedelta(days=random.randint(0, 180))
        stock_inicial = max(0, int(np.random.normal(loc=60, scale=25)))
        cantidad_ingresada = max(0, int(np.random.normal(loc=18, scale=9)))
        cantidad_egresada = max(0, int(np.random.normal(loc=15, scale=8)))
        stock_final = max(0, stock_inicial + cantidad_ingresada - cantidad_egresada)
        stock_minimo = max(1, int(np.random.normal(loc=20, scale=8)))
        tiempo_reposicion = max(1, int(np.random.normal(loc=7, scale=3)))

        precio_unitario = calcular_precio_unitario(registro.get("precio_actual_usd"))
        costo_logistica = round(precio_unitario * np.random.uniform(0.03, 0.12), 2)
        costo_almacenamiento = round(precio_unitario * np.random.uniform(0.01, 0.06), 2)
        costo_administrativo = round(precio_unitario * np.random.uniform(0.01, 0.04), 2)
        costo_indirecto_total = round(
            costo_logistica + costo_almacenamiento + costo_administrativo, 2
        )
        costo_total_unitario = round(precio_unitario + costo_indirecto_total, 2)
        valor_stock_final = round(stock_final * costo_total_unitario, 2)

        categoria = registro.get("categoria")
        if pd.isna(categoria) or not str(categoria).strip():
            categoria = random.choice(categorias_validas)

        if stock_final <= stock_minimo:
            estado = "critico"
        elif stock_final <= stock_minimo * 1.5:
            estado = "bajo"
        else:
            estado = "ok"

        registro.update(
            {
                "id_producto": i,
                "nombre_producto": registro.get("nombre_producto"),
                "categoria": categoria,
                "fecha": fecha,
                "stock_inicial": stock_inicial,
                "cantidad_ingresada": cantidad_ingresada,
                "cantidad_egresada": cantidad_egresada,
                "stock_final": stock_final,
                "stock_minimo": stock_minimo,
                "proveedor": random.choice(proveedores),
                "tiempo_reposicion_dias": tiempo_reposicion,
                "estado_stock": estado,
                "precio_unitario_usd": precio_unitario,
                "costo_logistica_usd": costo_logistica,
                "costo_almacenamiento_usd": costo_almacenamiento,
                "costo_administrativo_usd": costo_administrativo,
                "costo_indirecto_total_usd": costo_indirecto_total,
                "costo_total_unitario_usd": costo_total_unitario,
                "valor_stock_final_usd": valor_stock_final,
            }
        )

        data.append(registro)

    return pd.DataFrame(data)


def agregar_errores(df):
    n_errores = int(len(df) * MARGEN_ERROR)
    filas_con_error = np.random.choice(df.index, size=n_errores, replace=False)

    tipos_error = (
        ["nulo"] * (n_errores // 3)
        + ["outlier"] * (n_errores // 3)
        + ["inconsistencia"] * (n_errores - 2 * (n_errores // 3))
    )
    random.shuffle(tipos_error)

    columnas_nulas = [
        "nombre_producto",
        "categoria",
        "stock_inicial",
        "cantidad_ingresada",
        "cantidad_egresada",
        "stock_final",
        "stock_minimo",
        "proveedor",
        "tiempo_reposicion_dias",
        "precio_unitario_usd",
        "costo_logistica_usd",
        "costo_indirecto_total_usd",
        "estado_stock",
    ]

    columnas_outliers = [
        "stock_inicial",
        "cantidad_ingresada",
        "cantidad_egresada",
        "stock_final",
        "stock_minimo",
        "tiempo_reposicion_dias",
        "precio_unitario_usd",
        "costo_logistica_usd",
        "costo_indirecto_total_usd",
        "valor_stock_final_usd",
    ]

    for fila, tipo_error in zip(filas_con_error, tipos_error):
        if tipo_error == "nulo":
            columna = random.choice(columnas_nulas)
            if columna in df.columns:
                df.loc[fila, columna] = np.nan

        elif tipo_error == "outlier":
            columna = random.choice(columnas_outliers)
            if columna in df.columns:
                df.loc[fila, columna] = random.choice(
                    [np.random.randint(1000, 5000), np.random.randint(-500, -1)]
                )

        else:
            error = random.choice(
                ["fecha_futura", "categoria_invalida", "estado_invalido"]
            )
            if error == "fecha_futura":
                df.loc[fila, "fecha"] = datetime(2035, 1, 1)
            elif error == "categoria_invalida":
                df.loc[fila, "categoria"] = "categoria_desconocida"
            else:
                df.loc[fila, "estado_stock"] = "error"

    return df, n_errores


def guardar_csv(df, ruta_salida):
    try:
        df.to_csv(ruta_salida, index=False)
        return ruta_salida
    except PermissionError:
        ruta = Path(ruta_salida)
        ruta_alternativa = (
            f"{ruta.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ruta.suffix}"
        )
        df.to_csv(ruta_alternativa, index=False)
        return ruta_alternativa


base_productos = cargar_base_productos()
df = generar_dataset(base_productos)
df, n_errores = agregar_errores(df)
archivo_generado = guardar_csv(df, ARCHIVO_SALIDA)

print("Dataset generado correctamente")
print("Archivo de entrada:", ARCHIVO_ENTRADA)
print("Archivo de salida:", archivo_generado)
print("Filas base leidas:", len(base_productos))
print("Filas generadas:", len(df))
print("Filas con errores simulados:", n_errores)
