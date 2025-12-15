import streamlit as st
import base64

# ---------- GESTION DES IMAGES ----------
def image_to_base64(image_path):
    try:
        with open(image_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode("utf-8")
    except FileNotFoundError:
        return ""

bot_img_b64 = image_to_base64("images/bot_image.avif")
user_img_b64 = image_to_base64("images/user_image.png")

# ---------- CSS PREMIUM & MODERNE ----------
css = f'''
<style>
    /* IMPORTATION POLICE GOOGLE (Poppins) */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Poppins', sans-serif;
    }}

    /* 1. BACKGROUND & STRUCTURE */
    .stApp {{
        background-color: #ffffff;
        color: #333333;
    }}
    
    /* Cache le menu hamburger et le footer "Made with Streamlit" pour un look App native */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* 2. SIDEBAR ÉLÉGANTE */
    [data-testid="stSidebar"] {{
        background-color: #f8f9fa;
        border-right: 1px solid #eaeaea;
        padding-top: 2rem;
    }}
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
        color: #0288d1;
        font-weight: 600;
    }}

    /* 3. TITRE PRINCIPAL CENTRÉ */
    h1 {{
        text-align: center;
        color: #1a202c;
        font-weight: 600;
        margin-bottom: 1.5rem;
    }}
    
    /* 4. ZONE DE TEXTE (INPUT) MODERNE */
    div[data-baseweb="base-input"] {{
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        transition: all 0.3s ease;
    }}
    
    /* Effet "Glow" quand on clique dans la zone de texte */
    div[data-baseweb="base-input"]:focus-within {{
        border-color: #0288d1 !important;
        box-shadow: 0 0 0 3px rgba(2, 136, 209, 0.1) !important;
    }}

    input[type="text"] {{
        color: #2d3748 !important;
        font-size: 1rem;
    }}

    /* 5. BOUTONS (Effet 3D léger) */
    .stButton button {{
        background: linear-gradient(135deg, #0288d1 0%, #01579b 100%) !important;
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 500;
        box-shadow: 0 4px 6px rgba(2, 136, 209, 0.2);
        transition: transform 0.2s, box-shadow 0.2s;
        width: 100%; /* Boutons pleine largeur sidebar */
    }}
    
    .stButton button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(2, 136, 209, 0.3);
    }}
    
    .stButton button:active {{
        transform: translateY(0);
    }}

    /* 6. FILE UPLOADER (Clean) */
    [data-testid="stFileUploaderDropzone"] {{
        background-color: #ffffff !important;
        border: 2px dashed #cbd5e0 !important;
        border-radius: 12px;
        padding: 1rem;
        transition: border-color 0.3s;
    }}
    [data-testid="stFileUploaderDropzone"]:hover {{
        border-color: #0288d1 !important;
        background-color: #f0f9ff !important;
    }}
    [data-testid="stFileUploaderDropzone"] div, span, small {{
        color: #4a5568 !important;
    }}

    /* 7. CHAT BUBBLES (Arrondies et stylées) */
    .chat-container {{
        max-width: 850px;
        margin: auto;
    }}
    
    .chat-message {{
        padding: 1.2rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: flex-start;
        font-size: 0.95rem;
        line-height: 1.6;
    }}
    
    /* USER: Dégradé moderne et arrondi spécifique */
    .chat-message.user {{
        background: linear-gradient(135deg, #3182ce 0%, #2c5282 100%);
        color: white;
        flex-direction: row-reverse;
        margin-left: auto;
        box-shadow: 0 4px 15px rgba(49, 130, 206, 0.2);
        border-bottom-right-radius: 2px; /* Petite "queue" de bulle */
    }}
    
    /* BOT: Blanc cassé propre avec ombre */
    .chat-message.bot {{
        background: #ffffff;
        color: #2d3748;
        border: 1px solid #edf2f7;
        margin-right: auto;
        box-shadow: 0 4px 6px rgba(0,0,0,0.04);
        border-bottom-left-radius: 2px; /* Petite "queue" de bulle */
    }}
    
    .chat-message .avatar img {{
        width: 48px;
        height: 48px;
        border-radius: 50%;
        margin: 0 12px;
        border: 2px solid #fff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    
    /* Liens dans le chat */
    .chat-message a {{
        color: #63b3ed;
        text-decoration: none;
        font-weight: bold;
    }}
    .chat-message a:hover {{
        text-decoration: underline;
    }}
    
</style>
'''

st.markdown(css, unsafe_allow_html=True)

# ---------- TEMPLATES HTML ----------
bot_template = f'''
<div class="chat-message bot">
    <div class="avatar">
        <img src="data:image/avif;base64,{bot_img_b64}" alt="Bot Avatar">
    </div>
    <div class="message">{{{{MSG}}}}</div>
</div>
'''

user_template = f'''
<div class="chat-message user">
    <div class="avatar">
        <img src="data:image/png;base64,{user_img_b64}" alt="User Avatar">
    </div>    
    <div class="message">{{{{MSG}}}}</div>
</div>
'''