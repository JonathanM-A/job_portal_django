from typing import Any
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, Group, BaseUserManager, PermissionsMixin
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password, is_employer=False):
        if not email:
            raise ValueError("Users must have an email")
        if not first_name or not last_name:
            raise ValueError("Users must have a first name and last name")
        if not password:
            raise ValueError("Users must provide a password")

        validate_password(password)
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            is_employer = is_employer
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password, 
            is_employer= False)
        user.is_admin, user.is_staff, user.is_superuser = True, True, True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True, null=False)
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    is_employer = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default= timezone.now)
    last_login = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_superuser:
            group = Group.objects.get_or_create(name="Admin")[0]
        elif self.is_employer:
            group = Group.objects.get_or_create(name="Employers")[0]
        else:
            group = Group.objects.get_or_create(name="JobSeekers")[0]
        self.groups.add(group)


class Job(models.Model):
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posted_jobs"
    )
    company_name = models.CharField()
    title = models.CharField()
    job_type = models.CharField(default='In Office') # remote, hybrid, in office
    location = models.CharField(default='Accra')
    description = models.TextField()
    time_posted = models.DateField(auto_now_add=True)
    num_applicants = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Application(models.Model):
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications"
    )
    listing = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name="applications"
    )
    cv = models.FileField(upload_to="CVs/")
    status = models.CharField(default="pending")
    time_applied = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Job Title: {self.listing.title}, Applicant: {self.applicant}"
