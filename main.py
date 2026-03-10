from dotenv import load_dotenv
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
from constants import SOCIAL_NETWORKS, services,faq_data,adsense_script_src,ga_lib_src,guide_data
from styles import styles

load_dotenv() 
os.environ['U2NET_HOME'] = '/tmp'
FORMSPREE_ID = os.environ.get("FORMSPREE_ID", "TON_ID_DE_TEST")

# --- CONFIGURATION ---
CURRENT_YEAR = datetime.now().year

adsense_script = Script(
    src=adsense_script_src,
    async_=True,
    crossorigin="anonymous"
)


# --- SEO & META TAGS ---
meta_tags = (
    Meta(name="description", content="RetailBox - Identité digitale, étiquettes de soldes prix barré, QR Codes menu restaurant et codes-barres EAN13 gratuits."),
    Meta(name="keywords", content="Identité digitale QR, QR Code menu restaurant PDF, étiquettes soldes, créer barcode ean13, détourage photo produit"),
    Meta(property="og:title", content="RetailBox | Votre Identité Digitale & Outils Commerce"),
    Meta(name="viewport", content="width=device-width, initial-scale=1, maximum-scale=1"),
    Meta(name="color-scheme", content="light")
)

# --- STYLE STABILISÉ & TYPOGRAPHIE ---
custom_style = Style(styles)

ga_lib = Script(src=ga_lib_src, async_=True)

# Le deuxième script qui configure ton ID
ga_config = Script("""
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-YV2LEDEMR8');
""")

app, rt = fast_app(static_path='public', hdrs=(*meta_tags, Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"), custom_style,
                                               ga_lib, ga_config, adsense_script, Script(src="https://unpkg.com/lucide@latest"),# Dans ton main.py, assure-toi que ce script est présent pour HTMX
Script("""
    document.body.addEventListener('htmx:afterSwap', function(evt) {
        lucide.createIcons();
    });
""")))


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
def FooterSection():
    return Footer(
        # Section supérieure : 3 colonnes d'informations rassurer l'utilisateur
        Div(
            Div(
                H4("🚀 Usage & Service"), 
                P("Génération technique haute performance en mémoire vive pour retailers."), 
                cls="footer-section"
            ),
            Div(
                H4("🛡️ Confidentialité"), 
                P("Zéro stockage sur nos serveurs. Vos données et images sont éphémères."), 
                cls="footer-section"
            ),
            Div(
                H4("👤 Propriété UGC"), 
                P("User Generated Content : Vous détenez 100% des droits sur vos fichiers générés."), 
                cls="footer-section"
            ),
            cls="footer-content"
        ),
        
        # Section inférieure : Liens de navigation et mentions légales
        Div(
            A("À Propos", href="/about"), # Ajouté ici pour la cohérence
            A("Guide Complet", href="/guide"), # Ajouté
            A("FAQ", href="/faq"), 
            A("Conditions", href="/terms"), 
            A("Vie Privée", href="/privacy"), 
            A("UGC", href="/ugc"), 
            A("Contact", href="/contact"),
            Span(f"© {CURRENT_YEAR} RetailBox"),
            cls="legal-links"
        ),
        cls="pro-footer"
    )
def Layout(content, active_page, title="RetailBox"):
    nav_items = [
        ("Accueil", "/", "home"), 
        ("Guide", "/guide", "book-open"), 
        ("FAQ", "/faq", "help-circle"), 
        ("À Propos", "/about", "info"),
        ("Contact", "/contact", "mail")
    ]
    return Title(f"{active_page} | {title}"), Main(
        Header(
            Logo(),
            Div(H1("Générez et Transformez en un clic", cls="hero-title gradient-text"), style="text-align:center;"),
            Div(Nav(Div(*[A(Safe(f'<i data-lucide="{icon}" style="width:18px"></i> {name}'), href=url, cls="active" if active_page == name else "") for name, url, icon in nav_items], cls="nav-pills")), cls="nav-scroll-container")
        ),
        Div(P("Publicité", style="font-size:0.6rem; opacity:0.5; margin:0"), cls="top-ad-banner"),
        
        # Ici, on n'a que le contenu spécifique de la page
        Div(
            Section(content), 
            Aside(Div(P("Publicité"), style="background:rgba(0,0,0,0.02); border:1px dashed #ccc; border-radius:20px; height:600px; display:flex; align-items:center; justify-content:center; position:sticky; top:20px;"), cls="sidebar"), 
            cls="app-grid"
        ),
        
        FooterSection(),
        Script("lucide.createIcons();"), 
        cls="container"
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
    # On affiche les 8 cartes de services
    cards = Div(*[Card(
        Div(Safe(f'<i data-lucide="{s[0]}" style="width:32px; color:var(--primary);"></i>'), H3(s[1], style="margin:0; font-size:1.1rem;"), cls="card-header-flex"),
        P(s[2], style="font-size:0.9rem;"),
        Footer(A(Button("Ouvrir l'outil", cls="btn-full"), href=s[3])), cls="modern-card"
    ) for s in services], cls="services-grid")
    
    # On ajoute juste un petit titre SEO avant le footer uniquement sur l'accueil
    content = Div(
        cards,
        H2("Solutions digitales pour Small Business", style="margin-top:4rem; text-align:center;"),
        P("Accédez à nos tutoriels détaillés dans la page Guide pour optimiser vos ventes.", style="text-align:center; opacity:0.7;")
    )
    
    return Layout(content, "Accueil")
# --- OUTILS ---

def SocialRow():
    return Div(
        # 1. Sélection du réseau
        Select(*[Option(label, value=val) for val, label in SOCIAL_NETWORKS], 
               name="social_networks", onchange="checkDuplicates()"),
        
        # 2. Saisie de l'identifiant
        Input(name="social_handles", placeholder="Lien URL ou @identifiant", required=True),
        
        # 3. Bouton supprimer en bas (Full Width)
        Button(
            Safe('<i data-lucide="trash-2" style="width:18px"></i> Supprimer ce réseau'), 
            type="button", 
            onclick="this.parentElement.remove(); checkDuplicates();", 
            cls="btn-remove-final"
        ),
        
        cls="social-row"
    )

@rt("/add-social-row")
def get(): return SocialRow()

@rt("/digital-id")
def get():
    js_logic = Script("""
        function checkDuplicates() {
            const selects = document.querySelectorAll('select[name="social_networks"]');
            const selectedValues = Array.from(selects).map(s => s.value);
            selects.forEach(select => {
                const options = select.options;
                for (let i = 0; i < options.length; i++) {
                    const isSelectedElsewhere = selectedValues.filter(v => v === options[i].value).length > 1;
                    options[i].disabled = (isSelectedElsewhere && options[i].value !== select.value);
                }
            });
            if (window.lucide) lucide.createIcons();
        }
        document.body.addEventListener('htmx:afterSwap', checkDuplicates);
    """)

    content = Div(
        H2("Votre Identité Digitale", cls="gradient-text"),
        P("Centralisez tous vos réseaux. Sélectionnez une plateforme et ajoutez votre lien."),
        Form(
            # 1. ZONE DES INPUTS (Générée côté serveur immédiatement)
            Div(SocialRow(), id="social-list"),
            # 2. ZONE DES ACTIONS
            Div(
                Button("+ Ajouter un réseau", type="button", hx_get="/add-social-row", hx_target="#social-list", hx_swap="beforeend", cls="outline"),
                Button("🚀 Générer ma Social Card", type="submit", cls="btn-full"),
                style="margin-top: 2rem; border-top: 1px solid #e2e8f0; padding-top: 2rem;"
            ),
            hx_post="/gen-id", hx_target="#id-out"
        ),
        Div(id="id-out"), js_logic, cls="modern-card"
    )
    return Layout(content, "Accueil")


@rt("/gen-id", methods=["POST"])
async def post(social_networks: list = None, social_handles: list = None):
    nets = [social_networks] if isinstance(social_networks, str) else (social_networks or [])
    hands = [social_handles] if isinstance(social_handles, str) else (social_handles or [])
    
    data_lines = ["MA PRÉSENCE DIGITALE :"]
    seen_networks = set() # Pour doubler la sécurité côté serveur

    for n, h in zip(nets, hands):
        if h.strip() and n not in seen_networks:
            data_lines.append(f"• {n}: {h.strip()}")
            seen_networks.add(n)
    
    if len(data_lines) <= 1:
        return P("Veuillez remplir au moins un réseau.", style="color:red; font-weight:bold;")

    return generate_qr_response("\n".join(data_lines), "identite-digitale.png")

@rt("/vcard")
def get():
    content = Div(
        H2("Carte de Visite Digitale (VCard)", cls="gradient-text"),
        P("Générez un QR Code qui enregistre vos coordonnées complètes dans le répertoire de vos clients et partenaires."),
        
        Form(
            # --- BLOC : IDENTITÉ ---
            Grid(
                Div(Label("Prénom", Input(name="fn", placeholder="Ex: Jean"))),
                Div(Label("Nom", Input(name="ln", placeholder="Ex: Dupont")))
            ),
            # --- BLOC : PROFESSIONNEL ---
            Grid(
                Div(Label("Boutique / Entreprise", Input(name="org", placeholder="Ex: RetailBox SARL"))),
                Div(Label("Poste / Fonction", Input(name="title", placeholder="Ex: Gérant ou Consultant")))
            ),
            # --- BLOC : COORDONNÉES ---
            Grid(
                Div(Label("Téléphone", Input(name="tel", type="tel", placeholder="+33 6..."))),
                Div(Label("E-mail Pro", Input(name="email", type="email", placeholder="contact@pro.com")))
            ),
            # --- BLOC : RÉSEAUX & ADRESSE ---
            Grid(
                Div(Label("LinkedIn (URL)", Input(name="linkedin", placeholder="linkedin.com/in/profil"))),
                Div(Label("Site Web / Boutique", Input(name="url", type="url", placeholder="https://...")))
            ),
            Label("Adresse physique (pour GPS)", Input(name="adr", placeholder="Ex: 12 rue de la Paix, Paris")),

            Button("🚀 Générer ma Carte Pro", cls="btn-full"),
            hx_post="/gen-vcard", hx_target="#vcard-out"
        ),
        Div(id="vcard-out"),
        cls="modern-card"
    )
    return Layout(content, "VCard")

@rt("/gen-vcard", methods=["POST"])
async def post(fn:str="", ln:str="", org:str="", title:str="", tel:str="", email:str="", url:str="", adr:str="", linkedin:str=""):
    # Nettoyage simple du lien LinkedIn pour extraire l'identifiant si besoin
    li_link = linkedin.strip()
    if "linkedin.com/in/" in li_link:
        # On s'assure que le lien est bien en https pour la compatibilité
        if not li_link.startswith("http"): li_link = "https://" + li_link
    
    vcard_lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{fn} {ln}",
        f"N:{ln};{fn};;;",
        f"ORG:{org}",
        f"TITLE:{title}",
        f"TEL;TYPE=CELL,VOICE:{tel}",
        f"EMAIL;TYPE=PREF,INTERNET:{email}",
        f"URL;TYPE=Website:{url}",
        f"ADR;TYPE=WORK:;;{adr};;;;",
    ]
    
    if li_link:
        # Champ standard pour les réseaux sociaux dans les répertoires modernes (iPhone/Android)
        vcard_lines.append(f"X-SOCIALPROFILE;TYPE=linkedin:{li_link}")
        # On le remet en NOTE pour être sûr que l'utilisateur le voit s'il n'apparaît pas dans les champs
        vcard_lines.append(f"NOTE:Profil LinkedIn: {li_link}")

    vcard_lines.append("END:VCARD")
    vcard_data = "\n".join([line for line in vcard_lines if not line.endswith(":")])
    
    return generate_qr_response(vcard_data, "vcard-pro.png")
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
def get():
    
    # On définit le script pour gérer l'envoi sans redirection
    ajax_script = Script(f"""
        async function handleSubmit(event) {{
            event.preventDefault();
            const status = document.getElementById("contact-status");
            const data = new FormData(event.target);
            const btn = event.target.querySelector("button");
            
            btn.disabled = true;
            btn.innerText = "Envoi en cours...";
            
            fetch(event.target.action, {{
                method: 'POST',
                body: data,
                headers: {{ 'Accept': 'application/json' }}
            }}).then(response => {{
                if (response.ok) {{
                    status.innerHTML = "<div class='modern-card' style='background:#dcfce7; color:#166534; padding:1rem; margin-bottom:1rem; border:1px solid #166534;'>✅ Merci ! Votre message a été envoyé avec succès.</div>";
                    event.target.reset();
                }} else {{
                    status.innerHTML = "❌ Une erreur est survenue. Veuillez réessayer.";
                }}
            }}).catch(error => {{
                status.innerHTML = "❌ Erreur de connexion.";
            }}).finally(() => {{
                btn.disabled = false;
                btn.innerText = "🚀 Envoyer le message";
            }});
        }}
    """)

    content = Div(
        H2("Contactez l'équipe RetailBox", cls="gradient-text"),
        P("Une suggestion technique ou un partenariat ? Utilisez le formulaire ci-dessous."),
        
        # Zone pour afficher le message de succès/erreur
        Div(id="contact-status"),
        
        Form(
            Label("Votre adresse e-mail", 
                  Input(type="email", name="email", placeholder="votre@email.com", required=True)),
            
            Label("Sujet", 
                  Input(name="subject", placeholder="Ex: Support QR Code", required=True)),
            
            Label("Votre message", 
                  Textarea(name="message", placeholder="Comment pouvons-nous vous aider ?", rows=6, required=True)),
            
            Input(type="hidden", name="_gotcha", style="display:none"), # Anti-spam
            
            Button("🚀 Envoyer le message", type="submit", cls="btn-full"),
            
            action=f"https://formspree.io/f/{FORMSPREE_ID }",
            onsubmit="handleSubmit(event)" # On appelle le script ici
        ),
        ajax_script, # On injecte le script sur la page
        cls="modern-card", style="max-width: 700px; margin: auto; padding: 3rem;"
    )
    return Layout(content, "Contact")
@rt("/about")
def get():
    content = Div(
        H2("À propos de RetailBox", cls="gradient-text"),
        P("RetailBox est une suite d'outils techniques dédiée à l'optimisation des opérations pour le commerce moderne et les Small Businesses."),
        
        H4("Accompagner la croissance des entreprises"),
        P("""Nous centralisons les ressources critiques pour les entrepreneurs et gestionnaires de points de vente. 
          De la boutique physique au site e-commerce, nous fournissons les standards technologiques 
          indispensables pour rester compétitif dans un environnement digital en constante évolution."""),
        
        Grid(
            Div(
                H5("📦 Gestion de Stock & Inventaire"),
                P("Nous simplifions la logistique commerciale avec des générateurs de codes-barres conformes (EAN-13, Code 128). Nous facilitons l'organisation de vos stocks et l'étiquetage précis de vos produits.")
            ),
            Div(
                H5("🍽️ Solutions pour Restaurants"),
                P("Nous modernisons l'expérience client . Nous permettons un accès instantané à vos cartes et tarifs , optimisant ainsi votre service en salle.")
            )
        ),
        
        Grid(
            Div(
                H5("🌐 Identité Digitale"),
                P("Nous optimisons votre visibilité professionnelle avec des Social Cards et VCards intelligentes. Nous créons un point d'entrée unique pour regrouper vos réseaux sociaux et vos canaux de vente.")
            ),
            Div(
                H5("📸 Optimisation Produit"),
                P("Nous valorisons vos articles de vente grâce à notre IA de détourage. Nous transformons vos photos brutes en images produits de qualité studio pour vos fiches e-commerce et vos catalogues.")
            )
        ),
        
        H4("Notre engagement pour vos données"),
        P("""Nous appliquons une politique de confidentialité rigoureuse. Chaque traitement technique est 
          exécuté en mémoire vive (RAM) de manière isolée. Nous ne conservons aucune donnée commerciale, 
          photo produit ou information confidentielle sur nos serveurs. Nous garantissons votre 
          propriété exclusive sur 100% des contenus générés (UGC) via notre plateforme."""),
        
        cls="modern-card", style="max-width: 900px; margin: auto; padding: 3rem; line-height: 1.8;"
    )
    return Layout(content, "À Propos")

@rt("/faq")
def get():
    content = Div(
        H2("Foire aux Questions (FAQ)", cls="gradient-text"),
        P("Retrouvez toutes les réponses pour optimiser votre commerce avec nos outils digitaux."),
        
        Div(
            *[Details(
                Summary(item["q"]), 
                # On utilise NotStr pour permettre le HTML (les liens) dans la réponse
                P(NotStr(item["a"]))
              ) for item in faq_data],
            
        ),
        
        # Petit call-to-action en bas de FAQ
        Div(
            H4("Vous ne trouvez pas votre réponse ?"),
            A(Button("Contactez notre support gratuit", cls="outline"), href="/contact"),
            style="margin-top: 3rem; text-align: center;"
        ),
        
        cls="modern-card", style="max-width: 900px; margin: auto; padding: 3rem;"
    )
    return Layout(content, "FAQ")

@rt("/guide")
def get():
    # Mapping sur guide_data avec un style "Documentation Pro"
    guide_cards = Div(*[
        Div(
            # En-tête de carte : Icône + Titre alignés
            Div(
                Safe(f'<i data-lucide="{item["icon"]}" style="width:32px; height:32px; color:var(--primary); stroke-width:2.5px;"></i>'),
                H4(item["title"]),
                style="display:flex; align-items:center; gap:15px; margin-bottom:0.5rem;"
            ),
            # Description avec support des liens SEO
            P(NotStr(item["desc"])),
            
            # Bouton d'action en bas de carte
            A(Button(f"Utiliser l'outil {item['title']}", cls="outline"), 
              href=item["link"], style="margin-top:auto;"),
            
            cls="guide-card"
        ) for item in guide_data
    ], cls="guide-grid")

    content = Div(
        # Header de la page
        Div(
            H2("Guide d'utilisation professionnel", cls="gradient-text", style="font-size:3rem;"),
            P("Apprenez à configurer vos outils pour une performance maximale en boutique et en ligne.", 
              style="font-size:1.2rem; opacity:0.8;"),
            style="margin-bottom:4rem; text-align:center;"
        ),
        
        # La Grille de guides
        guide_cards,
        
        # Section de conseils techniques "Expert"
        Div(
            H3("💡 Conseils d'expert pour le Retail", style="margin-bottom:1.5rem;"),
            Grid(
                Div(
                    H5("Qualité d'impression"),
                    P("Pour vos codes-barres EAN-13, utilisez une imprimante thermique à 300 DPI minimum pour éviter les erreurs de lecture en caisse.")
                ),
                Div(
                    H5("Format de fichier"),
                    P("Privilégiez le format PNG pour vos QR Codes de menu restaurant. Il conserve la netteté des pixels même lors d'un agrandissement sur support rigide.")
                ),
                Div(
                    H5("Optimisation IA"),
                    P("Le détourage automatique (RemBg) est optimal lorsque le produit est photographié sur un fond uni, même s'il n'est pas parfaitement blanc.")
                )
            ),
            cls="modern-card", 
            style="margin-top:5rem; padding:3rem; border-left: 6px solid var(--primary); background: rgba(79, 70, 229, 0.03);"
        ),
        style="padding: 2rem 0;"
    )
    return Layout(content, "Guide")
if __name__ == "__main__":
    import uvicorn
   
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))