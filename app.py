import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import qrcode
from io import BytesIO

# --- DATI PIANTE ---
DATA = [
    {"id": "tronchetto", "nome": "Tronchetto del Madagascar", "desc": "Fusto sottile. Resistente poca luce.", "rules": [9, 6, 12, 18]},
    {"id": "aloe", "nome": "Aloe Vera", "desc": "Succulenta. No acqua se umido.", "rules": [17, 14, 25, 35]},
    {"id": "giglio", "nome": "Giglio della Pace", "desc": "Foglie lucide, fiori bianchi.", "rules": [7, 6, 12, 12]},
    {"id": "fusaggine", "nome": "Fusaggine Giapponese", "desc": "Arbusto resistente. Inverno: MAI.", "rules": [9, 4, 12, 999]},
    {"id": "kalanchoe", "nome": "Kalanchoe Variegata", "desc": "Foglie carnose. Teme ristagni.", "rules": [17, 14, 25, 35]},
    {"id": "fatsia", "nome": "Fatsia Japanica", "desc": "Grandi foglie lobate.", "rules": [6, 4, 9, 12]},
    {"id": "palma", "nome": "Palma della Fortuna", "desc": "Foglie a ventaglio.", "rules": [9, 6, 12, 17]},
    {"id": "pothos", "nome": "Pothos", "desc": "Liane, foglie a cuore.", "rules": [9, 6, 12, 17]},
    {"id": "zamioculca", "nome": "Zamioculca", "desc": "Foglie cerose. Poca acqua.", "rules": [17, 14, 25, 35]},
    {"id": "plectranthus", "nome": "Plectranthus", "desc": "Portamento ricadente.", "rules": [6, 4, 9, 12]},
    {"id": "dracaena", "nome": "Dracaena Fragrans", "desc": "Tronchetto della felicità.", "rules": [12, 9, 17, 25]},
    {"id": "cordyline", "nome": "Cordyline Fruticosa", "desc": "Foglie colorate (rosso/rosa).", "rules": [12, 9, 17, 25]},
    {"id": "pachira", "nome": "Pachira Acquatica", "desc": "Albero dei soldi. Tronco intrecciato.", "rules": [9, 9, 17, 17]},
    {"id": "alocasia", "nome": "Alocasia (Orecchie Elefante)", "desc": "Foglie enormi a cuore.", "rules": [6, 5, 9, 11]},
    {"id": "dyckia", "nome": "Dyckia", "desc": "Succulenta spinosa. Teme eccesso acqua.", "rules": [21, 21, 35, 35]}
]

def get_season_idx():
    m = datetime.now().month
    if 3 <= m <= 5: return 0 # Primavera
    if 6 <= m <= 8: return 1 # Estate
    if 9 <= m <= 11: return 2 # Autunno
    return 3 # Inverno

st.set_page_config(page_title="Green Office", page_icon="🌿")
season_names = ["Primavera", "Estate", "Autunno", "Inverno"]
s_idx = get_season_idx()

if 'log' not in st.session_state: st.session_state.log = {}

st.title(f"🌿 Gestione Piante - {season_names[s_idx]}")

# Logica QR
pid = st.query_params.get("plant_id")
if pid:
    p = next((x for x in DATA if x["id"] == pid), None)
    if p:
        st.header(p['nome'])
        st.info(p['desc'])
        days = p['rules'][s_idx]
        
        last = st.session_state.log.get(pid, datetime.now().strftime("%Y-%m-%d"))
        if days == 999:
            nxt = "Manuale (Controllare terreno)"
        else:
            nxt = (datetime.strptime(last, "%Y-%m-%d") + timedelta(days=days)).strftime("%Y-%m-%d")
        
        st.metric("Ultima Acqua", last)
        st.metric("Prossima", nxt)
        
        if st.button("💦 HO INNAFFIATO ORA"):
            st.session_state.log[pid] = datetime.now().strftime("%Y-%m-%d")
            st.success("Registrato!")
            st.rerun()

# Generatore QR
st.sidebar.header("🖨️ Stampa QR Code")
if st.sidebar.checkbox("Mostra codici"):
    # IL TUO LINK CORRETTO:
    url_base = "https://piante-ufficio-kchykjcgehambaqjlyfmvb.streamlit.app"
    for p in DATA:
        img = qrcode.make(f"{url_base}/?plant_id={p['id']}")
        buf = BytesIO(); img.save(buf); st.sidebar.image(buf.getvalue(), caption=p['nome'])
        
