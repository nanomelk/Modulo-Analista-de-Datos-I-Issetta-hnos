# 📊 Manual del Dataset de Inventario  
**Materia:** Estadística y Exploración de Datos I  
**Proyecto Integrador**

---

## 🎯 1. Objetivo del dataset

Este dataset fue diseñado para representar el comportamiento del inventario de una empresa, permitiendo analizar:

- Movimientos de stock (entradas y salidas)
- Niveles de inventario
- Relación con proveedores
- Comportamiento por categorías de productos

El objetivo es aplicar conceptos de estadística descriptiva, probabilidad e inferencia.

---

## 🧠 2. Unidad de análisis

👉 **Cada fila representa un producto en un día determinado**

Es decir, cada registro muestra cómo se movió el stock de un producto en una fecha específica.

---

## 📦 3. Descripción de las variables

### 🔑 id_producto
- **Tipo:** Numérica (discreta)
- **Descripción:** Identificador único de cada registro

---

### 📦 nombre_producto
- **Tipo:** Cualitativa (nominal)
- **Descripción:** Nombre del producto
- **Uso:** Permite identificar y agrupar productos

---

### 🏷️ categoria
- **Tipo:** Cualitativa (nominal)
- **Descripción:** Tipo de producto (Herramientas, Eléctrico, Hidráulico, etc.)
- **Uso:** Comparaciones entre grupos

---

### 📅 fecha
- **Tipo:** Temporal
- **Descripción:** Día en el que se registra el movimiento
- **Uso:** Análisis en el tiempo

---

### 📊 stock_inicial
- **Tipo:** Numérica
- **Descripción:** Cantidad disponible al inicio del día

---

### ➕ cantidad_ingresada
- **Tipo:** Numérica
- **Descripción:** Cantidad de productos que ingresan (compras/reposición)

---

### ➖ cantidad_egresada
- **Tipo:** Numérica
- **Descripción:** Cantidad de productos que salen (ventas/uso)

---

### 📦 stock_final
- **Tipo:** Numérica
- **Descripción:** Stock al final del día

📌 **Relación importante:**
