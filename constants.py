from datetime import datetime


CURRENT_YEAR = datetime.now().year


#script

adsense_script_src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4081303157053373",

ga_lib_src="https://www.googletagmanager.com/gtag/js?id=G-YV2LEDEMR8"


# --- TA LISTE DE SERVICES (SOURCE DE VÉRITÉ) ---
services = [
    ("users", "Identité Digitale", "Regroupez vos réseaux sociaux (Facebook, Instagram, TikTok, Spotify) dans un seul QR Code unique.", "/digital-id"),
    ("qr-code", "QR Code Pro", "Générez un QR Code simple ou  personnalisé avec votre logo pour vos menus restaurant PDF ou vos sites web.", "/qr-tab"),
    ("tag", "Étiquettes Soldes", "Créez vos étiquettes de soldes avec prix barré et code-barres prêtes pour l'impression en magasin.", "/soldes"),
    ("barcode", "Barcode Expert", "Générez des codes-barres EAN-13 et Code 128 professionnels pour la gestion de vos stocks et inventaires.", "/barcode-tab"),
    ("contact", "VCard Contact", "Créez un QR Code de contact pour permettre à vos clients d'enregistrer votre fiche d'un seul scan.", "/vcard"),
    ("message-circle", "QR WhatsApp", "Générez un lien QR direct pour ouvrir instantanément une discussion WhatsApp avec vos clients.", "/whatsapp-qr"),
    ("image", "RemBg IA", "Supprimez automatiquement le fond de vos photos produits pour vos fiches de vente en ligne WordpressShopify, Vinted ou eBay.", "/rembg-tab"),
    ("wifi", "Accès Wi-Fi", " Creez un qrcode pour offrire une connexion Wi-Fi sécurisée à vos clients sans saisie de mot de passe via un simple scan.", "/wifi-qr"),
    ("link", "Url Shortener Pro", "Créez  gratuitement un reducteur d'URL conforme RGPD  et suivez le nombre de clics en temps réel.", "/shortener")
]


MULTILINGUAL_DATA_Services = {
    'fr': {
        'home_title': "Solutions digitales pour Small Business",
        'home_sub': "Accédez à nos tutoriels détaillés dans la page Guide pour optimiser vos ventes.",
        'btn_open': "Ouvrir l'outil",
        'services': [
            {"icon": "users", "title": "Identité Digitale", "desc": "Regroupez vos réseaux sociaux (Facebook, Instagram, TikTok, Spotify) dans un seul QR Code unique.", "link": "/digital-id"},
            {"icon": "qr-code", "title": "QR Code Pro", "desc": "Générez un QR Code simple ou personnalisé avec votre logo pour vos menus restaurant PDF ou vos sites web.", "link": "/qr-tab"},
            {"icon": "tag", "title": "Étiquettes Soldes", "desc": "Créez vos étiquettes de soldes avec prix barré et code-barres prêtes pour l'impression en magasin.", "link": "/soldes"},
            {"icon": "barcode", "title": "Barcode Expert", "desc": "Générez des codes-barres EAN-13 et Code 128 professionnels pour la gestion de vos stocks et inventaires.", "link": "/barcode-tab"},
            {"icon": "contact", "title": "VCard Contact", "desc": "Créez un QR Code de contact pour permettre à vos clients d'enregistrer votre fiche d'un seul scan.", "link": "/vcard"},
            {"icon": "message-circle", "title": "QR WhatsApp", "desc": "Générez un lien QR direct pour ouvrir instantanément une discussion WhatsApp avec vos clients.", "link": "/whatsapp-qr"},
            {"icon": "image", "title": "RemBg IA", "desc": "Supprimez automatiquement le fond de vos photos produits pour vos fiches de vente Shopify, Vinted ou eBay.", "link": "/rembg-tab"},
            {"icon": "wifi", "title": "Accès Wi-Fi", "desc": "Créez un qrcode pour offrir une connexion Wi-Fi sécurisée à vos clients sans saisie de mot de passe.", "link": "/wifi-qr"},
            {"icon": "link", "title": "Url Shortener Pro", "desc": "Créez gratuitement un réducteur d'URL conforme RGPD et suivez le nombre de clics en temps réel.", "link": "/shortener"}
        ],
        # ... garde faq_data et guide_data ici ...
    },
    'en': {
        'home_title': "Digital Solutions for Small Business",
        'home_sub': "Access our detailed tutorials in the Guide page to optimize your sales.",
        'btn_open': "Open Tool",
        'services': [
            {"icon": "users", "title": "Digital Identity", "desc": "Group your social networks (Facebook, Instagram, TikTok, Spotify) into a single unique QR Code.", "link": "/digital-id"},
            {"icon": "qr-code", "title": "QR Code Pro", "desc": "Generate a simple or custom QR Code with your logo for your restaurant menus or websites.", "link": "/qr-tab"},
            {"icon": "tag", "title": "Sale Labels", "desc": "Create your sale labels with crossed-out prices and barcodes ready for in-store printing.", "link": "/soldes"},
            {"icon": "barcode", "title": "Barcode Expert", "desc": "Generate professional EAN-13 and Code 128 barcodes for stock and inventory management.", "link": "/barcode-tab"},
            {"icon": "contact", "title": "VCard Contact", "desc": "Create a contact QR Code to allow your customers to save your details with a single scan.", "link": "/vcard"},
            {"icon": "message-circle", "title": "QR WhatsApp", "desc": "Generate a direct QR link to instantly open a WhatsApp chat with your customers.", "link": "/whatsapp-qr"},
            {"icon": "image", "title": "AI RemBg", "desc": "Automatically remove the background from your product photos for Shopify, Vinted, or eBay.", "link": "/rembg-tab"},
            {"icon": "wifi", "title": "Wi-Fi Access", "desc": "Create a QR code to offer secure Wi-Fi connection to your customers without manual password entry.", "link": "/wifi-qr"},
            {"icon": "link", "title": "Url Shortener Pro", "desc": "Create a free GDPR-compliant URL shortener and track the number of clicks in real-time.", "link": "/shortener"}
        ],
        # ... garde faq_data et guide_data ici ...
    }
}

# faq data 
faq_data = [
    {
        "q": "Comment générer un QR code pour mon menu restaurant en PDF ?",
        "a": "Hébergez votre menu sur Google Drive ou Dropbox, copiez le lien de partage public et utilisez notre outil <a href='/qr-tab' class='faq-link'>QR Code Pro</a>. Vous pouvez même ajouter le logo de votre établissement pour un rendu professionnel."
    },
    {
        "q": "Le générateur d'étiquettes de soldes est-il vraiment gratuit ?",
        "a": "Oui, RetailBox permet de créer gratuitement des étiquettes avec prix barré et code-barres EAN-13 via notre service <a href='/soldes' class='faq-link'>Étiquettes de Soldes</a>. C'est idéal pour préparer vos promotions sans frais."
    },
    {
        "q": "Comment regrouper Instagram, TikTok et Facebook dans un seul QR ?",
        "a": "Utilisez notre service <a href='/digital-id' class='faq-link'>Identité Digitale</a>. En saisissant les liens de vos profils, vous générez une Social Card unique qui centralise toute votre présence en ligne."
    },
    {
        "q": "Comment connecter mes clients au Wi-Fi sans donner le mot de passe ?",
        "a": "Grâce à notre <a href='/wifi-qr' class='faq-link'>Générateur de QR Code Wi-Fi</a>, entrez le nom de votre réseau et la clé. Vos clients scannent et se connectent instantanément en toute sécurité."
    },
    {
        "q": "Comment créer un lien QR direct vers mon WhatsApp ?",
        "a": "Utilisez l'outil <a href='/whatsapp-qr' class='faq-link'>QR WhatsApp</a>. Entrez votre numéro et un message automatique. Le QR code ouvrira directement une discussion avec votre boutique."
    },
    {
        "q": "Peut-on supprimer l'arrière-plan d'une photo produit par IA ?",
        "a": "Absolument. Notre outil <a href='/rembg-tab' class='faq-link'>RemBg</a> utilise une IA pour détourer automatiquement vos photos. Obtenez un PNG transparent de qualité studio en quelques secondes."
    },
    {
        "q": "Quels formats de codes-barres sont disponibles pour mon stock ?",
        "a": "Nous supportons le format EAN-13 pour la vente et le format Code 128 pour l'inventaire interne. Gérez vos produits avec notre <a href='/barcode-tab' class='faq-link'>Générateur de Barcode</a>."
    },
    {
        "q": "Pourquoi utiliser un réducteur de lien pour mon commerce ?",
        "a": "Utilisez notre outil <a href='/shortener' class='faq-link'>Shortener Pro</a> pour transformer des URLs complexes en liens courts et mémorisables. Cela permet d'épurer vos supports de communication (flyers, affiches) et de rendre vos liens de boutique plus cliquables sur les réseaux sociaux."
    },
    {"q":"RetailLink est-il respectueux de la vie privée ?",
    "a":"Oui. Contrairement aux autres réducteurs de liens, RetailLink ne collecte aucune donnée personnelle sur les personnes qui cliquent sur vos liens. Nous comptabilisons uniquement le nombre total de clics de manière anonyme, sans stocker d'adresses IP ou utiliser de cookies de pistage."},
]

guide_data = [
    {
        "icon": "qr-code", "title": "QR Codes simple ou avec Logo", "link": "/qr-tab",
        "desc": "Sélectionnez le mode URL ou Fiche de données, personnalisez les couleurs et importez votre logo. Le générateur <a href='/qr-tab' class='faq-link'>QR Pro</a> produit un fichier haute résolution prêt pour l'impression de vos menus ou supports marketing."
    },
    {
        "icon": "users", "title": "Identité Digitale", "link": "/digital-id",
        "desc": "Sélectionnez vos réseaux (TikTok, Instagram, etc.) et saisissez vos liens. Cet outil crée une <a href='/digital-id' class='faq-link'>Social Card</a> unique pour regrouper toute votre présence en ligne et faciliter l'abonnement de vos clients."
    },
    {
        "icon": "contact", "title": "VCard : Carte de Visite", "link": "/vcard",
        "desc": "Remplissez vos coordonnées (nom, poste, boutique, adresse GPS). Le service <a href='/vcard' class='faq-link'>VCard QR</a> génère une fiche contact standard que vos clients peuvent enregistrer instantanément dans leur répertoire smartphone d'un seul scan."
    },
    {
        "icon": "message-circle", "title": "QR WhatsApp Direct", "link": "/whatsapp-qr",
        "desc": "Entrez votre numéro et rédigez un message d'accueil automatique. L'outil <a href='/whatsapp-qr' class='faq-link'>QR WhatsApp</a> génère un lien direct pour automatiser vos prises de commandes ou votre service client sans saisie de numéro."
    },
    {
        "icon": "tag", "title": "Étiquettes de Soldes", "link": "/soldes",
        "desc": "Saisissez le prix d'origine, le prix remisé et le code EAN-13. Notre <a href='/soldes' class='faq-link'>générateur d'étiquettes</a> crée un visuel pro avec prix barré, disponible en téléchargement individuel ou en planche A4 prête à imprimer."
    },
    {
        "icon": "barcode", "title": "Barcode EAN-13 & 128", "link": "/barcode-tab",
        "desc": "Choisissez le format EAN-13 pour la vente ou Code 128 pour la logistique. Entrez vos chiffres et le <a href='/barcode-tab' class='faq-link'>moteur de codes-barres</a> génère des étiquettes techniques lisibles par tous les scanners laser du commerce."
    },
    {
        "icon": "image", "title": "Détourage IA de Produit", "link": "/rembg-tab",
        "desc": "Importez votre photo au format JPG ou PNG. L'outil <a href='/rembg-tab' class='faq-link'>RemBg IA</a> analyse le sujet et supprime automatiquement l'arrière-plan pour créer des images de produits en PNG transparent de qualité studio."
    },
    {
        "icon": "wifi", "title": "QR Code Accès Wi-Fi", "link": "/wifi-qr",
        "desc": "Saisissez le nom de votre réseau (SSID) et sa clé de sécurité. Le <a href='/wifi-qr' class='faq-link'>QR Wi-Fi</a> génère un code de connexion automatique sécurisée permettant à vos visiteurs de se connecter sans taper de mot de passe."
    },
    {
        "icon": "link", "title": "Réducteur de Liens Pro", "link": "/shortener",
        "desc": "Collez votre URL longue et personnalisez l'alias pour vos campagnes. Via <a href='/shortener' class='faq-link'>RetailLink</a>, vous obtenez un lien court permanent, conforme au RGPD, tout en suivant vos statistiques de clics en temps réel."
    }
]



MULTILINGUAL_DATA_FaqGuide = {
    'fr': {
        'faq_title': "Foire aux Questions (FAQ)",
        'faq_sub': "Retrouvez toutes les réponses pour optimiser votre commerce avec nos outils digitaux.",
        'faq_data': [
            {"q": "Comment générer un QR code pour mon menu restaurant en PDF ?", "a": "Hébergez votre menu sur Google Drive ou Dropbox, copiez le lien de partage public et utilisez notre outil <a href='/qr-tab' class='faq-link'>QR Code Pro</a>. Vous pouvez même ajouter le logo de votre établissement pour un rendu professionnel."},
            {"q": "Le générateur d'étiquettes de soldes est-il vraiment gratuit ?", "a": "Oui, RetailBox permet de créer gratuitement des étiquettes avec prix barré et code-barres EAN-13 via notre service <a href='/soldes' class='faq-link'>Étiquettes de Soldes</a>. C'est idéal pour préparer vos promotions sans frais."},
            {"q": "Comment regrouper Instagram, TikTok et Facebook dans un seul QR ?", "a": "Utilisez notre service <a href='/digital-id' class='faq-link'>Identité Digitale</a>. En saisissant les liens de vos profils, vous générez une Social Card unique qui centralise toute votre présence en ligne."},
            {"q": "Comment connecter mes clients au Wi-Fi sans donner le mot de passe ?", "a": "Grâce à notre <a href='/wifi-qr' class='faq-link'>Générateur de QR Code Wi-Fi</a>, entrez le nom de votre réseau et la clé. Vos clients scannent et se connectent instantanément."},
            {"q": "Comment créer un lien QR direct vers mon WhatsApp ?", "a": "Utilisez l'outil <a href='/whatsapp-qr' class='faq-link'>QR WhatsApp</a>. Entrez votre numéro et un message automatique. Le QR code ouvrira directement une discussion avec votre boutique."},
            {"q": "Peut-on supprimer l'arrière-plan d'une photo produit par IA ?", "a": "Absolument. Notre outil <a href='/rembg-tab' class='faq-link'>RemBg</a> utilise une IA pour détourer automatiquement vos photos. Obtenez un PNG transparent de qualité studio."},
            {"q": "Quels formats de codes-barres sont disponibles pour mon stock ?", "a": "Nous supportons le format EAN-13 pour la vente et le format Code 128 pour l'inventaire interne. Gérez vos produits avec notre <a href='/barcode-tab' class='faq-link'>Générateur de Barcode</a>."},
            {"q": "Pourquoi utiliser un réducteur de lien pour mon commerce ?", "a": "Utilisez notre outil <a href='/shortener' class='faq-link'>Shortener Pro</a> pour transformer des URLs complexes en liens courts et mémorisables. Cela permet d'épurer vos supports de communication."},
            {"q": "RetailLink est-il respectueux de la vie privée ?", "a": "Oui. Contrairement aux autres réducteurs de liens, RetailLink ne collecte aucune donnée personnelle sur les personnes qui cliquent sur vos liens."}
        ],
        'guide_title': "Guide Complet : Maîtrisez vos outils digitaux",
        'guide_sub': "Suivez nos instructions étape par étape pour optimiser votre commerce et votre logistique.",
        'guide_data': [
            {"icon": "qr-code", "title": "QR Codes avec Logo", "link": "/qr-tab", "desc": "Sélectionnez le mode URL ou Fiche de données, personnalisez les couleurs et importez votre logo. Le générateur <a href='/qr-tab' class='faq-link'>QR Pro</a> produit un fichier haute résolution."},
            {"icon": "users", "title": "Identité Digitale", "link": "/digital-id", "desc": "Sélectionnez vos réseaux (TikTok, Instagram, etc.) et saisissez vos liens. Cet outil crée une <a href='/digital-id' class='faq-link'>Social Card</a> unique."},
            {"icon": "contact", "title": "VCard : Carte de Visite", "link": "/vcard", "desc": "Remplissez vos coordonnées pro. Le service <a href='/vcard' class='faq-link'>VCard QR</a> génère une fiche contact que vos clients enregistrent d'un scan."},
            {"icon": "message-circle", "title": "QR WhatsApp Direct", "link": "/whatsapp-qr", "desc": "Entrez votre numéro et rédigez un message d'accueil. L'outil <a href='/whatsapp-qr' class='faq-link'>QR WhatsApp</a> automatise vos prises de commandes."},
            {"icon": "tag", "title": "Étiquettes de Soldes", "link": "/soldes", "desc": "Saisissez prix d'origine et remisé. Notre <a href='/soldes' class='faq-link'>générateur d'étiquettes</a> crée un visuel pro avec prix barré prêt à imprimer."},
            {"icon": "barcode", "title": "Barcode EAN-13 & 128", "link": "/barcode-tab", "desc": "Choisissez EAN-13 (vente) ou Code 128 (logistique). Le <a href='/barcode-tab' class='faq-link'>moteur de codes-barres</a> génère des étiquettes lisibles par tous les scanners."},
            {"icon": "image", "title": "Détourage IA de Produit", "link": "/rembg-tab", "desc": "Importez votre photo. L'outil <a href='/rembg-tab' class='faq-link'>RemBg IA</a> supprime automatiquement l'arrière-plan pour des images PNG transparentes."},
            {"icon": "wifi", "title": "QR Code Accès Wi-Fi", "link": "/wifi-qr", "desc": "Saisissez le nom de votre réseau et sa clé. Le <a href='/wifi-qr' class='faq-link'>QR Wi-Fi</a> permet une connexion sécurisée sans saisie de mot de passe."},
            {"icon": "link", "title": "Réducteur de Liens Pro", "link": "/shortener", "desc": "Collez votre URL longue et personnalisez l'alias via <a href='/shortener' class='faq-link'>RetailLink</a> pour obtenir un lien court permanent."}
        ]
    },
    'en': {
        'faq_title': "Frequently Asked Questions (FAQ)",
        'faq_sub': "Find all the answers to optimize your business with our digital tools.",
        'faq_data': [
            {"q": "How to generate a QR code for my restaurant menu in PDF?", "a": "Host your menu on Google Drive, copy the public link and use our <a href='/qr-tab' class='faq-link'>QR Code Pro</a> tool. You can even add your logo for a professional look."},
            {"q": "Is the sale label generator really free?", "a": "Yes, RetailBox allows you to create free labels with crossed-out prices and EAN-13 barcodes via our <a href='/soldes' class='faq-link'>Sale Labels</a> service."},
            {"q": "How to group Instagram, TikTok, and Facebook in one QR?", "a": "Use our <a href='/digital-id' class='faq-link'>Digital Identity</a> service. Enter your profile links to generate a unique Social Card."},
            {"q": "How to connect my clients to Wi-Fi without giving the password?", "a": "With our <a href='/wifi-qr' class='faq-link'>Wi-Fi QR Code Generator</a>, enter your network name and key. Your clients scan and connect instantly."},
            {"q": "How to create a direct QR link to my WhatsApp?", "a": "Use the <a href='/whatsapp-qr' class='faq-link'>QR WhatsApp</a> tool. Enter your number and an automated message. The QR code opens a chat directly."},
            {"q": "Can I remove the background of a product photo with AI?", "a": "Absolutely. Our <a href='/rembg-tab' class='faq-link'>RemBg</a> tool uses AI to automatically crop your photos into transparent PNGs."},
            {"q": "What barcode formats are available for my stock?", "a": "We support EAN-13 for sales and Code 128 for internal inventory. Manage your products with our <a href='/barcode-tab' class='faq-link'>Barcode Generator</a>."},
            {"q": "Why use a link shortener for my business?", "a": "Use our <a href='/shortener' class='faq-link'>Shortener Pro</a> tool to turn complex URLs into short, memorable links."},
            {"q": "Is RetailLink privacy-friendly?", "a": "Yes. Unlike other link shorteners, RetailLink does not collect any personal data from people clicking your links."}
        ],
        'guide_title': "Complete Guide: Master Your Digital Tools",
        'guide_sub': "Follow our step-by-step instructions to optimize your commerce and logistics.",
        'guide_data': [
            {"icon": "qr-code", "title": "QR Codes with Logo", "link": "/qr-tab", "desc": "Select URL or Data mode, customize colors and upload your logo. The <a href='/qr-tab' class='faq-link'>QR Pro</a> generator creates a high-res file."},
            {"icon": "users", "title": "Digital Identity", "link": "/digital-id", "desc": "Select your networks and enter your links. This tool creates a unique <a href='/digital-id' class='faq-link'>Social Card</a> for your followers."},
            {"icon": "contact", "title": "VCard: Business Card", "link": "/vcard", "desc": "Fill in your pro details. The <a href='/vcard' class='faq-link'>VCard QR</a> service generates a contact file that clients save instantly."},
            {"icon": "message-circle", "title": "Direct WhatsApp QR", "link": "/whatsapp-qr", "desc": "Enter your number and write a welcome message. The <a href='/whatsapp-qr' class='faq-link'>QR WhatsApp</a> tool automates your order taking."},
            {"icon": "tag", "title": "Sale Labels", "link": "/soldes", "desc": "Enter original and discounted prices. Our <a href='/soldes' class='faq-link'>label generator</a> creates a pro visual with a crossed-out price."},
            {"icon": "barcode", "title": "Barcode EAN-13 & 128", "link": "/barcode-tab", "desc": "Choose EAN-13 or Code 128. The <a href='/barcode-tab' class='faq-link'>barcode engine</a> generates labels readable by all scanners."},
            {"icon": "image", "title": "AI Product Background Removal", "link": "/rembg-tab", "desc": "Upload your photo. The <a href='/rembg-tab' class='faq-link'>RemBg AI</a> tool automatically removes the background for studio-quality PNGs."},
            {"icon": "wifi", "title": "Wi-Fi Access QR Code", "link": "/wifi-qr", "desc": "Enter your network name and password. The <a href='/wifi-qr' class='faq-link'>Wi-Fi QR</a> allows connection without password typing."},
            {"icon": "link", "title": "Pro Link Shortener", "link": "/shortener", "desc": "Paste your long URL and customize the alias via <a href='/shortener' class='faq-link'>RetailLink</a> to get a permanent short link."}
        ]
    }
}


SOCIAL_NETWORKS = [
    ("Instagram", "Instagram"), ("TikTok", "TikTok"), ("YouTube", "YouTube"),
    ("Threads", "Threads"), ("Pinterest", "Pinterest"), ("Twitch", "Twitch"),
    ("Facebook", "Facebook"), ("LinkedIn", "LinkedIn"), ("X", "X (Twitter)"),
    ("Spotify", "Spotify"), ("Shopify", "Ma Boutique / Shopify"),
    ("WhatsApp", "WhatsApp"), ("Website", "Site Web Personnel")
]




LOCALES = {
    'fr': {
        'home': 'Accueil', 'guide': 'Guide', 'faq': 'FAQ', 'about': 'À Propos',
        'hero_title': 'Générez et Transformez en un clic',
        'hero_sub': 'La boîte à outils indispensable pour les vendeurs.',
        'open_tool': "Ouvrir l'outil",
        'lang_name': 'English', 'lang_code': 'en',
        # Ajoute ici tous tes titres de FAQ, descriptions de services, etc.
    },
    'en': {
        'home': 'Home', 'guide': 'Guide', 'faq': 'FAQ', 'about': 'About',
        'hero_title': 'Generate and Transform in one click',
        'hero_sub': 'The essential toolkit for retailers and sellers.',
        'open_tool': 'Open Tool',
        'lang_name': 'Français', 'lang_code': 'fr',
    }
}


LEGAL_CONTENT = {
    'fr': {
        'terms': {
            'title': "Conditions Générales d'Utilisation",
            'date': f"Dernière mise à jour : Mars {CURRENT_YEAR}",
            'sections': [
                {'h': "1. Description du Service", 'p': "RetailBox met à disposition des outils de génération de QR codes, de codes-barres techniques et de traitement d'images par IA. L'accès au service est gratuit et ne nécessite aucune inscription préalable."},
                {'h': "2. Utilisation autorisée et Interdictions", 'p': "En utilisant ce site, vous vous engagez à respecter les règles suivantes :", 
                 'li': ["Interdiction de générer des contenus frauduleux ou destinés à la contrefaçon.", "Interdiction d'intégrer des liens malveillants (phishing, virus).", "Interdiction d'utiliser des scripts ou bots pour saturer nos serveurs.", "Le service ne doit pas être utilisé pour harceler des tiers."]},
                {'h': "3. Limitation de responsabilité", 'p': "RetailBox décline toute responsabilité en cas d'erreur de lecture suite à une mauvaise configuration utilisateur ou une impression de faible qualité."},
                {'h': "4. Disponibilité", 'p': "Nous nous efforçons de maintenir le service accessible 24h/24, sans garantie de disponibilité ininterrompue."}
            ]
        },
        'privacy': {
            'title': "Politique de Confidentialité",
            'date': "Votre vie privée est au cœur de notre service technique.",
            'sections': [
                {'h': "1. Traitement des fichiers (RAM-Only)", 'p': "RetailBox utilise un traitement éphémère en mémoire vive (RAM) :", 
                 'li': ["Les fichiers sont traités instantanément.", "Aucun stockage sur disque dur permanent.", "Suppression totale après génération."]},
                {'h': "2. Publicité et Cookies", 'p': "Ce site utilise Google AdSense. Google utilise des cookies pour diffuser des annonces basées sur votre navigation. Vous pouvez désactiver la personnalisation dans vos paramètres Google."},
                {'h': "3. Collecte de données", 'p': "Nous ne collectons aucune donnée personnelle (nom, email, IP) à des fins marketing."},
                {'h': "4. RetailLink (Shortener)", 'p': "Notre réducteur d'URL mesure l'audience de manière quantitative (clics) sans identifier l'utilisateur final."}
            ]
        },
        'ugc': {
            'title': "Droits sur le Contenu Généré (UGC)",
            'date': "UGC : User Generated Content (Contenu généré par l'utilisateur).",
            'sections': [
                {'h': "1. Propriété exclusive", 'p': "Vous êtes le propriétaire unique de 100% des fichiers générés sur ce site (QR, Barcodes, photos détourées)."},
                {'h': "2. Usage Commercial", 'p': "RetailBox vous accorde un droit d'utilisation commerciale illimité et gratuit sur toutes vos créations."},
                {'h': "3. Responsabilité", 'p': "Vous certifiez posséder les droits sur les logos et liens intégrés. RetailBox agit comme un prestataire technique passif."}
            ]
        }
    },
    'en': {
        'terms': {
            'title': "Terms of Service",
            'date': f"Last updated: March {CURRENT_YEAR}",
            'sections': [
                {'h': "1. Description of Service", 'p': "RetailBox provides digital tools for generating QR codes, technical barcodes, and AI-powered image processing. Access to the service is free and requires no prior registration."},
                {'h': "2. Authorized Use and Prohibitions", 'p': "By using this site, you agree to comply with the following rules:", 
                 'li': ["Prohibition of generating fraudulent content or content intended for counterfeiting.", "Prohibition of embedding malicious links (phishing, viruses).", "Prohibition of using scripts or bots to overwhelm our servers.", "The service must not be used to harass third parties via direct contact tools."]},
                {'h': "3. Limitation of Liability", 'p': "RetailBox disclaims all liability for any scanning errors resulting from improper user configuration or low-quality printing."},
                {'h': "4. Availability", 'p': "We strive to keep the service accessible 24/7, without any guarantee of uninterrupted availability."}
            ]
        },
        'privacy': {
            'title': "Privacy Policy",
            'date': "Your privacy is at the core of our technical service.",
            'sections': [
                {'h': "1. File Processing (RAM-Only)", 'p': "RetailBox uses ephemeral processing in random access memory (RAM):", 
                 'li': ["Files are processed instantly.", "No permanent hard drive storage is used.", "Total deletion of data after generation."]},
                {'h': "2. Advertising and Cookies", 'p': "This site uses Google AdSense. Google uses cookies to serve ads based on your browsing history. You can disable personalized advertising in your Google account settings."},
                {'h': "3. Data Collection", 'p': "We do not collect any personal identifiable information (name, email, IP) for marketing purposes."},
                {'h': "4. RetailLink (Shortener)", 'p': "Our URL shortener measures audience quantitatively (clicks) without identifying the end user."}
            ]
        },
        'ugc': {
            'title': "UGC Rights & Ownership",
            'date': "UGC: User Generated Content.",
            'sections': [
                {'h': "1. Exclusive Ownership", 'p': "You are the sole owner of 100% of the files generated on this site (QR Codes, Barcodes, processed images)."},
                {'h': "2. Commercial Usage Rights", 'p': "RetailBox grants you an unlimited and free commercial usage right for all your creations. we do not claim any copyright on your work."},
                {'h': "3. Content Responsibility", 'p': "By generating a file, you certify that you own the rights to any uploaded logos or embedded links. RetailBox acts as a passive technical provider."}
            ]
        }
    }
}


ABOUT_DATA = {
    'fr': {
        'title': "À propos de RetailBox",
        'intro': "RetailBox est une suite d'outils techniques dédiée à l'optimisation des opérations pour le commerce moderne et les Small Businesses.",
        'mission_h': "Accompagner la croissance des entreprises",
        'mission_p': "Nous centralisons les ressources critiques pour les entrepreneurs et gestionnaires de points de vente. De la boutique physique au site e-commerce, nous fournissons les standards technologiques indispensables pour rester compétitif dans un environnement digital en constante évolution.",
        'stock_h': "📦 Gestion de Stock & Inventaire",
        'stock_p': "Nous simplifions la logistique commerciale avec des générateurs de codes-barres conformes (EAN-13, Code 128). Nous facilitons l'organisation de vos stocks et l'étiquetage précis de vos produits.",
        'restau_h': "🍽️ Solutions pour Restaurants",
        'restau_p': "Nous modernisons l'expérience client. Nous permettons un accès instantané à vos cartes et tarifs, optimisant ainsi votre service en salle.",
        'id_h': "🌐 Identité Digitale",
        'id_p': "Nous optimisons votre visibilité professionnelle avec des Social Cards et VCards intelligentes. Nous créons un point d'entrée unique pour regrouper vos réseaux sociaux et vos canaux de vente.",
        'prod_h': "📸 Optimisation Produit",
        'prod_p': "Nous valorisons vos articles de vente grâce à notre IA de détourage. Nous transformons vos photos brutes en images produits de qualité studio pour vos fiches e-commerce et vos catalogues.",
        'privacy_h': "Notre engagement pour vos données",
        'privacy_p': "Nous appliquons une politique de confidentialité rigoureuse. Chaque traitement technique est exécuté en mémoire vive (RAM) de manière isolée. Nous ne conservons aucune donnée commerciale, photo produit ou information confidentielle sur nos serveurs. Nous garantissons votre propriété exclusive sur 100% des contenus générés (UGC) via notre plateforme."
    },
    'en': {
        'title': "About RetailBox",
        'intro': "RetailBox is a suite of technical tools dedicated to optimizing operations for modern commerce and Small Businesses.",
        'mission_h': "Supporting Business Growth",
        'mission_p': "We centralize critical resources for entrepreneurs and point-of-sale managers. From physical stores to e-commerce sites, we provide the essential technological standards to remain competitive in a constantly evolving digital environment.",
        'stock_h': "📦 Stock & Inventory Management",
        'stock_p': "We simplify commercial logistics with compliant barcode generators (EAN-13, Code 128). We facilitate your stock organization and precise product labeling.",
        'restau_h': "🍽️ Solutions for Restaurants",
        'restau_p': "We modernize the customer experience. We provide instant access to your menus and rates, thus optimizing your floor service.",
        'id_h': "🌐 Digital Identity",
        'id_p': "We optimize your professional visibility with smart Social Cards and VCards. We create a single point of entry to group your social networks and sales channels.",
        'prod_h': "📸 Product Optimization",
        'prod_p': "We enhance your sales items through our AI background removal. We transform your raw photos into studio-quality product images for your e-commerce listings and catalogs.",
        'privacy_h': "Our Commitment to Your Data",
        'privacy_p': "We apply a rigorous privacy policy. Every technical process is executed in random access memory (RAM) in isolation. We do not store any commercial data, product photos, or confidential information on our servers. We guarantee your exclusive ownership of 100% of the content generated (UGC) via our platform."
    }
}



CONTACT_DATA = {
    'fr': {
        'title': "Contactez l'équipe RetailBox",
        'sub': "Une suggestion technique ou un partenariat ? Utilisez le formulaire ci-dessous.",
        'label_email': "Votre adresse e-mail",
        'label_subject': "Sujet",
        'subject_p': "Ex: Support QR Code",
        'label_message': "Votre message",
        'message_p': "Comment pouvons-nous vous aider ?",
        'btn_send': "🚀 Envoyer le message",
        'btn_sending': "Envoi en cours...",
        'msg_success': "✅ Merci ! Votre message a été envoyé avec succès.",
        'msg_error': "❌ Une erreur est survenue. Veuillez réessayer.",
        'msg_conn_error': "❌ Erreur de connexion."
    },
    'en': {
        'title': "Contact the RetailBox Team",
        'sub': "Technical suggestion or partnership? Use the form below.",
        'label_email': "Your email address",
        'label_subject': "Subject",
        'subject_p': "e.g. QR Code Support",
        'label_message': "Your message",
        'message_p': "How can we help you?",
        'btn_send': "🚀 Send Message",
        'btn_sending': "Sending...",
        'msg_success': "✅ Thank you! Your message has been sent successfully.",
        'msg_error': "❌ An error occurred. Please try again.",
        'msg_conn_error': "❌ Connection error."
    }
}


I18N_PATTERNS = {
    'fr': {
        # Patterns Communs (Réutilisables partout)
        'common': {
            'btn_add': "+ Ajouter une ligne",
            'btn_generate': "🚀 Générer le fichier",
            'btn_remove': "Supprimer",
            'btn_download': "⬇️ Télécharger",
            'placeholder_url': "Lien URL ou @identifiant",
            'error_empty': "Veuillez remplir au moins un champ.",
            'loading': "Traitement en cours...",
        },
        # Spécifique à l'Identité Digitale
        'social': {
            'title': "Votre Identité Digitale",
            'sub': "Centralisez tous vos réseaux. Sélectionnez une plateforme et ajoutez votre lien.",
            'qr_header': "MA PRÉSENCE DIGITALE :",
            'filename': "identite-digitale.png"
        },
        'vcard':{
    'title': "Carte de Visite Digitale (VCard)",
    'sub': "Générez un QR Code qui enregistre vos coordonnées complètes dans le répertoire de vos clients et partenaires.",
    'fn': "Prénom", 'ln': "Nom",
    'org': "Boutique / Entreprise", 'job': "Poste / Fonction",
    'tel': "Téléphone", 'email': "E-mail Pro",
    'li': "LinkedIn (URL)", 'web': "Site Web / Boutique",
    'adr': "Adresse physique (pour GPS)",
    'btn': "🚀 Générer ma Carte Pro",
    'filename': "vcard-retailbox.png"
},
'watsapp':{
    'title': "QR WhatsApp Direct",
    'sub': "Générez un lien qui ouvre instantanément une discussion WhatsApp avec un message pré-rempli.",
    'label_tel': "Numéro de téléphone (avec indicatif)",
    'ph_tel': "Ex: 33612345678",
    'label_msg': "Message automatique (optionnel)",
    'ph_msg': "Ex: Bonjour, je souhaite avoir des informations sur...",
    'btn': "🚀 Générer le QR WhatsApp",
    'filename': "whatsapp-retailbox.png"
},
'soldes':{
    'title': "Générateur d'Étiquettes & Planches A4",
    'sub': "Créez vos étiquettes de soldes avec prix barrés. Le système génère une image HD et une planche PDF A4 (24 étiquettes) prête pour vos planches d'autocollants standards.",
    'label_item': "Nom du produit / Référence",
    'ph_item': "Ex: Chemise Lin Bleu",
    'label_old': "Prix d'origine (€)",
    'label_new': "Prix soldé (€)",
    'label_code': "Code-barres EAN-13 (12 chiffres)",
    'btn': "🚀 Créer l'image et la Planche PDF",
    'preview': "Aperçu de l'étiquette :",
    'dl_png': "⬇️ Image seule (PNG)",
    'dl_pdf': "📄 Planche A4 (24 étiquettes)",
    'error': "Erreur : Vérifiez que le code contient bien 12 chiffres."
},
'barcode':{
    'title': "Générateur de Barcode Expert",
    'sub': "Saisissez vos données ou créez une fiche technique pour votre inventaire.",
    'label_format': "Format du code-barres",
    'opt_ean': "EAN-13 (Standard Commerce)",
    'opt_128': "Code 128 (Logistique / Données)",
    'ph_ean': "Entrez exactement 12 chiffres",
    'ph_key': "Clé (ex: SKU)",
    'ph_val': "Valeur",
    'ean_info': "Le 13ème chiffre de contrôle est calculé automatiquement.",
    'btn_add': "+ Ajouter une donnée",
    'btn_gen': "🚀 Générer le Code-barres",
    'err_ean': "Erreur : EAN-13 nécessite exactement 12 chiffres.",
    'err_empty': "Erreur : Veuillez saisir au moins une donnée.",
    'err_long': "Erreur : Trop de données pour la lisibilité du code.",
    'encoded': "Données encodées :",
    'dl': "⬇️ Télécharger Barcode"
},
'rembg':{
    'title': "Détourage Image par IA",
    'sub': "Supprimez automatiquement l'arrière-plan de vos photos produits pour un rendu studio professionnel.",
    'label_file': "Sélectionnez votre photo (JPG, PNG)",
    'btn_run': "🚀 Lancer le détourage IA",
    'success': "Traitement terminé !",
    'dl_btn': "⬇️ Télécharger l'image détourée",
    'filename': "retailbox-sans-fond.png"
},
'qr':{
    'title': "Générateur QR Code Pro",
    'sub': "Personnalisez votre QR Code pour vos menus restaurant, boutiques ou réseaux sociaux.",
    'label_type': "Type de contenu",
    'opt_url': "Lien URL Simple",
    'opt_kv': "Données Clé:Valeur (Fiche)",
    'label_fc': "Couleur du QR",
    'label_bc': "Couleur du Fond",
    'label_logo': "Logo de marque (Optionnel)",
    'btn_gen': "🚀 Générer le QR Code",
    'err_empty': "Erreur : Aucune donnée saisie.",
    'dl_btn': "⬇️ Télécharger le QR Code PNG",
    'filename': "qrcode-retailbox.png",
    'ph_url': "Entrez le lien (ex: https://...)"
},
'wifi':{
    'title': "Générateur QR Code Wi-Fi",
    'sub': "Offrez une connexion instantanée à vos clients. Pas de mot de passe à taper, juste un scan.",
    'label_ssid': "Nom du réseau (SSID)",
    'ph_ssid': "Ex: Wi-Fi_Boutique",
    'label_pass': "Mot de passe",
    'ph_pass': "Votre clé Wi-Fi",
    'label_type': "Sécurité",
    'btn': "🚀 Générer l'accès Wi-Fi",
    'tip': "💡 Conseil : Utilisez l'application 'Appareil Photo' native de l'iPhone pour une connexion automatique fluide.",
    'filename': "wifi-retailbox.png"
},
'shortener':{
    'title': "RetailLink : Réducteur & Statistiques",
    'sub': "Créez des URLs mémorables et suivez l'engagement en temps réel.",
    'label_url': "Lien de destination (URL longue)",
    'label_custom': "Alias personnalisé (Optionnel)",
    'ph_custom': "Ex: promo-printemps",
    'btn_gen': "🚀 Réduire et Activer",
    'res_title': "✅ Votre RetailLink est prêt !",
    'qr_info': "Ce QR Code redirige vers votre lien court et permet de suivre les scans.",
    'dl_qr': "⬇️ Télécharger le QR du lien",
    'stats_btn': "📊 Voir les stats",
    'copy_btn': "📋 Copier le lien",
    'err_db': "❌ Erreur : Base de données non connectée.",
    'err_taken': "❌ Cet alias est déjà utilisé.",
}

    },
    'en': {
        'common': {
            'btn_add': "+ Add a row",
            'btn_generate': "🚀 Generate file",
            'btn_remove': "Remove",
            'btn_download': "⬇️ Download",
            'placeholder_url': "URL link or @handle",
            'error_empty': "Please fill in at least one field.",
            'loading': "Processing...",
        },
        'social': {
            'title': "Your Digital Identity",
            'sub': "Centralize all your networks. Select a platform and add your link.",
            'qr_header': "MY DIGITAL PRESENCE:",
            'filename': "digital-identity.png"
        },
        'vcard':{
    'title': "Digital Business Card (VCard)",
    'sub': "Generate a QR Code that saves your full contact details into your clients' and partners' address books.",
    'fn': "First Name", 'ln': "Last Name",
    'org': "Shop / Company", 'job': "Job Title / Role",
    'tel': "Phone Number", 'email': "Pro Email",
    'li': "LinkedIn (URL)", 'web': "Website / Shop",
    'adr': "Physical Address (for GPS)",
    'btn': "🚀 Generate My Pro Card",
    'filename': "vcard-pro-retailbox.png"
},
'whatsapp':{
    'title': "Direct WhatsApp QR",
    'sub': "Generate a link that instantly opens a WhatsApp chat with a pre-filled message.",
    'label_tel': "Phone Number (with country code)",
    'ph_tel': "e.g. 44123456789",
    'label_msg': "Automatic Message (optional)",
    'ph_msg': "e.g. Hello, I would like more information about...",
    'btn': "🚀 Generate WhatsApp QR",
    'filename': "whatsapp-pro.png"
},

'soldes':{
    'title': "Sales Label & A4 Sheet Generator",
    'sub': "Create your sales labels with crossed-out prices. The system generates an HD image and an A4 PDF sheet (24 labels) ready for standard adhesive sticker sheets.",
    'label_item': "Product Name / Reference",
    'ph_item': "e.g. Blue Linen Shirt",
    'label_old': "Original Price (€)",
    'label_new': "Sale Price (€)",
    'label_code': "EAN-13 Barcode (12 digits)",
    'btn': "🚀 Create Image & PDF Sheet",
    'preview': "Label Preview:",
    'dl_png': "⬇️ Image only (PNG)",
    'dl_pdf': "📄 A4 Sheet (24 labels)",
    'error': "Error: Please check that the code contains 12 digits."
},
'barcode':
{
    'title': "Expert Barcode Generator",
    'sub': "Enter your data or create a technical sheet for your inventory.",
    'label_format': "Barcode Format",
    'opt_ean': "EAN-13 (Retail Standard)",
    'opt_128': "Code 128 (Logistics / Data)",
    'ph_ean': "Enter exactly 12 digits",
    'ph_key': "Key (e.g. SKU)",
    'ph_val': "Value",
    'ean_info': "The 13th check digit is calculated automatically.",
    'btn_add': "+ Add data row",
    'btn_gen': "🚀 Generate Barcode",
    'err_ean': "Error: EAN-13 requires exactly 12 digits.",
    'err_empty': "Error: Please enter at least one data point.",
    'err_long': "Error: Too much data for barcode readability.",
    'encoded': "Encoded data:",
    'dl': "⬇️ Download Barcode"
},
'rembg': {
    'title': "AI Background Removal",
    'sub': "Automatically remove the background from your product photos for a professional studio look.",
    'label_file': "Select your photo (JPG, PNG)",
    'btn_run': "🚀 Start AI Removal",
    'success': "Processing complete!",
    'dl_btn': "⬇️ Download transparent PNG",
    'filename': "retailbox-no-bg.png"
},
'qr': {
    'title': "Pro QR Code Generator",
    'sub': "Customize your QR Code for restaurant menus, shops, or social media.",
    'label_type': "Content Type",
    'opt_url': "Simple URL Link",
    'opt_kv': "Key-Value Data (Sheet)",
    'label_fc': "QR Color",
    'label_bc': "Background Color",
    'label_logo': "Brand Logo (Optional)",
    'btn_gen': "🚀 Generate QR Code",
    'err_empty': "Error: No data entered.",
    'dl_btn': "⬇️ Download QR Code PNG",
    'filename': "pro-qrcode-retailbox.png",
    'ph_url': "Enter link (e.g. https://...)"
},


'wifi': {
    'title': "Wi-Fi QR Code Generator",
    'sub': "Provide instant connection to your customers. No password typing, just one scan.",
    'label_ssid': "Network Name (SSID)",
    'ph_ssid': "e.g. Shop_WiFi",
    'label_pass': "Password",
    'ph_pass': "Your Wi-Fi key",
    'label_type': "Security",
    'btn': "🚀 Generate Wi-Fi Access",
    'tip': "💡 Tip: Use the native iPhone 'Camera' app for a smooth automatic connection.",
    'filename': "wifi-access-pro.png"
},
'shortener':{
    'title': "RetailLink: Shortener & Stats",
    'sub': "Create memorable URLs and track engagement in real-time.",
    'label_url': "Destination Link (Long URL)",
    'label_custom': "Custom Alias (Optional)",
    'ph_custom': "e.g. spring-sale",
    'btn_gen': "🚀 Shorten and Activate",
    'res_title': "✅ Your RetailLink is ready!",
    'qr_info': "This QR Code redirects to your short link and allows scan tracking.",
    'dl_qr': "⬇️ Download Link QR",
    'stats_btn': "📊 View Stats",
    'copy_btn': "📋 Copy Link",
    'err_db': "❌ Error: Database not connected.",
    'err_taken': "❌ This alias is already taken.",
}


    }
}

FOOTER_DATA = {
    'fr': {
        'h_usage': "🚀 Usage & Service",
        'p_usage': "Génération technique haute performance en mémoire vive pour retailers.",
        'h_privacy': "🛡️ Confidentialité",
        'p_privacy': "Zéro stockage sur nos serveurs. Vos données et images sont éphémères.",
        'h_ugc': "👤 Propriété UGC",
        'p_ugc': "User Generated Content : Vous détenez 100% des droits sur vos fichiers générés.",
        'links': {
            'about': "À Propos", 'guide': "Guide Complet", 'faq': "FAQ",
            'terms': "Conditions", 'privacy': "Vie Privée", 'ugc': "UGC", 'contact': "Contact"
        }
    },
    'en': {
        'h_usage': "🚀 Usage & Service",
        'p_usage': "High-performance technical generation in RAM for retailers.",
        'h_privacy': "🛡️ Privacy",
        'p_privacy': "Zero storage on our servers. Your data and images are ephemeral.",
        'h_ugc': "👤 UGC Ownership",
        'p_ugc': "User Generated Content: You own 100% of the rights to your generated files.",
        'links': {
            'about': "About", 'guide': "Full Guide", 'faq': "FAQ",
            'terms': "Terms", 'privacy': "Privacy Policy", 'ugc': "UGC", 'contact': "Contact"
        }
    }
}


MULTILINGUAL_DATA_MetaTags = {
    'fr': {
        # ... tes autres données (faq, guides, etc.)
        'meta': {
            'title': "RetailBox | Outils Commerce & Identité Digitale",
            'desc': "RetailBox : Outils pro gratuits. Générez QR Codes HD avec logo, réducteur de liens (Shortener), étiquettes de soldes prix barré, codes-barres EAN13 et détourage photo IA.",
            'keywords': "réducteur de lien gratuit, URL shortener pro, RetailLink, générer QR Code gratuit, barcode EAN13, étiquettes soldes prix barré, détourage photo IA, identité digitale",
            'og_title': "RetailBox | La Suite d'Outils Digitaux pour Commerçants",
            'og_desc': "9 outils gratuits en un clic : QR Codes, Barcodes, Shortener, IA Image, et Identité Digitale. Sans inscription."
        }
    },
    'en': {
        # ... tes autres données
        'meta': {
            'title': "RetailBox | Commerce Tools & Digital Identity",
            'desc': "RetailBox: Free pro tools. Generate HD QR Codes with logo, URL Shortener, sale labels with crossed-out prices, EAN13 barcodes, AI background removal.",
            'keywords': "free link shortener, URL shortener pro, RetailLink, generate free QR Code, QR Code with logo, barcode EAN13, sale labels, AI background removal, digital identity",
            'og_title': "RetailBox | Digital Toolset for Retailers & Creators",
            'og_desc': "9 free tools in one click: QR Codes, Barcodes, Shortener, AI Image, and Digital Identity. No registration required."
        }
    }
}