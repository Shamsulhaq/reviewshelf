from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


# Create your models here.
from reviewapp.account.models import User


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UnitOfHistory(BaseModel):
    title = models.CharField(
        max_length=255,
        blank=True, null=True,
        verbose_name="Name of Content",
        help_text="The name of the content from which this unit of history is generated"
    )
    description = models.CharField(
        max_length=255,
        blank=True, null=True,
        verbose_name="Description of Content",
        help_text="From where this unit of history is generated"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="history"
    )

    # Generic Foreignkey Configuration. DO NOT CHANGE
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


def upload_brand_path(instance, filename):
    return 'brand/{0}'.format(instance.name)


class Brand(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to="brands", blank=True, null=True)

    def __str__(self):
        return self.name


def upload_category_path(instance, filename):
    return 'categories/{0}'.format(instance.name)


class Category(BaseModel):
    name = models.CharField(max_length=120)
    cover = models.ImageField(upload_to="categories", blank=True, null=True)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "categories"
        verbose_name = "category"
        verbose_name_plural = "categories"