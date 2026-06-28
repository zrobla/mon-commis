"""Back-office MON COMMIS — admin Django pour le pilotage des prestations."""
from django.contrib import admin
from django.utils.html import format_html
from .models import (Zone, Client, Commis, Mission, FormuleSecretariat,
                     Souscription, Paiement)

admin.site.site_header = "MON COMMIS — Gestion"
admin.site.site_title = "MON COMMIS"
admin.site.index_title = "Pilotage des prestations"

_STATUT_COLORS = {
    "nouvelle": "#2bb4dd", "qualifiee": "#7a5cff", "affectee": "#e0a32f",
    "en_cours": "#1f9ec4", "livree": "#27a062", "cloturee": "#5b6b7b", "annulee": "#d04545",
}


class PaiementInline(admin.TabularInline):
    model = Paiement
    extra = 0
    fields = ("montant", "mode", "statut", "date")


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ("reference", "nom_affiche", "type_service", "zone", "statut_badge",
                    "commis", "urgence", "total", "canal", "cree_le")
    list_filter = ("statut", "type_service", "canal", "urgence", "zone", "mode_paiement")
    search_fields = ("reference", "contact_nom", "contact_tel", "client__nom",
                     "client__telephone", "description")
    list_select_related = ("client", "zone", "commis")
    autocomplete_fields = ("client", "commis", "zone")
    date_hierarchy = "cree_le"
    inlines = [PaiementInline]
    readonly_fields = ("uuid", "reference", "supplement_urgence", "cree_le", "maj_le")
    list_per_page = 30
    actions = ("marquer_qualifiee", "marquer_affectee", "marquer_en_cours",
               "marquer_livree", "marquer_cloturee")
    fieldsets = (
        ("Demande", {"fields": ("reference", "canal", "statut",
                                ("client",), ("contact_nom", "contact_tel", "contact_email"))}),
        ("Prestation", {"fields": ("type_service", "description", "zone",
                                   ("adresse_retrait", "adresse_livraison"),
                                   ("creneau", "urgence"), "commis")}),
        ("Tarification (FCFA)", {"fields": (("tarif_base", "frais_deplacement", "supplement_urgence"),
                                            ("total", "mode_paiement", "paye_avant_mission"))}),
        ("Suivi", {"fields": ("notes", ("cree_le", "maj_le"), "uuid")}),
    )

    @admin.display(description="Statut", ordering="statut")
    def statut_badge(self, obj):
        color = _STATUT_COLORS.get(obj.statut, "#5b6b7b")
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 9px;border-radius:999px;'
            'font-size:11px;font-weight:700;white-space:nowrap">{}</span>',
            color, obj.get_statut_display())

    def _set_statut(self, request, queryset, statut, label):
        n = queryset.update(statut=statut)
        self.message_user(request, f"{n} mission(s) → {label}.")

    @admin.action(description="→ Qualifiée")
    def marquer_qualifiee(self, request, qs): self._set_statut(request, qs, Mission.Statut.QUALIFIEE, "Qualifiée")
    @admin.action(description="→ Affectée")
    def marquer_affectee(self, request, qs): self._set_statut(request, qs, Mission.Statut.AFFECTEE, "Affectée")
    @admin.action(description="→ En cours")
    def marquer_en_cours(self, request, qs): self._set_statut(request, qs, Mission.Statut.EN_COURS, "En cours")
    @admin.action(description="→ Livrée")
    def marquer_livree(self, request, qs): self._set_statut(request, qs, Mission.Statut.LIVREE, "Livrée")
    @admin.action(description="→ Clôturée")
    def marquer_cloturee(self, request, qs): self._set_statut(request, qs, Mission.Statut.CLOTUREE, "Clôturée")


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("nom", "telephone", "commune", "type_client", "cree_le")
    list_filter = ("type_client", "commune")
    search_fields = ("nom", "telephone", "email")


@admin.register(Commis)
class CommisAdmin(admin.ModelAdmin):
    list_display = ("nom", "telephone", "zones", "disponible", "actif")
    list_filter = ("disponible", "actif")
    search_fields = ("nom", "telephone")


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ("__str__", "communes", "frais")
    search_fields = ("communes",)


@admin.register(FormuleSecretariat)
class FormuleAdmin(admin.ModelAdmin):
    list_display = ("nom", "prix_mensuel", "rdv_label", "confirmation_tel",
                    "gestion_contacts", "recherche_infos", "ordre")
    list_editable = ("prix_mensuel", "ordre")
    search_fields = ("nom",)


@admin.register(Souscription)
class SouscriptionAdmin(admin.ModelAdmin):
    list_display = ("client", "formule", "debut", "fin", "statut")
    list_filter = ("statut", "formule")
    search_fields = ("client__nom", "client__telephone")
    autocomplete_fields = ("client", "formule")
    inlines = [PaiementInline]


@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ("__str__", "statut", "mission", "souscription", "date")
    list_filter = ("statut", "mode")
