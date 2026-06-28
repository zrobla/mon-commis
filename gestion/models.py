"""
Modèles métier MON COMMIS — conciergerie & courses (Abidjan).
Deux pôles (source : CGV Mon Commis) :
  • Pôle Commissionnaire  -> Mission (facturée à l'acte : grille + zone + urgence)
  • Pôle Secrétariat       -> FormuleSecretariat + Souscription (abonnement mensuel)
"""
import uuid
from django.db import models
from django.utils import timezone


class Zone(models.Model):
    """Zone de couverture et frais de déplacement (CGV §1.3)."""
    STANDARD, ETENDUE, SPECIALE = "standard", "etendue", "speciale"
    TYPE_CHOICES = [
        (STANDARD, "Zone Standard"),
        (ETENDUE, "Zone Étendue"),
        (SPECIALE, "Zone Spéciale"),
    ]
    code = models.CharField("Type de zone", max_length=20, choices=TYPE_CHOICES, unique=True)
    communes = models.CharField("Communes concernées", max_length=255, blank=True)
    frais = models.CharField("Frais de déplacement", max_length=120, blank=True,
                             help_text="Ex. : « Inclus », « + 1 000 à 2 000 FCFA », « Sur devis ».")

    class Meta:
        verbose_name = "Zone de couverture"
        verbose_name_plural = "Zones de couverture"

    def __str__(self):
        return self.get_code_display()


class Client(models.Model):
    PARTICULIER, PRO = "particulier", "pro"
    TYPE_CHOICES = [(PARTICULIER, "Particulier"), (PRO, "Entreprise / Pro")]

    nom = models.CharField("Nom complet", max_length=120)
    telephone = models.CharField("Téléphone / WhatsApp", max_length=30)
    email = models.EmailField("Email", blank=True)
    commune = models.CharField("Commune", max_length=80, blank=True)
    type_client = models.CharField("Type", max_length=20, choices=TYPE_CHOICES, default=PARTICULIER)
    notes = models.TextField("Notes internes", blank=True)
    cree_le = models.DateTimeField("Créé le", auto_now_add=True)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"
        ordering = ["nom"]

    def __str__(self):
        return f"{self.nom} ({self.telephone})"


class Commis(models.Model):
    """Coursier / commis qui exécute les missions."""
    nom = models.CharField("Nom complet", max_length=120)
    telephone = models.CharField("Téléphone", max_length=30)
    zones = models.CharField("Zones couvertes", max_length=255, blank=True)
    disponible = models.BooleanField("Disponible", default=True)
    actif = models.BooleanField("Actif", default=True)
    cree_le = models.DateTimeField("Ajouté le", auto_now_add=True)

    class Meta:
        verbose_name = "Commis"
        verbose_name_plural = "Commis"
        ordering = ["nom"]

    def __str__(self):
        return self.nom


class Mission(models.Model):
    """Demande de prestation du Pôle Commissionnaire (cœur du système)."""

    class Service(models.TextChoices):
        MARCHE = "courses_marche", "Courses au marché"
        PHARMACIE = "pharmacie", "Pharmacie & ordonnances"
        DEMARCHES = "demarches", "Démarches administratives"
        SHOPPING = "shopping", "Shopping & cadeaux"
        COLIS = "colis", "Dépôt & retrait de colis"
        DOCUMENTS = "documents", "Retrait de documents"
        SECRETARIAT = "secretariat", "Secrétariat à distance"
        AUTRE = "autre", "Autre / sur-mesure"

    class Canal(models.TextChoices):
        WHATSAPP = "whatsapp", "WhatsApp"
        FORMULAIRE = "formulaire", "Formulaire site"
        TELEPHONE = "telephone", "Téléphone"

    class Statut(models.TextChoices):
        NOUVELLE = "nouvelle", "Nouvelle"
        QUALIFIEE = "qualifiee", "Qualifiée"
        AFFECTEE = "affectee", "Affectée"
        EN_COURS = "en_cours", "En cours"
        LIVREE = "livree", "Livrée"
        CLOTUREE = "cloturee", "Clôturée"
        ANNULEE = "annulee", "Annulée"

    class Paiement(models.TextChoices):
        ESPECES = "especes", "Espèces"
        MOBILE = "mobile_money", "Mobile money (Orange/MTN/Moov/Wave)"
        VIREMENT = "virement", "Virement"

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    reference = models.CharField("Référence", max_length=20, unique=True, blank=True)

    # Demande
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="missions", verbose_name="Client")
    # champs « bruts » utiles quand la demande arrive du formulaire sans client encore créé
    contact_nom = models.CharField("Nom (demande)", max_length=120, blank=True)
    contact_tel = models.CharField("Téléphone (demande)", max_length=30, blank=True)
    contact_email = models.EmailField("Email (demande)", blank=True)

    type_service = models.CharField("Service", max_length=20, choices=Service.choices, default=Service.MARCHE)
    description = models.TextField("Description du besoin", blank=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Zone")
    adresse_retrait = models.CharField("Adresse de retrait", max_length=255, blank=True)
    adresse_livraison = models.CharField("Adresse de livraison", max_length=255, blank=True)
    creneau = models.CharField("Créneau souhaité", max_length=120, blank=True)
    urgence = models.BooleanField("Urgence (+50 %)", default=False)

    canal = models.CharField("Canal", max_length=20, choices=Canal.choices, default=Canal.FORMULAIRE)
    statut = models.CharField("Statut", max_length=20, choices=Statut.choices, default=Statut.NOUVELLE)
    commis = models.ForeignKey(Commis, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="missions", verbose_name="Commis affecté")

    # Tarification (FCFA)
    tarif_base = models.PositiveIntegerField("Tarif de base (FCFA)", default=0)
    frais_deplacement = models.PositiveIntegerField("Frais de déplacement (FCFA)", default=0)
    supplement_urgence = models.PositiveIntegerField("Supplément urgence (FCFA)", default=0)
    total = models.PositiveIntegerField("Total (FCFA)", default=0)
    mode_paiement = models.CharField("Mode de paiement", max_length=20, choices=Paiement.choices,
                                     blank=True)
    paye_avant_mission = models.BooleanField("Réglé avant la mission", default=False,
                                             help_text="Règle CGV : les frais sont réglés avant le début de la mission.")

    notes = models.TextField("Notes internes", blank=True)
    cree_le = models.DateTimeField("Reçue le", auto_now_add=True)
    maj_le = models.DateTimeField("Mise à jour", auto_now=True)

    class Meta:
        verbose_name = "Mission / Demande"
        verbose_name_plural = "Missions / Demandes"
        ordering = ["-cree_le"]

    def __str__(self):
        return f"{self.reference or self.uuid.hex[:8]} — {self.get_type_service_display()}"

    def save(self, *args, **kwargs):
        # Supplément urgence = 50 % du tarif de base (règle CGV).
        self.supplement_urgence = round(self.tarif_base * 0.5) if self.urgence else 0
        if not self.total:
            self.total = self.tarif_base + self.frais_deplacement + self.supplement_urgence
        super().save(*args, **kwargs)
        if not self.reference:
            self.reference = f"MC-{self.cree_le:%y%m}-{self.pk:04d}"
            super().save(update_fields=["reference"])

    @property
    def nom_affiche(self):
        return self.client.nom if self.client else (self.contact_nom or "—")


class FormuleSecretariat(models.Model):
    """Formule d'abonnement du Pôle Secrétariat à Distance (CGV §1.2)."""
    nom = models.CharField("Formule", max_length=40, unique=True)  # STARTER / CONFORT / PREMIUM
    prix_mensuel = models.PositiveIntegerField("Tarif mensuel (FCFA)")
    rdv_max_mois = models.PositiveIntegerField("RDV pris en charge / mois", null=True, blank=True,
                                               help_text="Laisser vide = illimité.")
    recap_dimanche = models.BooleanField("Récapitulatif (dimanche)", default=True)
    rappels_30min = models.BooleanField("Rappels 30 min avant RDV", default=True)
    confirmation_tel = models.BooleanField("Confirmation téléphonique", default=False)
    gestion_contacts = models.BooleanField("Gestion carnet de contacts", default=False)
    recherche_infos = models.BooleanField("Recherche d'infos / tarifs", default=False)
    ordre = models.PositiveSmallIntegerField("Ordre d'affichage", default=0)

    class Meta:
        verbose_name = "Formule Secrétariat"
        verbose_name_plural = "Formules Secrétariat"
        ordering = ["ordre", "prix_mensuel"]

    def __str__(self):
        return f"{self.nom} — {self.prix_mensuel} FCFA/mois"

    @property
    def rdv_label(self):
        return f"Jusqu'à {self.rdv_max_mois} RDV/mois" if self.rdv_max_mois else "RDV illimités"


class Souscription(models.Model):
    class Statut(models.TextChoices):
        ACTIVE = "active", "Active"
        SUSPENDUE = "suspendue", "Suspendue"
        TERMINEE = "terminee", "Terminée"

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="souscriptions",
                               verbose_name="Client")
    formule = models.ForeignKey(FormuleSecretariat, on_delete=models.PROTECT, verbose_name="Formule")
    debut = models.DateField("Début", default=timezone.now)
    fin = models.DateField("Fin", null=True, blank=True)
    statut = models.CharField("Statut", max_length=20, choices=Statut.choices, default=Statut.ACTIVE)
    cree_le = models.DateTimeField("Créée le", auto_now_add=True)

    class Meta:
        verbose_name = "Souscription Secrétariat"
        verbose_name_plural = "Souscriptions Secrétariat"
        ordering = ["-debut"]

    def __str__(self):
        return f"{self.client.nom} — {self.formule.nom}"


class Paiement(models.Model):
    class Mode(models.TextChoices):
        ESPECES = "especes", "Espèces"
        MOBILE = "mobile_money", "Mobile money"
        VIREMENT = "virement", "Virement"

    class Statut(models.TextChoices):
        ATTENTE = "attente", "En attente"
        REGLE = "regle", "Réglé"

    mission = models.ForeignKey(Mission, on_delete=models.CASCADE, null=True, blank=True,
                                related_name="paiements", verbose_name="Mission")
    souscription = models.ForeignKey(Souscription, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name="paiements", verbose_name="Souscription")
    montant = models.PositiveIntegerField("Montant (FCFA)")
    mode = models.CharField("Mode", max_length=20, choices=Mode.choices, default=Mode.ESPECES)
    statut = models.CharField("Statut", max_length=20, choices=Statut.choices, default=Statut.ATTENTE)
    date = models.DateTimeField("Date", default=timezone.now)

    class Meta:
        verbose_name = "Paiement"
        verbose_name_plural = "Paiements"
        ordering = ["-date"]

    def __str__(self):
        return f"{self.montant} FCFA — {self.get_mode_display()}"
