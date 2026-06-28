# MON COMMIS — Conciergerie & Courses (Abidjan)

Plateforme **Mon Commis** : un site vitrine statique (WOW) + un système de gestion Django
pour piloter toutes les prestations (deux pôles : Commissionnaire & Secrétariat à distance).

```
MON COMMIS/
├── site/              # Vitrine statique générée (HTML/CSS/JS) — déployable sur mutualisé
│   ├── build_commis.py    # générateur (régénère toutes les pages)
│   ├── css/  js/  img/
│   └── *.html (générés)   # index, services, secretariat, a-propos, contact, 404
├── moncommis/         # projet Django (settings, urls)
├── gestion/           # app métier (modèles, admin, migrations + seed CGV)
├── api/               # endpoint POST /api/demandes/ (reçoit le formulaire vitrine)
├── .commis/           # venv Python (non versionné)
└── .env               # secrets locaux (non versionné — voir .env.example)
```

## 1) Vitrine statique

```bash
cd site
python3 build_commis.py        # régénère index/services/secretariat/a-propos/contact/404
                               # + robots.txt, sitemap.xml, llms.txt, site.webmanifest
# Prévisualiser :
python3 -m http.server 8765    # http://localhost:8765
```

- Charte : **navy `#112844` + cyan `#1f9ec4`** (couleurs du logo), police Bricolage Grotesque.
- Écosystème orbital (« logo_pastilles ») sur l'accueil ; galerie photos ; formulaire double
  canal (envoi API **ou** WhatsApp).
- ⚠️ **Logo = placeholder** : déposer le logo officiel et adapter `brand()` dans
  `build_commis.py` (emblème provisoire : `img/brand/emblem-mon-commis.svg`).
- Cache-busting : incrémenter `ASSETV` dans `build_commis.py` à chaque modif CSS/JS.

### Lien vitrine → backend
La vitrine POST vers `window.COMMIS_API_URL` (défini dans `head()`, défaut `/api/demandes/`).
Si le backend est injoignable, repli automatique sur WhatsApp. En production, pointer cette
URL vers le domaine de l'API et autoriser l'origine dans `CORS_ALLOWED_ORIGINS`.

## 2) Système de gestion (Django)

```bash
python3 -m venv .commis && source .commis/bin/activate
pip install -r requirements.txt
cp .env.example .env           # puis générer une SECRET_KEY
python manage.py migrate       # crée la base + préremplit zones & formules (CGV)
python manage.py createsuperuser
python manage.py runserver     # admin : http://127.0.0.1:8000/admin/
```

- **Modèles** : `Client`, `Commis`, `Zone`, `Mission` (cœur — courses à l'acte),
  `FormuleSecretariat` (STARTER/CONFORT/PREMIUM), `Souscription`, `Paiement`.
- **Admin** = back-office de la promotrice : liste filtrable des demandes, affectation d'un
  commis, changement de statut (actions groupées), tarification (urgence +50 % auto), paiements.
- **API** : `POST /api/demandes/` (JSON) crée une `Mission` (canal = Formulaire) ; anti-spam
  basique + CORS limité aux origines de la vitrine.

## Données de référence (CGV Mon Commis)
- Formules Secrétariat : STARTER 15 000 · CONFORT 25 000 · PREMIUM 50 000 FCFA/mois.
- Zones : Standard (inclus) · Étendue (+1 000–2 000 FCFA) · Spéciale (sur devis).
- Urgence +50 % · frais réglés avant la mission.

## À confirmer avec le client
Domaine & email officiels, adresse, liens réseaux (TikTok/Instagram/Facebook), grille
tarifaire détaillée du pôle Commissionnaire, **fichier logo officiel**.
