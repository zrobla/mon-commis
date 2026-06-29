# -*- coding: utf-8 -*-
"""
Générateur du site vitrine MON COMMIS — Conciergerie & Courses (Abidjan, CI).
Site statique FR (XOF). Design aligné sur NEXUS DKS GROUP (hero slider immersif,
cartes photo, écosystème orbital), reteinté aux couleurs Mon Commis (navy + cyan).

6 grandes lignes de services, chacune avec sa page dédiée :
  Courses · Démarches administratives · Shopping & Cadeaux · Dépôt & retrait de colis ·
  Secrétariat à distance · Autres (sur-mesure).

Le formulaire « Demander une prestation » alimente le système Django (POST /api/demandes/),
avec repli WhatsApp.

Régénère tout :  python3 build_commis.py
"""
import os
import json
import math
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))

SITE = {
    "name": "Mon Commis",
    "legal": "MON COMMIS",
    "domain": "https://moncommis.ci",          # ⚠️ à confirmer (placeholder)
    "email": "contact@moncommis.ci",            # ⚠️ à confirmer (placeholder)
    "tel1_disp": "07 47 79 10 73",
    "tel1_href": "+2250747791073",
    "wa": "2250747791073",
    "addr": "Abidjan, Côte d'Ivoire",
    "city": "Abidjan",
    "geo": {"lat": "5.3599517", "lng": "-4.0082563"},
    "year": "2026",
}
ASSETV = "20260629c3"  # cache-busting — incrémenter à chaque modif CSS/JS

# ---------------------------------------------------------------- Icônes SVG
_I = {
 "check":   '<path d="M20 6 9 17l-5-5"/>',
 "arrow":   '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "send":    '<path d="M22 2 11 13M22 2l-7 20-4-9-9-4 20-7z"/>',
 "phone":   '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2 4.2 2 2 0 0 1 4 2h3a2 2 0 0 1 2 1.7c.1 1 .4 2 .7 2.9a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.1-1.1a2 2 0 0 1 2.1-.5c.9.3 1.9.6 2.9.7A2 2 0 0 1 22 16.9z"/>',
 "mail":    '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
 "pin":     '<path d="M12 21s-7-5.5-7-11a7 7 0 0 1 14 0c0 5.5-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
 "message": '<path d="M21 11.5a8.5 8.5 0 0 1-12.3 7.6L3 21l1.9-5.7A8.5 8.5 0 1 1 21 11.5z"/>',
 "cart":    '<circle cx="9" cy="20" r="1.4"/><circle cx="17" cy="20" r="1.4"/><path d="M3 4h2l2.4 12.4a1 1 0 0 0 1 .8h8.7a1 1 0 0 0 1-.8L21 8H6"/>',
 "pill":    '<rect x="3" y="9" width="18" height="6" rx="3" transform="rotate(45 12 12)"/><path d="M8.5 8.5 15.5 15.5"/>',
 "stamp":   '<path d="M5 21h14M6 18h12v-1a2 2 0 0 0-2-2h-1.5l.6-3.2A3 3 0 0 0 12.2 8h-.4a3 3 0 0 0-2.9 3.8L9.5 15H8a2 2 0 0 0-2 2v1z"/>',
 "gift":    '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M5 12v9h14v-9M12 8v13"/><path d="M12 8S10.5 3 8 4.5 9 8 12 8zM12 8s1.5-5 4-3.5S15 8 12 8z"/>',
 "box":     '<path d="m21 8-9-5-9 5 9 5 9-5z"/><path d="M3 8v8l9 5 9-5V8M12 13v8"/>',
 "doc":     '<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M10 12h5M10 16h5"/>',
 "calendar":'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 9h18M8 3v4M16 3v4"/>',
 "grid":    '<rect x="3" y="3" width="7.5" height="7.5" rx="1.4"/><rect x="13.5" y="3" width="7.5" height="7.5" rx="1.4"/><rect x="3" y="13.5" width="7.5" height="7.5" rx="1.4"/><rect x="13.5" y="13.5" width="7.5" height="7.5" rx="1.4"/>',
 "clock":   '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "bolt":    '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>',
 "shield":  '<path d="M12 3 5 6v6c0 4 3 7 7 9 4-2 7-5 7-9V6l-7-3z"/><path d="m9 12 2 2 4-4"/>',
 "heart":   '<path d="M12 20S4 14.5 4 9a4 4 0 0 1 8-1 4 4 0 0 1 8 1c0 5.5-8 11-8 11z"/>',
 "users":   '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 5.5a3.5 3.5 0 0 1 0 7M22 20a6.5 6.5 0 0 0-5-6.3"/>',
 "wallet":  '<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18M16 14h2"/>',
 "route":   '<circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="18" r="2.5"/><path d="M8.5 6H15a3 3 0 0 1 0 6H9a3 3 0 0 0 0 6h6.5"/>',
 "bell":    '<path d="M18 8a6 6 0 1 0-12 0c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.7 21a2 2 0 0 1-3.4 0"/>',
 "list":    '<path d="M8 6h13M8 12h13M8 18h13M3 6h.01M3 12h.01M3 18h.01"/>',
 "search":  '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
 "down":    '<path d="m6 9 6 6 6-6"/>',
 "star":    '<path d="m12 3 2.6 5.5 6 .8-4.4 4.2 1.1 6L12 16.8 6.7 19.5l1.1-6L3.4 9.3l6-.8L12 3z"/>',
 "sparkle": '<path d="M12 3v6M9 6h6M5 13v4M3 15h4M16 11l1.5 3.5L21 16l-3.5 1.5L16 21l-1.5-3.5L11 16l3.5-1.5L16 11z"/>',
 "map":     '<path d="m9 4 6 2 6-2v14l-6 2-6-2-6 2V6z"/><path d="M9 4v14M15 6v14"/>',
 "building":'<path d="M3 21h18M6 21V4h9v17M15 9h3v12"/><path d="M9 8h2M9 12h2M9 16h2"/>',
 "key":     '<circle cx="8" cy="8" r="4"/><path d="m11 11 9 9M17 17l2-2M20 20l1-1"/>',
 "badge":   '<circle cx="12" cy="9" r="6"/><path d="m9.2 9 2 2 3.6-3.6"/><path d="M8 14l-1 7 5-3 5 3-1-7"/>',
}
def ico(name, cls=""):
    c = "nx-svg" + ((" " + cls) if cls else "")
    return '<svg class="%s" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % (c, _I.get(name, _I["check"]))

SOCIAL = {
 "facebook": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13.5 22v-8.1h2.7l.4-3.2h-3.1V8.7c0-.9.2-1.6 1.6-1.6H17V4.2c-.4-.1-1.5-.2-2.8-.2-2.8 0-4.7 1.7-4.7 4.8v2H6.8v3.2h2.7V22h4Z"/></svg>',
 "instagram": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5Zm0 2.3A2.7 2.7 0 0 0 4.3 7v10A2.7 2.7 0 0 0 7 19.7h10a2.7 2.7 0 0 0 2.7-2.7V7A2.7 2.7 0 0 0 17 4.3H7Zm10.2 1.5a1.1 1.1 0 1 1 0 2.2 1.1 1.1 0 0 1 0-2.2ZM12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10Zm0 2.3A2.7 2.7 0 1 0 12 14.7 2.7 2.7 0 0 0 12 9.3Z"/></svg>',
 "tiktok": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.5 3c.3 2.1 1.5 3.6 3.5 3.9v2.6c-1.3.1-2.5-.3-3.6-1v5.9c0 3.4-2.6 5.6-5.6 5.6A5.4 5.4 0 0 1 5.5 14a5.3 5.3 0 0 1 6-5.3v2.7a2.7 2.7 0 0 0-3.3 2.6 2.6 2.6 0 0 0 5.2.1V3h3.1z"/></svg>',
 "whatsapp": '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 3C9 3 3.3 8.7 3.3 15.7c0 2.4.7 4.7 1.9 6.7L3 29l6.8-2.1c1.9 1 4 1.6 6.2 1.6 7 0 12.7-5.7 12.7-12.7S23 3 16 3Zm0 23c-1.9 0-3.7-.5-5.3-1.5l-.4-.2-3.9 1.2 1.2-3.8-.3-.4c-1.1-1.7-1.6-3.6-1.6-5.6C5.7 10 10.3 5.4 16 5.4S26.3 10 26.3 15.7 21.7 26 16 26Zm5.7-7.5c-.3-.2-1.8-.9-2.1-1-.3-.1-.5-.2-.7.2-.2.3-.8 1-.9 1.2-.2.2-.3.2-.6.1-.3-.2-1.3-.5-2.5-1.5-.9-.8-1.5-1.8-1.7-2.1-.2-.3 0-.5.1-.6l.5-.5c.1-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1.1 2.8 1.2 3c.2.2 2.1 3.2 5 4.5.7.3 1.2.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.8-.7 2-1.4.3-.7.3-1.3.2-1.4-.1-.1-.3-.2-.6-.4Z"/></svg>',
}

# ================================================================ DONNÉES
# 6 grandes lignes de services (chacune = une page dédiée), avec sous-détails.
SERVICES = [
 {
  "slug": "courses", "title": "Courses", "short": "Courses", "icon": "cart",
  "img": "img/services/courses.jpg",
  "tagline": "Approvisionnement du quotidien — marché, officine, supérette — sélectionné et livré.",
  "lead": "Mon Commis prend en charge l'intégralité de votre approvisionnement quotidien : marché vivrier, "
          "officine pharmaceutique et commerces de proximité. Vous transmettez votre liste et votre budget ; "
          "nous assurons la sélection des produits, le contrôle de la fraîcheur et la livraison à votre adresse, "
          "dans toutes les communes d'Abidjan.",
  "sub": [
    ("cart", "Approvisionnement au marché", "Achat de denrées vivrières, produits frais et condiments, avec contrôle de la qualité et respect strict du budget alloué."),
    ("pill", "Officine & exécution d'ordonnances", "Exécution de vos ordonnances et retrait de médicaments en officine, dans le respect de la confidentialité — recours à la pharmacie de garde si nécessaire."),
    ("doc", "Achats récurrents", "Réassort planifié en supérette et commerces de proximité, pour les particuliers comme pour les professionnels."),
  ],
  "inclus": ["Sélection contrôlée selon votre budget", "Livraison dans votre commune", "Confidentialité des achats sensibles"],
  "gallery": ["courses.jpg", "pharmacie.jpg", "marche-2.jpg"],
 },
 {
  "slug": "demarches", "title": "Démarches administratives", "short": "Démarches", "icon": "stamp",
  "img": "img/services/demarches.jpg",
  "tagline": "Dépôt, instruction et retrait de vos dossiers administratifs — sans file d'attente.",
  "lead": "Mon Commis agit comme votre mandataire pour vos formalités administratives : mairie, CNPS, "
          "administration fiscale, préfecture, juridictions et études notariales. Nous assurons le dépôt des "
          "pièces, le suivi de l'instruction et le retrait de vos documents officiels, en vous tenant informé "
          "à chaque étape de la procédure.",
  "sub": [
    ("stamp", "Dépôt & retrait de dossiers", "Constitution, dépôt et retrait de vos dossiers auprès des administrations : mairie, CNPS, impôts, préfecture, juridictions, notaire et structures hospitalières."),
    ("doc", "Documents officiels", "Obtention d'actes d'état civil, d'extraits de casier judiciaire, de copies de diplômes et autres pièces justificatives, sur présentation des mandats requis."),
    ("shield", "Résultats & pièces médicales", "Récupération confidentielle de vos résultats d'analyses et documents de santé, dans le respect du secret médical."),
  ],
  "inclus": ["Gestion de la file d'attente et des guichets", "Suivi de l'instruction du dossier", "Traitement confidentiel des pièces justificatives"],
  "gallery": [],
 },
 {
  "slug": "shopping", "title": "Shopping & cadeaux", "short": "Shopping", "icon": "gift",
  "img": "img/services/shopping.jpg",
  "tagline": "Sourcing, négociation et livraison de l'article ou du cadeau recherché.",
  "lead": "Vous recherchez un article précis, un équipement ou un cadeau ? Mon Commis prend en charge le "
          "sourcing : identification du produit conforme à votre cahier des charges et à votre budget, "
          "négociation du prix, achat et livraison — avec conditionnement cadeau en option.",
  "sub": [
    ("gift", "Articles & équipements", "Recherche et achat d'articles vestimentaires, d'accessoires et d'équipements selon vos spécifications et votre budget."),
    ("sparkle", "Aménagement & décoration", "Sourcing d'objets de décoration et d'équipement de la maison : nous identifions les références correspondant à votre projet."),
    ("heart", "Cadeaux & conditionnement", "Sélection d'un cadeau adapté à l'occasion et au destinataire, avec conditionnement soigné sur demande."),
  ],
  "inclus": ["Conseil & sourcing personnalisé", "Tarif prestation 5 000 à 15 000 FCFA selon complexité", "Conditionnement cadeau possible"],
  "gallery": ["shopping.jpg", "cadeaux.jpg", "shopping-bag.jpg"],
 },
 {
  "slug": "colis", "title": "Dépôt & retrait de colis", "short": "Colis", "icon": "box",
  "img": "img/services/colis.jpg",
  "tagline": "Acheminement sécurisé de vos plis et colis, avec remise contre signature.",
  "lead": "Mon Commis assure l'acheminement de vos plis, paquets et objets entre deux adresses dans Abidjan. "
          "Chaque envoi fait l'objet d'une prise en charge sécurisée, d'un suivi de bout en bout et d'une "
          "remise en main propre contre confirmation du destinataire.",
  "sub": [
    ("route", "Acheminement point à point", "Enlèvement à l'adresse d'origine et livraison à l'adresse de destination, au sein des zones desservies."),
    ("shield", "Remise contre signature", "Remise du colis au destinataire désigné, avec confirmation de livraison."),
    ("check", "Traçabilité de bout en bout", "Information du donneur d'ordre, de l'enlèvement jusqu'à la livraison effective."),
  ],
  "inclus": ["Prise en charge sécurisée", "Remise en main propre", "Frais selon la zone de livraison"],
  "gallery": ["colis.jpg", "colis-2.jpg"],
 },
 {
  "slug": "secretariat", "title": "Secrétariat à distance", "short": "Secrétariat", "icon": "calendar",
  "img": "img/services/secretariat.jpg",
  "tagline": "Gestion d'agenda externalisée : saisie, rappels et confirmation de vos rendez-vous.",
  "lead": "Le pôle Secrétariat à Distance de Mon Commis prend en charge la gestion externalisée de votre "
          "agenda professionnel : saisie de vos rendez-vous, transmission du programme hebdomadaire, rappels "
          "avant échéance et confirmation auprès de vos interlocuteurs. Trois formules d'abonnement mensuel — "
          "STARTER, CONFORT, PREMIUM — calibrées selon votre volume d'activité.",
  "sub": [
    ("calendar", "Gestion d'agenda", "Saisie de vos rendez-vous dans un agenda partagé (Google Calendar) et transmission du programme hebdomadaire chaque dimanche."),
    ("bell", "Rappels & confirmations", "Rappel personnalisé 30 minutes avant chaque échéance et confirmation téléphonique auprès de vos interlocuteurs, selon la formule souscrite."),
    ("star", "Formules calibrées", "STARTER, CONFORT ou PREMIUM : gestion du carnet de contacts et recherche d'informations sur les formules supérieures."),
  ],
  "inclus": ["Agenda partagé (Google Calendar)", "Rappels 30 min avant chaque RDV", "Formules dès 15 000 FCFA/mois"],
  "gallery": ["secretariat-2.jpg", "secretariat-3.jpg"],
  "is_secretariat": True,
 },
 {
  "slug": "autres", "title": "Autres services", "short": "Autres", "icon": "grid",
  "img": "img/services/autres.jpg",
  "tagline": "Missions sur-mesure : un cahier des charges, une solution adaptée.",
  "lead": "Votre besoin sort du cadre habituel ? Mon Commis conçoit une prestation sur-mesure à partir de "
          "votre cahier des charges : analyse de la demande, organisation logistique et exécution, pour des "
          "missions ponctuelles ou récurrentes, au bénéfice des particuliers comme des professionnels.",
  "sub": [
    ("sparkle", "Missions sur-mesure", "Analyse de votre demande et mise en place d'une solution adaptée, même pour les besoins atypiques."),
    ("clock", "Ponctuel ou récurrent", "Interventions à la demande ou planifiées selon une périodicité définie avec vous."),
    ("users", "Particuliers & professionnels", "Prestations calibrées en fonction de vos contraintes opérationnelles et de votre budget."),
  ],
  "inclus": ["Devis clair en FCFA", "Flexibilité opérationnelle", "Interlocuteur unique"],
  "gallery": ["autres-2.jpg"],
 },
]
SERVICES_BY_SLUG = {s["slug"]: s for s in SERVICES}
# URL de chaque service (le Secrétariat est servi par sa page dédiée riche).
for _s in SERVICES:
    _s["url"] = "secretariat.html" if _s["slug"] == "secretariat" else f"service-{_s['slug']}.html"

# Slides du hero (design DKS) — (img, eyebrow, titre_html, h1?, lead, cta1, cta2, kpis[3])
HERO_SLIDES = [
 {"img": "img/hero/hero-courses.jpg", "is_h1": True,
  "eyebrow": "Mon Commis · Conciergerie & courses — Abidjan, Côte d'Ivoire",
  "title": 'Votre <span class="accent">commis de confiance</span>, au cœur d\'Abidjan.',
  "lead": "Courses, démarches administratives, shopping, colis et secrétariat à distance : "
          "une variété de services réunis chez un seul interlocuteur fiable. Vous décrivez, on s'occupe de tout.",
  "cta1": ("Demander un commis", "contact.html"), "cta2": ("Voir nos services", "services.html"),
  "kpis": [("grid", "Une variété de services", "un seul interlocuteur"),
           ("map", "Tout Abidjan", "toutes les communes"),
           ("clock", "Devis clair", "chiffré en FCFA")]},
 {"img": "img/hero/hero-shopping.jpg", "is_h1": False,
  "eyebrow": "Courses · Shopping · Colis · Démarches",
  "title": 'On s\'occupe de tout, <span class="accent">vous gagnez du temps</span>.',
  "lead": "Du marché à la pharmacie, du shopping aux démarches administratives et à l'acheminement de vos colis : "
          "déléguez les tâches qui grignotent vos journées et concentrez-vous sur l'essentiel.",
  "cta1": ("Découvrir les services", "services.html"), "cta2": ("Discuter sur WhatsApp", "https://wa.me/" + SITE["wa"]),
  "kpis": [("bolt", "Service express", "urgence dans l'heure"),
           ("shield", "Discrétion", "documents & achats sensibles"),
           ("wallet", "Paiement simple", "espèces & mobile money")]},
 {"img": "img/hero/hero-pharmacie.jpg", "is_h1": False,
  "eyebrow": "Pôle Secrétariat à Distance",
  "title": 'Un <span class="accent">secrétariat personnel</span> qui gère votre agenda.',
  "lead": "Vos rendez-vous saisis, rappelés et confirmés — vous ne ratez plus rien. "
          "Trois formules mensuelles, dès 15 000 FCFA, pour reprendre le contrôle de votre temps.",
  "cta1": ("Découvrir le secrétariat", "secretariat.html"), "cta2": ("Choisir une formule", "secretariat.html#formules"),
  "kpis": [("calendar", "Agenda partagé", "Google Calendar"),
           ("bell", "Rappels & confirmations", "avant chaque RDV"),
           ("star", "Dès 15 000 FCFA", "par mois")]},
]

FORMULES = [
 {"slug": "starter", "nom": "STARTER", "prix": "15 000", "rdv": "Jusqu'à 8 RDV / mois",
  "punch": "L'essentiel pour ne plus rien oublier.", "featured": False,
  "feats": [("Récapitulatif chaque dimanche", True), ("Rappels 30 min avant chaque RDV", True),
            ("Confirmation téléphonique", False), ("Gestion du carnet de contacts", False),
            ("Recherche d'infos / tarifs", False)]},
 {"slug": "confort", "nom": "CONFORT", "prix": "25 000", "rdv": "Jusqu'à 20 RDV / mois",
  "punch": "Le bon équilibre pour un agenda maîtrisé.", "featured": True,
  "feats": [("Récapitulatif chaque dimanche", True), ("Rappels 30 min avant chaque RDV", True),
            ("Confirmation téléphonique", True), ("Gestion du carnet de contacts", False),
            ("Recherche d'infos / tarifs", False)]},
 {"slug": "premium", "nom": "PREMIUM", "prix": "50 000", "rdv": "RDV illimités",
  "punch": "La sérénité totale, sans aucune limite.", "featured": False,
  "feats": [("Récapitulatif chaque dimanche", True), ("Rappels 30 min avant chaque RDV", True),
            ("Confirmation téléphonique", True), ("Gestion du carnet de contacts", True),
            ("Recherche d'infos / tarifs", True)]},
]

SECRET_INCLUS = [
 ("calendar", "Agenda partagé", "Saisie de vos rendez-vous dans Google Calendar, partagé avec vous."),
 ("bell", "Programme du dimanche", "Le programme de votre semaine envoyé chaque dimanche après-midi via WhatsApp."),
 ("clock", "Rappel 30 minutes avant", "Un rappel personnalisé avant chaque rendez-vous, pour ne rien manquer."),
 ("route", "Modifications en temps réel", "Gestion des reports et annulations de rendez-vous, en temps réel."),
 ("list", "Formulaire de collecte", "Un formulaire dédié pour nous transmettre vos rendez-vous facilement."),
]

# (nom, communes, frais_badge, icône, descriptif professionnel)
ZONES = [
 ("Zone Standard", "Cocody · Plateau · Marcory · Treichville · Adjamé · Attécoubé",
  "Inclus", "shield",
  "Périmètre central d'Abidjan — prestation au tarif de base, sans supplément de déplacement."),
 ("Zone Étendue", "Yopougon · Abobo · Bingerville · Anyama · Songon · Dabou · Grand-Bassam",
  "+1 000–2 000 FCFA", "map",
  "Couronne périphérique — supplément de déplacement appliqué selon la distance."),
 ("Zone Spéciale", "Toute destination hors du périmètre couvert",
  "Sur devis", "route",
  "Intervention sur devis préalable, établi en fonction de la destination."),
]

STEPS = [
 ("message", "Vous décrivez", "Envoyez votre besoin par WhatsApp ou via le formulaire — en quelques mots, c'est parti."),
 ("wallet", "On confirme & vous réglez", "Devis clair en FCFA. Les frais de commission sont réglés avant le début de la mission."),
 ("route", "Votre commis exécute", "Un commis de confiance s'occupe de tout et vous tient informé jusqu'à la remise en main propre."),
]

ARGS = [
 ("clock", "Vous gagnez du temps", "Déléguez vos courses et démarches ; concentrez-vous sur l'essentiel."),
 ("shield", "Confiance & discrétion", "Documents sensibles, ordonnances, colis : traités avec sérieux et confidentialité."),
 ("map", "Tout Abidjan couvert", "De Cocody à Yopougon jusqu'à Grand-Bassam — et au-delà sur devis."),
 ("bolt", "Service express", "Une urgence ? Intervention dans l'heure (supplément +50 %)."),
]

GALLERY = [
 ("marche.jpg", "Courses au marché", "Étal de fruits et légumes frais au marché à Abidjan"),
 ("pharmacie.jpg", "Pharmacie & ordonnances", "Retrait de médicaments et conseils en pharmacie"),
 ("cadeaux.jpg", "Shopping & cadeaux", "Cadeaux soigneusement sélectionnés et emballés"),
 ("colis.jpg", "Dépôt & retrait de colis", "Acheminement de colis en main propre à Abidjan"),
 ("shopping-bag.jpg", "Vos achats, livrés chez vous", "Sacs de shopping prêts à être livrés"),
]

TESTIMONIALS = [
 ("Mon Commis me fait mes courses au marché chaque semaine. Toujours à l'heure, produits bien choisis.", "Aïcha K.", "Cocody"),
 ("Ils ont retiré mes résultats médicaux et déposé un dossier à la CNPS le même jour. Un vrai gain de temps.", "Konan B.", "Plateau"),
 ("La formule Secrétariat CONFORT a changé mon organisation : je ne rate plus aucun rendez-vous.", "Mariam D.", "Marcory"),
]

# Champs spécifiques par service (en plus des champs communs nom/téléphone/zone/échéance/email).
# Adaptés à la nature de chaque prestation. Format : (name, label, type, placeholder_ou_options).
#   type ∈ {"text", "textarea", "options"} ("options" -> liste de valeurs pour un <select>).
SERVICE_FIELDS = {
 "courses": [
   ("sc_liste", "Liste des articles", "textarea", "Listez vos articles, quantités et marques : 2 kg de riz, 1 régime de banane, paracétamol 500 mg…"),
   ("sc_budget", "Budget approximatif", "text", "Ex. 25 000 FCFA"),
   ("sc_livraison", "Adresse de livraison", "text", "Commune, quartier, point de repère"),
 ],
 "demarches": [
   ("sc_organisme", "Administration concernée", "options", ["Mairie", "CNPS", "Direction des impôts", "Préfecture", "Tribunal / juridiction", "Étude notariale", "Structure hospitalière", "Autre administration"]),
   ("sc_dossier", "Nature du dossier / pièces", "textarea", "Décrivez la démarche : retrait d'acte de naissance, dépôt de dossier CNPS, extrait de casier judiciaire, légalisation de copie…"),
   ("sc_lieu", "Lieu de dépôt / retrait", "text", "Établissement et commune"),
 ],
 "shopping": [
   ("sc_article", "Article ou cadeau recherché", "textarea", "Décrivez l'article : type, marque, taille, couleur, occasion…"),
   ("sc_budget", "Budget alloué", "text", "Ex. 30 000 FCFA"),
   ("sc_emballage", "Conditionnement cadeau", "options", ["Oui, emballage cadeau", "Non merci"]),
 ],
 "colis": [
   ("sc_retrait", "Adresse de retrait", "text", "Commune, quartier, contact sur place"),
   ("sc_livraison", "Adresse de livraison", "text", "Commune, quartier, destinataire"),
   ("sc_nature", "Nature du colis", "options", ["Documents / pli", "Petit paquet", "Objet fragile", "Denrées", "Autre"]),
 ],
 "secretariat": [
   ("sc_formule", "Formule souhaitée", "options", ["STARTER — 15 000 FCFA/mois", "CONFORT — 25 000 FCFA/mois", "PREMIUM — 50 000 FCFA/mois", "À conseiller selon mon activité"]),
   ("sc_secteur", "Votre secteur d'activité", "text", "Profession libérale, santé, commerce, BTP…"),
   ("sc_volume", "Volume de RDV estimé / mois", "text", "Ex. environ 12 rendez-vous"),
 ],
 "autres": [
   ("sc_besoin", "Décrivez précisément votre besoin", "textarea", "Expliquez la tâche, le lieu d'intervention et le résultat attendu."),
   ("sc_frequence", "Fréquence", "options", ["Mission ponctuelle", "Hebdomadaire", "Mensuelle", "À définir ensemble"]),
 ],
}

# ---------------------------------------------------------------- BLOG (3 articles)
# Corps d'article : liste de blocs (type, contenu). type ∈ {h2, p, ul, quote}.
BLOG = [
 {
  "slug": "demarches-administratives-abidjan-sans-attente",
  "cat": "Démarches", "icon": "stamp", "img": "img/services/demarches.jpg",
  "service": "demarches",
  "date": "2026-06-10", "date_disp": "10 juin 2026", "read": "5 min de lecture",
  "title": "Démarches administratives à Abidjan : récupérez vos documents sans y perdre la journée",
  "excerpt": "Files d'attente, allers-retours, guichets fermés : les formalités administratives "
             "grignotent un temps précieux. Voici comment déléguer dépôt, suivi et retrait de vos dossiers.",
  "lead": "Acte de naissance, extrait de casier judiciaire, dossier CNPS, déclaration fiscale : à Abidjan, "
          "une simple formalité peut mobiliser une demi-journée entière entre déplacement, file d'attente et "
          "guichets engorgés. Pour un actif ou un chef d'entreprise, ce temps a un coût réel.",
  "body": [
    ("h2", "Le vrai coût d'une démarche administrative"),
    ("p", "Une formalité administrative ne se limite jamais au temps passé au guichet. Il faut compter le "
          "trajet, l'attente — souvent plusieurs heures — et, fréquemment, un second passage parce qu'une "
          "pièce manquait au dossier ou que l'agent compétent était absent. Pour une personne en activité, "
          "chaque déplacement représente une matinée de travail perdue."),
    ("p", "À cela s'ajoute l'incertitude : horaires variables, procédures qui évoluent, files qui s'allongent "
          "en début et en fin de mois. Sans une bonne connaissance du circuit, on multiplie les allers-retours."),
    ("h2", "Les démarches les plus chronophages"),
    ("ul", ["Retrait d'actes d'état civil et de copies certifiées en mairie ;",
            "Constitution et dépôt de dossiers à la CNPS ;",
            "Formalités auprès de l'administration fiscale et de la préfecture ;",
            "Obtention d'un extrait de casier judiciaire au tribunal ;",
            "Récupération de résultats médicaux et de documents hospitaliers."]),
    ("h2", "La solution Mon Commis : un mandataire qui gère l'attente à votre place"),
    ("p", "Mon Commis agit comme votre mandataire. Vous nous confiez la nature de la démarche et les pièces "
          "nécessaires ; nous nous chargeons du dépôt, du suivi de l'instruction et du retrait de vos documents. "
          "Vous êtes informé à chaque étape et vous ne vous déplacez plus inutilement."),
    ("quote", "Au lieu de poser une demi-journée de congé, j'ai reçu mon extrait de casier judiciaire le "
              "lendemain, sans bouger de mon bureau."),
    ("p", "Vos pièces justificatives sont traitées avec une stricte confidentialité, et les frais de la "
          "mission sont clairs et communiqués en FCFA avant toute intervention. Vous gardez le contrôle, "
          "nous prenons en charge la logistique et le temps d'attente."),
  ],
 },
 {
  "slug": "deleguer-courses-abidjan-budget-maitrise",
  "cat": "Courses", "icon": "cart", "img": "img/services/courses.jpg",
  "service": "courses",
  "date": "2026-06-04", "date_disp": "4 juin 2026", "read": "4 min de lecture",
  "title": "Déléguer ses courses à Abidjan sans exploser son budget : mode d'emploi",
  "excerpt": "Marché, officine, supérette : entre les embouteillages et la gestion du budget, faire ses "
             "courses devient une corvée. Déléguer ne veut pas dire dépenser plus — voici comment.",
  "lead": "Faire ses courses au marché ou en pharmacie à Abidjan, c'est composer avec les embouteillages, la "
          "chaleur, la négociation des prix et le contrôle de la fraîcheur. Beaucoup pensent que déléguer "
          "revient à payer plus cher. En réalité, une délégation bien cadrée protège votre temps… et votre budget.",
  "body": [
    ("h2", "Pourquoi les courses pèsent autant sur une journée"),
    ("p", "Entre le trajet jusqu'au marché vivrier, le temps de sélection des produits frais, le passage en "
          "officine et le retour, une simple tournée de courses peut mobiliser deux à trois heures. Multiplié "
          "par plusieurs fois dans la semaine, c'est un temps considérable soustrait à votre activité ou à votre famille."),
    ("h2", "Déléguer sans perdre le contrôle du budget"),
    ("p", "La clé d'une délégation maîtrisée tient en trois éléments : une liste précise, un budget plafond et "
          "un compte rendu transparent. Vous indiquez les articles, les quantités et le montant à ne pas "
          "dépasser ; le commis sélectionne, contrôle la qualité et respecte strictement l'enveloppe fixée."),
    ("ul", ["Une liste détaillée évite les achats superflus ;",
            "Un budget plafond cadre la dépense à l'avance ;",
            "Le contrôle de la fraîcheur garantit la qualité des produits ;",
            "La confidentialité couvre les achats sensibles, en pharmacie notamment."]),
    ("h2", "L'approche Mon Commis"),
    ("p", "Mon Commis prend en charge votre approvisionnement du quotidien — marché, officine, commerces de "
          "proximité — avec un objectif simple : vous restituer du temps sans alourdir votre budget. Vous "
          "transmettez votre liste, nous achetons au plus juste et nous livrons à votre adresse."),
    ("quote", "Je reçois mes courses du marché chaque semaine, produits bien choisis et budget respecté. "
              "Je récupère deux heures sur mon emploi du temps."),
    ("p", "Pour les achats récurrents, un réassort planifié peut être mis en place : vous ne pensez plus à "
          "vos courses, elles arrivent au bon moment."),
  ],
 },
 {
  "slug": "secretariat-a-distance-ne-plus-rater-rendez-vous",
  "cat": "Secrétariat", "icon": "calendar", "img": "img/services/secretariat.jpg",
  "service": "secretariat",
  "date": "2026-05-28", "date_disp": "28 mai 2026", "read": "5 min de lecture",
  "title": "Ne plus jamais oublier un rendez-vous : le secrétariat à distance pour professionnels occupés",
  "excerpt": "Un rendez-vous oublié, c'est un client perdu ou une opportunité manquée. Comment une gestion "
             "d'agenda externalisée sécurise votre emploi du temps, sans embaucher.",
  "lead": "Pour un professionnel libéral, un commerçant ou un dirigeant, l'agenda est le nerf de l'activité. "
          "Un rendez-vous oublié ou mal noté, c'est un client perdu, une opportunité manquée ou une "
          "réputation entamée. Pourtant, peu de structures peuvent justifier l'embauche d'un secrétaire à temps plein.",
  "body": [
    ("h2", "Le coût invisible d'une mauvaise gestion d'agenda"),
    ("p", "Les rendez-vous non honorés, les doubles réservations et les rappels oubliés ont un impact direct "
          "sur le chiffre d'affaires et sur l'image de l'entreprise. Gérer soi-même son agenda en plus de son "
          "cœur de métier conduit presque toujours à des oublis, surtout en période de forte activité."),
    ("h2", "Externaliser plutôt qu'embaucher"),
    ("p", "La gestion d'agenda externalisée offre les bénéfices d'un secrétariat sans les charges d'un poste "
          "à temps plein. Un prestataire dédié saisit vos rendez-vous, vous transmet votre programme, vous "
          "rappelle avant chaque échéance et confirme auprès de vos interlocuteurs."),
    ("ul", ["Saisie centralisée dans un agenda partagé (Google Calendar) ;",
            "Programme de la semaine transmis chaque dimanche ;",
            "Rappel personnalisé 30 minutes avant chaque rendez-vous ;",
            "Confirmation téléphonique auprès de vos contacts, selon la formule."]),
    ("h2", "Trois formules calibrées selon votre activité"),
    ("p", "Le pôle Secrétariat à Distance de Mon Commis propose trois formules d'abonnement mensuel : STARTER "
          "(15 000 FCFA, jusqu'à 8 RDV), CONFORT (25 000 FCFA, jusqu'à 20 RDV) et PREMIUM (50 000 FCFA, RDV "
          "illimités, avec gestion du carnet de contacts et recherche d'informations)."),
    ("quote", "Depuis que mon agenda est géré pour moi, je ne rate plus aucun rendez-vous — et mes clients "
              "reçoivent toujours leur rappel."),
    ("p", "Vous choisissez la formule adaptée à votre volume de rendez-vous, et vous reprenez le contrôle de "
          "votre temps. Sans embaucher, sans charges fixes."),
  ],
 },
]
# Métadonnées éditoriales (architecture article façon hub : hero + cartes synthèse + aside).
BLOG_EXTRA = {
 "demarches-administratives-abidjan-sans-attente": {
   "tags": ["Démarches", "Gain de temps", "Abidjan"],
   "audience": "Particuliers & pros",
   "points": [
     "Dépôt, suivi et retrait de vos dossiers menés de bout en bout.",
     "Un mandataire qui gère la file d'attente et les guichets à votre place.",
     "Traitement confidentiel de vos pièces justificatives.",
   ],
   "impacts": [
     "Plus de demi-journées perdues en déplacements.",
     "Un suivi clair de l'avancement de votre dossier.",
     "Des frais annoncés en FCFA avant toute intervention.",
   ],
   "keywords": ["Mairie", "CNPS", "Impôts", "Préfecture", "Acte d'état civil", "Casier judiciaire"],
   "essentiel": [
     "Confiez la nature de la démarche et les pièces requises.",
     "Mon Commis dépose, suit et retire le dossier à votre place.",
     "Vous êtes informé à chaque étape, sans vous déplacer.",
   ],
 },
 "deleguer-courses-abidjan-budget-maitrise": {
   "tags": ["Courses", "Budget", "Abidjan"],
   "audience": "Particuliers & pros",
   "points": [
     "Approvisionnement marché, officine et supérette délégué.",
     "Liste précise + budget plafond = dépense maîtrisée.",
     "Contrôle de la fraîcheur et des quantités.",
   ],
   "impacts": [
     "Deux à trois heures récupérées chaque semaine.",
     "Un budget respecté, sans achats superflus.",
     "Vos achats sensibles traités en toute discrétion.",
   ],
   "keywords": ["Marché", "Officine", "Supérette", "Liste de courses", "Budget plafond", "Livraison"],
   "essentiel": [
     "Transmettez votre liste et votre budget plafond.",
     "Le commis sélectionne et contrôle la qualité.",
     "Livraison à votre adresse, budget respecté.",
   ],
 },
 "secretariat-a-distance-ne-plus-rater-rendez-vous": {
   "tags": ["Secrétariat", "Organisation", "Pros"],
   "audience": "Professionnels",
   "points": [
     "Agenda saisi, rappelé et confirmé pour vous.",
     "Trois formules mensuelles selon votre volume de RDV.",
     "Les bénéfices d'un secrétariat, sans embaucher.",
   ],
   "impacts": [
     "Plus aucun rendez-vous oublié ni doublé.",
     "Une image professionnelle renforcée.",
     "Aucune charge fixe d'un poste à temps plein.",
   ],
   "keywords": ["Agenda", "Google Calendar", "Rappels", "Confirmations", "STARTER", "CONFORT", "PREMIUM"],
   "essentiel": [
     "Vos rendez-vous centralisés dans un agenda partagé.",
     "Rappel personnalisé 30 min avant chaque échéance.",
     "Confirmation téléphonique auprès de vos interlocuteurs.",
   ],
 },
}
for _a in BLOG:
    _a.update(BLOG_EXTRA[_a["slug"]])
    _a["url"] = f"blog-{_a['slug']}.html"

# ================================================================ STRUCTURE
def head(title, desc, path, page_class, og_type="website", page_type="WebPage", ld_extra=None):
    D = SITE["domain"]
    tel = SITE["tel1_href"]
    canonical = D + "/" + (path if path != "index.html" else "")
    page_node = {"@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title,
                 "description": desc, "isPartOf": {"@id": D + "/#website"}, "about": {"@id": D + "/#business"},
                 "inLanguage": "fr-CI"}
    if ld_extra:
        page_node.update(ld_extra)
    ldjson = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "LocalBusiness", "@id": D + "/#business", "name": SITE["legal"],
         "url": D + "/", "image": D + "/img/brand/og-mon-commis.jpg",
         "logo": D + "/img/brand/logo-mon-commis.png",
         "telephone": tel, "email": SITE["email"], "priceRange": "FCFA",
         "description": "Conciergerie & courses à Abidjan : courses au marché, pharmacie, démarches administratives, shopping, colis et secrétariat à distance.",
         "address": {"@type": "PostalAddress", "addressLocality": "Abidjan", "addressCountry": "CI"},
         "geo": {"@type": "GeoCoordinates", "latitude": SITE["geo"]["lat"], "longitude": SITE["geo"]["lng"]},
         "areaServed": "Abidjan", "currenciesAccepted": "XOF",
         "contactPoint": {"@type": "ContactPoint", "telephone": tel, "contactType": "customer service", "areaServed": "CI", "availableLanguage": ["fr"]}},
        {"@type": "WebSite", "@id": D + "/#website", "name": SITE["name"], "url": D + "/",
         "inLanguage": "fr-CI", "publisher": {"@id": D + "/#business"},
         "creator": {"@id": "https://tech-and-web.com/#agency"}},
        {"@type": ["Organization", "ProfessionalService"], "@id": "https://tech-and-web.com/#agency",
         "name": "Tech & Web", "url": "https://tech-and-web.com",
         "description": "Agence digitale : conception de sites web, d'applications métier et de solutions numériques sur mesure, avec optimisation pour le référencement (moteurs de recherche et assistants IA).",
         "knowsAbout": ["Conception de sites web", "Développement d'applications", "Référencement (SEO)", "Indexation par les assistants IA", "Solutions digitales sur mesure"]},
        page_node]},
        ensure_ascii=False)
    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="author" content="{SITE['legal']}">
<meta name="designer" content="Tech &amp; Web — tech-and-web.com">
<link rel="author" href="https://tech-and-web.com">
<meta name="format-detection" content="telephone=no">
<meta name="theme-color" content="#112844">
<link rel="canonical" href="{canonical}">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<meta property="og:site_name" content="{SITE['name']}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="fr_CI">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{D}/img/brand/og-mon-commis.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{D}/img/brand/og-mon-commis.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Hanken+Grotesk:wght@400;500;600;700;800&family=Caveat:wght@600;700&display=swap" rel="stylesheet">
<link href="css/commis-premium.css?v={ASSETV}" rel="stylesheet">
<link href="css/commis-brand.css?v={ASSETV}" rel="stylesheet">
<script>window.COMMIS_API_URL="/api/demandes/";</script>
<script type="application/ld+json">{ldjson}</script>
</head>
<body class="{page_class}">
"""

def brand():
    # Logo officiel (image temporaire fournie par le client).
    return (f'<a class="site-brand" href="index.html" aria-label="{SITE["legal"]} — accueil">'
            f'<img class="site-logo-img" src="img/brand/logo-mon-commis.jpg" alt="{SITE["legal"]} — conciergerie & courses, Abidjan" width="170" height="108"></a>')

def header(active=""):
    a = lambda k: " is-active" if active == k else ""
    serv_active = " is-active" if active in ("services", "service", "secretariat") else ""
    serv_items = "".join(
        f'<li role="none"><a class="nav-dropdown-link" href="{s["url"]}" role="menuitem">{s["title"]}</a></li>\n'
        for s in SERVICES)
    serv_items += '<li role="none"><a class="nav-dropdown-link" href="services.html" role="menuitem">Tous nos services &rarr;</a></li>'
    return f"""<a class="skip-link" href="#main">Aller au contenu</a>
<header class="site-header">
  <div class="container">
    <div class="header-inner">
      {brand()}
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="Ouvrir la navigation"><span></span><span></span><span></span></button>
      <nav class="site-nav" id="site-nav" aria-label="Navigation principale">
        <a class="nav-link{a('home')}" href="index.html">Accueil</a>
        <div class="nav-dropdown nav-dropdown-split">
          <div class="nav-dropdown-head">
            <a class="nav-link nav-link-parent{serv_active}" href="services.html">Services</a>
            <button class="nav-link nav-dropdown-toggle nav-dropdown-toggle-icon" type="button" aria-expanded="false" aria-controls="serv-menu" aria-haspopup="true" aria-label="Afficher les services">{ico('down')}</button>
          </div>
          <ul class="nav-dropdown-menu nav-dropdown-menu-list" id="serv-menu" role="menu">
{serv_items}
          </ul>
        </div>
        <a class="nav-link{a('about')}" href="a-propos.html">À propos</a>
        <a class="nav-link{a('blog')}" href="blog.html">Blog</a>
        <a class="nav-link{a('contact')}" href="contact.html">Contact</a>
        <a class="nav-cta" href="contact.html">{ico('send')} Demander un commis</a>
      </nav>
    </div>
  </div>
</header>
<main id="main">
"""

def footer():
    serv_links = "".join(f'<a href="{s["url"]}">{s["title"]}</a>\n' for s in SERVICES)
    return f"""</main>
<footer class="site-footer mc-footer">
  <div class="container">
    <div class="mc-footer-grid">
      <div class="mc-footer-brand">
        {brand()}
        <p class="mc-footer-desc">Conciergerie & courses à Abidjan — un commis de confiance pour vos courses, démarches, colis et rendez-vous.</p>
        <div class="footer-social">
          <a href="https://wa.me/{SITE['wa']}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">{SOCIAL['whatsapp']}</a>
          <a href="#" aria-label="TikTok">{SOCIAL['tiktok']}</a>
          <a href="#" aria-label="Instagram">{SOCIAL['instagram']}</a>
          <a href="#" aria-label="Facebook">{SOCIAL['facebook']}</a>
        </div>
      </div>
      <nav class="mc-footer-col" aria-label="Services">
        <h4>Services</h4>
        {serv_links}
      </nav>
      <nav class="mc-footer-col" aria-label="Mon Commis">
        <h4>Mon Commis</h4>
        <a href="a-propos.html">À propos</a>
        <a href="services.html">Tous les services</a>
        <a href="blog.html">Blog & conseils</a>
        <a href="services.html#zones">Zones de couverture</a>
        <a href="contact.html">Demander un commis</a>
      </nav>
      <div class="mc-footer-col mc-footer-contact">
        <h4>Contact</h4>
        <a class="mc-footer-phone" href="tel:{SITE['tel1_href']}">{ico('phone')} {SITE['tel1_disp']}</a>
        <a href="https://wa.me/{SITE['wa']}" target="_blank" rel="noopener noreferrer">{ico('message')} WhatsApp</a>
        <span>{ico('pin')} {SITE['addr']}</span>
      </div>
    </div>
    <div class="mc-footer-bottom">
      <span>&copy; {SITE['year']} {SITE['legal']} — Abidjan, Côte d'Ivoire. Tous droits réservés.</span>
      <a class="mc-credit" href="https://tech-and-web.com" target="_blank" rel="noopener" title="Tech &amp; Web — conception de sites web, applications et solutions digitales optimisés pour les moteurs de recherche et les assistants IA">Conception, développement &amp; référencement&nbsp;: <strong>Tech&nbsp;&amp;&nbsp;Web</strong></a>
    </div>
  </div>
</footer>
<a class="whatsapp-float" href="https://wa.me/{SITE['wa']}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">{SOCIAL['whatsapp']}</a>
<button class="scroll-top-btn" aria-label="Retour en haut" type="button"><svg viewBox="0 0 24 24"><polyline points="18 15 12 9 6 15"></polyline></svg></button>
<script src="js/commis-site.js?v={ASSETV}" defer></script>
</body></html>"""

# ---------------------------------------------------------------- Hero slider (design DKS)
def hero():
    slides = ""
    for i, s in enumerate(HERO_SLIDES):
        active = " is-active" if i == 0 else ""
        hidden = "false" if i == 0 else "true"
        tag = "h1" if s["is_h1"] else "p"
        title = f'<{tag} class="nx-hero-title">{s["title"]}</{tag}>'
        c1l, c1h = s["cta1"]; c2l, c2h = s["cta2"]
        ext = ' target="_blank" rel="noopener noreferrer"' if c2h.startswith("http") else ""
        kpis = ""
        styles = ["is-lime", "is-gold", "is-navy"]
        for j, (ic, strong, small) in enumerate(s["kpis"]):
            kpis += (f'<div class="nx-kpi"><span class="nx-ico {styles[j%3]}">{ico(ic)}</span>'
                     f'<div><strong>{strong}</strong><small>{small}</small></div></div>\n')
        slides += f"""      <article class="nx-hero-slide{active}" data-hero-slide aria-hidden="{hidden}">
        <div class="nx-hero-immersive">
          <img class="nx-hero-immersive-bg" src="{s['img']}" alt="" aria-hidden="true" {'fetchpriority="high"' if i==0 else 'loading="lazy"'} decoding="async" width="1920" height="1080">
          <div class="container nx-hero-inner">
            <div class="nx-hero-immersive-copy">
              <span class="nx-eyebrow">{s['eyebrow']}</span>
              {title}
              <p class="lead">{s['lead']}</p>
              <div class="nx-hero-cta">
                <a class="btn-lime" href="{c1h}">{c1l} {ico('arrow')}</a>
                <a class="btn-secondary" href="{c2h}"{ext}>{c2l}</a>
              </div>
            </div>
            <div class="nx-hero-kpis">
{kpis}            </div>
          </div>
        </div>
      </article>
"""
    dots = ""
    for i, s in enumerate(HERO_SLIDES):
        da = " is-active" if i == 0 else ""
        dots += f'<button type="button" class="nx-hero-dot{da}" data-hero-dot aria-label="Diapositive {i+1}"><i class="nx-hero-dot-fill" data-hero-progress aria-hidden="true"></i></button>\n'
    return f"""<section class="nx-hero nx-hero-slider" aria-roledescription="carrousel" aria-label="Mon Commis — présentation">
  <div class="nx-hero-track">
{slides}  </div>
  <div class="container">
    <div class="nx-hero-controls">
      <button type="button" class="nx-hero-arrow is-prev" data-hero-prev aria-label="Diapositive précédente">{ico('arrow')}</button>
      <div class="nx-hero-dots" role="tablist" aria-label="Choisir une diapositive">
{dots}      </div>
      <button type="button" class="nx-hero-arrow is-next" data-hero-next aria-label="Diapositive suivante">{ico('arrow')}</button>
    </div>
  </div>
</section>"""

# ---------------------------------------------------------------- Écosystème orbital
def hub():
    nodes = ""
    n = len(SERVICES)
    for i, s in enumerate(SERVICES):
        ang = math.radians(-90 + i * 360.0 / n)
        x = 50 + 38 * math.cos(ang)
        y = 50 + 38 * math.sin(ang)
        nodes += (f'<a class="nx-hub-node" style="left:{x:.2f}%;top:{y:.2f}%" href="{s["url"]}" aria-label="{s["title"]}">'
                  f'<span class="nx-hub-node-inner"><span class="nx-hub-ico">{ico(s["icon"])}</span>'
                  f'<span class="nx-hub-label">{s["short"]}</span></span></a>\n')
    return f"""<div class="nx-hub reveal">
  <span class="nx-hub-ring" aria-hidden="true"></span>
  <span class="nx-hub-orbit" aria-hidden="true"></span>
  <div class="nx-hub-rotor">{nodes}</div>
  <span class="nx-hub-core"><img src="img/brand/emblem-mon-commis.svg" alt="{SITE['legal']}"></span>
</div>"""

# ---------------------------------------------------------------- Section présentation (contenu hero descendu)
def section_intro():
    return f"""<section class="section">
  <div class="container">
    <div class="nx-split nx-why-inline">
      {hub()}
      <div class="reveal d1">
        <span class="nx-eyebrow">Présentation</span>
        <h2 class="section-title">Une conciergerie de proximité, <span class="nx-mark">au service d'Abidjan</span></h2>
        <p class="section-copy">Mon Commis est une structure ivoirienne de conciergerie et de courses. Nous prenons en charge vos achats, vos démarches administratives, vos colis et la gestion de vos rendez-vous, avec un seul objectif&nbsp;: vous restituer du temps et vous garantir un service fiable, ponctuel et confidentiel.</p>
        <p class="section-copy">Particuliers comme professionnels bénéficient d'un interlocuteur unique, d'un suivi rigoureux de chaque mission et d'une tarification claire en FCFA — dans toutes les communes d'Abidjan.</p>
        <ul class="nx-list" style="margin-top:18px">
          <li>{ico('check')}<span><strong>Interlocuteur unique</strong> — une seule équipe pour l'ensemble de vos besoins.</span></li>
          <li>{ico('check')}<span><strong>Couverture complète</strong> — toutes les communes d'Abidjan, et au-delà sur devis.</span></li>
          <li>{ico('check')}<span><strong>Sérieux & confidentialité</strong> — documents sensibles, ordonnances et colis traités avec soin.</span></li>
          <li>{ico('check')}<span><strong>Transparence</strong> — devis clair en FCFA, paiement espèces ou mobile money.</span></li>
        </ul>
        <div class="nx-hero-cta" style="margin-top:24px">
          <a class="btn-main" href="services.html">Découvrir nos services</a>
          <a class="btn-secondary" href="https://wa.me/{SITE['wa']}" target="_blank" rel="noopener noreferrer">{ico('message')} WhatsApp</a>
        </div>
      </div>
    </div>
  </div>
</section>"""

# ---------------------------------------------------------------- Services (cartes photo style DKS)
def services_photo_cards():
    cards = ""
    for i, s in enumerate(SERVICES):
        d = " d%d" % (i % 3) if i % 3 else ""
        cards += f"""<article class="nx-card-photo reveal{d}" id="{s['slug']}">
  <img class="nx-card-photo-bg" src="{s['img']}" alt="" aria-hidden="true" loading="lazy">
  <div class="nx-card-photo-body">
    <span class="nx-card-photo-ico">{ico(s['icon'])}</span>
    <h3>{s['title']}</h3>
    <p>{s['tagline']}</p>
    <span class="nx-card-photo-link">En savoir plus {ico('arrow')}</span>
  </div>
  <a class="nx-card-photo-cover" href="{s['url']}" aria-label="Découvrir : {s['title']}"></a>
</article>
"""
    return cards

def section_services(eyebrow="Nos services", titre="Tout ce qu'un commis peut faire pour vous",
                     intro="Six familles de services, un seul interlocuteur : déléguez vos tâches du quotidien à Mon Commis, partout dans Abidjan.",
                     soft=True):
    cls = "section section-soft" if soft else "section"
    return f"""<section class="{cls}" id="services">
  <div class="container">
    <div class="section-header reveal"><div class="section-heading">
      <span class="nx-eyebrow">{eyebrow}</span>
      <h2 class="section-title">{titre}</h2>
      <p class="section-copy">{intro}</p>
    </div></div>
    <div class="nx-grid cols-3 nx-cards-photo">{services_photo_cards()}</div>
  </div>
</section>"""

def compact_card(icon, title, badge, text, sub=None):
    """Carte compacte horizontale (icône + en-tête avec badge + descriptif), façon « Zones »."""
    badge_html = f'<span class="mc-compact-badge">{badge}</span>' if badge else ""
    sub_html = f'<p class="mc-compact-sub">{ico("pin")} <span>{sub}</span></p>' if sub else ""
    return f"""<article class="mc-compact-card reveal">
  <span class="mc-compact-ico">{ico(icon)}</span>
  <div class="mc-compact-body">
    <div class="mc-compact-head"><h3>{title}</h3>{badge_html}</div>
    <p class="mc-compact-text">{text}</p>
    {sub_html}
  </div>
</article>
"""

def section_steps():
    cards = "".join(compact_card(icn, t, f"Étape {i}", d) for i, (icn, t, d) in enumerate(STEPS, 1))
    return f"""<section class="section">
  <div class="container">
    <div class="section-header reveal"><div class="section-heading">
      <span class="nx-eyebrow">Comment ça marche&nbsp;?</span>
      <h2 class="section-title">Trois étapes, zéro stress</h2>
    </div></div>
    <div class="mc-compact-grid mc-swipe">{cards}</div>
  </div>
</section>"""

def section_args():
    cards = ""
    for n, (i, t, d) in enumerate(ARGS, 1):
        cards += (f'<article class="mc-why-card reveal">'
                  f'<span class="mc-why-num">0{n}</span>'
                  f'<span class="mc-why-ico">{ico(i)}</span>'
                  f'<h3>{t}</h3><p>{d}</p></article>\n')
    return f"""<section class="section section-soft">
  <div class="container">
    <div class="section-header reveal"><div class="section-heading">
      <span class="nx-eyebrow">Pourquoi nous&nbsp;?</span>
      <h2 class="section-title">Pourquoi Mon Commis&nbsp;?</h2>
      <p class="section-copy">Un partenaire de proximité, fiable et discret, qui prend en charge vos tâches du quotidien — pour que vous vous consacriez à l'essentiel.</p>
    </div></div>
    <div class="mc-why-grid mc-swipe">{cards}</div>
  </div>
</section>"""

def section_zones():
    rows = "".join(compact_card(icn, nom, frais, pro, sub=communes) for nom, communes, frais, icn, pro in ZONES)
    return f"""<section class="section" id="zones">
  <div class="container">
    <div class="section-header reveal"><div class="section-heading">
      <span class="nx-eyebrow">Zones de couverture</span>
      <h2 class="section-title">De Cocody à Grand-Bassam — et au-delà</h2>
      <p class="section-copy">Nous intervenons dans toutes les communes du Grand Abidjan. Les frais de déplacement sont déterminés selon la zone d'intervention.</p>
    </div></div>
    <div class="mc-compact-grid mc-swipe">{rows}</div>
  </div>
</section>"""

def formules_cards():
    cards = ""
    xmark = '<svg class="nx-svg" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>'
    for f in FORMULES:
        feats = ""
        for label, ok in f["feats"]:
            cls = "is-on" if ok else "is-off"
            feats += f'<li class="{cls}">{ico("check") if ok else xmark}<span>{label}</span></li>'
        featured = " is-featured" if f["featured"] else ""
        badge = '<span class="nx-price-badge">Le plus choisi</span>' if f["featured"] else ""
        cards += f"""<article class="nx-price-card reveal{featured}">
  {badge}
  <h3 class="nx-price-name">{f['nom']}</h3>
  <p class="nx-price-punch">{f['punch']}</p>
  <div class="nx-price-amount"><strong>{f['prix']}</strong><span>FCFA / mois</span></div>
  <p class="nx-price-rdv">{ico('calendar')} {f['rdv']}</p>
  <ul class="nx-price-feats">{feats}</ul>
  <a class="btn-lime nx-price-cta" href="contact.html?formule={f['slug']}">{ico('send')} Choisir {f['nom']}</a>
</article>
"""
    return cards

def section_formules(compact=False):
    inclus = "".join(f'<li class="nx-incl">{ico(icn)}<div><strong>{t}</strong><span>{d}</span></div></li>\n' for icn, t, d in SECRET_INCLUS)
    inclus_block = "" if compact else f"""<div class="nx-incl-wrap reveal">
      <h3 class="nx-incl-title">Inclus dans toutes les formules</h3>
      <ul class="nx-incl-grid">{inclus}</ul>
    </div>"""
    return f"""<section class="section section-soft" id="formules">
  <div class="container">
    <div class="section-header reveal"><div class="section-heading">
      <span class="nx-eyebrow">Pôle Secrétariat à Distance</span>
      <h2 class="section-title">Votre agenda, géré pour vous</h2>
      <p class="section-copy">Un secrétariat personnel par abonnement mensuel : vos rendez-vous saisis, rappelés et confirmés — vous ne ratez plus rien.</p>
    </div></div>
    <div class="nx-grid cols-3 nx-prices mc-swipe">{formules_cards()}</div>
    {inclus_block}
  </div>
</section>"""

def section_gallery():
    items = ""
    for img, cap, alt in GALLERY:
        items += (f'<figure class="mc-gal-item reveal"><img src="img/services/{img}" alt="{alt}" loading="lazy" decoding="async">'
                  f'<figcaption>{cap}</figcaption></figure>\n')
    return f"""<section class="section">
  <div class="container">
    <div class="section-header reveal"><div class="section-heading">
      <span class="nx-eyebrow">Mon Commis en images</span>
      <h2 class="section-title">Le service, sur le terrain</h2>
      <p class="section-copy">Du marché à votre porte : un aperçu de nos prestations au quotidien, partout dans Abidjan.</p>
    </div></div>
    <div class="mc-gallery">{items}</div>
  </div>
</section>"""

def section_testimonials():
    cards = ""
    for n, (txt, who, ville) in enumerate(TESTIMONIALS):
        ini = "".join(w[0] for w in who.split()[:2]).upper()
        d = f" d{n%3}" if n % 3 else ""
        cards += (f'<article class="mc-quote reveal{d}">'
                  f'<span class="mc-quote-mark" aria-hidden="true">&ldquo;</span>'
                  f'<p class="mc-quote-text">{txt}</p>'
                  f'<div class="mc-quote-by"><span class="mc-quote-avatar">{ini}</span>'
                  f'<span class="mc-quote-meta"><strong>{who}</strong><span>{ico("pin")} {ville}</span></span>'
                  f'<span class="mc-quote-stars">{ico("star")}{ico("star")}{ico("star")}{ico("star")}{ico("star")}</span></div>'
                  f'</article>\n')
    return f"""<section class="section section-soft mc-trust">
  <div class="container">
    <div class="section-header reveal"><div class="section-heading">
      <span class="nx-eyebrow">Ils nous font confiance</span>
      <h2 class="section-title">La satisfaction, notre meilleure référence</h2>
      <p class="section-copy">Des clients qui ont retrouvé du temps — et la tranquillité d'esprit.</p>
    </div></div>
    <div class="mc-quote-grid mc-swipe">{cards}</div>
  </div>
</section>"""

def contact_section(title="Demandez votre commis"):
    serv_opts = "".join(f'<option value="{s["title"]}">{s["title"]}</option>' for s in SERVICES)
    zone_opts = "".join(f'<option value="{z[0]}">{z[0]}</option>' for z in ZONES)
    wa_icon = SOCIAL["whatsapp"].replace("<svg ", '<svg class="nx-svg" ', 1)
    return f"""<section id="contact" class="section section-dark nx-contact">
  <div class="container">
    <div class="section-header reveal"><div class="section-heading">
      <span class="nx-eyebrow">Contact & demande</span>
      <h2 class="section-title">{title}</h2>
      <p class="section-copy">Décrivez votre besoin : nous vous recontactons rapidement avec un devis clair en FCFA. Envoyez votre demande directement, <strong>ou</strong> poursuivez sur WhatsApp — comme vous préférez.</p>
    </div></div>
    <div class="contact-layout">
      <div class="form-shell reveal">
        <form id="contact-brief" data-wa="{SITE['wa']}" novalidate>
          <div class="form-grid">
            <div class="form-group"><label class="form-label" for="full-name">Nom complet</label><input class="form-control" id="full-name" name="full_name" type="text" autocomplete="name" placeholder="Vos nom et prénom" data-field data-label="Nom"></div>
            <div class="form-group"><label class="form-label" for="phone-number">Téléphone / WhatsApp</label><input class="form-control" id="phone-number" name="phone_number" type="tel" autocomplete="tel" placeholder="07 …" data-field data-label="Téléphone"></div>
            <div class="form-group"><label class="form-label" for="service-type">Service souhaité</label><select class="form-control" id="service-type" name="project_type" data-field data-label="Service"><option value="">Choisir un service…</option>{serv_opts}</select></div>
            <div class="form-group"><label class="form-label" for="zone">Zone / commune</label><select class="form-control" id="zone" name="location" data-field data-label="Zone"><option value="">Choisir votre zone…</option>{zone_opts}</select></div>
            <div class="form-group"><label class="form-label" for="echeance">Quand ?</label><select class="form-control" id="echeance" name="timeline" data-field data-label="Échéance"><option value="">Choisir…</option><option>Dès que possible</option><option value="Urgent (dans l'heure, +50%)">Urgent — dans l'heure (+50 %)</option><option>Aujourd'hui</option><option>Cette semaine</option></select></div>
            <div class="form-group"><label class="form-label" for="email-address">Email (optionnel)</label><input class="form-control" id="email-address" name="email_address" type="email" autocomplete="email" placeholder="nom@domaine.com" data-field data-label="Email"></div>
            <div class="form-group full"><label class="form-label" for="project-message">Votre besoin en détail</label><textarea class="form-control" id="project-message" name="project_message" placeholder="Décrivez votre besoin : liste de courses, adresse de retrait/livraison, démarche précise, budget approximatif…" data-field data-label="Détails"></textarea></div>
          </div>
          <p class="form-note">{ico('shield')} Vos informations restent confidentielles et ne servent qu'à traiter votre demande.</p>
          <div class="nx-contact-actions">
            <button class="btn-lime" type="submit">{ico('send')} Envoyer ma demande</button>
            <button class="btn-wa" type="button" data-wa-contact data-wa="{SITE['wa']}">{wa_icon} …ou via WhatsApp</button>
          </div>
          <div class="form-success" hidden>{ico('check')} Merci ! Votre demande est bien reçue. Mon Commis vous recontacte rapidement.</div>
          <div class="form-error" hidden style="color:#ffd0d0;margin-top:12px;font-weight:600;"></div>
        </form>
      </div>
      <aside class="nx-contact-card reveal d1">
        <span class="nx-eyebrow">Joignez-nous</span>
        <h3>Un commis de confiance, <span class="nx-script">à portée de message</span></h3>
        <p>Le plus rapide : WhatsApp. Décrivez votre course, votre démarche ou votre colis, on s'occupe du reste.</p>
        <a class="nx-contact-wa" href="https://wa.me/{SITE['wa']}" target="_blank" rel="noopener noreferrer">
          <span class="nx-contact-wa-ico">{wa_icon}</span>
          <span class="nx-contact-wa-txt"><strong>Discuter sur WhatsApp</strong><small>{SITE['tel1_disp']} — appels & WhatsApp</small></span>
          <span class="nx-contact-wa-arr">{ico('arrow')}</span>
        </a>
        <div class="contact-points">
          <a class="contact-point" href="tel:{SITE['tel1_href']}">{ico('phone')}<div><strong>Téléphone</strong><span>{SITE['tel1_disp']}</span></div></a>
          <div class="contact-point">{ico('pin')}<div><strong>Zone d'action</strong><span>Toutes les communes d'Abidjan</span></div></div>
          <div class="contact-point">{ico('clock')}<div><strong>Réactivité</strong><span>Réponse rapide, 7j/7</span></div></div>
        </div>
        <div class="nx-contact-trust">
          <span>{ico('check')} Devis clair en FCFA</span>
          <span>{ico('shield')} Discrétion</span>
          <span>{ico('bolt')} Express possible</span>
        </div>
      </aside>
    </div>
  </div>
</section>"""

def _render_service_fields(slug):
    """Champs spécifiques au service, alimentés par SERVICE_FIELDS."""
    html = ""
    for name, label, ftype, extra in SERVICE_FIELDS.get(slug, []):
        fid = name.replace("_", "-")
        if ftype == "textarea":
            html += (f'<div class="form-group full"><label class="form-label" for="{fid}">{label}</label>'
                     f'<textarea class="form-control" id="{fid}" name="{name}" placeholder="{extra}" '
                     f'data-field data-label="{label}"></textarea></div>\n')
        elif ftype == "options":
            opts = "".join(f"<option>{o}</option>" for o in extra)
            html += (f'<div class="form-group"><label class="form-label" for="{fid}">{label}</label>'
                     f'<select class="form-control" id="{fid}" name="{name}" data-field data-label="{label}">'
                     f'<option value="">Choisir…</option>{opts}</select></div>\n')
        else:
            html += (f'<div class="form-group"><label class="form-label" for="{fid}">{label}</label>'
                     f'<input class="form-control" id="{fid}" name="{name}" type="text" placeholder="{extra}" '
                     f'data-field data-label="{label}"></div>\n')
    return html

def service_contact_section(s):
    """Formulaire dédié au service, adapté à la spécificité de la prestation."""
    zone_opts = "".join(f'<option value="{z[0]}">{z[0]}</option>' for z in ZONES)
    presta_opts = "".join(f'<option value="{t}">{t}</option>' for _, t, _ in s["sub"])
    presta_opts += '<option value="Plusieurs prestations / autre">Plusieurs prestations / autre</option>'
    extra_fields = _render_service_fields(s["slug"])
    wa_icon = SOCIAL["whatsapp"].replace("<svg ", '<svg class="nx-svg" ', 1)
    intro = (f"Commandez la prestation « {s['title']} » en quelques champs adaptés à votre besoin. "
             "Nous vous recontactons rapidement avec un devis clair en FCFA — ou poursuivez sur WhatsApp.")
    return f"""<section id="commander" class="section section-dark nx-contact mc-order">
  <div class="container">
    <div class="section-header reveal"><div class="section-heading">
      <span class="nx-eyebrow">Commander cette prestation</span>
      <h2 class="section-title">Commander : {s['title']}</h2>
      <p class="section-copy">{intro}</p>
    </div></div>
    <div class="contact-layout">
      <div class="form-shell reveal">
        <form id="contact-brief" data-wa="{SITE['wa']}" novalidate>
          <select hidden name="project_type" data-field data-label="Service"><option value="{s['title']}" selected>{s['title']}</option></select>
          <div class="form-grid">
            <div class="form-group full"><label class="form-label" for="prestation-select">Prestation souhaitée</label><select class="form-control" id="prestation-select" name="prestation" data-field data-label="Prestation"><option value="">Choisir la prestation…</option>{presta_opts}</select></div>
            {extra_fields}            <div class="form-group"><label class="form-label" for="full-name">Nom complet</label><input class="form-control" id="full-name" name="full_name" type="text" autocomplete="name" placeholder="Vos nom et prénom" data-field data-label="Nom"></div>
            <div class="form-group"><label class="form-label" for="phone-number">Téléphone / WhatsApp</label><input class="form-control" id="phone-number" name="phone_number" type="tel" autocomplete="tel" placeholder="07 …" data-field data-label="Téléphone"></div>
            <div class="form-group"><label class="form-label" for="zone">Zone / commune</label><select class="form-control" id="zone" name="location" data-field data-label="Zone"><option value="">Choisir votre zone…</option>{zone_opts}</select></div>
            <div class="form-group"><label class="form-label" for="echeance">Quand ?</label><select class="form-control" id="echeance" name="timeline" data-field data-label="Échéance"><option value="">Choisir…</option><option>Dès que possible</option><option value="Urgent (dans l'heure, +50%)">Urgent — dans l'heure (+50 %)</option><option>Aujourd'hui</option><option>Cette semaine</option></select></div>
            <div class="form-group full"><label class="form-label" for="email-address">Email (optionnel)</label><input class="form-control" id="email-address" name="email_address" type="email" autocomplete="email" placeholder="nom@domaine.com" data-field data-label="Email"></div>
            <div class="form-group full"><label class="form-label" for="project-message">Précisions complémentaires</label><textarea class="form-control" id="project-message" name="project_message" placeholder="Toute information utile : budget, contraintes, créneau préféré…" data-field data-label="Précisions"></textarea></div>
          </div>
          <p class="form-note">{ico('shield')} Vos informations restent confidentielles et ne servent qu'à traiter votre demande.</p>
          <div class="nx-contact-actions">
            <button class="btn-lime" type="submit">{ico('send')} Envoyer ma commande</button>
            <button class="btn-wa" type="button" data-wa-contact data-wa="{SITE['wa']}">{wa_icon} …ou via WhatsApp</button>
          </div>
          <div class="form-success" hidden>{ico('check')} Merci ! Votre commande est bien reçue. Mon Commis vous recontacte rapidement.</div>
          <div class="form-error" hidden style="color:#ffd0d0;margin-top:12px;font-weight:600;"></div>
        </form>
      </div>
      <aside class="nx-contact-card reveal d1">
        <span class="nx-eyebrow">Service {s['title']}</span>
        <h3>Une prestation, <span class="nx-script">un interlocuteur dédié</span></h3>
        <p>{s['tagline']}</p>
        <a class="nx-contact-wa" href="https://wa.me/{SITE['wa']}" target="_blank" rel="noopener noreferrer">
          <span class="nx-contact-wa-ico">{wa_icon}</span>
          <span class="nx-contact-wa-txt"><strong>Discuter sur WhatsApp</strong><small>{SITE['tel1_disp']} — appels & WhatsApp</small></span>
          <span class="nx-contact-wa-arr">{ico('arrow')}</span>
        </a>
        <ul class="nx-list" style="margin-top:18px">
          {"".join(f'<li>{ico("check")}<span>{x}</span></li>' for x in s["inclus"])}
        </ul>
        <div class="nx-contact-trust">
          <span>{ico('check')} Devis clair en FCFA</span>
          <span>{ico('shield')} Discrétion</span>
          <span>{ico('bolt')} Express possible</span>
        </div>
      </aside>
    </div>
  </div>
</section>"""

def cta(title="Besoin d'un coup de main aujourd'hui ?",
        text="Confiez votre course, votre démarche ou votre colis à Mon Commis. Devis clair en FCFA, réponse rapide."):
    return f"""<section class="section">
  <div class="container">
    <div class="nx-cta reveal">
      <span class="nx-eyebrow">Passons à l'action</span>
      <h2>{title}</h2>
      <p>{text}</p>
      <div class="nx-cta-row">
        <a class="btn-lime" href="contact.html">{ico('send')} Demander un commis</a>
        <a class="btn-secondary" href="https://wa.me/{SITE['wa']}" target="_blank" rel="noopener noreferrer">{ico('message')} WhatsApp</a>
      </div>
    </div>
  </div>
</section>"""

def section_tarifs():
    # (titre, badge, descriptif, icône)
    rows = [
        ("Tarif de base", "Sur grille", "Commission selon la grille tarifaire communiquée au client avant la mission.", "wallet"),
        ("Supplément urgence", "+50 %", "Appliqué sur le tarif de base pour une intervention dans l'heure.", "bolt"),
        ("Shopping", "5 000–15 000 FCFA", "Tarif de la prestation selon la complexité et le volume des achats.", "gift"),
        ("Collecte de documents", "En sus", "Prestation complémentaire, facturée séparément du tarif de base.", "doc"),
    ]
    cards = "".join(compact_card(i, t, b, d) for t, b, d, i in rows)
    return f"""<section class="section section-soft" id="tarifs">
  <div class="container">
    <div class="section-header reveal"><div class="section-heading">
      <span class="nx-eyebrow">Tarifs & paiement</span>
      <h2 class="section-title">Des tarifs clairs, sans surprise</h2>
      <p class="section-copy">Les frais de commission sont réglés avant le début de chaque mission. Paiement en espèces, mobile money (Orange, MTN, Moov, Wave) ou virement.</p>
    </div></div>
    <div class="mc-compact-grid mc-swipe">{cards}</div>
  </div>
</section>"""

# ---------------------------------------------------------------- Hero de page intérieure
def page_hero(eyebrow, title, lead):
    return f"""<section class="nx-pagehead">
  <div class="container">
    <div class="reveal">
      <span class="nx-eyebrow nx-eyebrow-light">{eyebrow}</span>
      <h1 class="nx-pagehead-title">{title}</h1>
      <p class="lead">{lead}</p>
    </div>
  </div>
</section>"""

def service_hero(s):
    return f"""<section class="mc-service-hero">
  <img class="mc-service-hero-bg" src="{s['img']}" alt="" aria-hidden="true" fetchpriority="high" decoding="async">
  <div class="container">
    <div class="mc-service-hero-copy reveal">
      <span class="nx-eyebrow nx-eyebrow-light">Service Mon Commis</span>
      <h1 class="mc-service-hero-title">{s['title']}</h1>
      <p class="lead">{s['tagline']}</p>
      <div class="nx-hero-cta">
        <a class="btn-lime" href="#commander">{ico('send')} Commander ce service</a>
        <a class="btn-secondary btn-on-dark" href="https://wa.me/{SITE['wa']}" target="_blank" rel="noopener noreferrer">{ico('message')} WhatsApp</a>
      </div>
    </div>
  </div>
</section>"""

# =================================================================== PAGES
def build_index():
    body = (hero()
            + section_args()
            + section_intro()
            + section_services()
            + section_steps()
            + section_gallery()
            + section_formules(compact=True)
            + section_zones()
            + section_testimonials()
            + section_blog_home()
            + contact_section())
    return (head("Mon Commis — Conciergerie & courses à Abidjan",
                 "Mon Commis, votre commis de confiance à Abidjan : courses au marché, pharmacie, démarches administratives, shopping, colis et secrétariat à distance. Devis en FCFA.",
                 "index.html", "page-home")
            + header("home") + body + footer())

def build_services():
    body = (page_hero("Nos services", "Tout ce qu'un commis peut faire pour vous",
                      "Six familles de services, un seul interlocuteur de confiance. Cliquez sur un service pour en découvrir le détail — et déléguez ce qui vous fait perdre du temps.")
            + section_services(soft=False)
            + section_gallery()
            + section_tarifs()
            + section_zones()
            + section_steps()
            + cta())
    return (head("Services — Courses, démarches, shopping, colis & secrétariat | Mon Commis",
                 "Les services Mon Commis à Abidjan : courses, démarches administratives, shopping & cadeaux, dépôt-retrait de colis, secrétariat à distance et tâches sur-mesure.",
                 "services.html", "page-inner", page_type="CollectionPage")
            + header("services") + body + footer())

def section_service_detail(s):
    cards = "".join(
        f'<article class="nx-card mc-presta-card reveal">'
        f'<span class="nx-ico is-lime">{ico(ic)}</span>'
        f'<h3>{t}</h3><p>{d}</p>'
        f'<a class="mc-presta-order" href="#commander" data-order-prestation="{t}">'
        f'{ico("send")} Commander ce service</a>'
        f'</article>\n'
        for ic, t, d in s["sub"])
    incl = "".join(f'<li>{ico("check")}<span>{x}</span></li>' for x in s["inclus"])
    return f"""<section class="section" id="prestations">
  <div class="container">
    <div class="section-header reveal"><div class="section-heading">
      <span class="nx-eyebrow">Nos prestations</span>
      <h2 class="section-title">{s['title']} : ce que nous faisons pour vous</h2>
      <p class="section-copy">{s['lead']}</p>
    </div></div>
    <div class="nx-grid cols-3">{cards}</div>
    <div class="mc-incl-band reveal"><span class="mc-incl-band-label">{ico('check')} Toujours inclus</span><ul>{incl}</ul></div>
  </div>
</section>"""

def service_gallery(s):
    if not s.get("gallery"):
        return ""
    items = "".join(f'<figure class="mc-gal-item reveal"><img src="img/services/{g}" alt="{s["title"]} — Mon Commis Abidjan" loading="lazy" decoding="async"></figure>\n' for g in s["gallery"])
    return f"""<section class="section section-soft">
  <div class="container">
    <div class="section-header reveal"><div class="section-heading">
      <span class="nx-eyebrow">En images</span>
      <h2 class="section-title">{s['title']} en pratique</h2>
    </div></div>
    <div class="mc-gallery">{items}</div>
  </div>
</section>"""

def build_service_page(s):
    """Page de service = mini-page d'accueil du service (landing orientée conversion)."""
    if s.get("is_secretariat"):
        offer = section_formules(compact=False)
        title = "Secrétariat à distance — STARTER, CONFORT, PREMIUM | Mon Commis"
        desc = ("Le secrétariat à distance Mon Commis à Abidjan : formules STARTER (15 000), "
                "CONFORT (25 000) et PREMIUM (50 000 FCFA/mois). Agenda partagé, rappels, confirmations.")
    else:
        offer = section_tarifs() + section_zones()
        title = f"{s['title']} à Abidjan | Mon Commis"
        desc = f"{s['title']} avec Mon Commis à Abidjan : {s['tagline']} Devis clair en FCFA, toutes les communes."
    body = (service_hero(s)
            + section_service_detail(s)
            + service_gallery(s)
            + section_steps()
            + offer
            + section_testimonials()
            + service_contact_section(s))
    active = "secretariat" if s.get("is_secretariat") else "service"
    return (head(title, desc, s["url"], "page-inner", og_type="article", page_type="Service")
            + header(active) + body + footer())

def build_about():
    vals = "".join(f'<article class="nx-card reveal"><span class="nx-ico is-lime">{ico(i)}</span><h3>{t}</h3><p>{d}</p></article>\n' for i, t, d in ARGS)
    body = (page_hero("À propos", "Mon Commis, le temps retrouvé",
                      "Une jeune structure ivoirienne née d'une idée simple : vous libérer des courses et démarches qui grignotent vos journées.")
            + f"""<section class="section">
  <div class="container">
    <div class="nx-split">
      <div class="reveal">
        <span class="nx-eyebrow">Notre mission</span>
        <h2 class="section-title">Vous faire gagner un temps précieux</h2>
        <p class="section-copy">À Abidjan, le temps est précieux et les files d'attente interminables. Mon Commis met à votre disposition des commis fiables et professionnels pour vos courses au marché, vos passages en pharmacie, vos démarches administratives, vos colis et la gestion de vos rendez-vous.</p>
        <p class="section-copy">Notre promesse : un service de proximité, sérieux et discret, au cœur d'Abidjan et au-delà — pour les particuliers comme pour les professionnels.</p>
        <div class="nx-hero-cta" style="margin-top:24px"><a class="btn-main" href="contact.html">{ico('send')} Demander un commis</a></div>
      </div>
      <div class="reveal d1"><div class="nx-grid cols-1">
        <article class="nx-card"><span class="nx-ico is-navy">{ico('map')}</span><h3>Au cœur d'Abidjan</h3><p>Toutes les communes couvertes, de Cocody à Yopougon jusqu'à Grand-Bassam.</p></article>
        <article class="nx-card"><span class="nx-ico is-navy">{ico('users')}</span><h3>Particuliers & pros</h3><p>Un service sur-mesure, adapté à chaque besoin et à chaque budget.</p></article>
      </div></div>
    </div>
  </div>
</section>"""
            + f"""<section class="section section-soft"><div class="container">
    <div class="section-header reveal"><div class="section-heading">
      <span class="nx-eyebrow">Nos engagements</span>
      <h2 class="section-title">Ce qui fait la différence</h2>
    </div></div>
    <div class="nx-grid cols-4 mc-swipe">{vals}</div>
  </div></section>"""
            + cta())
    return (head("À propos — Mon Commis, conciergerie à Abidjan",
                 "Mon Commis est une structure ivoirienne de conciergerie et de courses à Abidjan. Notre mission : vous faire gagner un temps précieux, avec sérieux et discrétion.",
                 "a-propos.html", "page-inner", page_type="AboutPage")
            + header("about") + body + footer())

def build_contact():
    body = (page_hero("Contact", "Demandez votre commis",
                      "Un besoin, une question ? Envoyez votre demande — par formulaire ou WhatsApp — et nous revenons vers vous rapidement.")
            + contact_section(title="Parlons de votre besoin"))
    return (head("Contact — Demander un commis à Abidjan | Mon Commis",
                 "Contactez Mon Commis à Abidjan : formulaire de demande ou WhatsApp 07 47 79 10 73. Courses, démarches, colis, secrétariat à distance. Devis clair en FCFA.",
                 "contact.html", "page-inner", og_type="website", page_type="ContactPage")
            + header("contact") + body + footer())

def build_404():
    body = f"""<section class="nx-pagehead"><div class="container"><div class="reveal" style="text-align:center">
      <span class="nx-eyebrow nx-eyebrow-light">Erreur 404</span>
      <h1 class="nx-pagehead-title">Cette page s'est égarée en chemin</h1>
      <p class="lead" style="margin-inline:auto">Mais votre commis, lui, ne se perd jamais. Revenez à l'accueil ou écrivez-nous.</p>
      <div class="nx-hero-cta" style="justify-content:center;margin-top:26px">
        <a class="btn-lime" href="index.html">{ico('arrow')} Retour à l'accueil</a>
        <a class="btn-secondary" href="https://wa.me/{SITE['wa']}" target="_blank" rel="noopener noreferrer">{ico('message')} WhatsApp</a>
      </div>
    </div></div></section>"""
    return (head("Page introuvable (404) | Mon Commis", "La page demandée est introuvable.",
                 "404.html", "page-inner") + header("") + body + footer())

# ---------------------------------------------------------------- BLOG
def blog_card(a, featured=False):
    cls = "nx-blog-card reveal" + (" is-featured" if featured else "")
    return f"""<article class="{cls}" data-cat="{a['cat']}">
  <a class="nx-blog-card-media" href="{a['url']}" aria-label="{a['title']}">
    <img src="{a['img']}" alt="{a['title']}" loading="lazy" decoding="async">
    <span class="nx-blog-tag">{ico(a['icon'])} {a['cat']}</span>
  </a>
  <div class="nx-blog-card-body">
    <div class="nx-blog-meta"><time datetime="{a['date']}">{a['date_disp']}</time><span>{a['read']}</span></div>
    <h3 class="nx-blog-card-title"><a href="{a['url']}">{a['title']}</a></h3>
    <p class="nx-blog-card-excerpt">{a['excerpt']}</p>
    <a class="nx-blog-card-link" href="{a['url']}">Lire l'article {ico('arrow')}</a>
  </div>
</article>
"""

def section_blog_home():
    cards = "".join(blog_card(a) for a in BLOG)
    return f"""<section class="section section-soft" id="blog">
  <div class="container">
    <div class="section-header reveal"><div class="section-heading">
      <span class="nx-eyebrow">Blog & conseils</span>
      <h2 class="section-title">Gagner du temps, mode d'emploi</h2>
      <p class="section-copy">Nos conseils pratiques pour déléguer vos courses, vos démarches et la gestion de votre agenda à Abidjan.</p>
    </div></div>
    <div class="nx-blog-grid">{cards}</div>
    <div class="nx-blog-more reveal"><a class="btn-main" href="blog.html">Tous les articles {ico('arrow')}</a></div>
  </div>
</section>"""

def build_blog():
    cats = []
    for a in BLOG:
        if a["cat"] not in cats:
            cats.append(a["cat"])
    chips = '<button type="button" class="nx-blog-chip is-active" data-filter="all">Tous</button>'
    chips += "".join(f'<button type="button" class="nx-blog-chip" data-filter="{c}">{c}</button>' for c in cats)
    cards = "".join(blog_card(a) for a in BLOG)
    body = (page_hero("Blog & conseils", "Gagner du temps, mode d'emploi",
                      "Conseils pratiques et retours d'expérience pour déléguer vos courses, vos démarches administratives, vos colis et la gestion de votre agenda — partout à Abidjan.")
            + f"""<section class="section">
  <div class="container">
    <div class="nx-blog-filter reveal">{chips}</div>
    <div class="nx-blog-grid" data-blog-grid>{cards}</div>
    <p class="nx-blog-empty" hidden>Aucun article dans cette catégorie pour le moment.</p>
  </div>
</section>"""
            + cta())
    return (head("Blog & conseils — Conciergerie, courses & démarches à Abidjan | Mon Commis",
                 "Le blog de Mon Commis : conseils pratiques pour déléguer vos courses, vos démarches administratives et la gestion de votre agenda à Abidjan. Gagnez du temps.",
                 "blog.html", "page-inner", page_type="CollectionPage")
            + header("blog") + body + footer())

def _render_article_body(a):
    """Groupe le corps en blocs .article-section (un par h2) + collecte le sommaire."""
    toc = []
    sections = []   # [hid, titre, html_interne]
    cur = None
    n = 0
    for kind, content in a["body"]:
        if kind == "h2":
            if cur:
                sections.append(cur)
            n += 1
            hid = f"sec-{n}"
            toc.append((hid, content))
            cur = [hid, content, ""]
        else:
            if cur is None:
                cur = ["sec-0", "", ""]
            if kind == "p":
                cur[2] += f"<p>{content}</p>\n"
            elif kind == "ul":
                cur[2] += "<ul>" + "".join(f"<li>{x}</li>" for x in content) + "</ul>\n"
            elif kind == "quote":
                cur[2] += f'<div class="article-highlight"><p>{content}</p></div>\n'
    if cur:
        sections.append(cur)
    html = ""
    for hid, title, inner in sections:
        head_h2 = f'<h2>{title}</h2>\n' if title else ""
        html += f'<div class="article-section" id="{hid}">{head_h2}{inner}</div>\n'
    return html, toc

def build_article(a):
    D = SITE["domain"]
    url = D + "/" + a["url"]
    svc = SERVICES_BY_SLUG.get(a.get("service"))
    related = [b for b in BLOG if b["slug"] != a["slug"]]
    sections_html, toc = _render_article_body(a)
    wa_svg = SOCIAL['whatsapp'].replace('<svg ', '<svg class="nx-svg" ', 1)
    fb_svg = SOCIAL['facebook'].replace('<svg ', '<svg class="nx-svg" ', 1)

    tags_html = "".join(f"<span>{t}</span>" for t in a["tags"])
    points_li = "".join(f"<li>{x}</li>" for x in a["points"])
    impacts_li = "".join(f"<li>{x}</li>" for x in a["impacts"])
    kw_li = "".join(f"<li>{k}</li>" for k in a["keywords"])
    essentiel_li = "".join(f"<li>{x}</li>" for x in a["essentiel"])
    toc_li = "".join(f'<li><a href="#{hid}">{txt}</a></li>' for hid, txt in toc)

    if svc:
        primary_href, primary_label = f'{svc["url"]}#commander', "Commander cette prestation"
    else:
        primary_href, primary_label = "contact.html", "Demander un commis"

    wa_share = "https://wa.me/?text=" + quote(f"{a['title']} — {url}")
    fb_share = "https://www.facebook.com/sharer/sharer.php?u=" + quote(url)

    svc_card = ""
    if svc:
        svc_card = f"""<div class="article-card article-card-highlight">
        <h3>Service associé</h3>
        <p><strong>{svc['title']}</strong> — {svc['tagline']}</p>
        <a class="article-card-cta" href="{svc['url']}#commander">Voir le service {ico('arrow')}</a>
      </div>"""

    rel_html = ""
    for b in related:
        rel_html += (f'<a href="{b["url"]}" class="related-article">'
                     f'<span>{b["cat"]}</span><strong>{b["title"]}</strong>'
                     f'<p>{b["excerpt"]}</p></a>')

    ld_extra = {
        "@type": "BlogPosting", "headline": a["title"], "description": a["excerpt"],
        "image": D + "/" + a["img"], "datePublished": a["date"], "dateModified": a["date"],
        "author": {"@type": "Organization", "name": SITE["legal"], "url": D + "/"},
        "publisher": {"@id": D + "/#business"},
        "mainEntityOfPage": url + "#webpage", "inLanguage": "fr-CI", "articleSection": a["cat"],
        "wordCount": sum(len(c.split()) for k, c in a["body"] if k in ("p", "quote")),
    }
    body = f"""<section class="article-hero">
  <div class="container article-hero-grid">
    <div class="article-hero-content">
      <div class="article-hero-panel reveal">
        <nav class="article-breadcrumb" aria-label="Fil d'Ariane">
          <a href="index.html">Accueil</a><span>/</span><a href="blog.html">Blog</a><span>/</span><span>{a['cat']}</span>
        </nav>
        <span class="article-hero-badge">Article de blog · Mon Commis</span>
        <div class="article-tags">{tags_html}</div>
        <h1>{a['title']}</h1>
        <p>{a['excerpt']}</p>
        <div class="article-meta">
          <span>{a['date_disp']}</span>
          <span>Par l'équipe Mon Commis</span>
        </div>
        <div class="article-meta article-meta-kpi" aria-label="Contexte de lecture">
          <span>{ico('clock')} {a['read']}</span>
          <span>{ico('users')} {a['audience']}</span>
          <span>{ico('calendar')} Mis à jour {a['date_disp']}</span>
        </div>
        <div class="article-hero-actions">
          <a class="btn-lime" href="{primary_href}">{ico('send')} {primary_label}</a>
          <a class="btn-secondary" href="blog.html">{ico('arrow')} Retour au blog</a>
        </div>
      </div>
    </div>
    <div class="article-hero-summary">
      <div class="summary-card summary-key reveal">
        <h3>Points clés</h3>
        <ul class="summary-list">{points_li}</ul>
      </div>
      <div class="summary-card summary-impact reveal">
        <h3>Bénéfices pour vous</h3>
        <ul class="summary-list">{impacts_li}</ul>
      </div>
      <div class="summary-card summary-keywords reveal">
        <h3>Mots clés</h3>
        <ul class="summary-list">{kw_li}</ul>
      </div>
    </div>
  </div>
</section>
<section class="article-body">
  <div class="container article-body-grid">
    <article class="article-content">
      <figure class="article-cover"><img src="{a['img']}" alt="{a['title']}" fetchpriority="high" decoding="async"></figure>
      <div class="article-intro">
        <h2>L'essentiel</h2>
        <p>{a['lead']}</p>
        <ul class="article-quick-list">{essentiel_li}</ul>
      </div>
      {sections_html}
      <div class="article-section article-final-note" id="conclusion">
        <h2>Passez à l'action</h2>
        <p>Confiez cette tâche à Mon Commis : devis clair en FCFA, réponse rapide, dans toutes les communes d'Abidjan.</p>
        <div class="article-final-actions">
          <a class="btn-lime" href="{primary_href}">{ico('send')} {primary_label}</a>
          <a class="btn-secondary" href="https://wa.me/{SITE['wa']}" target="_blank" rel="noopener noreferrer">{ico('message')} WhatsApp</a>
        </div>
      </div>
      <div class="article-share">
        <span class="article-share-label">Partager cet article</span>
        <div class="article-share-row">
          <a class="art-share-btn is-wa" href="{wa_share}" target="_blank" rel="noopener noreferrer" aria-label="Partager sur WhatsApp">{wa_svg}</a>
          <a class="art-share-btn is-fb" href="{fb_share}" target="_blank" rel="noopener noreferrer" aria-label="Partager sur Facebook">{fb_svg}</a>
          <button type="button" class="art-share-btn is-copy" data-copy="{url}" aria-label="Copier le lien">{ico('list')}</button>
        </div>
      </div>
    </article>
    <aside class="article-aside">
      <div class="article-card article-card-toc">
        <h3 class="toc-title">Sommaire</h3>
        <ul class="article-toc">{toc_li}</ul>
      </div>
      {svc_card}
      <div class="article-card article-related">
        <h3>À lire aussi</h3>
        <div class="related-articles">{rel_html}</div>
      </div>
      <div class="article-card article-card-contact">
        <h3>Une demande à confier ?</h3>
        <p>Décrivez votre besoin : réponse rapide et devis clair en FCFA, dans tout Abidjan.</p>
        <a class="btn-lime" href="contact.html">{ico('send')} Demander un commis</a>
        <a class="article-card-cta" href="https://wa.me/{SITE['wa']}" target="_blank" rel="noopener noreferrer">{ico('message')} Discuter sur WhatsApp</a>
      </div>
    </aside>
  </div>
</section>"""
    return (head(f"{a['title']} | Blog Mon Commis", a["excerpt"], a["url"], "page-inner page-article",
                 og_type="article", page_type="BlogPosting", ld_extra=ld_extra)
            + header("blog") + body + footer())

# ---------------------------------------------------------------- SEO
def build_robots():
    bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-Web",
            "PerplexityBot", "Google-Extended", "Applebot-Extended", "Bingbot"]
    lines = ["User-agent: *", "Allow: /", ""]
    for b in bots:
        lines += [f"User-agent: {b}", "Allow: /", ""]
    lines += [f"Sitemap: {SITE['domain']}/sitemap.xml", ""]
    return "\n".join(lines)

def build_sitemap():
    pages = [("index.html", "1.0", "weekly"), ("services.html", "0.9", "monthly"),
             ("a-propos.html", "0.7", "monthly"), ("blog.html", "0.7", "weekly"),
             ("contact.html", "0.8", "monthly")]
    pages += [(s["url"], "0.8", "monthly") for s in SERVICES]   # inclut secretariat.html
    pages += [(a["url"], "0.6", "monthly") for a in BLOG]
    items = ""
    for p, prio, freq in pages:
        loc = SITE["domain"] + "/" + (p if p != "index.html" else "")
        items += f"  <url><loc>{loc}</loc><changefreq>{freq}</changefreq><priority>{prio}</priority></url>\n"
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}</urlset>\n'

def build_llms():
    D = SITE["domain"]
    serv = "\n".join(f"- [{s['title']}]({D}/{s['url']}) : {s['tagline']}" for s in SERVICES)
    blog = "\n".join(f"- [{a['title']}]({D}/{a['url']}) : {a['excerpt']}" for a in BLOG)
    return f"""# {SITE['legal']}

> Conciergerie & courses à Abidjan (Côte d'Ivoire). Mon Commis met à disposition des commis de confiance pour vos courses, démarches administratives, colis et la gestion de vos rendez-vous. Tarifs en FCFA, toutes les communes d'Abidjan.

## Services
{serv}

## Secrétariat à Distance (abonnements mensuels)
- STARTER — 15 000 FCFA/mois, jusqu'à 8 RDV/mois.
- CONFORT — 25 000 FCFA/mois, jusqu'à 20 RDV/mois.
- PREMIUM — 50 000 FCFA/mois, RDV illimités.

## Zones de couverture
- Zone Standard : Cocody, Plateau, Marcory, Treichville, Adjamé, Attécoubé (frais inclus).
- Zone Étendue : Yopougon, Abobo, Bingerville, Anyama, Songon, Dabou, Grand-Bassam (+1 000 à 2 000 FCFA).
- Zone Spéciale : hors périmètre, sur devis.

## Blog & conseils
{blog}

## Pages clés
- [Accueil]({D}/)
- [Services]({D}/services.html)
- [Secrétariat à distance]({D}/secretariat.html)
- [Blog & conseils]({D}/blog.html)
- [À propos]({D}/a-propos.html)
- [Contact]({D}/contact.html)

## Contact
- WhatsApp & appels : {SITE['tel1_disp']}
- Zone : Abidjan, Côte d'Ivoire
"""

def build_manifest():
    return json.dumps({
        "name": SITE["legal"], "short_name": "Mon Commis",
        "description": "Conciergerie & courses à Abidjan.",
        "start_url": "/", "display": "standalone",
        "background_color": "#ffffff", "theme_color": "#112844",
        "icons": [
            {"src": "img/brand/icon-512.png", "sizes": "512x512", "type": "image/png"},
            {"src": "apple-touch-icon.png", "sizes": "180x180", "type": "image/png"},
        ],
    }, ensure_ascii=False, indent=2)

# =================================================================== BUILD
def write(path, content):
    full = os.path.join(ROOT, path)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("  ✓", path)

def main():
    print("Génération du site Mon Commis…")
    write("index.html", build_index())
    write("services.html", build_services())
    for s in SERVICES:
        write(s["url"], build_service_page(s))   # secretariat.html + service-*.html
    write("a-propos.html", build_about())
    write("blog.html", build_blog())
    for a in BLOG:
        write(a["url"], build_article(a))
    write("contact.html", build_contact())
    write("404.html", build_404())
    write("robots.txt", build_robots())
    write("sitemap.xml", build_sitemap())
    write("llms.txt", build_llms())
    write("site.webmanifest", build_manifest())
    print("Terminé.")

if __name__ == "__main__":
    main()
