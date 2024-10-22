import streamlit as st
from PIL import Image, ImageDraw, ImageColor
import io
import math

# Funzione per creare una griglia
def draw_grid(image, grid_type, rows, columns, line_thickness, line_opacity, color):
    width, height = image.size
    draw = ImageDraw.Draw(image, "RGBA")
    
    # Converti il colore in un formato RGBA con opacità
    color_with_opacity = (*color, int(line_opacity * 255 / 100))
    
    if grid_type == "Square":
        # Disegna la griglia quadrata
        for i in range(1, rows):
            y = i * height / rows
            draw.line([(0, y), (width, y)], fill=color_with_opacity, width=line_thickness)
        for j in range(1, columns):
            x = j * width / columns
            draw.line([(x, 0), (x, height)], fill=color_with_opacity, width=line_thickness)
    
    elif grid_type == "Hexagonal":
        # Disegna la griglia esagonale
        hex_radius = min(width // columns, height // (rows + 0.5)) / 2  # Calcola il raggio degli esagoni
        hex_height = math.sqrt(3) * hex_radius  # Altezza dell'esagono
        hex_width = 2 * hex_radius  # Larghezza dell'esagono
        
        for row in range(rows):
            for col in range(columns):
                # Calcola la posizione dell'esagono
                x_offset = col * hex_width * 3/4
                y_offset = row * hex_height + (hex_height / 2 if col % 2 == 1 else 0)
                
                # Calcola i vertici dell'esagono
                hexagon = [
                    (x_offset + hex_radius * math.cos(math.radians(60 * i)),
                     y_offset + hex_radius * math.sin(math.radians(60 * i))) for i in range(6)
                ]
                
                # Disegna l'esagono
                draw.polygon(hexagon, outline=color_with_opacity, width=line_thickness)

    return image

# Funzione per gestire l'accesso con password
def check_password():
    password = st.sidebar.text_input("Enter Personal Password", type="password")
    if password == "PicaxMart.Dungeon00":
        return True
    else:
        st.sidebar.error("Password incorrect. Please try again.")
        return False

# Controlla la password
if not check_password():
    st.stop()

# Titolo
st.title("Grid Image App")

# Colonna: Anteprima dell'immagine caricata e impostazioni
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Scheda con le impostazioni della griglia
    st.header("Grid Settings")
    grid_type = st.selectbox("Grid Type", ["Square", "Hexagonal"])
    color = st.color_picker("Select Grid Color", "#ff0000")
    rows = st.slider("Rows", min_value=1, max_value=50, value=5)
    columns = st.slider("Columns", min_value=1, max_value=50, value=5)
    line_thickness = st.slider("Grid Line Thickness", min_value=1, max_value=10, value=2)
    line_opacity = st.slider("Grid Line Opacity", min_value=0, max_value=100, value=100)

    # Disegna la griglia sull'immagine
    image_with_grid = draw_grid(image.copy(), grid_type, rows, columns, line_thickness, line_opacity, ImageColor.getrgb(color))
    
    # Mostra l'immagine con la griglia
    st.image(image_with_grid, caption="Image with Grid", use_column_width=True)

    # Sezione per il download e la rimozione dell'immagine
    st.header("Download/Remove")
    
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