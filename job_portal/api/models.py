from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.conf import settings


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True, null=False)
    is_employer = models.BooleanField(default=False)
    username = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "is_employer"]

    def save(self, *args ,**kwargs):
        super().save(*args, **kwargs)

        if self.is_employer:
            group = Group.objects.get_or_create(name="Employers")[0]
        else:
            group = Group.objects.get_or_create(name="JobSeekers")[0]
        
        self.groups.add(group)

    def __str__(self) -> str:
        return f"Name: {self.first_name} {self.last_name}, Email: {self.email}"
    
    def create_superuser(first_name, last_name, email, password, is_employer):
        if User.objects.filter(email=email).exists():
            print(f"Superuser with email '{email}' already exists.")
            return None

        superuser = User.objects.create_superuser(
            first_name=first_name, last_name=last_name, email=email, password=password, is_employer=is_employer)
        print(f"Superuser '{email}' created successfully!")

    
class Job(models.Model):
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posted_jobs"
    )
    title = models.CharField()
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
    time_applied = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Job Title: {self.job.title}, Applicant: {self.applicant}"



