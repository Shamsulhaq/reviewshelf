from django.contrib import admin


from .models import Item, ItemsFiles, Review


class ItemFileAdmin(admin.StackedInline):
    model = ItemsFiles


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [ItemFileAdmin]

    class Meta:
        model = Item


admin.site.register(Review)