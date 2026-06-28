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
ASSETV = "20260628b1"  # cache-busting — incrémenter à chaque modif CSS/JS

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
  "tagline": "Marché, pharmacie, quotidien : vos courses faites et livrées.",
  "lead": "Du marché à la pharmacie, Mon Commis se charge de toutes vos courses du quotidien. "
          "Vous transmettez votre liste, nous sélectionnons avec soin et nous livrons chez vous — "
          "dans toutes les communes d'Abidjan.",
  "sub": [
    ("cart", "Courses au marché", "Achats alimentaires, condiments, légumes et produits frais, choisis avec exigence et selon votre budget."),
    ("pill", "Pharmacie & ordonnances", "Retrait de vos médicaments et exécution de vos ordonnances, en toute discrétion — pharmacie de garde au besoin."),
    ("doc", "Courses du quotidien", "Supérette, boulangerie, petites emplettes récurrentes : confiez-nous vos achats réguliers et gagnez du temps."),
  ],
  "inclus": ["Sélection soignée selon votre budget", "Livraison dans votre commune", "Confidentialité pour vos achats sensibles"],
  "gallery": ["courses.jpg", "pharmacie.jpg", "marche-2.jpg"],
 },
 {
  "slug": "demarches", "title": "Démarches administratives", "short": "Démarches", "icon": "stamp",
  "img": "img/services/demarches.jpg",
  "tagline": "Vos dossiers déposés, suivis et retirés — sans la file d'attente.",
  "lead": "Mairie, CNPS, impôts, préfecture, tribunal, notaire, hôpitaux : nous prenons en charge "
          "le dépôt, le suivi et le retrait de vos dossiers et documents officiels. Vous gardez le contrôle, "
          "nous gérons l'attente et les déplacements.",
  "sub": [
    ("stamp", "Dépôt & retrait de dossiers", "Mairie, CNPS, impôts, préfecture, tribunal, notaire, hôpitaux : vos démarches menées de bout en bout."),
    ("doc", "Documents officiels", "Actes de naissance, casiers judiciaires, diplômes et autres documents officiels retirés pour vous."),
    ("shield", "Résultats médicaux", "Récupération discrète de vos résultats d'analyses et documents de santé."),
  ],
  "inclus": ["File d'attente gérée pour vous", "Suivi de l'avancement du dossier", "Traitement confidentiel des pièces"],
  "gallery": [],
 },
 {
  "slug": "shopping", "title": "Shopping & cadeaux", "short": "Shopping", "icon": "gift",
  "img": "img/services/shopping.jpg",
  "tagline": "Le bon article, le beau cadeau — choisis et livrés pour vous.",
  "lead": "Un article précis, une tenue, un objet déco ou un cadeau à offrir ? Décrivez-nous votre envie "
          "et votre budget : nous sélectionnons, nous négocions et nous livrons — emballage cadeau en option.",
  "sub": [
    ("gift", "Articles & vêtements", "Achat d'articles vestimentaires et accessoires selon votre description et votre budget."),
    ("sparkle", "Décoration & maison", "Objets déco, équipement de la maison, trouvailles : on déniche ce qu'il vous faut."),
    ("heart", "Cadeaux & emballage", "Sélection d'un cadeau qui fait plaisir, avec emballage soigné sur demande."),
  ],
  "inclus": ["Conseil & sélection personnalisée", "Tarif prestation 5 000 à 15 000 FCFA selon complexité", "Emballage cadeau possible"],
  "gallery": ["shopping.jpg", "cadeaux.jpg", "shopping-bag.jpg"],
 },
 {
  "slug": "colis", "title": "Dépôt & retrait de colis", "short": "Colis", "icon": "box",
  "img": "img/services/colis.jpg",
  "tagline": "Vos colis acheminés d'un point à un autre, en main propre.",
  "lead": "Un pli, un paquet, un objet à faire parvenir quelque part dans Abidjan ? Mon Commis assure "
          "l'acheminement de vos colis entre deux adresses, en toute sécurité et avec remise en main propre.",
  "sub": [
    ("route", "Acheminement point à point", "Récupération à une adresse, livraison à une autre, au sein des zones couvertes."),
    ("shield", "Remise en main propre", "Votre colis remis à la bonne personne, en toute sécurité."),
    ("check", "Suivi de bout en bout", "Vous êtes informé du retrait jusqu'à la livraison."),
  ],
  "inclus": ["Transport sécurisé", "Remise en main propre", "Frais selon la zone de livraison"],
  "gallery": ["colis.jpg", "colis-2.jpg"],
 },
 {
  "slug": "secretariat", "title": "Secrétariat à distance", "short": "Secrétariat", "icon": "calendar",
  "img": "img/services/secretariat.jpg",
  "tagline": "Votre agenda saisi, rappelé et confirmé — vous ne ratez plus rien.",
  "lead": "Un secrétariat personnel par abonnement mensuel : nous saisissons vos rendez-vous, vous envoyons "
          "le programme de la semaine, vous rappelons avant chaque rendez-vous et confirmons pour vous. "
          "Trois formules — STARTER, CONFORT, PREMIUM — selon votre rythme.",
  "sub": [
    ("calendar", "Gestion d'agenda", "Saisie de vos rendez-vous dans Google Calendar, partagé avec vous, et programme envoyé chaque dimanche."),
    ("bell", "Rappels & confirmations", "Rappel personnalisé 30 min avant chaque rendez-vous ; confirmation téléphonique selon la formule."),
    ("star", "Formules sur-mesure", "STARTER, CONFORT ou PREMIUM : carnet de contacts et recherche d'infos sur les formules supérieures."),
  ],
  "inclus": ["Agenda partagé (Google Calendar)", "Rappels 30 min avant chaque RDV", "Formules dès 15 000 FCFA/mois"],
  "gallery": [],
  "is_secretariat": True,
 },
 {
  "slug": "autres", "title": "Autres services", "short": "Autres", "icon": "grid",
  "img": "img/services/autres.jpg",
  "tagline": "Une tâche particulière ? On la prend en charge, sur-mesure.",
  "lead": "Votre besoin ne rentre dans aucune case ? C'est notre spécialité. Décrivez votre demande : "
          "nous l'organisons à la précision de votre besoin — missions ponctuelles ou récurrentes, "
          "pour particuliers comme pour professionnels.",
  "sub": [
    ("sparkle", "Tâches sur-mesure", "Une demande inhabituelle ? On s'adapte et on trouve la solution."),
    ("clock", "Missions ponctuelles ou récurrentes", "Une fois ou chaque semaine : vous fixez le rythme."),
    ("users", "Particuliers & professionnels", "Un service flexible, calibré à votre budget et à vos contraintes."),
  ],
  "inclus": ["Devis clair en FCFA", "Flexibilité totale", "Interlocuteur unique"],
  "gallery": [],
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

ZONES = [
 ("Zone Standard", "Cocody, Plateau, Marcory, Treichville, Adjamé, Attécoubé", "Inclus dans le tarif de base", "shield"),
 ("Zone Étendue", "Yopougon, Abobo, Bingerville, Anyama, Songon, Dabou, Grand-Bassam", "+ 1 000 à 2 000 FCFA selon distance", "map"),
 ("Zone Spéciale", "Toute destination hors du périmètre ci-dessus", "Sur devis préalable", "route"),
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
 ("courses.jpg", "Courses au marché", "Étal de fruits et légumes frais au marché à Abidjan"),
 ("pharmacie.jpg", "Pharmacie & ordonnances", "Retrait de médicaments et conseils en pharmacie"),
 ("cadeaux.jpg", "Shopping & cadeaux", "Cadeaux soigneusement sélectionnés et emballés"),
 ("marche-2.jpg", "Produits frais choisis avec soin", "Sélection de légumes frais au marché"),
 ("shopping-bag.jpg", "Vos achats, livrés chez vous", "Sacs de shopping prêts à être livrés"),
]

TESTIMONIALS = [
 ("Mon Commis me fait mes courses au marché chaque semaine. Toujours à l'heure, produits bien choisis.", "Aïcha K.", "Cocody"),
 ("Ils ont retiré mes résultats médicaux et déposé un dossier à la CNPS le même jour. Un vrai gain de temps.", "Konan B.", "Plateau"),
 ("La formule Secrétariat CONFORT a changé mon organisation : je ne rate plus aucun rendez-vous.", "Mariam D.", "Marcory"),
]

# ================================================================ STRUCTURE
def head(title, desc, path, page_class, og_type="website", page_type="WebPage"):
    D = SITE["domain"]
    tel = SITE["tel1_href"]
    canonical = D + "/" + (path if path != "index.html" else "")
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
         "inLanguage": "fr-CI", "publisher": {"@id": D + "/#business"}},
        {"@type": page_type, "@id": canonical + "#webpage", "url": canonical, "name": title,
         "description": desc, "isPartOf": {"@id": D + "/#website"}, "about": {"@id": D + "/#business"},
         "inLanguage": "fr-CI"}]},
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
<footer class="site-footer">
  <div class="footer-main">
    <div class="container">
      <div class="footer-top">
        <div class="footer-brand">
          {brand()}
          <p class="footer-desc">Conciergerie & courses à Abidjan. Vos courses, démarches, colis et rendez-vous confiés à un commis de confiance — vous gagnez un temps précieux.</p>
          <p class="footer-tagline">Au cœur d'Abidjan, <span class="nx-script">à votre service.</span></p>
        </div>
        <div class="footer-nav">
          <h4>Nos services</h4>
          {serv_links}
        </div>
        <div class="footer-nav">
          <h4>Mon Commis</h4>
          <a href="services.html">Tous les services</a>
          <a href="secretariat.html">Secrétariat à distance</a>
          <a href="a-propos.html">À propos</a>
          <a href="services.html#zones">Zones de couverture</a>
          <a href="contact.html">Demander un commis</a>
        </div>
        <div class="footer-nav footer-nav-contact">
          <h4>Contact</h4>
          <a class="footer-phone" href="tel:{SITE['tel1_href']}"><span class="footer-phone-ico">{ico('phone')}</span><span class="footer-phone-num">{SITE['tel1_disp']}</span></a>
          <a href="https://wa.me/{SITE['wa']}" target="_blank" rel="noopener noreferrer">{ico('message')} WhatsApp</a>
          <span class="footer-address">{ico('pin')} {SITE['addr']}</span>
          <div class="footer-social">
            <a href="https://wa.me/{SITE['wa']}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp">{SOCIAL['whatsapp']}</a>
            <a href="#" aria-label="TikTok">{SOCIAL['tiktok']}</a>
            <a href="#" aria-label="Instagram">{SOCIAL['instagram']}</a>
            <a href="#" aria-label="Facebook">{SOCIAL['facebook']}</a>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="container footer-bottom-inner">
      <span>&copy; {SITE['year']} {SITE['legal']} — Abidjan, Côte d'Ivoire. Tous droits réservés.</span>
      <a href="contact.html">Demander un commis</a>
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
        <h2 class="section-title">Un seul commis, <span class="nx-mark">tous vos besoins</span></h2>
        <p class="section-copy nx-lead-xl">Mon Commis est votre conciergerie de proximité à Abidjan. Une équipe fiable et discrète prend en charge vos courses, vos démarches et vos rendez-vous — pour vous faire gagner un temps précieux.</p>
        <ul class="nx-list" style="margin-top:18px">
          <li>{ico('check')}<span><strong>Un interlocuteur unique</strong> — du marché à la mairie, une seule équipe pour tout.</span></li>
          <li>{ico('check')}<span><strong>Toutes les communes d'Abidjan</strong> — et au-delà sur devis, jusqu'à Grand-Bassam.</span></li>
          <li>{ico('check')}<span><strong>Sérieux & confidentialité</strong> — documents sensibles, ordonnances et colis traités avec soin.</span></li>
          <li>{ico('check')}<span><strong>Devis clair en FCFA</strong> — sans surprise, paiement espèces ou mobile money.</span></li>
        </ul>
        <div class="nx-hero-cta" style="margin-top:26px">
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

def section_steps():
    cards = ""
    for i, (icn, t, d) in enumerate(STEPS, 1):
        cards += f"""<article class="mc-step reveal">
  <span class="mc-step-num">{i:02d}</span>
  <span class="nx-ico is-navy">{ico(icn)}</span>
  <h3>{t}</h3>
  <p>{d}</p>
</article>
"""
    return f"""<section class="section">
  <div class="container">
    <div class="section-header reveal"><div class="section-heading">
      <span class="nx-eyebrow">Comment ça marche</span>
      <h2 class="section-title">Trois étapes, zéro stress</h2>
    </div></div>
    <div class="nx-grid cols-3 mc-steps">{cards}</div>
  </div>
</section>"""

def section_args():
    cards = "".join(f'<article class="nx-card reveal"><span class="nx-ico is-lime">{ico(i)}</span><h3>{t}</h3><p>{d}</p></article>\n' for i, t, d in ARGS)
    return f"""<section class="section section-soft">
  <div class="container">
    <div class="section-header reveal"><div class="section-heading">
      <span class="nx-eyebrow">Pourquoi Mon Commis</span>
      <h2 class="section-title">Le bon réflexe pour gagner du temps</h2>
    </div></div>
    <div class="nx-grid cols-4">{cards}</div>
  </div>
</section>"""

def section_zones():
    rows = ""
    for nom, communes, frais, icn in ZONES:
        rows += f"""<article class="nx-card reveal">
  <span class="nx-ico is-navy">{ico(icn)}</span>
  <h3>{nom}</h3>
  <p>{communes}</p>
  <p class="nx-zone-fee">{ico('wallet')} <strong>{frais}</strong></p>
</article>
"""
    return f"""<section class="section" id="zones">
  <div class="container">
    <div class="section-header reveal"><div class="section-heading">
      <span class="nx-eyebrow">Zones de couverture</span>
      <h2 class="section-title">De Cocody à Grand-Bassam — et au-delà</h2>
      <p class="section-copy">Nous intervenons dans toutes les communes d'Abidjan. Les frais de déplacement dépendent de la zone.</p>
    </div></div>
    <div class="nx-grid cols-3">{rows}</div>
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
    <div class="nx-grid cols-3 nx-prices">{formules_cards()}</div>
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
    for txt, who, ville in TESTIMONIALS:
        ini = "".join(w[0] for w in who.split()[:2]).upper()
        cards += f'<article class="nx-quote reveal"><p>« {txt} »</p><div class="nx-quote-by"><span class="nx-avatar">{ini}</span><div><strong>{who}</strong><br><span>{ville}</span></div></div></article>\n'
    return f"""<section class="section section-soft">
  <div class="container">
    <div class="section-header reveal"><div class="section-heading">
      <span class="nx-eyebrow">Ils nous font confiance</span>
      <h2 class="section-title">La satisfaction, notre meilleure référence</h2>
    </div></div>
    <div class="nx-grid cols-3">{cards}</div>
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
    rows = [
        ("Tarif de base (commission)", "Selon grille tarifaire communiquée au client", "wallet"),
        ("Supplément urgence", "+50 % du tarif de base (intervention dans l'heure)", "bolt"),
        ("Shopping (prestation)", "5 000 à 15 000 FCFA selon la complexité des achats", "gift"),
        ("Collecte de documents", "Prestation complémentaire, facturée séparément", "doc"),
    ]
    cards = "".join(f'<article class="nx-card reveal"><span class="nx-ico is-lime">{ico(i)}</span><h3>{t}</h3><p>{d}</p></article>\n' for t, d, i in rows)
    return f"""<section class="section section-soft" id="tarifs">
  <div class="container">
    <div class="section-header reveal"><div class="section-heading">
      <span class="nx-eyebrow">Tarifs & paiement</span>
      <h2 class="section-title">Des tarifs clairs, sans surprise</h2>
      <p class="section-copy">Les frais de commission sont réglés avant le début de chaque mission. Paiement en espèces, mobile money (Orange, MTN, Moov, Wave) ou virement.</p>
    </div></div>
    <div class="nx-grid cols-4">{cards}</div>
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
        <a class="btn-lime" href="contact.html">{ico('send')} Demander ce service</a>
        <a class="btn-secondary btn-on-dark" href="https://wa.me/{SITE['wa']}" target="_blank" rel="noopener noreferrer">{ico('message')} WhatsApp</a>
      </div>
    </div>
  </div>
</section>"""

# =================================================================== PAGES
def build_index():
    body = (hero()
            + section_intro()
            + section_services()
            + section_steps()
            + section_args()
            + section_gallery()
            + section_formules(compact=True)
            + section_zones()
            + section_testimonials()
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
        f'<article class="nx-card reveal"><span class="nx-ico is-lime">{ico(ic)}</span><h3>{t}</h3><p>{d}</p></article>\n'
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
            + contact_section(title=f"Demander : {s['title']}"))
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
    <div class="nx-grid cols-4">{vals}</div>
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
             ("a-propos.html", "0.7", "monthly"), ("contact.html", "0.8", "monthly")]
    pages += [(s["url"], "0.8", "monthly") for s in SERVICES]   # inclut secretariat.html
    items = ""
    for p, prio, freq in pages:
        loc = SITE["domain"] + "/" + (p if p != "index.html" else "")
        items += f"  <url><loc>{loc}</loc><changefreq>{freq}</changefreq><priority>{prio}</priority></url>\n"
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}</urlset>\n'

def build_llms():
    D = SITE["domain"]
    serv = "\n".join(f"- [{s['title']}]({D}/{s['url']}) : {s['tagline']}" for s in SERVICES)
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

## Pages clés
- [Accueil]({D}/)
- [Services]({D}/services.html)
- [Secrétariat à distance]({D}/secretariat.html)
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
    write("contact.html", build_contact())
    write("404.html", build_404())
    write("robots.txt", build_robots())
    write("sitemap.xml", build_sitemap())
    write("llms.txt", build_llms())
    write("site.webmanifest", build_manifest())
    print("Terminé.")

if __name__ == "__main__":
    main()
