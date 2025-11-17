import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import qrcode
from io import BytesIO

# --- DATI PIANTE CON FOTO ---
DATA = [
    {
        "id": "tronchetto", 
        "nome": "Tronchetto del Madagascar", 
        "desc": "Fusto sottile. Resistente poca luce.", 
        "rules": [9, 6, 12, 18],
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Dracaena_marginata_var._tricolor.jpg/320px-Dracaena_marginata_var._tricolor.jpg"
    },
    {
        "id": "aloe", 
        "nome": "Aloe Vera", 
        "desc": "Succulenta. No acqua se umido.", 
        "rules": [17, 14, 25, 35],
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Aloe_vera_flower_inset.png/320px-Aloe_vera_flower_inset.png"
    },
    {
        "id": "giglio", 
        "nome": "Giglio della Pace", 
        "desc": "Foglie lucide, fiori bianchi.", 
        "rules": [7, 6, 12, 12],
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Spathiphyllum_cochlearispathum_RTBG.jpg/320px-Spathiphyllum_cochlearispathum_RTBG.jpg"
    },
    {
        "id": "fusaggine", 
        "nome": "Fusaggine Giapponese", 
        "desc": "Arbusto resistente. Inverno: MAI.", 
        "rules": [9, 4, 12, 999],
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Euonymus_japonicus_0.jpg/320px-Euonymus_japonicus_0.jpg"
    },
    {
        "id": "kalanchoe", 
        "nome": "Kalanchoe Variegata", 
        "desc": "Foglie carnose. Teme ristagni.", 
        "rules": [17, 14, 25, 35],
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Kalanchoe_blossfeldiana_4.jpg/320px-Kalanchoe_blossfeldiana_4.jpg"
    },
    {
        "id": "fatsia", 
        "nome": "Fatsia Japanica", 
        "desc": "Grandi foglie lobate.", 
        "rules": [6, 4, 9, 12],
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Fatsia_japonica_002.JPG/320px-Fatsia_japonica_002.JPG"
    },
    {
        "id": "palma", 
        "nome": "Palma della Fortuna", 
        "desc": "Foglie a ventaglio.", 
        "rules": [9, 6, 12, 17],
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Trachycarpus_fortunei_at_Kew_Gardens.jpg/320px-Trachycarpus_fortunei_at_Kew_Gardens.jpg"
    },
    {
        "id": "pothos", 
        "nome": "Pothos", 
        "desc": "Liane, foglie a cuore.", 
        "rules": [9, 6, 12, 17],
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2d/Epipremnum_aureum_31082013.jpg/320px-Epipremnum_aureum_31082013.jpg"
    },
    {
        "id": "zamioculca", 
        "nome": "Zamioculca", 
        "desc": "Foglie cerose. Poca acqua.", 
        "rules": [17, 14, 25, 35],
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Zamioculcas_zamiifolia_%28ZZ_plant%29.jpg/320px-Zamioculcas_zamiifolia_%28ZZ_plant%29.jpg"
    },
    {
        "id": "plectranthus", 
        "nome": "Plectranthus", 
        "desc": "Portamento ricadente.", 
        "rules": [6, 4, 9, 12],
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Plectranthus_verticillatus.jpg/320px-Plectranthus_verticillatus.jpg"
    },
    {
        "id": "dracaena", 
        "nome": "Dracaena Fragrans", 
        "desc": "Tronchetto della felicità.", 
        "rules": [12, 9, 17, 25],
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Starr_080117-1537_Dracaena_fragrans.jpg/320px-Starr_080117-1537_Dracaena_fragrans.jpg"
    },
    {
        "id": "cordyline", 
        "nome": "Cordyline Fruticosa", 
        "desc": "Foglie colorate (rosso/rosa).", 
        "rules": [12, 9, 17, 25],
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/17/Cordyline_fruticosa_11.jpg/320px-Cordyline_fruticosa_11.jpg"
    },
    {
        "id": "pachira", 
        "nome": "Pachira Acquatica", 
        "desc": "Albero dei soldi. Tronco intrecciato.", 
        "rules": [9, 9, 17, 17],
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/89/Pachira_aquatica_02.jpg/320px-Pachira_aquatica_02.jpg"
    },
    {
        "id": "alocasia", 
        "nome": "Alocasia (Orecchie Elefante)", 
        "desc": "Foglie enormi a cuore.", 
        "rules": [6, 5, 9, 11],
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Alocasia_macrorrhizos_3.jpg/320px-Alocasia_macrorrhizos_3.jpg"
    },
    {
        "id": "dyckia", 
        "nome": "Dyckia", 
        "desc": "Succulenta spinosa. Teme eccesso acqua.", 
        "rules": [21, 21, 35, 35],
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Dyckia_encholirioides_kz01.jpg/320px-Dyckia_encholirioides_kz01.jpg"
    }
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
        st.image(p['img'], width=300) # <-- ORA C'È LA FOTO!
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
    # LINK AGGIORNATO:
    url_base = "https://piante-ufficio-kchykjcgehambaqjlyfmvb.streamlit.app"
    for p in DATA:
        img = qrcode.make(f"{url_base}/?plant_id={p['id']}")
        st.sidebar.image(p['img'], width=100)
        buf = BytesIO(); img.save(buf); st.sidebar.image(buf.getvalue(), caption=p['nome'])
    
