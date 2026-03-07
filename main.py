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

# --- SEO & META TAGS ---
meta_tags = (
    Meta(name="description", content="Générez gratuitement vos étiquettes de soldes, cartes de visite QR VCard, identité digitale et codes-barres. Outils pro pour e-commerce."),
    Meta(name="keywords", content="Identité digitale QR, Étiquettes soldes, QR Code VCard, Barcode EAN13 gratuit, Détourage photo produit, RetailBox"),
    Meta(property="og:title", content="RetailBox | Étiquettes de Soldes & Identité Digitale"),
    Meta(name="viewport", content="width=device-width, initial-scale=1, maximum-scale=1"),
)

# --- STYLE STABILISÉ ---
custom_style = Style(f"""
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    :root {{
        --pico-font-family: 'Plus Jakarta Sans', sans-serif;
        --primary: #4f46e5;
        --secondary: #9333ea;
        --pico-color: #1e293b;
        --pico-background-color: #ffffff;
    }}

    @media (prefers-color-scheme: dark) {{
        :root {{
            --pico-color: #f8fafc !important;
            --pico-background-color: #0f172a !important;
        }}
        body {{ background-color: #0f172a !important; color: #f8fafc !important; }}
        .modern-card {{ background: #1e293b !important; border-color: #334155 !important; color: #f8fafc !important; }}
        p, h2, h3, h4, li, span, label, summary {{ color: #cbd5e1 !important; }}
        .nav-pills a {{ background: #1e293b !important; color: white !important; }}
        footer.pro-footer {{ background: #0f172a !important; border-top: 1px solid #334155 !important; }}
    }}

    body {{
        margin: 0; padding: 0; letter-spacing: -0.015em; line-height: 1.6;
        background-image: radial-gradient(at 0% 0%, rgba(79, 70, 229, 0.05) 0px, transparent 50%);
        background-attachment: fixed; min-height: 100vh;
    }}

    a {{ text-decoration: none !important; border: none !important; color: inherit; }}

    .gradient-text {{
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        display: inline-block;
    }}

    .hero-title {{ font-size: clamp(1.8rem, 8vw, 2.8rem); font-weight: 800; text-align: center; margin: 1.5rem 0; }}

    .nav-scroll-container {{ width: 100%; overflow-x: auto; padding: 10px 0; }}
    .nav-pills {{ display: flex; gap: 0.6rem; min-width: max-content; padding: 0 1rem; justify-content: center; }}
    .nav-pills a {{
        padding: 0.6rem 1.2rem; border-radius: 12px; background: white; border: 1px solid #e2e8f0;
        font-weight: 700; color: #1e293b; transition: 0.3s;
    }}
    .nav-pills a.active {{ background: var(--primary) !important; color: white !important; border-color: var(--primary); }}

    .services-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(min(100%, 350px), 1fr));
        gap: 2rem; margin-top: 2rem;
    }}

    .modern-card {{
        border: 1px solid #e2e8f0; padding: 2rem; border-radius: 24px;
        height: 100%; display: flex; flex-direction: column; background: #ffffff;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }}
    .modern-card:hover {{ transform: translateY(-6px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); }}
    .card-header-flex {{ display: flex; align-items: center; gap: 15px; margin-bottom: 1.2rem; }}
    .modern-card footer {{ background: transparent !important; border-top: 1px solid #e2e8f0; padding: 1.2rem 0 0 0 !important; margin-top: auto !important; }}

    button, .btn-full {{
        width: 100% !important; padding: 0.9rem !important; border-radius: 14px !important;
        font-weight: 700 !important; border: 1px solid #e2e8f0 !important;
        background: #f8fafc !important; color: #1e293b !important;
        cursor: pointer; transition: 0.3s ease !important;
    }}

    button:hover, .btn-full:hover {{
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%) !important;
        color: white !important; border-color: transparent !important;
    }}

    /* FAQ */
    .faq-section {{ margin-top: 5rem; }}
    details {{ background: rgba(255,255,255,0.5); padding: 1rem; border-radius: 16px; border: 1px solid #e2e8f0; margin-bottom: 1rem; }}
    summary {{ font-weight: 700; cursor: pointer; color: #1e293b; }}

    footer.pro-footer {{ padding: 4rem 1rem; margin-top: 6rem; border-top: 1px solid #e2e8f0; }}
    .footer-content {{ display: flex; flex-wrap: wrap; justify-content: space-between; max-width: 1100px; margin: 0 auto; gap: 3rem; }}
    .footer-section {{ flex: 1; min-width: 280px; }}
    .legal-links {{ display: flex; flex-wrap: wrap; gap: 20px; justify-content: center; margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #e2e8f0; font-size: 0.9rem; opacity: 0.8; }}

    .top-ad-banner {{ width: 100%; max-width: 1100px; margin: 1rem auto; min-height: 90px; background: rgba(0,0,0,0.02); border: 1px dashed #cbd5e1; border-radius: 16px; display: flex; align-items: center; justify-content: center; }}
    .app-grid {{ display: grid; grid-template-columns: 1fr 320px; gap: 2.5rem; max-width: 1200px; margin: auto; padding: 0 1rem; }}
    @media (max-width: 1024px) {{ .app-grid {{ grid-template-columns: 1fr; }} }}
""")

app, rt = fast_app(static_path='public', hdrs=(*meta_tags, Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"), custom_style, adsense_script, Script(src="https://unpkg.com/lucide@latest")))
services = [
        
        ("users", "Identité Digitale", "Un seul QR pour tous vos réseaux.", "/digital-id"),
        ("qr-code", "QR Code Pro", "Lien personnalisé avec votre logo.", "/qr-tab"),
        ("barcode", "Barcode Expert", "Codes EAN-13 et Code 128 pro.", "/barcode-tab"),
        
        ("wifi", "Accès Wi-Fi", "Connexion automatique sans mot de passe.", "/wifi-qr"),
        ("contact","VCard","Créer votre carte de visite digitale", "/vcard"),
        ("tag", "Étiquettes Soldes", "Prix barré + Barcode pour vos promos.", "/soldes"),
        ("image", "Détourage IA", "Enlever le fond des photos de vos produits.", "/rembg-tab"),
        ("message-circle", "QR WhatsApp", "Lien direct vers discussion.", "/whatsapp-qr")
    ]
# --- COMPOSANTS ---

def Logo():
    return Div(
        Safe(f'<svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="url(#grad)" stroke-width="3"><defs><linearGradient id="grad"><stop offset="0%" stop-color="#4f46e5"/><stop offset="100%" stop-color="#9333ea"/></linearGradient></defs><path d="M21 16V8l-9-5-9 5v8l9 5 9-5z"></path></svg>'),
        H1("RetailBox", cls="gradient-text", style="margin:0; font-size:1.5rem;"),
        style="display:flex; align-items:center; justify-content:center; gap:10px;"
    )

def FaqSection():
    return Section(
        Div(
            H2("Questions fréquentes sur nos outils digitaux"),
            Details(Summary("Comment générer un QR code gratuit pour mon commerce ?"), 
                    P("Il vous suffit d'utiliser notre outil 'QR Pro', d'entrer l'URL de votre boutique et de personnaliser les couleurs. Le téléchargement est immédiat et sans frais.")),
            Details(Summary("Comment créer une étiquette de soldes professionnelle ?"), 
                    P("Notre générateur d'étiquettes de soldes permet de saisir l'ancien prix, le nouveau prix et le code-barres. Il génère une image prête à imprimer avec le prix barré.")),
            Details(Summary("Regrouper ses réseaux sociaux dans un seul QR code ?"), 
                    P("Oui, utilisez notre service d'Identité Digitale. Entrez vos liens Instagram, TikTok et WhatsApp pour créer une Social Card unique pour vos clients.")),
            Details(Summary("Le détourage d'image par IA est-il illimité ?"), 
                    P("Absolument. Vous pouvez supprimer le fond de vos photos produits autant de fois que nécessaire pour vos fiches Shopify ou Vinted.")),
            cls="faq-section"
        )
    )

def SeoInstructional():
    return Section(
        Div(
            H2("Guide complet : Comment utiliser nos services gratuits"),
            # Première ligne : Identité, QR et Contacts
            Grid(
                Div(
                    H4("🚀 QR Codes avec Logo"), 
                    P("Entrez votre URL ou texte, personnalisez les couleurs et ajoutez le logo de votre marque. Téléchargez un QR code haute résolution prêt pour l'impression.")
                ),
                Div(
                    H4("🌐 Identité Digitale"), 
                    P("Regroupez tous vos réseaux sociaux (Facebook, Instagram, TikTok, Shopify) dans un seul QR Code unique pour faciliter l'accès à vos clients.")
                ),
                Div(
                    H4("👤 VCard : Carte de Visite"), 
                    P("Saisissez vos coordonnées pro (nom, tel, email). Le QR généré permet à vos clients d'enregistrer votre contact instantanément sur leur smartphone.")
                ),
                Div(
                    H4("💬 QR WhatsApp Direct"), 
                    P("Simplifiez vos commandes : générez un lien QR qui ouvre directement une discussion WhatsApp avec un message pré-rempli pour votre boutique.")
                ),
            ),
            # Deuxième ligne : Logistique, Prix et Technique
            Grid(
                Div(
                    H4("🏷️ Étiquettes de Soldes"), 
                    P("Indiquez le prix d'origine et le prix remisé. Notre outil génère une étiquette visuelle pro avec prix barré et code-barres pour vos rayons.")
                ),
                Div(
                    H4("🔢 Barcode EAN-13 & 128"), 
                    P("Entrez vos chiffres pour générer des codes-barres conformes aux standards du commerce et de la logistique, lisibles par tous les scanners laser.")
                ),
                Div(
                    H4("🖼️ Détourage IA de Produit"), 
                    P("Importez vos photos. Notre Intelligence Artificielle supprime l'arrière-plan automatiquement pour créer des fichiers PNG transparents de qualité studio.")
                ),
                Div(
                    H4("📶 QR Code Accès Wi-Fi"), 
                    P("Entrez le nom de votre réseau et le mot de passe pour générer un code de connexion automatique sécurisée sans saisie manuelle pour vos clients.")
                ),
            ),
            cls="modern-card", 
            style="margin-top:4rem; border-style: solid; border-width: 2px; border-color: var(--primary);"
        )
    )

def FooterSection():
    return Footer(
        Div(
            Div(H4("🚀 Usage"), P("Génération gratuite pour retailers. Traitement haute performance en mémoire vive."), cls="footer-section"),
            Div(H4("🛡️ Vie Privée"), P("Zéro stockage sur nos serveurs. Vos fichiers sont supprimés instantanément."), cls="footer-section"),
            Div(H4("👤 Propriété UGC"), P("Vous détenez 100% des droits sur tous les fichiers générés sur ce site."), cls="footer-section"),
            cls="footer-content"
        ),
        Div(
            A("Conditions", href="/terms"), A("Vie Privée", href="/privacy"), A("UGC", href="/ugc"), A("Contact", href="/contact"),
            Span(f"© {CURRENT_YEAR} RetailBox"),
            cls="legal-links"
        ),
        cls="pro-footer"
    )

def Layout(content, active_page, title="RetailBox"):
    nav_items = [("Accueil", "/", "home"), 
                 ("QR Pro", "/qr-tab", "qr-code"), 
                
                   ("Barcode", "/barcode-tab", "barcode"),
                    ("VCard", "/vcard", "contact"),
                    ("Étiquettes Soldes", "/soldes", "tag"),
                  
                 ("RemBg", "/rembg-tab", "image")]
    return Title(f"{active_page} | {title}"), Main(
        Header(
            Logo(),
            Div(H1("Générez et Transformez en un clic", cls="hero-title gradient-text"), style="text-align:center;"),
            Div(Nav(Div(*[A(Safe(f'<i data-lucide="{icon}" style="width:18px"></i> {name}'), href=url, cls="active" if active_page == name else "") for name, url, icon in nav_items], cls="nav-pills")), cls="nav-scroll-container")
        ),
        Div(P("Espace Publicitaire", style="font-size:0.6rem; opacity:0.5; margin:0"), cls="top-ad-banner"),
        Div(Section(content), Aside(Div(P("Publicité"), style="background:rgba(0,0,0,0.02); border:1px dashed #ccc; border-radius:20px; height:600px; display:flex; align-items:center; justify-content:center; position:sticky; top:20px;"), cls="sidebar"), cls="app-grid"),
        SeoInstructional(), FaqSection(),
        FooterSection(),
        Script("lucide.createIcons();"), cls="container"
    )

# --- ROUTES ACCUEIL ---

@rt("/")
def get():

    cards = Div(*[Card(
        Div(Safe(f'<i data-lucide="{s[0]}" style="width:32px; color:var(--primary);"></i>'), H3(s[1], style="margin:0;"), cls="card-header-flex"),
        P(s[2]),
        Footer(A(Button("Ouvrir l'outil", cls="btn-full"), href=s[3])), cls="modern-card"
    ) for s in services], cls="services-grid")
    return Layout(cards, "Accueil")

# --- SERVICES ---

@rt("/digital-id")
def get():
    content = Div(
        H2("Votre Identité Digitale"),
        P("Rassemblez vos réseaux sociaux dans un seul QR Code."),
        Form(
            Grid(Input(name="fb", placeholder="Lien Facebook"), Input(name="ig", placeholder="Lien Instagram")),
            Grid(Input(name="tk", placeholder="Lien TikTok"), Input(name="sh", placeholder="Lien Boutique / Shopify")),
            Button("🚀 Générer ma Social Card"), hx_post="/gen-id", hx_target="#o"
        ), Div(id="o"), cls="modern-card"
    )
    return Layout(content, "Identité Digitale")

@rt("/gen-id", methods=["POST"])
async def post(fb:str="", ig:str="", tk:str="", sh:str=""):
    data = f"Mes Réseaux :\nFB: {fb}\nIG: {ig}\nTK: {tk}\nBoutique: {sh}"
    return generate_qr_response(data, "social-id.png")

@rt("/soldes")
def get():
    content = Div(H2("Étiquettes de Soldes"), P("Créez une étiquette pro avec prix barré."), Form(Input(name="item", placeholder="Nom du produit"), Grid(Input(name="old_p", placeholder="Ancien Prix"), Input(name="new_p", placeholder="Prix Soldé")), Input(name="code", placeholder="Barcode (12 chiffres)"), Button("🚀 Créer"), hx_post="/gen-soldes", hx_target="#o"), Div(id="o"), cls="modern-card")
    return Layout(content, "Étiquettes Soldes")

@rt("/gen-soldes", methods=["POST"])
async def post(item:str, old_p:str, new_p:str, code:str):
    try:
        # Génération du Barcode
        bc_class = barcode.get_barcode_class('ean13')
        buf_bc = BytesIO()
        bc_class(code, writer=ImageWriter()).write(buf_bc)
        bc_img = Image.open(buf_bc).resize((300, 120))

        # Création de l'étiquette
        tag = Image.new('RGB', (400, 500), color='white')
        d = ImageDraw.Draw(tag)
        
        # Utilisation de la police par défaut pour éviter les erreurs de fichier .ttf
        try:
            # On essaye de charger une police de base si elle existe sur Linux
            font = ImageFont.load_default()
        except:
            font = None

        d.text((20, 20), f"PRODUIT: {item[:20]}", fill="black", font=font)
        d.text((20, 80), f"AVANT: {old_p}€", fill="red", font=font)
        d.line((15, 95, 120, 95), fill="red", width=3) # Barrer le prix
        d.text((20, 140), f"PRIX : {new_p}€", fill="black", font=font)
        
        # Coller le code barre en bas
        tag.paste(bc_img, (50, 300))

        buf_final = BytesIO()
        tag.save(buf_final, format="PNG")
        s = base64.b64encode(buf_final.getvalue()).decode()
        return Div(
            Img(src=f"data:image/png;base64,{s}", style="border:2px solid #e2e8f0; border-radius:10px;"),
            A(Button("⬇️ Télécharger l'étiquette", cls="btn-full"), href=f"data:image/png;base64,{s}", download="etiquette-soldes.png"),
            style="text-align:center; margin-top:1rem;"
        )
    except Exception as e:
        return P(f"Erreur : Vérifiez que le code a 12 chiffres ({e})", style="color:red")
@rt("/wifi-qr")
def get():
    content = Div(H2("QR Wi-Fi"), Form(Input(name="s", placeholder="Nom WiFi"), Input(name="p", placeholder="Mot de passe"), Button("Générer"), hx_post="/gen-wifi", hx_target="#o"), Div(id="o"), cls="modern-card")
    return Layout(content, "Wi-Fi")

@rt("/gen-wifi", methods=["POST"])
async def post(s:str, p:str): return generate_qr_response(f"WIFI:S:{s};T:WPA;P:{p};;", "wifi.png")

def generate_qr_response(data, name):
    qr = qrcode.make(data); buf = BytesIO(); qr.save(buf, format="PNG"); s = base64.b64encode(buf.getvalue()).decode()
    return Div(Img(src=f"data:image/png;base64,{s}", style="max-width:240px; margin:auto;"), A(Button("⬇️ Télécharger"), href=f"data:image/png;base64,{s}", download=name), style="text-align:center; padding:1rem;")

@rt("/qr-tab")
def get():
    content = Div(H2("QR Code Pro"), Form(Input(name="u", placeholder="URL"), Grid(Input(type="color", name="fc", value="#000000"), Input(type="color", name="bc", value="#ffffff")), Label("Logo", Input(type="file", name="l")), Button("Générer"), hx_post="/gen-qr", hx_target="#o", enctype="multipart/form-data"), Div(id="o"), cls="modern-card")
    return Layout(content, "QR Pro")

@rt("/gen-qr", methods=["POST"])
async def post(u:str, fc:str, bc:str, l:UploadFile=None):
    qr = qrcode.QRCode(border=4); qr.add_data(u); qr.make(fit=True); img = qr.make_image(fill_color=fc, back_color=bc).convert('RGB')
    if l and l.size > 0:
        log = Image.open(BytesIO(await l.read())); log.thumbnail((img.size[0]//4, img.size[1]//4)); img.paste(log, ((img.size[0]-log.size[0])//2, (img.size[1]-log.size[1])//2))
    buf = BytesIO(); img.save(buf, format="PNG"); s = base64.b64encode(buf.getvalue()).decode()
    return Div(Img(src=f"data:image/png;base64,{s}", style="max-width:240px;"), Br(), A(Button("⬇️ Télécharger"), href=f"data:image/png;base64,{s}", download="qr.png"), style="text-align:center")

@rt("/barcode-tab")
def get():
    content = Div(H2("Barcode Pro"), Form(Select(Option("EAN-13", value="ean13"), Option("Code 128", value="code128"), name="t"), Input(name="d", placeholder="Données"), Button("Générer"), hx_post="/gen-bc", hx_target="#o"), Div(id="o"), cls="modern-card")
    return Layout(content, "Barcode")

@rt("/gen-bc", methods=["POST"])
async def post(t:str, d:str):
    try:
        bc = barcode.get_barcode_class(t)(d, writer=ImageWriter()); buf = BytesIO(); bc.write(buf); s = base64.b64encode(buf.getvalue()).decode()
        return Div(Img(src=f"data:image/png;base64,{s}"), Br(), A(Button("⬇️ Télécharger"), href=f"data:image/png;base64,{s}", download="bc.png"), style="text-align:center")
    except: return P("Erreur format", style="color:red")

@rt("/rembg-tab")
def get():
    content = Div(H2("Détourage IA"), Form(Input(type="file", name="i", accept="image/*"), Button("Supprimer le fond"), hx_post="/gen-bg", hx_target="#o", hx_indicator="#l", enctype="multipart/form-data"), Div(id="l", cls="htmx-indicator", aria_busy="true"), Div(id="o"), cls="modern-card")
    return Layout(content, "RemBg")

@rt("/gen-bg", methods=["POST"])
async def post(i:UploadFile):
    res = remove(await i.read()); s = base64.b64encode(res).decode()
    return Div(Img(src=f"data:image/png;base64,{s}"), Br(), A(Button("⬇️ Télécharger"), href=f"data:image/png;base64,{s}", download="nobg.png"), style="text-align:center")

@rt("/vcard")
def get():
    content = Div(
        H2("Générateur de Carte de Visite QR (VCard)"),
        P("Remplissez vos informations professionnelles. Le QR Code permettra à vos clients d'enregistrer votre contact d'un simple scan."),
        Form(
            Grid(Input(name="fn", placeholder="Prénom"), Input(name="ln", placeholder="Nom")),
            Grid(Input(name="org", placeholder="Entreprise / Boutique"), Input(name="tel", placeholder="Téléphone")),
            Input(name="email", placeholder="Email professionnel"),
            Button("🚀 Générer la VCard"), hx_post="/gen-vcard", hx_target="#vcard-out"
        ), 
        Div(id="vcard-out"), cls="modern-card"
    )
    return Layout(content, "VCard")

@rt("/gen-vcard", methods=["POST"])
async def post(fn:str, ln:str, org:str, tel:str, email:str):
    # Format standard VCard 3.0
    vcard_data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{fn} {ln}\nORG:{org}\nTEL:{tel}\nEMAIL:{email}\nEND:VCARD"
    return generate_qr_response(vcard_data, "contact.png")

@rt("/whatsapp-qr")
def get():
    content = Div(H2("Générateur QR WhatsApp"), P("Créez un QR Code qui ouvre un chat WhatsApp avec vous."), Form(Input(name="phone", placeholder="Numéro (ex: 336...)"), Input(name="msg", placeholder="Message automatique"), Button("Générer"), hx_post="/gen-wa", hx_target="#o"), Div(id="o"), cls="modern-card")
    return Layout(content, "WhatsApp")

@rt("/gen-wa", methods=["POST"])
async def post(phone:str, msg:str=""): return generate_qr_response(f"https://wa.me/{phone}?text={msg}", "wa.png")

# --- PAGES LÉGALES ---
@rt("/ads.txt")
def get(): return PlainTextResponse("google.com, pub-4081303157053373, DIRECT, f08c47fec0942fa0")

@rt("/terms")
def get():
    content = Div(
        H2("Conditions Générales d'Utilisation"),
        P("Dernière mise à jour : Mars 2026", style="opacity: 0.6; font-size: 0.8rem;"),
        
        H4("1. Acceptation des services"),
        P("En accédant à RetailBox, vous acceptez d'utiliser nos outils de génération conformément aux présentes conditions. Le service est fourni gratuitement et 'en l'état', sans garantie de disponibilité ininterrompue."),
        
        H4("2. Limitations techniques"),
        P("Bien que nos générateurs respectent les standards (EAN-13, Code 128, QR), RetailBox ne peut être tenu responsable si un scanner tiers ne parvient pas à lire un code généré suite à une mauvaise configuration des couleurs ou une impression de faible qualité."),
        
        H4("3. Usages Interdits (Code de conduite)"),
        P("Il est strictement interdit d'utiliser nos outils pour :"),
        Ul(
            Li("Générer des codes-barres frauduleux pour des produits que vous ne possédez pas."),
            Li("Créer des QR codes redirigeant vers des sites de phishing, de malware ou de contenu illégal."),
            Li("Utiliser le service WhatsApp pour harceler ou envoyer des messages non sollicités (spam)."),
            Li("Tenter de saturer nos serveurs par des requêtes automatisées (bots).")
        ),
        
        H4("4. Responsabilité"),
        P("L'utilisateur est le seul responsable de l'usage commercial des fichiers téléchargés. RetailBox ne pourra être tenu responsable d'un quelconque préjudice lié à l'utilisation de ces outils."),
        
        cls="modern-card"
    )
    return Layout(content, "Conditions")

@rt("/privacy")
def get():
    content = Div(
        H2("Politique de Confidentialité"),
        P("Nous accordons une importance capitale à la protection de votre vie privée."),
        
        H4("1. Traitement des données"),
        P("RetailBox utilise un traitement éphémère. Lorsqu'un utilisateur importe une photo ou saisit des données :"),
        Ul(
            Li("Le traitement est effectué en mémoire vive (RAM)."),
            Li("Aucune donnée n'est écrite sur un disque dur permanent."),
            Li("Les fichiers sont supprimés instantanément après le traitement."),
        ),
        
        H4("2. Absence de collecte"),
        P("Nous ne demandons aucune inscription. Nous ne collectons ni noms, ni adresses e-mail, ni données de localisation."),
        
        H4("3. Cookies et Publicité (Google AdSense)"),
        P("Ce site utilise Google AdSense pour diffuser des annonces. Google peut utiliser des cookies pour diffuser des publicités basées sur vos visites précédentes sur ce site ou d'autres sites. Vous pouvez désactiver la publicité personnalisée dans les paramètres de votre compte Google."),
        
        H4("4. Sécurité"),
        P("Bien qu'aucune donnée ne soit stockée, les échanges entre votre navigateur et nos serveurs sont sécurisés par le protocole HTTPS (SSL)."),
        
        cls="modern-card"
    )
    return Layout(content, "Vie Privée")
@rt("/ugc")
def get():
    content = Div(
        H2("Droits sur le Contenu Généré (UGC)"),
        P("UGC signifie 'User Generated Content' (Contenu généré par l'utilisateur)."),
        
        H4("1. Propriété intellectuelle"),
        P("Vous êtes le propriétaire exclusif de 100% des fichiers générés sur RetailBox. Cela inclut les QR Codes, les étiquettes de soldes, les codes-barres et les images détourées."),
        
        H4("2. Usage Commercial"),
        P("Vous disposez d'un droit d'utilisation illimité, personnel et commercial sur vos créations. RetailBox ne perçoit aucune redevance et ne revendique aucun droit d'auteur sur votre travail."),
        
        H4("3. Responsabilité du contenu intégré"),
        P("En générant un fichier, vous certifiez que les informations intégrées (liens URL, logos, textes) ne violent aucun droit de propriété intellectuelle tiers. RetailBox n'agit que comme un outil technique passif."),
        
        cls="modern-card"
    )
    return Layout(content, "UGC")
@rt("/contact")
def get(): return Layout(Div(H2("Contact"), P("Email: utilitybox.project@gmail.com"), cls="modern-card"), "Contact")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))