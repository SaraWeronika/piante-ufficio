import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import qrcode
from io import BytesIO
from streamlit_lottie import st_lottie
import requests

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Ufficio Green", page_icon="🌿", layout="centered")

# --- FUNZIONI GRAFICHE E ANIMAZIONI ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

# Animazione Annaffiatoio
lottie_water = load_lottieurl("https://lottie.host/956d9c86-6e5f-4633-a261-2df633619a33/sI1Y7zYJp8.json")

# CSS PER SFONDO E STILE
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
background-image: url("https://images.unsplash.com/photo-1470058869958-2a77ade41c02?ixlib=rb-4.0.3&auto=format&fit=crop&w=2070&q=80");
background-size: cover;
}
[data-testid="stHeader"] {background-color: rgba(0,0,0,0);}
.stMarkdown, .stText, h1, h2, h3 {
    text-shadow: 2px 2px 4px #000000;
    color: white !important;
}
div[data-testid="stExpander"] {
    background-color: rgba(255, 255, 255, 0.85);
    border-radius: 15px;
    color: black !important;
}
div[data-testid="stExpander"] p, div[data-testid="stExpander"] h1 {
    color: black !important;
    text-shadow: none !important;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# --- DATABASE PIANTE (DAL TUO PDF) ---
DATA = [
    {
        "id": "tronchetto", "nome": "Tronchetto del Madagascar",
        "desc": "Pianta popolare con fusto sottile e legnoso. Foglie strette e arcuate. Resistente e tollerante alla scarsa luce.",
        "rules": [9, 6, 12, 18],
        "img": "https://images.unsplash.com/photo-1612362940127-23739773c642?w=500"
    },
    {
        "id": "aloe", "nome": "Aloe Vera",
        "desc": "Succulenta nota per il gel lenitivo. Ideale per scottature. Non innaffiare MAI se il terriccio è umido.",
        "rules": [17, 14, 25, 35],
        "img": "https://images.unsplash.com/photo-1602613823593-879418892928?w=500"
    },
    {
        "id": "giglio", "nome": "Giglio della Pace",
        "desc": "Apprezzata per foglie lucide e fiori bianchi a vela. Purifica l'aria. Facile da coltivare.",
        "rules": [7, 6, 12, 12],
        "img": "https://images.unsplash.com/photo-1593691973565-863d65dfb597?w=500"
    },
    {
        "id": "fusaggine", "nome": "Fusaggine Giapponese",
        "desc": "Arbusto sempreverde compatto. INVERNO: MAI acqua (solo se secchissimo). Trae acqua dalle piogge.",
        "rules": [9, 4, 12, 999],
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Euonymus_japonicus_0.jpg/320px-Euonymus_japonicus_0.jpg"
    },
    {
        "id": "kalanchoe", "nome": "Kalanchoe Variegata",
        "desc": "Succulenta a foglie carnose. Teme i ristagni. Innaffiare dal basso.",
        "rules": [17, 14, 25, 35],
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Kalanchoe_blossfeldiana_4.jpg/320px-Kalanchoe_blossfeldiana_4.jpg"
    },
    {
        "id": "fatsia", "nome": "Fatsia Japanica",
        "desc": "Grandi foglie lobate che ricordano mani aperte. Cresce rapidamente. Innaffiare abbondantemente.",
        "rules": [6, 4, 9, 12],
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Fatsia_japonica_002.JPG/320px-Fatsia_japonica_002.JPG"
    },
    {
        "id": "palma", "nome": "Palma della Fortuna",
        "desc": "Fogliame a ventaglio, tocco esotico. Evitare ristagni per prevenire marciume.",
        "rules": [9, 6, 12, 17],
        "img": "https://images.unsplash.com/photo-1598632721662-0413b6170367?w=500"
    },
    {
        "id": "pothos", "nome": "Pothos",
        "desc": "Liane lunghe e foglie a cuore. Resistente e purifica l'aria. Ottima per principianti.",
        "rules": [9, 6, 12, 17],
        "img": "https://images.unsplash.com/photo-1596727563993-2303f977f283?w=500"
    },
     {
        "id": "zamioculca", "nome": "Zamioculca",
        "desc": "Foglie cerose verde scuro. Richiede pochissima acqua grazie ai rizomi.",
        "rules": [17, 14, 25, 35],
        "img": "https://images.unsplash.com/photo-1600417148500-662e39a0c34c?w=500"
    }
]

# Gestione Stagione
def get_season_idx():
    m = datetime.now().month
    if 3 <= m <= 5: return 0 # Primavera
    if 6 <= m <= 8: return 1 # Estate
    if 9 <= m <= 11: return 2 # Autunno
    return 3 # Inverno

season_names = ["Primavera", "Estate", "Autunno", "Inverno"]
s_idx = get_season_idx()

# Memoria (Nota: Si resetta al riavvio se non usiamo Google Sheets!)
if 'log' not in st.session_state: st.session_state.log = {}

# --- INTERFACCIA ---

# 1. Se c'è un QR Code (plant_id nell'URL)
pid = st.query_params.get("plant_id")

if pid:
    # VISTA PIANTA SINGOLA
    p = next((x for x in DATA if x["id"] == pid), None)
    if p:
        st.title(p['nome'])
        st.image(p['img'], use_container_width=True)
        
        # Card bianca per i dettagli
        with st.container():
            st.markdown(f"### 📖 {p['desc']}")
            st.markdown("---")
            
            days = p['rules'][s_idx]
            last = st.session_state.log.get(pid, datetime.now().strftime("%Y-%m-%d"))
            
            if days == 999:
                nxt_date_str = "MANUALE"
                msg_col = "off"
            else:
                nxt_date = datetime.strptime(last, "%Y-%m-%d") + timedelta(days=days)
                nxt_date_str = nxt_date.strftime("%d %b %Y")
                days_left = (nxt_date.date() - datetime.now().date()).days
                
                if days_left < 0: msg_col = "red" # Ritardo
                elif days_left == 0: msg_col = "orange" # Oggi
                else: msg_col = "green" # Tutto ok

            col1, col2 = st.columns(2)
            col1.metric("📅 Ultima Acqua", last)
            col2.metric("💧 Prossima Acqua", nxt_date_str)
            
            st.write("") # Spazio
            
            # Animazione Annaffiatoio sopra il bottone
            st_lottie(lottie_water, height=150, key="water_anim")
            
            if st.button("💦 HO INNAFFIATO ORA", type="primary", use_container_width=True):
                st.session_state.log[pid] = datetime.now().strftime("%Y-%m-%d")
                st.balloons() # Festeggiamenti visuali!
                st.success("✅ Ottimo lavoro! Pianta registrata.")
                st.rerun()
            
            if st.button("🔙 Torna alla Dashboard"):
                st.query_params.clear()
                st.rerun()

else:
    # 2. VISTA DASHBOARD (Tutte le piante) - Per controllo da remoto
    st.title(f"🌿 Dashboard Ufficio ({season_names[s_idx]})")
    st.markdown("**Clicca su una pianta per vedere i dettagli e aggiornarla.**")
    
    # Griglia di piante
    for p in DATA:
        with st.expander(f"🌱 {p['nome']}"):
            c1, c2 = st.columns([1,2])
            with c1:
                st.image(p['img'], width=100)
            with c2:
                last = st.session_state.log.get(p['id'], "Mai registrata")
                st.write(f"**Ultima:** {last}")
                if st.button("Vedi Dettagli", key=p['id']):
                    st.query_params["plant_id"] = p['id']
                    st.rerun()

# Generatore QR (Nascosto in sidebar)
st.sidebar.header("🖨️ Stampa QR Code")
if st.sidebar.checkbox("Mostra codici"):
    # INCOLLA QUI IL TUO LINK CORRETTO:
    url_base = "https://piante-ufficio-kchykjcgehambaqjlyfmvb.streamlit.app"
    for p in DATA:
        img = qrcode.make(f"{url_base}/?plant_id={p['id']}")
        buf = BytesIO(); img.save(buf); st.sidebar.image(buf.getvalue(), caption=p['nome'])
