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


SOCIAL_NETWORKS = [
    ("Instagram", "Instagram"), ("TikTok", "TikTok"), ("YouTube", "YouTube"),
    ("Threads", "Threads"), ("Pinterest", "Pinterest"), ("Twitch", "Twitch"),
    ("Facebook", "Facebook"), ("LinkedIn", "LinkedIn"), ("X", "X (Twitter)"),
    ("Spotify", "Spotify"), ("Shopify", "Ma Boutique / Shopify"),
    ("WhatsApp", "WhatsApp"), ("Website", "Site Web Personnel")
]