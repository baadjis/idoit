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

faq_data = [
    {
        "q": "Comment générer un QR code pour mon menu restaurant en PDF ?",
        "a": "Hébergez votre menu sur Google Drive ou Dropbox, copiez le lien de partage public et utilisez notre outil 'QR Pro'. Vous pouvez même ajouter le logo de votre établissement pour un rendu professionnel."
    },
    {
        "q": "Le générateur d'étiquettes de soldes est-il vraiment gratuit ?",
        "a": "Oui, RetailBox permet de créer gratuitement des étiquettes avec prix barré et code-barres EAN-13. C'est un outil conçu pour aider les commerçants à préparer leurs périodes de promotions sans frais supplémentaires."
    },
    {
        "q": "Comment regrouper Instagram, TikTok et Facebook dans un seul QR ?",
        "a": "Utilisez notre service 'Identité Digitale'. En saisissant les liens de vos différents profils, vous générez une Social Card unique qui centralise toute votre présence en ligne pour vos clients."
    },
    {
        "q": "Comment connecter mes clients au Wi-Fi sans donner le mot de passe ?",
        "a": "Grâce à notre générateur de QR Code Wi-Fi, vous entrez le nom de votre réseau et la clé. Vos clients n'ont qu'à scanner le code avec leur smartphone pour être connectés instantanément et en toute sécurité."
    },
    {
        "q": "Comment créer un lien QR direct vers mon WhatsApp ?",
        "a": "Utilisez l'outil 'QR WhatsApp'. Entrez votre numéro de téléphone et un message de bienvenue automatique. Le QR code ouvrira directement une discussion avec votre boutique."
    },
    {
        "q": "Peut-on supprimer l'arrière-plan d'une photo produit par IA ?",
        "a": "Absolument. Notre outil 'RemBg' utilise une intelligence artificielle pour détourer automatiquement vos photos. Vous obtenez un fichier PNG transparent de qualité studio en moins de 10 secondes."
    },
    {
        "q": "Quels formats de codes-barres sont disponibles pour mon stock ?",
        "a": "Nous supportons le format EAN-13 (12 chiffres) pour les produits destinés à la vente, ainsi que le format Code 128 pour la logistique et l'inventaire interne de votre magasin."
    }
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
    footer.pro-footer {{ background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%) !important; padding: 4rem 1rem; margin-top: 6rem; color: white !important; border-radius: 16px;}}
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
                    H4("🚀 QR Codes avec ou sans Logo"), 
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
                    H4("🔢 Barcode EAN-13 & 128 "), 
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



def Layout(content, active_page, title="RetailBox"):
    nav_items = [("Accueil", "/", "home"), ("QR Pro", "/qr-tab", "qr-code"), ("VCard", "/vcard", "contact"), ("Étiquettes Soldes", "/soldes", "tag"), ("RemBg", "/rembg-tab", "image")]
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

def FaqSection():
    return Section(
        Div(
            H2("Questions fréquentes sur nos outils digitaux"),
            # On génère dynamiquement chaque bloc FAQ à partir de la liste
            *[Details(
                Summary(item["q"]), 
                P(item["a"])
              ) for item in faq_data],
            cls="faq-section"
        )
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

def DataRow(prefix):
    return Div(
        Input(name=f"{prefix}_keys", placeholder="Clé (ex: SKU)"),
        Input(name=f"{prefix}_vals", placeholder="Valeur"),
        Button(Safe('<i data-lucide="trash-2"></i>'), type="button", 
               onclick="this.parentElement.remove()", 
               style="width:40px; background:transparent !important; border:none; color:red;"),
        cls="key-value-row", 
        style="display:grid; grid-template-columns: 1fr 1fr 40px; gap:8px; margin-top:10px;"
    )

@rt("/barcode-tab")
def get():
    content = Div(
        H2("Générateur de Barcode Expert"),
        P("Saisissez vos données ou créez une fiche technique pour votre inventaire."),
        Form(
            Label("Format du code-barres",
                Select(
                    Option("EAN-13 (Standard Commerce)", value="ean13"),
                    Option("Code 128 (Logistique / Données)", value="code128", selected=True),
                    name="t", 
                    hx_get="/bc-f", 
                    hx_target="#f",
                    hx_trigger="load, change" 
                )
            ),
            Div(id="f", style="margin-bottom:20px;"),
            Button("🚀 Générer le Code-barres", cls="btn-full"),
            hx_post="/gen-bc", hx_target="#o"
        ),
        Div(id="o"),
        cls="modern-card"
    )
    return Layout(content, "Barcode")

@rt("/bc-f")
def get(t:str):
    if t == "ean13":
        return Div(
            Input(name="d", placeholder="Entrez 12 chiffres", required=True),
            P("Le 13ème chiffre de contrôle est calculé automatiquement.", style="font-size:0.8rem; opacity:0.7;")
        )
    # Mode Key-Value pour Code 128
    return Div(
        Div(DataRow("bc"), id="bc-kv-list"),
        Button("+ Ajouter une ligne", type="button", 
               hx_get="/add-bc-row", hx_target="#bc-kv-list", hx_swap="beforeend",
               cls="outline secondary", style="width:100%; margin-top:10px;"),
        id="bc-kv-container"
    )

@rt("/add-bc-row")
def get(): return DataRow("bc")


@rt("/gen-bc", methods=["POST"])
async def post(t:str, d:str=None, bc_keys:list=None, bc_vals:list=None):
    try:
        final_data = ""
        if t == "ean13":
            final_data = d.strip()
            if len(final_data) != 12: return P("Erreur : EAN-13 nécessite 12 chiffres.", style="color:red; font-weight:bold;")
        else:
            # Code 128 : On assemble les clés et valeurs
            keys = [bc_keys] if isinstance(bc_keys, str) else bc_keys
            vals = [bc_vals] if isinstance(bc_vals, str) else bc_vals
            # On filtre les lignes vides
            pairs = [f"{k}:{v}" for k, v in zip(keys, vals) if k and k.strip()]
            final_data = " ".join(pairs)
            if not final_data: return P("Erreur : Veuillez saisir au moins une donnée.", style="color:red;")

        # Génération
        bc_class = barcode.get_barcode_class(t)
        buf = BytesIO()
        bc_class(final_data, writer=ImageWriter()).write(buf)
        s = base64.b64encode(buf.getvalue()).decode()
        
        return Div(
            Img(src=f"data:image/png;base64,{s}", style="max-width:100%; border:1px solid #e2e8f0; border-radius:10px;"),
            P(f"Données encodées : {final_data}", style="font-size:0.8rem; margin-top:0.5rem; font-family:monospace;"),
            A(Button("⬇️ Télécharger le Barcode", cls="btn-full"), href=f"data:image/png;base64,{s}", download="barcode.png"),
            style="text-align:center; padding-top:1.5rem;"
        )
    except Exception as e:
        return P(f"Erreur technique : {str(e)}", style="color:red; font-weight:bold;")
    
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
    content = Div(
        H2("Générateur QR Code Pro"),
        P("Personnalisez votre QR Code pour vos menus, boutiques ou réseaux sociaux."),
        Form(
            Label("Type de contenu", 
                Select(
                    Option("Lien URL Simple", value="url", selected=True), 
                    Option("Fiche de données (Clé:Valeur)", value="kv"), 
                    name="qr_mode", 
                    hx_get="/qr-fields", 
                    hx_target="#qr-inputs",
                    hx_trigger="load, change"
                )
            ),
            # Les champs (URL ou KV) s'injectent ici
            Div(id="qr-inputs", style="margin-bottom:20px;"),
            
            # Grille de couleurs avec labels explicites
            Grid(
                Div(Label("Couleur du QR", Input(type="color", name="fc", value="#000000"))),
                Div(Label("Couleur du Fond", Input(type="color", name="bc", value="#ffffff")))
            ),
            
            Label("Logo central (PNG ou JPG)", Input(type="file", name="logo", accept="image/*")),
            
            Button("🚀 Générer le QR Code", cls="btn-full"),
            hx_post="/gen-qr", hx_target="#qr-result", enctype="multipart/form-data"
        ),
        Div(id="qr-result"),
        cls="modern-card"
    )
    return Layout(content, "QR Pro")

@rt("/qr-fields")
def get(qr_mode:str):
    if qr_mode == "url":
        return Input(name="url", placeholder="Entrez le lien (ex: https://...)", required=True)
    
    # Mode Key-Value
    return Div(
        Div(DataRow("qr"), id="qr-kv-list"),
        Button("+ Ajouter une information", type="button", 
               hx_get="/add-qr-row", hx_target="#qr-kv-list", hx_swap="beforeend",
               cls="outline secondary", style="width:100%; margin-top:10px;"),
        id="qr-kv-container"
    )

@rt("/add-qr-row")
def get(): return DataRow("qr")


@rt("/gen-qr", methods=["POST"])
async def post(qr_mode:str, fc:str, bc:str, url:str=None, qr_keys:list=None, qr_vals:list=None, logo:UploadFile=None):
    try:
        # 1. Construction des données
        if qr_mode == "url":
            final_data = url.strip() if url else ""
        else:
            # Normalisation des listes (FastHTML envoie str si 1 ligne, list si plusieurs)
            keys = [qr_keys] if isinstance(qr_keys, str) else (qr_keys or [])
            vals = [qr_vals] if isinstance(qr_vals, str) else (qr_vals or [])
            # Filtrage et assemblage
            lines = [f"{k}: {v}" for k, v in zip(keys, vals) if k and k.strip()]
            final_data = "\n".join(lines)

        if not final_data: 
            return P("Erreur : Aucune donnée saisie.", style="color:red; font-weight:bold;")

        # 2. Création du QR Code
        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
        qr.add_data(final_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fc, back_color=bc).convert('RGB')
        
        # 3. Ajout du Logo si présent
        if logo and logo.size > 0:
            log_img = Image.open(BytesIO(await logo.read()))
            # Redimensionnement intelligent du logo (max 25% de la taille du QR)
            size_ratio = 4 
            logo_size = img.size[0] // size_ratio
            log_img.thumbnail((logo_size, logo_size), Image.LANCZOS)
            # Centrage
            pos = ((img.size[0] - log_img.size[0]) // 2, (img.size[1] - log_img.size[1]) // 2)
            img.paste(log_img, pos)
            
        # 4. Envoi de la réponse
        buf = BytesIO()
        img.save(buf, format="PNG")
        s = base64.b64encode(buf.getvalue()).decode()
        
        return Div(
            Img(src=f"data:image/png;base64,{s}", 
                style="max-width:250px; margin: 2rem auto; border: 2px solid #e2e8f0; border-radius:16px; display:block;"),
            A(Button("⬇️ Télécharger le QR Code PNG", cls="btn-full"), 
              href=f"data:image/png;base64,{s}", download="qrcode-retailbox.png"),
            style="text-align:center; padding-top:1.5rem;"
        )
    except Exception as e:
        return P(f"Erreur technique : {str(e)}", style="color:red;")

@rt("/wifi-qr")
def get():
    content = Div(H2("QR Wi-Fi"), Form(Input(name="s", placeholder="SSID"), Button("Générer"), hx_post="/gen-wifi", hx_target="#o"), Div(id="o"), cls="modern-card")
    return Layout(content, "Accueil")

# --- PAGES LEGALES ---
@rt("/ads.txt")
def get(): return PlainTextResponse("google.com, pub-4081303157053373, DIRECT, f08c47fec0942fa0")

@rt("/terms")
def get():
    content = Div(
        H2("Conditions Générales d'Utilisation"),
        P("Dernière mise à jour : Mars 2026", style="opacity: 0.6; font-size: 0.85rem;"),
        
        H4("1. Description du Service"),
        P("RetailBox met à disposition des outils de génération de QR codes, de codes-barres techniques et de traitement d'images par IA. L'accès au service est gratuit et ne nécessite aucune inscription préalable."),
        
        H4("2. Utilisation autorisée et Interdictions"),
        P("En utilisant ce site, vous vous engagez à respecter les règles suivantes :"),
        Ul(
            Li("Interdiction de générer des contenus frauduleux, trompeurs ou destinés à la contrefaçon de produits."),
            Li("Interdiction d'intégrer des liens malveillants (phishing, virus) dans les QR codes générés."),
            Li("Interdiction d'utiliser nos outils de manière automatisée (scripts, bots) pour saturer nos serveurs."),
            Li("Le service ne doit pas être utilisé pour harceler des tiers via l'outil WhatsApp Direct.")
        ),
        
        H4("3. Limitation de responsabilité"),
        P("RetailBox décline toute responsabilité en cas d'erreur de lecture d'un code-barres ou d'un QR code suite à une mauvaise configuration utilisateur. Nous ne garantissons pas que les étiquettes de soldes générées soient conformes à toutes les réglementations locales d'affichage des prix."),
        
        H4("4. Disponibilité"),
        P("Nous nous efforçons de maintenir le service accessible 24h/24, mais nous nous réservons le droit d'interrompre l'accès pour maintenance sans préavis."),
        cls="modern-card"
    )
    return Layout(content, "Conditions")

@rt("/privacy")
def get():
    content = Div(
        H2("Politique de Confidentialité"),
        P("Votre vie privée est au cœur de notre service technique."),
        
        H4("1. Traitement des fichiers (RAM-Only)"),
        P("RetailBox utilise un traitement éphémère en mémoire vive (RAM). Pour les outils comme 'RemBg IA' :"),
        Ul(
            Li("Les photos produits sont traitées instantanément."),
            Li("Aucun fichier n'est écrit sur un disque dur permanent."),
            Li("Toutes les données sont effacées dès la fin de la génération."),
        ),
        
        H4("2. Publicité et Cookies (Google AdSense)"),
        P("Ce site utilise Google AdSense. Google utilise des cookies pour diffuser des annonces basées sur vos visites précédentes sur ce site ou d'autres sites. Ces cookies permettent à Google et à ses partenaires de diffuser des annonces basées sur votre navigation. Vous pouvez désactiver la publicité personnalisée dans vos paramètres Google."),
        
        H4("3. Collecte de données personnelles"),
        P("Nous ne collectons aucune donnée nominative (nom, email, adresse IP) à des fins de marketing. Le site est utilisable de manière totalement anonyme."),
        
        H4("4. Liens Externes"),
        P("RetailBox contient des liens vers des services tiers (WhatsApp, Facebook, etc.). Nous ne sommes pas responsables de la gestion des données sur ces plateformes externes."),
        cls="modern-card"
    )
    return Layout(content, "Vie Privée")
@rt("/ugc")
def get():
    content = Div(
        H2("Droits sur le Contenu Généré (UGC)"),
        P("UGC signifie 'User Generated Content' (Contenu généré par l'utilisateur)."),
        
        H4("1. Propriété exclusive"),
        P("Vous êtes le propriétaire unique de 100% des fichiers générés sur RetailBox. Cela inclut vos QR codes de menu, vos étiquettes de prix soldés et vos photos détourées."),
        
        H4("2. Usage Commercial et Droits"),
        P("RetailBox vous accorde un droit d'utilisation commerciale illimité et gratuit sur toutes vos créations réalisées via nos outils. Nous ne percevons aucune commission et ne revendiquons aucun droit d'auteur sur votre travail."),
        
        H4("3. Responsabilité du contenu"),
        P("En générant un fichier, vous certifiez posséder les droits sur les logos importés et les liens intégrés. RetailBox n'agit que comme un prestataire technique passif et ne valide pas la légalité du contenu que vous choisissez d'insérer dans vos codes."),
        cls="modern-card"
    )
    return Layout(content, "UGC")

@rt("/contact")
def get(): return Layout(Div(H2("Contact"), P("utilitybox.project@gmail.com"), cls="modern-card"), "Contact")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))