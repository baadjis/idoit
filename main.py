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
    Meta(name="description", content="Générateur gratuit de QR Codes HD, création de codes-barres EAN13 et détourage photo par IA. Instructions simples pour outils digitaux pro."),
    Meta(name="keywords", content="Générer QR Code, Créer Barcode, EAN13 gratuit, Détourage IA, PNG transparent, Étiquettes commerce, UGC"),
    Meta(property="og:title", content="RetailBox | Outils de génération QR et Barcode"),
    Meta(name="viewport", content="width=device-width, initial-scale=1, maximum-scale=1"),
    Meta(name="color-scheme", content="light")
)

# --- DESIGN STABILISÉ (FORCÉ CLAIR ET SANS SOULIGNEMENT) ---
custom_style = Style(f"""
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    :root {{
        --pico-font-family: 'Plus Jakarta Sans', sans-serif;
        --primary: #4f46e5;
        --pico-color: #0f172a !important; /* Noir profond */
        --pico-background-color: #ffffff !important;
        color-scheme: light;
    }}

    /* Désactiver mode sombre iPhone/Android */
    @media (prefers-color-scheme: dark) {{
        body, html, main, section, div, p, h1, h2, h3, h4, span, a, footer {{ 
            background-color: #ffffff !important; 
            color: #0f172a !important; 
        }}
        .modern-card {{ background: #f8fafc !important; border: 1px solid #e2e8f0 !important; }}
    }}

    body {{
        margin: 0; padding: 0; background-color: #ffffff;
        background-image: radial-gradient(at 0% 0%, rgba(79, 70, 229, 0.05) 0px, transparent 50%);
        min-height: 100vh; color: #0f172a;
    }}

    /* Suppression des traits sous les liens */
    a, a:hover, a:focus {{ text-decoration: none !important; color: inherit; border: none !important; outline: none !important; }}

    .hero-title {{
        font-size: clamp(1.8rem, 8vw, 3rem); font-weight: 800;
        color: #0f172a; line-height: 1.2;
    }}

    /* --- BOUTONS --- */
    .nav-pills a, button, .btn-download {{
        padding: 0.7rem 1.4rem !important; border-radius: 12px !important;
        background: #f1f5f9 !important; color: #0f172a !important;
        font-weight: 700 !important; border: 1px solid #e2e8f0 !important;
        display: inline-flex; align-items: center; justify-content: center;
        cursor: pointer; transition: 0.2s;
    }}

    .nav-pills a.active, button:not(.secondary):hover, .btn-download:hover {{
        background: var(--primary) !important; color: #ffffff !important;
        border-color: var(--primary) !important;
    }}

    /* --- CARTES ET BOUTONS LARGEUR TOTALE --- */
    .modern-card {{
        background: #f8fafc; border: 1px solid #e2e8f0;
        padding: 1.5rem; border-radius: 20px; color: #0f172a;
    }}
    .modern-card footer {{
        background: transparent !important; border-top: 1px solid #e2e8f0;
        padding: 1rem 0 0 0 !important; margin-top: 1rem !important;
    }}
    .modern-card footer a, .modern-card footer button {{
        width: 100% !important; /* Toute la largeur */
        display: flex !important;
    }}

    /* --- ESPACES PUB --- */
    .top-ad-banner {{
        width: 100%; max-width: 1100px; margin: 1rem auto;
        min-height: 90px; background: #f1f5f9; border: 1px dashed #cbd5e1;
        border-radius: 12px; display: flex; align-items: center; justify-content: center;
    }}
    .sidebar-ad {{
        background: #f1f5f9; border: 2px dashed #cbd5e1; border-radius: 20px;
        min-height: 300px; display: flex; align-items: center; justify-content: center;
    }}

    /* --- GRID --- */
    .app-grid {{
        display: grid; grid-template-columns: 1fr 320px; gap: 2rem;
        max-width: 1100px; margin: auto; padding: 0 1rem;
    }}
    @media (max-width: 1024px) {{ .app-grid {{ grid-template-columns: 1fr; }} }}

    .nav-scroll-container {{ width: 100%; overflow-x: auto; padding: 10px 0; }}
    .nav-pills {{ display: flex; gap: 0.6rem; min-width: max-content; }}

    footer.pro-footer {{ border-top: 1px solid #e2e8f0; padding: 3rem 1rem; margin-top: 5rem; }}
    .footer-content {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; max-width: 1200px; margin: auto; }}
    .legal-links {{ display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid #e2e8f0; font-size: 0.85rem; }}
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
            H2("Guide : Comment générer vos fichiers techniques"),
            Grid(
                Div(
                    H4("Génération de QR Code"),
                    P("1. Choisissez entre un lien URL ou une fiche texte. 2. Saisissez vos données. 3. Personnalisez les couleurs ou insérez un logo. 4. Téléchargez votre image haute définition pour impression.")
                ),
                Div(
                    H4("Création de Code-barres"),
                    P("1. Sélectionnez le format (EAN-13 pour commerce, Code 128 pour logistique). 2. Saisissez vos chiffres. 3. Obtenez instantanément une étiquette conforme aux scanners laser standards.")
                ),
                Div(
                    H4("Suppression de fond par IA"),
                    P("1. Téléchargez une photo produit. 2. Notre Intelligence Artificielle détourre automatiquement le sujet. 3. Exportez le résultat en format PNG transparent sans action manuelle.")
                )
            ),
            cls="modern-card", style="margin-top:2rem;"
        )
    )

# --- PAGES LÉGALES & FOOTER ---

def FooterSection():
    return Footer(
        Div(
            Div(H4("Technique"), P("Outils de génération gratuits. Traitement éphémère en mémoire vive."), cls="footer-section"),
            Div(H4("Confidentialité"), P("Zéro stockage de vos photos ou données saisies."), cls="footer-section"),
            Div(H4("Propriété (UGC)"), P("Vous êtes propriétaire exclusif des fichiers générés sur ce site."), cls="footer-section"),
            cls="footer-content"
        ),
        Div(
            A("Conditions", href="/terms"), 
            A("Vie Privée", href="/privacy"), 
            A("Droits UGC", href="/ugc"), # NOUVEAU LIEN UGC
            A("Contact", href="/contact"),
            Span(f"© {CURRENT_YEAR} RetailBox"),
            cls="legal-links"
        ),
        cls="pro-footer"
    )

def Layout(content, active_page, title="RetailBox"):
    nav_items = [("Accueil", "/", "home"), ("QR Code", "/qr-tab", "qr-code"), ("Barcode", "/barcode-tab", "barcode"), ("RemBg", "/rembg-tab", "image")]
    return Title(f"{active_page} | {title}"), Main(
        Header(
            Div(Safe(f'<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#4f46e5" stroke-width="3"><path d="M21 16V8l-9-5-9 5v8l9 5 9-5z"></path></svg>'), H1("RetailBox", style="margin:0; font-size:1.4rem; font-weight:800;"), style="display:flex; align-items:center; justify-content:center; gap:8px;"),
            Div(H1("Générez et Transformez en un clic", cls="hero-title"), style="text-align:center; margin-top:1rem;"),
            Div(Nav(Div(*[A(Safe(f'<i data-lucide="{icon}" style="width:18px"></i> {name}'), href=url, cls="active" if active_page == name else "") for name, url, icon in nav_items], cls="nav-pills")), cls="nav-scroll-container")
        ),
        Div(P("Annonce AdSense", style="font-size:0.6rem; opacity:0.4; margin:0"), cls="top-ad-banner"),
        Div(Section(content), Aside(Div(P("Publicité", style="font-size:0.6rem; opacity:0.4"), cls="sidebar-ad"), cls="sidebar"), cls="app-grid"),
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
        Card(Div(Safe('<i data-lucide="qr-code" style="width:32px; color:var(--primary);"></i>')), H3("Générer QR Code"), P("Format HD pro avec logo."), Footer(A(Button("Ouvrir l'outil"), href="/qr-tab")), cls="modern-card"),
        Card(Div(Safe('<i data-lucide="barcode" style="width:32px; color:var(--primary);"></i>')), H3("Générer Barcode"), P("EAN-13 et Code 128 standards."), Footer(A(Button("Ouvrir l'outil"), href="/barcode-tab")), cls="modern-card"),
        Card(Div(Safe('<i data-lucide="image" style="width:32px; color:var(--primary);"></i>')), H3("Détourer Image"), P("Suppression fond par IA."), Footer(A(Button("Ouvrir l'outil"), href="/rembg-tab")), cls="modern-card"),
    )
    return Layout(Div(cards, SeoContent()), "Accueil")

@rt("/ugc") # NOUVELLE ROUTE UGC
def get(): 
    content = Div(
        H2("Propriété des Contenus (UGC)"),
        P("Chez RetailBox, nous croyons en la propriété totale des utilisateurs sur leur travail."),
        H4("1. Propriété des fichiers"),
        P("Tout contenu généré (User Generated Content) via nos outils de QR Code, Barcode ou détourage d'image appartient exclusivement à l'utilisateur qui l'a créé. RetailBox ne revendique aucun droit d'auteur sur vos fichiers."),
        H4("2. Absence de stockage"),
        P("Nous ne conservons aucune copie de vos créations. Une fois le fichier téléchargé et votre session terminée, les données sont définitivement effacées de notre mémoire vive."),
        cls="modern-card"
    )
    return Layout(content, "Droits UGC")

@rt("/terms")
def get(): return Layout(Div(H2("Conditions"), P("Service gratuit sans garantie. Usage professionnel autorisé."), cls="modern-card"), "Conditions")
@rt("/privacy")
def get(): return Layout(Div(H2("Vie Privée"), P("Aucune image ou donnée n'est stockée sur nos serveurs."), cls="modern-card"), "Confidentialité")
@rt("/contact")
def get(): return Layout(Div(H2("Contact"), P("Email: utilitybox.project@gmail.com"), cls="modern-card"), "Contact")

@rt("/qr-tab")
def get():
    content = Div(H2("Générateur QR Code"), Form(Select(Option("URL", value="url"), Option("Fiche Clé:Valeur", value="kv"), name="qr_type", hx_get="/qr-fields", hx_target="#qr-f", hx_trigger="load, change"), Div(id="qr-f"), Grid(Label("Code", Input(type="color", name="fill_color", value="#000000")), Label("Fond", Input(type="color", name="back_color", value="#ffffff"))), Label("Logo", Input(type="file", name="logo", accept="image/*")), Button("Générer le QR Code"), hx_post="/generate-qrcode", hx_target="#qr-out", enctype="multipart/form-data"), Div(id="qr-out"), cls="modern-card")
    return Layout(content, "QR Code")

@rt("/qr-fields")
def get(qr_type:str):
    if qr_type == "url": return Input(name="url", placeholder="Lien https://...", required=True)
    return Div(Div(Input(name="qr_keys", placeholder="Clé"), Input(name="qr_values", placeholder="Valeur"), cls="key-value-row", id="qr-kv-list", style="display:grid; grid-template-columns: 1fr 1fr 40px; gap:8px;"), Button("+ Ligne", type="button", hx_get="/qr-add-row", hx_target="#qr-kv-list", hx_swap="afterend", cls="outline secondary"))

@rt("/qr-add-row")
def get(): return Div(Input(name="qr_keys", placeholder="Clé"), Input(name="qr_values", placeholder="Valeur"), Button("X", type="button", onclick="this.parentElement.remove()", cls="outline"), cls="key-value-row", style="display:grid; grid-template-columns: 1fr 1fr 40px; gap:8px; margin-top:8px;")

@rt("/barcode-tab")
def get():
    types = [("code128", "Code 128"), ("ean13", "EAN-13"), ("upca", "UPC-A")]
    content = Div(H2("Générateur de Barcode"), Form(Select(*[Option(l, value=v) for v, l in types], name="barcode_type", hx_get="/bc-fields", hx_target="#bc-f", hx_trigger="load, change"), Div(id="bc-f"), Button("Générer le Code"), hx_post="/generate-barcode", hx_target="#bc-out"), Div(id="bc-out"), cls="modern-card")
    return Layout(content, "Barcode")

@rt("/bc-fields")
def get(barcode_type:str): return Input(name="data", placeholder="Saisie données", required=True)

@rt("/rembg-tab")
def get():
    content = Div(H2("IA Suppression fond"), Form(Input(type="file", name="image", accept="image/*", required=True), Button("Détourer l'image"), hx_post="/remove-background", hx_target="#bg-out", hx_indicator="#load", enctype="multipart/form-data"), Div(id="load", cls="htmx-indicator", aria_busy="true"), Div(id="bg-out"), cls="modern-card")
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
    buf = BytesIO(); img.save(buf, format="PNG"); s = base64.b64encode(buf.getvalue()).decode()
    return Div(Img(src=f"data:image/png;base64,{s}", style="max-width:250px; margin:auto;"), Br(), A(Button("⬇️ Télécharger"), href=f"data:image/png;base64,{s}", download="qrcode.png"), cls="output-box")

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))