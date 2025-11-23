from django.contrib import admin, messages
from django.shortcuts import redirect, render
from django.urls import path

from apps.cards.admin_actions.send_cards_to_telegram import send_selected_cards_to_telegram
from apps.cards.forms import ExcelImportForm
from apps.cards.models import Card
from apps.cards.utils.card_format import card_mask, card_number_validate
from apps.cards.utils.import_cards import import_cards_from_excel
from apps.cards.utils.phone_format import phone_masK, normalize_phone_number


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = [
        "masked_card",
        "masked_phone",
        "balance",
        "expire",
        "card_status",
    ]
    list_display_links = list_display
    list_filter = ("card_status", "card_number", "phone_number")
    change_list_template = "cards/card_change_list.html"
    readonly_fields = ("card_status",)
    actions = [send_selected_cards_to_telegram]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.only("card_number", "phone_number", "balance", "expire", "card_status")

    @admin.display(description="Card number")
    def masked_card(self, obj):
        return card_mask(obj.card_number)

    @admin.display(description="Phone Number")
    def masked_phone(self, obj):
        return phone_masK(obj.phone_number)

    def save_model(self, request, obj, form, change):
        obj.card_number = card_number_validate(obj.card_number)
        obj.phone_number = normalize_phone_number(obj.phone_number)
        super().save_model(request, obj, form, change)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("import/", self.admin_site.admin_view(self.import_view), name="card_import"),
        ]
        return custom_urls + urls

    def import_view(self, request):
        if request.method == "POST":
            form = ExcelImportForm(request.POST, request.FILES)
            if form.is_valid():
                result = import_cards_from_excel(request.FILES["excel_file"])
                messages.success(
                    request,
                    f"✅ {result['created']} ta yangi karta, 🔁 {result['updated']} ta yangilangan."
                    f" ❌ {len(result['errors'])} ta xatolik."
                )
                for error in result['errors']:
                    messages.error(request, error)
                return redirect("..")
        else:
            form = ExcelImportForm()

        return render(request, "cards/import_card.html", {"form": form})

