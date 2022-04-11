# from django.contrib.auth.hashers import make_password
# from django.core.mail import send_mail
# from django.db import models
# from django.contrib.auth.models import AbstractUser, PermissionsMixin
# from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.validators import UnicodeUsernameValidator
# from django.contrib.auth.mixins import UserPassesTestMixin
# from django.contrib.auth import forms
# from django.contrib import contenttypes, auth
# from django.apps import apps
# from django.contrib.auth import get_user_model, authenticate
# from django.contrib.auth import backends
# from django.core.signals import setting_changed, request_started, request_finished, got_request_exception
# from django.utils import timezone
# from django.utils.translation import gettext_lazy as _
# from django.apps import apps
#
#
# # Create your models here.
# class AlterUserManager(BaseUserManager):
#     use_in_migration = True
#
#     def _create_user(self, username, email, password, first_name, last_name, **extra_fields):
#         """
#         Create and save a user with the given username, email and password.
#         :param username:
#         :param email:
#         :param password:
#         :param extra_fields:
#         :return:
#         """
#         if not (username or email):
#             raise ValueError("The given username must be set")
#         email = self.normalize_email(email)
#         # Lookup the real model class from the global app registry so this
#         # manager method can be used in migrations. This is fine because
#         # managers are by definition working on the real model.
#         GlobalUser = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
#         username = GlobalUser.normalize_username(username)
#         user = self.model(username=username, email=email, password=password, **extra_fields)
#         user.password = make_password(password)
#         user.first_name = first_name.strip()
#         user.last_name = last_name.strip()
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, username, email, password, first_name, last_name, **extra_fields):
#         extra_fields.setdefault("is_staff", False)
#         extra_fields.setdefault("is_superuser", False)
#         return self._create_user(self, username, email, password, first_name, last_name, **extra_fields)
#
#     def create_superuser(self, username, email, password, first_name, last_name, **extra_fields):
#         extra_fields.setdefault("is_staff", False)
#         extra_fields.setdefault("is_superuser", False)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#
#         return self._create_user(self, username, email, password, first_name, last_name, **extra_fields)
#
#     def with_perm(self, perm, is_active=True, include_superusers=True, backend=None, obj=None):
#         if backend is None:
#             backends = auth._get_backends(return_tuples=True)
#             if len(backends) == 1:
#                 backend, _ = backends[0]
#             else:
#                 raise ValueError(
#                     'You have multiple authentication backends configured and '
#                     'therefore must provide the `backend` argument.'
#                 )
#         elif not isinstance(backend, str):
#             raise TypeError(
#                 'backend must be a dotted import path string (got %r).'
#                 % backend
#             )
#         else:
#             backend = auth.load_backend(backend)
#         if hasattr(backend, 'with_perm'):
#             return backend.with_perm(
#                 perm,
#                 is_active=is_active,
#                 include_superusers=include_superusers,
#                 obj=obj,
#             )
#         return self.none()
#
#
# class AlterUser(AbstractBaseUser, PermissionsMixin):
#     username_validator = UnicodeUsernameValidator()
#     username = models.CharField(
#         _('username'),
#         max_length=150,
#         unique=True,
#         help_text=_('Required. 150 characters or fewer. Letters, digits and !/./+/-/_ only.'),
#         validators=[username_validator],
#         error_messages={
#             'unique': _('A user with that username already exists.'),
#         },
#     )
#     first_name = models.CharField(_('first_name'), max_length=150, blank=True)
#     last_name = models.CharField(_('last_name'), max_length=150, blank=True)
#     email = models.EmailField(_('email address'), blank=False)
#     date_of_birth = models.DateField(_('date or birth'), blank=True, null=True)
#     is_staff = models.BooleanField(
#         _('staff status'),
#         default=False,
#         help_text=_('Designates whether the user can log into this admin site.'),
#     )
#     date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
#
#     USERNAME_FIELD = 'username'
#     EMAIL_FIELD = 'email'
#     REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
#     ADDED_FIELDS = ['first_name', 'last_name', 'date_of_birth']
#
#     @classmethod
#     def get_added_fields(cls):
#         try:
#             return cls.ADDED_FIELDS
#         except AttributeError:
#             return []
#
#     def clean(self):
#         for attribute in self.ADDED_FIELDS:
#             setattr(self, attribute, getattr(self, attribute).strip())
#         self.email = self.__class__.objects.normalize_email(self.email)
#         super(AlterUser, self).clean()
#
#     def get_full_name(self):
#         """"
#             Return the first_name plus the last_name, with a space in between.
#         """
#         full_name = '%s %s' % (self.first_name, self.last_name)
#         return full_name.strip()
#
#     def get_short_name(self):
#         """Return the short name for the user."""
#         return self.first_name
#
#     def email_user(self, subject, message, from_email=None, **kwargs):
#         """Send an email to this user."""
#         return send_mail(subject, message, from_email, [self.email], **kwargs)
#
#     objects = AlterUserManager()
#
#     class Meta:
#         verbose_name = _("User")
#         verbose_name_plural = _("Users")
#
#
# class MinorUserManager(BaseUserManager):
#     def create_user(self, email, date_of_birth, password=None):
#         """
#         Creates and saves a user with the given email, date of birth and password.
#         :param email:
#         :param date_of_birth:
#         :param password:
#         :return:
#         """
#         if not email:
#             raise ValueError("Users mus have an email address")
#
#         user = self.model(
#             email=self.normalize_email(email),
#             date_of_birth=date_of_birth,
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, date_of_birth, password=None):
#         """
#         Creates and saves superuser with the given email, date of birth and password.
#         :param email:
#         :param date_of_birth:
#         :param password:
#         :return:
#         """
#         user = self.create_user(
#             email,
#             password=password,
#             date_of_birth=date_of_birth,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user
#
#
# class MinorUser(AbstractBaseUser):
#     email = models.EmailField(
#         verbose_name='email adress',
#         max_length=255,
#         unique=True,
#     )
#     date_of_birth = models.DateField()
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#
#     objects = MinorUserManager()
#
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ['date_of_birth']
#
#     def __str__(self):
#         return self.email
#
#     def has_perm(self, perm, obj=None):
#         """
#         Does the user have a specific permission?
#         simplest possible answer: Yes, always
#         :param perm:
#         :param obj:
#         :return:
#         """
#         return True
#
#     def has_module_perms(self, app_label):
#         """
#         Does the user have the permission to view the app 'app_label'?
#         simplest possible answer: Yes, always
#         :param app_label:
#         :return:
#         """
#         return True
#
#     @property
#     def is_staff(self):
#         """
#         Is the user a member of staff?
#         Simplest possible answer: All admins are staff
#         :return:
#         """
#         return self.is_admin
#
