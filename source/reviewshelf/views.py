from django.views.generic import ListView

from reviewapp.review.models import Item

from reviewapp.core.models import Category


class Index(ListView):
    template_name = 'index.html'
    model = Item

    def get_context_data(self, *args, **kwargs):
        context = super(Index, self).get_context_data(*args, **kwargs)
        context['category'] = Category.objects.filter(parent_category=None)
        return context