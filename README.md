# 📅 GestionReservas

**GestionReservas** es una aplicación de escritorio desarrollada en **Python** que permite administrar reservas de manera eficiente mediante una interfaz gráfica moderna creada con **Tkinter** y una base de datos **PostgreSQL**.

Este proyecto está orientado a demostrar habilidades prácticas en desarrollo de software, incluyendo CRUD, manejo de bases de datos, validaciones y diseño de interfaces gráficas.

---

## 🚀 Funcionalidades

- ➕ Crear reservas
- 📋 Listar reservas registradas
- ✏️ Actualizar reservas existentes
- ❌ Eliminar reservas
- 🖱️ Selección interactiva desde tabla
- ✅ Validación de campos obligatorios
- 📆 Validación de formato de fecha (YYYY-MM-DD)
- 🎨 Interfaz gráfica clara y profesional

---

## 🧰 Tecnologías utilizadas

| Tecnología | Descripción |
|----------|------------|
| Python 3 | Lenguaje principal |
| Tkinter / ttk | Interfaz gráfica |
| PostgreSQL | Base de datos relacional |
| psycopg2 | Conector PostgreSQL |
| datetime | Manejo y validación de fechas |

---

## 🗄️ Estructura de la base de datos

Tabla principal: `reservas`

```sql
CREATE TABLE reservas (
    id SERIAL PRIMARY KEY,
    cliente VARCHAR(100) NOT NULL,
    fecha DATE NOT NULL,
    servicio VARCHAR(100) NOT NULL,
    estado VARCHAR(20) NOT NULL
);
