from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from reviewapp.account.models import User
from reviewapp.core.models import BaseModel, Brand, Category, UnitOfHistory
from reviewapp.core.utils import ItemChoices


class Item(BaseModel):
    creat_by = models.ForeignKey(User, blank=True, related_name='creator', on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=250, unique=True)
    brand = models.ForeignKey(Brand, related_name='item_brand', blank=True, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, related_name='item_category', blank=True, on_delete=models.DO_NOTHING)
    sub_category = models.ForeignKey(Category, related_name='item_sub_category', blank=True,
                                     on_delete=models.DO_NOTHING)
    price = models.DecimalField(default=0, decimal_places=2, max_digits=9)
    image = models.ImageField(upload_to="review_items", blank=True, null=True)
    review = models.DecimalField(default=0, decimal_places=1, max_digits=2)
    review_count = models.DecimalField(default=0, decimal_places=0, max_digits=9)
    likes = models.DecimalField(max_digits=9, decimal_places=0, default=0)
    status = models.CharField(max_length=10, choices=ItemChoices.choices, default=ItemChoices.PENDING)
    approved_by = models.ForeignKey(User, blank=True, related_name='item_approved_by', null=True,
                                    on_delete=models.SET_NULL)
    reject_reason = models.TextField(blank=True, null=True)
    item_history = GenericRelation(UnitOfHistory)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "items"
        ordering = ['-created']

    def creator_bonus_add(self):
        creator = User.objects.get(id=self.creat_by.id)
        if self.status == ItemChoices.APPROVED:
            creator.balance += 10
        elif self.status == ItemChoices.REJECT:
            creator.balance -= 5
        creator.save()

    def review_generate(self):
        print('review generate')
        reviews = Review.objects.filter(item__id=self.id)
        num = reviews.count()
        print(num)
        rate = self.review_count/num
        self.review = rate


class ItemsFiles(BaseModel):
    item = models.ForeignKey(Item, related_name="item_files", on_delete=models.CASCADE)
    media = models.FileField(upload_to='item_file')

    class Meta:
        db_table = "item_files"

    def __str__(self):
        return self.item.title


@receiver(post_save, sender=Item)
def items_post_save(sender, instance, **kwargs):
    instance.creator_bonus_add()


@receiver(pre_save, sender=Item)
def items_pre_save(sender, instance, **kwargs):
    if instance.review_count > 0:
        instance.review_generate()
    if instance.status == ItemChoices.APPROVED:
        instance.reject_reason = ''


class Review(BaseModel):
    item = models.ForeignKey(Item, related_name='review_item',on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, related_name='reviewer', on_delete=models.DO_NOTHING)
    rate = models.DecimalField(max_digits=1, decimal_places=0, default=0)
    comment = models.TextField(blank=True)
    likes = models.DecimalField(max_digits=9, decimal_places=0, default=0)
    status = models.CharField(max_length=10, choices=ItemChoices.choices, default=ItemChoices.PENDING)
    approved_by = models.ForeignKey(User, blank=True, related_name='review_approved_by', null=True,
                                    on_delete=models.SET_NULL)
    reject_reason = models.TextField(blank=True, null=True)
    review_history = GenericRelation(UnitOfHistory)

    def __str__(self):
        return self.item.title

    class Meta:
        db_table = "reviews"
        ordering = ['-created']

    def creator_bonus_add(self):
        print("balance")
        creator = User.objects.get(id=self.user.id)
        creator.balance += 5
        creator.save()

    def review_count(self):
        print("review count")
        item = Item.objects.get(id = self.item.id)
        item.review_count += self.rate
        item.save()


@receiver(post_save, sender=Review)
def items_post_save(sender, instance, **kwargs):
    if instance.status == ItemChoices.APPROVED:
        instance.creator_bonus_add()
        instance.review_count()


