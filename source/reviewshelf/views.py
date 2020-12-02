from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView,UpdateView,CreateView

from reviewapp.review.models import Item, ItemsFiles

from reviewapp.core.models import Category
from reviewapp.account.models import User, BalanceHistory

from reviewapp.account.forms import UserUpdateForm

from reviewapp.review.permissions_mixin import VerifiedRequiredMixin
from reviewapp.review.forms import ItemCreateForms

from reviewapp.core.utils import ItemChoices


class Index(ListView):
    template_name = 'index.html'
    model = Item

    def get_context_data(self, *args, **kwargs):
        context = super(Index, self).get_context_data(*args, **kwargs)
        context['category'] = Category.objects.filter(parent_category=None)
        context['sliders'] = Item.objects.filter(status=ItemChoices.APPROVED).order_by('review_count' and 'review')[:3]
        return context

    def get_queryset(self):
        return Item.objects.filter(status=ItemChoices.APPROVED)


class MyAccount(LoginRequiredMixin, ListView):
    template_name = 'my_Account/home.html'
    model = User

    def get_context_data(self, *args, **kwargs):
        context = super(MyAccount, self).get_context_data(*args, **kwargs)
        context['user'] = User.objects.get(pk=self.request.user.pk)
        return context

    def get_login_url(self):
        return reverse('login')


class MyAccountUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'my_Account/profile_update.html'
    model = User
    form_class = UserUpdateForm

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('my_account')


class BalanceHistoryView(LoginRequiredMixin, ListView):
    template_name = 'my_Account/balance_history.html'
    model = BalanceHistory

    def get_context_data(self, *args, **kwargs):
        context = super(BalanceHistoryView, self).get_context_data(*args, **kwargs)
        context['user'] = User.objects.get(pk=self.request.user.pk)
        context['history'] = BalanceHistory.objects.filter(user=self.request.user.pk).order_by('-created')
        return context

    def get_login_url(self):
        return reverse('login')


class ItemCreateView(LoginRequiredMixin, VerifiedRequiredMixin, CreateView):
    template_name = 'my_Account/item_create.html'
    form_class = ItemCreateForms

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.creat_by = self.request.user
        instance.save()
        for file in self.request.FILES.getlist('images'):
            ItemsFiles.objects.create(media=file, item=instance)
        return super().form_valid(form)

    def get_login_url(self):
        return reverse('login')

    def get_success_url(self):
        return reverse('item_list')


def load_sub_category(request):
    category_id = request.GET.get('category')
    sub_category = Category.objects.filter(parent_category=category_id).order_by('name')
    return render(request, 'ajax/sub_category_dropdown_list_options.html', {'sub_category': sub_category})


class AllItems(LoginRequiredMixin, ListView):
    template_name = 'my_Account/items_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Item.objects.filter(creat_by=self.request.user)




