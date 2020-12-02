from django import forms
from django.contrib import messages
from .models import Item
from ..core.models import Category


class ItemCreateForms(forms.ModelForm):
    images = forms.FileField(required=False,label='More Images', widget=forms.ClearableFileInput(attrs={'multiple': True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(parent_category=None)
        self.fields['sub_category'].queryset = Category.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['sub_category'].queryset = Category.objects.filter(parent_category=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['sub_category'].queryset = self.instance.country.city_set.order_by('name')

    class Meta:
        model = Item
        fields = (
            'title',
            'brand',
            'category',
            'sub_category',
            'descriptions',
            'price',
            'image',
        )