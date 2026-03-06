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

# --- SEO & META TAGS (Pivote vers RetailBox) ---
meta_tags = (
    Meta(name="description", content="RetailBox - Outils pro pour e-commerçants : Générateur de QR Code, Code-barres pour stocks et détourage photo produit par IA. Gérez vos ventes facilement."),
    Meta(name="keywords", content="E-commerce, Vendeur, Gestion de stock, Barcode EAN13, Photo produit, Détourage IA, QR Code Restaurant, Shopify, Vinted, Retail"),
    Meta(property="og:title", content="RetailBox | Outils E-commerce & Logistique"),
    Meta(property="og:description", content="Optimisez vos fiches produits et gérez vos stocks avec nos outils premium gratuits."),
    Meta(property="og:type", content="website"),
    Meta(name="viewport", content="width=device-width, initial-scale=1, maximum-scale=1")
)

# --- DESIGN SPLENDIDE & RESPONSIVE ---
custom_style = Style(f"""
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
    
    :root {{
        --pico-font-family: 'Plus Jakarta Sans', sans-serif;
        --primary: #4f46e5;
        --secondary: #9333ea;
        --glass: rgba(255, 255, 255, 0.75);
    }}

    body {{
        margin: 0; padding: 0;
        background-color: #f8fafc;
        background-image: 
            radial-gradient(at 0% 0%, rgba(79, 70, 229, 0.1) 0px, transparent 50%),
            radial-gradient(at 100% 0%, rgba(147, 51, 234, 0.1) 0px, transparent 50%);
        background-attachment: fixed;
        min-height: 100vh;
        overflow-x: hidden;
    }}

    .hero-title {{
        font-size: clamp(1.8rem, 8vw, 3.2rem);
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }}

    /* --- NAVIGATION MOBILE SCROLLABLE --- */
    .nav-scroll-container {{
        width: 100%; overflow-x: auto; -webkit-overflow-scrolling: touch;
        padding: 10px 0; margin: 1rem 0;
    }}
    .nav-pills {{
        display: flex; gap: 0.8rem; justify-content: center;
        min-width: max-content; padding: 0 1rem;
    }}
    @media (max-width: 600px) {{ .nav-pills {{ justify-content: flex-start; }} }}

    /* --- BOUTONS COHÉRENTS --- */
    .nav-pills a, button:not(.secondary), .btn-download {{
        padding: 0.7rem 1.4rem !important;
        border-radius: 16px !important;
        background: white !important;
        color: #475569 !important;
        font-weight: 700 !important;
        border: 1px solid #e2e8f0 !important;
        transition: all 0.3s ease !important;
        display: inline-flex; align-items: center; gap: 8px;
        white-space: nowrap; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        cursor: pointer;
    }}

    .nav-pills a.active, button:not(.secondary):hover, .btn-download:hover {{
        background: var(--primary) !important;
        color: white !important; border-color: var(--primary) !important;
        box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.3) !important;
        transform: translateY(-2px);
    }}

    /* --- PUBLICITÉS --- */
    .top-ad-banner {{
        max-width: 1200px; margin: 0 auto 2rem auto;
        min-height: 90px; background: rgba(0,0,0,0.02);
        border: 1px dashed #cbd5e1; border-radius: 16px;
        display: flex; align-items: center; justify-content: center;
    }}

    .sidebar-ad {{
        position: sticky; top: 2rem; min-height: 250px;
        background: rgba(0,0,0,0.02); border: 2px dashed #cbd5e1;
        border-radius: 24px; display: flex; align-items: center; justify-content: center;
    }}

    /* --- LAYOUT GRID --- */
    .app-grid {{
        display: grid; grid-template-columns: 1fr 320px; gap: 2rem;
        max-width: 1200px; margin: auto; padding: 0 1rem;
    }}
    @media (max-width: 1024px) {{ .app-grid {{ grid-template-columns: 1fr; }} }}

    .modern-card {{
        background: var(--glass); backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.5);
        padding: clamp(1.2rem, 5vw, 2.5rem); border-radius: 24px;
    }}

    footer.pro-footer {{ background: rgba(255,255,255,0.4); border-top: 1px solid #e2e8f0; padding: 3rem 1rem; margin-top: 4rem; }}
    .footer-content {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; }}
    .legal-links {{ display: flex; flex-wrap: wrap; gap: 15px; justify-content: center; margin-top: 2rem; font-size: 0.8rem; }}
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

# --- COMPOSANTS ---

def Logo():
    return Div(
        Safe(f"""<svg width="35" height="35" viewBox="0 0 24 24" fill="none" stroke="url(#grad)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <defs><linearGradient id="grad" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" style="stop-color:#4f46e5" /><stop offset="100%" style="stop-color:#9333ea" /></linearGradient></defs>
            <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
            <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
            <line x1="12" y1="22.08" x2="12" y2="12"></line>
        </svg>"""),
        H1("RetailBox", style="margin:0; font-size: 1.5rem; font-weight: 800;"),
        style="display:flex; align-items:center; justify-content:center; gap:10px; margin-bottom:1rem;"
    )

def Layout(content, active_page, title="RetailBox"):
    nav_items = [("Accueil", "/", "home"), ("QR Code", "/qr-tab", "qr-code"), ("Barcode", "/barcode-tab", "barcode"), ("RemBg", "/rembg-tab", "image")]
    return Title(f"{active_page} | {title}"), Main(
        Header(
            Logo(),
            Div(H1("Générez, Créez et Transformez en un clic", cls="hero-title"), 
                P("La boîte à outils indispensable pour les vendeurs et e-commerçants.", style="text-align:center; padding:0 1rem;"), 
                style="text-align:center"),
            Div(
                Nav(Div(*[A(Safe(f'<i data-lucide="{icon}" style="width:18px"></i> {name}'), href=url, cls="active" if active_page == name else "") for name, url, icon in nav_items], cls="nav-pills")),
                cls="nav-scroll-container"
            )
        ),
        # --- NOUVELLE BANNIÈRE PUB TOP ---
        Div(P("Espace Publicitaire Premium", style="font-size:0.6rem; opacity:0.5; margin:0"), cls="top-ad-banner"),
        
        Div(
            Section(content, cls="main-content"),
            Aside(Div(P("Publicité", style="font-size:0.6rem; opacity:0.5"), cls="sidebar-ad"), cls="sidebar"),
            cls="app-grid"
        ),
        FooterSection(),
        Script("lucide.createIcons();"),
        cls="container"
    )

def SeoContent():
    return Section(
        Div(
            H2("Optimisez votre activité commerciale et vos ventes en ligne", style="margin-top:2rem; font-size: 2rem;"),
            P("RetailBox est la suite d'outils digitaux conçue pour les entrepreneurs et e-commerçants. Simplifiez votre logistique et améliorez vos fiches produits."),
            Grid(
                Div(H4("📸 Photos Produits"), P("Boostez vos ventes sur Shopify ou Vinted. Notre IA de détourage supprime l'arrière-plan de vos photos pour un rendu studio.")),
                Div(H4("📦 Gestion de Stock"), P("Générez des codes-barres EAN-13 conformes pour vos étiquetages de produits et votre logistique interne.")),
                Div(H4("🔗 Marketing QR"), P("Créez des QR Codes haute résolution avec logo pour lier vos fiches produits ou vos menus digitaux."))
            ),
            cls="modern-card", style="margin-top:2rem; line-height:1.7;"
        )
    )

# --- ROUTES ---

@rt("/ads.txt")
def get():
    return PlainTextResponse("google.com, pub-4081303157053373, DIRECT, f08c47fec0942fa0")

@rt("/")
def get():
    cards = Grid(
        Card(Div(Safe('<i data-lucide="qr-code" style="width:40px; height:40px; color:var(--primary);"></i>')), H3("Générer QR Code"), P("Codes QR HD avec logo pour produits et liens."), Footer(A(Button("Lancer"), href="/qr-tab")), cls="modern-card", style="text-align:center"),
        Card(Div(Safe('<i data-lucide="barcode" style="width:40px; height:40px; color:var(--primary);"></i>')), H3("Générer Barcode"), P("Formats EAN-13 et Code 128 pour vos étiquettes."), Footer(A(Button("Lancer"), href="/barcode-tab")), cls="modern-card", style="text-align:center"),
        Card(Div(Safe('<i data-lucide="image" style="width:40px; height:40px; color:var(--primary);"></i>')), H3("Détourer Photo"), P("Enlevez le fond de vos articles gratuitement via IA."), Footer(A(Button("Lancer"), href="/rembg-tab")), cls="modern-card", style="text-align:center"),
    )
    return Layout(Div(cards, SeoContent()), "Accueil")

@rt("/qr-tab")
def get():
    content = Div(
        H2("Générateur QR Code"),
        Form(
            Select(Option("Lien URL Simple", value="url"), Option("Fiche Produit (Clé:Valeur)", value="kv"), name="qr_type", hx_get="/qr-fields", hx_target="#qr-f", hx_trigger="load, change"),
            Div(id="qr-f"),
            Grid(Label("Code", Input(type="color", name="fill_color", value="#4f46e5")), Label("Fond", Input(type="color", name="back_color", value="#ffffff"))),
            Label("Logo de marque", Input(type="file", name="logo", accept="image/*")),
            Button("🚀 Générer"), hx_post="/generate-qrcode", hx_target="#qr-out", enctype="multipart/form-data"
        ),
        Div(id="qr-out"), cls="modern-card"
    )
    return Layout(content, "QR Code")

@rt("/qr-fields")
def get(qr_type:str):
    if qr_type == "url": return Input(name="url", placeholder="https://votre-boutique.com/produit", required=True)
    return Div(Div(Input(name="qr_keys", placeholder="Ex: Prix"), Input(name="qr_values", placeholder="Ex: 19.99€"), cls="key-value-row", id="qr-kv-list", style="display:grid; grid-template-columns: 1fr 1fr 40px; gap:8px;"), 
               Button("+ Ajouter une ligne", type="button", hx_get="/qr-add-row", hx_target="#qr-kv-list", hx_swap="afterend", cls="outline secondary", style="width:100%"))

@rt("/qr-add-row")
def get(): return Div(Input(name="qr_keys", placeholder="Clé"), Input(name="qr_values", placeholder="Valeur"), Button("X", type="button", onclick="this.parentElement.remove()", cls="outline"), cls="key-value-row", style="display:grid; grid-template-columns: 1fr 1fr 40px; gap:8px; margin-top:10px;")

@rt("/barcode-tab")
def get():
    types = [("code128", "Code 128 (Logistique)"), ("ean13", "EAN-13 (Commerce)"), ("upca", "UPC-A")]
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
    req = "Numéros uniquement" if barcode_type in ["ean13", "upca"] else "Texte ou chiffres"
    return Input(name="data", placeholder=req, required=True)

@rt("/rembg-tab")
def get():
    content = Div(
        H2("IA Background Remover"),
        Form(Label("Image du produit", Input(type="file", name="image", accept="image/*", required=True)), Button("Supprimer le fond"), hx_post="/remove-background", hx_target="#bg-out", hx_indicator="#load", enctype="multipart/form-data"),
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
    return Div(Img(src=f"data:image/png;base64,{s}", style="max-width:250px; margin:auto;"), Br(), A(Button("⬇️ Télécharger PNG"), href=f"data:image/png;base64,{s}", download="qrcode.png"), cls="output-box")

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

# --- PAGES LÉGALES & FOOTER ---
def FooterSection():
    return Footer(
        Div(
            Div(H4("📜 Conditions"), P("Usage gratuit pour les e-commerçants. Nous ne sommes pas responsables des erreurs logistiques."), cls="footer-section"),
            Div(H4("👤 UGC & Privacy"), P("Vos photos produits ne sont jamais stockées. Vous restez propriétaire des codes générés."), cls="footer-section"),
            Div(H4("🛡️ Sécurité"), P("Traitement sécurisé en mémoire vive (RAM). Suppression instantanée."), cls="footer-section"),
            cls="footer-content"
        ),
        Div(
            A("Conditions", href="/terms"), A("Confidentialité", href="/privacy"), A("Contact", href="/contact"),
            Span(f"© {CURRENT_YEAR} RetailBox"),
            cls="legal-links"
        ),
        cls="pro-footer"
    )

@rt("/terms")
def get(): return Layout(Div(H2("Conditions de RetailBox"), P("Usage gratuit pour tout commerçant. Aucune garantie sur la lecture des codes."), cls="modern-card"), "Conditions")
@rt("/privacy")
def get(): return Layout(Div(H2("Vie Privée"), P("Aucun stockage de photos ou de données commerciales."), cls="modern-card"), "Confidentialité")
@rt("/contact")
def get(): return Layout(Div(H2("Contactez RetailBox"), P("Support: utilitybox.project@gmail.com"), cls="modern-card"), "Contact")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))