from fasthtml.common import *
from starlette.responses import PlainTextResponse
import qrcode
import base64
from io import BytesIO
from rembg import remove
import barcode
from barcode.writer import ImageWriter
from datetime import datetime
from PIL import Image
import os

# --- CONFIGURATION ---
CURRENT_YEAR = datetime.now().year

# --- GOOGLE ADSENSE SCRIPT ---
adsense_script = Script(
    src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4081303157053373",
    async_=True,
    crossorigin="anonymous"
)

# --- SEO & META TAGS ---
meta_tags = (
    Meta(name="description", content="RetailBox - Service de génération de QR Code, Code-barres EAN13/Code128 et détourage d'image par IA. Outils gratuits pour le commerce et la logistique."),
    Meta(name="keywords", content="Générer QR Code, Créer Code-barres, EAN13, Code 128, Enlever fond image, Détourage IA, PNG transparent, Outil Retail"),
    Meta(property="og:title", content="RetailBox | Outils de génération QR et Barcode"),
    Meta(name="viewport", content="width=device-width, initial-scale=1, maximum-scale=1")
)

# --- DESIGN CORRIGÉ (SANS UNDERLINES & DARK MODE FIXED) ---
custom_style = Style(f"""
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    :root {{
        --pico-font-family: 'Plus Jakarta Sans', sans-serif;
        --primary: #4f46e5;
        --secondary: #9333ea;
        --glass: rgba(255, 255, 255, 0.9); /* Plus opaque pour la lisibilité mobile */
        --pico-color: #1e293b;
        --pico-background-color: #f8fafc;
    }}

    /* Désactiver le mode sombre forcé sur mobile */
    @media (prefers-color-scheme: dark) {{
        :root {{
            --pico-color: #1e293b;
            --pico-background-color: #f8fafc;
            --glass: rgba(255, 255, 255, 0.95);
        }}
    }}

    body {{
        margin: 0; padding: 0;
        background-color: #f8fafc;
        background-image: 
            radial-gradient(at 0% 0%, rgba(79, 70, 229, 0.1) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(147, 51, 234, 0.1) 0px, transparent 50%);
        background-attachment: fixed;
        min-height: 100vh;
        color: #1e293b;
    }}

    /* Supprimer les traits sous les liens */
    a {{ text-decoration: none !important; color: inherit; }}

    .hero-title {{
        font-size: clamp(1.6rem, 7vw, 3.2rem);
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
        margin-bottom: 1rem;
    }}

    /* --- NAVIGATION --- */
    .nav-scroll-container {{
        width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch;
        padding: 10px 0;
    }}
    .nav-pills {{
        display: flex; gap: 0.8rem; justify-content: center;
        min-width: max-content; padding: 0 1rem;
    }}
    @media (max-width: 600px) {{ .nav-pills {{ justify-content: flex-start; }} }}

    .nav-pills a, button:not(.secondary), .btn-download {{
        padding: 0.6rem 1.2rem !important;
        border-radius: 14px !important;
        background: white !important;
        color: #475569 !important;
        font-weight: 700 !important;
        border: 1px solid #e2e8f0 !important;
        transition: all 0.2s ease !important;
        display: inline-flex; align-items: center; gap: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        cursor: pointer;
    }}

    .nav-pills a.active, button:not(.secondary):hover {{
        background: var(--primary) !important;
        color: white !important;
        border-color: var(--primary) !important;
    }}

    /* --- CARTES & FOOTERS --- */
    .modern-card {{
        background: var(--glass);
        backdrop-filter: blur(10px);
        border: 1px solid #e2e8f0;
        padding: 1.5rem;
        border-radius: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05);
    }}

    .modern-card footer {{
        background: transparent !important; /* Enlever le fond noir/gris de Pico */
        border-top: 1px solid #f1f5f9;
        margin-top: 1rem;
        padding: 1rem 0 0 0;
    }}

    .app-grid {{
        display: grid; grid-template-columns: 1fr 320px; gap: 2rem;
        max-width: 1200px; margin: auto; padding: 0 1rem;
    }}
    @media (max-width: 1024px) {{ .app-grid {{ grid-template-columns: 1fr; }} }}

    .sidebar-ad {{
        background: rgba(0,0,0,0.02); border: 2px dashed #cbd5e1;
        border-radius: 20px; min-height: 250px;
        display: flex; align-items: center; justify-content: center;
    }}

    .top-ad-banner {{
        max-width: 1200px; margin: 0 auto 1.5rem auto;
        min-height: 90px; background: rgba(0,0,0,0.01);
        border-radius: 16px; border: 1px dashed #e2e8f0;
        display: flex; align-items: center; justify-content: center;
    }}
""")

# --- INITIALISATION APP ---
app, rt = fast_app(
    static_path='public',
    hdrs=(
        *meta_tags,
        Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"),
        custom_style,
        adsense_script,
        Script(src="https://unpkg.com/lucide@latest")
    )
)

# --- COMPOSANTS INSTRUCTIFS ---

def Logo():
    return Div(
        Safe(f"""<svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="url(#grad)" stroke-width="2.5">
            <defs><linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#4f46e5" /><stop offset="100%" style="stop-color:#9333ea" /></linearGradient></defs>
            <path d="M21 16V8l-9-5-9 5v8l9 5 9-5z"></path>
        </svg>"""),
        H1("RetailBox", style="margin:0; font-size: 1.4rem; font-weight: 800;"),
        style="display:flex; align-items:center; justify-content:center; gap:8px; margin-bottom:1rem;"
    )

def SeoContent():
    return Section(
        Div(
            H2("Comment utiliser nos services de génération"),
            Grid(
                Div(
                    H4("Générateur de QR Code"),
                    P("Saisissez une URL ou des données textuelles. Le moteur génère un code QR haute résolution. Support des logos personnalisés et des formats de couleurs pour l'impression pro.")
                ),
                Div(
                    H4("Générateur de Code-barres"),
                    P("Saisie de codes EAN-13 (12 chiffres) ou Code 128 (texte). Génération instantanée d'étiquettes conformes aux scanners laser pour la logistique et la vente.")
                ),
                Div(
                    H4("Suppression d'arrière-plan"),
                    P("Traitement d'image par IA pour le détourage automatique. Téléchargement direct au format PNG transparent sans perte de qualité.")
                )
            ),
            cls="modern-card", style="margin-top:2rem;"
        )
    )

def FooterSection():
    return Footer(
        Div(
            Div(H4("📜 Service"), P("Outils de génération gratuits. Traitement éphémère en mémoire vive."), cls="footer-section"),
            Div(H4("👤 Confidentialité"), P("Aucun stockage d'images ou de données saisies."), cls="footer-section"),
            Div(H4("🛡️ Légal"), P("Usage sous votre responsabilité. Standard conforme AdSense."), cls="footer-section"),
            cls="footer-content"
        ),
        Div(
            A("Conditions", href="/terms"), A("Vie Privée", href="/privacy"), A("Contact", href="/contact"),
            Span(f"© {CURRENT_YEAR} RetailBox"),
            cls="legal-links"
        ),
        cls="pro-footer"
    )

def Layout(content, active_page, title="RetailBox"):
    nav_items = [("Accueil", "/", "home"), ("QR Code", "/qr-tab", "qr-code"), ("Barcode", "/barcode-tab", "barcode"), ("RemBg", "/rembg-tab", "image")]
    return Title(f"{active_page} | {title}"), Main(
        Header(
            Logo(),
            Div(H1("Générez, Créez et Transformez en un clic", cls="hero-title"), 
                P("Outils techniques pour le commerce et la logistique.", style="text-align:center;"), 
                style="text-align:center"),
            Div(
                Nav(Div(*[A(Safe(f'<i data-lucide="{icon}" style="width:18px"></i> {name}'), href=url, cls="active" if active_page == name else "") for name, url, icon in nav_items], cls="nav-pills")),
                cls="nav-scroll-container"
            )
        ),
        Div(P("Annonce", style="font-size:0.6rem; opacity:0.3; margin:0"), cls="top-ad-banner"),
        Div(
            Section(content),
            Aside(Div(P("Publicité", style="font-size:0.6rem; opacity:0.3"), cls="sidebar-ad"), cls="sidebar"),
            cls="app-grid"
        ),
        FooterSection(),
        Script("lucide.createIcons();"),
        cls="container"
    )

# --- ROUTES ---

@rt("/ads.txt")
def get():
    return PlainTextResponse("google.com, pub-4081303157053373, DIRECT, f08c47fec0942fa0")

@rt("/")
def get():
    cards = Grid(
        Card(Div(Safe('<i data-lucide="qr-code" style="width:32px; color:var(--primary);"></i>')), H3("Générer QR Code"), P("Format PNG/SVG haute définition avec logo."), Footer(A(Button("Ouvrir"), href="/qr-tab")), cls="modern-card"),
        Card(Div(Safe('<i data-lucide="barcode" style="width:32px; color:var(--primary);"></i>')), H3("Générer Barcode"), P("Formats EAN-13, Code 128 et UPC-A."), Footer(A(Button("Ouvrir"), href="/barcode-tab")), cls="modern-card"),
        Card(Div(Safe('<i data-lucide="image" style="width:32px; color:var(--primary);"></i>')), H3("Détourer Image"), P("Suppression automatique d'arrière-plan par IA."), Footer(A(Button("Ouvrir"), href="/rembg-tab")), cls="modern-card"),
    )
    return Layout(Div(cards, SeoContent()), "Accueil")

@rt("/qr-tab")
def get():
    content = Div(
        H2("Générateur QR Code"),
        Form(
            Select(Option("URL", value="url"), Option("Fiche Clé:Valeur", value="kv"), name="qr_type", hx_get="/qr-fields", hx_target="#qr-f", hx_trigger="load, change"),
            Div(id="qr-f"),
            Grid(Label("Code", Input(type="color", name="fill_color", value="#4f46e5")), Label("Fond", Input(type="color", name="back_color", value="#ffffff"))),
            Label("Logo (Optionnel)", Input(type="file", name="logo", accept="image/*")),
            Button("🚀 Générer"), hx_post="/generate-qrcode", hx_target="#qr-out", enctype="multipart/form-data"
        ),
        Div(id="qr-out"), cls="modern-card"
    )
    return Layout(content, "QR Code")

@rt("/qr-fields")
def get(qr_type:str):
    if qr_type == "url": return Input(name="url", placeholder="Lien URL", required=True)
    return Div(Div(Input(name="qr_keys", placeholder="Clé"), Input(name="qr_values", placeholder="Valeur"), cls="key-value-row", id="qr-kv-list", style="display:grid; grid-template-columns: 1fr 1fr 40px; gap:8px;"), 
               Button("+ Ajouter", type="button", hx_get="/qr-add-row", hx_target="#qr-kv-list", hx_swap="afterend", cls="outline secondary"))

@rt("/qr-add-row")
def get(): return Div(Input(name="qr_keys", placeholder="Clé"), Input(name="qr_values", placeholder="Valeur"), Button("X", type="button", onclick="this.parentElement.remove()", cls="outline"), cls="key-value-row", style="display:grid; grid-template-columns: 1fr 1fr 40px; gap:8px; margin-top:10px;")

@rt("/barcode-tab")
def get():
    types = [("code128", "Code 128"), ("ean13", "EAN-13"), ("upca", "UPC-A")]
    content = Div(
        H2("Générateur Barcode"),
        Form(
            Select(*[Option(l, value=v) for v, l in types], name="barcode_type", hx_get="/bc-fields", hx_target="#bc-f", hx_trigger="load, change"),
            Div(id="bc-f"), Button("Générer"), hx_post="/generate-barcode", hx_target="#bc-out"
        ),
        Div(id="bc-out"), cls="modern-card"
    )
    return Layout(content, "Barcode")

@rt("/bc-fields")
def get(barcode_type:str):
    placeholder = "12 chiffres" if barcode_type == "ean13" else "Texte ou chiffres"
    return Input(name="data", placeholder=placeholder, required=True)

@rt("/rembg-tab")
def get():
    content = Div(
        H2("Détourage Image IA"),
        Form(Input(type="file", name="image", accept="image/*", required=True), Button("Détourer"), hx_post="/remove-background", hx_target="#bg-out", hx_indicator="#load", enctype="multipart/form-data"),
        Div(id="load", cls="htmx-indicator", aria_busy="true"), Div(id="bg-out"), cls="modern-card"
    )
    return Layout(content, "RemBg")

# --- LOGIQUE POST ---
@rt("/generate-qrcode", methods=["POST"])
async def post_qr(qr_type:str, url:str=None, qr_keys:list=None, qr_values:list=None, fill_color:str="#000000", back_color:str="#ffffff", logo:UploadFile=None):
    c = url if qr_type == "url" else "\n".join([f"{k}:{v}" for k,v in zip(qr_keys, qr_values) if k])
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(c); qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGB')
    if logo and logo.size > 0:
        log = Image.open(BytesIO(await logo.read())); log.thumbnail((img.size[0]//4, img.size[1]//4))
        img.paste(log, ((img.size[0]-log.size[0])//2, (img.size[1]-log.size[1])//2))
    buf = BytesIO(); img.save(buf, format="PNG")
    s = base64.b64encode(buf.getvalue()).decode()
    return Div(Img(src=f"data:image/png;base64,{s}", style="max-width:250px;"), Br(), A(Button("⬇️ Télécharger"), href=f"data:image/png;base64,{s}", download="qrcode.png"), cls="output-box")

@rt("/generate-barcode", methods=["POST"])
async def post_bc(barcode_type:str, data:str):
    try:
        bc = barcode.get_barcode_class(barcode_type)(data, writer=ImageWriter())
        buf = BytesIO(); bc.write(buf); s = base64.b64encode(buf.getvalue()).decode()
        return Div(Img(src=f"data:image/png;base64,{s}"), Br(), A(Button("⬇️ Télécharger"), href=f"data:image/png;base64,{s}", download="barcode.png"), cls="output-box")
    except Exception as e: return Div(f"Erreur format: {e}", cls="error-msg")

@rt("/remove-background", methods=["POST"])
async def post_bg(image:UploadFile):
    res = remove(await image.read()); s = base64.b64encode(res).decode()
    return Div(Img(src=f"data:image/png;base64,{s}"), Br(), A(Button("⬇️ Télécharger"), href=f"data:image/png;base64,{s}", download="nobg.png"), cls="output-box")

# --- PAGES LÉGALES ---
@rt("/terms")
def get(): return Layout(Div(H2("Conditions"), P("Service gratuit de génération de codes et détourage."), cls="modern-card"), "Conditions")
@rt("/privacy")
def get(): return Layout(Div(H2("Vie Privée"), P("Aucune donnée n'est stockée."), cls="modern-card"), "Confidentialité")
@rt("/contact")
def get(): return Layout(Div(H2("Contact"), P("Email: utilitybox.project@gmail.com"), cls="modern-card"), "Contact")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))