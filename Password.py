import streamlit as st

# Definisci la password generale
PASSWORD = "passwordtestrpgmaps"  # Sostituisci con la tua password unica

# Funzione per verificare la password
def check_password():
    # Se l'utente è già loggato, non richiedere di nuovo la password
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    # Se la password è stata inserita correttamente, non fare nulla
    if st.session_state.password_correct:
        return True

    # Altrimenti mostra il campo per inserire la password
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
    # Il contenuto della tua app va qui
    st.title("Benvenuto nella tua app!")
    st.write("Ora puoi accedere al contenuto della tua app.")
    # Aggiungi il codice della tua app qui
else:
    st.warning("Devi inserire la password corretta per accedere.")