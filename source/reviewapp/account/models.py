from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models

# Create your models here.
from reviewapp.account.manager import UserManager
from reviewapp.core.utils import GenderChoices


class BalanceHistory(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
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
    user = models.CharField(
        max_length=255,
        blank=True, null=True,
        verbose_name="User name",
        help_text="for which User"
    )

    # Generic Foreignkey Configuration. DO NOT CHANGE
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()



class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, unique=True, blank=True)
    photo = models.FileField(upload_to='users', blank=True, null=True)
    gender = models.CharField(max_length=8, choices=GenderChoices.choices, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=
                            "Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(_('phone number'), validators=[phone_regex],
                             max_length=15, unique=True, blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    activation_token = models.UUIDField(blank=True, null=True)
    balance = models.DecimalField(max_digits=9, decimal_places=0, default=0)
    bio = models.TextField(blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()
    balance_history = GenericRelation(BalanceHistory)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        new = False
        if self.pk is None:
            new = True
        super(User, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.get_full_name() + ": " + str(self.phone)

    def get_full_name(self):
        return self.first_name +" "+ self.last_name

    def get_short_name(self):
        "Returns the short name for the user."
        return self.last_name

    def get_absolute_update_url(self):
        return reverse("update_account", kwargs={"pk": self.pk})

    @property
    def is_admin_user(self):
        return self.is_staff or self.is_admin

    @property
    def is_email_verified(self):
        return not self.is_verified

    def verified(self):
        if not self.is_verified:
            self.is_verified = True
            self.save()

    # def send_sign_up_email(self):
    #     self.activation_token = uuid.uuid4()
    #     self.save()
    #     subject = "Review shelf Email Verification"
    #     body = """
    #         <html>
    #         <head></head>
    #         <body>
    #         <p>Dear {0}</p>
    #         <p>Welcome to Review shelf Family</p>
    #         <p>Please verify your email by clicking on the below link</p>
    #         <p><a href='{1}'>Click here to verify.</a></p>
    #         </body>
    #         </html>
    #         """.format(self.get_full_name(), f"{settings.EMAIL_DOMAIN}/api/users/verify/{self.activation_token}/")
    #     # print(body)
    #     send_mail(subject, body, self.email)


