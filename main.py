import random
import sqlite3
import string
import urllib.parse

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
from constants import ABOUT_DATA, CONTACT_DATA, CURRENT_YEAR, FOOTER_DATA, I18N_PATTERNS, LEGAL_CONTENT, LOCALES, SOCIAL_NETWORKS, MULTILINGUAL_DATA_FaqGuide, MULTILINGUAL_DATA_MetaTags, MULTILINGUAL_DATA_Services, services,faq_data,adsense_script_src,ga_lib_src,guide_data
from db import init_db
from styles import styles

#reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from supabase import create_client, Client
import os

# Ces valeurs sont lues depuis les secrets Hugging Face

from supabase import create_client, Client
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except:
        print("Erreur d'initialisation Supabase")

load_dotenv() 
#init_db()

os.environ['U2NET_HOME'] = '/tmp'
FORMSPREE_ID = os.environ.get("FORMSPREE_ID", "TON_ID_DE_TEST")

# --- CONFIGURATION ---


adsense_script = Script(
    src=adsense_script_src,
    async_=True,
    crossorigin="anonymous"
)

# Le petit losange (hexagone) de ton logo en format favicon
favicon_link = Link(rel="icon", type="image/svg+xml", href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234f46e5' stroke-width='3'><path d='M21 16V8l-9-5-9 5v8l9 5 9-5z'></path></svg>")

# --- SEO & META TAGS ---
# --- SEO & META TAGS ---



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

app, rt = fast_app(
    static_path='public', 
    hdrs=(
        favicon_link,
        # On garde le CSS et les outils tiers ici
        Link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"), 
        custom_style,
        ga_lib, ga_config, adsense_script, 
        Script(src="https://unpkg.com/lucide@latest"),
        Script("""
            document.body.addEventListener('htmx:afterSwap', function(evt) {
                lucide.createIcons();
            });
        """)
    )
)



def get_translated_metas(lang):
    m = MULTILINGUAL_DATA_MetaTags[lang]['meta']
    return (
        Title(m['title']),
        Meta(name="description", content=m['desc']),
        Meta(name="keywords", content=m['keywords']),
        
        # Open Graph (Facebook / WhatsApp)
        Meta(property="og:title", content=m['og_title']),
        Meta(property="og:description", content=m['og_desc']),
        Meta(property="og:image", content="https://baadjis-utilitybox.hf.space/og-banner.png?v=4"),
        Meta(property="og:url", content="https://baadjis-utilitybox.hf.space"),
        Meta(property="og:type", content="website"),
        Meta(property="og:site_name", content="RetailBox"),
        
        # Twitter
        Meta(name="twitter:card", content="summary_large_image"),
        Meta(name="twitter:title", content=m['og_title']),
        Meta(name="twitter:description", content=m['og_desc']),
        
        # Mobile & Theme
        Meta(name="viewport", content="width=device-width, initial-scale=1, maximum-scale=1"),
        Meta(name="color-scheme", content="light")
    )

# --- COMPOSANTS ---

def Logo():
    return Div(
        Safe(f'<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="url(#grad)" stroke-width="3"><defs><linearGradient id="grad"><stop offset="0%" stop-color="#4f46e5"/><stop offset="100%" stop-color="#9333ea"/></linearGradient></defs><path d="M21 16V8l-9-5-9 5v8l9 5 9-5z"></path></svg>'),
         H1("RetailBox", cls="gradient-text", 
           style="margin:0; font-size:1.2rem; font-weight:800;"), # gradient-text gère sa propre couleur
        style="display:flex; align-items:center; gap:5px; flex-shrink: 0;"
    )

def LegalPage(page_key, lang='fr'):
    data = LEGAL_CONTENT[lang][page_key]
    
    # Construction dynamique des sections
    sections_html = []
    for sec in data['sections']:
        elements = [H4(sec['h']), P(sec['p'])]
        if 'li' in sec:
            elements.append(Ul(*[Li(item) for item in sec['li']]))
        sections_html.append(Div(*elements))

    return Div(
        H2(data['title']),
        P(data['date'], style="opacity: 0.6; font-size: 0.85rem;"),
        *sections_html,
        cls="modern-card"
    )

def FooterSection(lang='fr'):
    d = FOOTER_DATA[lang]
    l = d['links']
    
    return Footer(
        # Section supérieure : 3 colonnes d'informations
        Div(
            Div(H4(d['h_usage']), P(d['p_usage']), cls="footer-section"),
            Div(H4(d['h_privacy']), P(d['p_privacy']), cls="footer-section"),
            Div(H4(d['h_ugc']), P(d['p_ugc']), cls="footer-section"),
            cls="footer-content"
        ),
        
        # Section inférieure : Liens de navigation et mentions légales
        Div(
            A(l['about'], href="/about"),
            A(l['guide'], href="/guide"),
            A(l['faq'], href="/faq"), 
            A(l['terms'], href="/terms"), 
            A(l['privacy'], href="/privacy"), 
            A(l['ugc'], href="/ugc"), 
            A(l['contact'], href="/contact"),
            Span(f"© {CURRENT_YEAR} RetailBox"),
            cls="legal-links"
        ),
        cls="pro-footer"
    )

def LangSwitcher(current_lang):
    target_lang = 'en' if current_lang == 'fr' else 'fr'
    label = "🇬🇧 EN" if current_lang == 'fr' else "🇫🇷 FR"
    return A(label, href=f"/set-lang/{target_lang}", cls="lang-btn", 
             style="""
                border: 2px solid var(--primary) !important;
                background: transparent !important;
                color: var(--primary) !important;
                border-radius: 12px !important;
                font-weight: 800;
                padding: 0.4rem 0.8rem;
                text-decoration: none !important;
             """)

def Layout(content, active_page, session, title="RetailBox"):
    lang = session.get('lang', 'fr')
    t = LOCALES[lang]
    page_metas = get_translated_metas(lang)
    # On ajoute "Contact" et "Dashboard" si besoin pour un menu complet
    nav_items = [
        (t['home'], "/", "home"), 
        (t['guide'], "/guide", "book-open"), 
        (t['faq'], "/faq", "help-circle"), 
        (t['about'], "/about", "info")
    ]
    
    return page_metas, Title(f"{active_page} | {title}"), Main(
        Header(
            Div(
                # 1. LOGO (Centré sur mobile via .logo-wrap)
                Div(Logo(), cls="logo-wrap"),
                
                # 2. CONTENEUR NAV + LANG (Une ligne sur mobile)
                Div(
                    Div(
                        Nav(
                            Div(*[A(Safe(f'<i data-lucide="{icon}" style="width:16px"></i> {name}'), 
                                   href=url, 
                                   cls="active" if active_page == name else "") 
                                 for name, url, icon in nav_items], 
                                cls="nav-pills")
                        ),
                        cls="nav-scroll-container"
                    ),
                    LangSwitcher(lang), # Langue à droite de la nav
                    cls="nav-lang-container"
                ),
                cls="top-nav-bar"
            )
        ),
        
        # Le reste du contenu descend un peu pour laisser la place au header fixe
        Div(
            Div(H1(t['hero_title'], cls="hero-title gradient-text"), style="margin-bottom:2rem;"),
            
            Div(P("Publicité", style="font-size:0.6rem; opacity:0.5; margin:0"), cls="top-ad-banner"),
            
            Div(
                Section(content), 
                Aside(Div(P("Publicité"), style="background:rgba(0,0,0,0.02); border:1px dashed #ccc; border-radius:20px; min-height:300px; display:flex; align-items:center; justify-content:center;"), cls="sidebar"), 
                cls="app-grid"
            ),
            
            FooterSection(lang=lang),
            cls="container"
        ),
        Script("lucide.createIcons();")
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

#datarow for barcode 
def DataRow(prefix, lang='fr'):
    t = I18N_PATTERNS[lang]['barcode']
    return Div(
        Input(name=f"{prefix}_keys", placeholder=t['ph_key'], maxlength="15"),
        Input(name=f"{prefix}_vals", placeholder=t['ph_val'], maxlength="30", required=True),
        Button(Safe('<i data-lucide="trash-2"></i>'), type="button", 
               onclick="this.parentElement.remove();", 
               style="width:40px; background:transparent !important; border:none; color:#ef4444;"),
        cls="key-value-row", 
        style="display:grid; grid-template-columns: 1fr 1fr 40px; gap:8px; margin-top:10px;"
    )
#social row
def SocialRow(lang='fr'):
    t = I18N_PATTERNS[lang]['common']
    return Div(
        # Le Select utilise la liste globale SOCIAL_NETWORKS
        Select(*[Option(label, value=val) for val, label in SOCIAL_NETWORKS], 
               name="social_networks", onchange="checkDuplicates()"),
        
        Input(name="social_handles", placeholder=t['placeholder_url'], required=True),
        
        Button(
            Safe(f'<i data-lucide="trash-2" style="width:18px"></i> {t["btn_remove"]}'), 
            type="button", 
            onclick="this.parentElement.remove(); checkDuplicates();", 
            cls="btn-remove-final"
        ),
        cls="social-row"
    )


#soldes 
def generate_pdf_sheet(label_pil_img):
    """
    Prend une image d'étiquette et crée un PDF A4 avec 24 étiquettes (3x8).
    """
    buffer = BytesIO()
    # Création du canvas ReportLab (A4 : 210mm x 297mm)
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Dimensions d'une étiquette sur le PDF (environ 70mm x 37mm)
    label_w = 65 * mm
    label_h = 35 * mm
    
    # Marges et espacements
    margin_x = 7 * mm
    margin_y = 15 * mm
    gap_x = 2 * mm
    gap_y = 0 * mm

    # On transforme l'image PIL en format lisible par ReportLab
    img_byte_arr = BytesIO()
    label_pil_img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    from reportlab.lib.utils import ImageReader
    img_reader = ImageReader(img_byte_arr)

    # Boucle pour placer les 24 étiquettes (3 colonnes x 8 lignes)
    for row in range(8):
        for col in range(3):
            x = margin_x + col * (label_w + gap_x)
            y = height - (margin_y + (row + 1) * label_h) # ReportLab commence en bas
            c.drawImage(img_reader, x, y, width=label_w, height=label_h)

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# --- ROUTES ACCUEIL ---

@rt("/")
def get(session):
    # 1. Détection de la langue
    lang = session.get('lang', 'fr')
    t = MULTILINGUAL_DATA_Services[lang]
    
    # 2. Génération dynamique des 9 cartes à partir de la liste 'services'
    cards_html = Div(*[
        Card(
            # En-tête : Icône + Titre alignés (32px comme demandé)
            Div(
                Safe(f'<i data-lucide="{s["icon"]}" style="width:32px; height:32px; color:var(--primary);"></i>'), 
                H3(s["title"], style="margin:0; font-size:1.1rem;"), 
                cls="card-header-flex"
            ),
            # Description traduisible
            P(s["desc"], style="font-size:0.9rem;"),
            # Pied de carte : Bouton Full-Width
            Footer(
                A(Button(t['btn_open'], cls="btn-full"), href=s["link"])
            ), 
            cls="modern-card"
        ) for s in t['services']
    ], cls="services-grid")
    
    # 3. Assemblage du contenu de la page
    content = Div(
        cards_html,
        
        # Section SEO avant le footer
        H2(t['home_title'], style="margin-top:4rem; text-align:center;"),
        P(t['home_sub'], style="text-align:center; opacity:0.7;")
    )
    
    return Layout(content, "Accueil" if lang == 'fr' else "Home", session)

#about 

@rt("/about")
def get(session):
    # Récupération de la langue (fr par défaut)
    lang = session.get('lang', 'fr')
    d = ABOUT_DATA[lang]
    
    content = Div(
        H2(d['title'], cls="gradient-text"),
        P(d['intro']),
        
        H4(d['mission_h']),
        P(d['mission_p']),
        
        Grid(
            Div(H5(d['stock_h']), P(d['stock_p'])),
            Div(H5(d['restau_h']), P(d['restau_p']))
        ),
        
        Grid(
            Div(H5(d['id_h']), P(d['id_p'])),
            Div(H5(d['prod_h']), P(d['prod_p']))
        ),
        
        H4(d['privacy_h']),
        P(d['privacy_p']),
        
        cls="modern-card", 
        style="max-width: 900px; margin: auto; padding: 3rem; line-height: 1.8;"
    )
    
    # On passe bien la session au Layout pour le menu
    return Layout(content, "À Propos" if lang == 'fr' else "About", session)
# --- OUTILS ---
#digital id 
@rt("/add-social-row")
def get(session):
    lang = session.get('lang', 'fr')
    return SocialRow(lang)

@rt("/digital-id")
def get(session):
    lang = session.get('lang', 'fr')
    t_common = I18N_PATTERNS[lang]['common']
    t_spec = I18N_PATTERNS[lang]['social']

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
        H2(t_spec['title'], cls="gradient-text"),
        P(t_spec['sub']),
        Form(
            # 1. ZONE DES INPUTS (Ligne initiale générée avec la bonne langue)
            Div(SocialRow(lang), id="social-list"),
            
            # 2. ZONE DES ACTIONS
            Div(
                Button(t_common['btn_add'], type="button", 
                       hx_get="/add-social-row", hx_target="#social-list", hx_swap="beforeend", cls="outline"),
                
                Button(t_spec['title'], type="submit", cls="btn-full"), # On réutilise le titre pour le bouton
                
                style="margin-top: 2rem; border-top: 1px solid #e2e8f0; padding-top: 2rem;"
            ),
            hx_post="/gen-id", hx_target="#id-out"
        ),
        Div(id="id-out"), js_logic, cls="modern-card"
    )
    return Layout(content, t_spec['title'], session)
@rt("/gen-id", methods=["POST"])
async def post(session, social_networks: list = None, social_handles: list = None):
    lang = session.get('lang', 'fr')
    t_common = I18N_PATTERNS[lang]['common']
    t_spec = I18N_PATTERNS[lang]['social']
    
    nets = [social_networks] if isinstance(social_networks, str) else (social_networks or [])
    hands = [social_handles] if isinstance(social_handles, str) else (social_handles or [])
    
    data_lines = [t_spec['qr_header']]
    seen_networks = set()

    for n, h in zip(nets, hands):
        if h.strip() and n not in seen_networks:
            data_lines.append(f"• {n}: {h.strip()}")
            seen_networks.add(n)
    
    if len(data_lines) <= 1:
        return P(t_common['error_empty'], style="color:red; font-weight:bold;")

    # On utilise ta fonction generate_qr_response stable
    return generate_qr_response("\n".join(data_lines), t_spec['filename'])
#vcard
@rt("/vcard")
def get(session):
    lang = session.get('lang', 'fr')
    t = I18N_PATTERNS[lang]['vcard']
    
    content = Div(
        H2(t['title'], cls="gradient-text"),
        P(t['sub']),
        
        Form(
            # --- BLOC : IDENTITÉ ---
            Grid(
                Div(Label(t['fn'], Input(name="fn", placeholder="Ex: Jean" if lang=='fr' else "Ex: John"))),
                Div(Label(t['ln'], Input(name="ln", placeholder="Ex: Dupont" if lang=='fr' else "Ex: Doe")))
            ),
            # --- BLOC : PROFESSIONNEL ---
            Grid(
                Div(Label(t['org'], Input(name="org", placeholder="Ex: RetailBox SARL"))),
                Div(Label(t['job'], Input(name="title", placeholder="Ex: Gérant" if lang=='fr' else "Ex: Manager")))
            ),
            # --- BLOC : COORDONNÉES ---
            Grid(
                Div(Label(t['tel'], Input(name="tel", type="tel", placeholder="+33..."))),
                Div(Label(t['email'], Input(name="email", type="email", placeholder="contact@pro.com")))
            ),
            # --- BLOC : RÉSEAUX & ADRESSE ---
            Grid(
                Div(Label(t['li'], Input(name="linkedin", placeholder="linkedin.com/in/..."))),
                Div(Label(t['web'], Input(name="url", type="url", placeholder="https://...")))
            ),
            Label(t['adr'], Input(name="adr", placeholder="Ex: 12 rue de la Paix, Paris")),

            Button(t['btn'], cls="btn-full", type="submit"),
            hx_post="/gen-vcard", hx_target="#vcard-out"
        ),
        Div(id="vcard-out"),
        cls="modern-card"
    )
    return Layout(content, t['title'], session)

@rt("/gen-vcard", methods=["POST"])
async def post(session, fn:str="", ln:str="", org:str="", title:str="", tel:str="", email:str="", url:str="", adr:str="", linkedin:str=""):
    lang = session.get('lang', 'fr')
    t = I18N_PATTERNS[lang]['vcard']
    
    # Nettoyage LinkedIn pour compatibilité mobile
    li_link = linkedin.strip()
    if li_link and "linkedin.com" in li_link and not li_link.startswith("http"):
        li_link = "https://" + li_link
    
    # Construction du format VCard 3.0
    vcard_lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"FN:{fn} {ln}",
        f"N:{ln};{fn};;;",
        f"ORG:{org}",
        f"TITLE:{title}",
        f"TEL;TYPE=CELL,VOICE:{tel}",
        f"EMAIL;TYPE=PREF,INTERNET:{email}",
        f"URL:{url}",
        f"ADR;TYPE=WORK:;;{adr};;;;",
    ]
    
    if li_link:
        # Ajout du profil social (reconnu par iOS/Android moderne)
        vcard_lines.append(f"X-SOCIALPROFILE;TYPE=linkedin:{li_link}")
        vcard_lines.append(f"NOTE:LinkedIn: {li_link}")

    vcard_lines.append("END:VCARD")
    
    # On filtre les lignes vides pour éviter un QR trop dense
    final_data = "\n".join([line for line in vcard_lines if not line.strip().endswith(":")])
    
    return generate_qr_response(final_data, t['filename'])

#whatsapp
@rt("/whatsapp-qr")
def get(session):
    lang = session.get('lang', 'fr')
    t = I18N_PATTERNS[lang]['whatsapp']
    
    content = Div(
        H2(t['title'], cls="gradient-text"),
        P(t['sub']),
        
        Form(
            Label(t['label_tel'], 
                  Input(name="phone", placeholder=t['ph_tel'], required=True, type="tel")),
            
            Label(t['label_msg'], 
                  Textarea(name="msg", placeholder=t['ph_msg'], rows=3)),
            
            P("Note : N'ajoutez pas de '+' ou de '00' au début du numéro.", 
              style="font-size:0.8rem; opacity:0.6; margin-top:-10px;"),

            Button(t['btn'], cls="btn-full", type="submit"),
            hx_post="/gen-wa", hx_target="#wa-out"
        ),
        Div(id="wa-out"),
        cls="modern-card"
    )
    return Layout(content, t['title'], session)




@rt("/gen-wa", methods=["POST"])
async def post(session, phone:str, msg:str=""):
    lang = session.get('lang', 'fr')
    t = I18N_PATTERNS[lang]['whatsapp']
    
    # 1. Nettoyage du numéro de téléphone
    clean_phone = "".join(filter(str.isdigit, phone))
    
    # 2. Encodage du message pour l'URL
    encoded_msg = urllib.parse.quote(msg.strip())
    
    # 3. Construction du lien de l'API WhatsApp
    wa_link = f"https://wa.me/{clean_phone}"
    if encoded_msg:
        wa_link += f"?text={encoded_msg}"
    
    # 4. Appel de ta fonction stable de génération
    return generate_qr_response(wa_link, t['filename'])

@rt("/soldes")
def get(session):
    lang = session.get('lang', 'fr')
    t = I18N_PATTERNS[lang]['soldes']
    
    content = Div(
        H2(t['title'], cls="gradient-text"),
        P(t['sub']),
        
        Form(
            Label(t['label_item'], 
                  Input(name="item", placeholder=t['ph_item'], required=True)),
            
            Grid(
                Div(Label(t['label_old'], Input(name="old_p", placeholder="Ex: 59", type="number", step="0.01"))),
                Div(Label(t['label_new'], Input(name="new_p", placeholder="Ex: 39", type="number", step="0.01")))
            ),
            
            Label(t['label_code'], 
                  Input(name="code", placeholder="366123456789", required=True, maxlength="12")),
            
            Button(t['btn'], type="submit", cls="btn-full"),
            
            hx_post="/gen-soldes", 
            hx_target="#soldes-result",
            hx_indicator="#loading-soldes"
        ),
        
        Div(id="loading-soldes", cls="htmx-indicator", aria_busy="true", style="text-align:center; margin-top:1rem;"),
        Div(id="soldes-result"),
        
        cls="modern-card"
    )
    return Layout(content, t['title'], session)

@rt("/gen-soldes", methods=["POST"])
async def post(session, item:str, old_p:str, new_p:str, code:str):
    lang = session.get('lang', 'fr')
    t = I18N_PATTERNS[lang]['soldes']
    
    try:
        # --- 1. GÉNÉRATION DE L'IMAGE (Logic intacte) ---
        bc_class = barcode.get_barcode_class('ean13')
        buf_bc = BytesIO()
        bc_class(code, writer=ImageWriter()).write(buf_bc)
        bc_img = Image.open(buf_bc).resize((300, 150))
        
        tag = Image.new('RGB', (400, 400), color='white')
        d = ImageDraw.Draw(tag)
        d.text((20, 20), f"{item[:25]}", fill="black")
        d.text((20, 60), f"{old_p}€", fill="red")
        d.line((15, 75, 100, 75), fill="red", width=3)
        d.text((20, 100), f"{new_p}€", fill="black")
        tag.paste(bc_img, (50, 200))

        # --- 2. CRÉATION DU PDF PLANCHE ---
        # On utilise ta fonction generate_pdf_sheet définie précédemment
        pdf_buffer = generate_pdf_sheet(tag)
        pdf_base64 = base64.b64encode(pdf_buffer.read()).decode()

        # --- 3. RENDU HTML TRADUIT ---
        buf_f = BytesIO()
        tag.save(buf_f, format="PNG")
        img_s = base64.b64encode(buf_f.getvalue()).decode()
        
        return Div(
            H4(t['preview']),
            Img(src=f"data:image/png;base64,{img_s}", style="max-width:200px; border:1px solid #ccc; margin:auto;"),
            Grid(
                A(Button(t['dl_png'], cls="outline"), 
                  href=f"data:image/png;base64,{img_s}", download="etiquette.png"),
                
                A(Button(t['dl_pdf'], cls="btn-full"), 
                  href=f"data:application/pdf;base64,{pdf_base64}", download="planche-retailbox.pdf")
            ),
            style="text-align:center; padding:1.5rem; background: rgba(0,0,0,0.02); border-radius:24px; margin-top:2rem;"
        )
    except:
        return P(t['error'], style="color:red; font-weight:bold;")


@rt("/barcode-tab")
def get(session):
    lang = session.get('lang', 'fr')
    t = I18N_PATTERNS[lang]['barcode']
    
    content = Div(
        H2(t['title'], cls="gradient-text"),
        P(t['sub']),
        Form(
            Label(t['label_format'],
                Select(
                    Option(t['opt_ean'], value="ean13"),
                    Option(t['opt_128'], value="code128", selected=True),
                    name="t", 
                    hx_get="/bc-f", 
                    hx_target="#f",
                    hx_trigger="load, change" 
                )
            ),
            Div(id="f", style="margin-bottom:20px;"),
            Button(t['btn_gen'], cls="btn-full", type="submit"),
            hx_post="/gen-bc", hx_target="#o"
        ),
        Div(id="o"),
        cls="modern-card"
    )
    return Layout(content, "Barcode", session)

@rt("/bc-f")
def get(session, t:str):
    lang = session.get('lang', 'fr')
    p = I18N_PATTERNS[lang]['barcode']
    
    if t == "ean13":
        return Div(
            Input(name="d", placeholder=p['ph_ean'], required=True,
                  maxlength="12", minlength="12", pattern="[0-9]{12}",
                  oninput="this.value = this.value.replace(/[^0-9]/g, '');"),
            P(p['ean_info'], style="font-size:0.8rem; opacity:0.7; margin-top:5px;")
        )
    
    return Div(
        Div(DataRow("bc", lang), id="bc-kv-list"),
        Button(p['btn_add'], type="button", 
               hx_get="/add-bc-row", hx_target="#bc-kv-list", hx_swap="beforeend",
               cls="outline secondary", style="width:100%; margin-top:10px;"),
        id="bc-kv-container"
    )

@rt("/add-bc-row")
def get(session): 
    return DataRow("bc", session.get('lang', 'fr'))


@rt("/gen-bc", methods=["POST"])
async def post(session, t:str, d:str=None, bc_keys:list=None, bc_vals:list=None):
    lang = session.get('lang', 'fr')
    p = I18N_PATTERNS[lang]['barcode']
    
    try:
        final_data = ""
        if t == "ean13":
            final_data = d.strip()
            if not final_data.isdigit() or len(final_data) != 12:
                return P(p['err_ean'], style="color:red; font-weight:bold; border:1px solid red; padding:10px; border-radius:10px;")
        else:
            keys = [bc_keys] if isinstance(bc_keys, str) else (bc_keys or [])
            vals = [bc_vals] if isinstance(bc_vals, str) else (bc_vals or [])
            pairs = [f"{k}:{v}" for k, v in zip(keys, vals) if k and k.strip()]
            final_data = " ".join(pairs)
            
            if not final_data: return P(p['err_empty'], style="color:red;")
            if len(final_data) > 60: return P(p['err_long'], style="color:red;")

        # Génération de l'image
        bc_class = barcode.get_barcode_class(t)
        buf = BytesIO()
        bc_class(final_data, writer=ImageWriter()).write(buf)
        s = base64.b64encode(buf.getvalue()).decode()
        
        return Div(
            Img(src=f"data:image/png;base64,{s}", style="max-width:100%; border:1px solid #e2e8f0; border-radius:10px; background: white;"),
            P(f"{p['encoded']} {final_data}", style="font-size:0.8rem; margin-top:0.5rem; font-family:monospace;"),
            A(Button(p['dl'], cls="btn-full"), href=f"data:image/png;base64,{s}", download="barcode-retailbox.png"),
            style="text-align:center; padding-top:1.5rem;"
        )
    except Exception as e:
        return P(f"Error: {str(e)}", style="color:red; font-weight:bold;")
    
#rembg
@rt("/rembg-tab")
def get(session):
    lang = session.get('lang', 'fr')
    t = I18N_PATTERNS[lang]['rembg']
    
    content = Div(
        H2(t['title'], cls="gradient-text"),
        P(t['sub']),
        
        Form(
            Label(t['label_file'], 
                  Input(type="file", name="image", accept="image/*", required=True)),
            
            Button(t['btn_run'], type="submit", cls="btn-full"),
            
            hx_post="/gen-bg", 
            hx_target="#rembg-result",
            hx_indicator="#loading-ai",
            enctype="multipart/form-data"
        ),
        
        # Indicateur de chargement stylisé
        Div(id="loading-ai", cls="htmx-indicator", aria_busy="true", 
            style="text-align:center; margin-top:1.5rem;"),
        
        # Zone de résultat
        Div(id="rembg-result"),
        
        cls="modern-card"
    )
    return Layout(content, "RemBg", session)

@rt("/gen-bg", methods=["POST"])
async def post(session, image: UploadFile):
    lang = session.get('lang', 'fr')
    t = I18N_PATTERNS[lang]['rembg']
    
    try:
        # 1. Lecture et traitement IA
        input_data = await image.read()
        output_data = remove(input_data)
        
        # 2. Encodage Base64
        s = base64.b64encode(output_data).decode()
        
        # 3. Rendu HTML avec boutons larges et visibilité iPhone
        return Div(
            H4(t['success'], style="margin-top:2rem;"),
            # Aperçu de l'image détourée
            Img(src=f"data:image/png;base64,{s}", 
                style="max-width:100%; border: 2px solid #e2e8f0; border-radius:16px; background: white; margin: 1rem auto; display: block;"),
            
            # Bouton de téléchargement Full-Width
            A(Button(t['dl_btn'], cls="btn-full"), 
              href=f"data:image/png;base64,{s}", 
              download=t['filename']),
            
            style="text-align:center; padding:1.5rem; background: rgba(0,0,0,0.02); border-radius:24px; margin-top:2rem;"
        )
    except Exception as e:
        return P(f"Erreur : {str(e)}", style="color:red; font-weight:bold;")
    



#qrcode
@rt("/qr-tab")
def get(session):
    lang = session.get('lang', 'fr')
    t = I18N_PATTERNS[lang]['qr']
    
    content = Div(
        H2(t['title'], cls="gradient-text"),
        P(t['sub']),
        Form(
            Label(t['label_type'], 
                Select(
                    Option(t['opt_url'], value="url", selected=True), 
                    Option(t['opt_kv'], value="kv"), 
                    name="qr_mode", 
                    hx_get="/qr-fields", 
                    hx_target="#qr-inputs",
                    hx_trigger="load, change"
                )
            ),
            # Injection dynamique
            Div(id="qr-inputs", style="margin-bottom:20px;"),
            
            # Grille de couleurs
            Grid(
                Div(Label(t['label_fc'], Input(type="color", name="fc", value="#000000"))),
                Div(Label(t['label_bc'], Input(type="color", name="bc", value="#ffffff")))
            ),
            
            Label(t['label_logo'], Input(type="file", name="logo", accept="image/*")),
            
            Button(t['btn_gen'], cls="btn-full", type="submit"),
            hx_post="/gen-qr", hx_target="#qr-result", enctype="multipart/form-data"
        ),
        Div(id="qr-result"),
        cls="modern-card"
    )
    return Layout(content, "QR Pro", session)

@rt("/qr-fields")
def get(session, qr_mode:str):
    lang = session.get('lang', 'fr')
    t = I18N_PATTERNS[lang]['qr']
    t_common = I18N_PATTERNS[lang]['common']
    
    if qr_mode == "url":
        return Input(name="url", placeholder=t['ph_url'], required=True)
    
    return Div(
        Div(DataRow("qr", lang), id="qr-kv-list"),
        Button(t_common['btn_add'], type="button", 
               hx_get="/add-qr-row", hx_target="#qr-kv-list", hx_swap="beforeend",
               cls="outline secondary", style="width:100%; margin-top:10px;"),
        id="qr-kv-container"
    )

@rt("/add-qr-row")
def get(session): 
    return DataRow("qr", session.get('lang', 'fr'))

@rt("/gen-qr", methods=["POST"])
async def post(session, qr_mode:str, fc:str, bc:str, url:str=None, qr_keys:list=None, qr_vals:list=None, logo:UploadFile=None):
    lang = session.get('lang', 'fr')
    t = I18N_PATTERNS[lang]['qr']
    
    try:
        # 1. Préparation des données
        if qr_mode == "url":
            final_data = url.strip() if url else ""
        else:
            keys = [qr_keys] if isinstance(qr_keys, str) else (qr_keys or [])
            vals = [qr_vals] if isinstance(qr_vals, str) else (qr_vals or [])
            lines = [f"{k}: {v}" for k, v in zip(keys, vals) if k and k.strip()]
            final_data = "\n".join(lines)

        if not final_data: 
            return P(t['err_empty'], style="color:red; font-weight:bold;")

        # 2. Création du QR Code (High Correction pour le logo)
        qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
        qr.add_data(final_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fc, back_color=bc).convert('RGB')
        
        # 3. Traitement du Logo
        if logo and logo.size > 0:
            log_img = Image.open(BytesIO(await logo.read()))
            # Redimensionnement (max 20% de la surface)
            logo_size = img.size[0] // 5
            log_img.thumbnail((logo_size, logo_size), Image.LANCZOS)
            pos = ((img.size[0] - log_img.size[0]) // 2, (img.size[1] - log_img.size[1]) // 2)
            img.paste(log_img, pos)
            
        # 4. Conversion et Rendu
        buf = BytesIO()
        img.save(buf, format="PNG")
        s = base64.b64encode(buf.getvalue()).decode()
        
        return Div(
            Img(src=f"data:image/png;base64,{s}", 
                style="max-width:250px; margin: 2rem auto; border: 2px solid #e2e8f0; border-radius:16px; display:block; background: white;"),
            A(Button(t['dl_btn'], cls="btn-full"), 
              href=f"data:image/png;base64,{s}", download=t['filename']),
            style="text-align:center; padding-top:1.5rem;"
        )
    except Exception as e:
        return P(f"Error: {str(e)}", style="color:red;")

#wifi qr 
@rt("/wifi-qr")
def get(session):
    lang = session.get('lang', 'fr')
    t = I18N_PATTERNS[lang]['wifi']
    
    content = Div(
        H2(t['title'], cls="gradient-text"),
        P(t['sub']),
        
        Form(
            Label(t['label_ssid'], 
                  Input(name="ssid", placeholder=t['ph_ssid'], required=True)),
            
            Grid(
                Div(Label(t['label_pass'], 
                          Input(name="password", type="password", placeholder=t['ph_pass']))),
                Div(Label(t['label_type'], 
                          Select(Option("WPA/WPA2", value="WPA"), 
                                 Option("WEP", value="WEP"), 
                                 Option("Aucune (Ouvert)", value="nopass"), 
                                 name="encryption")))
            ),
            
            P(t['tip'], style="font-size:0.85rem; opacity:0.7; margin-top:10px;"),

            Button(t['btn'], cls="btn-full", type="submit"),
            hx_post="/gen-wifi", hx_target="#wifi-out"
        ),
        Div(id="wifi-out"),
        cls="modern-card"
    )
    return Layout(content, "Wi-Fi", session)

# --- ROUTE : PAGE DU FORMULAIRE ---
@rt("/shortener")
def get():
    content = Div(
        H2("RetailLink : Réducteur de liens pro", cls="gradient-text"),
        P("Créez des URLs mémorables sous le domaine ", B("rtbx.space"), " et suivez l'engagement de vos clients en temps réel."),
        
        Form(
            Label("Lien de destination (URL longue)", 
                  Input(name="url", type="url", placeholder="https://votre-boutique.com/produit-tres-long", required=True)),
            
            Label("Alias personnalisé (Optionnel)", 
                  Input(name="custom_code", 
                        placeholder="Ex: promo-printemps", 
                        maxlength="20",
                        oninput="this.value = this.value.replace(/[^a-zA-Z0-9-_]/g, '').toLowerCase();")),
            P("Laissez vide pour un code aléatoire. Pas d'espaces, uniquement lettres, chiffres et tirets.", 
              style="font-size:0.8rem; opacity:0.6;"),
            
            Button("🚀 Réduire et activer sur rtbx.space", cls="btn-full"),
            hx_post="/gen-short", hx_target="#short-result", hx_indicator="#loading-short"
        ),
        Div(id="loading-short", cls="htmx-indicator", aria_busy="true", style="text-align:center;"),
        Div(id="short-result"),
        cls="modern-card"
    )
    return Layout(content, "Shortener")

@rt("/gen-wifi", methods=["POST"])
async def post(session, ssid:str, password:str="", encryption:str="WPA"):
    lang = session.get('lang', 'fr')
    t = I18N_PATTERNS[lang]['wifi']
    
    # Construction du format standard Wi-Fi QR
    # WIFI:T:WPA;S:mon_reseau;P:mon_mdp;;
    if encryption == "nopass":
        wifi_data = f"WIFI:S:{ssid};T:;P:;;"
    else:
        wifi_data = f"WIFI:T:{encryption};S:{ssid};P:{password};;"
    
    # Appel de la fonction universelle de génération
    return generate_qr_response(wifi_data, t['filename'])

# --- ROUTE : LOGIQUE DE GÉNÉRATION ---
@rt("/gen-short", methods=["POST"])
async def post(session, url: str, custom_code: str):
    lang = session.get('lang', 'fr')
    t = I18N_PATTERNS[lang]['shortener']
    
    if not supabase: return P(t['err_db'], style="color:red;")

    # 1. Définition du code
    if custom_code and custom_code.strip():
        code = custom_code.strip().lower()
        check = supabase.table("links").select("short_code").eq("short_code", code).execute()
        if check.data:
            return Div(P(t['err_taken'], style="color:red; font-weight:bold;"), cls="modern-card", style="border-color:red;")
    else:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=4))

    # 2. Sauvegarde Supabase
    try:
        supabase.table("links").insert({"short_code": code, "long_url": url}).execute()
    except Exception as e:
        return P(f"Erreur : {e}", style="color:red;")

    # 3. Construction du lien pro
    direct_domain = "rtbx.space"
    short_link = f"https://{direct_domain}/s/{code}"
    
    # 4. Génération du QR Code pour ce lien court (pour le tracking)
    qr = qrcode.make(short_link)
    buf = BytesIO(); qr.save(buf, format="PNG")
    qr_s = base64.b64encode(buf.getvalue()).decode()

    return Div(
        H4(t['res_title']),
        
        # Affichage du lien court
        Input(value=short_link, readonly=True, id="shortlink-res",
              style="text-align:center; font-weight:800; color:var(--primary); font-size:1.2rem; border:2px solid var(--primary); background:#fff;"),
        
        # Affichage du QR Code automatique
        Div(
            Img(src=f"data:image/png;base64,{qr_s}", style="max-width:180px; margin: 1.5rem auto; border: 4px solid white; border-radius:12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);"),
            P(t['qr_info'], style="font-size:0.8rem; opacity:0.7;"),
            style="text-align:center;"
        ),
        
        # Boutons d'actions
        Grid(
            Button(t['copy_btn'], onclick="copyToClipboard()", cls="btn-full"),
            A(Button(t['dl_qr'], cls="outline"), href=f"data:image/png;base64,{qr_s}", download=f"qr-{code}.png")
        ),
        A(Button(t['stats_btn'], cls="outline", style="width:100%; margin-top:10px;"), href=f"/stats/{code}"),
        
        Script("""
            function copyToClipboard() {
                var copyText = document.getElementById("shortlink-res");
                copyText.select();
                copyText.setSelectionRange(0, 99999);
                navigator.clipboard.writeText(copyText.value);
                alert("Lien copié !");
            }
        """),
        style="text-align:center; margin-top:2rem; padding:2rem; background:rgba(79, 70, 229, 0.05); border-radius:24px; border: 1px solid var(--primary);"
    )

@rt("/gen-short", methods=["POST"])
async def post(session, url: str, custom_code: str):
    lang = session.get('lang', 'fr')
    t = I18N_PATTERNS[lang]['shortener']
    
    if not supabase: return P(t['err_db'], style="color:red;")

    # 1. Définition du code
    if custom_code and custom_code.strip():
        code = custom_code.strip().lower()
        check = supabase.table("links").select("short_code").eq("short_code", code).execute()
        if check.data:
            return Div(P(t['err_taken'], style="color:red; font-weight:bold;"), cls="modern-card", style="border-color:red;")
    else:
        code = ''.join(random.choices(string.ascii_letters + string.digits, k=4))

    # 2. Sauvegarde Supabase
    try:
        supabase.table("links").insert({"short_code": code, "long_url": url}).execute()
    except Exception as e:
        return P(f"Erreur : {e}", style="color:red;")

    # 3. Construction du lien pro
    direct_domain = "rtbx.space"
    short_link = f"https://{direct_domain}/s/{code}"
    
    # 4. Génération du QR Code pour ce lien court (pour le tracking)
    qr = qrcode.make(short_link)
    buf = BytesIO(); qr.save(buf, format="PNG")
    qr_s = base64.b64encode(buf.getvalue()).decode()

    return Div(
        H4(t['res_title']),
        
        # Affichage du lien court
        Input(value=short_link, readonly=True, id="shortlink-res",
              style="text-align:center; font-weight:800; color:var(--primary); font-size:1.2rem; border:2px solid var(--primary); background:#fff;"),
        
        # Affichage du QR Code automatique
        Div(
            Img(src=f"data:image/png;base64,{qr_s}", style="max-width:180px; margin: 1.5rem auto; border: 4px solid white; border-radius:12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);"),
            P(t['qr_info'], style="font-size:0.8rem; opacity:0.7;"),
            style="text-align:center;"
        ),
        
        # Boutons d'actions
        Grid(
            Button(t['copy_btn'], onclick="copyToClipboard()", cls="btn-full"),
            A(Button(t['dl_qr'], cls="outline"), href=f"data:image/png;base64,{qr_s}", download=f"qr-{code}.png")
        ),
        A(Button(t['stats_btn'], cls="outline", style="width:100%; margin-top:10px;"), href=f"/stats/{code}"),
        
        Script("""
            function copyToClipboard() {
                var copyText = document.getElementById("shortlink-res");
                copyText.select();
                copyText.setSelectionRange(0, 99999);
                navigator.clipboard.writeText(copyText.value);
                alert("Lien copié !");
            }
        """),
        style="text-align:center; margin-top:2rem; padding:2rem; background:rgba(79, 70, 229, 0.05); border-radius:24px; border: 1px solid var(--primary);"
    )

@rt("/stats/{code}")
def get(session, code: str):
    lang = session.get('lang', 'fr')
    if not supabase: return RedirectResponse("/")
    
    res = supabase.table("links").select("long_url, clicks, created_at").eq("short_code", code).execute()
    
    if res.data:
        item = res.data[0]
        date_obj = datetime.fromisoformat(item['created_at'].replace('Z', '+00:00'))
        date_str = date_obj.strftime("%d/%m/%Y")

        content = Div(
            H2(f"Analyses du lien : {code}", cls="gradient-text"),
            Div(
                H3(f"{item['clicks']}", style="font-size:4rem; margin:0; color:var(--primary);"),
                P("CLICS / SCANS", style="font-weight:800; opacity:0.6;"),
                style="text-align:center; padding:2rem; background:rgba(255,255,255,0.5); border-radius:30px; margin-bottom:2rem;"
            ),
            Grid(
                Div(B("Destination :"), P(item['long_url'], style="word-break:break-all; font-size:0.9rem;")),
                Div(B("Date :"), P(date_str))
            ),
            A(Button("← Nouveau lien", cls="outline", style="margin-top:2rem;"), href="/shortener"),
            cls="modern-card"
        )
        return Layout(content, "Stats", session)
    
    return Layout(P("Lien introuvable."), "Erreur", session)


# --- ROUTE DE SECOURS (FALLBACK) AVEC SESSION ---
@rt("/s/{code}")
def get(code: str, session):
    if not supabase: return RedirectResponse("/")
    
    try:
        # On cherche l'URL dans Supabase
        res = supabase.table("links").select("long_url", "clicks").eq("short_code", code).execute()
        
        if res.data:
            item = res.data[0]
            # On incrémente le clic (on garde les stats même sur le lien de secours)
            supabase.table("links").update({"clicks": item['clicks'] + 1}).eq("short_code", code).execute()
            
            # Redirection directe vers l'URL longue
            return RedirectResponse(item['long_url'])
            
        # Si le code n'existe pas, retour à l'accueil (qui utilisera la session pour la langue)
        return RedirectResponse("/")
        
    except Exception as e:
        print(f"Erreur redirection fallback: {e}")
        return RedirectResponse("/")

# --- PAGES LEGALES ---
@rt("/ads.txt")
def get(): return PlainTextResponse("google.com, pub-4081303157053373, DIRECT, f08c47fec0942fa0")

@rt("/terms")
def get(session):
    lang = session.get('lang', 'fr')
    return Layout(LegalPage('terms', lang), "Conditions", session)

@rt("/privacy")
def get(session):
    lang = session.get('lang', 'fr')
    return Layout(LegalPage('privacy', lang), "Confidentialité", session)

@rt("/ugc")
def get(session):
    lang = session.get('lang', 'fr')
    return Layout(LegalPage('ugc', lang), "UGC", session)

@rt("/contact")
def get(session):
    lang = session.get('lang', 'fr')
    d = CONTACT_DATA[lang]
    
    # Script AJAX dynamique selon la langue
    ajax_script = Script(f"""
        async function handleSubmit(event) {{
            event.preventDefault();
            const status = document.getElementById("contact-status");
            const data = new FormData(event.target);
            const btn = event.target.querySelector("button");
            
            btn.disabled = true;
            btn.innerText = "{d['btn_sending']}";
            
            fetch(event.target.action, {{
                method: 'POST',
                body: data,
                headers: {{ 'Accept': 'application/json' }}
            }}).then(response => {{
                if (response.ok) {{
                    status.innerHTML = "<div class='modern-card' style='background:#dcfce7; color:#166534; padding:1rem; margin-bottom:1rem; border:1px solid #166534; border-radius:12px;'>{d['msg_success']}</div>";
                    event.target.reset();
                }} else {{
                    status.innerHTML = "<div style='color:#ef4444; margin-bottom:1rem;'>{d['msg_error']}</div>";
                }}
            }}).catch(error => {{
                status.innerHTML = "<div style='color:#ef4444; margin-bottom:1rem;'>{d['msg_conn_error']}</div>";
            }}).finally(() => {{
                btn.disabled = false;
                btn.innerText = "{d['btn_send']}";
            }});
        }}
    """)

    content = Div(
        H2(d['title'], cls="gradient-text"),
        P(d['sub']),
        
        Div(id="contact-status"),
        
        Form(
            Label(d['label_email'], 
                  Input(type="email", name="email", placeholder="votre@email.com", required=True)),
            
            Label(d['label_subject'], 
                  Input(name="subject", placeholder=d['subject_p'], required=True)),
            
            Label(d['label_message'], 
                  Textarea(name="message", placeholder=d['message_p'], rows=6, required=True)),
            
            Input(type="hidden", name="_gotcha", style="display:none"),
            
            Button(d['btn_send'], type="submit", cls="btn-full"),
            
            action=f"https://formspree.io/f/{os.environ.get('FORMSPREE_ID')}",
            onsubmit="handleSubmit(event)"
        ),
        ajax_script,
        cls="modern-card", style="max-width: 700px; margin: auto; padding: 3rem;"
    )
    
    return Layout(content, "Contact", session)

@rt("/faq")
def get(session):
    lang = session.get('lang', 'fr')
    t = MULTILINGUAL_DATA_FaqGuide[lang]
    
    content = Div(
        H2(t['faq_title'], cls="gradient-text"),
        P(t['faq_sub']),
        
        Div(
            *[Details(
                Summary(item["q"]), 
                P(NotStr(item["a"]))
              ) for item in t['faq_data']],
            cls="faq-section"
        ),
        
        Div(
            H4("Contact Us" if lang == 'en' else "Contactez-nous"),
            A(Button("Support" if lang == 'en' else "Support Gratuit", cls="outline"), href="/contact"),
            style="margin-top: 3rem; text-align: center;"
        ),
        
        cls="modern-card", style="max-width: 900px; margin: auto; padding: 3rem;"
    )
    return Layout(content, "FAQ", session)

@rt("/guide")
def get(session):
    lang = session.get('lang', 'fr')
    t = MULTILINGUAL_DATA_FaqGuide[lang]
    
    # Mapping dynamique sur guide_data
    guide_cards = Div(*[
        Div(
            Div(
                Safe(f'<i data-lucide="{item["icon"]}" style="width:32px; height:32px; color:var(--primary); stroke-width:2.5px;"></i>'),
                H4(item["title"]),
                style="display:flex; align-items:center; gap:15px; margin-bottom:0.5rem;"
            ),
            P(NotStr(item["desc"])),
            A(Button("Use Tool" if lang == 'en' else "Utiliser l'outil", cls="outline"), 
              href=item["link"], style="margin-top:auto;"),
            cls="guide-card"
        ) for item in t['guide_data']
    ], cls="guide-grid")

    content = Div(
        Div(
            H2(t['guide_title'], cls="gradient-text", style="font-size:3rem;"),
            P(t['guide_sub'], style="font-size:1.2rem; opacity:0.8;"),
            style="margin-bottom:4rem; text-align:center;"
        ),
        guide_cards,
        cls="container"
    )
    return Layout(content, "Guide", session)

@rt("/set-lang/{lang}")
def get(lang: str, session):
    if lang in ['fr', 'en']:
        session['lang'] = lang
    return RedirectResponse(url='/')
if __name__ == "__main__":
    #main
    import uvicorn
   
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))