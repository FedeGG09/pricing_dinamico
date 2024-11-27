import streamlit as st
import pandas as pd

# Configuración de la app
st.set_page_config(page_title="Formulario de Cotización", layout="wide")

# Inicializar el estado de la aplicación
if "current_step" not in st.session_state:
    st.session_state.current_step = 1

if "productos" not in st.session_state:
    st.session_state.productos = []

# Cargar clientes desde el CSV
try:
    clientes_csv_path = "Nombredecliente.csv"
    df_clientes = pd.read_csv(clientes_csv_path, encoding="latin1", header=None)
    lista_clientes = df_clientes[0].tolist()
except Exception as e:
    lista_clientes = []
    st.error(f"No se pudo cargar el archivo de clientes: {e}")

# Cargar productos desde el CSV
try:
    productos_csv_path = "PRODUCTOS_UNICOS.csv"
    df_productos_csv = pd.read_csv(productos_csv_path, encoding="latin1", header=None)
    lista_productos = df_productos_csv[0].tolist()
except Exception as e:
    lista_productos = []
    st.error(f"No se pudo cargar el archivo de productos: {e}")

# Lista de sucursales
sucursales = [
    "Bahía Blanca", "Buenos Aires", "Neuquén", "Comodoro Rivadavia",
    "Córdoba", "Mendoza", "Tucumán", "Rosario", "Panamericana", "Salta", "Mar Del Plata"
]

# Paso 1: Datos básicos
if st.session_state.current_step == 1:
    st.title("Formulario de Cotización - Paso 1: Datos Básicos")

    # Formulario para datos básicos
    with st.form("datos_basicos_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            fecha = st.date_input("Fecha")
        with col2:
            cliente = st.selectbox(
                "Cliente",
                options=lista_clientes,
                placeholder="Selecciona un cliente"
            )
        with col3:
            sucursal = st.selectbox("Sucursal", options=sucursales, help="Selecciona la sucursal")

        col4, col5 = st.columns(2)
        with col4:
            plazo = st.text_input("Plazo", placeholder="Plazo del contrato")
        with col5:
            volumen = st.number_input("Volumen Total del Contrato", min_value=0.0, step=1000.0)

        # Botón para pasar al siguiente paso
        continuar = st.form_submit_button("Siguiente")

        # Guardar los datos y avanzar al siguiente paso
        if continuar and cliente and sucursal:
            st.session_state.current_step = 2
            st.session_state.datos_basicos = {
                "Fecha": fecha,
                "Cliente": cliente,
                "Sucursal": sucursal,
                "Plazo": plazo,
                "Volumen Total": volumen
            }
        elif continuar:
            st.error("Por favor, complete todos los campos obligatorios.")

    # Botón para agregar productos desde esta pantalla
    st.subheader("Productos Agregados")
    producto = st.selectbox(
        "Producto",
        options=lista_productos,
        placeholder="Selecciona un producto"
    )
    precio_lista = st.number_input("Precio de lista (USD)", min_value=0.0, step=100.0)
    if st.button("Agregar Producto") and producto and precio_lista > 0:
        st.session_state.productos.append({
            "Producto": producto,
            "Precio lista (USD)": precio_lista
        })
        st.success(f"Producto {producto} agregado.")

    # Mostrar productos agregados con opción para eliminar
    if st.session_state.productos:
        st.subheader("Productos agregados")
        df_productos = pd.DataFrame(st.session_state.productos)
        st.table(df_productos)

        # Selección de producto para eliminar
        productos_disponibles = [prod["Producto"] for prod in st.session_state.productos]
        producto_a_eliminar = st.selectbox("Seleccionar producto para eliminar", options=productos_disponibles)
        if st.button("Eliminar Producto"):
            st.session_state.productos = [
                prod for prod in st.session_state.productos if prod["Producto"] != producto_a_eliminar
            ]
            st.success(f"Producto {producto_a_eliminar} eliminado.")
    else:
        st.info("No hay productos agregados aún.")

# Paso 2: Configurar descuentos y probabilidades
elif st.session_state.current_step == 2:
    st.title("Formulario de Cotización - Paso 2: Configuración de Descuentos")

    # Mostrar resumen de los datos básicos
    st.subheader("Datos Básicos")
    for key, value in st.session_state.datos_basicos.items():
        st.write(f"**{key}:** {value}")

    # Mostrar productos agregados
    st.subheader("Productos Agregados")
    if st.session_state.productos:
        df_productos = pd.DataFrame(st.session_state.productos)
        st.table(df_productos)
    else:
        st.info("No hay productos agregados aún.")

    # Inputs para configurar descuentos y probabilidades
    descuento_cols = st.columns(6)
    with descuento_cols[0]:
        descuento1 = st.number_input("Descuento Nivel 1 (%)", min_value=0.0, step=1.0, value=1.0)
    with descuento_cols[1]:
        probabilidad1 = st.number_input("Probabilidad Nivel 1 (%)", min_value=0.0, max_value=100.0, step=1.0, value=0.0)
    with descuento_cols[2]:
        descuento2 = st.number_input("Descuento Nivel 2 (%)", min_value=0.0, step=1.0, value=0.0)
    with descuento_cols[3]:
        probabilidad2 = st.number_input("Probabilidad Nivel 2 (%)", min_value=0.0, max_value=100.0, step=1.0, value=0.0)
    with descuento_cols[4]:
        descuento3 = st.number_input("Descuento Nivel 3 (%)", min_value=0.0, step=1.0, value=0.0)
    with descuento_cols[5]:
        probabilidad3 = st.number_input("Probabilidad Nivel 3 (%)", min_value=0.0, max_value=100.0, step=1.0, value=0.0)

    # Botones para volver al paso 1 o finalizar la cotización
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Regresar al Paso 1"):
            st.session_state.current_step = 1
    with col2:
        if st.button("Finalizar Cotización"):
            st.success("¡Cotización generada exitosamente!")
            # Lógica para guardar/exportar los datos
