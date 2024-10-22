import streamlit as st
from PIL import Image, ImageDraw
import io  # Necessario per gestire il buffer


def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if st.session_state.password_correct:
        return True

    password = st.text_input("Inserisci la password:", type="password")
    if st.button("Accedi"):
        if password == PASSWORD:
            st.session_state.password_correct = True
            st.success("Accesso riuscito!")
            return True
        else:
            st.error("Password errata, riprova.")

    return False

# Controlla se l'utente ha inserito la password corretta
if check_password():
    # Se la password è corretta, prosegui con la tua app esistente
    st.title("Benvenuto nella tua app!")
    
    # Il codice della tua app attuale
    uploaded_file = st.file_uploader("Scegli un'immagine", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        rows = st.slider("Righe", min_value=2, max_value=20, value=5)
        columns = st.slider("Colonne", min_value=2, max_value=20, value=5)

        width, height = image.size
        draw = ImageDraw.Draw(image)

        for i in range(1, rows):
            y = i * height / rows
            draw.line([(0, y), (width, y)], fill="red")
        for j in range(1, columns):
            x = j * width / columns
            draw.line([(x, 0), (x, height)], fill="red")

        st.image(image, caption='Immagine con griglia', use_column_width=True)
else:
    st.warning("Devi inserire la password corretta per accedere.")



# Caricamento dell'immagine
st.title("Grid Image App")

uploaded_file = st.file_uploader("Scegli un'immagine", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    # Sliders per controllare le righe e le colonne
    rows = st.slider("Righe", min_value=2, max_value=20, value=5)
    columns = st.slider("Colonne", min_value=2, max_value=20, value=5)

    # Disegna la griglia sull'immagine
    width, height = image.size
    draw = ImageDraw.Draw(image)

    # Disegna le linee della griglia
    for i in range(1, rows):
        y = i * height / rows
        draw.line([(0, y), (width, y)], fill="red")
    for j in range(1, columns):
        x = j * width / columns
        draw.line([(x, 0), (x, height)], fill="red")

    # Mostra l'immagine con la griglia
    st.image(image, caption='Immagine con griglia', use_column_width=True)

    # Buffer per salvare l'immagine con la griglia
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    byte_im = buf.getvalue()

    # Bottone per scaricare l'immagine con la griglia
    st.download_button(
        label="Scarica immagine con griglia",
        data=byte_im,
        file_name="image_with_grid.png",
        mime="image/png"
    )