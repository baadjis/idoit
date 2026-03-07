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
    Meta(name="description", content="Générateur gratuit de QR Codes HD, création de codes-barres EAN13 et détourage photo par IA. Solution gratuite pour commerçants."),
    Meta(name="keywords", content="Générer QR Code gratuit, Créer Barcode en ligne, EAN13, Code 128, Enlever fond image gratuit, PNG transparent, RetailBox"),
    Meta(property="og:title", content="RetailBox | Outils QR et Barcode Gratuit"),
    Meta(name="viewport", content="width=device-width, initial-scale=1, maximum-scale=1"),
)

# --- STYLE COMPLET ET ADAPTATIF (LIGHT/DARK) ---
custom_style = Style(f"""
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    :root {{
        --pico-font-family: 'Plus Jakarta Sans', sans-serif;
        --primary: #4f46e5;
        --secondary: #9333ea;
        --pico-color: #1e293b;
        --pico-background-color: #ffffff;
    }}

    /* ADAPTATION AUTOMATIQUE AU MODE SOMBRE */
    @media (prefers-color-scheme: dark) {{
        :root {{
            --pico-color: #f8fafc !important;
            --pico-background-color: #0f172a !important;
        }}
        body {{ background-color: #0f172a !important; color: #f8fafc !important; }}
        .modern-card {{ background: #1e293b !important; border-color: #334155 !important; color: #f8fafc !important; }}
        p, h4, li, span {{ color: #cbd5e1 !important; }}
        .nav-pills a, button {{ background: #334155 !important; color: white !important; border-color: #475569 !important; }}
    }}

    body {{
        margin: 0; padding: 0;
        background-image: radial-gradient(at 0% 0%, rgba(79, 70, 229, 0.08) 0px, transparent 50%);
        background-attachment: fixed; min-height: 100vh;
    }}

    /* Suppression des traits sous les liens */
    a {{ text-decoration: none !important; color: inherit; border: none !important; }}

    /* GRADIENT POUR BRAND ET TITRES */
    .gradient-text {{
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }}

    .hero-title {{
        font-size: clamp(1.8rem, 8vw, 3rem);
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 1rem;
    }}

    /* ALIGNEMENT ICONE + TITRE DANS LES CARTES */
    .card-header-flex {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 1rem;
    }}

    /* BOUTONS ET NAVIGATION */
    .nav-pills a, button, .btn-download {{
        padding: 0.7rem 1.4rem !important; border-radius: 12px !important;
        background: #ffffff; color: #1e293b;
        font-weight: 700 !important; border: 1px solid #e2e8f0;
        display: inline-flex; align-items: center; justify-content: center;
        cursor: pointer; transition: 0.2s;
    }}

    .nav-pills a.active, button:not(.secondary):hover, .btn-download:hover {{
        background: var(--primary) !important; color: #ffffff !important;
        border-color: var(--primary) !important;
    }}

    /* CARTES ET BOUTONS LARGEUR TOTALE */
    .modern-card {{
        background: #ffffff; border: 1px solid #e2e8f0;
        padding: 1.5rem; border-radius: 20px;
        height: 100%; display: flex; flex-direction: column;
    }}
    .modern-card footer {{
        background: transparent !important; border-top: 1px solid #e2e8f0;
        padding: 1rem 0 0 0 !important; margin-top: auto !important;
    }}
    .modern-card footer a {{ width: 100%; }}
    .modern-card footer button {{ width: 100% !important; }}

    .nav-scroll-container {{ width: 100%; overflow-x: auto; padding: 10px 0; }}
    .nav-pills {{ display: flex; gap: 0.6rem; min-width: max-content; }}

    .app-grid {{
        display: grid; grid-template-columns: 1fr 320px; gap: 2rem;
        max-width: 1200px; margin: auto; padding: 0 1rem;
    }}
    @media (max-width: 1024px) {{ .app-grid {{ grid-template-columns: 1fr; }} }}

    /* ESPACES PUB */
    .top-ad-banner {{
        width: 100%; max-width: 1100px; margin: 1rem auto;
        min-height: 90px; background: rgba(0,0,0,0.02); border: 1px dashed #cbd5e1;
        border-radius: 12px; display: flex; align-items: center; justify-content: center;
    }}
    .sidebar-ad {{
        background: rgba(0,0,0,0.02); border: 1px dashed #cbd5e1; border-radius: 20px;
        min-height: 300px; display: flex; align-items: center; justify-content: center;
    }}

    footer.pro-footer {{ border-top: 1px solid #e2e8f0; padding: 3rem 1rem; margin-top: 5rem; }}
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

# --- COMPOSANTS ---

def Logo():
    return Div(
        Safe(f'<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="url(#grad)" stroke-width="3"><defs><linearGradient id="grad"><stop offset="0%" stop-color="#4f46e5"/><stop offset="100%" stop-color="#9333ea"/></linearGradient></defs><path d="M21 16V8l-9-5-9 5v8l9 5 9-5z"></path></svg>'),
        H1("RetailBox", cls="gradient-text", style="margin:0; font-size:1.4rem; font-weight:800;"),
        style="display:flex; align-items:center; justify-content:center; gap:8px;"
    )

def SeoKeywords():
    """Section dédiée aux moteurs de recherche (Google)"""
    return Section(
        Div(
            H2("Générer gratuitement vos outils de vente en ligne"),
            P("Vous cherchez comment créer des étiquettes produits ? RetailBox vous permet de générer facilement des QR codes gratuits et des codes-barres EAN-13 standards. Notre service inclut également un outil pour enlever le fond d'une image gratuitement grâce à une IA haute précision."),
            Ul(
                Li("Générer QR Code pour menu restaurant ou lien boutique."),
                Li("Créer des codes-barres EAN-13 et Code 128 pour inventaire."),
                Li("Détourage photo produit automatique pour Vinted, Shopify et Amazon."),
                Li("Fichiers PNG haute définition prêts pour l'impression pro.")
            ),
            cls="modern-card", style="margin-top:3rem; border-style: dashed;"
        )
    )

def FooterSection():
    return Footer(
        Div(
            Div(H4("Technique"), P("Outils de génération en mémoire vive."), cls="footer-section"),
            Div(H4("Vie Privée"), P("Aucun stockage de vos données."), cls="footer-section"),
            Div(H4("Propriété"), P("Vous détenez les droits sur vos fichiers."), cls="footer-section"),
            cls="footer-content", style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:2rem; max-width:1200px; margin:auto;"
        ),
        Div(
            A("Conditions", href="/terms"), A("Vie Privée", href="/privacy"), A("UGC", href="/ugc"), A("Contact", href="/contact"),
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
            Div(H1("Générez et Transformez en un clic", cls="hero-title gradient-text"), style="text-align:center; margin-top:1rem;"),
            Div(Nav(Div(*[A(Safe(f'<i data-lucide="{icon}" style="width:18px"></i> {name}'), href=url, cls="active" if active_page == name else "") for name, url, icon in nav_items], cls="nav-pills")), cls="nav-scroll-container")
        ),
        Div(P("Annonce Partenaire", style="font-size:0.6rem; opacity:0.5; margin:0"), cls="top-ad-banner"),
        Div(Section(content), Aside(Div(P("Publicité", style="font-size:0.6rem; opacity:0.5"), cls="sidebar-ad"), cls="sidebar"), cls="app-grid"),
        SeoKeywords(),
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
        Card(
            Div(Safe('<i data-lucide="qr-code" style="width:28px; color:var(--primary);"></i>'), H3("QR Code", style="margin:0;"), cls="card-header-flex"),
            P("Instructions : Saisissez votre lien, choisissez vos couleurs et téléchargez votre code HD."),
            Footer(A(Button("Ouvrir l'outil"), href="/qr-tab")), cls="modern-card"
        ),
        Card(
            Div(Safe('<i data-lucide="barcode" style="width:28px; color:var(--primary);"></i>'), H3("Barcode", style="margin:0;"), cls="card-header-flex"),
            P("Instructions : Entrez vos 12 chiffres EAN-13 pour créer vos étiquettes de stock."),
            Footer(A(Button("Ouvrir l'outil"), href="/barcode-tab")), cls="modern-card"
        ),
        Card(
            Div(Safe('<i data-lucide="image" style="width:28px; color:var(--primary);"></i>'), H3("RemBg", style="margin:0;"), cls="card-header-flex"),
            P("Instructions : Importez une photo. L'IA supprime le fond pour créer un PNG transparent."),
            Footer(A(Button("Ouvrir l'outil"), href="/rembg-tab")), cls="modern-card"
        ),
    )
    return Layout(cards, "Accueil")

# --- PAGES LÉGALES ---
@rt("/ugc")
def get(): return Layout(Div(H2("Droits UGC"), P("Les fichiers générés sur ce site appartiennent à 100% à l'utilisateur."), cls="modern-card"), "UGC")
@rt("/terms")
def get(): return Layout(Div(H2("Conditions"), P("Service de génération gratuit pour usage pro."), cls="modern-card"), "Conditions")
@rt("/privacy")
def get(): return Layout(Div(H2("Vie Privée"), P("Aucun stockage d'images sur nos serveurs."), cls="modern-card"), "Confidentialité")
@rt("/contact")
def get(): return Layout(Div(H2("Contact"), P("Support : utilitybox.project@gmail.com"), cls="modern-card"), "Contact")

# --- OUTILS (QR, BARCODE, REMBG) ---

@rt("/qr-tab")
def get():
    content = Div(
        H2("Générateur de QR Code"),
        P("Guide : Remplissez le champ URL ou texte, puis personnalisez le rendu visuel."),
        Form(
            Select(Option("URL", value="url"), Option("Fiche Données", value="kv"), name="qr_type", hx_get="/qr-fields", hx_target="#qr-f", hx_trigger="load, change"),
            Div(id="qr-f"),
            Grid(Label("Code", Input(type="color", name="fill_color", value="#000000")), Label("Fond", Input(type="color", name="back_color", value="#ffffff"))),
            Label("Logo", Input(type="file", name="logo", accept="image/*")),
            Button("🚀 Générer le QR Code"), hx_post="/generate-qrcode", hx_target="#qr-out", enctype="multipart/form-data"
        ),
        Div(id="qr-out"), cls="modern-card"
    )
    return Layout(content, "QR Code")

@rt("/qr-fields")
def get(qr_type:str):
    if qr_type == "url": return Input(name="url", placeholder="Lien https://...", required=True)
    return Div(Div(Input(name="qr_keys", placeholder="Clé"), Input(name="qr_values", placeholder="Valeur"), cls="key-value-row", id="qr-kv-list", style="display:grid; grid-template-columns: 1fr 1fr 40px; gap:8px;"), Button("+ Ligne", type="button", hx_get="/qr-add-row", hx_target="#qr-kv-list", hx_swap="afterend", cls="outline secondary"))

@rt("/qr-add-row")
def get(): return Div(Input(name="qr_keys", placeholder="Clé"), Input(name="qr_values", placeholder="Valeur"), Button("X", type="button", onclick="this.parentElement.remove()", cls="outline"), cls="key-value-row", style="display:grid; grid-template-columns: 1fr 1fr 40px; gap:8px; margin-top:8px;")

@rt("/barcode-tab")
def get():
    types = [("ean13", "EAN-13 (Produits)"), ("code128", "Code 128 (Logistique)")]
    content = Div(H2("Générateur de Barcode"), P("Guide : Entrez 12 chiffres pour l'EAN-13. Le système ajoute la clé de contrôle."), Form(Select(*[Option(l, value=v) for v, l in types], name="barcode_type", hx_get="/bc-fields", hx_target="#bc-f", hx_trigger="load, change"), Div(id="bc-f"), Button("Générer le Code"), hx_post="/generate-barcode", hx_target="#bc-out"), Div(id="bc-out"), cls="modern-card")
    return Layout(content, "Barcode")

@rt("/bc-fields")
def get(barcode_type:str): return Input(name="data", placeholder="Saisie des données", required=True)

@rt("/rembg-tab")
def get():
    content = Div(H2("Détourage IA"), P("Guide : Importez une photo, l'IA s'occupe de supprimer l'arrière-plan."), Form(Input(type="file", name="image", accept="image/*", required=True), Button("Détourer l'image"), hx_post="/remove-background", hx_target="#bg-out", hx_indicator="#load", enctype="multipart/form-data"), Div(id="load", cls="htmx-indicator", aria_busy="true"), Div(id="bg-out"), cls="modern-card")
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
    return Div(Img(src=f"data:image/png;base64,{s}", style="max-width:250px; margin:auto;"), Br(), A(Button("⬇️ Télécharger"), href=f"data:image/png;base64,{s}", download="qrcode.png"), cls="output-box", style="text-align:center; padding-top:1rem;")

@rt("/generate-barcode", methods=["POST"])
async def post_bc(barcode_type:str, data:str):
    try:
        bc = barcode.get_barcode_class(barcode_type)(data, writer=ImageWriter())
        buf = BytesIO(); bc.write(buf); s = base64.b64encode(buf.getvalue()).decode()
        return Div(Img(src=f"data:image/png;base64,{s}"), Br(), A(Button("⬇️ Télécharger"), href=f"data:image/png;base64,{s}", download="barcode.png"), cls="output-box", style="text-align:center; padding-top:1rem;")
    except Exception as e: return Div(f"Erreur format: {e}", style="color:red;")

@rt("/remove-background", methods=["POST"])
async def post_bg(image:UploadFile):
    res = remove(await image.read()); s = base64.b64encode(res).decode()
    return Div(Img(src=f"data:image/png;base64,{s}"), Br(), A(Button("⬇️ Télécharger"), href=f"data:image/png;base64,{s}", download="nobg.png"), cls="output-box", style="text-align:center; padding-top:1rem;")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))