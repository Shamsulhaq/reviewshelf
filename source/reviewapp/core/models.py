from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .utils import unique_slug_generator


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


def upload_brand_path(instance, filename):
    return 'brand/{0}'.format(instance.name)


class Brand(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to="brands", blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name


def upload_category_path(instance, filename):
    return 'categories/{0}'.format(instance.name)


class Category(BaseModel):
    name = models.CharField(max_length=120)
    cover = models.ImageField(upload_to="categories", blank=True, null=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name

    class Meta:
        db_table = "categories"
        verbose_name = "category"
        verbose_name_plural = "categories"


@receiver(pre_save, sender=Category)
def category_pre_save(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


@receiver(pre_save, sender=Brand)
def brand_pre_save(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)