styles= f"""
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

    
    /* Barre supérieure : s'adapte au mode clair/sombre */
    /* Barre supérieure Inline */
    .top-nav-bar {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 15px;
        padding: 0.8rem 0;
        border-bottom: 1px solid var(--pico-border-color);
        margin-bottom: 2rem;
    }}

    /* Conteneur de défilement (Scroll) */
    .nav-scroll-container {{
        flex: 1;
        overflow-x: auto;
        white-space: nowrap;
        display: flex;
        justify-content: center;
        scrollbar-width: none; /* Cache la barre sur Firefox */
    }}
    .nav-scroll-container::-webkit-scrollbar {{ display: none; }} /* Cache la barre sur Chrome/Safari */

    .nav-pills {{
        display: flex;
        gap: 0.8rem;
        padding: 4px;
        background: rgba(0, 0, 0, 0.03); /* Fond léger pour l'effet "capsule" */
        border-radius: 18px;
        min-width: max-content;
    }}

    /* L'onglet individuel (Le Pill) */
    .nav-pills a {{
        padding: 0.6rem 1.2rem !important;
        border-radius: 14px !important;
        background: transparent;
        border: 1px solid transparent !important;
        font-weight: 700;
        font-size: 0.85rem;
        color: var(--pico-color) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        display: inline-flex;
        align-items: center;
        gap: 8px;
        text-decoration: none !important;
    }}

    /* Effet au survol (Hover) */
    .nav-pills a:hover:not(.active) {{
        background: rgba(79, 70, 229, 0.08) !important;
        color: var(--primary) !important;
        transform: translateY(-1px);
    }}

    /* L'onglet ACTIF (Le Gradient) */
    .nav-pills a.active {{
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
        border: none !important;
    }}

    /* ADAPTATION DARK MODE IPHONE */
    @media (prefers-color-scheme: dark) {{
        .nav-pills {{ background: rgba(255, 255, 255, 0.05); }}
        .nav-pills a {{ color: #f8fafc !important; }}
        .nav-pills a:hover:not(.active) {{ background: rgba(255, 255, 255, 0.1) !important; }}
    }}

    /* RESPONSIVE MOBILE */
    @media (max-width: 800px) {{
        .nav-scroll-container {{ justify-content: flex-start; }}
        .top-nav-bar {{ padding: 0.5rem 0.2rem; gap: 8px; }}
        .nav-pills a {{ padding: 0.5rem 1rem !important; font-size: 0.8rem !important; }}
        .lang-btn {{ font-size: 0.7rem !important; padding: 0.4rem 0.6rem !important; }}
    }}

    .services-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 350px), 1fr)); gap: 2rem; margin-top: 2rem; }}
    .modern-card {{ border: 1px solid #e2e8f0; padding: 2rem; border-radius: 24px; height: 100%; display: flex; flex-direction: column; background: #ffffff; transition: 0.3s ease; }}
    .modern-card:hover {{ transform: translateY(-6px); box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); }}
    .card-header-flex {{ display: flex; align-items: center; gap: 15px; margin-bottom: 1.2rem; }}
    .modern-card footer {{ background: transparent !important; border-top: 1px solid #e2e8f0; padding: 1.2rem 0 0 0 !important; margin-top: auto !important; }}

    /* Style de base (Light Mode) */
    button, .btn-full {{ 
        width: 100% !important; 
        padding: 0.9rem !important; 
        border-radius: 14px !important; 
        font-weight: 700 !important; 
        border: 1px solid #e2e8f0; 
        background: #f8fafc; 
        color: #1e293b; 
        cursor: pointer; 
        transition: 0.3s; 
    }}

    /* Correction pour le Dark Mode */
    @media (prefers-color-scheme: dark) {{
        button, .btn-full {{
            background: #334155 !important; /* Gris-bleu sombre pro */
            color: #ffffff !important; 
            border-color: #475569 !important;
        }}
    }}

    /* Effet Hover (Identique dans les deux modes) */
    button:hover, .btn-full:hover {{ 
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%) !important; 
        color: white !important; 
        border-color: transparent !important; 
        transform: scale(1.01);
    }}
                     
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
    .faq-link {{
        color: var(--primary) !important;
        font-weight: 700;
        text-decoration: underline !important; /* On garde l'underline ici pour l'accessibilité dans le texte */
    }}
    .faq-link:hover {{
        color: var(--secondary) !important;
    }}


    /* Grille spécifique pour le Guide */
    .guide-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(min(100%, 450px), 1fr));
        gap: 2rem;
        margin-top: 2rem;
    }}

    .guide-card {{
        border: 1px solid #e2e8f0;
        padding: 2.5rem !important; /* Plus d'espace interne */
        border-radius: 24px;
        background: #ffffff;
        display: flex;
        flex-direction: column;
        gap: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }}

    @media (prefers-color-scheme: dark) {{
        .guide-card {{ background: #1e293b !important; border-color: #334155 !important; }}
    }}

    .guide-card h4 {{
        margin: 0;
        font-size: 1.5rem;
        font-weight: 800;
    }}

    .guide-card p {{
        font-size: 1rem;
        line-height: 1.7;
        color: var(--pico-color);
        opacity: 0.9;
    }}


/* Grille des lignes sociales */
  .social-row {{
        display: grid;
        grid-template-columns: 1fr 2fr 50px;
        gap: 12px;
        align-items: center;
        background: #f8fafc;
        padding: 1.2rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
    }}
    /* BOUTON SUPPRIMER ROUGE FIXE */
   /* Bloc conteneur de chaque réseau social */
    .social-row {{
        display: flex;
        flex-direction: column; /* Empile les éléments verticalement */
        gap: 10px;
        background: rgba(0, 0, 0, 0.03);
        padding: 1.2rem;
        border-radius: 18px;
        margin-bottom: 1.5rem;
        border: 1px solid #e2e8f0;
    }}

    /* Bouton SUPPRIMER : Rouge Fixe, Largeur Totale, Sans traits */
    .btn-remove-final {{
        background-color: #ef4444 !important; /* Rouge pur AdSense compatible */
        color: #ffffff !important;
        border: none !important;
        width: 100% !important; /* Toute la largeur */
        height: 48px !important;
        display: flex !important;
        align-items: center;
        justify-content: center;
        gap: 8px;
        border-radius: 12px !important;
        cursor: pointer;
        font-weight: 700 !important;
        text-decoration: none !important;
        box-shadow: none !important;
    }}

    .btn-remove-final:hover {{
        background-color: #dc2626 !important; /* Rouge plus sombre au survol */
    }}

    /* Forcer la visibilité des inputs dans le bloc */
    .social-row select, .social-row input {{
        margin-bottom: 0 !important;
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
    }}

    @media (prefers-color-scheme: dark) {{
        .social-row {{ background: rgba(255, 255, 255, 0.05); border-color: #334155; }}
    }}

"""