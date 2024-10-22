import streamlit as st
from PIL import Image, ImageDraw, ImageColor
import io
import math

# Funzione per creare una griglia
def draw_grid(image, grid_type, rows, columns, line_thickness, line_opacity, color):
    width, height = image.size
    draw = ImageDraw.Draw(image.convert("RGBA"), "RGBA")

    # Converti il colore in un formato RGBA con opacità
    color_with_opacity = (*color, int(line_opacity * 255 / 100))

    if grid_type == "Square":
        for i in range(1, rows):
            y = i * height / rows
            draw.line([(0, y), (width, y)], fill=color_with_opacity, width=line_thickness)
        for j in range(1, columns):
            x = j * width / columns
            draw.line([(x, 0), (x, height)], fill=color_with_opacity, width=line_thickness)

    elif grid_type == "Hexagonal":
        hex_radius = min(width // (columns + 1), height // (rows + 0.5)) / 2
        hex_height = math.sqrt(3) * hex_radius
        hex_width = 2 * hex_radius
        
        for row in range(rows):
            for col in range(columns):
                x_offset = col * hex_width * 3/4
                y_offset = row * hex_height + (hex_height / 2 if col % 2 == 1 else 0)
                hexagon = [
                    (x_offset + hex_radius * math.cos(math.radians(60 * i)),
                     y_offset + hex_radius * math.sin(math.radians(60 * i))) for i in range(6)
                ]
                draw.polygon(hexagon, outline=color_with_opacity, width=line_thickness)

    return image

# Funzione per gestire l'accesso con password
def check_password():
    return st.session_state.get("password", "") == "PicaxMart.Dungeon00"

# Pannello di accesso con password
if 'password' not in st.session_state:
    st.session_state.password = ""

if 'access_granted' not in st.session_state:
    st.session_state.access_granted = False

if not st.session_state.access_granted:
    password_input = st.text_input("Enter Personal Password", type="password")
    if st.button("Submit"):
        if password_input == "PicaxMart.Dungeon00":
            st.session_state.access_granted = True
        else:
            st.error("Password incorrect. Please try again.")
    st.stop()

# Titolo
st.title("Grid Image App")

# Colonne: A sinistra l'anteprima, a destra impostazioni e download
col1, col2 = st.columns([2, 1])  # Due sezioni: anteprima e impostazioni/download

with col1:
    st.header("Image Preview")

    # Placeholder per l'immagine caricata
    image_with_grid = None
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"], label_visibility="collapsed")

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Image Preview", use_column_width=True)  # Visualizza anteprima

        # Sezione per impostazioni della griglia
        st.header("Grid Settings")
        grid_type = st.selectbox("Grid Type", ["Square", "Hexagonal"])
        color = st.color_picker("Select Grid Color", "#ff0000")
        rows = st.slider("Rows", min_value=1, max_value=50, value=5)
        columns = st.slider("Columns", min_value=1, max_value=50, value=5)
        line_thickness = st.slider("Grid Line Thickness", min_value=1, max_value=10, value=2)
        line_opacity = st.slider("Grid Line Opacity", min_value=0, max_value=100, value=100)

        # Disegna la griglia sull'immagine se caricata
        image_with_grid = draw_grid(image.copy(), grid_type, rows, columns, line_thickness, line_opacity, ImageColor.getrgb(color))

        # Mostra l'immagine modificata con la griglia
        st.image(image_with_grid, caption="Image with Grid", use_column_width=True)

with col2:
    # Sezione per il download e la rimozione dell'immagine
    st.header("Download/Remove")

    if image_with_grid:  # Se l'immagine con griglia è disponibile
        # Buffer per salvare l'immagine con la griglia
        buf = io.BytesIO()
        image_with_grid.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # Bottone per scaricare l'immagine con la griglia
        st.download_button(
            label="Download Image with Grid",
            data=byte_im,
            file_name="image_with_grid.png",
            mime="image/png"
        )

    # Bottone per rimuovere l'immagine caricata
    if st.button("Remove Image"):
        st.experimental_rerun()
