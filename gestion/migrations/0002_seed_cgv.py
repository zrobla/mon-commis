"""Préremplissage des données de la CGV Mon Commis : zones + formules Secrétariat."""
from django.db import migrations


ZONES = [
    ("standard", "Cocody, Plateau, Marcory, Treichville, Adjamé, Attécoubé", "Inclus dans le tarif de base"),
    ("etendue", "Yopougon, Abobo, Bingerville, Anyama, Songon, Dabou, Grand-Bassam", "+ 1 000 à 2 000 FCFA selon distance"),
    ("speciale", "Toute destination hors du périmètre standard/étendu", "Sur devis préalable"),
]

# (nom, prix, rdv_max, recap, rappels, confirmation_tel, gestion_contacts, recherche_infos, ordre)
FORMULES = [
    ("STARTER", 15000, 8,  True, True, False, False, False, 1),
    ("CONFORT", 25000, 20, True, True, True,  False, False, 2),
    ("PREMIUM", 50000, None, True, True, True, True, True, 3),
]


def seed(apps, schema_editor):
    Zone = apps.get_model("gestion", "Zone")
    Formule = apps.get_model("gestion", "FormuleSecretariat")
    for code, communes, frais in ZONES:
        Zone.objects.get_or_create(code=code, defaults={"communes": communes, "frais": frais})
    for nom, prix, rdv, rec, rap, conf, gest, rech, ordre in FORMULES:
        Formule.objects.get_or_create(nom=nom, defaults={
            "prix_mensuel": prix, "rdv_max_mois": rdv, "recap_dimanche": rec,
            "rappels_30min": rap, "confirmation_tel": conf, "gestion_contacts": gest,
            "recherche_infos": rech, "ordre": ordre,
        })


def unseed(apps, schema_editor):
    apps.get_model("gestion", "Zone").objects.all().delete()
    apps.get_model("gestion", "FormuleSecretariat").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("gestion", "0001_initial")]
    operations = [migrations.RunPython(seed, unseed)]
