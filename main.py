from fasthtml.common import *
from starlette.responses import PlainTextResponse
import qrcode
import base64
from io import BytesIO
from rembg import remove
import barcode
from barcode.writer import ImageWriter
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os

# --- CONFIGURATION ---
CURRENT_YEAR = datetime.now().year

adsense_script = Script(
    src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4081303157053373",
    async_=True,
    crossorigin="anonymous"
)

# --- TA LISTE DE SERVICES (SOURCE DE VÉRITÉ) ---
services = [
    ("users", "Identité Digitale", "Un seul QR pour regrouper Facebook, Instagram, TikTok, Spotify et plus.", "/digital-id"),
    ("qr-code", "QR Code Pro", "Lien personnalisé avec logo. Idéal pour menus restaurant PDF ou sites web.", "/qr-tab"),
    ("tag", "Étiquettes Soldes", "Prix barré + Barcode. Générez vos étiquettes promos prêtes à imprimer.", "/soldes"),
    ("barcode", "Barcode Expert", "Codes EAN-13 et Code 128 pro pour la gestion de vos stocks.", "/barcode-tab"),
    ("contact", "VCard Contact", "QR Code de contact. Vos clients enregistrent votre fiche d'un seul scan.", "/vcard"),
    ("message-circle", "QR WhatsApp", "Ouvrez une discussion directe avec vos clients via un lien QR.", "/whatsapp-qr"),
    ("image", "RemBg IA", "Suppression de fond par IA pour vos photos produits (Shopify, Vinted).", "/rembg-tab"),
    ("wifi", "Accès Wi-Fi", "Connexion automatique sécurisée pour vos clients sans mot de passe.", "/wifi-qr"),
]

# --- SEO & META TAGS ---
meta_tags = (
    Meta(name="description", content="RetailBox - Identité digitale, étiquettes de soldes prix barré, QR Codes menu restaurant et codes-barres EAN13 gratuits."),
    Meta(name="keywords", content="Identité digitale QR, QR Code menu restaurant PDF, étiquettes soldes, créer barcode ean13, détourage photo produit"),
    Meta(property="og:title", content="RetailBox | Votre Identité Digitale & Outils Commerce"),
    Meta(name="viewport", content="width=device-width, initial-scale=1, maximum-scale=1"),
    Meta(name="color-scheme", content="light")
)

# --- STYLE STABILISÉ & TYPOGRAPHIE ---
custom_style = Style(f"""
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    :root {{
        --pico-font-family: 'Plus Jakarta Sans', sans-serif;
        --primary: #4f46e5;
        --secondary: #9333ea;
        --pico-color: #1e293b;
        --pico-background-color: #ffffff;
    }}

    /* FIX DARK MODE IPHONE / ANDROID */
    @media (prefers-color-scheme: dark) {{
        :root {{ --pico-color: #f8fafc !important; --pico-background-color: #0f172a !important; }}
        body {{ background-color: #0f172a !important; color: #f8fafc !important; }}
        .modern-card {{ background: #1e293b !important; border-color: #334155 !important; color: #f8fafc !important; }}
        p, h2, h3, h4, li, span, label, summary, details {{ color: #f8fafc !important; }}
        .nav-pills a {{ background: #1e293b !important; color: white !important; }}
    }}

    body {{ margin: 0; padding: 0; background-image: radial-gradient(at 0% 0%, rgba(79, 70, 229, 0.05) 0px, transparent 50%); background-attachment: fixed; min-height: 100vh; }}
    a {{ text-decoration: none !important; border: none !important; color: inherit; }}

    .gradient-text {{ background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; display: inline-block; }}
    .hero-title {{ font-size: clamp(1.8rem, 8vw, 2.8rem); font-weight: 800; text-align: center; margin: 1.5rem 0; }}

    .nav-scroll-container {{ width: 100%; overflow-x: auto; padding: 10px 0; }}
    .nav-pills {{ display: flex; gap: 0.6rem; min-width: max-content; padding: 0 1rem; justify-content: center; }}
    .nav-pills a {{ padding: 0.6rem 1.2rem; border-radius: 12px; background: white; border: 1px solid #e2e8f0; font-weight: 700; color: #1e293b; }}
    .nav-pills a.active {{ background: var(--primary) !important; color: white !important; border-color: var(--primary); }}

    .services-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 350px), 1fr)); gap: 2rem; margin-top: 2rem; }}
    .modern-card {{ border: 1px solid #e2e8f0; padding: 2rem; border-radius: 24px; height: 100%; display: flex; flex-direction: column; background: #ffffff; transition: 0.3s ease; }}
    .modern-card:hover {{ transform: translateY(-6px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); }}
    .card-header-flex {{ display: flex; align-items: center; gap: 15px; margin-bottom: 1.2rem; }}
    .modern-card footer {{ background: transparent !important; border-top: 1px solid #e2e8f0; padding: 1.2rem 0 0 0 !important; margin-top: auto !important; }}

    button, .btn-full {{ width: 100% !important; padding: 0.9rem !important; border-radius: 14px !important; font-weight: 700 !important; border: 1px solid #e2e8f0; background: #f8fafc; color: #1e293b; cursor: pointer; transition: 0.3s; }}
    button:hover, .btn-full:hover {{ background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%) !important; color: white !important; border-color: transparent !important; }}

    /* FAQ ELEVATION */
    .faq-section {{ margin-top: 5rem; padding: 2rem; background: #ffffff; border-radius: 32px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.1); border: 1px solid #e2e8f0; }}
    @media (prefers-color-scheme: dark) {{ .faq-section {{ background: #1e293b !important; }} }}
    details {{ background: rgba(0,0,0,0.02); padding: 1.2rem; border-radius: 16px; margin-bottom: 1rem; }}
    summary {{ font-weight: 700; cursor: pointer; }}

    /* FOOTER GRADIENT */
    footer.pro-footer {{ background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%) !important; padding: 4rem 1rem; margin-top: 6rem; color: white !important; }}
    footer.pro-footer h4, footer.pro-footer p, footer.pro-footer a, footer.pro-footer span {{ color: white !important; }}
    .legal-links {{ display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; margin-top: 3rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.2); font-size: 0.9rem; }}

    .top-ad-banner {{ width: 100%; max-width: 1100px; margin: 1rem auto; min-height: 90px; background: rgba(0,0,0,0.02); border: 1px dashed #cbd5e1; border-radius: 16px; display: flex; align-items: center; justify-content: center; }}
    .app-grid {{ display: grid; grid-template-columns: 1fr 320px; gap: 2rem; max-width: 1200px; margin: auto; padding: 0 1rem; }}
    @media (max-width: 1024px) {{ .app-grid {{ grid-template-columns: 1fr; }} }}
""")

app, rt = fast_app(static_path='public', hdrs=(*meta_tags, Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"), custom_style, adsense_script, Script(src="https://unpkg.com/lucide@latest")))

# --- COMPOSANTS ---

def Logo():
    return Div(
        Safe(f'<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="url(#grad)" stroke-width="3"><defs><linearGradient id="grad"><stop offset="0%" stop-color="#4f46e5"/><stop offset="100%" stop-color="#9333ea"/></linearGradient></defs><path d="M21 16V8l-9-5-9 5v8l9 5 9-5z"></path></svg>'),
        H1("RetailBox", cls="gradient-text", style="margin:0; font-size:1.4rem;"), style="display:flex; align-items:center; justify-content:center; gap:8px;"
    )

def SeoInstructional():
    return Section(
        Div(
            H2("Guide complet : Comment générer vos services gratuitement"),
            # Première ligne : Identité et Contacts
            Grid(
                Div(
                    H4("🚀 QR Codes avec Logo"), 
                    P("Entrez votre URL ou le lien de votre menu restaurant PDF. Personnalisez les couleurs et ajoutez le logo de votre marque. Téléchargez un QR code haute résolution prêt pour l'impression.")
                ),
                Div(
                    H4("🌐 Identité Digitale"), 
                    P("Centralisez votre présence : regroupez Facebook, Instagram, TikTok et Shopify dans un seul QR Code 'Social Card' unique pour faciliter l'accès à vos abonnés.")
                ),
                Div(
                    H4("👤 VCard : Carte de Visite"), 
                    P("Créez une carte de visite digitale. Saisissez vos coordonnées pro (nom, tel, email). Le QR généré permet à vos clients d'enregistrer votre contact d'un simple scan.")
                ),
                Div(
                    H4("💬 QR WhatsApp Direct"), 
                    P("Boostez vos commandes : générez un lien QR qui ouvre instantanément une discussion WhatsApp avec un message pré-rempli pour votre boutique ou service client.")
                ),
            ),
            # Deuxième ligne : Commerce et Technique
            Grid(
                Div(
                    H4("🏷️ Étiquettes de Soldes"), 
                    P("Générez vos étiquettes de prix : indiquez le prix d'origine et le prix remisé. L'outil crée un visuel pro avec prix barré et code-barres conforme pour vos rayons.")
                ),
                Div(
                    H4("🔢 Barcode EAN-13 & 128"), 
                    P("Gérez vos stocks facilement. Saisissez vos chiffres pour générer des codes-barres standards (EAN-13 commerce ou Code 128 logistique) lisibles par tous les scanners laser.")
                ),
                Div(
                    H4("🖼️ Détourage IA de Produit"), 
                    P("Optimisez vos photos : importez vos fichiers JPG/PNG. Notre Intelligence Artificielle supprime l'arrière-plan automatiquement pour créer des PNG transparents qualité studio.")
                ),
                Div(
                    H4("📶 QR Code Accès Wi-Fi"), 
                    P("Service client premium : entrez le nom de votre réseau et le mot de passe pour générer un code de connexion automatique sécurisée sans aucune saisie manuelle.")
                ),
            ),
            cls="modern-card", 
            style="margin-top:4rem; border-style: solid; border-width: 2px; border-color: var(--primary);"
        )
    )

def FaqSection():
    return Section(
        Div(
            H2("Questions fréquentes sur RetailBox"),
            Details(Summary("Comment générer un QR code pour mon menu restaurant PDF ?"), P("Utilisez notre outil 'QR Pro', collez le lien de votre PDF hébergé et téléchargez votre QR haute définition.")),
            Details(Summary("Le générateur d'étiquettes de soldes est-il gratuit ?"), P("Oui, vous pouvez créer gratuitement des étiquettes prix barrés avec codes-barres pour vos rayons.")),
            Details(Summary("Puis-je regrouper mes réseaux sociaux dans un seul QR ?"), P("Absolument. Notre service d'Identité Digitale regroupe TikTok, Instagram et Facebook dans une Social Card unique.")),
            cls="faq-section"
        )
    )

def Layout(content, active_page, title="RetailBox"):
    nav_items = [("Accueil", "/", "home"), ("QR Pro", "/qr-tab", "qr-code"), ("VCard", "/vcard", "contact"), ("Soldes", "/soldes", "tag"), ("RemBg", "/rembg-tab", "image")]
    return Title(f"{active_page} | {title}"), Main(
        Header(
            Logo(),
            Div(H1("Générez et Transformez en un clic", cls="hero-title gradient-text"), style="text-align:center;"),
            Div(Nav(Div(*[A(Safe(f'<i data-lucide="{icon}" style="width:18px"></i> {name}'), href=url, cls="active" if active_page == name else "") for name, url, icon in nav_items], cls="nav-pills")), cls="nav-scroll-container")
        ),
        Div(P("Publicité", style="font-size:0.6rem; opacity:0.5; margin:0"), cls="top-ad-banner"),
        Div(Section(content), Aside(Div(P("Publicité"), style="background:rgba(0,0,0,0.02); border:1px dashed #ccc; border-radius:20px; height:600px; display:flex; align-items:center; justify-content:center; position:sticky; top:20px;"), cls="sidebar"), cls="app-grid"),
        SeoInstructional(), FaqSection(),
        Footer(Div(Div(H4("Usage"), P("Génération gratuite en mémoire vive."), cls="footer-section"), Div(H4("Confidentialité"), P("Zéro stockage sur serveurs."), cls="footer-section"), Div(H4("Propriété"), P("100% droits UGC (User Generated Content)."), cls="footer-section"), cls="footer-content"), Div(A("Conditions", href="/terms"), A("Vie Privée", href="/privacy"), A("UGC", href="/ugc"), A("Contact", href="/contact"), Span(f"© {CURRENT_YEAR} RetailBox"), cls="legal-links"), cls="pro-footer"),
        Script("lucide.createIcons();"), cls="container"
    )

def generate_qr_response(data, filename):
    qr = qrcode.QRCode(version=1, box_size=10, border=4); qr.add_data(data); qr.make(fit=True); img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO(); img.save(buf, format="PNG"); s = base64.b64encode(buf.getvalue()).decode()
    return Div(Img(src=f"data:image/png;base64,{s}", style="max-width:250px; margin: 1.5rem auto; border: 2px solid #f1f5f9; border-radius: 16px; display: block;"), A(Button("⬇️ Télécharger l'image PNG", cls="btn-full"), href=f"data:image/png;base64,{s}", download=filename), style="text-align:center; padding: 1.5rem; background: rgba(0,0,0,0.02); border-radius: 24px; margin-top: 2rem; border: 1px solid #e2e8f0;")

def DataRow(prefix):
    return Div(Input(name=f"{prefix}_keys", placeholder="Nom (ex: TikTok)"), Input(name=f"{prefix}_vals", placeholder="Lien URL"), Button(Safe('<i data-lucide="trash-2"></i>'), type="button", onclick="this.parentElement.remove()", style="width:40px; background:transparent !important; border:none;"), cls="key-value-row", style="display:grid; grid-template-columns: 1fr 1fr 40px; gap:8px; margin-top:10px;")

# --- ROUTES ACCUEIL ---

@rt("/")
def get():
    cards = Div(*[Card(
        Div(Safe(f'<i data-lucide="{s[0]}" style="width:28px; color:var(--primary);"></i>'), H3(s[1], style="margin:0; font-size:1.1rem;"), cls="card-header-flex"),
        P(s[2], style="font-size:0.9rem;"),
        Footer(A(Button("Ouvrir l'outil", cls="btn-full"), href=s[3])), cls="modern-card"
    ) for s in services], cls="services-grid")
    return Layout(cards, "Accueil")

# --- OUTILS ---

@rt("/digital-id")
def get():
    content = Div(H2("Votre Identité Digitale"), P("Regroupez vos réseaux sociaux dans un seul QR Code."), Form(Grid(Input(name="fb", placeholder="Facebook"), Input(name="ig", placeholder="Instagram")), Grid(Input(name="tk", placeholder="TikTok"), Input(name="sp", placeholder="Spotify")), Div(id="soc-kv"), Button("+ Autre réseau (X, Shop...)", type="button", hx_get="/add-soc", hx_target="#soc-kv", hx_swap="beforeend", cls="outline"), Button("🚀 Générer ma Social Card"), hx_post="/gen-id", hx_target="#o"), Div(id="o"), cls="modern-card")
    return Layout(content, "Accueil")

@rt("/add-soc")
def get(): return DataRow("extra")

@rt("/gen-id", methods=["POST"])
async def post(fb:str="", ig:str="", tk:str="", sp:str="", extra_keys:list=None, extra_vals:list=None):
    d = [f"FB: {fb}", f"IG: {ig}", f"TK: {tk}", f"SP: {sp}"]
    if extra_keys:
        k_list = [extra_keys] if isinstance(extra_keys, str) else extra_keys
        v_list = [extra_vals] if isinstance(extra_vals, str) else extra_vals
        d += [f"{k}: {v}" for k,v in zip(k_list, v_list) if k.strip()]
    return generate_qr_response("\n".join(d), "social.png")

@rt("/vcard")
def get():
    content = Div(H2("Carte VCard"), Form(Grid(Input(name="fn", placeholder="Prénom"), Input(name="ln", placeholder="Nom")), Input(name="tel", placeholder="Tel"), Button("Générer"), hx_post="/gen-vcard", hx_target="#o"), Div(id="o"), cls="modern-card")
    return Layout(content, "VCard")

@rt("/gen-vcard", methods=["POST"])
async def post(fn:str, ln:str, tel:str): return generate_qr_response(f"BEGIN:VCARD\nFN:{fn} {ln}\nTEL:{tel}\nEND:VCARD", "contact.png")

@rt("/whatsapp-qr")
def get():
    content = Div(H2("QR WhatsApp"), Form(Input(name="n", placeholder="Numéro"), Button("Générer"), hx_post="/gen-wa", hx_target="#o"), Div(id="o"), cls="modern-card")
    return Layout(content, "Accueil")

@rt("/gen-wa", methods=["POST"])
async def post(n:str): return generate_qr_response(f"https://wa.me/{n}", "wa.png")

@rt("/soldes")
def get():
    content = Div(H2("Étiquettes Soldes"), Form(Input(name="item", placeholder="Produit"), Grid(Input(name="old_p", placeholder="Ancien Prix"), Input(name="new_p", placeholder="Prix Soldé")), Input(name="code", placeholder="Barcode EAN"), Button("Créer"), hx_post="/gen-soldes", hx_target="#o"), Div(id="o"), cls="modern-card")
    return Layout(content, "Soldes")

@rt("/gen-soldes", methods=["POST"])
async def post(item:str, old_p:str, new_p:str, code:str):
    try:
        bc_class = barcode.get_barcode_class('ean13'); buf_bc = BytesIO(); bc_class(code, writer=ImageWriter()).write(buf_bc)
        tag = Image.new('RGB', (400, 400), color='white'); d = ImageDraw.Draw(tag)
        d.text((20, 20), f"{item}", fill="black"); d.text((20, 60), f"{old_p}€", fill="red"); d.text((20, 100), f"{new_p}€", fill="black")
        buf_f = BytesIO(); tag.save(buf_f, format="PNG"); s = base64.b64encode(buf_f.getvalue()).decode()
        return Div(Img(src=f"data:image/png;base64,{s}"), A(Button("⬇️ Télécharger"), href=f"data:image/png;base64,{s}", download="tag.png"))
    except: return P("Erreur code", style="color:red")

@rt("/barcode-tab")
def get():
    content = Div(H2("Barcode"), Form(Select(Option("EAN-13", value="ean13"), Option("Code 128", value="code128"), name="t", hx_get="/bc-f", hx_target="#f", hx_trigger="load, change"), Div(id="f"), Button("Générer"), hx_post="/gen-bc", hx_target="#o"), Div(id="o"), cls="modern-card")
    return Layout(content, "Barcode")

@rt("/bc-f")
def get(t:str): return Input(name="d", placeholder="Entrez 12 chiffres") if t=="ean13" else Input(name="d", placeholder="Données")

@rt("/gen-bc", methods=["POST"])
async def post(t:str, d:str):
    try:
        bc = barcode.get_barcode_class(t)(d, writer=ImageWriter()); buf = BytesIO(); bc.write(buf); s = base64.b64encode(buf.getvalue()).decode()
        return Div(Img(src=f"data:image/png;base64,{s}"), A(Button("⬇️ Télécharger"), href=f"data:image/png;base64,{s}", download="bc.png"))
    except: return P("Erreur format", style="color:red")

@rt("/rembg-tab")
def get():
    content = Div(H2("Détourage IA"), Form(Input(type="file", name="i", accept="image/*"), Button("Lancer l'IA"), hx_post="/gen-bg", hx_target="#o", hx_indicator="#l", enctype="multipart/form-data"), Div(id="l", cls="htmx-indicator", aria_busy="true"), Div(id="o"), cls="modern-card")
    return Layout(content, "RemBg")

@rt("/gen-bg", methods=["POST"])
async def post(i:UploadFile):
    res = remove(await i.read()); s = base64.b64encode(res).decode()
    return Div(Img(src=f"data:image/png;base64,{s}"), A(Button("⬇️ Télécharger"), href=f"data:image/png;base64,{s}", download="nobg.png"))

@rt("/qr-tab")
def get():
    content = Div(H2("QR Pro"), Form(Select(Option("URL", value="url"), Option("Fiche", value="kv"), name="m", hx_get="/qr-f", hx_target="#f", hx_trigger="load, change"), Div(id="f"), Grid(Label("QR", Input(type="color", name="fc")), Label("Fond", Input(type="color", name="bc", value="#ffffff"))), Label("Logo", Input(type="file", name="l")), Button("Générer"), hx_post="/gen-qr", hx_target="#o", enctype="multipart/form-data"), Div(id="o"), cls="modern-card")
    return Layout(content, "QR Pro")

@rt("/qr-f")
def get(m:str): return Input(name="u", placeholder="Entrez le lien") if m=="url" else Input(name="u", placeholder="Données")

@rt("/gen-qr", methods=["POST"])
async def post(u:str, fc:str, bc:str, l:UploadFile=None):
    qr = qrcode.QRCode(border=4); qr.add_data(u); qr.make(fit=True); img = qr.make_image(fill_color=fc, back_color=bc).convert('RGB')
    if l and l.size > 0:
        log = Image.open(BytesIO(await l.read())); log.thumbnail((img.size[0]//4, img.size[1]//4)); img.paste(log, ((img.size[0]-log.size[0])//2, (img.size[1]-log.size[1])//2))
    buf = BytesIO(); img.save(buf, format="PNG"); s = base64.b64encode(buf.getvalue()).decode()
    return Div(Img(src=f"data:image/png;base64,{s}"), A(Button("⬇️ Télécharger"), href=f"data:image/png;base64,{s}", download="qr.png"))

@rt("/wifi-qr")
def get():
    content = Div(H2("QR Wi-Fi"), Form(Input(name="s", placeholder="SSID"), Button("Générer"), hx_post="/gen-wifi", hx_target="#o"), Div(id="o"), cls="modern-card")
    return Layout(content, "Accueil")

# --- PAGES LEGALES ---
@rt("/ads.txt")
def get(): return PlainTextResponse("google.com, pub-4081303157053373, DIRECT, f08c47fec0942fa0")
@rt("/ugc")
def get(): return Layout(Div(H2("UGC"), P("Chaque fichier appartient à l'utilisateur."), cls="modern-card"), "UGC")
@rt("/terms")
def get(): return Layout(Div(H2("Conditions"), P("Service gratuit."), cls="modern-card"), "Conditions")
@rt("/privacy")
def get(): return Layout(Div(H2("Vie Privée"), P("Aucun stockage."), cls="modern-card"), "Vie Privée")
@rt("/contact")
def get(): return Layout(Div(H2("Contact"), P("utilitybox.project@gmail.com"), cls="modern-card"), "Contact")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))