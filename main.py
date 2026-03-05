from fasthtml.common import *
import qrcode
import base64
from io import BytesIO
from rembg import remove
import barcode
from barcode.writer import ImageWriter
from datetime import datetime
from PIL import Image

# --- CONFIGURATION ---
CURRENT_YEAR = datetime.now().year

# --- DESIGN SPLENDIDE (MESH GRADIENT & GLASSMORPHISM) ---
custom_style = Style(f"""
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    :root {{
        --pico-font-family: 'Plus Jakarta Sans', sans-serif;
        --primary: #6366f1;
        --secondary: #a855f7;
        --glass: rgba(255, 255, 255, 0.7);
    }}

    body {{
        margin: 0;
        background-color: #f8fafc;
        /* Mesh Gradient Splendide */
        background-image: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(168, 85, 247, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
            radial-gradient(at 0% 100%, rgba(168, 85, 247, 0.15) 0px, transparent 50%);
        background-attachment: fixed;
        min-height: 100vh;
    }}

    .modern-card {{
        background: var(--glass);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        box-shadow: 0 20px 40px rgba(0,0,0,0.05);
        padding: 2.5rem;
        border-radius: 24px;
        transition: transform 0.3s ease;
    }}

    .hero-title {{
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }}

    .nav-pills {{
        display: flex; gap: 0.8rem; justify-content: center; margin: 2rem 0;
    }}
    .nav-pills a {{
        padding: 0.7rem 1.4rem; border-radius: 16px; text-decoration: none;
        background: white; color: #475569; font-weight: 600;
        border: 1px solid #e2e8f0; transition: all 0.3s ease;
        display: flex; align-items: center; gap: 8px;
    }}
    .nav-pills a.active {{ 
        background: #4f46e5; color: white; border-color: #4f46e5;
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3);
    }}

    .app-grid {{
        display: grid; grid-template-columns: 1fr 320px; gap: 2.5rem;
        max-width: 1200px; margin: auto; padding: 0 1.5rem;
    }}

    @media (max-width: 1000px) {{ .app-grid {{ grid-template-columns: 1fr; }} .sidebar {{ display: none; }} }}

    .sidebar-ad {{
        position: sticky; top: 2rem; height: 600px;
        background: rgba(0,0,0,0.03); border: 2px dashed #cbd5e1;
        border-radius: 24px; display: flex; align-items: center; justify-content: center;
    }}

    .logo-container {{
        display: flex; align-items: center; justify-content: center; gap: 12px; margin-bottom: 10px;
    }}

    .key-value-row {{ display: grid; grid-template-columns: 1fr 1fr 50px; gap: 10px; margin-bottom: 12px; }}
    .output-box {{ 
        margin-top: 2rem; padding: 2rem; border-radius: 20px; 
        background: white; border: 2px solid #f1f5f9; text-align: center; 
    }}
""")

app, rt = fast_app(hdrs=(
    Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"),
    custom_style,
    # Script pour les icônes Lucide
    Script(src="https://unpkg.com/lucide@latest")
))

# --- COMPOSANTS ---

def Logo():
    """Génère un logo SVG moderne"""
    return Div(
        # SVG d'un cube abstrait stylisé
        Safe(f"""<svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="url(#grad)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <defs><linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#4f46e5" /><stop offset="100%" style="stop-color:#9333ea" /></linearGradient></defs>
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
            <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
            <line x1="12" y1="22.08" x2="12" y2="12"></line>
        </svg>"""),
        H1("UtilityBox", style="margin:0; font-size: 1.8rem; font-weight: 800;"),
        cls="logo-container"
    )

def DataRow(name="keys", val_name="values"):
    """Ligne générique pour Clé:Valeur"""
    return Div(
        Input(name=name, placeholder="Clé (ex: Nom)"),
        Input(name=val_name, placeholder="Valeur"),
        Button(Safe('<i data-lucide="trash-2"></i>'), type="button", cls="outline secondary", onclick="this.parentElement.remove()", style="padding: 10px;"),
        cls="key-value-row"
    )

def Layout(content, active_page, title="UtilityBox"):
    nav_items = [
        ("Accueil", "/", "home"),
        ("QR Code", "/qr-tab", "qr-code"),
        ("Barcode", "/barcode-tab", "barcode"),
        ("RemBg", "/rembg-tab", "image")
    ]
    return Title(title), Main(
        Header(
            Logo(),
            Div(H1("Boostez votre productivité", cls="hero-title"), P("Outils premium, gratuits pour toujours."), cls="text-center", style="text-align:center"),
            Nav(Div(*[A(Safe(f'<i data-lucide="{icon}"></i> {name}'), href=url, cls="active" if active_page == name else "") for name, url, icon in nav_items], cls="nav-pills"))
        ),
        Div(
            Section(content),
            Aside(Div(P("Publicité Sponsorisée", style="font-size:0.7rem; color:#94a3b8"), cls="sidebar-ad"), cls="sidebar"),
            cls="app-grid"
        ),
        Footer(P(f"© {CURRENT_YEAR} UtilityBox"), style="text-align:center; padding: 4rem; opacity:0.6;"),
       
        # Initialise les icônes après le rendu
        Script("lucide.createIcons();"),
         cls="container",
    )

# --- ROUTES ---

@rt("/")
def get():
    cards = Grid(
        Card(H3("📱 QR Code"), P("Mode lien ou fiches de données complexes."), Footer(A(Button("Lancer"), href="/qr-tab")), cls="modern-card"),
        Card(H3("🔢 Barcode"), P("Formats standards EAN/UPC et Code 128."), Footer(A(Button("Lancer"), href="/barcode-tab")), cls="modern-card"),
        Card(H3("🖼️ RemBg"), P("Suppression du fond par Intelligence Artificielle."), Footer(A(Button("Lancer"), href="/rembg-tab")), cls="modern-card"),
    )
    return Layout(cards, "Accueil")

# --- SECTION QR CODE (MISE À JOUR KEY-VALUE) ---

@rt("/qr-tab")
def get():
    content = Div(
        H2("Générateur de QR Code Pro"),
        Form(
            Label("Type de contenu", 
                Select(Option("Lien URL Simple", value="url"), Option("Données Clé:Valeur (Fiche)", value="kv"), 
                       name="qr_type", hx_get="/qr-fields", hx_target="#qr-fields-container", hx_trigger="load, change")
            ),
            Div(id="qr-fields-container"),
            Grid(
                Label("Couleur Code", Input(type="color", name="fill_color", value="#4f46e5")),
                Label("Couleur Fond", Input(type="color", name="back_color", value="#ffffff"))
            ),
            Label("Logo central", Input(type="file", name="logo", accept="image/*")),
            Button("🚀 Générer le QR Code"),
            hx_post="/generate-qrcode", hx_target="#qr-out", enctype="multipart/form-data"
        ),
        Div(id="qr-out"),
        cls="modern-card"
    )
    return Layout(content, "QR Code")

@rt("/qr-fields")
def get(qr_type: str):
    if qr_type == "url":
        return Input(name="url", placeholder="https://votre-lien.com", required=True)
    else:
        return Div(
            Div(DataRow("qr_keys", "qr_values"), id="qr-kv-list"),
            Button("+ Ajouter une donnée", type="button", cls="outline", hx_get="/qr-add-row", hx_target="#qr-kv-list", hx_swap="beforeend"),
            style="margin-bottom:20px"
        )

@rt("/qr-add-row")
def get(): return DataRow("qr_keys", "qr_values")

# --- SECTION BARCODE ---

@rt("/barcode-tab")
def get():
    types = [("code128", "Code 128 (Clé-Valeur)"), ("ean13", "EAN-13 (Standard)"), ("upca", "UPC-A")]
    content = Div(
        H2("Générateur de Code-barres"),
        Form(
            Select(*[Option(l, value=v) for v, l in types], name="barcode_type", hx_get="/barcode-fields", hx_target="#bc-fields", hx_trigger="load, change"),
            Div(id="bc-fields"),
            Button("Générer"),
            hx_post="/generate-barcode", hx_target="#bc-out"
        ),
        Div(id="bc-out"),
        cls="modern-card"
    )
    return Layout(content, "Barcode")

@rt("/barcode-fields")
def get(barcode_type: str):
    if barcode_type in ["ean13", "upca"]:
        return Input(name="data", placeholder="Numéros uniquement", required=True)
    else:
        return Div(Div(DataRow(), id="bc-kv-list"), Button("+ Ajouter", type="button", cls="outline", hx_get="/bc-add-row", hx_target="#bc-kv-list", hx_swap="beforeend"))

@rt("/bc-add-row")
def get(): return DataRow()

@rt("/rembg-tab")
def get():
    content = Div(
        H2("IA : Suppression d'Arrière-plan"),
        Form(
            Input(type="file", name="image", accept="image/*", required=True),
            Button("Supprimer le fond"),
            hx_post="/remove-background", hx_target="#bg-out", hx_indicator="#load-ai", enctype="multipart/form-data"
        ),
        Div(id="load-ai", cls="htmx-indicator", aria_busy="true"),
        Div(id="bg-out"),
        cls="modern-card"
    )
    return Layout(content, "RemBg")

# --- LOGIQUE POST ---

@rt("/generate-qrcode", methods=["POST"])
async def post_qr(qr_type:str, url:str=None, qr_keys:list=None, qr_values:list=None, fill_color:str="#000000", back_color:str="#ffffff", logo:UploadFile=None):
    # Construction du contenu
    content = url if qr_type == "url" else ""
    if qr_type == "kv" and qr_keys:
        if isinstance(qr_keys, str): qr_keys, qr_values = [qr_keys], [qr_values]
        content = "\n".join([f"{k}: {v}" for k, v in zip(qr_keys, qr_values) if k.strip()])
    
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(content)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGB')
    
    if logo and logo.size > 0:
        l_img = Image.open(BytesIO(await logo.read()))
        l_img.thumbnail((img.size[0]//4, img.size[1]//4))
        img.paste(l_img, ((img.size[0]-l_img.size[0])//2, (img.size[1]-l_img.size[1])//2))
        
    buf = BytesIO()
    img.save(buf, format="PNG")
    img_str = base64.b64encode(buf.getvalue()).decode()
    return Div(Img(src=f"data:image/png;base64,{img_str}", style="max-width:280px"), Br(), A(Button("⬇️ Télécharger PNG"), href=f"data:image/png;base64,{img_str}", download="qrcode.png"), cls="output-box")

@rt("/generate-barcode", methods=["POST"])
async def post_bc(barcode_type:str, data:str=None, keys:list=None, values:list=None):
    try:
        final_data = data if data else ""
        if keys and values:
            if isinstance(keys, str): keys, values = [keys], [values]
            final_data = " | ".join([f"{k}:{v}" for k,v in zip(keys, values) if k.strip()])
        
        bc_class = barcode.get_barcode_class(barcode_type)
        my_bc = bc_class(final_data, writer=ImageWriter())
        buf = BytesIO()
        my_bc.write(buf)
        img_str = base64.b64encode(buf.getvalue()).decode()
        return Div(Img(src=f"data:image/png;base64,{img_str}"), Br(), A(Button("⬇️ Télécharger"), href=f"data:image/png;base64,{img_str}", download="barcode.png"), cls="output-box")
    except Exception as e: return Div(f"Erreur: {e}", cls="error-msg")

@rt("/remove-background", methods=["POST"])
async def post_bg(image:UploadFile):
    res = remove(await image.read())
    img_str = base64.b64encode(res).decode()
    return Div(Img(src=f"data:image/png;base64,{img_str}"), Br(), A(Button("⬇️ Télécharger"), href=f"data:image/png;base64,{img_str}", download="nobg.png"), cls="output-box")


if __name__ == "__main__":
    import uvicorn
    import os
    # Hugging Face utilise 7860 par défaut, les autres utilisent PORT
    port = int(os.environ.get("PORT", os.environ.get("PORT", 7860)))
    uvicorn.run(app, host="0.0.0.0", port=port)
