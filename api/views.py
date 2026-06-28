"""API publique MON COMMIS — réception des demandes du formulaire vitrine."""
import json
import time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from gestion.models import Mission, Zone

# Anti-spam mémoire simple : 1 IP -> timestamp dernière requête (fenêtre courte).
_LAST_HIT = {}
_MIN_INTERVAL = 8  # secondes entre deux envois d'une même IP

# Map libellé du select vitrine (6 grandes lignes) -> code Service du modèle.
_SERVICE_MAP = {
    "Courses": Mission.Service.MARCHE,
    "Démarches administratives": Mission.Service.DEMARCHES,
    "Shopping & cadeaux": Mission.Service.SHOPPING,
    "Dépôt & retrait de colis": Mission.Service.COLIS,
    "Secrétariat à distance": Mission.Service.SECRETARIAT,
    "Autres services": Mission.Service.AUTRE,
}
_ZONE_MAP = {"Zone Standard": "standard", "Zone Étendue": "etendue", "Zone Spéciale": "speciale"}


def _client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    return xff.split(",")[0].strip() if xff else request.META.get("REMOTE_ADDR", "")


@csrf_exempt
@require_POST
def demandes(request):
    # Throttle basique par IP
    ip = _client_ip(request)
    now = time.time()
    if now - _LAST_HIT.get(ip, 0) < _MIN_INTERVAL:
        return JsonResponse({"ok": False, "error": "Trop de requêtes, réessayez dans un instant."}, status=429)

    try:
        data = json.loads(request.body or "{}")
    except (ValueError, TypeError):
        return JsonResponse({"ok": False, "error": "Données invalides."}, status=400)

    # Honeypot optionnel : si rempli, on ignore silencieusement (bot).
    if data.get("website"):
        return JsonResponse({"ok": True})

    nom = (data.get("nom") or "").strip()
    tel = (data.get("telephone") or "").strip()
    if not nom or not tel:
        return JsonResponse({"ok": False, "error": "Nom et téléphone requis."}, status=400)

    service_label = (data.get("service") or "").strip()
    type_service = _SERVICE_MAP.get(service_label, Mission.Service.AUTRE)

    echeance = (data.get("echeance") or "").strip()
    urgence = "urgent" in echeance.lower()

    # Construit une description lisible pour la promotrice.
    parts = []
    if data.get("message"):
        parts.append(data["message"].strip())
    if echeance:
        parts.append(f"Quand : {echeance}")
    if service_label:
        parts.append(f"Service demandé : {service_label}")
    if data.get("email"):
        parts.append(f"Email : {data['email'].strip()}")
    description = "\n".join(parts)

    zone = None
    zone_code = _ZONE_MAP.get((data.get("zone") or "").strip())
    if zone_code:
        zone = Zone.objects.filter(code=zone_code).first()

    Mission.objects.create(
        contact_nom=nom,
        contact_tel=tel,
        contact_email=(data.get("email") or "").strip(),
        type_service=type_service,
        description=description,
        zone=zone,
        creneau=echeance,
        urgence=urgence,
        canal=Mission.Canal.FORMULAIRE,
        statut=Mission.Statut.NOUVELLE,
    )
    _LAST_HIT[ip] = now
    return JsonResponse({"ok": True, "message": "Demande reçue. Mon Commis vous recontacte rapidement."})
