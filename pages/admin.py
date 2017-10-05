from django.contrib import admin

from pages.models import Vacancie, Product, PurchasesPrice

# Register your models here.

admin.site.register(Vacancie)
admin.site.register(Product)
admin.site.register(PurchasesPrice)