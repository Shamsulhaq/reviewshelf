from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from .models import Item ,ItemsFiles
from ..core.utils import ItemChoices


class ProductDetailsView(DetailView):
    template_name = 'product_details.html'
    model = Item

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailsView, self).get_context_data(*args, **kwargs)
        context['related_post'] = Item.objects.filter(status=ItemChoices.APPROVED, category=self.object.category)
        context['item_images'] = ItemsFiles.objects.filter(item=self.object)
        return context