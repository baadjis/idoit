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

adsense_script = Script(
    src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4081303157053373",
    async_=True,
    crossorigin="anonymous"
)

# --- SEO & META TAGS ---
meta_tags = (
    Meta(name="description", content="Service professionnel pour générer des QR Codes HD, créer des codes-barres EAN-13/Code128 et supprimer l'arrière-plan d'images par IA gratuitement."),
    Meta(name="keywords", content="Générateur QR Code, Créer Barcode, EAN13 gratuit, Détourage IA, PNG transparent, Étiquettes commerce"),
    Meta(property="og:title", content="RetailBox | Outils de génération QR et Barcode"),
    Meta(name="viewport", content="width=device-width, initial-scale=1, maximum-scale=1"),
    # Force le mode clair pour éviter les bugs de couleurs sur mobile
    Meta(name="color-scheme", content="light")
)

# --- DESIGN CORRIGÉ (SANS UNDERLINES & DARK MODE FIXED) ---
custom_style = Style(f"""
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    :root {{
        --pico-font-family: 'Plus Jakarta Sans', sans-serif;
        --primary: #4f46e5;
        --glass: #ffffff;
        --pico-color: #0f172a; /* Texte noir profond pour lisibilité max */
        --pico-background-color: #f8fafc;
        color-scheme: light; /* Force le navigateur en mode clair */
    }}

    /* Désactiver totalement le mode sombre forcé des systèmes mobiles */
    @media (prefers-color-scheme: dark) {{
        :root {{
            --pico-color: #0f172a !important;
            --pico-background-color: #f8fafc !important;
        }}
        body {{ background-color: #f8fafc !important; color: #0f172a !important; }}
        .modern-card {{ background: #ffffff !important; color: #0f172a !important; }}
    }}

    body {{
        margin: 0; padding: 0;
        background-color: #f8fafc;
        background-image: radial-gradient(at 0% 0%, rgba(79, 70, 229, 0.08) 0px, transparent 50%),
                          radial-gradient(at 100% 0%, rgba(147, 51, 234, 0.08) 0px, transparent 50%);
        background-attachment: fixed;
        min-height: 100vh;
        color: #0f172a;
    }}

    /* Suppression des soulignements sur tous les liens */
    a {{ text-decoration: none !important; color: inherit; border: none; }}

    .hero-title {{
        font-size: clamp(1.7rem, 8vw, 3rem);
        font-weight: 800;
        color: #1e293b;
        line-height: 1.2;
        margin-bottom: 0.5rem;
    }}

    /* --- BOUTONS --- */
    .nav-pills a, button, .btn-download {{
        padding: 0.8rem 1.5rem !important;
        border-radius: 12px !important;
        background: white !important;
        color: #1e293b !important;
        font-weight: 700 !important;
        border: 2px solid #e2e8f0 !important;
        transition: all 0.2s ease !important;
        display: inline-flex; align-items: center; justify-content: center;
        box-shadow: none !important;
        cursor: pointer;
    }}

    .nav-pills a.active, button:not(.secondary):hover {{
        background: var(--primary) !important;
        color: white !important;
        border-color: var(--primary) !important;
    }}

    /* --- CARTES & BOUTONS LARGEUR TOTALE --- */
    .modern-card {{
        background: #ffffff;
        border: 2px solid #e2e8f0;
        padding: 1.5rem;
        border-radius: 16px;
        color: #0f172a;
    }}

    .modern-card footer {{
        background: transparent !important;
        padding: 1rem 0 0 0 !important;
        margin-top: 1rem !important;
        border-top: 1px solid #f1f5f9;
    }}

    .modern-card footer button, .modern-card footer a {{
        width: 100% !important; /* Bouton occupe toute la largeur */
        display: flex !important;
    }}

    /* --- LAYOUT --- */
    .app-grid {{
        display: grid; grid-template-columns: 1fr 300px; gap: 2rem;
        max-width: 1100px; margin: auto; padding: 0 1rem;
    }}
    @media (max-width: 1024px) {{ .app-grid {{ grid-template-columns: 1fr; }} }}

    .nav-scroll-container {{ width: 100%; overflow-x: auto; padding: 10px 0; }}
    .nav-pills {{ display: flex; gap: 0.5rem; min-width: max-content; }}

    .sidebar-ad {{
        background: #f1f5f9; border: 2px dashed #cbd5e1;
        border-radius: 16px; min-height: 250px;
        display: flex; align-items: center; justify-content: center;
    }}
""")

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

# --- CONTENU INSTRUCTIF (SEO) ---

def SeoContent():
    return Section(
        Div(
            H2("Instructions : Comment générer vos fichiers", style="color: #0f172a;"),
            Grid(
                Div(
                    H4("Génération de QR Code"),
                    P("1. Sélectionnez le type 'URL' ou 'Données'. 2. Saisissez vos informations. 3. Personnalisez les couleurs ou ajoutez un logo. 4. Cliquez sur générer pour obtenir un fichier PNG haute définition prêt pour l'impression.")
                ),
                Div(
                    H4("Création de Code-barres"),
                    P("1. Choisissez le format (EAN-13 pour le commerce, Code 128 pour l'inventaire). 2. Entrez les chiffres ou le texte requis. 3. Le système vérifie automatiquement la conformité du format. 4. Téléchargez l'étiquette conforme aux scanners laser.")
                ),
                Div(
                    H4("Détourage Image par IA"),
                    P("1. Téléchargez une photo (JPG, PNG). 2. Notre Intelligence Artificielle identifie le sujet principal. 3. L'arrière-plan est supprimé sans aucune action manuelle. 4. Exportez instantanément au format PNG avec fond transparent.")
                )
            ),
            cls="modern-card", style="margin-top:2rem;"
        )
    )

# --- COMPOSANTS INTERFACE ---

def Logo():
    return Div(
        Safe(f"""<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#4f46e5" stroke-width="3"><path d="M21 16V8l-9-5-9 5v8l9 5 9-5z"></path></svg>"""),
        H1("RetailBox", style="margin:0; font-size: 1.3rem; font-weight: 800; color:#0f172a;"),
        style="display:flex; align-items:center; justify-content:center; gap:8px; margin-bottom:1rem;"
    )

def FooterSection():
    return Footer(
        Div(
            Div(H4("Service"), P("Outils techniques de génération. Traitement éphémère sécurisé."), cls="footer-section"),
            Div(H4("Confidentialité"), P("Zéro stockage de fichiers ou d'images."), cls="footer-section"),
            Div(H4("Légal"), P("Usage gratuit conforme aux standards publicitaires."), cls="footer-section"),
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
            Div(H1("Générez et Transformez vos outils digitaux", cls="hero-title"), 
                P("Services techniques gratuits pour le commerce et l'industrie.", style="text-align:center; color:#475569;"), 
                style="text-align:center"),
            Div(Nav(Div(*[A(Safe(f'<i data-lucide="{icon}" style="width:18px"></i> {name}'), href=url, cls="active" if active_page == name else "") for name, url, icon in nav_items], cls="nav-pills")), cls="nav-scroll-container")
        ),
        Div(
            Section(content),
            Aside(Div(P("Publicité", style="font-size:0.6rem; color:#94a3b8"), cls="sidebar-ad"), cls="sidebar"),
            cls="app-grid"
        ),
        FooterSection(),
        Script("lucide.createIcons();"),
        cls="container"
    )

# --- ROUTES ---

@rt("/ads.txt")
def get(): return PlainTextResponse("google.com, pub-4081303157053373, DIRECT, f08c47fec0942fa0")

@rt("/")
def get():
    cards = Grid(
        Card(Div(Safe('<i data-lucide="qr-code" style="width:32px; color:var(--primary);"></i>')), H3("Générer QR Code"), P("Format HD avec logo pour liens et données."), Footer(A(Button("Ouvrir l'outil"), href="/qr-tab")), cls="modern-card"),
        Card(Div(Safe('<i data-lucide="barcode" style="width:32px; color:var(--primary);"></i>')), H3("Générer Barcode"), P("Formats EAN-13, Code 128 et UPC-A."), Footer(A(Button("Ouvrir l'outil"), href="/barcode-tab")), cls="modern-card"),
        Card(Div(Safe('<i data-lucide="image" style="width:32px; color:var(--primary);"></i>')), H3("Détourer Image"), P("Suppression fond automatique par IA."), Footer(A(Button("Ouvrir l'outil"), href="/rembg-tab")), cls="modern-card"),
    )
    return Layout(Div(cards, SeoContent()), "Accueil")

@rt("/qr-tab")
def get():
    content = Div(
        H2("Générateur QR Code HD"),
        Form(
            Select(Option("Lien URL", value="url"), Option("Fiche Données", value="kv"), name="qr_type", hx_get="/qr-fields", hx_target="#qr-f", hx_trigger="load, change"),
            Div(id="qr-f"),
            Grid(Label("Couleur Code", Input(type="color", name="fill_color", value="#000000")), Label("Couleur Fond", Input(type="color", name="back_color", value="#ffffff"))),
            Label("Logo Central (Optionnel)", Input(type="file", name="logo", accept="image/*")),
            Button("🚀 Générer le QR Code"), hx_post="/generate-qrcode", hx_target="#qr-out", enctype="multipart/form-data"
        ),
        Div(id="qr-out"), cls="modern-card"
    )
    return Layout(content, "QR Code")

@rt("/qr-fields")
def get(qr_type:str):
    if qr_type == "url": return Input(name="url", placeholder="Lien (ex: https://...)", required=True)
    return Div(Div(Input(name="qr_keys", placeholder="Clé"), Input(name="qr_values", placeholder="Valeur"), cls="key-value-row", id="qr-kv-list", style="display:grid; grid-template-columns: 1fr 1fr 40px; gap:8px;"), 
               Button("+ Ajouter une ligne", type="button", hx_get="/qr-add-row", hx_target="#qr-kv-list", hx_swap="afterend", cls="outline secondary"))

@rt("/qr-add-row")
def get(): return Div(Input(name="qr_keys", placeholder="Clé"), Input(name="qr_values", placeholder="Valeur"), Button("X", type="button", onclick="this.parentElement.remove()", cls="outline"), cls="key-value-row", style="display:grid; grid-template-columns: 1fr 1fr 40px; gap:8px; margin-top:10px;")

@rt("/barcode-tab")
def get():
    types = [("code128", "Code 128"), ("ean13", "EAN-13"), ("upca", "UPC-A")]
    content = Div(
        H2("Générateur de Barcode"),
        Form(
            Select(*[Option(l, value=v) for v, l in types], name="barcode_type", hx_get="/bc-fields", hx_target="#bc-f", hx_trigger="load, change"),
            Div(id="bc-f"), Button("Générer le Code-barres"), hx_post="/generate-barcode", hx_target="#bc-out"
        ),
        Div(id="bc-out"), cls="modern-card"
    )
    return Layout(content, "Barcode")

@rt("/bc-fields")
def get(barcode_type:str):
    placeholder = "Entrez 12 chiffres" if barcode_type == "ean13" else "Entrez votre texte"
    return Input(name="data", placeholder=placeholder, required=True)

@rt("/rembg-tab")
def get():
    content = Div(
        H2("Suppression fond par IA"),
        Form(Input(type="file", name="image", accept="image/*", required=True), Button("Détourer l'image"), hx_post="/remove-background", hx_target="#bg-out", hx_indicator="#load", enctype="multipart/form-data"),
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
def get(): return Layout(Div(H2("Conditions"), P("Service gratuit de génération technique sans garantie de disponibilité."), cls="modern-card"), "Conditions")
@rt("/privacy")
def get(): return Layout(Div(H2("Vie Privée"), P("Aucune donnée personnelle ou binaire n'est conservée après traitement."), cls="modern-card"), "Confidentialité")
@rt("/contact")
def get(): return Layout(Div(H2("Contact"), P("Email Support : utilitybox.project@gmail.com"), cls="modern-card"), "Contact")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))