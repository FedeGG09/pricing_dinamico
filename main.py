import streamlit as st
import pandas as pd

# Configuración de la app
st.set_page_config(page_title="Formulario de Cotización", layout="wide")

# Header principal
st.title("Formulario de Cotización")

# Número de cotización en la esquina superior derecha
cotizacion_col, _ = st.columns([1, 3])
with cotizacion_col:
    st.text_input("Número de cotización:", "000000", disabled=True)

# Cargar productos desde el archivo CSV
csv_path = "C:\\Users\\Federico Gravina\\Downloads\\PRODUCTOS_UNICOS.csv"
try:
    df_productos_csv = pd.read_csv(csv_path, encoding="latin1", header=None)  # Indica que no hay encabezado
    lista_productos = df_productos_csv[0].tolist()  # Usa la primera columna como lista de productos
except Exception as e:
    st.error(f"No se pudo cargar el archivo CSV: {e}")
    lista_productos = []
except Exception as e:
    st.error(f"No se pudo cargar el archivo CSV: {e}")
    lista_productos = []
    st.error(f"No se encontró la columna 'Producto' en el archivo CSV. Columnas detectadas: {df_productos_csv.columns.tolist()}")
    lista_productos = []
except Exception as e:
    st.error(f"No se pudo cargar el archivo CSV: {e}")
    lista_productos = []

# Formulario para los datos del header
with st.form("formulario_cotizacion"):
    st.subheader("Datos de la cotización")

    # Sección Header
    col1, col2, col3 = st.columns(3)
    with col1:
        fecha = st.date_input("Fecha")
    with col2:
        cliente = st.text_input("Cliente", placeholder="Nombre del cliente")
    with col3:
        sucursal = st.text_input("Sucursal", placeholder="Nombre de la sucursal")

    col4, col5 = st.columns(2)
    with col4:
        plazo = st.text_input("Plazo", placeholder="Plazo del Contrato")
    with col5:
        volumen = st.number_input("Volumen Total del Contrato", min_value=0.0, step=1000.0)

    # Sección Productos
    st.subheader("Productos y descuentos")

    if "productos" not in st.session_state:
        st.session_state.productos = []

    # Inputs para agregar productos
    producto_col, precio_col = st.columns([2, 1])
    with producto_col:
        # Usar un campo de selección con autocompletar
        producto = st.selectbox(
            "Producto",
            options=lista_productos,
            placeholder="Escribe para buscar o selecciona un producto"
        )
    with precio_col:
        precio_lista = st.number_input("Precio de lista en USD", min_value=0.0, step=100.0)

    # Inputs para descuentos y probabilidades
    descuento_cols = st.columns(6)
    with descuento_cols[0]:
        descuento1 = st.number_input("Descuento Nivel 1 (%)", min_value=0.0, step=1.0)
    with descuento_cols[1]:
        probabilidad1 = st.number_input("Probabilidad Nivel 1 (%)", min_value=0.0, max_value=100.0, step=1.0)
    with descuento_cols[2]:
        descuento2 = st.number_input("Descuento Nivel 2 (%)", min_value=0.0, step=1.0)
    with descuento_cols[3]:
        probabilidad2 = st.number_input("Probabilidad Nivel 2 (%)", min_value=0.0, max_value=100.0, step=1.0)
    with descuento_cols[4]:
        descuento3 = st.number_input("Descuento Nivel 3 (%)", min_value=0.0, step=1.0)
    with descuento_cols[5]:
        probabilidad3 = st.number_input("Probabilidad Nivel 3 (%)", min_value=0.0, max_value=100.0, step=1.0)

    # Botón para agregar productos
    agregar_producto = st.form_submit_button("Agregar Producto")

    # Agregar productos a la lista si se hace clic en el botón
    if agregar_producto and producto and precio_lista > 0:
        st.session_state.productos.append({
            "Producto": producto,
            "Precio lista (USD)": precio_lista,
            "Descuento Nivel 1 (%)": descuento1,
            "Probabilidad Nivel 1 (%)": probabilidad1,
            "Descuento Nivel 2 (%)": descuento2,
            "Probabilidad Nivel 2 (%)": probabilidad2,
            "Descuento Nivel 3 (%)": descuento3,
            "Probabilidad Nivel 3 (%)": probabilidad3
        })
        st.success(f"Producto {producto} agregado.")

# Mostrar productos agregados
st.subheader("Productos agregados")
if st.session_state.productos:
    df_productos = pd.DataFrame(st.session_state.productos)
    st.table(df_productos)
else:
    st.info("No hay productos agregados aún.")

# Botón para generar cotización
if st.button("Generar Cotización"):
    if st.session_state.productos:
        st.success("¡Cotización generada exitosamente!")
        # Aquí puedes agregar la lógica para guardar o exportar los datos
    else:
        st.error("Debe agregar al menos un producto para generar la cotización.")