from django.db import models


class GenderChoices(models.TextChoices):
    MALE = 'male'
    FEMALE = 'female'
    OTHERS = 'others'


class ItemChoices(models.TextChoices):
    APPROVED = 'approved'
    REJECT = 'reject'
    PENDING = 'pending'
