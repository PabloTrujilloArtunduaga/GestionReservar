import tkinter as tk
from tkinter import ttk
import psycopg2
from tkinter import messagebox
from datetime import datetime

# -----------------------------------------------
#   Funciones para Gestión de Reservas (sin cambios)
# -----------------------------------------------

def mostrar_datos():
    for item in tree.get_children():
        tree.delete(item)
    try:
        with conexion() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, cliente, fecha, servicio, estado FROM reservas ORDER BY id ASC")
                filas = cur.fetchall()
                for i, fila in enumerate(filas):
                    tag = 'evenrow' if i % 2 == 0 else 'oddrow'
                    tree.insert("", tk.END, values=fila, tags=(tag,))
    except Exception as e:
        messagebox.showerror("Error", e)

def seleccionar_item(event):
    seleccion = tree.focus()
    if seleccion:
        valores = tree.item(seleccion, "values")
        entry_cliente.delete(0, tk.END)
        entry_fecha.delete(0, tk.END)
        combo_estado.set("")
        entry_servicio.delete(0, tk.END)

        entry_cliente.insert(0, valores[1])
        entry_fecha.insert(0, valores[2])
        combo_estado.set(valores[4])
        entry_servicio.insert(0, valores[3])

# -----------------------------
# Conexion a la base de datos
# -----------------------------
def conexion():
    return psycopg2.connect(
        host="localhost",
        dbname="Name",
        user="postgres",
        password="password",
        port=5432
    )

# -----------------------------
# Crear tabla
# -----------------------------
def crear_tabla():
    try:
        with conexion() as conn:
            with conn.cursor() as cur:
                cur.execute("DROP TABLE IF EXISTS reservas;")
                cur.execute("""
                    CREATE TABLE reservas (
                        id SERIAL PRIMARY KEY,
                        cliente VARCHAR(100) NOT NULL,
                        fecha DATE NOT NULL,
                        servicio VARCHAR(100) NOT NULL,
                        estado VARCHAR(20) NOT NULL
                    );
                """)
                conn.commit()
        messagebox.showinfo("Tabla creada", "Tabla 'reservas' creada correctamente.")
    except Exception as error:
        messagebox.showerror("Error", f"Error al crear la tabla:\n{error}")

# -----------------------------
# Insertar reserva
# -----------------------------
def agregar_reserva():
    if entry_cliente.get().strip() == "":
        messagebox.showwarning("Advertencia", "El campo Cliente está vacío")
        return
    if entry_fecha.get().strip() == "":
        messagebox.showwarning("Advertencia", "El campo Fecha está vacío")
        return
    if entry_servicio.get().strip() == "":
        messagebox.showwarning("Advertencia", "El campo Servicio está vacío")
        return
    if combo_estado.get().strip() == "":
        messagebox.showwarning("Advertencia", "Debe seleccionar un Estado")
        return

    try:
        fecha_str = entry_fecha.get().strip()
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Formato de fecha incorrecto (aaaa-mm-dd)")
        return

    try:
        with conexion() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO reservas (cliente, fecha, servicio, estado) VALUES (%s, %s, %s, %s)",
                    (entry_cliente.get(), fecha_str, entry_servicio.get(), combo_estado.get())
                )
                conn.commit()
        messagebox.showinfo("Éxito", "Reserva registrada correctamente.")
        mostrar_datos()
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Error: {e}")

# -----------------------------
# Borrar reserva
# -----------------------------
def borrar_reserva():
    seleccion = tree.focus()
    if not seleccion:
        messagebox.showwarning("Sin selección", "Debes seleccionar una reserva en la tabla.")
        return

    valores = tree.item(seleccion, "values")
    client_id = valores[0]
    try:
        with conexion() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM reservas WHERE id = %s", (client_id,))
                conn.commit()

        limpiar_campos()
        messagebox.showinfo("Éxito", "Reserva eliminada correctamente.")
        mostrar_datos()
    except psycopg2.Error as e:
        messagebox.showerror("Error en la BD", f"{e}")

# -----------------------------
# Actualizar reserva
# -----------------------------
def actualizar_reserva():
    if entry_cliente.get().strip() == "":
        messagebox.showwarning("Advertencia", "El campo Cliente está vacío")
        return
    if entry_fecha.get().strip() == "":
        messagebox.showwarning("Advertencia", "El campo Fecha está vacío")
        return
    if entry_servicio.get().strip() == "":
        messagebox.showwarning("Advertencia", "El campo Servicio está vacío")
        return
    if combo_estado.get().strip() == "":
        messagebox.showwarning("Advertencia", "Debe seleccionar un Estado")
        return

    seleccion = tree.focus()
    if not seleccion:
        messagebox.showwarning("Sin selección", "Debes seleccionar una reserva en la tabla.")
        return

    valores = tree.item(seleccion, "values")
    client_id = valores[0]

    try:
        fecha_str = entry_fecha.get().strip()
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Formato de fecha incorrecto (aaaa-mm-dd)")
        return

    try:
        with conexion() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE reservas SET cliente = %s, fecha = %s, servicio = %s, estado = %s WHERE id = %s",
                    (entry_cliente.get(), fecha_str, entry_servicio.get(), combo_estado.get(), client_id)
                )
                conn.commit()
        messagebox.showinfo("Éxito", "Reserva actualizada correctamente.")
        mostrar_datos()
    except psycopg2.Error as e:
        messagebox.showerror("Error", f"Error: {e}")

# -----------------------------
# Funcion limpiar campos
# -----------------------------
def limpiar_campos():
    entry_cliente.delete(0, tk.END)
    entry_fecha.delete(0, tk.END)
    entry_servicio.delete(0, tk.END)
    combo_estado.set("")

# -----------------------------
# DISEÑO / UI (mejorado, solo apariencia)
# -----------------------------

root = tk.Tk()
root.title("Reservas Pro — Gestión de Reservas")
root.geometry("1100x620")
root.configure(bg="#f6f8fa")
root.minsize(900, 520)

# Fuentes y paleta
FONT_TITLE = ("Segoe UI Semibold", 18)
FONT_SUB = ("Segoe UI", 10)
FONT_LABEL = ("Segoe UI", 11)
FONT_ENTRY = ("Segoe UI", 11)
FONT_BTN = ("Segoe UI", 10, "bold")

PRIMARY = "#2563eb"   # azul elegante
ACCENT = "#06b6d4"    # turquesa suave
BG = "#f6f8fa"
PANEL = "#ffffff"
TEXT = "#0f172a"
MUTED = "#64748b"

# Style ttk
style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview",
                background="#ffffff",
                foreground=TEXT,
                fieldbackground="#ffffff",
                rowheight=26,
                font=FONT_ENTRY)
style.configure("Treeview.Heading",
                background=PRIMARY,
                foreground="white",
                font=("Segoe UI Semibold", 11))
style.map("Treeview", background=[("selected", ACCENT)])

# Header
header = tk.Frame(root, bg=PANEL)
header.pack(fill="x", padx=14, pady=(14,6))

lbl_title = tk.Label(header, text="Reservas Pro", font=FONT_TITLE, bg=PANEL, fg=TEXT)
lbl_title.pack(side="left", padx=(12,6))

lbl_desc = tk.Label(header, text="— Administración de reservas", font=FONT_SUB, bg=PANEL, fg=MUTED)
lbl_desc.pack(side="left")

# Main content
content = tk.Frame(root, bg=BG)
content.pack(fill="both", expand=True, padx=14, pady=(0,14))

# Left panel (form)
left_panel = tk.Frame(content, bg=PANEL, bd=0, relief="flat")
left_panel.pack(side="left", fill="y", padx=(0,12), pady=8)

form_title = tk.Label(left_panel, text="Datos de la Reserva", font=("Segoe UI Semibold", 12), bg=PANEL, fg=TEXT)
form_title.pack(anchor="w", padx=12, pady=(12,6))

form = tk.Frame(left_panel, bg=PANEL)
form.pack(padx=12, pady=6)

tk.Label(form, text="Cliente", font=FONT_LABEL, bg=PANEL, fg=TEXT).grid(row=0, column=0, sticky="w", padx=6, pady=8)
entry_cliente = tk.Entry(form, font=FONT_ENTRY, width=30, bd=1, relief="solid")
entry_cliente.grid(row=0, column=1, padx=6, pady=8)

tk.Label(form, text="Fecha (aaaa-mm-dd)", font=FONT_LABEL, bg=PANEL, fg=TEXT).grid(row=1, column=0, sticky="w", padx=6, pady=8)
entry_fecha = tk.Entry(form, font=FONT_ENTRY, width=30, bd=1, relief="solid")
entry_fecha.grid(row=1, column=1, padx=6, pady=8)

tk.Label(form, text="Servicio", font=FONT_LABEL, bg=PANEL, fg=TEXT).grid(row=2, column=0, sticky="w", padx=6, pady=8)
entry_servicio = tk.Entry(form, font=FONT_ENTRY, width=30, bd=1, relief="solid")
entry_servicio.grid(row=2, column=1, padx=6, pady=8)

tk.Label(form, text="Estado", font=FONT_LABEL, bg=PANEL, fg=TEXT).grid(row=3, column=0, sticky="w", padx=6, pady=8)
combo_estado = ttk.Combobox(form, values=["Pendiente", "Confirmada", "Cancelada"], font=FONT_ENTRY, width=28, state="readonly")
combo_estado.grid(row=3, column=1, padx=6, pady=8)
combo_estado.set("Pendiente")

# Buttons block
btns = tk.Frame(left_panel, bg=PANEL)
btns.pack(padx=12, pady=(6,12), fill="x")

def make_btn(parent, text, cmd, color=PRIMARY):
    return tk.Button(parent, text=text, command=cmd, bg=color, fg="white", font=FONT_BTN, bd=0, relief="flat", cursor="hand2", padx=10, pady=8)

btn_add = make_btn(btns, "Agregar", agregar_reserva, color=ACCENT)
btn_add.grid(row=0, column=0, padx=6, pady=6, sticky="ew")
btn_update = make_btn(btns, "Actualizar", actualizar_reserva, color=PRIMARY)
btn_update.grid(row=0, column=1, padx=6, pady=6, sticky="ew")
btn_delete = make_btn(btns, "Eliminar", borrar_reserva, color="#ef4444")
btn_delete.grid(row=1, column=0, padx=6, pady=6, sticky="ew")
btn_clear = make_btn(btns, "Limpiar", limpiar_campos, color="#6b7280")
btn_clear.grid(row=1, column=1, padx=6, pady=6, sticky="ew")

# Right panel (table)
right_panel = tk.Frame(content, bg=PANEL, bd=0, relief="flat")
right_panel.pack(side="right", fill="both", expand=True, pady=8)

table_title = tk.Label(right_panel, text="Reservas", font=("Segoe UI Semibold", 12), bg=PANEL, fg=TEXT)
table_title.pack(anchor="w", padx=12, pady=(12,6))

# Table container with scrollbars
table_container = tk.Frame(right_panel, bg=PANEL)
table_container.pack(fill="both", expand=True, padx=12, pady=(0,12))

columns = ("ID", "Cliente", "Fecha", "Servicio", "Estado")
tree = ttk.Treeview(table_container, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.column("ID", width=60, anchor="center")
tree.column("Cliente", width=260, anchor="w")
tree.column("Fecha", width=120, anchor="center")
tree.column("Servicio", width=220, anchor="w")
tree.column("Estado", width=120, anchor="center")

# Scrollbars
vsb = ttk.Scrollbar(table_container, orient="vertical", command=tree.yview)
hsb = ttk.Scrollbar(table_container, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

tree.grid(row=0, column=0, sticky="nsew")
vsb.grid(row=0, column=1, sticky="ns")
hsb.grid(row=1, column=0, sticky="ew")
table_container.grid_rowconfigure(0, weight=1)
table_container.grid_columnconfigure(0, weight=1)

tree.tag_configure('evenrow', background='#ffffff')
tree.tag_configure('oddrow', background='#f5f9ff')
tree.bind("<<TreeviewSelect>>", seleccionar_item)

# Footer / status
status = tk.Label(root, text="Listo", bg=BG, fg=MUTED, anchor="w", font=("Segoe UI", 9))
status.pack(fill="x", side="bottom", ipady=6, padx=10)

# Inicializar datos
mostrar_datos()

root.mainloop()
